# kokoro-tts-tool - Project Specification

## Goal

A CLI that provides local text-to-speech using Kokoro TTS on Apple Silicon.

## What is kokoro-tts-tool?

`kokoro-tts-tool` is a Python CLI for local text-to-speech synthesis using the Kokoro-82M model. It provides:

- **Local inference**: ONNX runtime for fast, CPU-optimized synthesis
- **60+ voices**: Multiple languages (English, Japanese, Mandarin, Spanish, etc.)
- **Infinite streaming**: Continuous TTS for long documents without audio artifacts
- **Fast rendering**: 20-50x real-time on Apple Silicon M4

## Technical Requirements

### Runtime

- Python 3.14+
- Installable globally with mise
- Cross-platform (macOS, Linux, Windows)

### Dependencies

- `click` - CLI framework
- `kokoro-onnx` - ONNX implementation of Kokoro TTS
- `sounddevice` - Audio playback
- `soundfile` - WAV file handling
- `numpy` - Audio array processing

### Development Dependencies

- `ruff` - Linting and formatting
- `mypy` - Type checking
- `pytest` - Testing framework
- `bandit` - Security linting
- `pip-audit` - Dependency vulnerability scanning
- `gitleaks` - Secret detection (requires separate installation)

## CLI Commands

```bash
kokoro-tts-tool [OPTIONS] COMMAND [ARGS]
```

### Global Options

- `-v, --verbose` - Enable verbose output (count flag: -v, -vv, -vvv)
  - `-v` (count=1): INFO level logging
  - `-vv` (count=2): DEBUG level logging
  - `-vvv` (count=3+): TRACE level (includes library internals)
- `--help` / `-h` - Show help message
- `--version` - Show version

### Commands

| Command | Description |
|---------|-------------|
| `init` | Download and initialize TTS models (~350MB) |
| `synthesize` | Convert text to speech (speakers or file) |
| `infinite` | Stream continuous TTS from long documents |
| `list-voices` | List all 60+ available TTS voices |
| `info` | Display configuration status |
| `completion` | Generate shell completion script |

### Quick Start Examples

```bash
# Initialize (downloads models)
kokoro-tts-tool init

# Basic synthesis to speakers
kokoro-tts-tool synthesize "Hello world"

# Save to file with different voice
kokoro-tts-tool synthesize "Hello" --voice am_adam --output speech.wav

# Stream a book to speakers
kokoro-tts-tool infinite --input book.md

# Render audiobook (fast offline mode)
kokoro-tts-tool infinite --input book.md --output audiobook.wav
```

## Project Structure

```
kokoro-tts-tool/
├── kokoro_tts_tool/
│   ├── __init__.py
│   ├── cli.py            # Click CLI entry point (group with subcommands)
│   ├── engine.py         # TTS engine wrapper (kokoro-onnx)
│   ├── models.py         # Model downloading and management
│   ├── voices.py         # Voice definitions and validation
│   ├── splitter.py       # Text chunking for long documents
│   ├── streaming.py      # Audio streaming for speaker playback
│   ├── completion.py     # Shell completion command
│   ├── logging_config.py # Multi-level verbosity logging
│   ├── utils.py          # Utility functions
│   └── commands/         # CLI command modules
│       ├── __init__.py
│       ├── synthesize_commands.py  # Text-to-speech synthesis
│       ├── voice_commands.py       # Voice listing/filtering
│       ├── init_commands.py        # Model initialization
│       ├── info_commands.py        # Configuration display
│       └── infinite_commands.py    # Long document streaming
├── tests/
│   ├── __init__.py
│   ├── test_utils.py
│   ├── test_models.py
│   ├── test_voices.py
│   ├── test_splitter.py
│   └── test_streaming.py
├── plugins/              # Claude Code plugin
│   └── kokoro-tts-tool/
│       ├── commands/     # Slash commands
│       └── skills/       # Skills
├── references/           # Research documentation
├── pyproject.toml        # Project configuration
├── README.md             # User documentation
├── CLAUDE.md             # This file
├── Makefile              # Development commands
├── LICENSE               # MIT License
├── .mise.toml            # mise configuration
├── .gitleaks.toml        # Gitleaks configuration
└── .gitignore
```

## Code Style

- Type hints for all functions
- Docstrings for all public functions
- Follow PEP 8 via ruff
- 100 character line length
- Strict mypy checking

## Development Workflow

```bash
# Install dependencies
make install

# Run linting
make lint

# Format code
make format

# Type check
make typecheck

# Run tests
make test

# Security scanning
make security-bandit       # Python security linting
make security-pip-audit    # Dependency CVE scanning
make security-gitleaks     # Secret detection
make security              # Run all security checks

# Run all checks (includes security)
make check

# Full pipeline (includes security)
make pipeline
```

## Security

The template includes three lightweight security tools:

1. **bandit** - Python code security linting
   - Detects: SQL injection, hardcoded secrets, unsafe functions
   - Speed: ~2-3 seconds

2. **pip-audit** - Dependency vulnerability scanning
   - Detects: Known CVEs in dependencies
   - Speed: ~2-3 seconds

3. **gitleaks** - Secret and API key detection
   - Detects: AWS keys, GitHub tokens, API keys, private keys
   - Speed: ~1 second
   - Requires: `brew install gitleaks` (macOS)

