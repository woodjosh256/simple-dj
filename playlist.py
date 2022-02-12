import pprint

import spotipy


class Playlist:

    def __init__(self, uri, sp: spotipy.Spotify):
        self.uri = uri
        playlist = sp.playlist(uri)
        self.name = playlist["name"]
        track_num = playlist['tracks']['total']
        self.tracks = []

        for offset in range(0, track_num, 50):
            tracks = sp.playlist_tracks(uri, offset=offset, limit=50)
            # pprint.PrettyPrinter().pprint(tracks)
            for track in tracks['items']:
                self.tracks.append(track['track']['id'])


    def __str__(self):
        return f"name: {self.name} tracks: {len(self.tracks)}"

    def __repr__(self):
        return self.__str__()
