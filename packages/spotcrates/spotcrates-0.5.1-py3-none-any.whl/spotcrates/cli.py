#!/usr/bin/env python

"""
CLI runner for Spotify automation.
"""

import argparse
import logging
import sys

import pygtrie

from spotcrates.common import BaseLookup, truncate_long_value
from spotcrates.filters import FieldName

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

__author__ = "cmayes"

from pathlib import Path

import spotipy

from spotcrates.playlists import Playlists, PlaylistResult
from appdirs import user_config_dir, user_cache_dir

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

DEFAULT_CONFIG_DIR = user_config_dir("spotcrates")
DEFAULT_CONFIG_FILE = Path(DEFAULT_CONFIG_DIR, "spotcrates_config.toml")
DEFAULT_CACHE_DIR = user_cache_dir("spotcrates")
DEFAULT_AUTH_CACHE_FILE = Path(DEFAULT_CACHE_DIR, "spotcrates_auth_cache")
DEFAULT_AUTH_SCOPES = ["playlist-modify-private", "playlist-read-private"]
DEFAULT_TARGET = "default_target"

COMMANDS = ["daily", "list-playlists", "subscriptions", "commands"]

COMMAND_DESCRIPTION = f"""
{'COMMAND NAME':<16} DESCRIPTION
{'daily':<16} Add "Daily Mix" entries to the end of the target playlist, filtering for excluded entries.
{'subscriptions':<16} Add new tracks from configured playlists to the target playlist, filtering for excluded entries.
{'list-playlists':<16} Prints a table describing your playlists.
{'randomize':<16} Randomizes the playlists with the given names, IDs, or in the given collections.
{'copy':<16} Copies a playlist into a new playlist. You may optionally specify a destination playlist name.
{'commands':<16} Prints this command list.
"""


def print_commands():
    """Prints available commands."""
    print(COMMAND_DESCRIPTION)


def get_config(config_file):
    """Loads the specified TOML-formatted config file or returns an empty dict"""
    if config_file.exists():
        with open(config_file, mode="rb") as fp:
            return tomllib.load(fp)
    else:
        logging.debug(f"Config file '{config_file}' does not exist")
        return {}


def prepare_auth_cache_loc(config):
    auth_cache_file = Path(config.get("auth_cache", DEFAULT_AUTH_CACHE_FILE))
    if not auth_cache_file.exists():
        auth_cache_file.parent.mkdir(parents=True, exist_ok=True)
    return auth_cache_file


def get_spotify_handle(config):
    spotify_cfg = config.get("spotify")
    auth_scopes = spotify_cfg.get("auth_scopes", DEFAULT_AUTH_SCOPES)
    cache_path = prepare_auth_cache_loc(spotify_cfg)
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=cache_path)
    if spotify_cfg:
        auth_manager = spotipy.oauth2.SpotifyOAuth(
            client_id=spotify_cfg.get("client_id"),
            client_secret=spotify_cfg.get("client_secret"),
            redirect_uri=spotify_cfg.get("redirect_uri"),
            cache_handler=cache_handler,
            scope=auth_scopes,
        )
    else:
        auth_manager = spotipy.oauth2.SpotifyOAuth(
            cache_handler=cache_handler, scope=auth_scopes
        )
    return spotipy.Spotify(auth_manager=auth_manager)


def append_daily_mix(config, args):
    sp = get_spotify_handle(config)

    playlists = Playlists(sp, config.get("playlists"))
    playlists.append_daily_mix(args.randomize, args.target)


def append_recent_subscriptions(config, args):
    sp = get_spotify_handle(config)

    playlists = Playlists(sp, config.get("subscriptions"))
    playlists.append_recent_subscriptions(args.randomize, args.target)


def randomize_lists(config, args):
    arguments = args.arguments
    if arguments:
        sp = get_spotify_handle(config)
        playlists = Playlists(sp, config.get("playlists"))
        results = playlists.randomize_playlists(arguments)

        for item, result in results.items():
            print(f"{item}: {result.label}")
    else:
        logger.warning("No playlists specified; nothing to randomize")
        return 5


