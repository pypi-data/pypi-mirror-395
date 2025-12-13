"""
Voice management for ElevenLabs TTS.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class VoiceProfile:
    """Voice profile with metadata."""

    voice_id: str
    name: str
    gender: str
    age: str
    accent: str
    language: str
    description: str
    category: str


class VoiceManager:
    """Manages voice lookup and selection."""

    def __init__(self, lookup_file: Path | None = None):
        """
        Initialize VoiceManager.

        Args:
            lookup_file: Path to voice lookup JSON file. If None, uses default.
                Checks user config directory first (~/.config/elevenlabs-tty-tool/),
                then falls back to package default.
        """
        if lookup_file is None:
            # Check user config directory first
            user_config = Path.home() / ".config" / "elevenlabs-tty-tool" / "voices_lookup.json"
            if user_config.exists():
                lookup_file = user_config
            else:
                # Fall back to package default
                lookup_file = Path(__file__).parent / "voices_lookup.json"

        self.lookup_file = lookup_file
        self._voices = self._load_voices()

    def _load_voices(self) -> dict[str, VoiceProfile]:
        """
        Load voices from lookup file.

        Returns:
            Dictionary mapping friendly names to VoiceProfile objects.

        Raises:
            FileNotFoundError: If lookup file doesn't exist.
            json.JSONDecodeError: If lookup file is invalid JSON.
        """
        if not self.lookup_file.exists():
            raise FileNotFoundError(
                f"Voice lookup file not found: {self.lookup_file}\n"
                f"Run: elevenlabs-tty-tool update-voices"
            )

        with open(self.lookup_file) as f:
            data = json.load(f)

        return {key: VoiceProfile(**profile) for key, profile in data.items()}

    def get_voice_id(self, friendly_name: str) -> str:
        """
        Get voice ID from friendly name or return as-is if it's already an ID.

        Args:
            friendly_name: Friendly voice name (e.g., 'rachel') or voice ID.

        Returns:
            Voice ID string.

        Raises:
            ValueError: If voice not found.
        """
        profile = self._voices.get(friendly_name.lower())
        if profile:
            return profile.voice_id

        # Check if it might be a valid voice ID (32-character alphanumeric)
        if len(friendly_name) == 20 and friendly_name.isalnum():
            return friendly_name

        # Voice not found
        available = ", ".join(sorted(self._voices.keys())[:10])
        raise ValueError(
            f"Voice '{friendly_name}' not found.\n"
            f"Available voices: {available}...\n"
            f"Use 'elevenlabs-tty list-voices' to see all voices."
        )

    def get_voice_profile(self, friendly_name: str) -> VoiceProfile:
        """
        Get complete voice profile.

        Args:
            friendly_name: Friendly voice name (e.g., 'rachel').

        Returns:
            VoiceProfile object.

        Raises:
            ValueError: If voice not found.
        """
        profile = self._voices.get(friendly_name.lower())
        if not profile:
            raise ValueError(
                f"Voice '{friendly_name}' not found. "
                f"Use 'elevenlabs-tty list-voices' to see available voices."
            )
        return profile

    def list_voices(self) -> list[tuple[str, VoiceProfile]]:
        """
        List all available voices.

        Returns:
            List of (friendly_name, profile) tuples sorted by name.
        """
        return sorted(self._voices.items())

    def get_default_voice_id(self) -> str:
        """
        Get default voice ID (rachel).

        Returns:
            Voice ID for default voice.
        """
        return self.get_voice_id("rachel")
