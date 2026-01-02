#!/usr/bin/env python3
"""
CLI DJ - AI-Powered YouTube Music Playlist Generator
"""

import sys
from pathlib import Path
from .config import Config
from .claude_client import ClaudeClient
from .ytmusic_client import YouTubeMusicClient


YTMUSIC_SETUP_INSTRUCTIONS = """
To configure YouTube Music access:

1. Install the ytmusicapi Python package (if not already installed):
   pip install ytmusicapi

2. Generate authentication file:
   ytmusicapi oauth

3. This will create an 'oauth.json' file in your current directory.

4. Note the path to this file (you can move it to a permanent location if desired).

5. You'll need to provide the full path to this file when prompted.

For more details, visit: https://ytmusicapi.readthedocs.io/
"""


def print_header(text: str):
    """Print a header."""
    print('\n' + '=' * 60)
    print(text)
    print('=' * 60 + '\n')


def print_success(text: str):
    """Print a success message."""
    print(f'✓ {text}')


def print_error(text: str):
    """Print an error message."""
    print(f'✗ {text}', file=sys.stderr)


def print_info(text: str):
    """Print an info message."""
    print(f'ℹ {text}')


def setup_configuration(config: Config) -> bool:
    """Set up configuration if needed. Returns True if successful."""
    if not config.has_claude_key():
        print_info('Claude API key not found in configuration.')
        api_key = input('Please enter your Claude API key: ').strip()

        if not api_key:
            print_error('API key is required to continue.')
            return False

        config.claude_api_key = api_key
        config.save()
        print_success('Claude API key saved!')

    if not config.has_ytmusic_auth():
        print_info('YouTube Music authentication not found.')
        print(YTMUSIC_SETUP_INSTRUCTIONS)

        auth_path = input('Please enter the full path to your oauth.json file (or press Enter to exit): ').strip()

        if not auth_path:
            print_info('You can run this tool again after setting up YouTube Music authentication.')
            return False

        # Expand ~ to home directory
        auth_path = str(Path(auth_path).expanduser())

        if not Path(auth_path).exists():
            print_error(f'File not found: {auth_path}')
            return False

        config.ytmusic_auth_path = auth_path
        config.save()
        print_success('YouTube Music authentication saved!')

    return True


def search_and_add_tracks(ytmusic: YouTubeMusicClient, playlist_id: str, playlist):
    """Search for tracks and add them to the playlist."""
    print_header('Searching for tracks on YouTube Music')

    results = []
    video_ids = []

    for i, track in enumerate(playlist.tracks, 1):
        print(f'[{i}/{len(playlist.tracks)}] Searching: {track}... ', end='', flush=True)

        result = ytmusic.search_track(track)
        results.append(result)

        if result.found and result.video_id:
            video_ids.append(result.video_id)
            print('✓ Found')
        else:
            error_msg = f' ({result.error})' if result.error else ''
            print(f'✗ Not found{error_msg}')

    if video_ids:
        print_info(f'\nAdding {len(video_ids)} track(s) to playlist...')
        ytmusic.add_tracks_to_playlist(playlist_id, video_ids)

    return len(video_ids), len(playlist.tracks) - len(video_ids), results


def print_summary(playlist, added: int, skipped: int, results):
    """Print a summary of the operation."""
    print_header('Summary')

    print(f'Playlist: {playlist.name}')
    print(f'Description: {playlist.description}\n')

    print_success(f'{added} track(s) added to playlist')

    if skipped > 0:
        print_error(f'{skipped} track(s) could not be found and were skipped:\n')

        for result in results:
            if not result.found:
                print(f'  - {result.track}')

    print('')


def main():
    """Main entry point."""
    try:
        print_header('CLI DJ - AI-Powered YouTube Music Playlist Generator')

        config = Config()

        if not setup_configuration(config):
            sys.exit(1)

        if not config.is_configured():
            print_error('Configuration incomplete. Please try again.')
            sys.exit(1)

        print_success('Configuration loaded!\n')

        user_prompt = input('What kind of playlist would you like to create? ').strip()

        if not user_prompt:
            print_info('No prompt provided. Exiting.')
            sys.exit(0)

        print_info('\nGenerating playlist with Claude AI...')

        claude = ClaudeClient(config.claude_api_key)
        playlist = claude.generate_playlist(user_prompt)

        print_success('Playlist generated!\n')
        print(f'Name: {playlist.name}')
        print(f'Description: {playlist.description}')
        print(f'Tracks: {len(playlist.tracks)}\n')

        print_info('Connecting to YouTube Music...')

        ytmusic = YouTubeMusicClient(config.ytmusic_auth_path)

        print_success('Connected to YouTube Music!')

        print_info('Creating playlist...')

        playlist_id = ytmusic.create_playlist(playlist.name, playlist.description)

        print_success(f'Playlist created! (ID: {playlist_id})')

        added, skipped, results = search_and_add_tracks(ytmusic, playlist_id, playlist)

        print_summary(playlist, added, skipped, results)

        print_success('All done! Enjoy your new playlist!')

    except KeyboardInterrupt:
        print_info('\n\nOperation cancelled by user.')
        sys.exit(0)
    except Exception as e:
        print_error(f'An error occurred: {e}')
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
