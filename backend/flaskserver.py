import os
from flask import Flask, jsonify, request
from flask_cors import CORS  # Import the CORS module
from appleclient import AppleClient
from spotifyclient import SpotifyClient
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)
CORS(app)

# file paths for authentication
SPOTIFY_AUTH_FILE_PATH = os.path.abspath("backend/Auth-Text-Files/SpotifyAuth.txt")
IDS_PATH = os.path.abspath("backend/Auth-Text-Files/AppleMusicAuth.txt")
PRIVATE_KEY_PATH = os.path.abspath("backend/Auth-Text-Files/AppleMusicSecretKey.txt")


@app.route("/developer-token")
def get_developer_token():
    """Get apple developer token to pass to apis

    Returns:
        string: developer token
    """
    apple_client = AppleClient(IDS_PATH, PRIVATE_KEY_PATH)
    developer_token = apple_client.generate_token()
    return jsonify(developer_token=developer_token)


@app.route("/spotify-tracks")
def get_spotify_tracks_from_playlist():
    """Returns a list of all songs in a given spotify playlist

    Args:
        playlistName (string): name of the playlist to search for

    Returns:
        list: list of spotify songs
    """
    spotify_client = SpotifyClient(SPOTIFY_AUTH_FILE_PATH)
    sp = Spotify(
        auth_manager=SpotifyOAuth(
            client_id=spotify_client.client_id,
            client_secret=spotify_client.client_secret,
            redirect_uri=spotify_client.redirect_uri,
            scope=spotify_client.scope,
        )
    )
    return spotify_client.fetch_spotify_playlist_tracks(
        sp, request.args.get("playlistName")
    )


if __name__ == "__main__":
    app.run(debug=True)
