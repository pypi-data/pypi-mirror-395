# Spotcrates
## A set of tools for finding and managing music on Spotify

![Code Coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/cmayes/3c8214e2bd942821496440b93acd3582/raw/covbadge.json)

# Installation

## Requirements

Spotcrates requires [Python](https://www.python.org/) 10 or newer. You will also need a Spotify account.

## Install from PyPI

```shell
pip install spotcrates
```

## Configuration

Spotcrates will need, at minimum, credentials for accessing your Spotify account. You may also specify
playlists to subscribe to, among other settings.

### Initial Configuration File

Spotcrates can create an initial configuration file for itself. It will write to the specified configuration file
location, i.e. what you configure with `-c` or `--config_file`. If you don't specify anything, Spotcrates will use
a platform-specific configuration file location, e.g. `/home/$USER/.config/spotcrates/spotcrates_config.toml` 
on Linux. The output of `spotcrates -h` includes the default location for your configuration file.

```shell
spotcrates init-config
```

### Spotify API Credentials

This bit is not terribly user-friendly as it's assumed that developers will be the ones creating these credentials.
Since this app runs as a script on your own machine, you'll need to create your own credentials. You will need
a `Client ID` and a `Client Secret`. The process is a little involved, and the 
[Spotify docs on the subject](https://developer.spotify.com/documentation/general/guides/authorization/app-settings/) 
are a bit opaque for the casual user (as I very recently was). These pages do a pretty good job describing 
the process:

- https://support.heateor.com/get-spotify-client-id-client-secret/
- https://cran.r-project.org/web/packages/spotidy/vignettes/Connecting-with-the-Spotify-API.html

Note that these projects are mainly interested in extracting data for their respective applications, so the 
instructions are geared to that end.

Once you have your client ID and client secret, paste them into your Spotcrates configuration file in the `[spotify]`
section:

```toml
[spotify]
client_id = "(your ID here)"
client_secret = "(your secret here)"
```

#### Testing Your Credentials

Spotcrates will request and cache authorization info the first time you use your Spotify credentials. The cache location
is platform-specific. On Linux, it's usually at `/home/$USER/.cache/spotcrates/spotcrates_auth_cache`.

To trigger this step, you can try listing your playlists:

`spotcrates list-playlists`

Spotcrates will initiate an authorization process with Spotify via your default browser. If the authorization
succeeds, the browser tab will close itself, and your playlists will be listed on the command line.

### Customizable Settings for Spotify

These settings can be changed from their defaults, though you won't usually need to do so. They are defined
under the `[spotify]` config file heading.

- `auth_cache`: The location of the Spotify authorization cache. This defaults to your platform's default cache
    location base, plus `spotcrates/spotcrates_auth_cache`.
- `auth_scopes`: A list of authorization scopes that Spotcrates requests. The default scopes are
    `["playlist-modify-private", "playlist-read-private"]`.

## Playlists

These settings control playlist-related commands like [daily](#daily) or [randomize](#randomize). They
can be customized under the [playlists] heading in the configuration file.

- `daily_mix_target`: The name of the playlist to target, which is created if it does not exist. Defaults to "Now."
- `daily_mix_prefix`: The prefix of the "Daily Mix" playlists to be aggregated. Defaults to "Daily Mix."
- `daily_mix_excludes`: The prefix of the playlists that contain tracks to exclude. Defaults to "Overplayed."

## Subscriptions

These settings are for the [subscriptions](#subscriptions) command. They can be configured under the `[subscriptions]` 
configuration file heading. 

- `subscriptions_target`: The name of the playlists where the new subscriptions will be appended. Created if 
    the playlist does not exist. Defaults to `NewSubscriptions`.
- `max_age`: The maximum age of a track in a playlist for it to be considered "new." Values can be English
    expressions like `2 weeks` or `96 hours`. Defaults to `3 days`.
- `include_zero_timestamps`: Whether to include tracks with an `added_at` of `1970-01-01T00:00:00Z`. Some
    Spotify playlists do not set a useful `added_at` value. This flag includes those tracks despite
    their not passing the `max_age` test.

### Subscription Playlists

These are the playlist groups used by [subscriptions](#subscriptions) and related commands. All groups are included
by default. The values are the "spotify IDs" listed in the [list-playlists](#list-playlists) command. These playlist 
groups are configured under the [subscriptions.playlists] section of the configuration file.


```toml
[subscriptions.playlists]
# IRL ANGEL, Twin Peaks Vibes, Folk Fabrique,
# FADO PORTUGAL, While You Work
quiet = ["37i9dQZF1DX7Ocjwy96xTX", "38rrtWgflrw7grB37aMlsO", "37i9dQZF1DX62XscWX9t6h",
"67waO0NR8HTySxtB7wfMBZ", "6bUIofrj5PWNIeb67DbUqf"]
# Japanese Shoegaze, Modern Psychedelia, Adrenaline Coding
noisy = ["2uiYiQFpynkWCpIXcBGir9", "37i9dQZF1DX8gDIpdqp1XJ", "3JEvwuKbVKoggEA75gWqET"]
# State of Jazz, Jazz-Funk, Jazz Funk (Instrumental),
# Jazz Funk & Groove
jazz = ["37i9dQZF1DX7YCknf2jT6s", "37i9dQZF1DWUb0uBnlJuTi", "4xRrCdkn4r5lrDOElek5oC",
"2puFFdGTID0iJdQtjLvhal"]
```

# Commands

The installation script puts the command `spotcrates` in your Python environment
(e.g. `/.pyenv/shims/spotcrates`). The command `spotcrates commands` lists all of the 
commands available along with a short description of each.

Note that Spotcrates will accept the shortest unique command substring, so for example you can run
`spotcrates sub` for the `subscriptions` command.

## daily
`spotcrates daily` collects the contents of the "Daily Mix" playlists, filters them 
against an exclusion list ("Overplayed" by default), and adds them to the end of 
a target list ("Now" by default).

## subscriptions
`spotcrates subscriptions` adds new tracks from configured playlists to the target playlist, 
filtering for excluded entries. Three days is the default maximum age for a track to be 
considered "new."

## list-playlists
`spotcrates list-playlists` lists playlists' name, owner, track count, and description.
The command accepts `-f` for filter expressions and `-s` for sort expressions. (TODO: 
add description of filter and search expressions and link to it here)

### Search Patterns

The command `list-playlists` accepts search filters passed via the `-f` option. Multiple
filter expressions are separated by commas.

#### Search Examples

`spotcrates li -f jazz`

List playlists where any field contains the string "jazz" (case-insensitive)

```
PLAYLIST NAME                    SIZE  ID                       OWNER            DESCRIPTION
Jazz Piano Classics              100   37i9dQZF1DX5q7wCXFrkHh   spotify          The classic piano recordings in Jazz. Cover: Oscar Peterson
Acid Jazz                        90    37i9dQZF1DWXHghfFFOaS6   spotify          Where hip-hop and soul meets jazz. Cover: Digable Planets
Jazz Funk                        6     61Q9DgzF3f1ULr3i1uRyUy   cmayes3          
Acid Jazz                        3     1h6rEPX9qRpBCBbjuAysMz   cmayes3          
General Jazz                     513   1j6ndSnyYn6oUlnwpGiRWc   cmayes3          
Jazz Funk (Instrumental)         272   4xRrCdkn4r5lrDOElek5oC   1226030890       
Instrumental Acid Jazz Mix       50    37i9dQZF1EIgnEnn8SKPjM   spotify          Instrumental Acid Jazz music picked just for you
State of Jazz                    100   37i9dQZF1DX7YCknf2jT6s   spotify          New jazz for open minds. Cover: Walter Smith III
Jazz-Funk                        200   37i9dQZF1DWUb0uBnlJuTi   spotify          Jazz. But funky. Cover: Takuya Kuroda
Jazz                             1     6VH2cw8n115fbQ7Ls2wzdR   cmayes3          
FaLaLaLaLa GREAT BIG Christmas V 4051  6A2Kj9cWUpuu0UcEbWVf5E   kingofjingaling  Over 170 hours of classic Christmas music. The focus is on classic Christma
```

`spotcrates li -f o:spotify,n:rise`

List playlists where the owner contains `spotify` and name contains `rise`.

```
PLAYLIST NAME                    SIZE  ID                       OWNER            DESCRIPTION
Rise                             230   37i9dQZF1DWUOhRIDwDB7M   spotify          Positive and uplifting ambient instrumental tracks.
```

`spotcrates li -f n:ends:villains`

List playlists where name ends with `villains`.

```
PLAYLIST NAME                    SIZE  ID                       OWNER            DESCRIPTION
classical music for villains     66    0zkl7eKzuUit1QRPVKtga2   225uye2hek5id23t 
```

#### Search Fields

The default search field is `all`.

- spotify_id
- playlist_name
- size
- owner
- playlist_description
- all: Search any/all of the above fields.

#### Search Types

The default search type is `contains`.

- contains
- equals
- starts
- ends
- greater
- less
- greater_equal
- less_equal

### Sort Patterns

The command `list-playlists` accepts sort filters passed via the `-s` option. Multiple
sort expressions are separated by commas.

#### Sort Examples

`spotcrates li -f n:jazz -s name`

Name contains `jazz`; sort by name ascending.

```
PLAYLIST NAME                    SIZE  ID                       OWNER            DESCRIPTION
Acid Jazz                        90    37i9dQZF1DWXHghfFFOaS6   spotify          Where hip-hop and soul meets jazz. Cover: Digable Planets
Acid Jazz                        3     1h6rEPX9qRpBCBbjuAysMz   cmayes3          
General Jazz                     513   1j6ndSnyYn6oUlnwpGiRWc   cmayes3          
Instrumental Acid Jazz Mix       50    37i9dQZF1EIgnEnn8SKPjM   spotify          Instrumental Acid Jazz music picked just for you
Jazz                             1     6VH2cw8n115fbQ7Ls2wzdR   cmayes3          
Jazz Funk                        6     61Q9DgzF3f1ULr3i1uRyUy   cmayes3          
Jazz Funk (Instrumental)         272   4xRrCdkn4r5lrDOElek5oC   1226030890       
Jazz Piano Classics              100   37i9dQZF1DX5q7wCXFrkHh   spotify          The classic piano recordings in Jazz. Cover: Oscar Peterson
Jazz-Funk                        200   37i9dQZF1DWUb0uBnlJuTi   spotify          Jazz. But funky. Cover: Takuya Kuroda
State of Jazz                    100   37i9dQZF1DX7YCknf2jT6s   spotify          New jazz for open minds. Cover: Walter Smith III
```

`spotcrates li -f jazz,size:ge:100 -s size:desc`

Any field contains `jazz`; size is greater than or equal to 100, sort by size descending.

```
PLAYLIST NAME                    SIZE  ID                       OWNER            DESCRIPTION
FaLaLaLaLa GREAT BIG Christmas V 4051  6A2Kj9cWUpuu0UcEbWVf5E   kingofjingaling  Over 170 hours of classic Christmas music. The focus is on classic Christma
General Jazz                     513   1j6ndSnyYn6oUlnwpGiRWc   cmayes3          
Jazz Funk (Instrumental)         272   4xRrCdkn4r5lrDOElek5oC   1226030890       
Jazz-Funk                        200   37i9dQZF1DWUb0uBnlJuTi   spotify          Jazz. But funky. Cover: Takuya Kuroda
Jazz Piano Classics              100   37i9dQZF1DX5q7wCXFrkHh   spotify          The classic piano recordings in Jazz. Cover: Oscar Peterson
State of Jazz                    100   37i9dQZF1DX7YCknf2jT6s   spotify          New jazz for open minds. Cover: Walter Smith III
```

#### Sort Types

The default sort type is `ascending`, i.e. a-z.

- ascending
- descending

## randomize
`spotcrates randomize (playlist1) (playlist2)...` randomizes the playlists with the given names, 
IDs, or in the given collections. 

## copy
`spotcrates copy (source) (dest)` copies a playlist into a new playlist. You may optionally specify 
a destination playlist name; the default is to name the destination based on the source name with
the general form `f"{source_name}-{count:02d}"`.

## commands
`spotcrates commands` displays a summary of the available commands.