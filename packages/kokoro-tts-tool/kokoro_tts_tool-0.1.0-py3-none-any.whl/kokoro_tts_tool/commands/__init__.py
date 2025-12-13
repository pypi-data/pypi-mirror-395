"""
CLI command implementations for Kokoro TTS tool.

This package contains all Click command definitions that wrap the core
library functions with CLI-specific concerns like argument parsing, error
formatting, and user output.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from kokoro_tts_tool.commands.infinite_commands import infinite
from kokoro_tts_tool.commands.info_commands import info_command
from kokoro_tts_tool.commands.init_commands import init_command
from kokoro_tts_tool.commands.synthesize_commands import synthesize
from kokoro_tts_tool.commands.voice_commands import list_voices_command

__all__ = [
    "synthesize",
    "infinite",
    "list_voices_command",
    "info_command",
    "init_command",
]
