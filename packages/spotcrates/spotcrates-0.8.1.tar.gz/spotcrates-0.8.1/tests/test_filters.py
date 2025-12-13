import unittest

from spotcrates.common import NotFoundException
from spotcrates.filters import (
    FilterLookup,
    FilterType,
    FieldLookup,
    FieldName,
    parse_filters,
    FieldFilter,
)


class FilterLookupTestCase(unittest.TestCase):
    def setUp(self):
        self.lookup = FilterLookup()

    def test_contains(self):
        self.assertEqual(FilterType.CONTAINS, self.lookup.find("contains"))

    def test_con(self):
        self.assertEqual(FilterType.CONTAINS, self.lookup.find("con"))

    def test_c(self):
        self.assertEqual(FilterType.CONTAINS, self.lookup.find("c"))

    def test_equ(self):
        self.assertEqual(FilterType.EQUALS, self.lookup.find("equ"))

    def test_st(self):
        self.assertEqual(FilterType.STARTS, self.lookup.find("st"))

    def test_end(self):
        self.assertEqual(FilterType.ENDS, self.lookup.find("end"))

    def test_gr(self):
        self.assertEqual(FilterType.GREATER, self.lookup.find("gr"))

    def test_geq(self):
        self.assertEqual(FilterType.GREATER_EQUAL, self.lookup.find("geq"))

    def test_lt(self):
        self.assertEqual(FilterType.LESS, self.lookup.find("lt"))

    def test_leq(self):
        self.assertEqual(FilterType.LESS_EQUAL, self.lookup.find("leq"))

    def test_invalid(self):
        with self.assertRaises(NotFoundException):
            self.lookup.find("zyzygy")

    def test_none(self):
        with self.assertRaises(NotFoundException):
            self.lookup.find(None)

    def test_blank(self):
        with self.assertRaises(NotFoundException):
            self.lookup.find(None)


class FieldNameTestCase(unittest.TestCase):
    def setUp(self):
        self.lookup = FieldLookup()

    def test_name(self):
        self.assertEqual(FieldName.PLAYLIST_NAME, self.lookup.find("name"))

    def test_pname(self):
        self.assertEqual(FieldName.PLAYLIST_NAME, self.lookup.find("pname"))

    def test_playlistname(self):
        self.assertEqual(FieldName.PLAYLIST_NAME, self.lookup.find("playlistname"))

    def test_p(self):
        self.assertEqual(FieldName.PLAYLIST_NAME, self.lookup.find("p"))

    def test_d(self):
        self.assertEqual(FieldName.PLAYLIST_DESCRIPTION, self.lookup.find("d"))

    def test_pd(self):
        self.assertEqual(FieldName.PLAYLIST_DESCRIPTION, self.lookup.find("pd"))

    def test_desc(self):
        self.assertEqual(FieldName.PLAYLIST_DESCRIPTION, self.lookup.find("desc"))

    def test_c(self):
        self.assertEqual(FieldName.SIZE, self.lookup.find("c"))

    def test_s(self):
        self.assertEqual(FieldName.SIZE, self.lookup.find("s"))

    def test_size(self):
        self.assertEqual(FieldName.SIZE, self.lookup.find("size"))

    def test_count(self):
        self.assertEqual(FieldName.SIZE, self.lookup.find("count"))

    def test_o(self):
        self.assertEqual(FieldName.OWNER, self.lookup.find("o"))

    def test_owner(self):
        self.assertEqual(FieldName.OWNER, self.lookup.find("owner"))


class ParseFiltersTestCase(unittest.TestCase):
    def test_owner_contains_default(self):
        filters = parse_filters("o:testuser")
        owner_filters = filters.get(FieldName.OWNER)
        self.assertEqual(1, len(owner_filters))
        first_filter = owner_filters[0]
        self.assertEqual(FieldFilter(FieldName.OWNER, FilterType.CONTAINS, "testuser"), first_filter)

    def test_desc(self):
        filters = parse_filters("desc:sta:beginning")
        desc_filters = filters.get(FieldName.PLAYLIST_DESCRIPTION)
        self.assertEqual(1, len(desc_filters))
        first_filter = desc_filters[0]
        self.assertEqual(
            FieldFilter(FieldName.PLAYLIST_DESCRIPTION, FilterType.STARTS, "beginning"),
            first_filter,
        )

    def test_name_size(self):
        filters = parse_filters("name:eq:specific_name, s:ge :99")
        name_filters = filters.get(FieldName.PLAYLIST_NAME)
        self.assertEqual(1, len(name_filters))
        first_filter = name_filters[0]
        self.assertEqual(
            FieldFilter(FieldName.PLAYLIST_NAME, FilterType.EQUALS, "specific_name"),
            first_filter,
        )

        size_filters = filters.get(FieldName.SIZE)
        self.assertEqual(1, len(size_filters))
        first_size_filter = size_filters[0]
        self.assertEqual(
            FieldFilter(FieldName.SIZE, FilterType.GREATER_EQUAL, "99"),
            first_size_filter,
        )

    def test_name_size_multi(self):
        filters = parse_filters("name:eq:specific_name, s:ge :99, s:lt: 1234")
        name_filters = filters.get(FieldName.PLAYLIST_NAME)
        self.assertEqual(1, len(name_filters))
        first_filter = name_filters[0]
        self.assertEqual(
            FieldFilter(FieldName.PLAYLIST_NAME, FilterType.EQUALS, "specific_name"),
            first_filter,
        )

        size_filters = filters.get(FieldName.SIZE)
        self.assertEqual(2, len(size_filters))
        first_size_filter = size_filters[0]
        self.assertEqual(
            FieldFilter(FieldName.SIZE, FilterType.GREATER_EQUAL, "99"),
            first_size_filter,
        )

        second_size_filter = size_filters[1]
        self.assertEqual(FieldFilter(FieldName.SIZE, FilterType.LESS, "1234"), second_size_filter)

    def test_implicit_all(self):
        filters = parse_filters("filterval")
        desc_filters = filters.get(FieldName.ALL)
        self.assertEqual(1, len(desc_filters))
        first_filter = desc_filters[0]
        self.assertEqual(
            FieldFilter(FieldName.ALL, FilterType.CONTAINS, "filterval"),
            first_filter,
        )

    def test_explicit_all(self):
        filters = parse_filters("all:st:filterval")
        desc_filters = filters.get(FieldName.ALL)
        self.assertEqual(1, len(desc_filters))
        first_filter = desc_filters[0]
        self.assertEqual(
            FieldFilter(FieldName.ALL, FilterType.STARTS, "filterval"),
            first_filter,
        )

    def test_invalid_field(self):
        with self.assertRaises(NotFoundException):
            parse_filters("zzz:testuser")

    def test_invalid_filter_type(self):
        with self.assertRaises(NotFoundException):
            parse_filters("o:zzz:testuser")

    def test_empty_filter(self):
        self.assertEqual({}, parse_filters(""))

    def test_null_filter(self):
        self.assertEqual({}, parse_filters(None))
