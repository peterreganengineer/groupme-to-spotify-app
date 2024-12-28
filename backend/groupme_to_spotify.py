import re
import sys
import os
import time
from backend.spotify_client import SpotifyClient
from datetime import datetime, timedelta, timezone
from groupy.client import Client
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth


def get_all_spotify_track_ids(messages):
    spotify_track_ids = []
    for message in messages:
        if message:
            urls = re.findall(r"(https://open.spotify.com/track/[\w\d]+)", message)
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
    # playlist = sp.user_playlist_create(user_id, playlist_name, public=True)

    # Get unique ids only
    unique_ids = get_unique_spotify_track_ids(spotify_track_ids)
    print(len(unique_ids))

    results = sp.playlist_items(
        "200Vt1KP4GTc6Y1GQplTbu",
        None,
        1,
    )
    total = results["total"]
    track_ids = []
    for x in range(0, total, 100):
        results = sp.playlist_items("200Vt1KP4GTc6Y1GQplTbu", None, 100, x)
        tracks = results["items"]
        track_ids = track_ids + [
            item["track"]["id"] for item in tracks if item["track"]
        ]
    print(len(track_ids))

    # Concatenate the lists
    merged_list = unique_ids - set(track_ids)

    # Remove duplicates
    merged_list = set(merged_list)
    print(len(merged_list))

    # Loop to add each track one by one to playlist
    for track_id in merged_list:
        sp.playlist_add_items("200Vt1KP4GTc6Y1GQplTbu", [track_id])
        time.sleep(0.2)


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
    messages = []
    page = group.messages.list(limit=1)
    start_message = group.messages.list()[0]

    outer_loop_broken = False
    while end_datetime <= start_message.created_at.replace(tzinfo=timezone.utc):
        page = group.messages.list(before_id=start_message.id, limit=20)
        start_message = page[19]
        for message in page:
            if end_datetime >= message.created_at.replace(tzinfo=timezone.utc):
                start_message = message
                outer_loop_broken = True
                break
        if outer_loop_broken:
            break
        print(start_message.created_at, flush=True)
        print(start_message.text, flush=True)

    while start_datetime <= start_message.created_at.replace(tzinfo=timezone.utc):
        page = group.messages.list(before_id=start_message.id, limit=20)
        start_message = page[19]
        for message in page:
            messages.append(message.text)
        print(start_message.created_at)
        print(start_message.text)
        time.sleep(0.5)
    # Get track ids from all messages
    track_ids = get_all_spotify_track_ids(messages)

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
