import requests


class groupmeClient:
    REQUIRED_VARIABLES = {"token", "group_id"}

    def __init__(self, file_path):
        self.token = None
        self.group_id = None
        self.read_auth_text_file(file_path)

    def read_auth_text_file(self, file_path):

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

    def get_group_message_count(self):
        """
        Fetches the total message count for a GroupMe group using the GroupMe API.

        :param access_token: Your GroupMe API access token.
        :param group_id: The ID of the GroupMe group.
        :return: Total message count or an error message.
        """
        url = f"https://api.groupme.com/v3/groups/{self.group_id}"
        params = {"token": self.token}

        response = self.get_request(url, params)

        if "error" in response:
            return response["error"]

        return response["response"]["messages"]["count"]

    def get_group(self):
        """
        Fetches the total message count for a GroupMe group using the GroupMe API.

        :param access_token: Your GroupMe API access token.
        :param group_id: The ID of the GroupMe group.
        :return: Total message count or an error message.
        """
        url = f"https://api.groupme.com/v3/groups/{self.group_id}"
        params = {"token": self.token}

        response = self.get_request(url, params)

        if "error" in response:
            return response["error"]

        return response["response"]

    def get_group_messages(
        self, limit=20, before_id=None, since_id=None, after_id=None
    ):
        """get groupme messages based on passed params

        Args:
            limit (integer): Number of messages returned. Default is 20. Max is 100.
            before_id (string): Returns messages created before the given message ID
            since_id (string): Returns most recent messages created after the given message ID
            after_id (string): Returns messages created immediately after the given message ID


        Returns:
            (dict): python dictonary containing messages list
        """
        url = f"https://api.groupme.com/v3/groups/{self.group_id}/messages"
        params = {"token": self.token}

        if limit:
            params["limit"] = limit
        if before_id:
            params["before_id"] = before_id
        if since_id:
            params["since_id"] = since_id
        if after_id:
            params["after_id"] = after_id

        response = self.get_request(url, params)

        if "error" in response:
            return response["error"]

        return response["response"]["messages"]

    def get_request(self, url, params):
        """
        Makes a GET request to the given URL with the provided parameters.

        :param url: The URL to send the GET request to.
        :param params: A dictionary of query parameters for the request.
        :return: Parsed JSON response if successful, or an error message.
        """
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            return response.json()  # Return the parsed JSON response
        except requests.exceptions.RequestException as e:
            return {"error": f"An error occurred: {e}"}
