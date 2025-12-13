import json

import spotipy

from spotcrates.playlists import Playlists


def get_spotify_handle():
    cache_handler = spotipy.cache_handler.CacheFileHandler()
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler, scope=["playlist-modify-private",
                                                                                   "playlist-read-private"])
    return spotipy.Spotify(auth_manager=auth_manager)


def print_all_playlists():
    sp = get_spotify_handle()

    playlists = sp.current_user_playlists()
    while playlists:
        for key, value in playlists.items():
            print(f"Playlists entry: {key} -> {value}")
        for i, playlist in enumerate(playlists['items']):
            for key, value in playlist.items():
                print(f"Playlist entry: {key} -> {value}")
            print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'], playlist['name']))
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None


def run_append_daily():
    sp = get_spotify_handle()

    playlists = Playlists(sp)
    playlists.append_daily_mix()


def run_list_all():
    sp = get_spotify_handle()

    playlists = Playlists(sp)
    print(json.dumps(playlists.get_all_playlists()))


def print_tracks():
    sp = get_spotify_handle()

    playlist_items = sp.playlist_items("20HoheMV2htBPBX07D8pHm")
    print_playlist_page(playlist_items)

    # next_playlist_page = sp.next(playlist_items)
    # print_playlist_page(next_playlist_page)

    track_ids = {playlist_item['track']['id'] for playlist_item in playlist_items['items']}

    next_playlist_page = sp.next(playlist_items)
    while next_playlist_page:
        track_ids.update({playlist_item['track']['id'] for playlist_item in next_playlist_page['items']})
        next_playlist_page = sp.next(next_playlist_page)

    print(f"Track IDs type: {type(track_ids)}")
    print(f"Track IDs size: {len(track_ids)}")
    print(f"Track IDs: {track_ids}")
    # for i, playlist_item in enumerate(playlist_items['items']):
    #     print("=====================%4d %s %s=====================" % (i + 1, playlist_item['added_at'],
    #                                                                    playlist_item['track']['id']))

    # track = playlist_item['track']
    # for key, value in track.items():
    #     print(f"Track entry: {key} -> {value}")
    #
    #
    # for key, value in playlist_item.items():
    #     print(f"Playlist item entry: {key} -> {value}")


def print_playlist_page(playlist_items):
    for key, value in playlist_items.items():
        # print(f"Playlists key: {key}")
        # print(f"Playlists key: {type(key)}")
        # print(f"{key} == 'items'? {key == 'items'}")
        if key == 'items':
            print("Skipping items")
            continue
        print(f"Playlists Item: {key} -> {value}")


if __name__ == '__main__':
    # print_all_playlists()
    # print_tracks()
    run_append_daily()
    #run_list_all()
