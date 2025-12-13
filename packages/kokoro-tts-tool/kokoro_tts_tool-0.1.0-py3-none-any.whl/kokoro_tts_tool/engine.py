"""
TTS engine wrapper for Kokoro ONNX.

Provides a high-level interface for text-to-speech synthesis with support
for audio generation, file output, and speaker playback.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from pathlib import Path
from typing import Any

import numpy as np
import sounddevice as sd
import soundfile as sf

from kokoro_tts_tool.logging_config import get_logger
from kokoro_tts_tool.models import get_model_paths
from kokoro_tts_tool.voices import get_language_code

logger = get_logger(__name__)

# Audio constants
SAMPLE_RATE = 24000
CHANNELS = 1
DEFAULT_SILENCE_MS = 500  # Default trailing silence in milliseconds

# Kokoro model limits
# The model truncates phonemes at 510, which causes IndexError
# ~150 chars is a safe limit to avoid phoneme overflow
MAX_SAFE_CHARS = 150


class KokoroEngine:
    """Wrapper for Kokoro TTS engine using ONNX runtime."""

    def __init__(self) -> None:
        """Initialize the Kokoro engine."""
        self._engine: Any = None
        self._model_path: Path | None = None
        self._voices_path: Path | None = None

    def load(self) -> None:
        """Load the model into memory.

        Downloads models if necessary on first call.
        """
        if self._engine is not None:
            logger.debug("Engine already loaded")
            return

        logger.info("Loading Kokoro TTS engine...")

        # Get model paths (downloads if needed)
        self._model_path, self._voices_path = get_model_paths()

        # Import here to avoid import errors if not installed
        from kokoro_onnx import Kokoro

        logger.debug(f"Model path: {self._model_path}")
        logger.debug(f"Voices path: {self._voices_path}")

        self._engine = Kokoro(
            str(self._model_path),
            str(self._voices_path),
        )

        logger.info("Kokoro TTS engine loaded successfully")

    def is_loaded(self) -> bool:
        """Check if the engine is loaded.

        Returns:
            True if engine is ready
        """
        return self._engine is not None

    def generate(
        self,
        text: str,
        voice: str = "af_heart",
        speed: float = 1.0,
    ) -> tuple[np.ndarray, int]:
        """Generate speech audio from text.

        Args:
            text: Input text to synthesize
            voice: Voice ID (e.g., 'af_heart')
            speed: Speech speed multiplier (0.5-2.0)

        Returns:
            Tuple of (audio_samples, sample_rate)
        """
        self.load()

        if self._engine is None:
            raise RuntimeError("Engine failed to load")

        # Get language code from voice ID
        lang = get_language_code(voice)

        logger.debug(f"Generating speech: voice={voice}, speed={speed}, lang={lang}")
        logger.debug(f"Input text length: {len(text)} characters")

        samples, sample_rate = self._engine.create(
            text=text,
            voice=voice,
            speed=speed,
            lang=lang,
        )

        logger.debug(f"Generated {len(samples)} samples at {sample_rate}Hz")
        return samples, sample_rate

    def generate_long(
        self,
        text: str,
        voice: str = "af_heart",
        speed: float = 1.0,
    ) -> tuple[np.ndarray, int]:
        """Generate speech audio from long text by splitting into safe chunks.

        This method handles text that may exceed the phoneme limit by splitting
        it into sentence-level chunks and concatenating the audio.

        Args:
            text: Input text to synthesize (any length)
            voice: Voice ID (e.g., 'af_heart')
            speed: Speech speed multiplier (0.5-2.0)

        Returns:
            Tuple of (audio_samples, sample_rate)
        """
        self.load()

        if self._engine is None:
            raise RuntimeError("Engine failed to load")

        # If text is short enough, use regular generate
        if len(text) <= MAX_SAFE_CHARS:
            return self.generate(text, voice, speed)

        logger.debug(f"Text length {len(text)} exceeds safe limit, splitting into chunks")

        # Split text into safe chunks at sentence boundaries
        chunks = self._split_into_safe_chunks(text)
        logger.debug(f"Split into {len(chunks)} chunks for safe generation")

        # Generate audio for each chunk
        audio_parts: list[np.ndarray] = []
        sample_rate = SAMPLE_RATE

        for i, chunk in enumerate(chunks):
            if not chunk.strip():
                continue

            logger.debug(f"Generating chunk {i + 1}/{len(chunks)}: {len(chunk)} chars")

            try:
                samples, sample_rate = self.generate(chunk, voice, speed)
                audio_parts.append(samples)
            except IndexError as e:
                # Phoneme limit exceeded even with safe chunk
                # Try splitting this chunk further
                logger.warning(f"Chunk {i + 1} exceeded phoneme limit, splitting further")
                sub_chunks = self._split_into_safe_chunks(chunk, max_chars=MAX_SAFE_CHARS // 2)
                for sub_chunk in sub_chunks:
                    if sub_chunk.strip():
                        try:
                            samples, sample_rate = self.generate(sub_chunk, voice, speed)
                            audio_parts.append(samples)
                        except IndexError:
                            logger.error(f"Cannot generate: {sub_chunk[:50]}...")
                            raise RuntimeError(
                                f"Text chunk too complex for phoneme limit: {sub_chunk[:50]}..."
                            ) from e

        if not audio_parts:
            raise RuntimeError("No audio generated from text")

        # Concatenate all audio parts
        combined = np.concatenate(audio_parts)
        logger.debug(f"Combined {len(audio_parts)} chunks into {len(combined)} samples")

        return combined, sample_rate

    def _split_into_safe_chunks(self, text: str, max_chars: int = MAX_SAFE_CHARS) -> list[str]:
        """Split text into chunks that are safe for the phoneme limit.

        Attempts to split at sentence boundaries first, then at word boundaries.

        Args:
            text: Text to split
            max_chars: Maximum characters per chunk

        Returns:
            List of text chunks
        """
        import re

        # First try splitting by sentences
        sentences = re.split(r"(?<=[.!?])\s+", text)

        chunks: list[str] = []
        current_chunk = ""

        for sentence in sentences:
            # If single sentence is too long, split by words
            if len(sentence) > max_chars:
                # Flush current chunk
                if current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = ""

                # Split long sentence by words
                words = sentence.split()
                for word in words:
                    if len(current_chunk) + len(word) + 1 > max_chars:
                        if current_chunk:
                            chunks.append(current_chunk.strip())
                        current_chunk = word
                    else:
                        current_chunk = f"{current_chunk} {word}".strip()
            elif len(current_chunk) + len(sentence) + 1 > max_chars:
                # Sentence fits but would exceed limit, start new chunk
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence
            else:
                # Add sentence to current chunk
                current_chunk = f"{current_chunk} {sentence}".strip()

        # Don't forget the last chunk
        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    def save_audio(
        self,
        text: str,
        output_path: Path,
        voice: str = "af_heart",
        speed: float = 1.0,
    ) -> int:
        """Generate and save audio to file.

        Args:
            text: Input text to synthesize
            output_path: Output file path (WAV format)
            voice: Voice ID
            speed: Speech speed multiplier

        Returns:
            Number of characters processed
        """
        samples, sample_rate = self.generate(text, voice, speed)

        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        logger.info(f"Saving audio to: {output_path}")
        sf.write(str(output_path), samples, sample_rate)

        return len(text)

    def play_audio(
        self,
        text: str,
        voice: str = "af_heart",
        speed: float = 1.0,
        silence_ms: int = DEFAULT_SILENCE_MS,
    ) -> int:
        """Generate and play audio through speakers.

        Args:
            text: Input text to synthesize
            voice: Voice ID
            speed: Speech speed multiplier
            silence_ms: Trailing silence in milliseconds (avoids audio cutoff)

        Returns:
            Number of characters processed
        """
        samples, sample_rate = self.generate(text, voice, speed)

        logger.info("Playing audio through speakers...")
        logger.debug(f"Audio duration: {len(samples) / sample_rate:.2f}s")

        # Add trailing silence to avoid abrupt audio cutoff
        if silence_ms > 0:
            silence_samples = int(sample_rate * silence_ms / 1000)
            samples = np.concatenate([samples, np.zeros(silence_samples, dtype=samples.dtype)])
            logger.debug(f"Added {silence_ms}ms trailing silence ({silence_samples} samples)")

        # Play audio
        sd.play(samples, samplerate=sample_rate)
        sd.wait()

        logger.info("Playback complete")
        return len(text)


# Global engine instance (singleton pattern for CLI efficiency)
_engine: KokoroEngine | None = None


def get_engine() -> KokoroEngine:
    """Get the global engine instance.

    Returns:
        KokoroEngine instance (creates if needed)
    """
    global _engine
    if _engine is None:
        _engine = KokoroEngine()
    return _engine


def synthesize_to_file(
    text: str,
    output_path: Path,
    voice: str = "af_heart",
    speed: float = 1.0,
) -> int:
    """Synthesize text to an audio file.

    Args:
        text: Input text
        output_path: Output file path
        voice: Voice ID
        speed: Speech speed

    Returns:
        Number of characters processed
    """
    engine = get_engine()
    return engine.save_audio(text, output_path, voice, speed)


def synthesize_and_play(
    text: str,
    voice: str = "af_heart",
    speed: float = 1.0,
    silence_ms: int = DEFAULT_SILENCE_MS,
) -> int:
    """Synthesize text and play through speakers.

    Args:
        text: Input text
        voice: Voice ID
        speed: Speech speed
        silence_ms: Trailing silence in milliseconds

    Returns:
        Number of characters processed
    """
    engine = get_engine()
    return engine.play_audio(text, voice, speed, silence_ms)


def read_from_stdin() -> str:
    """Read text from stdin.

    Returns:
        Text from stdin, stripped of leading/trailing whitespace
    """
    import sys

    logger.debug("Reading from stdin...")
    text = sys.stdin.read().strip()
    logger.debug(f"Read {len(text)} characters from stdin")
    return text
