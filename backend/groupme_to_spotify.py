import re
import sys
import os
from backend.spotifyclient import SpotifyClient
from datetime import datetime, timedelta, timezone
from groupy.client import Client
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth


def get_all_spotify_track_ids(messages):
    spotify_track_ids = []
    for message in messages:
        if message.text:
            urls = re.findall(r"(https://open.spotify.com/track/[\w\d]+)", message.text)
            for url in urls:
                track_id = url.split("/")[-1]
                spotify_track_ids.append(track_id)
    return spotify_track_ids


def get_unique_spotify_track_ids(spotify_track_ids):

    # Sets do not allow duplicate elements, this automatically removes any duplicate ID
    unique_ids = set(spotify_track_ids)
    return unique_ids


def create_spotify_playlist(sp, playlist_name, spotify_track_ids):

    user_id = sp.me()["id"]

    # Create empty playlist
    playlist = sp.user_playlist_create(user_id, playlist_name, public=True)

    # Get unique ids only
    unique_ids = get_unique_spotify_track_ids(spotify_track_ids)

    # Loop to add each track one by one to playlist
    for track_id in unique_ids:
        sp.playlist_add_items(playlist["id"], [track_id])


def main(playlist_name, start_date, end_date):
    # Spotify/Spotipy Clients
    file_path = os.path.abspath("backend/Auth-Text-Files/SpotifyAuth.txt")
    spotify_client = SpotifyClient(file_path)
    sp = Spotify(
        auth_manager=SpotifyOAuth(
            client_id=spotify_client.client_id,
            client_secret=spotify_client.client_secret,
            redirect_uri=spotify_client.redirect_uri,
            scope=spotify_client.scope,
        )
    )

    # Groupme Client
    GROUPME_TOKEN = "4We4OiSLGXghh2ooSMUkFfVaB6AdXJG8sE98VWs9"
    groupme_client = Client.from_token(GROUPME_TOKEN)
    group = groupme_client.groups.get(
        "86830992"
    )  # Replace 'your_group_id' with the actual group ID

    # Convert start and end dates to datetime objects
    start_datetime = datetime.strptime(start_date, "%Y-%m-%d").replace(
        tzinfo=timezone.utc
    )
    end_datetime = datetime.strptime(end_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)

    # Filter messages to only include those within the specified date range
    messages = group.messages.list().autopage()
    relevant_messages = [
        message
        for message in messages
        if start_datetime
        <= message.created_at.replace(tzinfo=timezone.utc)
        <= end_datetime
    ]

    # Get track ids from all messages
    track_ids = get_all_spotify_track_ids(relevant_messages)

    # Create playlist
    playlist_name = playlist_name
    create_spotify_playlist(sp, playlist_name, track_ids)


if __name__ == "__main__":
    playlist_name = sys.argv[1]
    start_date = sys.argv[2]
    end_date = sys.argv[3]
    print("Playlist name:", playlist_name)
    print("Start date:", start_date)
    print("End date:", end_date)
    main(playlist_name, start_date, end_date)
