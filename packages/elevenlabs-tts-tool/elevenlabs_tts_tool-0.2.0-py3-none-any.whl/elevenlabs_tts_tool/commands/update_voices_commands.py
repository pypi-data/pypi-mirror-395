"""
Update voices command implementation.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import json
import sys
from pathlib import Path
from typing import Any

import click

from elevenlabs_tts_tool.core.client import get_client
from elevenlabs_tts_tool.logging_config import get_logger

logger = get_logger(__name__)


@click.command(name="update-voices")
@click.option(
    "--output",
    "-o",
    type=click.Path(path_type=Path),
    default=None,
    help="Output file path (default: ~/.config/elevenlabs-tty-tool/voices_lookup.json)",
)
def update_voices(output: Path | None) -> None:
    """
    Update voice lookup table from ElevenLabs API.

    Fetches all premade voices from the ElevenLabs API and updates
    the voices_lookup.json file with current voice information.

    \b
    Examples:

    \b
        # Update default voice lookup file
        elevenlabs-tty-tool update-voices

    \b
        # Save to custom location
        elevenlabs-tty-tool update-voices --output custom_voices.json

    \b
    Note:
        Requires ELEVENLABS_API_KEY environment variable to be set.
        Only updates premade voices (not custom cloned voices).
    """
    try:
        logger.info("Updating voice lookup table from ElevenLabs API")

        # Initialize client
        logger.debug("Initializing ElevenLabs client")
        client = get_client()

        # Determine output path
        if output is None:
            config_dir = Path.home() / ".config" / "elevenlabs-tts-tool"
            logger.debug(f"Using default config directory: {config_dir}")
            config_dir.mkdir(parents=True, exist_ok=True)
            output = config_dir / "voices_lookup.json"

        logger.info(f"Output file: {output}")
        click.echo("Fetching voices from ElevenLabs API...")

        # Fetch premade voices
        logger.debug("Calling API: client.voices.search(category='premade')")
        response = client.voices.search(
            category="premade", page_size=100, sort="name", sort_direction="asc"
        )
        logger.debug(f"Received {len(response.voices)} voices from API")

        voice_data: dict[str, Any] = {}

        for voice in response.voices:
            friendly_key = voice.name.lower().replace(" ", "_")

            voice_data[friendly_key] = {
                "voice_id": voice.voice_id,
                "name": voice.name,
                "gender": voice.voice_tag.gender if voice.voice_tag else "unknown",
                "age": voice.voice_tag.age if voice.voice_tag else "unknown",
                "accent": voice.voice_tag.accent if voice.voice_tag else "unknown",
                "language": voice.voice_tag.language if voice.voice_tag else "en",
                "description": voice.description or "",
                "category": voice.category,
            }

        # Write to file
        with open(output, "w") as f:
            json.dump(voice_data, f, indent=2)

        click.echo(f"✅ Updated {len(voice_data)} voices")
        click.echo(f"📝 Saved to: {output}")

    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error updating voices: {e}", err=True)
        sys.exit(1)
