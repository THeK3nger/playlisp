'''
PlayLisp main module.
'''

from configparser import ConfigParser

import spotipy
import spotipy.oauth2 as oauth2


class PlayLisp(object):
    '''
    Main application class. It handles and, in the future, abstracts over all the
    PlayLisp functionalities
    '''

    def __init__(self):
        self._parser = ConfigParser()
        self._parser.read(['./config/default.ini', './config/local.ini'])

        if "client_id" not in self._parser["Spotify"] or \
            "client_secret" not in self._parser["Spotify"]:
            print("ERROR")

        self._client_id = self._parser["Spotify"]["client_id"]
        self._client_secret = self._parser["Spotify"]["client_secret"]

        credentials = oauth2.SpotifyClientCredentials(
            client_id=self._client_id, client_secret=self._client_secret)

        token = credentials.get_access_token()

        self._spotify = spotipy.Spotify(auth=token)

    def search(self):
        '''
        Test function for searching using the API
        '''
        results = self._spotify.search(q='weezer', limit=20)
        print(results)


if __name__ == '__main__':
    pl = PlayLisp()
    pl.search()
