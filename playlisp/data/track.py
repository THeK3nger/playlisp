"""
Store information about playlist's tracks.
"""

import collections

Track = collections.namedtuple('Track', ['id', 'title', 'artists', 'album'])


def from_spotify_dto(track_dto):
    track = track_dto["track"]

    return Track(
        id=track["id"],
        title=track["name"],
        artists=[x["name"] for x in track["artists"]],
        album=track["album"]["name"])
