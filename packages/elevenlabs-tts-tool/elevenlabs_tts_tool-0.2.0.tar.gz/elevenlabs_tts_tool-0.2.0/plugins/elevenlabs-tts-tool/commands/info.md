---
description: Show subscription and usage information
---

Display ElevenLabs subscription tier, character usage, and historical stats.

## Usage

```bash
elevenlabs-tts-tool info [--days N]
```

## Arguments

- `--days, -d N`: Number of days of historical usage (default: 7)

## Examples

```bash
# View subscription with last 7 days
elevenlabs-tts-tool info

# View last 30 days
elevenlabs-tts-tool info --days 30

# Quick quota check
elevenlabs-tts-tool info --days 1
```

## Output

Subscription tier, quota usage, remaining characters, and daily usage breakdown.
