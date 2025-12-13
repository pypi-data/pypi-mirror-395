"""Tests for kokoro_tts_tool.voices module.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import pytest

from kokoro_tts_tool.voices import (
    DEFAULT_VOICE,
    VOICES,
    get_language_code,
    get_voice,
    list_accents,
    list_languages,
    list_voices,
    validate_voice,
)


def test_default_voice_exists() -> None:
    """Test that default voice exists in voice list."""
    assert DEFAULT_VOICE in VOICES


def test_default_voice_is_af_heart() -> None:
    """Test that default voice is af_heart."""
    assert DEFAULT_VOICE == "af_heart"


def test_get_voice_valid() -> None:
    """Test getting a valid voice."""
    voice = get_voice("af_heart")
    assert voice is not None
    assert voice["id"] == "af_heart"
    assert voice["gender"] == "Female"


def test_get_voice_invalid() -> None:
    """Test getting an invalid voice."""
    voice = get_voice("invalid_voice")
    assert voice is None


def test_get_voice_case_insensitive() -> None:
    """Test that voice lookup is case insensitive."""
    voice = get_voice("AF_HEART")
    assert voice is not None
    assert voice["id"] == "af_heart"


def test_validate_voice_valid() -> None:
    """Test validating a valid voice."""
    result = validate_voice("af_heart")
    assert result == "af_heart"


def test_validate_voice_case_insensitive() -> None:
    """Test that validation is case insensitive."""
    result = validate_voice("AF_HEART")
    assert result == "af_heart"


def test_validate_voice_invalid() -> None:
    """Test that invalid voice raises ValueError."""
    with pytest.raises(ValueError, match="Unknown voice"):
        validate_voice("invalid_voice")


def test_get_language_code_american() -> None:
    """Test language code for American English voices."""
    assert get_language_code("af_heart") == "en-us"
    assert get_language_code("am_adam") == "en-us"


def test_get_language_code_british() -> None:
    """Test language code for British English voices."""
    assert get_language_code("bf_emma") == "en-gb"
    assert get_language_code("bm_george") == "en-gb"


def test_get_language_code_japanese() -> None:
    """Test language code for Japanese voices."""
    assert get_language_code("jf_alpha") == "ja"


def test_get_language_code_mandarin() -> None:
    """Test language code for Mandarin voices."""
    assert get_language_code("zf_xiaobei") == "zh"


def test_get_language_code_default() -> None:
    """Test default language code for unknown prefix."""
    assert get_language_code("unknown") == "en-us"
    assert get_language_code("") == "en-us"


def test_list_voices_all() -> None:
    """Test listing all voices."""
    voices = list_voices()
    assert len(voices) > 50  # We have 60+ voices


def test_list_voices_filter_language() -> None:
    """Test filtering voices by language."""
    english_voices = list_voices(language="English")
    assert len(english_voices) > 10
    for voice in english_voices:
        assert voice["language"] == "English"


def test_list_voices_filter_gender() -> None:
    """Test filtering voices by gender."""
    female_voices = list_voices(gender="Female")
    assert len(female_voices) > 10
    for voice in female_voices:
        assert voice["gender"] == "Female"


def test_list_voices_filter_combined() -> None:
    """Test filtering voices by multiple criteria."""
    voices = list_voices(language="English", gender="Male")
    assert len(voices) > 5
    for voice in voices:
        assert voice["language"] == "English"
        assert voice["gender"] == "Male"


def test_list_languages() -> None:
    """Test listing available languages."""
    languages = list_languages()
    assert "English" in languages
    assert "Japanese" in languages
    assert "Mandarin" in languages
    assert len(languages) >= 6


def test_list_accents() -> None:
    """Test listing available accents."""
    accents = list_accents()
    assert "American" in accents
    assert "British" in accents
    assert "Japanese" in accents
    assert len(accents) >= 6


def test_voice_info_structure() -> None:
    """Test that voice info has all required fields."""
    voice = get_voice("af_heart")
    assert voice is not None
    assert "id" in voice
    assert "name" in voice
    assert "gender" in voice
    assert "language" in voice
    assert "accent" in voice
    assert "grade" in voice
    assert "description" in voice
