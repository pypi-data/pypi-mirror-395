import logging
from collections import defaultdict
from enum import Enum, auto
from typing import Dict, List

import pygtrie

from spotcrates.common import NotFoundException

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class InvalidFilterException(Exception):
    pass


class FilterType(Enum):
    CONTAINS = auto()
    EQUALS = auto()
    STARTS = auto()
    ENDS = auto()
    GREATER = auto()
    LESS = auto()
    GREATER_EQUAL = auto()
    LESS_EQUAL = auto()

    def test(self, filter_val, target_val) -> bool:
        if self == FilterType.CONTAINS:
            return str(filter_val).lower() in str(target_val).lower()
        elif self == FilterType.EQUALS:
            return str(filter_val).lower() == str(target_val).lower()
        elif self == FilterType.STARTS:
            return str(target_val).lower().startswith(str(filter_val).lower())
        elif self == FilterType.ENDS:
            return str(target_val).lower().endswith(str(filter_val).lower())
        elif self == FilterType.GREATER:
            return int(target_val) > int(filter_val)
        elif self == FilterType.GREATER_EQUAL:
            return int(target_val) >= int(filter_val)
        elif self == FilterType.LESS:
            return int(target_val) < int(filter_val)
        elif self == FilterType.LESS_EQUAL:
            return int(target_val) <= int(filter_val)
        else:
            raise NotFoundException(f"Unhandled filter type {self}")


class FieldName(Enum):
    SPOTIFY_ID = auto()
    PLAYLIST_NAME = auto()
    SIZE = auto()
    OWNER = auto()
    PLAYLIST_DESCRIPTION = auto()
    ALL = auto()

    @staticmethod
    def list_regular_fields():
        for field in FieldName:
            if field == FieldName.ALL:
                continue
            yield field


class FilterLookup:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.lookup = FilterLookup._init_lookup()

    def find(self, type_name):
        if not type_name:
            raise NotFoundException(f"Blank/null filter type {type_name}")

        found_type = self.lookup.longest_prefix(type_name)

        if found_type:
            self.logger.debug(
                "Got %s (%s) for %s", found_type.value, found_type.key, type_name
            )
            found_val = found_type.value
            return found_val
        else:
            raise NotFoundException(f"No filter type for {type_name}")

    def eval_filter_type(self, filter_type) -> FilterType:
        filter_type_type = type(filter_type)
        if filter_type_type == FilterType:
            return filter_type
        elif filter_type_type == str:
            return self.find(filter_type)
        else:
            raise InvalidFilterException(f"Invalid filter type {filter_type_type}")

    @staticmethod
    def _init_lookup():
        lookup = pygtrie.CharTrie()
        lookup["c"] = FilterType.CONTAINS
        lookup["eq"] = FilterType.EQUALS
        lookup["s"] = FilterType.STARTS
        lookup["en"] = FilterType.ENDS
        lookup["g"] = FilterType.GREATER
        lookup["l"] = FilterType.LESS
        lookup["ge"] = FilterType.GREATER_EQUAL
        lookup["leq"] = FilterType.LESS_EQUAL

        return lookup


class FieldLookup:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.lookup = FieldLookup._init_lookup()

    def find(self, field_name):
        if not field_name:
            raise NotFoundException(f"Blank/null field name {field_name}")

        found_field = self.lookup.longest_prefix(field_name)

        if found_field:
            self.logger.debug(
                "Got %s (%s) for %s", found_field.value, found_field.key, field_name
            )
            found_val = found_field.value
            return found_val
        else:
            raise NotFoundException(f"No field name for {field_name}")

    def eval_field_name(self, field_name):
        field_name_type = type(field_name)
        if field_name_type == FieldName:
            return field_name
        elif field_name_type == str:
            return self.find(field_name)
        else:
            raise InvalidFilterException(f"Invalid field name type {field_name_type}")

    @staticmethod
    def _init_lookup():
        lookup = pygtrie.CharTrie()
        lookup["n"] = FieldName.PLAYLIST_NAME
        lookup["p"] = FieldName.PLAYLIST_NAME
        lookup["pl"] = FieldName.PLAYLIST_NAME
        lookup["pn"] = FieldName.PLAYLIST_NAME
        lookup["s"] = FieldName.SIZE
        lookup["ps"] = FieldName.SIZE
        lookup["d"] = FieldName.PLAYLIST_DESCRIPTION
        lookup["pd"] = FieldName.PLAYLIST_DESCRIPTION
        lookup["c"] = FieldName.SIZE
        lookup["s"] = FieldName.SIZE
        lookup["o"] = FieldName.OWNER
        lookup["a"] = FieldName.ALL

        return lookup


class FieldFilter:
    def __init__(self, field, filter_type, value):
        self.filter_lookup = FilterLookup()
        self.field_lookup = FieldLookup()
        self.filter_type = self.filter_lookup.eval_filter_type(filter_type)
        self.field = self.field_lookup.eval_field_name(field)
        self.value = value

    def passes(self, target_value) -> bool:
        return self.filter_type.test(self.value, target_value)

    def __repr__(self):
        return f"FieldFilter({self.field}, {self.value}, {self.filter_type})"

    def __eq__(self, other):
        if isinstance(other, FieldFilter):
            return (
                self.field == other.field
                and self.value == other.value
                and self.filter_type == other.filter_type
            )
        return NotImplemented


