"""CLI entry point for elevenlabs-tts-tool.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import click

from elevenlabs_tts_tool.commands import (
    completion,
    info,
    list_models,
    list_voices,
    pricing,
    synthesize,
    update_voices,
)
from elevenlabs_tts_tool.logging_config import setup_logging


@click.group()
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Enable verbose output (use -v for INFO, -vv for DEBUG, -vvv for TRACE)",
)
@click.version_option(version="0.2.0")
@click.pass_context
def main(ctx: click.Context, verbose: int) -> None:
    """
    ElevenLabs TTS CLI - Professional text-to-speech synthesis.

    Convert text to natural-sounding speech using ElevenLabs' advanced AI voices.

    Use -v for informational messages, -vv for detailed debugging,
    or -vvv to see full API request/response details.
    """
    # Setup logging based on verbosity
    setup_logging(verbose)

    # Store verbose count in context for subcommands
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose


# Register commands
main.add_command(completion)
main.add_command(info)
main.add_command(list_models)
main.add_command(list_voices)
main.add_command(pricing)
main.add_command(synthesize)
main.add_command(update_voices)


if __name__ == "__main__":
    main()
