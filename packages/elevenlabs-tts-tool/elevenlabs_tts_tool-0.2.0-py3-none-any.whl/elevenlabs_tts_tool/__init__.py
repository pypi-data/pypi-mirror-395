"""
elevenlabs-tts-tool: Professional ElevenLabs TTS CLI.

A command-line tool for text-to-speech synthesis using ElevenLabs API.
Supports both speaker playback and WAV file output.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from elevenlabs_tts_tool.core import get_client, play_speech, save_speech
from elevenlabs_tts_tool.voices import VoiceManager, VoiceProfile

__version__ = "0.2.0"

__all__ = [
    "get_client",
    "play_speech",
    "save_speech",
    "VoiceManager",
    "VoiceProfile",
]
