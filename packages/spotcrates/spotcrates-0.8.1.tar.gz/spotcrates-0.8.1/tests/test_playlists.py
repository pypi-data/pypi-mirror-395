import os
import unittest
from unittest.mock import MagicMock, ANY, Mock

from spotcrates.filters import FieldName
from spotcrates.playlists import Playlists, PlaylistResult
from tests.utils import file_json

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
PLAYLIST_LIST = file_json(os.path.join(DATA_DIR, "playlists.json"))
PLAYLIST_NO_DAILY_LIST = file_json(os.path.join(DATA_DIR, "playlists_no_daily.json"))
TRACKS_DAILY1 = file_json(os.path.join(DATA_DIR, "tracks_daily1.json"))
TRACKS_DAILY1_SOME_INVALID = file_json(os.path.join(DATA_DIR, "tracks_daily1_some_invalid.json"))
TRACKS_DAILY1_MINUS_INVALID = file_json(os.path.join(DATA_DIR, "tracks_daily1_minus_invalid.json"))
TRACKS_DAILY1_SOME_EPOCH = file_json(os.path.join(DATA_DIR, "tracks_daily1_some_epoch_tracks.json"))
TRACKS_OVERPLAYED = file_json(os.path.join(DATA_DIR, "tracks_overplayed.json"))
TRACKS_TARGET = file_json(os.path.join(DATA_DIR, "tracks_target.json"))


def get_canned_tracks(*args, **kwargs):
    playlist_id = args[0]
    if playlist_id == "37i9dQZF1E37hnawmowyJn":
        return TRACKS_DAILY1
    elif playlist_id == "0y8aCYE2OsnLzzxtqcDGf8":
        return TRACKS_OVERPLAYED
    elif playlist_id == "1JJB9ICuIoE6aD4jg9vgmV":
        return TRACKS_TARGET
    elif playlist_id == "some_invalid":
        return TRACKS_DAILY1_SOME_INVALID
    elif playlist_id == "minus_invalid":
        return TRACKS_DAILY1_MINUS_INVALID
    elif playlist_id == "some_epoch":
        return TRACKS_DAILY1_SOME_EPOCH
    else:
        raise Exception(f"Unhandled tracks ID {playlist_id}")


