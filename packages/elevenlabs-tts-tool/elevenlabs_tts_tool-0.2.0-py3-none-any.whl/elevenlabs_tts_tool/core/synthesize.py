"""
Text-to-speech synthesis functions.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import sys
from collections.abc import Iterator
from pathlib import Path

from elevenlabs import save
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play


def synthesize_audio(
    client: ElevenLabs,
    text: str,
    voice_id: str,
    output_format: str = "mp3_44100_128",
    model_id: str = "eleven_turbo_v2_5",
) -> Iterator[bytes]:
    """
    Synthesize text to audio using ElevenLabs API.

    Args:
        client: Initialized ElevenLabs client.
        text: Text to convert to speech.
        voice_id: Voice ID to use for synthesis.
        output_format: Output format (default: mp3_44100_128).
            Common formats: mp3_44100_128, pcm_44100, pcm_24000, pcm_16000.
        model_id: Model ID (default: eleven_turbo_v2_5).

    Returns:
        Iterator of audio bytes.

    Raises:
        Exception: If synthesis fails.
    """
    try:
        audio = client.text_to_speech.convert(
            text=text,
            voice_id=voice_id,
            model_id=model_id,
            output_format=output_format,
        )
        return audio  # type: ignore[no-any-return]
    except Exception as e:
        raise Exception(f"Speech synthesis failed: {e}") from e


def play_speech(
    client: ElevenLabs,
    text: str,
    voice_id: str,
    output_format: str = "mp3_44100_128",
    model_id: str = "eleven_turbo_v2_5",
) -> None:
    """
    Synthesize text and play through speakers.

    Args:
        client: Initialized ElevenLabs client.
        text: Text to convert to speech.
        voice_id: Voice ID to use for synthesis.
        output_format: Output format (default: mp3_44100_128).
        model_id: Model ID (default: eleven_turbo_v2_5).

    Raises:
        Exception: If synthesis or playback fails.
    """
    try:
        audio = synthesize_audio(client, text, voice_id, output_format, model_id)
        play(audio)
    except Exception as e:
        raise Exception(f"Playback failed: {e}") from e


def save_speech(
    client: ElevenLabs,
    text: str,
    voice_id: str,
    output_path: Path,
    output_format: str = "mp3_44100_128",
    model_id: str = "eleven_turbo_v2_5",
) -> None:
    """
    Synthesize text and save to audio file.

    Args:
        client: Initialized ElevenLabs client.
        text: Text to convert to speech.
        voice_id: Voice ID to use for synthesis.
        output_path: Path where to save the audio file.
        output_format: Output format (default: mp3_44100_128).
            Use pcm_* formats for WAV files (e.g., pcm_44100).
        model_id: Model ID (default: eleven_turbo_v2_5).

    Raises:
        Exception: If synthesis or file save fails.
    """
    try:
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        audio = synthesize_audio(client, text, voice_id, output_format, model_id)
        save(audio, str(output_path))
    except Exception as e:
        raise Exception(f"Failed to save audio: {e}") from e


def read_from_stdin() -> str:
    """
    Read text from stdin.

    Returns:
        Text read from stdin.

    Raises:
        ValueError: If stdin is empty.
    """
    if sys.stdin.isatty():
        raise ValueError(
            "No input provided via stdin.\nUsage: echo 'text' | elevenlabs-tty synthesize --stdin"
        )

    text = sys.stdin.read().strip()
    if not text:
        raise ValueError("Empty input received from stdin.")

    return text
