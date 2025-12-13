"""
Voice commands for kokoro-tts-tool.

This module provides commands for listing and managing TTS voices.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import click

from kokoro_tts_tool.logging_config import get_logger
from kokoro_tts_tool.voices import list_accents, list_languages, list_voices

logger = get_logger(__name__)


def format_table_row(
    voice_id: str,
    name: str,
    gender: str,
    accent: str,
    grade: str,
    description: str,
) -> str:
    """Format a row for table display with consistent column widths."""
    return f"  {voice_id:<14} {name:<12} {gender:<8} {accent:<12} {grade:<6} {description:<40}"


@click.command("list-voices")
@click.option(
    "--language",
    "-l",
    help="Filter by language (e.g., English, Japanese, Mandarin)",
)
@click.option(
    "--gender",
    "-g",
    type=click.Choice(["Male", "Female"], case_sensitive=False),
    help="Filter by gender",
)
@click.option(
    "--json",
    "as_json",
    is_flag=True,
    help="Output as JSON for scripting",
)
def list_voices_command(
    language: str | None,
    gender: str | None,
    as_json: bool,
) -> None:
    """List all available Kokoro TTS voices.

    Displays voice information including ID, name, gender, accent, quality
    grade, and description. Over 60 voices across 9 languages are available.

    Examples:

    \b
        # List all voices
        kokoro-tts-tool list-voices

    \b
        # Filter by language
        kokoro-tts-tool list-voices --language English

    \b
        # Filter by gender
        kokoro-tts-tool list-voices --gender Female

    \b
        # Combined filters
        kokoro-tts-tool list-voices --language English --gender Male

    \b
        # JSON output for scripting
        kokoro-tts-tool list-voices --json

    \b
    Voice ID Format:
        The voice ID follows a pattern: [language][gender]_[name]
        - First letter: language (a=American, b=British, j=Japanese, etc.)
        - Second letter: gender (f=Female, m=Male)
        - Rest: voice name

    \b
    Quality Grades:
        - A/A-: Highest quality (af_heart, af_bella, am_adam)
        - B+/B: Good quality
        - B-: Acceptable quality
    """
    logger.info("Listing available Kokoro TTS voices")

    voices = list_voices(language=language, gender=gender)

    if not voices:
        click.echo("No voices found matching the criteria.", err=True)
        return

    if as_json:
        import json

        click.echo(json.dumps(voices, indent=2))
        return

    # Display header
    click.echo("\nKokoro TTS Voices")
    click.echo("=" * 100)
    click.echo(format_table_row("Voice ID", "Name", "Gender", "Accent", "Grade", "Description"))
    click.echo("-" * 100)

    # Display voices
    for voice in voices:
        click.echo(
            format_table_row(
                voice["id"],
                voice["name"],
                voice["gender"],
                voice["accent"],
                voice["grade"],
                voice["description"][:40],
            )
        )

    click.echo("-" * 100)
    click.echo(f"\nTotal: {len(voices)} voices")

    # Show available filters
    languages = list_languages()
    accents = list_accents()
    click.echo(f"\nLanguages: {', '.join(languages)}")
    click.echo(f"Accents: {', '.join(accents)}")

    logger.info(f"Listed {len(voices)} voices")
