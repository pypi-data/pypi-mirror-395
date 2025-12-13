"""
Infinite streaming TTS command.

Implements continuous text-to-speech using the producer-consumer pattern.
Reads markdown/text input, splits into chunks, and streams audio seamlessly
without pop artifacts between paragraphs.

Supports two output modes:
- Speaker: Real-time playback (seamless, no artifacts)
- File: Fast offline rendering (20-50x real-time on M4)

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import sys
import time
from collections.abc import Iterator
from pathlib import Path

import click
import numpy as np
import soundfile as sf

from kokoro_tts_tool.engine import SAMPLE_RATE, get_engine
from kokoro_tts_tool.logging_config import get_logger
from kokoro_tts_tool.splitter import DEFAULT_CHUNK_SIZE_WORDS, TextChunk, split_text
from kokoro_tts_tool.streaming import DEFAULT_SILENCE_BETWEEN_CHUNKS_MS, AudioStreamer
from kokoro_tts_tool.voices import DEFAULT_VOICE, validate_voice

logger = get_logger(__name__)

# Default pause between paragraphs for file output (ms)
DEFAULT_FILE_PAUSE_MS = 300


def _read_input(stdin: bool, input_file: Path | None) -> str:
    """Read input text from stdin or file.

    Args:
        stdin: If True, read from stdin
        input_file: Path to input file (if not stdin)

    Returns:
        Input text content
    """
    if stdin:
        logger.debug("Reading from stdin...")
        if sys.stdin.isatty():
            click.echo(
                "Error: No input on stdin.\n\n"
                "Either pipe text to this command or use --input:\n"
                "  cat document.md | kokoro-tts-tool infinite --stdin\n"
                "  kokoro-tts-tool infinite --input document.md",
                err=True,
            )
            sys.exit(1)
        text = sys.stdin.read()
        logger.debug(f"Read {len(text)} characters from stdin")
        return text
    elif input_file:
        logger.debug(f"Reading from file: {input_file}")
        if not input_file.exists():
            click.echo(
                f"Error: File not found: {input_file}\n\n"
                "Verify the file path exists and try again.",
                err=True,
            )
            sys.exit(1)
        text = input_file.read_text(encoding="utf-8")
        logger.debug(f"Read {len(text)} characters from file")
        return text
    else:
        click.echo(
            "Error: No input provided.\n\n"
            "Use --stdin or --input to provide text:\n"
            "  cat document.md | kokoro-tts-tool infinite --stdin\n"
            "  kokoro-tts-tool infinite --input document.md",
            err=True,
        )
        sys.exit(1)


def _generate_audio_chunks(
    chunks: list[TextChunk],
    voice: str,
    speed: float,
    pause_ms: int,
    show_progress: bool = True,
) -> Iterator[tuple[np.ndarray, int, TextChunk]]:
    """Generate audio for each text chunk.

    This is the producer that yields audio samples for each chunk.

    Args:
        chunks: List of text chunks to process
        voice: Voice ID
        speed: Speech speed
        pause_ms: Pause between chunks in milliseconds
        show_progress: Whether to print progress to stderr

    Yields:
        Tuple of (audio_samples, sample_rate, chunk)
    """
    engine = get_engine()
    engine.load()

    for i, chunk in enumerate(chunks):
        if show_progress:
            preview = chunk.content[:60] + "..." if len(chunk.content) > 60 else chunk.content
            location = ""
            if chunk.chapter:
                location = f"[{chunk.chapter}] "
            elif chunk.section:
                location = f"[{chunk.section}] "
            click.echo(f"[{i + 1}/{len(chunks)}] {location}{preview}", err=True)

        # Use generate_long to handle text that may exceed phoneme limit
        samples, sample_rate = engine.generate_long(
            chunk.content,
            voice=voice,
            speed=speed,
        )

        yield samples, sample_rate, chunk


def _play_to_speaker(
    chunks: list[TextChunk],
    voice: str,
    speed: float,
    pause_ms: int,
) -> None:
    """Stream audio to speakers using producer-consumer pattern.

    Args:
        chunks: List of text chunks
        voice: Voice ID
        speed: Speech speed
        pause_ms: Pause between chunks in milliseconds
    """
    click.echo("Starting continuous playback (Ctrl+C to stop)...\n", err=True)

    with AudioStreamer() as streamer:
        for i, (samples, sample_rate, chunk) in enumerate(
            _generate_audio_chunks(chunks, voice, speed, pause_ms)
        ):
            streamer.add_audio(samples)

            # Add pause between chunks (not after last)
            if i < len(chunks) - 1:
                streamer.add_silence(pause_ms)

        streamer.signal_end()
        streamer.wait_until_finished()

    click.echo("\nPlayback complete!", err=True)


def _render_to_file(
    output_path: Path,
    chunks: list[TextChunk],
    voice: str,
    speed: float,
    pause_ms: int,
) -> float:
    """Render audio to file at maximum speed.

    This is significantly faster than real-time playback (20-50x on M4).

    Args:
        output_path: Output WAV file path
        chunks: List of text chunks
        voice: Voice ID
        speed: Speech speed
        pause_ms: Pause between chunks in milliseconds

    Returns:
        Total rendering time in seconds
    """
    click.echo(f"Rendering to {output_path} (fast offline mode)...\n", err=True)

    start_time = time.time()
    total_samples = 0

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Open file once and stream directly to disk
    with sf.SoundFile(
        str(output_path),
        mode="w",
        samplerate=SAMPLE_RATE,
        channels=1,
        format="WAV",
    ) as audio_file:
        for i, (samples, sample_rate, chunk) in enumerate(
            _generate_audio_chunks(chunks, voice, speed, pause_ms)
        ):
            # Ensure correct shape for soundfile (1D)
            if len(samples.shape) > 1:
                samples = samples.flatten()

            audio_file.write(samples)
            total_samples += len(samples)

            # Add silence between chunks (not after last)
            if i < len(chunks) - 1 and pause_ms > 0:
                silence_samples = int(SAMPLE_RATE * pause_ms / 1000)
                silence = np.zeros(silence_samples, dtype=samples.dtype)
                audio_file.write(silence)
                total_samples += silence_samples

    render_time = time.time() - start_time
    audio_duration = total_samples / SAMPLE_RATE

    click.echo(f"\nRendered {audio_duration:.1f}s of audio in {render_time:.1f}s", err=True)
    click.echo(f"Speed: {audio_duration / render_time:.1f}x real-time", err=True)
    click.echo(f"Saved to: {output_path}", err=True)

    return render_time


@click.command()
@click.option(
    "--stdin",
    "-s",
    is_flag=True,
    help="Read text from stdin stream",
)
@click.option(
    "--input",
    "-i",
    "input_file",
    type=click.Path(exists=False, path_type=Path),
    help="Input text/markdown file to read",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(path_type=Path),
    help="Save audio to WAV file instead of playing (fast offline mode)",
)
@click.option(
    "--voice",
    default=DEFAULT_VOICE,
    help=f"Voice ID to use (default: {DEFAULT_VOICE})",
)
@click.option(
    "--speed",
    type=click.FloatRange(0.5, 2.0),
    default=1.0,
    help="Speech speed from 0.5 (slow) to 2.0 (fast) (default: 1.0)",
)
@click.option(
    "--chunk-size",
    type=click.IntRange(50, 1000),
    default=DEFAULT_CHUNK_SIZE_WORDS,
    help=f"Target words per chunk (default: {DEFAULT_CHUNK_SIZE_WORDS})",
)
@click.option(
    "--pause",
    type=click.IntRange(0, 2000),
    default=DEFAULT_SILENCE_BETWEEN_CHUNKS_MS,
    help=f"Pause between chunks in ms (default: {DEFAULT_SILENCE_BETWEEN_CHUNKS_MS})",
)
@click.option(
    "--no-markdown",
    is_flag=True,
    help="Treat input as plain text (skip markdown header splitting)",
)
def infinite(
    stdin: bool,
    input_file: Path | None,
    output: Path | None,
    voice: str,
    speed: float,
    chunk_size: int,
    pause: int,
    no_markdown: bool,
) -> None:
    """Stream text-to-speech continuously without audio artifacts.

    Reads markdown or plain text, splits it intelligently into chunks,
    and either streams to speakers or renders to file.

    Output Modes:
    - Speaker (default): Real-time playback, seamless audio
    - File (--output): Fast offline rendering (20-50x real-time on M4)

    Best for:
    - Study materials and books
    - Long-form articles
    - Audiobook generation

    Examples:

    \b
        # Stream a markdown file to speakers
        kokoro-tts-tool infinite --input book.md

    \b
        # Render to WAV file (fast, ~2-3min for 1hr audio)
        kokoro-tts-tool infinite --input book.md --output audiobook.wav

    \b
        # Pipe from stdin
        cat chapter.md | kokoro-tts-tool infinite --stdin

    \b
        # With custom voice and speed
        kokoro-tts-tool infinite --input notes.md \\
            --voice am_adam \\
            --speed 1.2

    \b
        # Render audiobook with narrator voice
        kokoro-tts-tool infinite --input book.md \\
            --output book.wav \\
            --voice bm_george \\
            --speed 0.95

    \b
        # Shorter chunks for studying
        kokoro-tts-tool infinite --input study.md \\
            --chunk-size 200 \\
            --pause 600

    \b
        # Plain text (no markdown processing)
        kokoro-tts-tool infinite --input plain.txt --no-markdown

    \b
    Input Format:
        Markdown with headers (#, ##, ###) works best.
        The splitter respects document structure:
        - Splits by headers first (chapters/sections)
        - Then by paragraphs
        - Then by sentences (if needed)

    \b
    Available Voices:
        Use 'kokoro-tts-tool list-voices' to see all 60+ voices.
        Recommended for books: am_adam, bm_george, af_heart
    """
    try:
        # Validate voice
        validated_voice = validate_voice(voice)

        # Validate output format
        if output and not str(output).lower().endswith(".wav"):
            click.echo(
                f"Error: Output file must have .wav extension. Got: {output}\n\n"
                "What to do:\n"
                "  Change output to: --output audiobook.wav",
                err=True,
            )
            sys.exit(1)

        # Read input
        text = _read_input(stdin, input_file)

        if not text.strip():
            click.echo("Error: Input is empty.\n\nProvide non-empty text.", err=True)
            sys.exit(1)

        # Split into chunks
        click.echo(f"Processing input ({len(text)} characters)...", err=True)
        chunks = split_text(
            text,
            chunk_size_words=chunk_size,
            use_markdown_headers=not no_markdown,
        )

        if not chunks:
            click.echo("Error: No text chunks generated.\n\nInput may be empty.", err=True)
            sys.exit(1)

        click.echo(f"Split into {len(chunks)} chunks", err=True)
        click.echo(f"Voice: {validated_voice}, Speed: {speed}x", err=True)

        # Route to appropriate output
        if output:
            # Fast offline rendering to file
            is_default_pause = pause == DEFAULT_SILENCE_BETWEEN_CHUNKS_MS
            file_pause = DEFAULT_FILE_PAUSE_MS if is_default_pause else pause
            _render_to_file(output, chunks, validated_voice, speed, file_pause)
        else:
            # Real-time speaker playback
            _play_to_speaker(chunks, validated_voice, speed, pause)

        total_words = sum(len(c.content.split()) for c in chunks)
        click.echo(f"Processed {len(chunks)} chunks (~{total_words} words)", err=True)

    except KeyboardInterrupt:
        click.echo("\n\nInterrupted by user.", err=True)
        sys.exit(0)
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