# noinspection DuplicatedCode,PyTypeChecker
class DailyAppendTestCase(unittest.TestCase):
    def setUp(self):
        self.spotify = MagicMock()
        self.spotify.next.return_value = None
        self.playlists = Playlists(self.spotify)

    def test_list_all(self):
        self.spotify.current_user_playlists.return_value = {"items": PLAYLIST_LIST}

        playlists = self.playlists.get_all_playlists()

        self.assertEqual(PLAYLIST_LIST, playlists)

    def test_append_daily_mix(self):
        self.spotify.current_user_playlists.return_value = {"items": PLAYLIST_LIST}

        self.spotify.playlist_items.side_effect = get_canned_tracks

        self.playlists.append_daily_mix(randomize=False, target_name=None)

        self.spotify.playlist_add_items.assert_called_with("1JJB9ICuIoE6aD4jg9vgmV", ["3DrlHWCoFqHQYGwE8MWsuv"])

    def test_append_daily_mix_random_target(self):
        self.spotify.current_user_playlists.return_value = {"items": PLAYLIST_LIST}

        self.spotify.me.return_value = {"id": "testuser"}
        self.spotify.user_playlist_create.return_value = {"id": "1JJB9ICuIoE6aD4jg9vgmV"}

        self.spotify.playlist_items.side_effect = get_canned_tracks

        self.playlists.append_daily_mix(randomize=True, target_name="Custom Target")

        self.spotify.playlist_add_items.assert_called_with("1JJB9ICuIoE6aD4jg9vgmV", ["3DrlHWCoFqHQYGwE8MWsuv"])

        self.spotify.user_playlist_create.assert_called_with("testuser", "Custom Target", public=False)

    def test_append_empty_entries(self):
        self.spotify.current_user_playlists.return_value = {"items": [{}, {}, {}]}

        self.spotify.playlist_items.side_effect = get_canned_tracks

        self.playlists.append_daily_mix(randomize=False, target_name=None)

        self.spotify.playlist_add_items.assert_not_called()

    def test_append_daily_mix_missing_target(self):
        self.spotify.current_user_playlists.return_value = {"items": PLAYLIST_LIST}
        self.spotify.me.return_value = {"id": "testuser"}
        self.spotify.user_playlist_create.return_value = {"id": "1JJB9ICuIoE6aD4jg9vgmV"}

        self.spotify.playlist_items.side_effect = get_canned_tracks

        local_playlists = Playlists(self.spotify, {"daily_mix_target": "missing_playlist"})
        local_playlists.append_daily_mix(randomize=False, target_name=None)
        self.spotify.playlist_add_items.assert_called_with("1JJB9ICuIoE6aD4jg9vgmV", ["3DrlHWCoFqHQYGwE8MWsuv"])
        self.spotify.user_playlist_create.assert_called_with("testuser", "missing_playlist", public=False)

    # No dailies
    def test_append_daily_mix_no_dailies(self):
        self.spotify.current_user_playlists.return_value = {"items": PLAYLIST_NO_DAILY_LIST}

        self.spotify.playlist_items.side_effect = get_canned_tracks

        self.playlists.append_daily_mix(randomize=False, target_name=None)

        self.spotify.playlist_add_items.assert_not_called()

    # Paged tracks

    def test_append_daily_mix_paged(self):
        self.spotify.current_user_playlists.return_value = {"items": PLAYLIST_LIST}

        self.spotify.playlist_items.side_effect = get_canned_tracks

        def get_next_page(*args, **kwargs):
            page = args[0]
            if page == TRACKS_TARGET:
                return TRACKS_DAILY1
            else:
                return None

        self.spotify.next.side_effect = get_next_page

        self.playlists.append_daily_mix(randomize=False, target_name=None)

        self.spotify.playlist_add_items.assert_not_called()

    def test_append_daily_mix_paged_tracks(self):
        self.spotify.current_user_playlists.return_value = {"items": PLAYLIST_LIST}

        self.spotify.playlist_items.side_effect = get_canned_tracks

        def get_next_page(*args, **kwargs):
            page = args[0]
            if page == TRACKS_DAILY1:
                return TRACKS_TARGET
            else:
                return None

        self.spotify.next.side_effect = get_next_page

        self.playlists.append_daily_mix(randomize=False, target_name=None)

        self.spotify.playlist_add_items.assert_called_with("1JJB9ICuIoE6aD4jg9vgmV", ["3DrlHWCoFqHQYGwE8MWsuv"])

    def test_append_daily_mix_paged_tracks_filter_none(self):
        self.spotify.current_user_playlists.return_value = {"items": PLAYLIST_LIST}

        self.spotify.playlist_items.side_effect = get_canned_tracks

        def get_next_page(*args, **kwargs):
            page = args[0]
            if page == TRACKS_DAILY1:
                return TRACKS_TARGET + [None]
            else:
                return None

        self.spotify.next.side_effect = get_next_page

        self.playlists.append_daily_mix(randomize=False, target_name=None)

        self.spotify.playlist_add_items.assert_called_with("1JJB9ICuIoE6aD4jg9vgmV", ["3DrlHWCoFqHQYGwE8MWsuv"])

    def test_append_daily_mix_paged_tracks_exception_next(self):
        self.spotify.current_user_playlists.return_value = {"items": PLAYLIST_LIST}

        self.spotify.playlist_items.side_effect = get_canned_tracks

        self.spotify.next.side_effect = Mock(side_effect=IOError("Problems paging"))

        self.playlists.append_daily_mix(randomize=False, target_name=None)

        self.spotify.playlist_add_items.assert_called_with("1JJB9ICuIoE6aD4jg9vgmV", ["3DrlHWCoFqHQYGwE8MWsuv"])


class ListPlaylistsTestCase(unittest.TestCase):
    def setUp(self):
        self.spotify = MagicMock()
        self.spotify.next.return_value = None
        self.playlists = Playlists(self.spotify)

    def test_list_all(self):
        self.spotify.current_user_playlists.return_value = {"items": PLAYLIST_LIST}

        playlists = self.playlists.list_all_playlists()
        self.assertEqual(6, len(playlists))
        print(playlists)

    def test_filter(self):
        self.spotify.current_user_playlists.return_value = {"items": PLAYLIST_LIST}

        playlists = self.playlists.list_all_playlists(filters="name:eq:Overplayed")
        self.assertEqual(1, len(playlists))
        self.assertEqual("Overplayed", playlists[0][FieldName.PLAYLIST_NAME])
        print(playlists)

    def test_sort(self):
        self.spotify.current_user_playlists.return_value = {"items": PLAYLIST_LIST}

        playlists = self.playlists.list_all_playlists(sort_fields="name:rev")
        self.assertEqual(6, len(playlists))
        self.assertEqual("Your Top Songs 2022", playlists[0][FieldName.PLAYLIST_NAME])
        print(playlists)


class RandomizePlaylistTestCase(unittest.TestCase):
    def setUp(self):
        self.spotify = MagicMock()
        self.spotify.next.return_value = None
        self.playlists = Playlists(self.spotify)

    def test_randomize(self):
        self.spotify.playlist_items.side_effect = get_canned_tracks

        playlist = {"id": "37i9dQZF1E37hnawmowyJn", "name": "test_name"}
        result = self.playlists.randomize_playlist(playlist)
        self.assertEqual(PlaylistResult.SUCCESS, result)

        self.spotify.playlist_replace_items.assert_called_with("37i9dQZF1E37hnawmowyJn", ANY)

    def test_randomize_exception(self):
        self.spotify.playlist_items.side_effect = Mock(side_effect=Exception("Bad playlist items"))

        playlist = {"id": "37i9dQZF1E37hnawmowyJn", "name": "test_name"}
        result = self.playlists.randomize_playlist(playlist)
        self.assertEqual(PlaylistResult.FAILURE, result)

        self.spotify.playlist_replace_items.assert_not_called()