def parse_filters(filters: str) -> Dict[FieldName, List[FieldFilter]]:
    """Returns a dict keyed by field with values being a list of
    name:PoP
    size:gt:22
    name:twin


    :param filters: A str with a comma-separated list of filters
    :return: A map of field names to lower-case "contains" filter strings.
    """
    parsed_filters: Dict[FieldName, List[FieldFilter]] = defaultdict(list)

    if not filters:
        return parsed_filters

    raw_filters = [raw_filter.strip() for raw_filter in filters.split(",")]
    split_raw_filters = [raw_filter.split(":") for raw_filter in raw_filters]

    for raw_exp in split_raw_filters:
        exp_field_count = len(raw_exp)

        if exp_field_count < 1:
            raise InvalidFilterException(
                f"Invalid filter expression {':'.join(raw_exp)}"
            )

        stripped_exp = [field.strip() for field in raw_exp]

        if exp_field_count == 1:
            field_filter = FieldFilter(
                FieldName.ALL, FilterType.CONTAINS, stripped_exp[0]
            )
        elif exp_field_count == 2:
            field_filter = FieldFilter(
                stripped_exp[0], FilterType.CONTAINS, stripped_exp[1]
            )
        else:
            field_filter = FieldFilter(
                stripped_exp[0], stripped_exp[1], stripped_exp[2]
            )
        parsed_filters[field_filter.field].append(field_filter)

    return parsed_filters


# TODO: Test filter_list and consider moving filter to separate file
def filter_list(items, filters):
    parsed_filters = parse_filters(filters)

    filtered_items = items
    for field in FieldName:
        field_filters = parsed_filters[field]
        if field_filters:
            for cur_filter in field_filters:
                matching_items = []
                for cur_item in filtered_items:
                    if FieldName.ALL == field:
                        for regular_field in FieldName.list_regular_fields():
                            item_field = cur_item.get(regular_field)
                            if cur_filter.passes(item_field):
                                matching_items.append(cur_item)
                    else:
                        item_field = cur_item.get(field)
                        if cur_filter.passes(item_field):
                            matching_items.append(cur_item)

                filtered_items = list(
                    {v[FieldName.SPOTIFY_ID]: v for v in matching_items}.values()
                )

    return filtered_items


class SortType(Enum):
    ASCENDING = auto()
    DESCENDING = auto()


class SortLookup:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.lookup = SortLookup._init_lookup()

    def find(self, sort_type):
        if not sort_type:
            raise NotFoundException(f"Blank/null sort type {sort_type}")

        found_sort = self.lookup.longest_prefix(sort_type)

        if found_sort:
            self.logger.debug(
                "Got %s (%s) for %s", found_sort.value, found_sort.key, sort_type
            )
            found_val = found_sort.value
            return found_val
        else:
            raise NotFoundException(f"No sort type for {sort_type}")

    def eval_sort_type(self, sort_type):
        sort_type_type = type(sort_type)
        if sort_type_type == SortType:
            return sort_type
        elif sort_type_type == str:
            return self.find(sort_type)
        else:
            raise InvalidFilterException(f"Invalid sort type {sort_type_type}")

    @staticmethod
    def _init_lookup():
        lookup = pygtrie.CharTrie()
        lookup["a"] = SortType.ASCENDING
        lookup["d"] = SortType.DESCENDING
        lookup["r"] = SortType.DESCENDING
        return lookup


class FieldSort:
    def __init__(self, field, sort_type):
        self.sort_lookup = SortLookup()
        self.field_lookup = FieldLookup()
        self.sort_type = self.sort_lookup.eval_sort_type(sort_type)
        self.field = self.field_lookup.eval_field_name(field)


def parse_sorts(sorts: str) -> List[FieldSort]:
    parsed_sorts: List[FieldSort] = []

    if not sorts:
        return parsed_sorts

    raw_sorts = [raw_sort.strip() for raw_sort in sorts.split(",")]
    split_raw_sorts = [raw_sort.split(":") for raw_sort in raw_sorts]

    for raw_exp in split_raw_sorts:
        exp_field_count = len(raw_exp)

        stripped_exp = [field.strip() for field in raw_exp]
        if exp_field_count == 1:
            parsed_sorts.append(FieldSort(stripped_exp[0], SortType.ASCENDING))
        elif exp_field_count == 2:
            parsed_sorts.append(FieldSort(stripped_exp[0], stripped_exp[1]))

    return parsed_sorts


def sort_list(items, sort_exp):
    parsed_sorts = parse_sorts(sort_exp)

    if not parsed_sorts:
        return items

    if len(parsed_sorts) > 1:
        logger.warning("Only the first sort field is currently applied")

    sorter = parsed_sorts[0]

    return sorted(
        items,
        key=lambda d: d[sorter.field],
        reverse=sorter.sort_type == SortType.DESCENDING,
    )
