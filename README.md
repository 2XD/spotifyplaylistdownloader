
# Spotify Playlist Downloader

This script allows you to download songs from a Spotify playlist
## Requirements

The script requires all of the below. the libraries are found in the requirements.txt, but you will have to setup the developer account yuorself.
- **Python 3.6+** (Ensure that Python is installed on your system)
- **Spotify Developer Account** (To get your `SPOTIPY_CLIENT_ID` and `SPOTIPY_CLIENT_SECRET`)
- **yt-dlp** (For downloading YouTube videos)
- **Spotipy** (Spotify API for fetching playlist data)

## Installation

1. Clone the repository or download the script files to your local machine.

2. Install the required packages using `pip`:

   ```
   pip install -r requirements.txt
   
## Getting Your Spotify API Credentials

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications).
2. Log in with your Spotify account
3. Click on the **Create an App** button.
4. Fill in the app name, none of the other details matter put whatever you want:
5. Agree to the terms and conditions and click **Create**.
6. Once your app is created, locate the following. These will be used in the config to find your spotify playlists:
   - **Client ID** (Copy this into the `SPOTIPY_CLIENT_ID` field of `config.txt`)
   - **Client Secret** (Copy this into the `SPOTIPY_CLIENT_SECRET` field of `config.txt`)
7. Add your Spotify API credentials to `config.txt`:

You are all good to go then! Just run the downloader.py and follow the instructions on screen.

# Goals

Save as a .mp3 instead of a .webm
