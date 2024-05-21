import re
import sys
import os
from backend.spotifyclient import SpotifyClient
from datetime import datetime, timedelta, timezone
from groupy.client import Client


def get_all_soundcloud_track_ids(messages):
    spotify_track_ids = []
    for message in messages:
        if message.text:
            urls = re.findall(r"(https?://soundcloud\.com/[^ ]+)", message.text)

            for url in urls:
                track_id = url.split("/")[-1]
                spotify_track_ids.append(track_id)
    return spotify_track_ids
