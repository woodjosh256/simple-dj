import random

import remi.gui as gui
from remi import start, App
import config
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from playlist import Playlist


class MyApp(App):

    def __init__(self, *args):
        super(MyApp, self).__init__(*args)
        self.added_song = False

    def _gather_playlists(self):
        scope = "user-library-read, user-modify-playback-state, user-read-playback-state"

        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(scope=scope, client_id=config.CLIENT_ID, client_secret=config.CLIENT_SECRET,
                                      redirect_uri=config.REDIRECT_URI))
        self.playlists = []

        for uri in config.PLAYLIST_OPTIONS:
            self.playlists.append(Playlist(uri, self.sp))

        self.playlist_ratios = {}
        for playlist in self.playlists:
            self.playlist_ratios[playlist] = 0

    def main(self):
        self._gather_playlists()
        self.played_songs = []  # list of already played song URIs

        container = gui.VBox(width=360, height=640)

        gui_elements = []
        self.input_map = {}  # textInput => playlistObject

        self.title = gui.Label('DJ Roomba')
        gui_elements.append(self.title)

        for playlist in self.playlists:
            label = gui.Label(playlist.name)
            gui_elements.append(label)

            text_input = gui.TextInput()
            text_input.set_text("0")
            text_input.onchange.connect(self.update_playlist_ratio)
            self.input_map[text_input] = playlist
            gui_elements.append(text_input)

        for gui_element in gui_elements:
            container.append(gui_element)

        # returning the root widget
        return container

    def idle(self):
        state = self.sp.current_playback()
        if state:
            percent_complete = state["progress_ms"] / state["item"]["duration_ms"]
            if percent_complete >= .85 and not self.added_song:
                self.added_song = True
                self.add_song()
            if percent_complete < .85:
                self.added_song = False

    def update_playlist_ratio(self, widget, new_value, ):
        for textInput in self.input_map.keys():
            playlist = self.input_map[textInput]
            val = textInput.get_value().strip()
            try:
                val = int(val)
            except ValueError:
                return
            self.playlist_ratios[playlist] = val
        print("updated playlist ratio")

    def add_song(self):
        possible_playlists = []
        for playlist in self.playlist_ratios:
            possible_playlists.extend(
                [playlist for i in range(self.playlist_ratios[playlist])]
            )
        if len(possible_playlists) == 0:
            return
        chosen_playlist = random.choice(possible_playlists)
        unplayed = [track for track in chosen_playlist.tracks if track not in self.played_songs]
        if len(unplayed) == 0:
            return
        track = random.choice(unplayed)
        self.sp.add_to_queue(track)
        self.played_songs.append(track)


# starts the web server
start(MyApp, address='192.168.0.2', port=8081)
