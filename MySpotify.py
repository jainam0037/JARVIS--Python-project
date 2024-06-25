import spotipy # type: ignore
from spotipy.oauth2 import SpotifyOAuth # type: ignore
import random

class SpotifyPlayer:
    def __init__(self, client_id, client_secret, redirect_uri):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope="user-library-read user-read-playback-state user-modify-playback-state"
        ))

    def play_random_song(self):
        # Get the list of user's available devices
        devices = self.sp.devices()
        if not devices['devices']:
            print("No active devices found. Please start Spotify on a device.")
            return

        # Choose a random saved track from the user's library
        results = self.sp.current_user_saved_tracks()
        tracks = results['items']
        if not tracks:
            print("No saved tracks found.")
            return
        track = random.choice(tracks)['track']
        track_uri = track['uri']
        
        # Start playback on an active device
        active_device_id = devices['devices'][0]['id']  # Select the first available device
        self.sp.start_playback(device_id=active_device_id, uris=[track_uri])
        print(f"Now playing: {track['name']} by {track['artists'][0]['name']}")

    def stop_song(self):
        self.sp.pause_playback()
        print("Playback stopped.")