def copy_list(config, args):
    arguments = args.arguments
    if arguments:
        sp = get_spotify_handle(config)
        playlists = Playlists(sp, config.get("playlists"))
        result, copy_name = playlists.copy_list(arguments, args.randomize)

        if PlaylistResult.SUCCESS == result:
            print(f"Successfully copied {arguments[0]} to {copy_name}")
        else:
            logger.warning(f"Problems copying {arguments[0]}")

    else:
        logger.warning("No playlist specified; nothing to copy")
        return 6


def list_playlists(config, args):
    sp = get_spotify_handle(config)
    playlists = Playlists(sp, config.get("playlists"))

    try:
        all_playlists = playlists.list_all_playlists(
            filters=args.filters, sort_fields=args.sort_fields
        )
    except Exception as e:
        logger.warning(f"Problems listing playlists: {e}")
        return 1

    print(f"{'PLAYLIST NAME':<32} {'SIZE':<5} {'ID':<24} {'OWNER':<16} DESCRIPTION")
    for playlist_row in all_playlists:
        print(
            f"""{truncate_long_value(playlist_row[FieldName.PLAYLIST_NAME], 32):<32} \
{playlist_row[FieldName.SIZE]:<5} \
{playlist_row[FieldName.SPOTIFY_ID]:<24} \
{truncate_long_value(playlist_row[FieldName.OWNER], 16):<16} \
{truncate_long_value(playlist_row[FieldName.PLAYLIST_DESCRIPTION], 75)}"""
        )


class CommandLookup(BaseLookup):

    def _init_lookup(self):
        lookup = pygtrie.CharTrie()
        lookup["d"] = "daily"
        lookup["l"] = "list-playlists"
        lookup["s"] = "subscriptions"
        lookup["r"] = "randomize"
        lookup["cop"] = "copy"
        lookup["com"] = "commands"
        return lookup


def parse_cmdline(argv):
    """
    Returns the parsed argument list and return code.
    `argv` is a list of arguments, or `None` for ``sys.argv[1:]``.
    """
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config_file",
                        help=f"The location of the config file (default: {DEFAULT_CONFIG_FILE})",
                        default=DEFAULT_CONFIG_FILE, type=Path)
    parser.add_argument("-s", "--sort_fields", help="The fields to sort against, applied in order")
    parser.add_argument("-f", "--filters", help="Filters to apply to the list")
    parser.add_argument("-r", "--randomize", help="Randomize the target list", action='store_true')
    parser.add_argument("-t", "--target",
                        help="Specify the target name of the operation (overrides any default value)")
    parser.add_argument("command", metavar="COMMAND",
                        help=f"The command to run (one of {','.join(COMMANDS)})")
    parser.add_argument("arguments", metavar='ARGUMENTS', nargs='*',
                        help="the arguments to the command")
    args = None
    try:
        args = parser.parse_args(argv)
    except IOError as e:
        logger.warning("Problems reading file:", e)
        parser.print_help()
        return args, 2

    return args, 0


def main(argv=None):
    args, ret = parse_cmdline(argv)
    if ret != 0:
        return ret
    config = get_config(args.config_file)

    command = CommandLookup().find(args.command.lower())

    # TODO: Add trie for commands

    if command == "daily":
        return append_daily_mix(config, args)
    elif command == "list-playlists":
        return list_playlists(config, args)
    elif command == "subscriptions":
        return append_recent_subscriptions(config, args)
    elif command == "randomize":
        return randomize_lists(config, args)
    elif command == "copy":
        return copy_list(config, args)
    elif command == "commands":
        return print_commands()
    else:
        print(
            f"Invalid command '{args.command}'.  Valid commands: {','.join(COMMANDS)}"
        )
        return 1


if __name__ == "__main__":
    status = main()
    sys.exit(status)
