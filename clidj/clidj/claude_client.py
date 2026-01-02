import json
import re
from typing import List, Dict
from anthropic import Anthropic


class Track:
    """Represents a music track."""

    def __init__(self, artist: str, title: str):
        self.artist = artist
        self.title = title

    def __repr__(self):
        return f"{self.artist} - {self.title}"


class Playlist:
    """Represents a generated playlist."""

    def __init__(self, name: str, description: str, tracks: List[Track]):
        self.name = name
        self.description = description
        self.tracks = tracks


PLAYLIST_GENERATION_PROMPT = """You are a music curator creating a playlist based on the user's request.

Generate a playlist with:
- A creative and fitting name
- A short description (2 sentences max)
- A list of 15-25 tracks that match the theme

Each track should include the artist name and song title.
Make sure the tracks are real, popular songs that would be available on YouTube Music.

Return your response in the following JSON format:
{
  "name": "Playlist Name",
  "description": "Brief description of the playlist theme and mood.",
  "tracks": [
    {"artist": "Artist Name", "title": "Song Title"},
    ...
  ]
}"""


class ClaudeClient:
    """Client for interacting with Claude API."""

    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)

    def generate_playlist(self, user_prompt: str) -> Playlist:
        """Generate a playlist based on user prompt."""
        response = self.client.messages.create(
            model='claude-sonnet-4-5-20250929',
            max_tokens=4096,
            messages=[
                {
                    'role': 'user',
                    'content': f"{PLAYLIST_GENERATION_PROMPT}\n\nUser request: {user_prompt}",
                }
            ],
        )

        content = response.content[0]
        if content.type != 'text':
            raise ValueError('Unexpected response type from Claude')

        # Extract JSON from response
        json_match = re.search(r'\{[\s\S]*\}', content.text)
        if not json_match:
            raise ValueError('Failed to extract JSON from Claude response')

        playlist_data = json.loads(json_match.group(0))
        self._validate_playlist(playlist_data)

        tracks = [Track(t['artist'], t['title']) for t in playlist_data['tracks']]
        return Playlist(playlist_data['name'], playlist_data['description'], tracks)

    @staticmethod
    def _validate_playlist(data: dict):
        """Validate playlist data structure."""
        if not data.get('name') or not isinstance(data['name'], str):
            raise ValueError('Invalid playlist: missing or invalid name')

        if not data.get('description') or not isinstance(data['description'], str):
            raise ValueError('Invalid playlist: missing or invalid description')

        if not isinstance(data.get('tracks'), list) or len(data['tracks']) == 0:
            raise ValueError('Invalid playlist: missing or empty tracks array')

        for track in data['tracks']:
            if not track.get('artist') or not isinstance(track['artist'], str):
                raise ValueError('Invalid track: missing or invalid artist')
            if not track.get('title') or not isinstance(track['title'], str):
                raise ValueError('Invalid track: missing or invalid title')
