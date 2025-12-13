import datetime
import logging
import random
from contextlib import suppress
from enum import Enum
from typing import List, Set, Dict, Optional, Tuple

from durations_nlp import Duration
from spotipy import Spotify

from spotcrates.common import batched, get_all_items
from spotcrates.filters import FieldName, filter_list, sort_list

ISO_8601_TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

config_defaults = {
    "daily_mix_prefix": "Daily Mix",
    "daily_mix_target": "Now",
    "daily_mix_exclude_prefix": "Overplayed",
    "subscriptions_target": "NewSubscriptions",
    "max_age": "3 days",
    "playlists": {},
}


class PlaylistException(Exception):
    pass


class PlaylistConfigException(PlaylistException):
    pass


class PlaylistNamingException(PlaylistException):
    pass


# True, False, File not found
class PlaylistResult(Enum):
    """Represents the result of a playlist operation."""

    def __init__(self, label):
        self.label = label

    SUCCESS = "Success"
    FAILURE = "Failure"
    NOT_FOUND = "Not Found"


class Playlists:
    def __init__(self, spotify: Spotify, config: Optional[Dict] = None):
        self.spotify = spotify
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        self.config = self._process_config(config)

    def get_all_playlists(self) -> List[Dict]:
        return get_all_items(self.spotify, self.spotify.current_user_playlists())

    def list_all_playlists(self, sort_fields=None, filters=None) -> List[Dict]:
        playlist_entries = []
        for playlist in self.get_all_playlists():
            playlist_entries.append(
                {
                    FieldName.SPOTIFY_ID: playlist["id"],
                    FieldName.PLAYLIST_NAME: playlist["name"],
                    FieldName.SIZE: playlist["tracks"]["total"],
                    FieldName.OWNER: playlist["owner"]["id"],
                    FieldName.PLAYLIST_DESCRIPTION: playlist["description"],
                }
            )

        if not sort_fields and not filters:
            return playlist_entries

        processed_entries = playlist_entries
        if filters:
            processed_entries = filter_list(processed_entries, filters)

        if sort_fields:
            processed_entries = sort_list(processed_entries, sort_fields)

        return processed_entries

    def append_daily_mix(self, randomize, target_name):
        dailies = []
        target_list = None
        exclude_lists = []
        daily_mix_prefix = self.config.get("daily_mix_prefix")
        if target_name:
            daily_mix_target = target_name
        else:
            daily_mix_target = self.config.get("daily_mix_target")
        daily_mix_exclude_prefix = self.config.get("daily_mix_exclude_prefix")
        for playlist in self.get_all_playlists():
            list_name = playlist.get("name")
            if list_name:
                if list_name.startswith(daily_mix_prefix):
                    dailies.append(playlist)
                elif list_name == daily_mix_target:
                    target_list = playlist
                elif list_name.startswith(daily_mix_exclude_prefix):
                    exclude_lists.append(playlist)

        # TODO: Optionally create if it doesn't exist
        if not target_list:
            me = self.spotify.me()

            target_list = self.spotify.user_playlist_create(
                me["id"], daily_mix_target, public=False
            )

        # user_playlist_add_tracks(user, playlist_id, tracks, position=None)
        if not dailies:
            self.logger.warning(
                f"No daily mixes found with the prefix '{daily_mix_prefix}'"
            )
            return

        exclude_ids = self._get_excludes(exclude_lists, target_list)

        add_tracks, orig_daily_count = self._fetch_daily_tracks(dailies, exclude_ids)

        self.logger.info(
            f"{len(add_tracks)} to add from an original count of {orig_daily_count}"
        )
        if add_tracks:
            if randomize:
                random.shuffle(add_tracks)
            self._add_tracks_to_playlist(target_list, add_tracks)
        else:
            self.logger.warning("No daily songs to add")

    def _fetch_daily_tracks(self, dailies, exclude_ids):
        add_tracks = []
        orig_daily_count = 0
        for daily in dailies:
            daily_items = self._get_playlist_id_tracks(daily["id"])
            orig_daily_count += len(daily_items)
            add_tracks.extend(
                [
                    daily_item
                    for daily_item in daily_items
                    if daily_item["track"]["id"] not in exclude_ids
                ]
            )
        return add_tracks, orig_daily_count

    def randomize_playlist(self, playlist) -> PlaylistResult:
        try:
            playlist_tracks = self._get_playlist_id_tracks(playlist["id"])
            random.shuffle(playlist_tracks)
            self._add_tracks_to_playlist(playlist, playlist_tracks, replace_playlist=True)
            return PlaylistResult.SUCCESS
        except Exception:
            self.logger.warning(f"Problems randomizing playlist '{playlist['name']}'", exc_info=True)
            return PlaylistResult.FAILURE

    def append_recent_subscriptions(self, randomize, target_name):
        target_list = None
        exclude_lists = []
        if target_name:
            subscriptions_target = target_name
        else:
            subscriptions_target = self.config.get("subscriptions_target")
        exclude_prefix = self.config.get("daily_mix_exclude_prefix")
        for playlist in self.get_all_playlists():
            list_name = playlist["name"]
            if list_name:
                if list_name == subscriptions_target:
                    target_list = playlist
                elif list_name.startswith(exclude_prefix):
                    exclude_lists.append(playlist)

        max_age = "NO_MAX_AGE"
        try:
            max_age = self.config.get("max_age", "NO_MAX_AGE")

            oldest_timestamp = datetime.datetime.now() - datetime.timedelta(
                seconds=Duration(max_age).to_seconds()
            )
        except Exception as e:
            raise PlaylistConfigException(f"Could not parse track age {max_age}", e)

        # TODO: Optionally create if it doesn't exist
        if not target_list:
            me = self.spotify.me()

            target_list = self.spotify.user_playlist_create(
                me["id"], subscriptions_target, public=False
            )

        excludes = self._get_excludes(exclude_lists, target_list)

        playlist_ids = self._get_subscription_playlist_ids(oldest_timestamp, excludes)

        if randomize:
            playlist_ids = list(playlist_ids)
            random.shuffle(playlist_ids)

        for id_batch in batched(playlist_ids, 100):
            self.logger.debug(f"Batch size: {len(id_batch)}")
            self.spotify.playlist_add_items(target_list["id"], id_batch)

    def _get_subscription_playlist_ids(self, oldest_timestamp, excluded_ids) -> Set[str]:
        target_playlist_ids: Set[str] = set()
        subscription_playlists = self.config.get("playlists")
        if not subscription_playlists:
            self.logger.warning("No subscription playlists defined")
            return target_playlist_ids

        for playlist_set, playlist_ids in subscription_playlists.items():
            self.logger.debug(f"Processing subscription set '{playlist_set}'")
            set_playlist_ids = set()
            for track in self._get_playlist_id_tracks(*playlist_ids):
                iso_added = track.get("added_at")
                if iso_added:
                    try:
                        track_timestamp = datetime.datetime.strptime(
                            iso_added, ISO_8601_TIMESTAMP_FORMAT
                        )
                        if track_timestamp >= oldest_timestamp:
                            track_id = track.get("track", {}).get("id")
                            if track_id and track_id not in excluded_ids:
                                set_playlist_ids.add(track_id)
                    except Exception:
                        self.logger.warning(
                            f"Could not parse timestamp {iso_added}. Skipping track.",
                            exc_info=True,
                        )
                else:
                    logging.debug("No 'added_at' field for track. Skipping.")
            self.logger.debug(
                f"Found {len(set_playlist_ids)} newer than {oldest_timestamp} "
                f"in playlist set '{playlist_set}'"
            )
            target_playlist_ids.update(set_playlist_ids)

        self.logger.debug(
            f"Found a total of {len(target_playlist_ids)} newer than {oldest_timestamp}"
        )
        return target_playlist_ids

    def _get_playlist_track_ids(self, *args: str) -> Set[str]:
        track_ids: Set[str] = set([])
        for playlist_id in args:
            # TODO: See about paring down to just the ID via "fields" param
            playlist_items = get_all_items(
                self.spotify, self.spotify.playlist_items(playlist_id)
            )
            track_ids.update(
                {playlist_item.get("track", {}).get("id") for playlist_item in playlist_items}
            )

        # Remove None in case any IDs failed to resolve
        with suppress(KeyError):
            # noinspection PyTypeChecker
            track_ids.remove(None)  # type: ignore
        return track_ids

    def _get_playlist_names_to_ids(self, lower=False) -> Dict[str, str]:
        name_ids = {}
        for playlist in self.get_all_playlists():
            if lower:
                name_ids[playlist['name'].lower()] = playlist['id']
            else:
                name_ids[playlist['name']] = playlist['id']

        return name_ids

    def _get_playlist_name_tracks(self, *playlist_names: str) -> List[dict]:
        name_id_map = self._get_playlist_names_to_ids(lower=True)
        playlist_ids = []
        for lower_name in [name.lower() for name in playlist_names]:
            playlist_id = name_id_map.get(lower_name)
            if playlist_id:
                playlist_ids.append(playlist_id)
            else:
                self.logger.warning(f"No playlist found for name '{lower_name}'")
        return self._get_playlist_id_tracks(*playlist_ids)

    def _get_playlist_id_tracks(self, *playlist_ids: str) -> List[dict]:
        tracks = []
        for playlist_id in playlist_ids:
            # TODO: See about paring down to just the ID via "fields" param
            tracks.extend(
                get_all_items(self.spotify, self.spotify.playlist_items(playlist_id))
            )

        return tracks

    def _add_tracks_to_playlist(self, target_list, add_tracks, replace_playlist=False):
        track_ids = {add_song["track"]["id"] for add_song in add_tracks}

        first_batch = True
        for id_batch in batched(track_ids, 100):
            if replace_playlist and first_batch:
                self.spotify.playlist_replace_items(target_list["id"], id_batch)
            else:
                self.spotify.playlist_add_items(target_list["id"], id_batch)
            self.logger.debug(f"Batch size: {len(id_batch)}")
            first_batch = False

    def _get_excludes(self, exclude_lists, target_list):
        exclude_ids = self._get_playlist_track_ids(target_list["id"])
        for exclude_list in exclude_lists:
            exclude_ids.update(self._get_playlist_track_ids(exclude_list["id"]))
        return exclude_ids

    @staticmethod
    def _process_config(config: Optional[Dict]) -> Dict:
        processed_config = {}

        source_config = {}
        if config:
            source_config = config

        for key, default_value in config_defaults.items():
            processed_config[key] = source_config.get(key, default_value)

        return processed_config

    def randomize_playlists(self, playlists: List[str]) -> Dict[str, PlaylistResult]:
        """Replaces the tracks in the target lists with a randomized version of the same tracks.

        :param playlists: A list of playlist names and/or IDs.
        :return: The results of the randomizing.
        """

        lower_playlists = [playlist.lower() for playlist in playlists]

        results = {}
        for playlist in self.get_all_playlists():
            list_name = playlist["name"]
            if list_name and list_name.lower() in lower_playlists:
                results[list_name] = self.randomize_playlist(playlist)
            else:
                list_id = playlist['id']
                if list_id in playlists:
                    results[list_id] = self.randomize_playlist(playlist)

        found_targets = results.keys()
        missing_targets = [missing for missing in playlists if missing not in found_targets]
        for missing_target in missing_targets:
            results[missing_target] = PlaylistResult.NOT_FOUND

        return results

    def copy_list(self, arguments: List[str], randomize: bool) -> Tuple[PlaylistResult, str | None]:
        try:
            source_name = arguments[0]
            if len(arguments) < 2:
                dest_name = self._create_unique_dest_name(source_name)
            else:
                dest_name = arguments[1]

            # TODO: make public flag settable
            new_playlist = self.spotify.user_playlist_create(self.spotify.me()['id'], dest_name, public=False)
            tracks_to_copy = self._get_playlist_name_tracks(source_name)

            if randomize:
                random.shuffle(tracks_to_copy)

            self._add_tracks_to_playlist(new_playlist, tracks_to_copy)
            return PlaylistResult.SUCCESS, dest_name
        except Exception:
            self.logger.warning("Problems copying list", exc_info=True)
            return PlaylistResult.FAILURE, None

    def _get_playlist_names(self, lower=False) -> List[str]:
        if lower:
            return [playlist["name"].lower() for playlist in self.get_all_playlists()]
        else:
            return [playlist["name"] for playlist in self.get_all_playlists()]

    def _create_unique_dest_name(self, source_name):
        existing_lists = self._get_playlist_names(lower=True)
        count = 1

        dest_name = f"{source_name}-{count:02d}"

        if dest_name.lower() not in existing_lists:
            return dest_name

        max_count = 99

        while count <= max_count:
            count += 1
            dest_name = f"{source_name}-{count:02d}"

            if dest_name.lower() not in existing_lists:
                return dest_name

        raise PlaylistNamingException(f"Unable to find a unique playlist name (gave up at {dest_name})")
