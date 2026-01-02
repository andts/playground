from typing import List, Optional, Dict
import json
from pathlib import Path
from ytmusicapi import YTMusic
from clidj.claude_client import Track


class SearchResult:
    """Result of searching for a track."""

    def __init__(self, track: Track, found: bool, video_id: Optional[str] = None, error: Optional[str] = None):
        self.track = track
        self.found = found
        self.video_id = video_id
        self.error = error


class YouTubeMusicClient:
    """Client for interacting with YouTube Music API."""

    def __init__(self, auth_path: str):
        # Validate that the auth file exists
        auth_file = Path(auth_path)
        if not auth_file.exists():
            raise FileNotFoundError(f"Authentication file not found: {auth_path}")

        # Try to load and validate the JSON file
        try:
            with open(auth_file, 'r') as f:
                auth_data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in authentication file: {e}")

        # Initialize YTMusic with OAuth authentication
        # Pass the file path - ytmusicapi will handle loading it
        self.ytmusic = YTMusic(auth_path)

    def create_playlist(self, name: str, description: str) -> str:
        """Create a new playlist and return its ID."""
        return self.ytmusic.create_playlist(name, description)

    def search_track(self, track: Track) -> SearchResult:
        """Search for a track on YouTube Music."""
        try:
            query = f"{track.artist} {track.title}"
            results = self.ytmusic.search(query, filter='songs', limit=5)

            if not results:
                return SearchResult(track, False, error='No results found')

            # Get the first song result
            song = results[0]
            video_id = song.get('videoId')

            if not video_id:
                return SearchResult(track, False, error='No video ID found')

            return SearchResult(track, True, video_id=video_id)

        except Exception as e:
            return SearchResult(track, False, error=str(e))

    def add_tracks_to_playlist(self, playlist_id: str, video_ids: List[str]):
        """Add tracks to a playlist."""
        if not video_ids:
            return

        self.ytmusic.add_playlist_items(playlist_id, video_ids)
