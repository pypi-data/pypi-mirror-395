import datetime
import logging
import random
from contextlib import suppress
from enum import Enum
from typing import List, Set, Dict, Tuple, Any, Iterable

from durations_nlp import Duration
from spotipy import Spotify, SpotifyException

from spotcrates.common import batched, get_all_items, ISO_8601_TIMESTAMP_FORMAT, ZERO_TIMESTAMP, ValueFilter
from spotcrates.filters import FieldName, filter_list, sort_list

config_defaults = {
    "daily_mix_prefix": "Daily Mix",
    "daily_mix_target": "Now",
    "daily_mix_exclude_prefix": "Overplayed",
    "subscriptions_target": "NewSubscriptions",
    "max_age": "3 days",
    "include_zero_timestamps": True,
    "playlists": {},
    "oldest_timestamp": None,
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
    def __init__(self, spotify: Spotify, config: Dict | None = None):
        """Creates an instance of the playlist manipulation class.

        :param spotify: A handle for the initialized SpotiPy client.
        :param config: The configuration for the playlists class.
        """
        self.spotify = spotify
        self.logger = logging.getLogger(__name__)

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

    def append_daily_mix(self, randomize: bool, target_name: str):
        """Combines all of the "daily mix" playlists for the account and removes any
        tracks found in the "exclude" playlists along with any that are already in
        the given target list. Optionally randomizes the remainder before appending to
        (or creating) the target list.

        :param randomize: Whether to randomize the "daily mix" tracks before appending to
        the target list.
        :param target_name: The name of the list to append to or create. The configured
        list at 'daily_mix_target' is used if no name is provided here.
        """
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

            target_list = self.spotify.user_playlist_create(me["id"], daily_mix_target, public=False)

        # user_playlist_add_tracks(user, playlist_id, tracks, position=None)
        if not dailies:
            self.logger.warning(f"No daily mixes found with the prefix '{daily_mix_prefix}'")
            return

        exclude_ids = self._get_excludes(exclude_lists, target_list)

        add_tracks, orig_daily_count = self._fetch_daily_tracks(dailies, exclude_ids)

        self.logger.info(f"{len(add_tracks)} to add from an original count of {orig_daily_count}")
        if add_tracks:
            if randomize:
                random.shuffle(add_tracks)
            self._add_tracks_to_playlist(target_list, add_tracks)
        else:
            self.logger.warning("No daily songs to add")

    def randomize_playlist(self, playlist: Dict[str, Any]) -> PlaylistResult:
        """Randomizes the tracks in the given playlist.

        :param playlist: The name of the playlist to randomize.
        :return: The result of the randomization attempt.
        """
        try:
            playlist_tracks = self._get_playlist_id_tracks(playlist["id"])
            if not playlist_tracks:
                self.logger.warning(f"No tracks found for playlist '{playlist['name']}'")
                return PlaylistResult.FAILURE
            random.shuffle(playlist_tracks)
            self._add_tracks_to_playlist(playlist, playlist_tracks, replace_playlist=True)
            return PlaylistResult.SUCCESS
        except Exception:
            self.logger.warning(f"Problems randomizing playlist '{playlist['name']}'", exc_info=True)
            return PlaylistResult.FAILURE

    def append_recent_subscriptions(self, randomize: bool, target_name: str, playlist_set_filter: ValueFilter | None = None):
        """Adds new tracks from configured lists to the target list. Newness is determined
        based on the configured maximum age, which is 3 days by default.

        :param randomize: Whether to randomize the new tracks before appending them.
        :param target_name: The target list to append to. The configured target list at
          'subscriptions_target' is used if no name is provided here.
        :param playlist_set_filter: A filter to apply to the playlist sets.
        """
        target_list = None
        exclude_lists = []
        if target_name:
            subscriptions_target = target_name
        else:
            subscriptions_target = self.config.get("subscriptions_target")
        exclude_prefix = self.config.get("daily_mix_exclude_prefix")

        if playlist_set_filter is None:
            playlist_set_filter = ValueFilter()

        for playlist in self.get_all_playlists():
            list_name = playlist["name"]
            if list_name:
                if list_name == subscriptions_target:
                    target_list = playlist
                elif list_name.startswith(exclude_prefix):
                    exclude_lists.append(playlist)

        oldest_timestamp = self._get_oldest_timestamp()

        # TODO: Optionally create if it doesn't exist
        if not target_list:
            me = self.spotify.me()

            target_list = self.spotify.user_playlist_create(me["id"], subscriptions_target, public=False)

        excludes = self._get_excludes(exclude_lists, target_list)

        include_zero_timestamps = self.config.get("include_zero_timestamps", False)
        playlist_ids = self._get_subscription_playlist_ids(
            oldest_timestamp, excludes, include_zero_timestamps, playlist_set_filter
        )

        self.logger.info(f"{len(playlist_ids)} subscription tracks to add")

        if randomize:
            playlist_ids = list(playlist_ids)
            random.shuffle(playlist_ids)

        for id_batch in batched(playlist_ids, 100):
            self.logger.debug(f"Batch size: {len(id_batch)}")
            self.spotify.playlist_add_items(target_list["id"], id_batch)

    def _get_oldest_timestamp(self):
        cfg_oldest_timestamp = self.config.get("oldest_timestamp")

        if cfg_oldest_timestamp:
            try:
                return datetime.datetime.strptime(cfg_oldest_timestamp, ISO_8601_TIMESTAMP_FORMAT)
            except Exception:
                self.logger.warning(f"Could not parse oldest_timestamp value {cfg_oldest_timestamp}", exc_info=True)

        max_age = "NO_MAX_AGE"
        try:
            max_age = self.config.get("max_age", "NO_MAX_AGE")

            return datetime.datetime.now() - datetime.timedelta(seconds=Duration(max_age).to_seconds())
        except Exception as e:
            raise PlaylistConfigException(f"Could not parse track age {max_age}", e) from e

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
                list_id = playlist["id"]
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
            new_playlist = self.spotify.user_playlist_create(self.spotify.me()["id"], dest_name, public=False)
            tracks_to_copy = self._get_playlist_name_tracks(source_name)

            if randomize:
                random.shuffle(tracks_to_copy)

            self._add_tracks_to_playlist(new_playlist, tracks_to_copy)
            return PlaylistResult.SUCCESS, dest_name
        except Exception:
            self.logger.warning("Problems copying list", exc_info=True)
            return PlaylistResult.FAILURE, None

    def randomize_owned_playlists(self) -> Dict[str, PlaylistResult]:
        """Randomizes all playlists owned by the current user.

        Returns:
            Dict mapping playlist names to their randomization results
        """
        results = {}
        current_user_id = self.spotify.current_user()["id"]

        for playlist in self.get_all_playlists():
            if playlist["owner"]["id"] == current_user_id:
                results[playlist["name"]] = self.randomize_playlist(playlist)

        return results

    # ===Internal Methods=== #

    def _fetch_daily_tracks(self, dailies: List, exclude_ids: Iterable[str]):
        add_tracks = []
        orig_daily_count = 0
        for daily in dailies:
            daily_items = self._get_playlist_id_tracks(daily["id"])
            orig_daily_count += len(daily_items)
            add_tracks.extend([daily_item for daily_item in daily_items if daily_item["track"]["id"] not in exclude_ids])
        return add_tracks, orig_daily_count

    def _get_subscription_playlist_ids(
        self,
        oldest_timestamp: datetime,
        excluded_ids: Iterable[str],
        include_zero_timestamps: bool,
        playlist_set_filter: ValueFilter,
    ) -> Set[str]:
        target_playlist_ids: Set[str] = set()
        subscription_playlists = self.config.get("playlists")
        if not subscription_playlists:
            self.logger.warning("No subscription playlists defined")
            return target_playlist_ids

        for playlist_set, playlist_ids in subscription_playlists.items():
            self.logger.debug(f"Processing subscription set '{playlist_set}'")
            if playlist_set_filter.exclude(playlist_set):
                self.logger.debug(f"Skipping set '{playlist_set}'")
                continue
            set_playlist_ids = set()
            for track in self._get_playlist_id_tracks(*playlist_ids):
                iso_added = track.get("added_at")
                if iso_added:
                    try:
                        track_timestamp = datetime.datetime.strptime(iso_added, ISO_8601_TIMESTAMP_FORMAT)
                        if self._include_for_added_at(oldest_timestamp, track_timestamp, include_zero_timestamps):
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
            self.logger.debug(f"Found {len(set_playlist_ids)} newer than {oldest_timestamp} in playlist set '{playlist_set}'")
            target_playlist_ids.update(set_playlist_ids)

        self.logger.debug(f"Found a total of {len(target_playlist_ids)} newer than {oldest_timestamp}")
        return target_playlist_ids

    @staticmethod
    def _include_for_added_at(oldest_timestamp: datetime, track_timestamp: datetime, include_zero_timestamps: bool) -> bool:
        if include_zero_timestamps:
            return track_timestamp >= oldest_timestamp or track_timestamp == ZERO_TIMESTAMP
        else:
            return track_timestamp >= oldest_timestamp

    def _get_playlist_track_ids(self, *args: str) -> Set[str]:
        track_ids: Set[str] = set()
        for playlist_id in args:
            playlist_items = self._filter_for_tracks(playlist_id)

            track_ids.update({playlist_item.get("track", {}).get("id") for playlist_item in playlist_items})

        # Remove None in case any IDs failed to resolve
        with suppress(KeyError):
            # noinspection PyTypeChecker
            track_ids.remove(None)  # type: ignore
        return track_ids

    def _get_playlist_names_to_ids(self, lower=False) -> Dict[str, str]:
        name_ids = {}
        for playlist in self.get_all_playlists():
            if lower:
                name_ids[playlist["name"].lower()] = playlist["id"]
            else:
                name_ids[playlist["name"]] = playlist["id"]

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
            filtered_tracks = self._filter_for_tracks(playlist_id)

            tracks.extend(filtered_tracks)

        return tracks

    def _filter_for_tracks(self, playlist_id: str) -> List[dict]:
        try:
            all_tracks = get_all_items(self.spotify, self.spotify.playlist_items(playlist_id))
        except SpotifyException as e:
            if e.http_status == 404:
                self.logger.info(f"Playlist '{playlist_id}' not found")
                return []
            else:
                self.logger.warning(f"Spotify problems getting tracks for playlist '{playlist_id}': {e}")
                return []
        except Exception as e:
            self.logger.warning(f"Problems getting tracks for playlist '{playlist_id}': {e}")
            return []
        filtered_tracks = []
        for cur_track in all_tracks:
            if cur_track.get("track") and cur_track["track"].get("id"):
                filtered_tracks.append(cur_track)
        return filtered_tracks

    def _add_tracks_to_playlist(self, target_list: Dict[str, Any], add_tracks: List, replace_playlist=False):
        track_ids = {add_song["track"]["id"] for add_song in add_tracks}

        first_batch = True
        for id_batch in batched(track_ids, 100):
            if replace_playlist and first_batch:
                self.spotify.playlist_replace_items(target_list["id"], id_batch)
            else:
                self.spotify.playlist_add_items(target_list["id"], id_batch)
            self.logger.debug(f"Batch size: {len(id_batch)}")
            first_batch = False

    def _get_excludes(self, exclude_lists: List[Dict], target_list: Dict):
        exclude_ids = self._get_playlist_track_ids(target_list["id"])
        for exclude_list in exclude_lists:
            exclude_ids.update(self._get_playlist_track_ids(exclude_list["id"]))
        return exclude_ids

    @staticmethod
    def _process_config(config: Dict | None) -> Dict:
        processed_config = {}

        source_config = {}
        if config:
            source_config = config

        for key, default_value in config_defaults.items():
            processed_config[key] = source_config.get(key, default_value)

        return processed_config

    def _get_playlist_names(self, lower=False) -> List[str]:
        if lower:
            return [playlist["name"].lower() for playlist in self.get_all_playlists()]
        else:
            return [playlist["name"] for playlist in self.get_all_playlists()]

    def _create_unique_dest_name(self, source_name: str):
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
