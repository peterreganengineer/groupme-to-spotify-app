import sys
import time
import os
import mysql.connector
from dotenv import load_dotenv
from spotify_client import SpotifyClient
from datetime import datetime, timezone
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

# Load environment variables from .env file
load_dotenv()


def get_all_spotify_song_ids(mydb, start_date, end_date):
    """Query database holding groupme messages to get all spotify songs based on a data range.

    Args:
        mydb (mysql database): mysql database to connect to
        start_date (date): start date range format YYYY-MM-DD
        end_date (date): end date range format YYYY-MM-DD

    Returns:
        set: set of unqiue spotify song ids
    """
    # Convert start and end dates to datetime objects
    start_datetime = datetime.strptime(start_date, "%Y-%m-%d").replace(
        tzinfo=timezone.utc
    )
    end_datetime = datetime.strptime(end_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)

    mycursor = mydb.cursor()

    # Query for all song links
    get_spotify_songs_query = "SELECT text FROM groupme.message WHERE is_song AND created_at < %s AND created_at > %s"

    mycursor.execute(
        get_spotify_songs_query,
        (end_datetime, start_datetime),
    )
    spotify_song_urls = mycursor.fetchall()

    # Set so unique ids only to avoid dupes added to playlist
    spotify_song_urls = [song[0] for song in spotify_song_urls]
    
    # Get songIds from spotify urls
    spotify_song_ids = []
    for url in spotify_song_urls:
        id = url.split("/")[-1].split("?")[0]
        spotify_song_ids.append(id)

    return set(spotify_song_ids)


def create_spotify_playlist(sp, playlist_name, spotify_song_ids):
    """Create a spotify playlist given a playlist name and a list of valid spotify song ids.

    Args:
        sp (spotipy): _description_
        playlist_name (string): playlist name
        spotify_song_ids (list): list of valid spotfiy ids ex: 1aUnILXf9hIRbCqQUpqihD
    """

    user_id = sp.me()["id"]

    # Create empty playlist
    playlist = sp.user_playlist_create(user_id, playlist_name, public=True)
    print("Playlist Created: " + playlist["name"])

    # Loop to add each song one by one to playlist
    for song_id in spotify_song_ids:
        try:
            add_song = sp.playlist_add_items(playlist["id"], [song_id])
            print("Added Song: " + song_id)
            if "error" in add_song:
                print("Error on Song: " + song_id)
                time.sleep(10)
                add_song = sp.playlist_add_items(playlist["id"], [song_id])
        except:
            print("Error on Song: " + song_id)


def main(playlist_name, start_date, end_date):

    # Spotify/Spotipy Client
    spotify_client = SpotifyClient()
    sp = Spotify(
        auth_manager=SpotifyOAuth(
            client_id=spotify_client.client_id,
            client_secret=spotify_client.client_secret,
            redirect_uri=spotify_client.redirect_uri,
            scope=spotify_client.scope,
        )
    )

    # Set up the connection to database
    mydb = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )

    if mydb.is_connected():
        print("Connected to groupme db")

    # Function call to query and return unique list of spotify songs
    spotify_song_ids = get_all_spotify_song_ids(mydb, start_date, end_date)

    # Function call to create playlist with spotify songs
    create_spotify_playlist(sp, playlist_name, spotify_song_ids)


if __name__ == "__main__":
    playlist_name = sys.argv[1]
    start_date = sys.argv[2]
    end_date = sys.argv[3]
    print("Playlist name:", playlist_name)
    print("Start date:", start_date)
    print("End date:", end_date)
    main(playlist_name, start_date, end_date)
