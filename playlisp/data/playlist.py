"""
Store information about playlists
"""

import itertools
from random import shuffle

from playlisp.data.track import Track, from_spotify_dto


class PlayList(object):
    """
    Represents a generic playlist
    """

    def __init__(self):
        self._tracks = []

    def add(self, track):
        """
        Add a Track to the the playlist
        :param track:
        :type track: Track
        :return:
        :rtype: PlayList
        """
        # TODO: Make the playlist collapse every generator.
        self.collect()
        self._tracks.append(track)
        self._tracks = iter(self._tracks)

    def collect(self):
        """
        Finally collapse every pending operation on the tracks.abs
        :rtype: PlayList
        """
        self._tracks = list(self._tracks)
        return self

    def shuffle(self):
        """
        Shuffle the playlist
        :return:
        :rtype: PlayList
        """
        # TODO: Make the playlist collapse every generator.
        self.collect()
        new_pl = PlayList()
        new_pl._tracks = self._tracks
        shuffle(new_pl._tracks)
        return new_pl

    def take(self, n):
        """
        Create a new playlist with the first n elements.
        :param n:
        :type n: int
        :return:
        :rtype: PlayList
        """
        new_pl = PlayList()
        new_pl._tracks = itertools.islice(self._tracks, n)
        return new_pl

    def drop(self, n):
        """
        Create a new playlist with  the first n elements dropped.
        :param n:
        :type n: int
        :return:
        :rtype: PlayList
        """
        new_pl = PlayList()
        new_pl._tracks = next(itertools.islice(self._tracks, n, n), None)
        return new_pl

    def interleave(self, other):
        """
        Create a new playlist by mixing self and other.
        :param other: A different playlist.
        :type other: PlayList
        :return:
        :rtype: PlayList
        """
        new_pl = PlayList()
        if self._tracks == other._tracks:
            new_pl._tracks = _bicycle(self._tracks)
        else:
            new_pl._tracks = _roundrobin(self._tracks, other._tracks)
        return new_pl

    def subtract(self, other):
        """
        Create a new playlist with all the tracks in self without the tracks in other.
        :param other: A different playlist.
        :type other: PlayList
        :return:
        :rtype: PlayList
        """
        new_pl = PlayList()
        new_pl._tracks = itertools.filterfalse(lambda x: x not in other._tracks, self._tracks)
        return new_pl

    def filter(self, pred):
        new_pl = PlayList()
        new_pl._tracks = itertools.filterfalse(pred, self._tracks)
        return new_pl

    def __str__(self):
        self.collect()
        result = ""
        for i, t in enumerate(self._tracks):
            result += "{} - {} - {} - {}\n".format(i, t.title, t.album, t.artists)
        return result


class SpotifyPlaylist(PlayList):
    """
    Represent a Spotify playlist
    """

    def __init__(self):
        super(SpotifyPlaylist, self).__init__()

    @staticmethod
    def from_spotify_dto(spotify_pl_dto):
        """
        Creates a playlist from a raw playlist DTO from Spotify APIs.
        :param spotify_pl_dto:
        :type spotify_pl_dto: dict
        :return:
        :rtype: SpotifyPlaylist
        """
        result = SpotifyPlaylist()
        for t in spotify_pl_dto:
            result.add(from_spotify_dto(t))
        return result


# Utils
def _roundrobin(*iterables):
    "roundrobin('ABC', 'D', 'EF') --> A D E B F C"
    # Recipe credited to George Sakkis
    pending = len(iterables)
    nexts = itertools.cycle(iter(it).__next__ for it in iterables)
    while pending:
        try:
            for next in nexts:
                yield next()
        except StopIteration:
            pending -= 1
            nexts = itertools.cycle(itertools.islice(nexts, pending))


def _bicycle(iterable, repeat=2):
    for item in iterable:
        for _ in range(repeat):
            yield item
