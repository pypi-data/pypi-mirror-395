import logging
from itertools import islice
from typing import List, Set

from spotipy import Spotify

DAILY_MIX_PREFIX = 'Daily Mix'
DAILY_MIX_TARGET = 'Now'
DAILY_MIX_EXCLUDES = 'Overplayed'


class PlaylistException(Exception):
    pass


def batched(iterable, n):
    "Batch data into lists of length n. The last batch may be shorter."
    # batched('ABCDEFG', 3) --> ABC DEF G
    it = iter(iterable)
    while True:
        batch = list(islice(it, n))
        if not batch:
            return
        yield batch


class Playlists:
    def __init__(self, spotify: Spotify):
        self.spotify = spotify
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

    def get_all_playlists(self) -> dict:
        all_lists = []
        first_page = self.spotify.current_user_playlists()
        all_lists.extend(first_page['items'])

        next_page = self.spotify.next(first_page)
        while next_page:
            all_lists.extend(next_page['items'])
            next_page = self.spotify.next(next_page)

        return all_lists

    def append_daily_mix(self, target_list_name=DAILY_MIX_TARGET, daily_mix_prefix=DAILY_MIX_PREFIX,
                         exclude_list_name=DAILY_MIX_EXCLUDES):
        dailies = []
        target_list = None
        exclude_list = None
        for playlist in self.get_all_playlists():
            list_name = playlist['name']
            if list_name:
                if list_name.startswith(daily_mix_prefix):
                    dailies.append(playlist)
                elif list_name == target_list_name:
                    target_list = playlist
                elif list_name == exclude_list_name:
                    exclude_list = playlist

        # TODO: Optionally create if it doesn't exist
        if not target_list:
            raise PlaylistException(f"Could not find target list '{target_list_name}")

        # user_playlist_add_tracks(user, playlist_id, tracks, position=None)
        if not dailies:
            self.logger.warning(f"No daily mixes found with the prefix '{daily_mix_prefix}'")

        exclude_ids = self._get_playlist_track_ids(target_list["id"])

        if exclude_list:
            exclude_ids.update(self._get_playlist_track_ids(exclude_list["id"]))

        add_tracks = []
        orig_daily_count = 0
        for daily in dailies:
            daily_items = self._get_playlist_tracks(daily["id"])
            orig_daily_count += len(daily_items)
            add_tracks.extend(
                [daily_item for daily_item in daily_items if daily_item['track']['id'] not in exclude_ids])

        self.logger.info(f"{len(add_tracks)} to add from an original count of {orig_daily_count}")
        if add_tracks:
            self._add_tracks_to_playlist(target_list, add_tracks)
        else:
            self.logger.warning("No daily songs to add")

    def _get_playlist_track_ids(self, *args: str) -> Set[str]:
        track_ids = set()
        for playlist_id in args:
            # TODO: See about paring down to just the ID via "fields" param
            playlist_items = self.spotify.playlist_items(playlist_id)

            track_ids.update({playlist_item['track']['id'] for playlist_item in playlist_items['items']})

            next_playlist_page = self.spotify.next(playlist_items)
            while next_playlist_page:
                track_ids.update({playlist_item['track']['id'] for playlist_item in next_playlist_page['items']})
                next_playlist_page = self.spotify.next(next_playlist_page)

        return track_ids

    def _get_playlist_tracks(self, *args: str) -> List[dict]:
        tracks = []
        for playlist_id in args:
            # TODO: See about paring down to just the ID via "fields" param
            playlist_items = self.spotify.playlist_items(playlist_id)
            tracks.extend(playlist_items['items'])

            next_playlist_page = self.spotify.next(playlist_items)
            while next_playlist_page:
                tracks.extend(next_playlist_page['items'])
                next_playlist_page = self.spotify.next(next_playlist_page)

        return tracks

    def _add_tracks_to_playlist(self, target_list, add_tracks):
        track_ids = {add_song['track']['id'] for add_song in add_tracks}

        for id_batch in batched(track_ids, 100):
            self.logger.debug(f"Batch size: {len(id_batch)}")
            self.spotify.playlist_add_items(target_list["id"], id_batch)
