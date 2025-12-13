"""CLI entry point for kokoro-tts-tool.

Provides local text-to-speech using Kokoro TTS on Apple Silicon.
Uses ONNX runtime for fast, efficient inference without GPU requirements.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import click

from kokoro_tts_tool.commands import (
    infinite,
    info_command,
    init_command,
    list_voices_command,
    synthesize,
)
from kokoro_tts_tool.completion import completion_command
from kokoro_tts_tool.logging_config import get_logger, setup_logging

logger = get_logger(__name__)


@click.group()
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Verbose output: -v (INFO), -vv (DEBUG), -vvv (TRACE with library logs)",
)
@click.version_option(version="0.1.0")
def main(verbose: int) -> None:
    """Local Text-to-Speech CLI using Kokoro TTS.

    A command-line tool for converting text to speech using the Kokoro-82M
    model running locally on your Apple Silicon Mac. No API keys required.

    Quick Start:

    \b
        # Initialize (downloads models on first run)
        kokoro-tts-tool init

    \b
        # Basic text-to-speech
        kokoro-tts-tool synthesize "Hello, world!"

    \b
        # List available voices (60+)
        kokoro-tts-tool list-voices

    \b
        # Show configuration
        kokoro-tts-tool info

    \b
    Examples:

        # Synthesize with specific voice
        kokoro-tts-tool synthesize "Hello" --voice am_adam --speed 1.2

        # Save to file
        kokoro-tts-tool synthesize "Hello" --output speech.wav

        # Pipe input
        echo "Hello" | kokoro-tts-tool synthesize --stdin

        # Filter voices by language
        kokoro-tts-tool list-voices --language Japanese

    \b
    Model Info:
        - Model: Kokoro-82M (82 million parameters)
        - Size: ~350MB (downloaded to ~/.kokoro-tts/models/)
        - Sample rate: 24,000 Hz
        - Languages: English, Japanese, Mandarin, Spanish, French, etc.
    """
    setup_logging(verbose)


# Register all commands
main.add_command(synthesize)
main.add_command(infinite)
main.add_command(list_voices_command, name="list-voices")
main.add_command(info_command, name="info")
main.add_command(init_command, name="init")
main.add_command(completion_command)


if __name__ == "__main__":
    main()
