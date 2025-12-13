"""
Tests for model management functionality.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import pytest

from elevenlabs_tts_tool.models import (
    AVAILABLE_MODELS,
    DEFAULT_MODEL,
    get_deprecation_warning,
    is_deprecated,
    validate_model,
)


def test_available_models_not_empty():
    """Test that available models dictionary is not empty."""
    assert len(AVAILABLE_MODELS) > 0


def test_all_models_have_required_fields():
    """Test that all models have required metadata fields."""
    for model_id, info in AVAILABLE_MODELS.items():
        assert info.name
        assert info.model_id == model_id
        assert info.description
        assert info.languages > 0
        assert info.char_limit > 0
        assert info.latency
        assert info.best_for
        assert info.status in ["stable", "alpha", "deprecated"]


def test_default_model_exists():
    """Test that default model exists in available models."""
    assert DEFAULT_MODEL in AVAILABLE_MODELS


def test_validate_model_valid():
    """Test validating a valid model ID."""
    result = validate_model("eleven_turbo_v2_5")
    assert result == "eleven_turbo_v2_5"


def test_validate_model_case_insensitive():
    """Test that model validation is case-insensitive."""
    result = validate_model("ELEVEN_TURBO_V2_5")
    assert result == "eleven_turbo_v2_5"


def test_validate_model_with_spaces():
    """Test that model validation trims spaces."""
    result = validate_model("  eleven_turbo_v2_5  ")
    assert result == "eleven_turbo_v2_5"


def test_validate_model_invalid():
    """Test that invalid model ID raises ValueError."""
    with pytest.raises(ValueError) as exc_info:
        validate_model("invalid_model")

    error_msg = str(exc_info.value)
    assert "Invalid model ID: 'invalid_model'" in error_msg
    assert "Available models:" in error_msg
    assert "list-models" in error_msg


def test_is_deprecated_stable_model():
    """Test that stable models are not deprecated."""
    assert not is_deprecated("eleven_turbo_v2_5")
    assert not is_deprecated("eleven_multilingual_v2")
    assert not is_deprecated("eleven_flash_v2_5")


def test_is_deprecated_alpha_model():
    """Test that alpha models are not deprecated."""
    assert not is_deprecated("eleven_v3")


def test_is_deprecated_deprecated_model():
    """Test that deprecated models are identified correctly."""
    assert is_deprecated("eleven_monolingual_v1")
    assert is_deprecated("eleven_multilingual_v1")
    assert is_deprecated("eleven_turbo_v2")
    assert is_deprecated("eleven_flash_v2")


def test_is_deprecated_invalid_model():
    """Test that invalid model returns False."""
    assert not is_deprecated("invalid_model")


def test_get_deprecation_warning_stable():
    """Test that stable models have no deprecation warning."""
    warning = get_deprecation_warning("eleven_turbo_v2_5")
    assert warning is None


def test_get_deprecation_warning_deprecated():
    """Test that deprecated models return warning message."""
    warning = get_deprecation_warning("eleven_monolingual_v1")
    assert warning is not None
    assert "WARNING" in warning
    assert "deprecated" in warning.lower()


def test_get_deprecation_warning_invalid_model():
    """Test that invalid model returns None."""
    warning = get_deprecation_warning("invalid_model")
    assert warning is None


def test_current_generation_models():
    """Test that current generation models are present."""
    current_gen = ["eleven_v3", "eleven_multilingual_v2", "eleven_flash_v2_5", "eleven_turbo_v2_5"]
    for model_id in current_gen:
        assert model_id in AVAILABLE_MODELS


def test_legacy_models():
    """Test that legacy models are present."""
    legacy = [
        "eleven_turbo_v2",
        "eleven_flash_v2",
        "eleven_monolingual_v1",
        "eleven_multilingual_v1",
    ]
    for model_id in legacy:
        assert model_id in AVAILABLE_MODELS
        assert AVAILABLE_MODELS[model_id].status == "deprecated"


def test_model_char_limits():
    """Test that model character limits are reasonable."""
    for model_id, info in AVAILABLE_MODELS.items():
        # Character limits should be between 1,000 and 50,000
        assert 1000 <= info.char_limit <= 50000, f"{model_id} has unexpected char limit"


def test_model_language_counts():
    """Test that model language counts are reasonable."""
    for model_id, info in AVAILABLE_MODELS.items():
        # Language counts should be between 1 and 100
        assert 1 <= info.languages <= 100, f"{model_id} has unexpected language count"
