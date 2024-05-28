from flask import Flask, jsonify
from flask_cors import CORS  # Import the CORS module
from appleclient import AppleClient

app = Flask(__name__)
CORS(app)

# file paths for authentication
IDS_PATH = "../backend/Auth-Text-Files/AppleMusicAuth.txt"
PRIVATE_KEY_PATH = "../backend/Auth-Text-Files/AppleMusicSecretKey.txt"


@app.route("/developer-token")
def get_developer_token():
    apple_client = AppleClient(IDS_PATH, PRIVATE_KEY_PATH)
    developer_token = apple_client.generate_token()
    return jsonify(developer_token=developer_token)


if __name__ == "__main__":
    app.run(debug=True)
