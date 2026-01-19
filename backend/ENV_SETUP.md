# Environment Setup Guide

This project uses environment variables to manage sensitive credentials like API keys and database passwords.

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Environment Variables Setup

### Step 1: Create your `.env` file

Copy the `.env.example` file to create your own `.env` file:
```bash
cp .env.example .env
```

### Step 2: Fill in your credentials

Edit the `.env` file with your actual credentials:

```bash
# Spotify Configuration
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
SPOTIFY_REDIRECT_URI=http://localhost:8888/callback
SPOTIFY_USERNAME=your_spotify_username
SPOTIFY_SCOPE=playlist-modify-public

# GroupMe Configuration
GROUPME_TOKEN=your_groupme_token
GROUPME_GROUP_ID=your_group_id

# Database Configuration
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_database_password
DB_NAME=groupme
```

### Step 3: Keep `.env` Secure

⚠️ **Important**: The `.env` file is in `.gitignore` and should **never** be committed to version control. It contains sensitive credentials.

## Getting Your Credentials

### Spotify
1. Go to https://developer.spotify.com/dashboard
2. Create a new application
3. Copy your Client ID and Client Secret
4. Set your Redirect URI in the app settings

### GroupMe
1. Go to https://dev.groupme.com/
2. Create an API token
3. Get your group ID from the GroupMe API

## Running the Scripts

Once your `.env` file is set up, you can run the scripts:

```bash
python groupme_refresh_messages.py
python groupme_refresh_users.py
python groupme_to_spotify.py <playlist_name> <start_date> <end_date>
```

The environment variables will be automatically loaded from your `.env` file.
