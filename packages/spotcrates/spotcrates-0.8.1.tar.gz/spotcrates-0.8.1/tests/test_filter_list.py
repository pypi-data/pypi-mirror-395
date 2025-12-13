import os
import unittest

from spotcrates.filters import filter_list, FieldName, sort_list
from tests.utils import load_playlist_listing_file, get_all_field_val_str

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
PLAYLISTS = load_playlist_listing_file(os.path.join(DATA_DIR, "playlists.json"))


class FilterListTestCase(unittest.TestCase):
    # filter_list
    def test_empty_filter(self):
        self.assertEqual(PLAYLISTS, filter_list(PLAYLISTS, ""))

    def test_null_filter(self):
        self.assertEqual(PLAYLISTS, filter_list(PLAYLISTS, None))

    def test_implicit_contains(self):
        filtered_list = filter_list(PLAYLISTS, "na:Songs")

        self.assertEqual(2, len(filtered_list))

        for playlist in filtered_list:
            self.assertTrue("Songs" in playlist[FieldName.PLAYLIST_NAME])

    def test_explicit_all(self):
        playlists = PLAYLISTS
        filtered_list = filter_list(playlists, "all:Spotify")

        self.assertEqual(3, len(filtered_list))

        for playlist in filtered_list:
            all_val_str = get_all_field_val_str(playlist)
            self.assertTrue("spotify" in all_val_str.lower())

    def test_implicit_all(self):
        playlists = PLAYLISTS
        filtered_list = filter_list(playlists, "Now")

        self.assertEqual(2, len(filtered_list))

        for playlist in filtered_list:
            all_val_str = get_all_field_val_str(playlist)
            self.assertTrue("now" in all_val_str.lower())

    def test_implicit_contains_caseless(self):
        filtered_list = filter_list(PLAYLISTS, "na:sOnGs")

        self.assertEqual(2, len(filtered_list))

        for playlist in filtered_list:
            self.assertTrue("Songs" in playlist[FieldName.PLAYLIST_NAME])

    def test_explicit_contains_caseless(self):
        filtered_list = filter_list(PLAYLISTS, "pname:con:sOnGs")

        self.assertEqual(2, len(filtered_list))

        for playlist in filtered_list:
            self.assertTrue("Songs" in playlist[FieldName.PLAYLIST_NAME])

    def test_equals(self):
        filtered_list = filter_list(PLAYLISTS, "na:eq:Now")

        self.assertEqual(1, len(filtered_list))

        for playlist in filtered_list:
            self.assertTrue("Now" == playlist[FieldName.PLAYLIST_NAME])

    def test_starts(self):
        filtered_list = filter_list(PLAYLISTS, "na:sta:your")

        self.assertEqual(2, len(filtered_list))

        for playlist in filtered_list:
            self.assertTrue(str(playlist[FieldName.PLAYLIST_NAME]).startswith("Your"))

    def test_ends(self):
        filtered_list = filter_list(PLAYLISTS, "desc:ends:MoRe")

        self.assertEqual(1, len(filtered_list))

        for playlist in filtered_list:
            self.assertTrue(str(playlist[FieldName.PLAYLIST_DESCRIPTION]).endswith("more"))

    def test_greater(self):
        filtered_list = filter_list(PLAYLISTS, "size:greater:300")

        self.assertEqual(2, len(filtered_list))

        for playlist in filtered_list:
            self.assertTrue(int(playlist[FieldName.SIZE]) > 300)

    def test_less(self):
        filtered_list = filter_list(PLAYLISTS, "size:lt:300")

        self.assertEqual(4, len(filtered_list))

        for playlist in filtered_list:
            self.assertTrue(int(playlist[FieldName.SIZE]) < 300)

    def test_greater_equal(self):
        filtered_list = filter_list(PLAYLISTS, "size:geq:101")

        self.assertEqual(3, len(filtered_list))

        for playlist in filtered_list:
            self.assertTrue(int(playlist[FieldName.SIZE]) >= 101)

    def test_less_equal(self):
        filtered_list = filter_list(PLAYLISTS, "size:leq:100")

        self.assertEqual(3, len(filtered_list))

        for playlist in filtered_list:
            self.assertTrue(int(playlist[FieldName.SIZE]) <= 100)


class SortListTestCase(unittest.TestCase):
    playlists = PLAYLISTS

    # sort_list
    def test_blank_filter(self):
        self.assertEqual(PLAYLISTS, sort_list(PLAYLISTS, ""))

    def test_null_filter(self):
        self.assertEqual(PLAYLISTS, sort_list(PLAYLISTS, None))

    def test_name_sort(self):
        asc_name_sorted = sorted(PLAYLISTS, key=lambda d: d[FieldName.PLAYLIST_NAME])
        self.assertEqual(asc_name_sorted, sort_list(PLAYLISTS, "name"))

    def test_name_sort_descending(self):
        desc_name_sorted = sorted(PLAYLISTS, key=lambda d: d[FieldName.PLAYLIST_NAME], reverse=True)
        self.assertEqual(desc_name_sorted, sort_list(PLAYLISTS, "name:descending"))

    def test_name_sort_reverse(self):
        desc_name_sorted = sorted(PLAYLISTS, key=lambda d: d[FieldName.PLAYLIST_NAME], reverse=True)
        self.assertEqual(desc_name_sorted, sort_list(PLAYLISTS, "name:reverse"))

    def test_count_desc_multi(self):
        desc_count_sorted = sorted(PLAYLISTS, key=lambda d: d[FieldName.SIZE], reverse=True)
        self.assertEqual(desc_count_sorted, sort_list(PLAYLISTS, "count:desc,name"))
