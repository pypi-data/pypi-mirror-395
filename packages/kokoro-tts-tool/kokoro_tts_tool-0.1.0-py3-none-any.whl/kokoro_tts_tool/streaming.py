"""
Audio streaming with producer-consumer pattern.

Implements continuous audio playback using a thread-safe queue.
The consumer (audio callback) runs in a background thread and pulls
audio chunks from the queue. The producer feeds generated audio
into the queue without blocking playback.

This eliminates audio "pop" artifacts that occur when repeatedly
opening/closing the audio device.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import queue
import threading
import time
from typing import Any

import numpy as np
import sounddevice as sd

from kokoro_tts_tool.logging_config import get_logger

logger = get_logger(__name__)

# Audio constants
SAMPLE_RATE = 24000
CHANNELS = 1
BLOCK_SIZE = SAMPLE_RATE // 2  # 0.5s buffer to prevent stuttering
DEFAULT_SILENCE_BETWEEN_CHUNKS_MS = 400  # Natural pause between paragraphs


class AudioStreamer:
    """Producer-consumer audio streamer for continuous playback.

    Keeps the audio stream open throughout playback to eliminate
    pop/click artifacts between chunks.
    """

    def __init__(
        self,
        sample_rate: int = SAMPLE_RATE,
        channels: int = CHANNELS,
        block_size: int = BLOCK_SIZE,
        max_queue_size: int = 5,
    ) -> None:
        """Initialize the audio streamer.

        Args:
            sample_rate: Audio sample rate in Hz
            channels: Number of audio channels
            block_size: Audio buffer size in samples
            max_queue_size: Maximum chunks to buffer before blocking producer
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self.block_size = block_size
        self.max_queue_size = max_queue_size

        self._queue: queue.Queue[np.ndarray | None] = queue.Queue()
        self._stream: sd.OutputStream | None = None
        self._current_chunk: np.ndarray | None = None
        self._chunk_position: int = 0
        self._running: bool = False
        self._finished: bool = False
        self._lock = threading.Lock()

    def _audio_callback(
        self,
        outdata: np.ndarray,
        frames: int,
        time_info: Any,
        status: sd.CallbackFlags,
    ) -> None:
        """Background thread callback that pulls audio from queue.

        Args:
            outdata: Output buffer to fill
            frames: Number of frames requested
            time_info: Timing info (unused)
            status: Stream status flags
        """
        if status:
            logger.warning(f"Audio stream status: {status}")

        frames_written = 0

        while frames_written < frames:
            # If we have no current chunk or finished it, get next one
            if self._current_chunk is None or self._chunk_position >= len(self._current_chunk):
                try:
                    chunk = self._queue.get_nowait()
                    if chunk is None:
                        # Sentinel received, stream is ending
                        self._finished = True
                        outdata[frames_written:] = 0
                        return
                    self._current_chunk = chunk
                    self._chunk_position = 0
                except queue.Empty:
                    # No data available, play silence
                    outdata[frames_written:] = 0
                    return

            # Copy as much as we can from current chunk
            remaining_in_chunk = len(self._current_chunk) - self._chunk_position
            frames_needed = frames - frames_written
            frames_to_copy = min(remaining_in_chunk, frames_needed)

            outdata[frames_written : frames_written + frames_to_copy] = self._current_chunk[
                self._chunk_position : self._chunk_position + frames_to_copy
            ]

            frames_written += frames_to_copy
            self._chunk_position += frames_to_copy

    def start(self) -> None:
        """Start the audio stream.

        Opens the audio device and begins the callback loop.
        The stream plays silence until audio is added to the queue.
        """
        if self._running:
            logger.warning("Stream already running")
            return

        logger.info("Starting audio stream...")

        self._stream = sd.OutputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            callback=self._audio_callback,
            blocksize=self.block_size,
            dtype="float32",
        )
        self._stream.start()
        self._running = True
        self._finished = False

        logger.debug(f"Audio stream started: {self.sample_rate}Hz, {self.channels}ch")

    def stop(self) -> None:
        """Stop the audio stream.

        Closes the audio device. Any remaining queued audio is discarded.
        """
        if not self._running:
            return

        logger.info("Stopping audio stream...")

        self._running = False
        if self._stream is not None:
            self._stream.stop()
            self._stream.close()
            self._stream = None

        # Clear the queue
        while not self._queue.empty():
            try:
                self._queue.get_nowait()
            except queue.Empty:
                break

        logger.debug("Audio stream stopped")

    def add_audio(self, samples: np.ndarray) -> None:
        """Add audio samples to the playback queue.

        Blocks if queue is full (backpressure to prevent RAM overflow).

        Args:
            samples: Audio samples as numpy array (1D or 2D)
        """
        if not self._running:
            raise RuntimeError("Stream not running. Call start() first.")

        # Ensure correct shape (frames, channels)
        if len(samples.shape) == 1:
            samples = samples.reshape(-1, 1)

        # Ensure float32
        if samples.dtype != np.float32:
            samples = samples.astype(np.float32)

        # Wait if queue is full (backpressure)
        while self._queue.qsize() >= self.max_queue_size:
            logger.debug("Queue full, waiting for consumer...")
            time.sleep(0.1)

        self._queue.put(samples)
        logger.debug(f"Added {len(samples)} samples to queue (qsize={self._queue.qsize()})")

    def add_silence(self, duration_ms: int = DEFAULT_SILENCE_BETWEEN_CHUNKS_MS) -> None:
        """Add silence to the playback queue.

        Useful for adding natural pauses between paragraphs.

        Args:
            duration_ms: Silence duration in milliseconds
        """
        samples = int(self.sample_rate * duration_ms / 1000)
        silence = np.zeros((samples, self.channels), dtype=np.float32)
        self.add_audio(silence)
        logger.debug(f"Added {duration_ms}ms silence")

    def signal_end(self) -> None:
        """Signal that no more audio will be added.

        Adds a sentinel to the queue so the consumer knows to stop.
        """
        self._queue.put(None)
        logger.debug("End signal sent")

    def wait_until_finished(self, timeout: float | None = None) -> bool:
        """Wait for all queued audio to finish playing.

        Args:
            timeout: Maximum time to wait in seconds (None = infinite)

        Returns:
            True if finished, False if timeout
        """
        logger.info("Waiting for audio playback to complete...")

        start_time = time.time()
        while not self._finished:
            if timeout is not None and (time.time() - start_time) > timeout:
                logger.warning("Wait timeout exceeded")
                return False
            time.sleep(0.1)

        # Give a small buffer for final samples to play
        time.sleep(0.2)

        logger.info("Audio playback complete")
        return True

    @property
    def is_running(self) -> bool:
        """Check if the stream is currently running."""
        return self._running

    @property
    def queue_size(self) -> int:
        """Get current number of chunks in queue."""
        return self._queue.qsize()

    def __enter__(self) -> "AudioStreamer":
        """Context manager entry."""
        self.start()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit."""
        self.stop()
