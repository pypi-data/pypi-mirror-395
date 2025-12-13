"""Tests for kokoro_tts_tool.models module.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from pathlib import Path

from kokoro_tts_tool.models import (
    MODEL_FILENAME,
    VOICES_FILENAME,
    get_model_info,
    get_model_path,
    get_models_dir,
    get_voices_path,
)


def test_get_models_dir() -> None:
    """Test that models directory path is correct."""
    models_dir = get_models_dir()
    assert models_dir == Path.home() / ".kokoro-tts" / "models"


def test_get_model_path() -> None:
    """Test that model path is correct."""
    model_path = get_model_path()
    assert model_path.name == MODEL_FILENAME
    assert model_path.parent == get_models_dir()


def test_get_voices_path() -> None:
    """Test that voices path is correct."""
    voices_path = get_voices_path()
    assert voices_path.name == VOICES_FILENAME
    assert voices_path.parent == get_models_dir()


def test_get_model_info_structure() -> None:
    """Test that model info has required fields."""
    info = get_model_info()
    assert "models_dir" in info
    assert "model_exists" in info
    assert "voices_exists" in info
    assert "ready" in info


def test_model_filename_is_correct() -> None:
    """Test that model filename matches expected."""
    assert MODEL_FILENAME == "kokoro-v1.0.onnx"


def test_voices_filename_is_correct() -> None:
    """Test that voices filename matches expected."""
    assert VOICES_FILENAME == "voices-v1.0.bin"
