import time
import jwt
import requests


class AppleClient:
    """Client for communicating with apple apis"""

    REQUIRED_VARIABLES = {"key_id", "team_id"}

    def __init__(self, ids_file, private_key_file):
        self.key_id = None
        self.team_id = None
        self.read_auth_text_file(ids_file, private_key_file)

    def read_auth_text_file(self, ids_file, private_key_file):
        """read auth text files to auth with apple apis

        Args:
            ids_file (string): file path to the key_id and team_id
            private_key_file (string): file path to the apple music secret key

        """
        with open(private_key_file, "r") as f:
            self.secret_key = f.read()

        # Open txt file
        with open(ids_file, "r") as file:
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

    def generate_token(self):
        """generates jwt token to be used fo apple music api calls

        Returns:
            token: jwt token
        """
        headers = {"kid": self.key_id, "typ": "JWT", "alg": "ES256"}

        payload = {
            "iss": self.team_id,
            "iat": int(time.time()),
            "exp": int(time.time()) + 3600,  # Token is valid for 1 hour
        }

        token = jwt.encode(payload, self.secret_key, algorithm="ES256", headers=headers)
        return token

    def search_apple_music(self, jwt_token, term, limit=1):
        """searchs for a single song in apple music

        Args:
            jwt_token (string): the jwt auth token (generated from generate_token)
            term (string): the song title to search for
            limit (int, optional): number of results to return from search. Defaults to 1.

        Returns:
            response (json): the json body response of the apple music search request
        """
        url = f"https://api.music.apple.com/v1/catalog/us/search"
        headers = {
            "Authorization": f"Bearer {jwt_token}",
        }
        params = {
            "term": term,
            "limit": limit,
            "types": "songs",
        }

        response = requests.get(url, headers=headers, params=params)
        return response.json()

    def create_library_playlist(self, jwt_token, music_user_token, name, description):
        """create a single library playlist

        Args:
            jwt_token (string): the jwt auth token (generated from generate_token)
            term (dict): A dictionary that includes strings for the name and description of the new playlist.

        Returns:
            response (json): the json body response of the apple music playlist creation
        """
        url = f"https://api.music.apple.com/v1/me/library/playlists"
        headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Music-User-Token": music_user_token,
        }
        params = {
            "attributes": {
                "description": {"standard": description},
                "name": name,
            }
        }

        response = requests.post(url, headers=headers, params=params)
        return response.json()
