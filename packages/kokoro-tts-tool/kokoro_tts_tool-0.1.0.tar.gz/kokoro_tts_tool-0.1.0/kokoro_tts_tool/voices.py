"""
Voice definitions and management for Kokoro TTS.

Contains voice metadata, validation, and listing functionality for all
60+ Kokoro voices across multiple languages.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from typing import TypedDict

from kokoro_tts_tool.logging_config import get_logger

logger = get_logger(__name__)


class VoiceInfo(TypedDict):
    """Voice information structure."""

    id: str
    name: str
    gender: str
    language: str
    accent: str
    grade: str
    description: str


# Default voice
DEFAULT_VOICE = "af_heart"

# Voice naming convention:
# First letter: language (a=American, b=British, j=Japanese, z=Mandarin, etc.)
# Second letter: gender (f=Female, m=Male)
# Rest: voice name

VOICES: dict[str, VoiceInfo] = {
    # American English Female
    "af_heart": {
        "id": "af_heart",
        "name": "Heart",
        "gender": "Female",
        "language": "English",
        "accent": "American",
        "grade": "A",
        "description": "Default voice, emotional, soft (highest quality)",
    },
    "af_bella": {
        "id": "af_bella",
        "name": "Bella",
        "gender": "Female",
        "language": "English",
        "accent": "American",
        "grade": "A-",
        "description": "Expressive, dynamic range",
    },
    "af_sarah": {
        "id": "af_sarah",
        "name": "Sarah",
        "gender": "Female",
        "language": "English",
        "accent": "American",
        "grade": "B+",
        "description": "Natural, neutral tone",
    },
    "af_nicole": {
        "id": "af_nicole",
        "name": "Nicole",
        "gender": "Female",
        "language": "English",
        "accent": "American",
        "grade": "B-",
        "description": "Tech-savvy, modern",
    },
    "af_sky": {
        "id": "af_sky",
        "name": "Sky",
        "gender": "Female",
        "language": "English",
        "accent": "American",
        "grade": "B",
        "description": "High pitch, young, energetic",
    },
    "af_jessica": {
        "id": "af_jessica",
        "name": "Jessica",
        "gender": "Female",
        "language": "English",
        "accent": "American",
        "grade": "B",
        "description": "Warm, friendly",
    },
    "af_kailey": {
        "id": "af_kailey",
        "name": "Kailey",
        "gender": "Female",
        "language": "English",
        "accent": "American",
        "grade": "B-",
        "description": "Casual, relatable",
    },
    "af_nova": {
        "id": "af_nova",
        "name": "Nova",
        "gender": "Female",
        "language": "English",
        "accent": "American",
        "grade": "B",
        "description": "Crisp, clear",
    },
    "af_river": {
        "id": "af_river",
        "name": "River",
        "gender": "Female",
        "language": "English",
        "accent": "American",
        "grade": "B-",
        "description": "Calm, flowing",
    },
    "af_alloy": {
        "id": "af_alloy",
        "name": "Alloy",
        "gender": "Female",
        "language": "English",
        "accent": "American",
        "grade": "B",
        "description": "Versatile, balanced",
    },
    "af_aoede": {
        "id": "af_aoede",
        "name": "Aoede",
        "gender": "Female",
        "language": "English",
        "accent": "American",
        "grade": "B-",
        "description": "Musical, poetic",
    },
    # American English Male
    "am_adam": {
        "id": "am_adam",
        "name": "Adam",
        "gender": "Male",
        "language": "English",
        "accent": "American",
        "grade": "A-",
        "description": "Deep, narrator voice (audiobooks)",
    },
    "am_michael": {
        "id": "am_michael",
        "name": "Michael",
        "gender": "Male",
        "language": "English",
        "accent": "American",
        "grade": "B+",
        "description": "Natural, casual (student)",
    },
    "am_echo": {
        "id": "am_echo",
        "name": "Echo",
        "gender": "Male",
        "language": "English",
        "accent": "American",
        "grade": "B",
        "description": "Resonant, clear",
    },
    "am_eric": {
        "id": "am_eric",
        "name": "Eric",
        "gender": "Male",
        "language": "English",
        "accent": "American",
        "grade": "B",
        "description": "Professional, warm",
    },
    "am_fenrir": {
        "id": "am_fenrir",
        "name": "Fenrir",
        "gender": "Male",
        "language": "English",
        "accent": "American",
        "grade": "B-",
        "description": "Strong, commanding",
    },
    "am_liam": {
        "id": "am_liam",
        "name": "Liam",
        "gender": "Male",
        "language": "English",
        "accent": "American",
        "grade": "B",
        "description": "Friendly, approachable",
    },
    "am_onyx": {
        "id": "am_onyx",
        "name": "Onyx",
        "gender": "Male",
        "language": "English",
        "accent": "American",
        "grade": "B-",
        "description": "Deep, smooth",
    },
    "am_puck": {
        "id": "am_puck",
        "name": "Puck",
        "gender": "Male",
        "language": "English",
        "accent": "American",
        "grade": "B-",
        "description": "Playful, mischievous",
    },
    "am_santa": {
        "id": "am_santa",
        "name": "Santa",
        "gender": "Male",
        "language": "English",
        "accent": "American",
        "grade": "B",
        "description": "Jolly, warm",
    },
    # British English Female
    "bf_emma": {
        "id": "bf_emma",
        "name": "Emma",
        "gender": "Female",
        "language": "English",
        "accent": "British",
        "grade": "B+",
        "description": "Polished, formal (education)",
    },
    "bf_isabella": {
        "id": "bf_isabella",
        "name": "Isabella",
        "gender": "Female",
        "language": "English",
        "accent": "British",
        "grade": "B",
        "description": "Soft, elegant (poetry)",
    },
    "bf_alice": {
        "id": "bf_alice",
        "name": "Alice",
        "gender": "Female",
        "language": "English",
        "accent": "British",
        "grade": "B-",
        "description": "Clear, articulate",
    },
    "bf_lily": {
        "id": "bf_lily",
        "name": "Lily",
        "gender": "Female",
        "language": "English",
        "accent": "British",
        "grade": "B-",
        "description": "Sweet, gentle",
    },
    # British English Male
    "bm_george": {
        "id": "bm_george",
        "name": "George",
        "gender": "Male",
        "language": "English",
        "accent": "British",
        "grade": "B+",
        "description": "Resonant, classic (history)",
    },
    "bm_lewis": {
        "id": "bm_lewis",
        "name": "Lewis",
        "gender": "Male",
        "language": "English",
        "accent": "British",
        "grade": "B",
        "description": "Young, bright (modern)",
    },
    "bm_daniel": {
        "id": "bm_daniel",
        "name": "Daniel",
        "gender": "Male",
        "language": "English",
        "accent": "British",
        "grade": "B-",
        "description": "Warm, trustworthy",
    },
    "bm_fable": {
        "id": "bm_fable",
        "name": "Fable",
        "gender": "Male",
        "language": "English",
        "accent": "British",
        "grade": "B",
        "description": "Storyteller, expressive",
    },
    # Japanese Female
    "jf_alpha": {
        "id": "jf_alpha",
        "name": "Alpha",
        "gender": "Female",
        "language": "Japanese",
        "accent": "Japanese",
        "grade": "B",
        "description": "Clear, standard Japanese",
    },
    "jf_gongitsune": {
        "id": "jf_gongitsune",
        "name": "Gongitsune",
        "gender": "Female",
        "language": "Japanese",
        "accent": "Japanese",
        "grade": "B-",
        "description": "Soft, storytelling",
    },
    "jf_nezumi": {
        "id": "jf_nezumi",
        "name": "Nezumi",
        "gender": "Female",
        "language": "Japanese",
        "accent": "Japanese",
        "grade": "B-",
        "description": "Cute, energetic",
    },
    "jf_tebukuro": {
        "id": "jf_tebukuro",
        "name": "Tebukuro",
        "gender": "Female",
        "language": "Japanese",
        "accent": "Japanese",
        "grade": "B",
        "description": "Gentle, warm",
    },
    # Japanese Male
    "jm_kumo": {
        "id": "jm_kumo",
        "name": "Kumo",
        "gender": "Male",
        "language": "Japanese",
        "accent": "Japanese",
        "grade": "B",
        "description": "Deep, calm",
    },
    # Mandarin Chinese Female
    "zf_xiaobei": {
        "id": "zf_xiaobei",
        "name": "Xiaobei",
        "gender": "Female",
        "language": "Mandarin",
        "accent": "Chinese",
        "grade": "B",
        "description": "Standard Mandarin",
    },
    "zf_xiaoni": {
        "id": "zf_xiaoni",
        "name": "Xiaoni",
        "gender": "Female",
        "language": "Mandarin",
        "accent": "Chinese",
        "grade": "B-",
        "description": "Soft, gentle",
    },
    "zf_xiaoxiao": {
        "id": "zf_xiaoxiao",
        "name": "Xiaoxiao",
        "gender": "Female",
        "language": "Mandarin",
        "accent": "Chinese",
        "grade": "B",
        "description": "Young, energetic",
    },
    "zf_xiaoyi": {
        "id": "zf_xiaoyi",
        "name": "Xiaoyi",
        "gender": "Female",
        "language": "Mandarin",
        "accent": "Chinese",
        "grade": "B-",
        "description": "Clear, professional",
    },
    # Mandarin Chinese Male
    "zm_yunjian": {
        "id": "zm_yunjian",
        "name": "Yunjian",
        "gender": "Male",
        "language": "Mandarin",
        "accent": "Chinese",
        "grade": "B",
        "description": "News anchor style",
    },
    "zm_yunxi": {
        "id": "zm_yunxi",
        "name": "Yunxi",
        "gender": "Male",
        "language": "Mandarin",
        "accent": "Chinese",
        "grade": "B-",
        "description": "Casual, friendly",
    },
    "zm_yunxia": {
        "id": "zm_yunxia",
        "name": "Yunxia",
        "gender": "Male",
        "language": "Mandarin",
        "accent": "Chinese",
        "grade": "B",
        "description": "Warm, narrative",
    },
    "zm_yunyang": {
        "id": "zm_yunyang",
        "name": "Yunyang",
        "gender": "Male",
        "language": "Mandarin",
        "accent": "Chinese",
        "grade": "B-",
        "description": "Standard, clear",
    },
    # Spanish
    "ef_dora": {
        "id": "ef_dora",
        "name": "Dora",
        "gender": "Female",
        "language": "Spanish",
        "accent": "Spanish",
        "grade": "B",
        "description": "Warm, expressive",
    },
    "em_alex": {
        "id": "em_alex",
        "name": "Alex",
        "gender": "Male",
        "language": "Spanish",
        "accent": "Spanish",
        "grade": "B",
        "description": "Clear, modern",
    },
    "em_santa": {
        "id": "em_santa",
        "name": "Santa",
        "gender": "Male",
        "language": "Spanish",
        "accent": "Spanish",
        "grade": "B-",
        "description": "Festive, jolly",
    },
    # French
    "ff_siwis": {
        "id": "ff_siwis",
        "name": "Siwis",
        "gender": "Female",
        "language": "French",
        "accent": "French",
        "grade": "B",
        "description": "Elegant, Parisian",
    },
    # Hindi
    "hf_alpha": {
        "id": "hf_alpha",
        "name": "Alpha",
        "gender": "Female",
        "language": "Hindi",
        "accent": "Hindi",
        "grade": "B",
        "description": "Standard Hindi",
    },
    "hf_beta": {
        "id": "hf_beta",
        "name": "Beta",
        "gender": "Female",
        "language": "Hindi",
        "accent": "Hindi",
        "grade": "B-",
        "description": "Soft, expressive",
    },
    "hm_omega": {
        "id": "hm_omega",
        "name": "Omega",
        "gender": "Male",
        "language": "Hindi",
        "accent": "Hindi",
        "grade": "B",
        "description": "Deep, authoritative",
    },
    "hm_psi": {
        "id": "hm_psi",
        "name": "Psi",
        "gender": "Male",
        "language": "Hindi",
        "accent": "Hindi",
        "grade": "B-",
        "description": "Casual, friendly",
    },
    # Italian
    "if_sara": {
        "id": "if_sara",
        "name": "Sara",
        "gender": "Female",
        "language": "Italian",
        "accent": "Italian",
        "grade": "B",
        "description": "Melodic, expressive",
    },
    "im_nicola": {
        "id": "im_nicola",
        "name": "Nicola",
        "gender": "Male",
        "language": "Italian",
        "accent": "Italian",
        "grade": "B",
        "description": "Warm, passionate",
    },
    # Brazilian Portuguese
    "pf_dora": {
        "id": "pf_dora",
        "name": "Dora",
        "gender": "Female",
        "language": "Portuguese",
        "accent": "Brazilian",
        "grade": "B",
        "description": "Warm, Brazilian",
    },
    "pm_alex": {
        "id": "pm_alex",
        "name": "Alex",
        "gender": "Male",
        "language": "Portuguese",
        "accent": "Brazilian",
        "grade": "B",
        "description": "Clear, modern",
    },
    "pm_santa": {
        "id": "pm_santa",
        "name": "Santa",
        "gender": "Male",
        "language": "Portuguese",
        "accent": "Brazilian",
        "grade": "B-",
        "description": "Festive, jolly",
    },
}

# Language codes mapping
LANGUAGE_CODES: dict[str, str] = {
    "a": "en-us",  # American English
    "b": "en-gb",  # British English
    "j": "ja",  # Japanese
    "z": "zh",  # Mandarin Chinese
    "e": "es",  # Spanish
    "f": "fr-fr",  # French
    "h": "hi",  # Hindi
    "i": "it",  # Italian
    "p": "pt-br",  # Brazilian Portuguese
}


def get_voice(voice_id: str) -> VoiceInfo | None:
    """Get voice information by ID.

    Args:
        voice_id: Voice identifier (e.g., 'af_heart')

    Returns:
        VoiceInfo if found, None otherwise
    """
    return VOICES.get(voice_id.lower())


def validate_voice(voice_id: str) -> str:
    """Validate a voice ID.

    Args:
        voice_id: Voice identifier to validate

    Returns:
        Validated voice ID (lowercase)

    Raises:
        ValueError: If voice is invalid
    """
    voice_lower = voice_id.lower()
    if voice_lower not in VOICES:
        available = ", ".join(sorted(VOICES.keys())[:10])
        raise ValueError(
            f"Unknown voice: {voice_id}\n\n"
            f"Available voices include: {available}...\n\n"
            "Use 'kokoro-tts-tool list-voices' to see all options."
        )
    return voice_lower


def get_language_code(voice_id: str) -> str:
    """Get the language code for a voice.

    Args:
        voice_id: Voice identifier

    Returns:
        Language code (e.g., 'en-us')
    """
    if voice_id and len(voice_id) >= 1:
        lang_prefix = voice_id[0].lower()
        return LANGUAGE_CODES.get(lang_prefix, "en-us")
    return "en-us"


def list_voices(
    language: str | None = None,
    gender: str | None = None,
) -> list[VoiceInfo]:
    """List voices with optional filtering.

    Args:
        language: Filter by language (e.g., 'English', 'Japanese')
        gender: Filter by gender ('Male' or 'Female')

    Returns:
        List of matching VoiceInfo entries
    """
    voices = list(VOICES.values())

    if language:
        lang_lower = language.lower()
        voices = [v for v in voices if v["language"].lower() == lang_lower]

    if gender:
        gender_lower = gender.lower()
        voices = [v for v in voices if v["gender"].lower() == gender_lower]

    # Sort by grade (A first) then by ID
    return sorted(voices, key=lambda v: (v["grade"], v["id"]))


def list_languages() -> list[str]:
    """Get list of unique languages.

    Returns:
        Sorted list of available languages
    """
    return sorted({v["language"] for v in VOICES.values()})


def list_accents() -> list[str]:
    """Get list of unique accents.

    Returns:
        Sorted list of available accents
    """
    return sorted({v["accent"] for v in VOICES.values()})
