import json
import os
from pathlib import Path
from typing import Optional


class Config:
    """Manages configuration for the CLI DJ application."""

    def __init__(self):
        self.config_path = Path.home() / '.clidjrc'
        self.data = self._load()

    def _load(self) -> dict:
        """Load configuration from file."""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading config: {e}")
        return {}

    def save(self):
        """Save configuration to file."""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
            raise

    @property
    def claude_api_key(self) -> Optional[str]:
        """Get Claude API key."""
        return self.data.get('claudeApiKey')

    @claude_api_key.setter
    def claude_api_key(self, value: str):
        """Set Claude API key."""
        self.data['claudeApiKey'] = value

    @property
    def ytmusic_auth_path(self) -> Optional[str]:
        """Get YouTube Music authentication file path."""
        return self.data.get('ytmusicAuthPath')

    @ytmusic_auth_path.setter
    def ytmusic_auth_path(self, value: str):
        """Set YouTube Music authentication file path."""
        self.data['ytmusicAuthPath'] = value

    def is_configured(self) -> bool:
        """Check if both Claude and YTMusic are configured."""
        return bool(self.claude_api_key and self.ytmusic_auth_path)

    def has_claude_key(self) -> bool:
        """Check if Claude API key is configured."""
        return bool(self.claude_api_key)

    def has_ytmusic_auth(self) -> bool:
        """Check if YouTube Music auth is configured."""
        return bool(self.ytmusic_auth_path)
