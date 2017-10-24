from playlisp.playlisp import PlayLisp
from optparse import OptionParser
import playlisp.parser.parser as P


def main():
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename",
                      help="Load script from FILE", metavar="FILE")

    (options, args) =  parser.parse_args()

    with open(options.filename, 'r') as script:
        P.run_script(script.read())

    # pl = PlayLisp()
    # playlist_id = input('Paste an input Spotify ID: ')
    # playlist = pl.playlist(playlist_id)
    # p2 = playlist.interleave(playlist).shuffle().collect()
    # print(str(p2))
    # print("Save Playlist")
    # output_playlist_id = input('Paste an output Spotify ID (WARNING: IT WILL BE REPLACED): ')
    # pl.save_on(output_playlist_id, p2)

if __name__ == '__main__':
    main()
