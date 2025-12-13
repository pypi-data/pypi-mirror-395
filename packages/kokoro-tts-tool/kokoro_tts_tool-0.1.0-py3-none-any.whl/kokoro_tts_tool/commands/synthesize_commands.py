"""
Text-to-speech synthesis CLI commands.

Implements the primary TTS functionality as a CLI command, handling
user input (text or stdin), voice selection, and output routing
(speakers or file).

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import sys
from pathlib import Path

import click

from kokoro_tts_tool.engine import (
    DEFAULT_SILENCE_MS,
    read_from_stdin,
    synthesize_and_play,
    synthesize_to_file,
)
from kokoro_tts_tool.logging_config import get_logger
from kokoro_tts_tool.voices import DEFAULT_VOICE, validate_voice

logger = get_logger(__name__)


@click.command()
@click.argument("text", required=False)
@click.option("--stdin", "-s", is_flag=True, help="Read text from stdin instead of argument")
@click.option(
    "--voice",
    "-v",
    default=DEFAULT_VOICE,
    help=f"Voice ID to use (default: {DEFAULT_VOICE})",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(path_type=Path),
    help="Save audio to file instead of playing through speakers (WAV format)",
)
@click.option(
    "--speed",
    type=click.FloatRange(0.5, 2.0),
    default=1.0,
    help="Speech speed from 0.5 (slow) to 2.0 (fast) (default: 1.0)",
)
@click.option(
    "--silence",
    type=click.IntRange(0, 5000),
    default=DEFAULT_SILENCE_MS,
    help=f"Trailing silence in milliseconds to avoid audio cutoff (default: {DEFAULT_SILENCE_MS})",
)
def synthesize(
    text: str | None,
    stdin: bool,
    voice: str,
    output: Path | None,
    speed: float,
    silence: int,
) -> None:
    """Convert text to speech using local Kokoro TTS.

    Synthesizes text using the Kokoro TTS model running locally on your
    Apple Silicon Mac. Audio can be played through speakers or saved to file.

    The model files (~350MB) are downloaded automatically on first use and
    cached in ~/.kokoro-tts/models/.

    Examples:

    \b
        # Play text with default voice (af_heart)
        kokoro-tts-tool synthesize "Hello world"

    \b
        # Use different voice
        kokoro-tts-tool synthesize "Hello" --voice am_adam

    \b
        # Save to file
        kokoro-tts-tool synthesize "Hello" --output speech.wav

    \b
        # Read from stdin
        echo "Hello world" | kokoro-tts-tool synthesize --stdin

    \b
        # Adjust playback speed
        kokoro-tts-tool synthesize "Hello" --speed 1.5

    \b
        # Multiple options combined
        cat article.txt | kokoro-tts-tool synthesize --stdin \\
            --voice bf_emma \\
            --output article.wav \\
            --speed 0.9

    \b
    Output Format:
        Audio is played directly through speakers by default.
        Use --output to save to a WAV file (24kHz, mono, 16-bit).

    \b
    Available Voices:
        Use 'kokoro-tts-tool list-voices' to see all 60+ voices.
        Examples: af_heart, am_adam, bf_emma, bm_george
    """
    try:
        # Validate input
        if stdin:
            logger.debug("Reading text from stdin")
            input_text = read_from_stdin()
        elif text:
            input_text = text
        else:
            logger.error("No text provided")
            click.echo(
                "Error: No text provided.\n\n"
                "Provide text as argument or use --stdin:\n"
                "  kokoro-tts-tool synthesize 'your text'\n"
                "  echo 'text' | kokoro-tts-tool synthesize --stdin\n\n"
                "Use --help for more examples.",
                err=True,
            )
            sys.exit(1)

        if not input_text.strip():
            click.echo(
                "Error: Empty text provided.\n\nProvide non-empty text to synthesize.",
                err=True,
            )
            sys.exit(1)

        # Validate voice
        logger.debug(f"Validating voice: {voice}")
        validated_voice = validate_voice(voice)

        # Show what we're doing
        truncated = input_text[:50] + "..." if len(input_text) > 50 else input_text
        click.echo(f"Synthesizing: {truncated}", err=True)
        click.echo(f"Voice: {validated_voice}, Speed: {speed}x", err=True)

        # Execute synthesis
        if output:
            # Validate output format
            if not str(output).lower().endswith(".wav"):
                click.echo(
                    f"Error: Output file must have .wav extension. Got: {output}\n\n"
                    "What to do:\n"
                    "  Change output to: --output speech.wav",
                    err=True,
                )
                sys.exit(1)

            logger.info(f"Synthesizing audio to file: {output}")
            char_count = synthesize_to_file(
                input_text,
                output,
                validated_voice,
                speed,
            )
            click.echo(f"\nAudio saved to: {output}", err=True)
        else:
            logger.info("Synthesizing audio for playback")
            char_count = synthesize_and_play(
                input_text,
                validated_voice,
                speed,
                silence,
            )
            click.echo("\nPlayback complete!", err=True)

        # Show processing summary
        click.echo(f"Processed {char_count} characters", err=True)

    except ValueError as e:
        logger.error(f"Validation error: {e}")
        logger.debug("Full traceback:", exc_info=True)
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except RuntimeError as e:
        logger.error(f"Runtime error: {e}")
        logger.debug("Full traceback:", exc_info=True)
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        logger.debug("Full traceback:", exc_info=True)
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
