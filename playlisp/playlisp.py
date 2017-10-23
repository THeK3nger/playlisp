"""
PlayLisp main module.
"""

from configparser import ConfigParser

import spotipy
import spotipy.util as util


class PlayLisp(object):
    """
    Main application class. It handles and, in the future, abstracts over all the
    PlayLisp functionality
    """

    def __init__(self):
        self._parser = ConfigParser()
        self._parser.read(['./config/default.ini', './config/local.ini'])

        if "Spotify" not in self._parser:
            raise Exception("Wrong configuration file! No `Spotify` section found!")

        if "client_id" not in self._parser["Spotify"]:
            raise Exception("`client_id` is required in the configuration.")
        if "client_secret" not in self._parser["Spotify"]:
            raise Exception("`client_secret` is required in the configuration.")
        if "username" not in self._parser["Spotify"]:
            raise Exception("`username` is required in the configuration.")
        if "redirect_url" not in self._parser["Spotify"]:
            raise Exception("`redirect_url` is required in the configuration.")

        self._client_id = self._parser["Spotify"]["client_id"]
        self._client_secret = self._parser["Spotify"]["client_secret"]
        self._username = self._parser["Spotify"]["username"]
        self._redirect_url = self._parser["Spotify"]["redirect_url"]

        token = self._authorize()

        self._spotify = spotipy.Spotify(auth=token)

    def search(self):
        '''
        Test function for searching using the API
        '''
        results = self._spotify.search(q='weezer', limit=20)
        print(results)

    def playlist(self, playlist_id):
        results = self._spotify.user_playlist_tracks(self._username, playlist_id)
        return results["items"]

    def save_on(self, id, new_playlist):
        tracks = [ x.id for x in new_playlist._tracks ]
        self._spotify.user_playlist_replace_tracks(self._username, id, tracks)

    def _authorize(self):
        return util.prompt_for_user_token(self._username,'playlist-modify-public',self._client_id,self._client_secret,'http://localhost/')

