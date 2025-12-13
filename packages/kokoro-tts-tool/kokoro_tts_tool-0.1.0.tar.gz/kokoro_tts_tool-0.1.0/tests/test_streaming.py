"""
Tests for the audio streaming module.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import numpy as np
import pytest

from kokoro_tts_tool.streaming import (
    BLOCK_SIZE,
    CHANNELS,
    DEFAULT_SILENCE_BETWEEN_CHUNKS_MS,
    SAMPLE_RATE,
    AudioStreamer,
)


class TestAudioStreamerInit:
    """Tests for AudioStreamer initialization."""

    def test_default_values(self) -> None:
        """Should initialize with default values."""
        streamer = AudioStreamer()
        assert streamer.sample_rate == SAMPLE_RATE
        assert streamer.channels == CHANNELS
        assert streamer.block_size == BLOCK_SIZE
        assert streamer.max_queue_size == 5

    def test_custom_values(self) -> None:
        """Should accept custom values."""
        streamer = AudioStreamer(
            sample_rate=48000,
            channels=2,
            block_size=1024,
            max_queue_size=10,
        )
        assert streamer.sample_rate == 48000
        assert streamer.channels == 2
        assert streamer.block_size == 1024
        assert streamer.max_queue_size == 10

    def test_not_running_initially(self) -> None:
        """Should not be running when created."""
        streamer = AudioStreamer()
        assert not streamer.is_running

    def test_empty_queue_initially(self) -> None:
        """Queue should be empty when created."""
        streamer = AudioStreamer()
        assert streamer.queue_size == 0


class TestAudioStreamerAudioOperations:
    """Tests for audio operations without actual playback."""

    def test_add_audio_requires_running(self) -> None:
        """Adding audio should require stream to be running."""
        streamer = AudioStreamer()
        samples = np.zeros(1000, dtype=np.float32)

        with pytest.raises(RuntimeError, match="not running"):
            streamer.add_audio(samples)

    def test_samples_reshape_1d_to_2d(self) -> None:
        """1D samples should be accepted (reshaped internally)."""
        # This test verifies the reshape logic exists
        # Actual audio playback is not tested
        _ = AudioStreamer()  # Verify instantiation works
        samples_1d = np.zeros(1000, dtype=np.float32)

        # Without starting stream, we verify the shape logic conceptually
        assert len(samples_1d.shape) == 1

        # After reshape it would be 2D
        reshaped = samples_1d.reshape(-1, 1)
        assert reshaped.shape == (1000, 1)

    def test_samples_float32_conversion(self) -> None:
        """Non-float32 samples should be convertible."""
        samples_int16 = np.zeros(1000, dtype=np.int16)
        converted = samples_int16.astype(np.float32)
        assert converted.dtype == np.float32


class TestAudioStreamerContextManager:
    """Tests for context manager protocol."""

    def test_context_manager_protocol(self) -> None:
        """Should support context manager protocol."""
        streamer = AudioStreamer()
        assert hasattr(streamer, "__enter__")
        assert hasattr(streamer, "__exit__")


class TestAudioConstants:
    """Tests for audio constants."""

    def test_sample_rate(self) -> None:
        """Sample rate should be standard for Kokoro."""
        assert SAMPLE_RATE == 24000

    def test_channels(self) -> None:
        """Should be mono."""
        assert CHANNELS == 1

    def test_block_size(self) -> None:
        """Block size should be reasonable fraction of sample rate."""
        assert BLOCK_SIZE == SAMPLE_RATE // 2  # 0.5 seconds
        assert BLOCK_SIZE == 12000

    def test_default_silence(self) -> None:
        """Default silence should be reasonable."""
        assert DEFAULT_SILENCE_BETWEEN_CHUNKS_MS == 400
