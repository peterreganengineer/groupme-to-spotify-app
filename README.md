# Peter Regan GroupMe To Spotify Music App 🎵

A Python-based application that integrates GroupMe messaging with Spotify playlists. This project fetches music links shared in GroupMe conversations and automatically creates Spotify playlists based on date ranges.

## Features

- 🎵 **GroupMe Integration** - Fetches messages from GroupMe groups via API
- 🎶 **Spotify Integration** - Creates and manages Spotify playlists
- 💾 **MySQL Database** - Stores GroupMe messages and user data
- 🔍 **Music Detection** - Automatically identifies Spotify song links in messages
- 📊 **Data Management** - Refresh and sync GroupMe data with local database
- 🔐 **Secure Credentials** - Environment variables for sensitive data

## Prerequisites

- Python 3.8 or higher
- MySQL Server
- Spotify Developer Account
- GroupMe API Access

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/peterreganengineer/peter-regan-music.git
cd peter-regan-music
```

### 2. Install Dependencies

```bash
cd backend
python3 -m pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Copy the example environment file and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your actual credentials:

```bash
# Spotify Configuration
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
SPOTIFY_REDIRECT_URI=http://127.0.0.1:8888/callback
SPOTIFY_USERNAME=your_username
SPOTIFY_SCOPE=playlist-modify-public

# GroupMe Configuration
GROUPME_TOKEN=your_groupme_token
GROUPME_GROUP_ID=your_group_id

# Database Configuration
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_db_password
DB_NAME=groupme
```

### 4. Set Up Database

Create a MySQL database and tables:

```sql
CREATE DATABASE groupme;
```

Refer to your database schema files for table structures.

## Configuration

### Getting Spotify Credentials

1. Visit [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new application
3. Copy your **Client ID** and **Client Secret**
4. Go to **Edit Settings** and add Redirect URI: `http://127.0.0.1:8888/callback`
5. Update your `.env` file

### Getting GroupMe Credentials

1. Go to [GroupMe Developer](https://dev.groupme.com/)
2. Create an API token
3. Find your group ID from the GroupMe API
4. Update your `.env` file

## Usage

### Refresh GroupMe Messages

Fetches the latest messages from your GroupMe group and stores them in the database:

```bash
python3 groupme_refresh_messages.py
```

### Refresh GroupMe Users

Updates user information from GroupMe group members:

```bash
python3 groupme_refresh_users.py
```

### Create Spotify Playlist from GroupMe Songs

Creates a new Spotify playlist with songs shared in GroupMe within a date range:

```bash
python3 groupme_to_spotify.py "Playlist Name" "2024-01-01" "2024-12-31"
```

**Parameters:**
- `Playlist Name`: Name for the new Spotify playlist
- `start_date`: Start date (YYYY-MM-DD format)
- `end_date`: End date (YYYY-MM-DD format)

## Project Structure

```
peter-regan-music/
├── backend/
│   ├── .env                          # Local environment variables (git-ignored)
│   ├── .env.example                  # Template for environment variables
│   ├── requirements.txt              # Python dependencies
│   ├── spotify_client.py             # Spotify API client
│   ├── groupme_client.py             # GroupMe API client
│   ├── groupme_refresh_messages.py   # Fetch GroupMe messages
│   ├── groupme_refresh_users.py      # Fetch GroupMe users
│   └── groupme_to_spotify.py         # Create Spotify playlists
├── index.html                        # Frontend (optional)
├── package.json                      # Node.js dependencies (optional)
├── .gitignore                        # Git ignore rules
├── README.md                         # This file
└── ENV_SETUP.md                      # Detailed environment setup guide
```

## Security

⚠️ **Important Security Notes:**

- **Never commit `.env`** - It contains sensitive credentials
- **Keep `.env` local** - This file should only exist on your machine
- **Share `.env.example`** - Other developers use this as a template
- **Regenerate credentials if exposed** - If keys are ever public, regenerate them immediately
- **Add to `.gitignore`** - `.env` is already in `.gitignore`

## Environment Variables

The application uses the following environment variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `SPOTIFY_CLIENT_ID` | Spotify app client ID | `abc123...` |
| `SPOTIFY_CLIENT_SECRET` | Spotify app secret | `xyz789...` |
| `SPOTIFY_REDIRECT_URI` | OAuth redirect URL | `http://127.0.0.1:8888/callback` |
| `SPOTIFY_USERNAME` | Your Spotify username | `username123` |
| `SPOTIFY_SCOPE` | Spotify API scope | `playlist-modify-public` |
| `GROUPME_TOKEN` | GroupMe API token | `abc123...` |
| `GROUPME_GROUP_ID` | GroupMe group ID | `123456789` |
| `DB_HOST` | MySQL host | `localhost` |
| `DB_USER` | MySQL user | `root` |
| `DB_PASSWORD` | MySQL password | `your_password` |
| `DB_NAME` | MySQL database name | `groupme` |

## Dependencies

- **spotipy** - Spotify Web API library
- **python-dotenv** - Environment variable management
- **requests** - HTTP library for GroupMe API
- **mysql-connector-python** - MySQL database connector

See `requirements.txt` for the complete list.

## Troubleshooting

### Module not found errors

Make sure you've installed all dependencies:
```bash
python3 -m pip install -r requirements.txt
```

### Authentication errors

- Verify your `.env` file has the correct credentials
- Check that tokens haven't expired (regenerate if needed)
- Ensure redirect URI matches exactly in Spotify settings

### Database connection errors

- Ensure MySQL is running
- Verify database host, user, and password in `.env`
- Check that the database exists

### Python version issues

Use `python3` instead of `python`:
```bash
python3 groupme_refresh_messages.py
```

## Contributing

This is a personal project. For improvements or bug reports, please open an issue or submit a pull request.

## License

This project is provided as-is. See LICENSE file for details.

## Support

For issues or questions, please refer to:
- [Spotify API Documentation](https://developer.spotify.com/documentation/web-api)
- [GroupMe API Documentation](https://dev.groupme.com/docs/v3)
- [Python-Dotenv Documentation](https://python-dotenv.readthedocs.io/)

---

**Last Updated:** January 2026
