class AppleClient:
    REQUIRED_VARIABLES = {"team_id", "key_id"}
    SECRET_KEY = """-----BEGIN PRIVATE KEY-----
MIGTAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBHkwdwIBAQQgeHszMFN1GvYxlqf7
YljB72wYKB7sJCb7m8353X231Z+gCgYIKoZIzj0DAQehRANCAASQtzqRK1vJRD41
gNSG0xd/1s7vcza/t55gDUFMvWIwB8mgJqKDJmXJrv5Z1NU4lylPOiHypPEe9Vwl
PnBJDyIt
-----END PRIVATE KEY-----"""

    def __init__(self, file_path):
        self.team_id = None
        self.key_id = None
        self.secret_key = self.SECRET_KEY
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
