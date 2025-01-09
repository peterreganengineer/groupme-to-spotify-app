import sys
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth


class SpotifyClient:
    """Client for communicating with spotify apis"""

    REQUIRED_VARIABLES = {
        "client_id",
        "client_secret",
        "redirect_uri",
        "username",
        "scope",
    }

    def __init__(self, file_path):
        self.client_id = None
        self.client_secret = None
        self.redirect_uri = None
        self.username = None
        self.scope = None
        self.read_auth_text_file(file_path)

    def read_auth_text_file(self, file_path):
        """read spotify auth text files to call spotify apis

        Args:
            file_path (string): location of the spotify auth files

        Raises:
            ValueError: raises error if the file is missing one of the required variables above
        """
        # Open txt file
        with open(file_path, "r") as file:
            lines = file.readlines()

        # Read each line in txt file
        for line in lines:
            parts = line.strip().split("=")
            if len(parts) == 2:
                var_name = parts[0].strip()
                var_value = parts[1].strip()
                if var_name in self.REQUIRED_VARIABLES:
                    setattr(self, var_name, var_value)

        # Check if all required variables are present
        missing_variables = [
            var for var in self.REQUIRED_VARIABLES if getattr(self, var) is None
        ]
        if missing_variables:
            raise ValueError(
                f"Missing required variables: {', '.join(missing_variables)}"
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
