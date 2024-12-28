import json
from backend.spotify_client import SpotifyClient
from appleclient import AppleClient
from datetime import datetime, timedelta, timezone
from groupy.client import Client
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from applemusicpy import AppleMusic


def get_spotify_playlist_id(sp, playlist_name):

    # Get the current user's profile information
    user_id = sp.me()["id"]

    # Search for playlists by name
    playlists = sp.user_playlists(user=user_id)
    playlists

    # Iterate through the playlists to find the matching playlist
    for playlist in playlists["items"]:
        if playlist["name"] == playlist_name:
            return playlist["id"]
        else:
            print("Playlist not found.")
            return None


def fetch_spotify_playlist_tracks(sp, playlist_name):

    # Get playlist id
    playlist_id = get_spotify_playlist_id(sp, playlist_name)

    # Fetch the tracks from the Spotify playlist
    playlist_tracks = sp.playlist_tracks(playlist_id=playlist_id)
    return playlist_tracks["items"]


def search_apple_music(amp, track_name):
    results = amp.search(term=track_name, limit=1)
    # If no track found, return None
    return results


def convert_to_apple_music(amp, spotify_tracks):
    apple_music_tracks = []
    for track in spotify_tracks:
        spotify_track_name = track["track"]["name"]
        print(spotify_track_name)
        # Search for the corresponding track on Apple Music
        apple_track = search_apple_music(amp, spotify_track_name)
        print(apple_track)
        if apple_track:
            apple_music_tracks.append(apple_track)
    return apple_music_tracks


def create_apple_music_playlist(apple_music_tracks):
    # Create a new playlist on Apple Music with the fetched tracks
    # You'll need to implement this part using Apple Music API or third-party libraries
    pass


def main(spotify_playlist_name):
    # Spotify/Spotipy Clients
    spotify_client = SpotifyClient("../Auth-Text-Files/SpotifyAuth.txt")
    sp = Spotify(
        auth_manager=SpotifyOAuth(
            client_id=spotify_client.client_id,
            client_secret=spotify_client.client_secret,
            redirect_uri=spotify_client.redirect_uri,
            scope=spotify_client.scope,
        )
    )

    # Fetch tracks from Spotify playlist
    spotify_tracks = fetch_spotify_playlist_tracks(sp, spotify_playlist_name)

    # Apple Music/ applemusicpy Clients
    apple_client = AppleClient("../Auth-Text-Files/AppleMusicAuth.txt")
    amp = AppleMusic(
        secret_key=apple_client.secret_key,
        key_id=apple_client.key_id,
        team_id=apple_client.team_id,
    )
    convert_to_apple_music(amp, spotify_tracks)


if __name__ == "__main__":
    spotify_playlist_name = "Test Playlist 4"
    main(spotify_playlist_name)
