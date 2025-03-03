import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import yt_dlp

def load_config():
    config = {}
    with open("config.txt", "r") as f:
        for line in f.readlines():
            key, value = line.strip().split("=")
            config[key] = value
    return config

def download_song(song_url, download_folder, failed_songs):
    print(f"Downloading: {song_url}")
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            # Try downloading directly using yt_dlp
            ydl.download([song_url])
        except Exception as e:
            print(f"Failed to download {song_url}: {str(e)}")
            failed_songs.append(song_url)

def get_spotify_playlist(playlist_url, client_id, client_secret):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                   client_secret=client_secret,
                                                   redirect_uri="http://127.0.0.1:8080", scope="playlist-read-private"))
    
    playlist_id = playlist_url.split("/")[-1].split("?")[0]
    results = sp.playlist_tracks(playlist_id)
    
    song_urls = []
    for item in results['items']:
        track = item['track']
        track_name = track['name']
        artist_name = track['artists'][0]['name']
        search_query = f"{track_name} {artist_name} youtube"
        search_url = f"https://www.youtube.com/results?search_query={search_query.replace(' ', '+')}"
        song_urls.append(search_url)
        
    return song_urls

def is_valid_video(title, first_result=True):
    """
    Checks if the video title is valid.
    Skips titles containing 'official video' only if it's not the first result.
    """
    invalid_keywords = ["official video", "official music video", "music video", "live"]
    
    if first_result:
        return True  # Always accept the first result, even if it's labeled as "official video"
    return not any(keyword in title.lower() for keyword in invalid_keywords)

def search_and_download_song(song_url, download_folder, failed_songs):
    page = 1
    while page <= 10:  # Set the limit of pages to 10
        try:
            print(f"Searching page {page} for: {song_url}")
            ydl_opts = {
                'quiet': True,
                'extract_flat': True,
                'force_generic_extractor': True
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(song_url, download=False)
                if 'entries' in info_dict:
                    if len(info_dict['entries']) > 0:
                        # Check if the video title is valid (doesn't contain unwanted keywords)
                        video_info = info_dict['entries'][0]
                        video_title = video_info['title']
                        first_result = (page == 1)  # If it's the first result, we allow it
                        if is_valid_video(video_title, first_result):
                            video_url = video_info['url']
                            download_song(video_url, download_folder, failed_songs)
                            return
                        else:
                            print(f"Skipping invalid video: {video_title}")
            page += 1
        except Exception as e:
            print(f"Error searching on page {page}: {str(e)}")
            break  # Stop if an error occurs

    failed_songs.append(song_url)  # Append song to failed if not found after 10 pages
    print(f"Could not find: {song_url} after 10 pages.")

def main():
    # Load config values from the file
    config = load_config()
    client_id = config.get("SPOTIPY_CLIENT_ID")
    client_secret = config.get("SPOTIPY_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        print("Error: Missing Spotify credentials in config.txt")
        return
    
    playlist_url = input("Enter Spotify playlist URL: ")
    download_folder = input("Enter download folder: ")
    os.makedirs(download_folder, exist_ok=True)

    print(f"Downloading songs to: {download_folder}")

    song_urls = get_spotify_playlist(playlist_url, client_id, client_secret)
    
    failed_songs = []  # List to store failed songs

    for song_url in song_urls:
        search_and_download_song(song_url, download_folder, failed_songs)

    if failed_songs:
        # Write failed songs to a text file
        with open(os.path.join(download_folder, "failed_downloads.txt"), "w") as f:
            for song in failed_songs:
                f.write(song + "\n")
        print(f"Some songs failed to download. See failed_downloads.txt for details.")

if __name__ == "__main__":
    main()
