import datetime
import itertools
import logging
from abc import ABC, abstractmethod
from itertools import islice
from pathlib import Path
from typing import Iterable, Dict, Any

import spotipy
import tomli
from appdirs import user_config_dir, user_cache_dir
from pygtrie import CharTrie

from spotipy import Spotify

DEFAULT_CONFIG_DIR = user_config_dir("spotcrates")
DEFAULT_CONFIG_FILE = Path(DEFAULT_CONFIG_DIR, "spotcrates_config.toml")
DEFAULT_CACHE_DIR = user_cache_dir("spotcrates")
DEFAULT_AUTH_CACHE_FILE = Path(DEFAULT_CACHE_DIR, "spotcrates_auth_cache")
DEFAULT_AUTH_SCOPES = ["playlist-modify-private", "playlist-read-private"]
DEFAULT_REDIRECT_URI = "http://127.0.0.1:5000/"
DEFAULT_TARGET = "default_target"
ISO_8601_TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
ZERO_TIMESTAMP = datetime.datetime.strptime("1970-01-01T00:00:00Z", ISO_8601_TIMESTAMP_FORMAT)


class NotFoundException(Exception):
    pass


def batched(iterable: Iterable, n: int):
    """Batch data into lists of length n. The last batch may be shorter."""
    it = iter(iterable)
    while True:
        batch = list(islice(it, n))
        if not batch:
            return
        yield batch


def get_all_items(spotify: Spotify, first_page: Dict[str, Any]):
    """Collects the 'items' contents from every page in the given result set."""
    all_items = []

    all_items.extend(first_page["items"])

    try:
        next_page = spotify.next(first_page)
        while next_page:
            all_items.extend(next_page["items"])
            next_page = spotify.next(next_page)
    except TimeoutError:
        logging.info("Timeout error encountered while paging Spotify items")
    except Exception as e:
        logging.warning(f"Problems paging given Spotify items list: {e}", exc_info=True)

    return [item for item in all_items if item is not None]


def truncate_long_value(full_value: str | None, length: int, trim_tail: bool = True) -> str:
    """Returns the given value truncated from the start of the value so that it is at most the given length.

    :param full_value: The value to trim.
    :param length: The maximum length of the returned value.
    :param trim_tail: Whether to trim from the head or tail of the string.
    :return: The value trimmed from the start of the string to be at most the given length.
    """
    if not full_value:
        return full_value

    if len(full_value) > length:
        if trim_tail:
            return full_value[:length]
        else:
            return full_value[-length:]
    return full_value


class BaseLookup(ABC):
    def __init__(self):
        """Uses a trie to find the longest matching prefix for the given lookup value"""
        self.logger = logging.getLogger(__name__)
        self.lookup = self._init_lookup()

    def find(self, lookup_val):
        if not lookup_val:
            raise NotFoundException(f"Blank/null lookup value {lookup_val}")

        found_command = self.lookup.longest_prefix(lookup_val)

        if found_command:
            self.logger.debug("Got %s (%s) for %s", found_command.value, found_command.key, lookup_val)
            return found_command.value
        else:
            raise NotFoundException(f"No value for {lookup_val}")

    @abstractmethod
    def _init_lookup(self) -> CharTrie:
        pass


def get_spotify_handle(config: Dict[str, Dict[str, Any]]):
    spotify_cfg = config.get("spotify")
    if not spotify_cfg:
        raise Exception("No Spotify config defined")
    auth_scopes = spotify_cfg.get("auth_scopes", DEFAULT_AUTH_SCOPES)
    redirect_uri = spotify_cfg.get("redirect_uri", DEFAULT_REDIRECT_URI)
    cache_path = prepare_auth_cache_loc(spotify_cfg)
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=cache_path)
    if spotify_cfg:
        auth_manager = spotipy.oauth2.SpotifyOAuth(
            client_id=spotify_cfg.get("client_id"),
            client_secret=spotify_cfg.get("client_secret"),
            redirect_uri=redirect_uri,
            cache_handler=cache_handler,
            scope=auth_scopes,
        )
    else:
        auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler, scope=auth_scopes)
    return spotipy.Spotify(auth_manager=auth_manager)


def prepare_auth_cache_loc(config: Dict[str, Any]):
    auth_cache_file = Path(config.get("auth_cache", DEFAULT_AUTH_CACHE_FILE))
    if not auth_cache_file.exists():
        auth_cache_file.parent.mkdir(parents=True, exist_ok=True)
    return auth_cache_file


def get_config(config_file: Path):
    """Loads the specified TOML-formatted config file or returns an empty dict"""
    if config_file.exists():
        with open(config_file, mode="rb") as fp:
            return tomli.load(fp)
    else:
        logging.debug(f"Config file '{config_file}' does not exist")
        return {}


class ValueFilter:
    def __init__(self, includes: list[str] | None = None, excludes: list[str] | None = None):
        self._includes = includes
        self._excludes = excludes

    def include(self, value: str) -> bool:
        if self._excludes and value in self._excludes:
            return False
        return not self._includes or value in self._includes

    def exclude(self, value: str) -> bool:
        return not self.include(value)

    @classmethod
    def from_nested(cls, includes: list[list[str]] | None = None, excludes: list[list[str]] | None = None):
        flat_includes = list(itertools.chain.from_iterable(includes)) if includes else includes
        flat_excludes = list(itertools.chain.from_iterable(excludes)) if excludes else excludes
        return cls(flat_includes, flat_excludes)
