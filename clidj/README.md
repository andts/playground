# CLI DJ 🎵

An AI-powered CLI tool that generates custom YouTube Music playlists using Claude AI.

## Features

- 🤖 Uses Claude AI to generate creative playlists based on your prompts
- 🎵 Automatically creates playlists on YouTube Music
- 🔍 Searches and adds tracks to your playlist
- 📊 Provides detailed summary of added and skipped tracks
- 💾 Stores configuration securely in your home directory

## Prerequisites

- Python 3.8 or higher
- `uv` (recommended) or `pip` for package management
- A Claude API key
- YouTube Music account

## Installation

### Option 1: Using uv (recommended)

[uv](https://github.com/astral-sh/uv) is a fast Python package and project manager.

1. Install uv if you haven't already:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Navigate to the project directory:
```bash
cd clidj
```

3. Install the project:
```bash
uv pip install -e .
```

4. Run the tool:
```bash
clidj
```

Or run directly without installing:
```bash
uv run clidj
```

### Option 2: Using pip

1. Clone or navigate to this directory:
```bash
cd clidj
```

2. Install the package:
```bash
pip install -e .
```

This will install the `clidj` command globally.

### Option 3: Install dependencies only

If you prefer to run directly without installing:
```bash
pip install -r requirements.txt
```

Then run with:
```bash
python -m clidj
```

## Configuration

### 1. Claude API Key

You'll need a Claude API key from Anthropic. Get one at: https://console.anthropic.com/

The tool will prompt you for this on first run and store it in `~/.clidjrc`.

### 2. YouTube Music Authentication

You need to set up YouTube Music API authentication:

1. Make sure ytmusicapi is installed (it's included as a dependency):
```bash
# With uv
uv pip install ytmusicapi

# Or with pip
pip install ytmusicapi
```

2. Generate OAuth credentials:
```bash
ytmusicapi oauth
```

3. This creates an `oauth.json` file in your current directory

4. Note the full path to this file (you can move it to a permanent location like `~/.config/clidj/oauth.json` if desired)

5. The tool will prompt you for this path on first run

For detailed instructions, see: https://ytmusicapi.readthedocs.io/en/stable/setup/oauth.html

## Usage

Run the tool:

```bash
# If installed globally
clidj

# With uv (without installing)
uv run clidj

# Or directly with Python
python -m clidj
```

### First Run

On your first run, the tool will:
1. Ask for your Claude API key
2. Show instructions for YouTube Music setup
3. Ask for the path to your oauth.json file

These credentials are saved to `~/.clidjrc` for future use.

### Creating Playlists

Once configured, simply describe the kind of playlist you want:

```
What kind of playlist would you like to create? 90s hip hop classics

What kind of playlist would you like to create? Relaxing jazz for studying

What kind of playlist would you like to create? Energetic workout music
```

The tool will:
1. Generate a playlist using Claude AI (name, description, and 15-25 tracks)
2. Create the playlist on YouTube Music
3. Search for each track on YouTube Music
4. Add found tracks to the playlist
5. Show you a summary of what was added and what was skipped

## Example Session

```
============================================================
CLI DJ - AI-Powered YouTube Music Playlist Generator
============================================================

✓ Configuration loaded!

What kind of playlist would you like to create? chill lo-fi beats for coding

ℹ Generating playlist with Claude AI...
✓ Playlist generated!

Name: Code & Chill: Lo-Fi Programming Beats
Description: A carefully curated collection of smooth lo-fi hip-hop and ambient beats perfect for maintaining focus during long coding sessions. Gentle rhythms and mellow vibes to keep you in the flow.
Tracks: 20

ℹ Connecting to YouTube Music...
✓ Connected to YouTube Music!
ℹ Creating playlist...
✓ Playlist created! (ID: PLxxxxxxxxxx)

============================================================
Searching for tracks on YouTube Music
============================================================

[1/20] Searching: Jinsang - Summer ✓ Found
[2/20] Searching: Aso - Blue ✓ Found
...

ℹ Adding 18 track(s) to playlist...

============================================================
Summary
============================================================

Playlist: Code & Chill: Lo-Fi Programming Beats
Description: A carefully curated collection of smooth lo-fi hip-hop and ambient beats perfect for maintaining focus during long coding sessions.

✓ 18 track(s) added to playlist
✗ 2 track(s) could not be found and were skipped:

  - Example Artist - Example Song

✓ All done! Enjoy your new playlist!
```

## Configuration File

The configuration is stored at `~/.clidjrc`:

```json
{
  "claudeApiKey": "your-api-key",
  "ytmusicAuthPath": "/path/to/oauth.json"
}
```

You can manually edit this file or delete it to reconfigure.

## Development

### Project Structure

```
clidj/
├── clidj/
│   ├── __init__.py
│   ├── __main__.py         # Main CLI application
│   ├── config.py           # Configuration management
│   ├── claude_client.py    # Claude API integration
│   └── ytmusic_client.py   # YouTube Music integration
├── requirements.txt
├── setup.py
├── pyproject.toml
└── README.md
```

### Running in Development Mode

```bash
# Install in editable mode
pip install -e .

# Run the tool
clidj
```

## Troubleshooting

### "No results found" for many tracks

- Make sure your oauth.json file is valid and not expired
- Try re-authenticating using `ytmusicapi oauth`
- The authentication may expire after some time

### "Invalid API key" error

- Verify your Claude API key at https://console.anthropic.com/
- Check that the key is correctly saved in `~/.clidjrc`
- Make sure you didn't accidentally include quotes or extra whitespace

### "Authentication file not found" error

- Verify the path to your oauth.json file is correct
- Use the full absolute path (e.g., `/home/username/.config/clidj/oauth.json`)
- You can use `~` for your home directory, which will be expanded automatically

### Permission errors

- Make sure the tool has write permissions to your home directory
- On Unix systems, check the permissions of `~/.clidjrc`

## How It Works

1. **User Input**: You provide a natural language description of the playlist you want
2. **AI Generation**: Claude analyzes your request and generates a creative playlist with:
   - A fitting name
   - A descriptive summary
   - 15-25 carefully selected tracks that match the theme
3. **Playlist Creation**: The tool creates the playlist on your YouTube Music account
4. **Track Search**: Each track is searched on YouTube Music to find the best match
5. **Population**: Found tracks are added to the playlist
6. **Summary**: You get a complete report of what was added and what couldn't be found

## License

ISC
