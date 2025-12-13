"""
Voice listing command implementation.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import sys

import click

from elevenlabs_tts_tool.logging_config import get_logger
from elevenlabs_tts_tool.voices import VoiceManager

logger = get_logger(__name__)


@click.command(name="list-voices")
def list_voices() -> None:
    """
    List all available voices.

    Displays voice names, characteristics, and descriptions to help you
    choose the right voice for your TTS needs.

    \b
    Examples:

    \b
        # List all available voices
        elevenlabs-tty-tool list-voices

    \b
        # Find voices with specific characteristics (using grep)
        elevenlabs-tty-tool list-voices | grep British
        elevenlabs-tty-tool list-voices | grep male
        elevenlabs-tty-tool list-voices | grep young

    \b
    Output Format:
        Each line shows: voice_name | gender | age | accent | description
    """
    try:
        logger.info("Loading voice list")
        logger.debug("Initializing VoiceManager")
        voice_manager = VoiceManager()
        voices = voice_manager.list_voices()
        logger.debug(f"Loaded {len(voices)} voices")

        if not voices:
            logger.error("No voices available from VoiceManager")
            click.echo("No voices available.", err=True)
            sys.exit(1)

        logger.info(f"Displaying {len(voices)} voices")

        # Print header
        click.echo(f"{'Voice':<15} {'Gender':<10} {'Age':<12} {'Accent':<15} Description")
        click.echo("=" * 100)

        # Print each voice
        for name, profile in voices:
            logger.debug(f"Voice: {name} - {profile.gender}, {profile.age}, {profile.accent}")
            click.echo(
                f"{name:<15} {profile.gender:<10} {profile.age:<12} "
                f"{profile.accent:<15} {profile.description}"
            )

        # Print summary
        click.echo("=" * 100)
        click.echo(f"\nTotal: {len(voices)} voices available")

    except Exception as e:
        logger.error(f"Failed to list voices: {type(e).__name__}: {e}")
        logger.debug("Full traceback:", exc_info=True)
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
