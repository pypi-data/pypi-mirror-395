"""
Model management for ElevenLabs text-to-speech models.

This module provides model metadata, validation, and discovery functionality
for all available ElevenLabs TTS models.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ModelInfo:
    """Metadata for an ElevenLabs TTS model."""

    name: str
    model_id: str
    description: str
    languages: int
    char_limit: int
    latency: str
    best_for: str
    status: str  # "stable", "alpha", "deprecated"
    notes: str = ""


# All available ElevenLabs TTS models
AVAILABLE_MODELS: dict[str, ModelInfo] = {
    "eleven_v3": ModelInfo(
        name="Eleven v3 (Alpha)",
        model_id="eleven_v3",
        description="Most emotionally expressive",
        languages=70,
        char_limit=5000,
        latency="High",
        best_for="Emotional dialogue, audiobooks",
        status="alpha",
        notes="Alpha release - may have inconsistencies. Generate multiple options.",
    ),
    "eleven_multilingual_v2": ModelInfo(
        name="Eleven Multilingual v2",
        model_id="eleven_multilingual_v2",
        description="Highest production quality",
        languages=29,
        char_limit=10000,
        latency="Medium",
        best_for="Professional content, e-learning",
        status="stable",
    ),
    "eleven_flash_v2_5": ModelInfo(
        name="Eleven Flash v2.5",
        model_id="eleven_flash_v2_5",
        description="Ultra-low latency (~75ms)",
        languages=32,
        char_limit=40000,
        latency="Ultra-low (~75ms)",
        best_for="Real-time agents, bulk processing",
        status="stable",
        notes="50% cheaper per character",
    ),
    "eleven_turbo_v2_5": ModelInfo(
        name="Eleven Turbo v2.5",
        model_id="eleven_turbo_v2_5",
        description="Balanced quality/speed",
        languages=32,
        char_limit=40000,
        latency="Low (~250ms)",
        best_for="General-purpose TTS",
        status="stable",
        notes="50% cheaper per character. Current default.",
    ),
    "eleven_turbo_v2": ModelInfo(
        name="Eleven Turbo v2",
        model_id="eleven_turbo_v2",
        description="Previous generation turbo",
        languages=32,
        char_limit=10000,
        latency="Low (~250ms)",
        best_for="Legacy projects",
        status="deprecated",
        notes="Superseded by Turbo v2.5. Migrate for 50% cost savings.",
    ),
    "eleven_flash_v2": ModelInfo(
        name="Eleven Flash v2",
        model_id="eleven_flash_v2",
        description="Previous generation flash",
        languages=29,
        char_limit=10000,
        latency="Low",
        best_for="Legacy projects",
        status="deprecated",
        notes="Superseded by Flash v2.5. Migrate for 50% cost savings.",
    ),
    "eleven_monolingual_v1": ModelInfo(
        name="Eleven English v1",
        model_id="eleven_monolingual_v1",
        description="English-only (deprecated)",
        languages=1,
        char_limit=5000,
        latency="Medium",
        best_for="Legacy English-only projects",
        status="deprecated",
        notes="DEPRECATED. Migrate to eleven_multilingual_v2.",
    ),
    "eleven_multilingual_v1": ModelInfo(
        name="Eleven Multilingual v1",
        model_id="eleven_multilingual_v1",
        description="First generation multilingual",
        languages=20,
        char_limit=5000,
        latency="Medium",
        best_for="Legacy multilingual projects",
        status="deprecated",
        notes="DEPRECATED. Migrate to eleven_multilingual_v2.",
    ),
}

# Default model
DEFAULT_MODEL = "eleven_turbo_v2_5"


def validate_model(model_id: str) -> str:
    """
    Validate model ID and return normalized model ID.

    Args:
        model_id: Model ID to validate (case-insensitive)

    Returns:
        Normalized model ID

    Raises:
        ValueError: If model ID is invalid with helpful error message
    """
    normalized_id = model_id.lower().strip()

    if normalized_id not in AVAILABLE_MODELS:
        available = ", ".join(sorted(AVAILABLE_MODELS.keys()))
        msg = (
            f"Invalid model ID: '{model_id}'\n\n"
            f"Available models:\n{available}\n\n"
            "Run 'elevenlabs-tty-tool list-models' to see all models with details."
        )
        raise ValueError(msg)

    return normalized_id


def is_deprecated(model_id: str) -> bool:
    """
    Check if a model is deprecated.

    Args:
        model_id: Model ID to check

    Returns:
        True if model is deprecated, False otherwise
    """
    model_info = AVAILABLE_MODELS.get(model_id.lower())
    return model_info is not None and model_info.status == "deprecated"


def get_deprecation_warning(model_id: str) -> str | None:
    """
    Get deprecation warning message for a model.

    Args:
        model_id: Model ID to check

    Returns:
        Warning message if deprecated, None otherwise
    """
    model_info = AVAILABLE_MODELS.get(model_id.lower())
    if model_info and model_info.status == "deprecated":
        return f"WARNING: {model_info.name} is deprecated. {model_info.notes}"
    return None
