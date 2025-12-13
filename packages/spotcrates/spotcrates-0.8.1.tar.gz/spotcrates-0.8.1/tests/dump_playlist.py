from pathlib import Path

from spotcrates.common import get_spotify_handle, get_config, get_all_items

config = get_config(Path("/home/cmayes/.config/spotcrates/spotcrates_config.toml"))

sp = get_spotify_handle(config)

items = get_all_items(sp, sp.playlist_items("37i9dQZF1EP6YuccBxUcC1"))

print(items)
