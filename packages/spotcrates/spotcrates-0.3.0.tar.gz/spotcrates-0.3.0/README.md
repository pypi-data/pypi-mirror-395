# Spotcrates
### A set of tools for finding and managing music on Spotify

![Code Coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/cmayes/3c8214e2bd942821496440b93acd3582/raw/covbadge.json)

# Installation

(TODO: Add detailed instructions once uploaded to PyPI)

# Commands

The installation script puts the command `spotcrates` in your Python environment
(e.g. `/.pyenv/shims/spotcrates`). The command `spotcrates commands` lists all of the 
commands available along with a short description of each.

## daily
`spotcrates daily` collects the contents of the "Daily Mix" playlists, filters them 
against an exclusion list ("Overplayed" by default), and adds them to the end of 
a target list ("Now" by default).

## list-playlists
`spotcrates list-playlists` lists playlists' name, owner, track count, and description.
The command accepts `-f` for filter expressions and `-s` for sort expressions. (TODO: 
add description of filter and search expressions and link to it here)