#!/usr/bin/env python

"""
CLI runner for Spotify automation.
"""

import sys
import argparse
import logging

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

__author__ = 'cmayes'

from pathlib import Path

import spotipy

from spotcrates.playlists import Playlists
from appdirs import user_config_dir

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

DEFAULT_CONFIG_DIR = user_config_dir('spotcrates')
DEFAULT_CONFIG_FILE = Path(DEFAULT_CONFIG_DIR, "spotcrates_config.toml")

COMMANDS = ['daily']

COMMAND_DESCRIPTION = f"""
{'COMMAND NAME':<16} DESCRIPTION
{'daily':<16} Add "Daily Mix" entries to the end of the target playlist, filtering for excluded entries.
"""


def warning(*objs):
    """Writes a message to stderr."""
    print("WARNING: ", *objs, file=sys.stderr)


def get_config(config_file):
    if config_file.exists():
        with open(config_file, mode="rb") as fp:
            return tomllib.load(fp)
    else:
        logging.debug(f"Config file '{config_file}' does not exist")
        return {}


def print_commands():
    """Prints available commands."""
    print(COMMAND_DESCRIPTION)


def get_spotify_handle(config):
    cache_handler = spotipy.cache_handler.CacheFileHandler()
    spotify_cfg = config.get("spotify")
    if spotify_cfg:
        auth_manager = spotipy.oauth2.SpotifyOAuth(client_id=spotify_cfg.get("client_id"),
                                                   client_secret=spotify_cfg.get("client_secret"),
                                                   redirect_uri=spotify_cfg.get("redirect_uri"),
                                                   cache_handler=cache_handler,
                                                   scope=["playlist-modify-private", "playlist-read-private"])
    else:
        auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler,
                                                   scope=["playlist-modify-private", "playlist-read-private"])
    return spotipy.Spotify(auth_manager=auth_manager)


def append_daily_mix(config):
    sp = get_spotify_handle(config)

    playlists = Playlists(sp)
    playlists.append_daily_mix()


def parse_cmdline(argv):
    """
    Returns the parsed argument list and return code.
    `argv` is a list of arguments, or `None` for ``sys.argv[1:]``.
    """
    if argv is None:
        argv = sys.argv[1:]

    # initialize the parser object:
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config_file", help="The location of the config file",
                        default=DEFAULT_CONFIG_FILE, type=Path)
    parser.add_argument("command", metavar='COMMAND',
                        help=f"The command to run (one of {','.join(COMMANDS)})")
    args = None
    try:
        args = parser.parse_args(argv)
    except IOError as e:
        warning("Problems reading file:", e)
        parser.print_help()
        return args, 2

    return args, 0


def main(argv=None):
    args, ret = parse_cmdline(argv)
    if ret != 0:
        return ret
    config = get_config(args.config_file)
    command = args.command.lower()

    if command == 'daily':
        append_daily_mix(config)
    elif command == 'commands':
        print_commands()
    else:
        print(f"Invalid command '{args.command}'.  Valid commands: {','.join(COMMANDS)}")
        return 1

    return 0  # success


if __name__ == '__main__':
    status = main()
    sys.exit(status)
