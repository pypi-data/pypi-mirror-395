"""
Shell completion command implementation.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import click
from click.shell_completion import BashComplete, FishComplete, ZshComplete

from elevenlabs_tts_tool.logging_config import get_logger

logger = get_logger(__name__)


@click.command()
@click.argument("shell", type=click.Choice(["bash", "zsh", "fish"]))
def completion(shell: str) -> None:
    """Generate shell completion script.

    SHELL: The shell type (bash, zsh, fish)

    Install instructions:

    \b
    # Bash (add to ~/.bashrc):
    eval "$(elevenlabs-tts-tool completion bash)"

    \b
    # Zsh (add to ~/.zshrc):
    eval "$(elevenlabs-tts-tool completion zsh)"

    \b
    # Fish (add to ~/.config/fish/completions/elevenlabs-tts-tool.fish):
    elevenlabs-tts-tool completion fish > ~/.config/fish/completions/elevenlabs-tts-tool.fish

    \b
    Examples:

    \b
        # Generate bash completion script
        elevenlabs-tts-tool completion bash

    \b
        # Install bash completion (add to ~/.bashrc)
        echo 'eval "$(elevenlabs-tts-tool completion bash)"' >> ~/.bashrc

    \b
        # Install zsh completion (add to ~/.zshrc)
        echo 'eval "$(elevenlabs-tts-tool completion zsh)"' >> ~/.zshrc

    \b
        # Install fish completion
        mkdir -p ~/.config/fish/completions
        elevenlabs-tts-tool completion fish > \\
            ~/.config/fish/completions/elevenlabs-tts-tool.fish

    \b
    For better performance, save completion to a file:

    \b
        # Bash
        elevenlabs-tts-tool completion bash > ~/.elevenlabs-tts-tool-complete.bash
        echo 'source ~/.elevenlabs-tts-tool-complete.bash' >> ~/.bashrc

    \b
        # Zsh
        elevenlabs-tts-tool completion zsh > ~/.elevenlabs-tts-tool-complete.zsh
        echo 'source ~/.elevenlabs-tts-tool-complete.zsh' >> ~/.zshrc
    """
    logger.info(f"Generating {shell} completion script")
    logger.debug(f"Getting completion class for shell: {shell}")

    ctx = click.get_current_context()

    # Get the appropriate completion class
    completion_classes = {
        "bash": BashComplete,
        "zsh": ZshComplete,
        "fish": FishComplete,
    }

    completion_class = completion_classes.get(shell)
    if completion_class:
        logger.debug(f"Creating completer with command path: {ctx.command_path}")
        completer = completion_class(
            cli=ctx.find_root().command,
            ctx_args={},
            prog_name=ctx.find_root().info_name or "elevenlabs-tts-tool",
            complete_var=f"_{ctx.find_root().info_name or 'elevenlabs_tts_tool'}_COMPLETE".upper(),
        )
        completion_script = completer.source()
        logger.debug(f"Generated completion script ({len(completion_script)} characters)")
        click.echo(completion_script)
    else:
        logger.error(f"Unsupported shell: {shell}")
        raise click.BadParameter(f"Unsupported shell: {shell}")
