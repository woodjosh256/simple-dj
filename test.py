import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pprint
from playlist import Playlist

import config

scope = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=config.CLIENT_ID, client_secret=config.CLIENT_SECRET, redirect_uri=config.REDIRECT_URI))

pprint.PrettyPrinter().pprint(sp.current_user_playlists())

for playlist in config.PLAYLIST_OPTIONS:
    a = Playlist(playlist, sp)
