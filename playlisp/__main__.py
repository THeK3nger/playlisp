from playlisp.playlisp import PlayLisp
from playlisp.data.playlist import SpotifyPlaylist

if __name__ == '__main__':
    pl = PlayLisp()
    playlist = SpotifyPlaylist.from_spotify_dto(pl.playlist())
    p2 = playlist.interleave(playlist).shuffle()
    print(str(p2))