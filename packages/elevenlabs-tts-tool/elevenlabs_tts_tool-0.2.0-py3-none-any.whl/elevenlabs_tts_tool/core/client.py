"""
ElevenLabs client initialization and management.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import os

from elevenlabs.client import ElevenLabs


def get_api_key() -> str:
    """
    Get ElevenLabs API key from environment.

    Returns:
        API key string.

    Raises:
        ValueError: If API key not found in environment.
    """
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError(
            "ELEVENLABS_API_KEY environment variable not set.\n"
            "Set it with: export ELEVENLABS_API_KEY='your-api-key'\n"
            "Get your API key from: https://elevenlabs.io/app/settings/api-keys"
        )
    return api_key


def get_client() -> ElevenLabs:
    """
    Initialize and return ElevenLabs client.

    Returns:
        Initialized ElevenLabs client.

    Raises:
        ValueError: If API key not found.
    """
    api_key = get_api_key()
    return ElevenLabs(api_key=api_key)