# noinspection PyTypeChecker
class RecentSubscriptionsTestCase(unittest.TestCase):
    def setUp(self):
        self.spotify = MagicMock()
        self.spotify.next.return_value = None
        self.playlists = Playlists(self.spotify)

    def test_recent_subscriptions_none_defined(self):
        self.spotify.current_user_playlists.return_value = {"items": PLAYLIST_LIST}

        self.spotify.playlist_items.side_effect = get_canned_tracks
        self.spotify.me.return_value = {"id": "testuser"}
        self.spotify.user_playlist_create.return_value = {"id": "1JJB9ICuIoE6aD4jg9vgmV"}
        self.playlists.append_recent_subscriptions(randomize=False, target_name=None)

        self.spotify.playlist_add_items.assert_not_called()

    def test_recent_subscriptions_exclude_zeros(self):
        config = {
            "playlists": {"test": ["some_epoch"]},
            "oldest_timestamp": "2022-12-10T15:56:13Z",
            "include_zero_timestamps": False,
        }
        local_playlists = Playlists(self.spotify, config=config)
        self.spotify.current_user_playlists.return_value = {"items": PLAYLIST_LIST}

        self.spotify.playlist_items.side_effect = get_canned_tracks
        self.spotify.me.return_value = {"id": "testuser"}
        self.spotify.user_playlist_create.return_value = {"id": "1JJB9ICuIoE6aD4jg9vgmV"}
        local_playlists.append_recent_subscriptions(randomize=False, target_name=None)

        # self.spotify.playlist_add_items(target_list["id"], id_batch)
        call_args = self.spotify.playlist_add_items.call_args.args
        self.assertEqual(2, len(call_args))
        self.assertEqual("1JJB9ICuIoE6aD4jg9vgmV", call_args[0])
        all_track_ids = [
            "GWzB3Hhj22I8SLs6Gt9B5O",
            "X4snMZtCekj688i8a1H7P7",
            "gD5YUJdvxOg2LBURBFg8MO",
            "vM3EbgX80HHmN7j7r67X3J",
        ]
        self.assertListEqual(sorted(all_track_ids), sorted(call_args[1]))
        print(f"Call args: {call_args}")

    def test_recent_subscriptions_include_zeros(self):
        config = {
            "playlists": {"test": ["some_epoch"]},
            "oldest_timestamp": "2022-12-10T15:56:13Z",
            "include_zero_timestamps": True,
        }
        local_playlists = Playlists(self.spotify, config=config)
        self.spotify.current_user_playlists.return_value = {"items": PLAYLIST_LIST}

        self.spotify.playlist_items.side_effect = get_canned_tracks
        self.spotify.me.return_value = {"id": "testuser"}
        self.spotify.user_playlist_create.return_value = {"id": "1JJB9ICuIoE6aD4jg9vgmV"}
        local_playlists.append_recent_subscriptions(randomize=False, target_name=None)

        # self.spotify.playlist_add_items(target_list["id"], id_batch)
        call_args = self.spotify.playlist_add_items.call_args.args
        self.assertEqual(2, len(call_args))
        self.assertEqual("1JJB9ICuIoE6aD4jg9vgmV", call_args[0])
        all_track_ids = [
            "GWzB3Hhj22I8SLs6Gt9B5O",
            "Q2zReqJDrr0GMyu8cU8KtD",
            "X4snMZtCekj688i8a1H7P7",
            "gD5YUJdvxOg2LBURBFg8MO",
            "sl2AA4JIQbn2R3eRkAsvx0",
            "vM3EbgX80HHmN7j7r67X3J",
            "yHBi3S6eRcld0JtNYzmy3k",
        ]
        self.assertListEqual(sorted(all_track_ids), sorted(call_args[1]))
        print(f"Call args: {call_args}")


class PlaylistFilterTestCase(unittest.TestCase):
    def setUp(self):
        self.spotify = MagicMock()
        self.spotify.next.return_value = None
        self.playlists = Playlists(self.spotify)

    def test_all_valid(self):
        self.spotify.playlist_items.side_effect = get_canned_tracks

        result = self.playlists._filter_for_tracks("37i9dQZF1E37hnawmowyJn")

        tracks = get_canned_tracks("37i9dQZF1E37hnawmowyJn")

        self.assertEqual(tracks["items"], result)

    def test_some_invalid(self):
        self.spotify.playlist_items.side_effect = get_canned_tracks

        result = self.playlists._filter_for_tracks("some_invalid")

        tracks = get_canned_tracks("minus_invalid")

        self.assertEqual(tracks["items"], result)
