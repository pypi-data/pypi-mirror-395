"""
Tests for elevenlabs_tts_tool.voices module.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import pytest

from elevenlabs_tts_tool.voices import VoiceManager


def test_voice_manager_loads_voices() -> None:
    """Test that VoiceManager loads voices from lookup file."""
    manager = VoiceManager()
    voices = manager.list_voices()

    assert len(voices) > 0
    assert all(isinstance(name, str) for name, _ in voices)


def test_get_voice_id_for_rachel() -> None:
    """Test getting voice ID for rachel."""
    manager = VoiceManager()
    voice_id = manager.get_voice_id("rachel")

    assert voice_id == "21m00Tcm4TlvDq8ikWAM"
    assert isinstance(voice_id, str)


def test_get_voice_id_case_insensitive() -> None:
    """Test that voice lookup is case-insensitive."""
    manager = VoiceManager()

    voice_id_lower = manager.get_voice_id("rachel")
    voice_id_upper = manager.get_voice_id("RACHEL")
    voice_id_mixed = manager.get_voice_id("Rachel")

    assert voice_id_lower == voice_id_upper == voice_id_mixed


def test_get_voice_id_invalid() -> None:
    """Test that getting invalid voice raises ValueError."""
    manager = VoiceManager()

    with pytest.raises(ValueError, match="Voice 'invalid_voice' not found"):
        manager.get_voice_id("invalid_voice")


def test_get_voice_profile() -> None:
    """Test getting complete voice profile."""
    manager = VoiceManager()
    profile = manager.get_voice_profile("rachel")

    assert profile.voice_id == "21m00Tcm4TlvDq8ikWAM"
    assert profile.name == "Rachel"
    assert profile.gender == "female"
    assert profile.age == "young"
    assert profile.accent == "American"


def test_get_default_voice_id() -> None:
    """Test getting default voice ID."""
    manager = VoiceManager()
    default_id = manager.get_default_voice_id()

    assert default_id == "21m00Tcm4TlvDq8ikWAM"
