---
description: Update voice lookup table from API
---

Fetch latest voices from ElevenLabs API and update local lookup table.

## Usage

```bash
elevenlabs-tts-tool update-voices [--output PATH]
```

## Arguments

- `--output, -o PATH`: Output file path (default: ~/.config/elevenlabs-tts-tool/voices_lookup.json)

## Examples

```bash
# Update default voice lookup
elevenlabs-tts-tool update-voices

# Save to custom location
elevenlabs-tts-tool update-voices --output custom_voices.json
```

## Output

Updates voice lookup table with latest premade voices from API.
