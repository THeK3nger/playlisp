'''
Store information about playlists
'''

from data.track import Track, from_spotify_dto

class PlayList(object):
    
    def __init__(self):
        self._tracks = []

    def add(self, track):
        self._tracks.append(track)

    def __str__(self):
        result = ""
        for i, t in enumerate(self._tracks):
            result +="{} - {} - {} - {}\n".format(i,t.title, t.album, t.artists)
        return result

class SpotifyPlaylist(PlayList):

    def __init__(self):
        super(SpotifyPlaylist, self).__init__()

    @staticmethod
    def from_spotify_dto(spotify_pl_dto):
        result = SpotifyPlaylist()
        for t in spotify_pl_dto:
            result.add(from_spotify_dto(t))
        return result