import sys
import os
from dotenv import load_dotenv
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

# Load environment variables from .env file
load_dotenv()


class SpotifyClient:
    """Client for communicating with spotify apis"""

    REQUIRED_VARIABLES = {
        "client_id",
        "client_secret",
        "redirect_uri",
        "username",
        "scope",
    }

    def __init__(self):
        self.client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        self.redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")
        self.username = os.getenv("SPOTIFY_USERNAME")
        self.scope = os.getenv("SPOTIFY_SCOPE")
        self._validate_required_variables()

    def _validate_required_variables(self):
        """Validate that all required environment variables are set.

        Raises:
            ValueError: raises error if any required variable is missing
        """
        missing_variables = [
            var for var in self.REQUIRED_VARIABLES if getattr(self, var) is None
        ]
        if missing_variables:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_variables)}"
            )

    def get_spotify_playlist_id(self, sp, playlist_name):
        """get a spotify playlist id given its name

        Args:
            sp (spotipy): spotipy python library instance
            playlist_name (string): name of playlist to fetch id from

        Returns:
            string: the id of the playlist
        """
        # Get the current user's profile information
        user_id = sp.me()["id"]

        # Search for playlists by name
        playlists = sp.user_playlists(user=user_id, limit=50, offset=0)

        # Iterate through the playlists to find the matching playlist

        print(playlist_name, file=sys.stderr)

        for playlist in playlists["items"]:
            print(playlist["name"])
            if playlist["name"] == playlist_name:
                return playlist["id"]

        return None

    def fetch_spotify_playlist_tracks(self, sp, playlist_name):
        """fetch all tracks from a spotify playlist

        Args:
            sp (spotipy): spotipy python library instance
            playlist_name (string): name of playlist to fetch tracks from

        Returns:
            list: list containing all tracks from given playlist
        """

        # Get playlist id
        playlist_id = self.get_spotify_playlist_id(sp, playlist_name)

        if playlist_id is not None:
            # Fetch the tracks from the Spotify playlist
            playlist_tracks = sp.playlist_tracks(playlist_id=playlist_id)
            playlist_tracks = playlist_tracks["items"]
            tracks_final = [
                {
                    "name": track["track"]["name"],
                    "artists": [artist["name"] for artist in track["track"]["artists"]],
                }
                for track in playlist_tracks
            ]

            return tracks_final
        else:
            print("Playlist not found.")
            return None
