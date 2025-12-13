"""
Info command for kokoro-tts-tool.

Displays configuration status and system information.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import click

from kokoro_tts_tool.logging_config import get_logger
from kokoro_tts_tool.models import get_model_info
from kokoro_tts_tool.voices import DEFAULT_VOICE, list_languages

logger = get_logger(__name__)


@click.command("info")
def info_command() -> None:
    """Display configuration and model status.

    Shows information about the Kokoro TTS installation including model
    download status, file locations, and available options.

    Examples:

    \b
        # Show status
        kokoro-tts-tool info
    """
    logger.info("Displaying configuration info")

    click.echo("\nKokoro TTS Tool - Configuration")
    click.echo("=" * 50)

    # Model status
    model_info = get_model_info()

    click.echo("\nModel Status:")
    if model_info["ready"]:
        click.echo("  Status: Ready")
        click.echo(f"  Model size: {model_info.get('model_size_mb', 'N/A')} MB")
        click.echo(f"  Voices size: {model_info.get('voices_size_mb', 'N/A')} MB")
    else:
        click.echo("  Status: Not downloaded")
        click.echo("  Run 'kokoro-tts-tool init' to download models")

    click.echo("\nModels Directory:")
    click.echo(f"  {model_info['models_dir']}")

    if model_info.get("model_path"):
        click.echo("\nModel Files:")
        click.echo(f"  Model: {model_info['model_path']}")
        click.echo(f"  Voices: {model_info.get('voices_path', 'N/A')}")

    # Defaults
    click.echo("\nDefaults:")
    click.echo(f"  Voice: {DEFAULT_VOICE}")
    click.echo("  Speed: 1.0x")
    click.echo("  Output: Speakers (or WAV file)")

    # Languages
    languages = list_languages()
    click.echo(f"\nSupported Languages ({len(languages)}):")
    click.echo(f"  {', '.join(languages)}")

    # Performance info
    click.echo("\nPerformance:")
    click.echo("  Sample rate: 24,000 Hz")
    click.echo("  Runtime: ONNX (CPU optimized)")
    click.echo("  Speed: Near real-time on Apple Silicon")

    # Quick start
    click.echo("\nQuick Start:")
    click.echo('  kokoro-tts-tool synthesize "Hello world"')
    click.echo("  kokoro-tts-tool list-voices")

    logger.info("Info display complete")
