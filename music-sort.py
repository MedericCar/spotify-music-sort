import pprint
import sys
import spotipy  # la librairie pour manipuler l'api spotify
import spotipy.util as util
import simplejson as json  # pour manipuler les réponses json
import time  # pour créer une playlist horodatée
from datetime import datetime


# Given by Spotify
clientId = "xxxx"
clientSecret = "xxxx"

if len(sys.argv) > 1:
    username = sys.argv[1]
    playlist_name = sys.argv[2]
else:
    print("Usage: %s username playlist" % (sys.argv[0],))
    sys.exit()

scope = 'playlist-read-private, playlist-modify-private, playlist-modify-public'
token = util.prompt_for_user_token(username, scope, client_id=clientId, client_secret=clientSecret, redirect_uri='http://localhost/')


if token:
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    playlists = sp.current_user_playlists(limit=50)
    for item in playlists['items']:
        if item['name'] == playlist_name:
            uri = item['uri']
            uri_playlist_id = uri.split(':')[2]
            playlist = sp.user_playlist(username, uri_playlist_id, fields='tracks, items')
            tracks = playlist['tracks']['items']
            new_playlist_dic = dict()
            for track in tracks:
                feature = sp.audio_features(track['track']['id'])[0]
                coefficient = (feature["danceability"] + feature["valence"]) / 2
                new_playlist_dic[coefficient] = track['track']['id']
                print(track['track']['name'], coefficient)
            track_ids = []
            for key in sorted(new_playlist_dic.keys(), reverse=True):
                track_ids.append(new_playlist_dic[key])
            playlist_name2 = playlist_name + ' sorted'
            new_playlist = sp.user_playlist_create(username, playlist_name2)
            sp.user_playlist_add_tracks(username, new_playlist['id'], track_ids)
            break
else:
    print("Can't get token for", username)
