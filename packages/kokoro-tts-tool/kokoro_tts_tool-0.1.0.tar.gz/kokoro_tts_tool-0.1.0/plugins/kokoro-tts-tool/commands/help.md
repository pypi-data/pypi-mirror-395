---
description: Show help information for kokoro-tts-tool
argument-hint: command
---

Display help information for kokoro-tts-tool CLI commands.

## Usage

```bash
# Show general help
kokoro-tts-tool --help

# Show command-specific help
kokoro-tts-tool COMMAND --help

# Show version
kokoro-tts-tool --version
```

## Available Commands

| Command | Description |
|---------|-------------|
| `init` | Download and initialize TTS models (~350MB) |
| `synthesize` | Convert text to speech (speakers or file) |
| `infinite` | Stream continuous TTS from long documents |
| `list-voices` | List all 60+ available TTS voices |
| `info` | Display configuration status |
| `completion` | Generate shell completion script |

## Examples

```bash
# General help
kokoro-tts-tool --help

# Synthesize command help
kokoro-tts-tool synthesize --help

# Infinite streaming help
kokoro-tts-tool infinite --help

# List voices help
kokoro-tts-tool list-voices --help

# Version information
kokoro-tts-tool --version
```

## Quick Start

```bash
# 1. Initialize (downloads models)
kokoro-tts-tool init

# 2. Basic synthesis
kokoro-tts-tool synthesize "Hello world"

# 3. Save to file
kokoro-tts-tool synthesize "Hello" --output speech.wav

# 4. Stream a document
kokoro-tts-tool infinite --input book.md
```

## Output

Displays usage information, available commands, and options for the specified command.