All security checks run automatically in `make check` and `make pipeline`.

## Multi-Level Verbosity Logging

The template includes a centralized logging system with progressive verbosity levels.

### Implementation Pattern

1. **logging_config.py** - Centralized logging configuration
   - `setup_logging(verbose_count)` - Configure logging based on -v count
   - `get_logger(name)` - Get logger instance for module
   - Maps verbosity to Python logging levels (WARNING/INFO/DEBUG)

2. **CLI Integration** - Add to every CLI command
   ```python
   from kokoro_tts_tool.logging_config import get_logger, setup_logging

   logger = get_logger(__name__)

   @click.command()
   @click.option("-v", "--verbose", count=True, help="...")
   def command(verbose: int):
       setup_logging(verbose)  # First thing in command
       logger.info("Operation started")
       logger.debug("Detailed info")
   ```

3. **Logging Levels**
   - **0 (no -v)**: WARNING only - production/quiet mode
   - **1 (-v)**: INFO - high-level operations
   - **2 (-vv)**: DEBUG - detailed debugging
   - **3+ (-vvv)**: TRACE - enable library internals

4. **Best Practices**
   - Always log to stderr (keeps stdout clean for piping)
   - Use structured messages with placeholders: `logger.info("Found %d items", count)`
   - Call `setup_logging()` first in every command
   - Use `get_logger(__name__)` at module level
   - For TRACE level, enable third-party library loggers in `logging_config.py`

5. **Customizing Library Logging**
   Edit `logging_config.py` to add project-specific libraries:
   ```python
   if verbose_count >= 3:
       logging.getLogger("requests").setLevel(logging.DEBUG)
       logging.getLogger("urllib3").setLevel(logging.DEBUG)
   ```

## Shell Completion

The template includes shell completion for bash, zsh, and fish following the Click Shell Completion Pattern.

### Implementation

1. **completion.py** - Separate module for completion command
   - Uses Click's `BashComplete`, `ZshComplete`, `FishComplete` classes
   - Generates shell-specific completion scripts
   - Includes installation instructions in help text

2. **CLI Integration** - Added as subcommand
   ```python
   from kokoro_tts_tool.completion import completion_command

   @click.group(invoke_without_command=True)
   def main(ctx: click.Context):
       # Default behavior when no subcommand
       if ctx.invoked_subcommand is None:
           # Main command logic here
           pass

   # Add completion subcommand
   main.add_command(completion_command)
   ```

3. **Usage Pattern** - User-friendly command
   ```bash
   # Generate completion script
   kokoro-tts-tool completion bash
   kokoro-tts-tool completion zsh
   kokoro-tts-tool completion fish

   # Install (eval or save to file)
   eval "$(kokoro-tts-tool completion bash)"
   ```

4. **Supported Shells**
   - **Bash** (≥ 4.4) - Uses bash-completion
   - **Zsh** (any recent) - Uses zsh completion system
   - **Fish** (≥ 3.0) - Uses fish completion system
   - **PowerShell** - Not supported by Click

5. **Installation Methods**
   - **Temporary**: `eval "$(kokoro-tts-tool completion bash)"`
   - **Permanent**: Add eval to ~/.bashrc or ~/.zshrc
   - **File-based** (recommended): Save to dedicated completion file

### Adding More Commands

The CLI uses `@click.group()` for extensibility. To add new commands:

1. Create new command module in `kokoro_tts_tool/`
2. Import and add to CLI group:
   ```python
   from kokoro_tts_tool.new_command import new_command
   main.add_command(new_command)
   ```

3. Completion will automatically work for new commands and their options

## Installation Methods

### Global installation with mise

```bash
cd /path/to/kokoro-tts-tool
mise use -g python@3.14
uv sync
uv tool install .
```

After installation, `kokoro-tts-tool` command is available globally.

### Local development

```bash
uv sync
uv run kokoro-tts-tool [args]
```

## Publishing to PyPI

The template includes GitHub Actions workflow for automated PyPI publishing with trusted publishing (no API tokens required).

### Setup PyPI Trusted Publishing

1. **Create PyPI Account** at https://pypi.org/account/register/
   - Enable 2FA (required)
   - Verify email

2. **Configure Trusted Publisher** at https://pypi.org/manage/account/publishing/
   - Click "Add a new pending publisher"
   - **PyPI Project Name**: `kokoro-tts-tool`
   - **Owner**: `dnvriend`
   - **Repository name**: `kokoro-tts-tool`
   - **Workflow name**: `publish.yml`
   - **Environment name**: `pypi`

3. **(Optional) Configure TestPyPI** at https://test.pypi.org/manage/account/publishing/
   - Same settings but use environment: `testpypi`

### Publishing Workflow

The `.github/workflows/publish.yml` workflow:
- Builds on every push
- Publishes to TestPyPI and PyPI on git tags (v*)
- Uses trusted publishing (no secrets needed)

### Create a Release

```bash
# Commit your changes
git add .
git commit -m "Release v0.1.0"
git push

# Create and push tag
git tag v0.1.0
git push origin v0.1.0
```

The workflow automatically builds and publishes to PyPI.

### Install from PyPI

After publishing, users can install with:

```bash
pip install kokoro-tts-tool
```

### Build Locally

```bash
# Build package with force rebuild (avoids cache issues)
make build

# Output in dist/
ls dist/
```
