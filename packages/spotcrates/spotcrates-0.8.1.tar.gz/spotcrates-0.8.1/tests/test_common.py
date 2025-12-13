import unittest

from spotcrates.common import truncate_long_value, ValueFilter

# ruff: noqa: E712

# truncate_long_value


class TruncateLongValueTestCase(unittest.TestCase):
    def test_default_trunc(self):
        self.assertEqual("some_", truncate_long_value("some_long_string", 5))

    def test_end_trunc(self):
        self.assertEqual("tring", truncate_long_value("some_long_string", 5, trim_tail=False))

    def test_empty(self):
        self.assertEqual("", truncate_long_value("", 5, trim_tail=False))

    def test_null(self):
        self.assertEqual(None, truncate_long_value(None, 5, trim_tail=False))


## ValueFilter ##


# include
def test_empty_value_filter():
    assert ValueFilter().include("anything") == True


def test_explicit_include():
    assert ValueFilter(includes=["anything"]).include("anything") == True
    assert ValueFilter(includes=["anything"]).include("nothing") == False


def test_explicit_exclude():
    assert ValueFilter(excludes=["anything"]).include("anything") == False
    assert ValueFilter(excludes=["anything"]).include("nothing") == True


def test_explicit_include_exclude():
    assert ValueFilter(includes=["anything"], excludes=["nothing"]).include("anything") == True
    assert ValueFilter(includes=["anything"], excludes=["nothing"]).include("nothing") == False


def test_explicit_include_exclude_precedence():
    assert ValueFilter(includes=["anything"], excludes=["anything"]).include("anything") == False


def test_nested_include():
    assert ValueFilter.from_nested(includes=[["anything"]]).include("anything") == True
    assert ValueFilter.from_nested(includes=[["anything"]]).include("nothing") == False


def test_nested_include_multi():
    assert ValueFilter.from_nested(includes=[["anything", "nothing"]]).include("anything") == True
    assert ValueFilter.from_nested(includes=[["anything", "nothing"]]).include("nothing") == True
    assert ValueFilter.from_nested(includes=[["anything", "nothing"]]).include("something") == False


# exclude
def test_empty_value_filter_exclude():
    assert ValueFilter().exclude("anything") == False


def test_explicit_include_exclude_exclude():
    assert ValueFilter(includes=["anything"], excludes=["anything"]).exclude("anything") == True
    assert ValueFilter(includes=["anything"], excludes=["anything"]).exclude("nothing") == True


def test_explicit_include_exclude_exclude_precedence():
    assert ValueFilter(includes=["anything"], excludes=["anything"]).exclude("anything") == True


def test_nested_exclude():
    assert ValueFilter.from_nested(excludes=[["anything"]]).exclude("anything") == True
    assert ValueFilter.from_nested(excludes=[["anything"]]).exclude("nothing") == False


def test_nested_exclude_multi():
    assert ValueFilter.from_nested(excludes=[["anything", "nothing"]]).exclude("anything") == True
    assert ValueFilter.from_nested(excludes=[["anything", "nothing"]]).exclude("nothing") == True
    assert ValueFilter.from_nested(excludes=[["anything", "nothing"]]).exclude("something") == False
