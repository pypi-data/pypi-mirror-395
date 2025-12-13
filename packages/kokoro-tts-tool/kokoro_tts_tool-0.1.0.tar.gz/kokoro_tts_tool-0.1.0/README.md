<p align="center">
  <img src=".github/assets/logo.png" alt="kokoro-tts-tool logo" width="128">
</p>

# kokoro-tts-tool

[![Python Version](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Type checked: mypy](https://img.shields.io/badge/type%20checked-mypy-blue.svg)](https://github.com/python/mypy)
[![AI Generated](https://img.shields.io/badge/AI-Generated-blueviolet.svg)](https://www.anthropic.com/claude)
[![Built with Claude Code](https://img.shields.io/badge/Built_with-Claude_Code-5A67D8.svg)](https://www.anthropic.com/claude/code)

A CLI that provides local text-to-speech using Kokoro TTS on Apple Silicon. No API keys required.

## Table of Contents

- [About](#about)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Infinite Streaming](#infinite-streaming)
- [Available Voices](#available-voices)
- [Multi-Level Verbosity Logging](#multi-level-verbosity-logging)
- [Shell Completion](#shell-completion)
- [Development](#development)
- [Testing](#testing)
- [Security](#security)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

## About

`kokoro-tts-tool` is a Python CLI tool for local text-to-speech synthesis using the Kokoro-82M model. It runs entirely on your machine with no cloud dependencies, optimized for Apple Silicon Macs.

**Key highlights:**
- **Local inference**: Uses ONNX runtime for fast, CPU-optimized synthesis
- **60+ voices**: Multiple languages and accents (English, Japanese, Mandarin, etc.)
- **Near real-time**: Fast enough for interactive use on Apple Silicon
- **Infinite streaming**: Continuous TTS for long documents without audio artifacts
- **No API keys**: Everything runs locally, completely free

## Features

- Local TTS with Kokoro-82M (82 million parameters)
- 60+ voices across 8 languages
- Near real-time synthesis on Apple Silicon
- Auto-download of model files (~350MB)
- WAV output or direct speaker playback
- Infinite streaming for long documents (books, articles)
- Seamless audio without pop artifacts between chunks
- Fast offline rendering (20-50x real-time on M4)
- Type-safe with mypy strict mode
- Tested with pytest
- Multi-level verbosity logging (-v/-vv/-vvv)
- Shell completion for bash, zsh, and fish
- Security scanning with bandit, pip-audit, and gitleaks

## Installation

### Prerequisites

- Python 3.14 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- Apple Silicon Mac (recommended) or any platform with Python 3.14+

### Install from source

```bash
# Clone the repository
git clone https://github.com/dnvriend/kokoro-tts-tool.git
cd kokoro-tts-tool

# Install globally with uv
uv tool install .
```

### Install with mise (recommended for development)

```bash
cd kokoro-tts-tool
mise trust
mise install
uv sync
uv tool install .
```

### Verify installation

```bash
kokoro-tts-tool --version
```

## Quick Start

```bash
# 1. Initialize (downloads models on first run, ~350MB)
kokoro-tts-tool init

# 2. Synthesize text to speakers
kokoro-tts-tool synthesize "Hello world!"

# 3. Save to file
kokoro-tts-tool synthesize "Hello world!" --output hello.wav

# 4. Use different voice
kokoro-tts-tool synthesize "This is Adam." --voice am_adam

# 5. List available voices
kokoro-tts-tool list-voices
```

## Usage

### Commands

```bash
# Show all commands
kokoro-tts-tool --help

# Download/update models
kokoro-tts-tool init

# Synthesize text
kokoro-tts-tool synthesize "Your text here"
kokoro-tts-tool synthesize "Your text" --output speech.wav
kokoro-tts-tool synthesize "Your text" --voice bf_emma --speed 1.2

# Read from stdin
echo "Hello from stdin" | kokoro-tts-tool synthesize --stdin

# List voices
kokoro-tts-tool list-voices
kokoro-tts-tool list-voices --language English
kokoro-tts-tool list-voices --gender Female
kokoro-tts-tool list-voices --json

# Show configuration
kokoro-tts-tool info
```

### Synthesize Options

| Option | Description | Default |
|--------|-------------|---------|
| `--voice`, `-v` | Voice ID (e.g., af_heart, am_adam) | af_heart |
| `--output`, `-o` | Output WAV file path | (plays to speakers) |
| `--speed` | Speech speed (0.5 to 2.0) | 1.0 |
| `--stdin`, `-s` | Read text from stdin | false |

## Infinite Streaming

Stream long documents (books, articles, study materials) without audio artifacts:

```bash
# Stream a markdown file to speakers
kokoro-tts-tool infinite --input book.md

# Render to WAV file (fast offline mode, 20-50x real-time on M4)
kokoro-tts-tool infinite --input book.md --output audiobook.wav

# Pipe from stdin
cat chapter.md | kokoro-tts-tool infinite --stdin

# With custom voice and speed
kokoro-tts-tool infinite --input notes.md --voice am_adam --speed 1.2
```

### Infinite Streaming Options

| Option | Description | Default |
|--------|-------------|---------|
| `--input`, `-i` | Input text/markdown file | - |
| `--stdin`, `-s` | Read text from stdin | false |
| `--output`, `-o` | Save to WAV file (fast offline mode) | (plays to speakers) |
| `--voice` | Voice ID | af_heart |
| `--speed` | Speech speed (0.5 to 2.0) | 1.0 |
| `--chunk-size` | Target words per chunk (50-1000) | 200 |
| `--pause` | Pause between chunks in ms (0-2000) | 150 |
| `--no-markdown` | Treat input as plain text | false |

## Available Voices

The tool includes 60+ voices across 8 languages:

### American English (20 voices)
| Voice ID | Gender | Grade | Description |
|----------|--------|-------|-------------|
| `af_heart` | Female | A | Default, emotional, soft (highest quality) |
| `af_bella` | Female | A- | Expressive, dynamic range |
| `am_adam` | Male | A- | Deep narrator (audiobooks) |
| `am_michael` | Male | B+ | Natural, casual |

### British English (8 voices)
| Voice ID | Gender | Grade | Description |
|----------|--------|-------|-------------|
| `bf_emma` | Female | B+ | Polished, formal (education) |
| `bm_george` | Male | B+ | Resonant, classic (history) |

### Other Languages
- **Japanese**: jf_alpha, jm_kumo, and more
- **Mandarin**: zf_xiaobei, zm_yunjian, and more
- **Spanish**: ef_dora, em_alex
- **French**: ff_siwis
- **Hindi**: hf_alpha, hm_omega
- **Italian**: if_sara, im_nicola
- **Portuguese (Brazilian)**: pf_dora, pm_alex

Run `kokoro-tts-tool list-voices` for the complete list.

### Voice Quality Grades
- **A/A-**: Highest quality, recommended for production
- **B+/B**: Good quality
- **B-**: Acceptable quality

## Multi-Level Verbosity Logging

The CLI supports progressive verbosity levels for debugging:

| Flag | Level | Output | Use Case |
|------|-------|--------|----------|
| (none) | WARNING | Errors and warnings only | Production |
| `-v` | INFO | + High-level operations | Normal debugging |
| `-vv` | DEBUG | + Detailed info | Development |
| `-vvv` | TRACE | + Library internals | Deep debugging |

```bash
# Quiet mode
kokoro-tts-tool synthesize "Hello"

# With debug output
kokoro-tts-tool -vv synthesize "Hello"
```

## Shell Completion

The CLI provides native shell completion for bash, zsh, and fish:

```bash
# Bash - add to ~/.bashrc
echo 'eval "$(kokoro-tts-tool completion bash)"' >> ~/.bashrc

# Zsh - add to ~/.zshrc
echo 'eval "$(kokoro-tts-tool completion zsh)"' >> ~/.zshrc

# Fish - save to completions
mkdir -p ~/.config/fish/completions
kokoro-tts-tool completion fish > ~/.config/fish/completions/kokoro-tts-tool.fish
```

## Development

### Setup Development Environment

```bash
git clone https://github.com/dnvriend/kokoro-tts-tool.git
cd kokoro-tts-tool
make install
make help
```

### Available Make Commands

```bash
make install         # Install dependencies
make format          # Format code
make lint            # Run linting
make typecheck       # Type checking
make test            # Run tests
make security        # Security scans
make check           # All checks
make pipeline        # Full pipeline
```

### Project Structure

```
kokoro-tts-tool/
├── kokoro_tts_tool/
│   ├── __init__.py
│   ├── cli.py              # CLI entry point
│   ├── engine.py           # TTS engine wrapper
│   ├── models.py           # Model management
│   ├── voices.py           # Voice definitions
│   ├── splitter.py         # Text chunking for long documents
│   ├── streaming.py        # Audio streaming for speaker playback
│   ├── utils.py            # Utilities
│   ├── logging_config.py   # Logging setup
│   ├── completion.py       # Shell completion
│   └── commands/           # CLI commands
│       ├── synthesize_commands.py
│       ├── voice_commands.py
│       ├── init_commands.py
│       ├── info_commands.py
│       └── infinite_commands.py
├── tests/
├── references/             # Research documentation
├── plugins/                # Claude Code plugin
├── pyproject.toml
├── Makefile
├── README.md
└── CLAUDE.md
```

## Testing

```bash
# Run all tests
make test

# Run tests with verbose output
uv run pytest tests/ -v
```

## Security

The project includes security scanning:

```bash
# Run all security checks
make security

# Individual scans
make security-bandit       # Python security linting
make security-pip-audit    # Dependency CVE scanning
make security-gitleaks     # Secret detection
```

### Prerequisites

```bash
# Install gitleaks (macOS)
brew install gitleaks
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run `make pipeline`
5. Submit a Pull Request

## License

MIT License - see [LICENSE](LICENSE) for details.

## Author

**Dennis Vriend** - [@dnvriend](https://github.com/dnvriend)

## Acknowledgments

- [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) - The TTS model
- [kokoro-onnx](https://github.com/thewh1teagle/kokoro-onnx) - ONNX implementation
- [Click](https://click.palletsprojects.com/) - CLI framework
- [uv](https://github.com/astral-sh/uv) - Fast Python tooling

---

**Generated with AI**

This project was generated using [Claude Code](https://www.anthropic.com/claude/code).

Made with Python 3.14
