"""
Init command for kokoro-tts-tool.

Handles model downloading and initialization.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import sys

import click

from kokoro_tts_tool.logging_config import get_logger
from kokoro_tts_tool.models import download_models, get_model_info, models_exist

logger = get_logger(__name__)


@click.command("init")
@click.option(
    "--force",
    "-f",
    is_flag=True,
    help="Re-download models even if they exist",
)
def init_command(force: bool) -> None:
    """Download and initialize TTS models.

    Downloads the Kokoro ONNX model (~300MB) and voice embeddings (~50MB)
    required for speech synthesis. Files are cached in ~/.kokoro-tts/models/.

    Examples:

    \b
        # Download models (skips if already present)
        kokoro-tts-tool init

    \b
        # Force re-download
        kokoro-tts-tool init --force
    """
    logger.info("Initializing Kokoro TTS models")

    model_info = get_model_info()

    if models_exist() and not force:
        click.echo("\nModels already downloaded!")
        click.echo(f"  Model: {model_info.get('model_size_mb', 'N/A')} MB")
        click.echo(f"  Voices: {model_info.get('voices_size_mb', 'N/A')} MB")
        click.echo(f"  Location: {model_info['models_dir']}")
        click.echo("\nUse --force to re-download.")
        return

    click.echo("\nDownloading Kokoro TTS models...")
    click.echo("This may take a few minutes on first run.\n")

    try:
        model_path, voices_path = download_models(force=force)

        click.echo("\nModels downloaded successfully!")
        click.echo(f"  Model: {model_path}")
        click.echo(f"  Voices: {voices_path}")
        click.echo("\nYou're ready to go!")
        click.echo('  kokoro-tts-tool synthesize "Hello world"')

    except RuntimeError as e:
        logger.error(f"Download failed: {e}")
        click.echo(f"\nError: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        logger.debug("Full traceback:", exc_info=True)
        click.echo(f"\nError: {e}", err=True)
        sys.exit(1)
