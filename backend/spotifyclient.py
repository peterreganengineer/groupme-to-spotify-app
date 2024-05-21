class SpotifyClient:
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
