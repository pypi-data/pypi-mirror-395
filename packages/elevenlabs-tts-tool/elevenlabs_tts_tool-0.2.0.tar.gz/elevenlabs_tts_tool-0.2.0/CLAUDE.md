# elevenlabs-tts-tool - Developer Guide

## Overview

`elevenlabs-tts-tool` is a professional command-line tool for ElevenLabs text-to-speech synthesis. Built with Python 3.13+, uv, mise, and click, it provides both CLI and library interfaces for TTS generation.

**Tech Stack:**
- Python 3.13+
- [uv](https://github.com/astral-sh/uv) - Fast Python package manager
- [mise](https://mise.jdx.dev/) - Runtime version manager
- [click](https://click.palletsprojects.com/) - CLI framework
- [ElevenLabs SDK](https://github.com/elevenlabs/elevenlabs-python) - TTS API client

## Architecture

The project follows a clean separation of concerns with modular architecture:

```
elevenlabs-tts-tool/
├── elevenlabs_tts_tool/
│   ├── __init__.py              # Public API exports for library usage
│   ├── cli.py                   # CLI entry point (Click group)
│   ├── voices.py                # Voice management (VoiceManager, VoiceProfile)
│   ├── voices_lookup.json       # Voice lookup table (42 premium voices)
│   ├── models.py                # Model management (ModelInfo, validation)
│   ├── core/                    # Core library functions (importable, CLI-independent)
│   │   ├── __init__.py
│   │   ├── client.py           # ElevenLabs client initialization
│   │   └── synthesize.py       # TTS synthesis functions
│   ├── commands/                # CLI command implementations (Click wrappers)
│   │   ├── __init__.py
│   │   ├── synthesize_commands.py  # Synthesize command
│   │   ├── voice_commands.py       # List-voices command
│   │   ├── model_commands.py       # List-models, pricing commands
│   │   └── update_voices_commands.py  # Update-voices command
│   └── utils.py                 # Shared utilities
├── references/                  # Research documentation
│   ├── free-tier.md            # Free tier limits and features
│   ├── emotions-and-pauses.md  # Emotion control, SSML, voice settings
│   └── models.md               # Complete model guide
├── tests/                       # Test suite
│   ├── test_utils.py
│   ├── test_voices.py
│   └── test_models.py
├── pyproject.toml               # Project configuration
├── Makefile                     # Development commands
├── README.md                    # User documentation
└── CLAUDE.md                    # This file (developer guide)
```

### Key Design Principles

1. **Separation of Concerns**
   - `core/` contains pure library functions (no CLI dependencies)
   - `commands/` contains CLI wrappers with Click decorators
   - Core functions are fully importable and reusable

2. **Exception-Based Errors**
   - Core functions raise exceptions (NOT sys.exit)
   - CLI layer catches exceptions and formats user-friendly messages
   - Error messages include suggested fixes for agent-friendly ReAct loops

3. **Composability**
   - JSON output to stdout, logs/errors to stderr
   - Enables piping and integration with automation tools

4. **Type Safety**
   - Strict mypy checks throughout
   - Comprehensive type hints on all functions
   - Modern Python 3.13+ syntax (dict/list over Dict/List)

## Development Commands

### Quick Start

```bash
# Install dependencies
make install

# Run full quality pipeline
make pipeline
```

### Quality Checks

```bash
make format      # Auto-format with ruff
make lint        # Lint with ruff
make typecheck   # Type check with mypy (strict mode)
make test        # Run pytest suite
make check       # Run all checks (lint + typecheck + test)
```

### Build & Install

```bash
make build            # Build wheel package
make install-global   # Install globally with uv tool
make clean            # Remove build artifacts
make pipeline         # Full pipeline: format, check, build, install-global
```

## Code Standards

- **Python Version**: 3.13+ with modern syntax
- **Line Length**: 100 characters
- **Type Hints**: Required for all functions
- **Docstrings**: Module-level and function-level with Args/Returns/Raises sections
- **Formatting**: Automated with ruff
- **Linting**: Strict ruff rules (E, F, I, N, W, UP)
- **Type Checking**: Strict mypy mode (disallow_untyped_defs, disallow_any_generics)

### Module-Level Docstrings

All modules include AI-generation acknowledgment:

```python
"""
Module description here.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""
```

## CLI Commands

### synthesize

Convert text to speech with flexible input/output options.

**Signature:**
```bash
elevenlabs-tts-tool synthesize [TEXT] [OPTIONS]
```

**Arguments:**
- `TEXT` - Text to synthesize (optional if --stdin used)

**Options:**
- `--stdin, -s` - Read text from stdin instead of argument
- `--voice, -v` - Voice name or ID (default: rachel)
- `--model, -m` - Model ID (default: eleven_turbo_v2_5)
- `--output, -o PATH` - Save to audio file instead of playing
- `--format, -f` - Output format (default: mp3_44100_128)

**Examples:**
```bash
# Play through speakers
elevenlabs-tts-tool synthesize "Hello world"

# Use different voice
elevenlabs-tts-tool synthesize "Hello" --voice adam

# Use specific model
elevenlabs-tts-tool synthesize "Hello" --model eleven_multilingual_v2

# Emotional expression (requires eleven_v3)
elevenlabs-tts-tool synthesize "[happy] Welcome!" --model eleven_v3

# Read from stdin
echo "Text" | elevenlabs-tts-tool synthesize --stdin

# Save to file
elevenlabs-tts-tool synthesize "Text" --output speech.mp3
```

### list-voices

List all available voices with characteristics.

**Signature:**
```bash
elevenlabs-tts-tool list-voices
```

**Output Format:**
```
Voice           Gender     Age          Accent          Description
====================================================================================================
rachel          female     young        American        Calm and friendly American voice...
adam            male       middle_aged  American        Deep, authoritative American male...
...
====================================================================================================
Total: 42 voices available
```

**Examples:**
```bash
# List all voices
elevenlabs-tts-tool list-voices

# Filter by characteristics
elevenlabs-tts-tool list-voices | grep British
elevenlabs-tts-tool list-voices | grep "female.*young"
```

### update-voices

Update voice lookup table from ElevenLabs API.

**Signature:**
```bash
elevenlabs-tts-tool update-voices [OPTIONS]
```

**Options:**
- `--output, -o PATH` - Output file path (default: `~/.config/elevenlabs-tts-tool/voices_lookup.json`)

**Examples:**
```bash
# Update default voice lookup (user config directory)
elevenlabs-tts-tool update-voices

# Save to custom location
elevenlabs-tts-tool update-voices --output custom_voices.json
```

**Behavior:**
- Fetches all premade voices from ElevenLabs API
- Saves to user config directory by default (`~/.config/elevenlabs-tts-tool/`)
- Creates config directory if it doesn't exist
- Updates take precedence over package default

### list-models

List all available ElevenLabs TTS models with characteristics.

**Signature:**
```bash
elevenlabs-tts-tool list-models
```

**Output Format:**
```
Current Generation Models:

1. Eleven v3 (Alpha) - eleven_v3
   - Most emotionally expressive
   - 70+ languages
   - 5,000 char limit
   - High latency
   - Best for: Emotional dialogue, audiobooks
   - Note: Alpha release - may have inconsistencies. Generate multiple options.

2. Eleven Multilingual v2 - eleven_multilingual_v2
   - Highest production quality
   - 29 languages
   - 10,000 char limit
   - Medium latency
   - Best for: Professional content, e-learning

...

Legacy Models (Deprecated):

- eleven_turbo_v2
  Superseded by Turbo v2.5. Migrate for 50% cost savings.
```

**Examples:**
```bash
# List all models
elevenlabs-tts-tool list-models

# Filter by status
elevenlabs-tts-tool list-models | grep stable
elevenlabs-tts-tool list-models | grep deprecated

# Find specific features
elevenlabs-tts-tool list-models | grep -i "ultra-low"
```

### pricing

Display ElevenLabs pricing tiers and features.

**Signature:**
```bash
elevenlabs-tts-tool pricing
```

**Output Information:**
- Pricing tiers (Free, Starter, Creator, Pro, Scale, Business)
- Minutes included per tier
- Additional minute costs
- Audio quality options
- Concurrency limits
- Priority levels
- API formats by tier
- Model cost multipliers (v3 = 2x cost)

**Examples:**
```bash
# View full pricing table
elevenlabs-tts-tool pricing

# Find specific tier information
elevenlabs-tts-tool pricing | grep Creator
elevenlabs-tts-tool pricing | grep "44.1kHz PCM"
```

**Key Insights:**
- v3 models cost 2x as much as Flash/Turbo models (half the minutes/tokens)
- Use Flash v2.5 for high-volume Claude Code integrations
- Reserve v3 for content requiring emotional expression

### info

Display subscription and usage information.

**Signature:**
```bash
elevenlabs-tts-tool info [OPTIONS]
```

**Options:**
- `--days, -d` - Number of days of historical usage to display (default: 7)

**Output Information:**
- Subscription tier and status
- Character usage (used/limit/remaining)
- Quota reset date
- Historical usage breakdown by day
- Average daily usage
- Projected monthly usage
- Warnings when approaching quota limits

**Examples:**
```bash
# View subscription with last 7 days of usage
elevenlabs-tts-tool info

# View last 30 days of usage
elevenlabs-tts-tool info --days 30

# Quick quota check (1 day)
elevenlabs-tts-tool info --days 1
```

**Use Cases:**
- Monitor character quota consumption
- Track usage patterns over time
- Plan when to upgrade subscription tier
- Avoid hitting quota limits unexpectedly
- Identify high-usage periods

**API Endpoints Used:**
- `client.user.subscription.get()` - Current subscription info
- `client.usage.get()` - Historical usage metrics

## Advanced Features

### Emotion Control

ElevenLabs v3 model (`eleven_v3`) supports **Audio Tags** for emotional expression.

**Available Emotion Tags:**
- `[happy]`, `[excited]`, `[sad]`, `[angry]`, `[nervous]`, `[curious]`
- `[cheerfully]`, `[playfully]`, `[mischievously]`, `[resigned tone]`, `[flatly]`, `[deadpan]`

**Speech Characteristics:**
- `[whispers]`, `[laughs]`, `[gasps]`, `[sighs]`, `[pauses]`, `[hesitates]`, `[stammers]`, `[gulps]`

**Usage:**
```bash
# Basic emotion (requires eleven_v3 model)
elevenlabs-tts-tool synthesize "[happy] Welcome to our service!" --model eleven_v3

# Multiple emotions in sequence
elevenlabs-tts-tool synthesize "[excited] Great news! [cheerfully] Your project is approved!" --model eleven_v3
```

**Best Practices:**
- Place tags at the beginning of phrases
- Align text content with emotional intent
- Test with different voices for best results
- Use sparingly - let AI infer emotion from context when possible

### Pause Control (SSML)

Add natural pauses using SSML `<break>` tags.

**Syntax:**
```xml
<break time="X.Xs" />
```

**Examples:**
```bash
# 1-second pause
elevenlabs-tts-tool synthesize "Welcome <break time=\"1.0s\" /> to our service."

# Multiple pauses
elevenlabs-tts-tool synthesize "Point one <break time=\"0.5s\" /> Point two <break time=\"0.5s\" /> Point three."

# Combine with emotions (requires eleven_v3)
elevenlabs-tts-tool synthesize "[happy] Hello! <break time=\"0.5s\" /> [cheerfully] How are you?" --model eleven_v3
```

**Limitations:**
- Maximum pause duration: 3 seconds
- Recommended: 2-4 breaks per generation
- Too many breaks can cause:
  - AI speedup
  - Audio artifacts
  - Background noise
  - Generation instability

**Alternative Methods:**
- Dashes (`-` or `—`) for shorter pauses (less consistent)
- Ellipses (`...`) for hesitation (may add nervous tone)
- SSML `<break>` is most reliable

### Voice Settings Parameters

Fine-tune voice characteristics via API:

**Parameters:**
- **stability** (0.0-1.0, default 0.5): Controls emotional range vs. consistency
  - Lower: More expressive, varied delivery
  - Higher: More monotonous, consistent
- **similarity_boost** (0.0-1.0, default 0.75): Adherence to original voice
  - Lower: More creative interpretation
  - Higher: Closer to original voice
- **style** (0.0-1.0, default 0.0): Exaggerate voice's natural style
  - Higher values increase computational cost and latency
- **speed** (default 1.0): Speaking speed multiplier
  - < 1.0: Slower (e.g., 0.8 = 80% speed)
  - > 1.0: Faster (e.g., 1.2 = 120% speed)
- **use_speaker_boost** (boolean, default true): Enhance similarity to speaker
  - Increases computational cost and latency when enabled

**Note:** Voice settings are only available via library API, not CLI. See [Library Usage](#library-usage) for examples.

### Research Documents

Comprehensive guides available in `references/`:
- [Free Tier Limitations](references/free-tier.md) - Character limits, features, upgrade tiers
- [Emotions and Pauses](references/emotions-and-pauses.md) - Complete emotion tags, SSML, voice settings

## Free Tier Limitations

**ElevenLabs Free Tier (2024-2025):**
- ✅ 10,000-20,000 characters per month
- ✅ All 42 premade voices
- ✅ Create up to 3 custom voices
- ✅ MP3 formats (all bitrates)
- ✅ Basic SSML support (`<break>`, phonemes)
- ✅ Emotional tags (v3 models)
- ✅ Full API access
- ❌ No commercial license (personal/experimentation only)
- ❌ PCM 44.1kHz format (requires Pro tier)
- ⚠️ Max 2,500 characters per single generation

**Upgrade Tiers:**
- **Creator Tier**: PCM formats, higher limits, commercial license
- **Pro Tier**: PCM 44.1kHz, highest limits, Director's Mode (alpha)

**Rate Limits:** Not publicly documented - expect reasonable use restrictions on free tier

For detailed free tier information: [references/free-tier.md](references/free-tier.md)

## Claude Code Integration

Use `elevenlabs-tts-tool` as notification system for Claude Code hooks.

### Use Cases

**1. Task Completion Alerts**
```bash
# After long-running task
elevenlabs-tts-tool synthesize "[excited] Task completed successfully!"
```

**2. Error Notifications**
```bash
# On build failure
elevenlabs-tts-tool synthesize "[nervous] Error detected. Please check output."
```

**3. Custom Workflows**
```bash
# Shell script integration
make build && elevenlabs-tts-tool synthesize "[cheerfully] Build successful!" || \
    elevenlabs-tts-tool synthesize "[sad] Build failed. Check logs."
```

**4. Multi-Tool Integration**
```bash
# Combine with other CLI tools
gemini-google-search-tool query "AI news" | \
    elevenlabs-tts-tool synthesize --stdin --voice charlotte --output news.mp3
```

### Hook Configuration

Create hooks in `~/.config/claude-code/hooks.json`:

```json
{
  "hooks": {
    "after_command": {
      "type": "bash",
      "command": "elevenlabs-tts-tool synthesize \"[happy] Task completed!\" --voice rachel"
    },
    "on_error": {
      "type": "bash",
      "command": "elevenlabs-tts-tool synthesize \"[nervous] Error occurred!\" --voice adam"
    }
  }
}
```

**Benefits:**
- Audio alerts for completed tasks without monitoring terminal
- Error notifications while away from screen
- Multi-step automation with voice feedback
- Voice-enabled AI agent pipelines

## Library Usage

The tool can be imported as a Python library:

```python
from elevenlabs_tts_tool import get_client, play_speech, save_speech
from elevenlabs_tts_tool import VoiceManager, VoiceProfile
from pathlib import Path

# Initialize client
client = get_client()  # Reads ELEVENLABS_API_KEY from env

# Get voice ID from friendly name
manager = VoiceManager()
voice_id = manager.get_voice_id("rachel")  # Case-insensitive

# Synthesize and play
play_speech(client, "Hello world", voice_id)

# Synthesize and save
save_speech(client, "Hello world", voice_id, Path("output.wav"))

# List available voices
for name, profile in manager.list_voices():
    print(f"{name}: {profile.gender}, {profile.age}, {profile.accent}")
```

### Public API

**Exported from `elevenlabs_tts_tool`:**
- `get_client()` - Initialize ElevenLabs client
- `play_speech(client, text, voice_id)` - Play through speakers
- `save_speech(client, text, voice_id, output_path)` - Save to file
- `VoiceManager` - Voice lookup and management
- `VoiceProfile` - Voice metadata dataclass

## Testing

### Run Tests

```bash
# All tests
make test

# Verbose output
uv run pytest tests/ -v

# Specific test file
uv run pytest tests/test_voices.py

# With coverage
uv run pytest tests/ --cov=elevenlabs_tts_tool
```

### Test Structure

- `tests/test_utils.py` - Utility function tests
- `tests/test_voices.py` - VoiceManager tests (no API calls)

Core TTS functions are tested manually as they require API access.

## Important Notes

### Dependencies

- **click** - CLI framework ([docs](https://click.palletsprojects.com/))
- **elevenlabs** - Official SDK ([GitHub](https://github.com/elevenlabs/elevenlabs-python))

### Authentication

All commands require `ELEVENLABS_API_KEY` environment variable:

```bash
export ELEVENLABS_API_KEY='your-api-key'
```

Get your API key: https://elevenlabs.io/app/settings/api-keys

### Shell Completion

The tool provides built-in shell completion support for bash, zsh, and fish.

**Implementation:**
- Uses Click's built-in `ShellComplete` classes
- Follows the `my-cli completion <shell>` pattern (like kubectl, helm, docker)
- Provides self-documenting help with installation instructions

**Generate completion scripts:**
```bash
# Bash
elevenlabs-tts-tool completion bash

# Zsh
elevenlabs-tts-tool completion zsh

# Fish
elevenlabs-tts-tool completion fish
```

**Installation:**
```bash
# Bash (add to ~/.bashrc)
eval "$(elevenlabs-tts-tool completion bash)"

# Zsh (add to ~/.zshrc)
eval "$(elevenlabs-tts-tool completion zsh)"

# Fish (save to completion file)
elevenlabs-tts-tool completion fish > ~/.config/fish/completions/elevenlabs-tts-tool.fish
```

**Code Location:**
- Command: `elevenlabs_tts_tool/commands/completion_commands.py`
- Uses: `click.shell_completion.BashComplete`, `ZshComplete`, `FishComplete`

**Features:**
- Tab-complete commands and subcommands
- Tab-complete options and flags
- Context-aware completion for file paths and choices
- Self-documenting with `--help`

### Verbosity and Logging

The tool supports multi-level verbosity for progressive detail control:

**Verbosity Levels:**
- **No flag** (default): WARNING level - only critical issues
- **`-v`**: INFO level - high-level operations, important events
- **`-vv`**: DEBUG level - detailed operations, API calls, validation steps
- **`-vvv`**: TRACE level - full HTTP requests/responses, ElevenLabs SDK internals

**Implementation:**
```python
# Logging configuration in elevenlabs_tts_tool/logging_config.py
from elevenlabs_tts_tool.logging_config import setup_logging, get_logger

# Setup logging (called automatically by CLI group)
setup_logging(verbose_count)  # 0, 1, 2, or 3+

# Get logger in any module
logger = get_logger(__name__)
logger.info("High-level operation")
logger.debug("Detailed operation step")
logger.error("Error occurred")
```

**CLI Usage:**
```bash
# Quiet mode (warnings only)
elevenlabs-tts-tool synthesize "Hello world"

# INFO level
elevenlabs-tts-tool -v synthesize "Hello world"

# DEBUG level
elevenlabs-tts-tool -vv synthesize "Hello world"

# TRACE level (shows ElevenLabs SDK and HTTP client logs)
elevenlabs-tts-tool -vvv synthesize "Hello world"
```

**Dependent Library Logging:**

At trace level (`-vvv`), the following libraries enable DEBUG logging:
- `elevenlabs` - ElevenLabs SDK internals
- `httpx` / `httpcore` - HTTP request/response details
- `urllib3` - Low-level HTTP operations

This is configured in `logging_config.py:setup_logging()`.

### Voice Lookup Table

The `voices_lookup.json` file contains 42 curated ElevenLabs premium voices with:
- Friendly names (e.g., "rachel", "adam", "charlotte")
- Voice metadata (gender, age, accent, language, description)
- Voice IDs for API calls

**Voice lookup locations** (checked in order):
1. User config: `~/.config/elevenlabs-tts-tool/voices_lookup.json` (if exists)
2. Package default: Bundled `voices_lookup.json` (fallback)

**Update voice table:**
```bash
# Updates ~/.config/elevenlabs-tts-tool/voices_lookup.json
elevenlabs-tts-tool update-voices

# Save to custom location
elevenlabs-tts-tool update-voices --output /path/to/voices.json
```

This design allows:
- ✅ Updates persist across package reinstalls
- ✅ Works with read-only package installations
- ✅ Users can customize voice list without modifying package files
- ✅ Falls back to bundled voices if user never updates

### Voice Selection

The VoiceManager supports:
1. **Friendly names**: `rachel`, `adam`, `charlotte` (case-insensitive)
2. **Direct voice IDs**: 20-character alphanumeric strings
3. **Validation**: Raises ValueError with helpful message if voice not found

### Default Voice

Default voice is **rachel** (Voice ID: `21m00Tcm4TlvDq8ikWAM`):
- Gender: female
- Age: young
- Accent: American
- Description: Calm and friendly American voice

### Audio Format

- **Model**: `eleven_turbo_v2_5` (fast, high-quality)
- **Output Format**: `mp3_44100_128` (44.1kHz, 128kbps MP3)
- **Playback**: Uses elevenlabs.play() for direct speaker output
- **File Save**: Uses elevenlabs.save() for WAV file output

### Version Consistency

Keep version synced across three files:
1. `pyproject.toml` - `[project] version = "0.1.0"`
2. `cli.py` - `@click.version_option(version="0.1.0")`
3. `__init__.py` - `__version__ = "0.1.0"`

## Known Issues & Future Fixes

### ElevenLabs SDK Pydantic Compatibility

**Issue**: The ElevenLabs SDK uses Pydantic V1 compatibility layer, which causes warnings with Python 3.14+

**Solution**: Project uses Python 3.13 to avoid Pydantic V1 compatibility warnings

**Note**: When ElevenLabs SDK migrates to native Pydantic V2 API, we can upgrade to Python 3.14+

**GitHub Issue**: Track SDK migration at https://github.com/elevenlabs/elevenlabs-python/issues

### Type Hints for ElevenLabs SDK

**Issue**: SDK returns `Any` type for audio iterators, causing mypy errors

**Workaround**: Added `# type: ignore[no-any-return]` in `core/synthesize.py:41`

**Future Fix**: When SDK adds proper type hints, remove type ignore comments

## Resources

- **ElevenLabs Docs**: https://elevenlabs.io/docs
- **API Reference**: https://elevenlabs.io/docs/api-reference
- **Python SDK**: https://github.com/elevenlabs/elevenlabs-python
- **Voice Library**: https://elevenlabs.io/voice-library
- **Click Docs**: https://click.palletsprojects.com/
- **uv Docs**: https://github.com/astral-sh/uv
- **mise Docs**: https://mise.jdx.dev/

## Contributing

When making changes:

1. Follow the architecture principles (separation of concerns, exceptions over exits)
2. Add type hints to all new functions
3. Write tests for new functionality
4. Update documentation (README.md, CLAUDE.md, docstrings)
5. Run `make pipeline` before committing
6. Keep version numbers in sync across all three locations

## License

MIT License - see [LICENSE](LICENSE) file.

---

**Note**: This project was developed with assistance from Claude Code, Anthropic's AI-powered development tool.
