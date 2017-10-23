from playlisp.playlisp import PlayLisp

def main():
    pl = PlayLisp()
    playlist_id = input('Paste an input Spotify ID: ')
    playlist = pl.playlist(playlist_id)
    p2 = playlist.interleave(playlist).shuffle()
    print(str(p2))
    print("Save Playlist")
    output_playlist_id = input('Paste an output Spotify ID (WARNING: IT WILL BE REPLACED): ')
    pl.save_on(output_playlist_id, p2)

if __name__ == '__main__':
    main()
