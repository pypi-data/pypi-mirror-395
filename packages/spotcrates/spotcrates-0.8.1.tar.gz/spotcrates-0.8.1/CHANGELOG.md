# (Unreleased)

# Version 0.8.0

## Updated
- Moved to uv.

# Version 0.7.4

## Updated
- Added randomize-all command.

# Version 0.7.3

## Fixed
- Upgraded dependency versions to patch vulnerable spotipy version.

# Version 0.7.2

## Fixed
- Fixed handling of nested lists of values for includes and excludes.

# Version 0.7.1

## Added
- Added -i and -e to include and exclude (respectively) playlist sets.

# Version 0.7.0

## Added
- Allow zero-epoch ('1970-01-01T00:00:00Z') timestamps with the 'include_zero_timestamps' flag for subscriptions.

# Version 0.6.5

## Fixed

- Added a filter to remove invalid tracks.

# Version 0.6.4

## Added

- A loglevel CLI option.

# Version 0.6.3

## Added

- An initial version flag --version.

# Version 0.6.2

## Fixed

- Added try/catch for Spotify list paging.
- Added None filter for Spotify list paging.

# Version 0.6.1

## Fixed

- Create parent dirs for new config file.

# Version 0.6.0

## Added

- init-config command for creating an initial config file.
- A lot of documentation.

# Version 0.5.1

## Added

- Trie for command name evaluation.

## Updated

- Extracted common ABC for lookup classes.

# Version 0.5.0

## Added

- -r option to randomize the added tracks for applicable commands.
- -t option to provide a custom target name for applicable commands.
- copy command to copy a source playlist to a target playlist.
- randomize command to randomize the contents of the given tracks.

# Version 0.4.0

## Updated

- Changed "overplayed" to use a prefix pattern rather than a single list to account for 
    the 10K playlist size limit.

# Version 0.3.1

## Added

- Implicit and explicit `all` filter
  - Filters for any field containing the filter string
  - `all:spotify` looks for "spotify" in any field
    - `spotify` without the `all` qualifier is equivalent
- Added "spotify_id" field to results


# Version 0.3.0

## Added 

- `playlist-list` command
  - `-f` filter option
  - `-s` sort option

# 2022-12-18

## Added

- created common.py for common logic.

- Create a target playlist if it doesn't exist.
