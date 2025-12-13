"""
Model listing command implementation.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import click

from elevenlabs_tts_tool.logging_config import get_logger
from elevenlabs_tts_tool.models import AVAILABLE_MODELS, DEFAULT_MODEL

logger = get_logger(__name__)


@click.command()
def list_models() -> None:
    """
    List all available ElevenLabs TTS models.

    Displays model names, IDs, characteristics, and use cases.
    Use this command to discover models before using --model in synthesize.

    \b
    Examples:

    \b
        # List all available models
        elevenlabs-tty-tool list-models

    \b
        # Filter models by status
        elevenlabs-tty-tool list-models | grep stable
        elevenlabs-tty-tool list-models | grep deprecated

    \b
        # Find ultra-low latency models
        elevenlabs-tty-tool list-models | grep -i "ultra-low"
    """
    logger.info("Listing available TTS models")
    logger.debug(f"Total models in registry: {len(AVAILABLE_MODELS)}")

    # Group models by status
    current_gen = []
    legacy = []

    for model_id, info in AVAILABLE_MODELS.items():
        if info.status in ["stable", "alpha"]:
            current_gen.append((model_id, info))
        else:
            legacy.append((model_id, info))

    logger.debug(f"Current generation models: {len(current_gen)}")
    logger.debug(f"Legacy models: {len(legacy)}")

    # Display current generation models
    click.echo("\nCurrent Generation Models:\n")

    for idx, (model_id, info) in enumerate(current_gen, 1):
        # Show star indicator for default model
        default_marker = " ⭐ (Current default)" if model_id == DEFAULT_MODEL else ""
        status_marker = " (Alpha)" if info.status == "alpha" else ""

        click.echo(f"{idx}. {info.name}{status_marker} - {info.model_id}{default_marker}")
        click.echo(f"   - {info.description}")
        click.echo(f"   - {info.languages}+ languages")
        click.echo(f"   - {info.char_limit:,} char limit")
        click.echo(f"   - {info.latency}")
        click.echo(f"   - Best for: {info.best_for}")

        if info.notes:
            click.echo(f"   - Note: {info.notes}")

        click.echo()

    # Display legacy models if any
    if legacy:
        click.echo("\nLegacy Models (Deprecated):\n")

        for model_id, info in legacy:
            click.echo(f"- {info.model_id}")
            click.echo(f"  {info.notes}")
            click.echo()

    click.echo("All models are available on the Free tier.\n")


@click.command()
def pricing() -> None:
    """
    Display ElevenLabs pricing tiers and features.

    Shows pricing information as of November 2025 including minutes included,
    audio quality, concurrency limits, and API formats for each tier.

    \b
    Important Notes:
        - v3 models cost TWICE as much as Flash models (half the minutes/tokens)
        - For Claude Code integration, use Flash models for cost efficiency
        - Prices and features subject to change - check elevenlabs.io/pricing

    \b
    Examples:

    \b
        # View pricing information
        elevenlabs-tty-tool pricing

    \b
        # Find specific tier
        elevenlabs-tty-tool pricing | grep Creator
        elevenlabs-tty-tool pricing | grep "44.1kHz PCM"
    """
    click.echo("\n" + "=" * 90)
    click.echo("ElevenLabs Pricing (as of November 2025)")
    click.echo("=" * 90)
    click.echo()
    click.echo("⚠️  IMPORTANT: v3 models cost 2x as much as Flash models (half the minutes/tokens)")
    click.echo("💡 RECOMMENDATION: Use Flash models for Claude Code integration to optimize costs")
    click.echo()
    click.echo("=" * 90)
    click.echo()

    # Pricing table data
    tiers = [
        {
            "name": "Free",
            "price": "$0/mo",
            "minutes": "~10",
            "additional": "-",
            "quality": "128 kbps, 44.1kHz",
            "concurrency": "2",
            "priority": "3",
            "formats": "16kHz PCM, uLaw",
        },
        {
            "name": "Starter",
            "price": "$5/mo",
            "minutes": "~30",
            "additional": "-",
            "quality": "128 kbps, 44.1kHz",
            "concurrency": "3",
            "priority": "4",
            "formats": "22.05kHz PCM, uLaw",
        },
        {
            "name": "Creator",
            "price": "$11/mo",
            "minutes": "~100",
            "additional": "~$0.30/min",
            "quality": "128 & 192 kbps (API), 44.1kHz",
            "concurrency": "5",
            "priority": "5",
            "formats": "24kHz PCM, uLaw",
        },
        {
            "name": "Pro",
            "price": "$99/mo",
            "minutes": "~500",
            "additional": "~$0.24/min",
            "quality": "128 & 192 kbps (Studio & API), 44.1kHz",
            "concurrency": "10",
            "priority": "5",
            "formats": "44.1kHz PCM, uLaw",
        },
        {
            "name": "Scale",
            "price": "$330/mo",
            "minutes": "~2,000",
            "additional": "~$0.18/min",
            "quality": "128 & 192 kbps (Studio & API), 44.1kHz",
            "concurrency": "15",
            "priority": "5",
            "formats": "44.1kHz PCM, uLaw",
        },
        {
            "name": "Business",
            "price": "$1,320/mo",
            "minutes": "~11,000",
            "additional": "~$0.12/min",
            "quality": "128 & 192 kbps (Studio & API), 44.1kHz",
            "concurrency": "15",
            "priority": "5",
            "formats": "44.1kHz PCM, uLaw",
        },
    ]

    # Print header
    header = (
        f"{'Tier':<12} {'Price':<12} {'Minutes':<10} {'Additional':<15} "
        f"{'Quality':<38} {'Concurrency':<12} {'Priority':<10}"
    )
    click.echo(header)
    click.echo("-" * 90)

    # Print each tier
    for tier in tiers:
        row = (
            f"{tier['name']:<12} {tier['price']:<12} {tier['minutes']:<10} "
            f"{tier['additional']:<15} {tier['quality']:<38} "
            f"{tier['concurrency']:<12} {tier['priority']:<10}"
        )
        click.echo(row)

    click.echo("-" * 90)
    click.echo()

    # Print API formats section
    click.echo("API Formats by Tier:")
    click.echo()
    for tier in tiers:
        click.echo(f"  {tier['name']:<12} - {tier['formats']}")

    click.echo()
    click.echo("=" * 90)
    click.echo()
    click.echo("📊 Model Cost Multipliers:")
    click.echo("  - Flash/Turbo v2.5 models: Standard pricing")
    click.echo("  - v3 models: 2x cost (half the included minutes)")
    click.echo()
    click.echo("💡 Cost Optimization Tips:")
    click.echo("  - Use Flash v2.5 for high-volume or real-time applications")
    click.echo("  - Use Turbo v2.5 for general-purpose TTS (current default)")
    click.echo("  - Reserve v3 for content requiring emotional expression")
    click.echo("  - Use Multilingual v2 for highest quality professional content")
    click.echo()
    click.echo("🔗 For latest pricing: https://elevenlabs.io/pricing")
    click.echo()
    click.echo("=" * 90)
    click.echo()
