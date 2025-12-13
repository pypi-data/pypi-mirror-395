"""
Model management for Kokoro TTS.

Handles model downloading, caching, and path management for the ONNX models.
Models are stored in ~/.kokoro-tts/models/ and auto-downloaded on first use.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import urllib.request
from pathlib import Path

from kokoro_tts_tool.logging_config import get_logger

logger = get_logger(__name__)

# Model download URLs
MODEL_URL = (
    "https://github.com/thewh1teagle/kokoro-onnx/releases/download/"
    "model-files-v1.0/kokoro-v1.0.onnx"
)
VOICES_URL = (
    "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin"
)

# Model file names
MODEL_FILENAME = "kokoro-v1.0.onnx"
VOICES_FILENAME = "voices-v1.0.bin"

# Model sizes for progress display
MODEL_SIZE_MB = 300
VOICES_SIZE_MB = 50


def get_models_dir() -> Path:
    """Get the models directory path.

    Returns:
        Path to ~/.kokoro-tts/models/
    """
    models_dir = Path.home() / ".kokoro-tts" / "models"
    models_dir.mkdir(parents=True, exist_ok=True)
    return models_dir


def get_model_path() -> Path:
    """Get the path to the ONNX model file.

    Returns:
        Path to the kokoro-v1.0.onnx file
    """
    return get_models_dir() / MODEL_FILENAME


def get_voices_path() -> Path:
    """Get the path to the voices binary file.

    Returns:
        Path to the voices-v1.0.bin file
    """
    return get_models_dir() / VOICES_FILENAME


def models_exist() -> bool:
    """Check if both model files exist.

    Returns:
        True if both model and voices files exist
    """
    return get_model_path().exists() and get_voices_path().exists()


def _download_with_progress(url: str, dest: Path, description: str) -> None:
    """Download a file with progress reporting.

    Args:
        url: URL to download from
        dest: Destination path
        description: Description for progress display
    """
    logger.info(f"Downloading {description}...")
    logger.debug(f"URL: {url}")
    logger.debug(f"Destination: {dest}")

    # Create a request with headers
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "kokoro-tts-tool/0.1.0"},
    )

    # Download the file (only from known GitHub URLs)
    with urllib.request.urlopen(request) as response:  # nosec B310
        total_size = int(response.headers.get("Content-Length", 0))
        downloaded = 0
        chunk_size = 8192

        with open(dest, "wb") as f:
            while True:
                chunk = response.read(chunk_size)
                if not chunk:
                    break
                f.write(chunk)
                downloaded += len(chunk)

                if total_size > 0:
                    percent = (downloaded / total_size) * 100
                    mb_downloaded = downloaded / (1024 * 1024)
                    mb_total = total_size / (1024 * 1024)
                    logger.debug(
                        f"Progress: {mb_downloaded:.1f}/{mb_total:.1f} MB ({percent:.1f}%)"
                    )

    logger.info(f"Downloaded {description} successfully")


def download_models(force: bool = False) -> tuple[Path, Path]:
    """Download model files if they don't exist.

    Args:
        force: If True, re-download even if files exist

    Returns:
        Tuple of (model_path, voices_path)

    Raises:
        RuntimeError: If download fails
    """
    model_path = get_model_path()
    voices_path = get_voices_path()

    try:
        # Download model if needed
        if force or not model_path.exists():
            _download_with_progress(MODEL_URL, model_path, "ONNX model (~300MB)")
        else:
            logger.debug(f"Model already exists: {model_path}")

        # Download voices if needed
        if force or not voices_path.exists():
            _download_with_progress(VOICES_URL, voices_path, "voices file (~50MB)")
        else:
            logger.debug(f"Voices file already exists: {voices_path}")

        return model_path, voices_path

    except Exception as e:
        # Clean up partial downloads
        if model_path.exists() and model_path.stat().st_size == 0:
            model_path.unlink()
        if voices_path.exists() and voices_path.stat().st_size == 0:
            voices_path.unlink()

        raise RuntimeError(
            f"Failed to download models: {e}\n\n"
            "What to do:\n"
            "  1. Check your internet connection\n"
            "  2. Try again with: kokoro-tts-tool init --force\n"
            "  3. Manually download from:\n"
            f"     {MODEL_URL}\n"
            f"     {VOICES_URL}\n"
            f"  4. Place files in: {get_models_dir()}"
        ) from e


def get_model_paths() -> tuple[Path, Path]:
    """Get model paths, downloading if necessary.

    Returns:
        Tuple of (model_path, voices_path)

    Raises:
        RuntimeError: If models cannot be obtained
    """
    if not models_exist():
        logger.info("Models not found, downloading...")
        return download_models()

    return get_model_path(), get_voices_path()


def get_model_info() -> dict[str, str | bool | int]:
    """Get information about installed models.

    Returns:
        Dictionary with model status and paths
    """
    model_path = get_model_path()
    voices_path = get_voices_path()

    info: dict[str, str | bool | int] = {
        "models_dir": str(get_models_dir()),
        "model_exists": model_path.exists(),
        "voices_exists": voices_path.exists(),
        "ready": models_exist(),
    }

    if model_path.exists():
        info["model_size_mb"] = int(model_path.stat().st_size / (1024 * 1024))
        info["model_path"] = str(model_path)

    if voices_path.exists():
        info["voices_size_mb"] = int(voices_path.stat().st_size / (1024 * 1024))
        info["voices_path"] = str(voices_path)

    return info
