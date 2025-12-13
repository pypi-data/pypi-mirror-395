---
description: Convert text to speech with ElevenLabs
argument-hint: text
---

Convert TEXT to speech using ElevenLabs API. Play through speakers or save to file.

## Usage

```bash
elevenlabs-tts-tool synthesize TEXT [OPTIONS]
```

## Arguments

- `TEXT`: Text to synthesize (required, or use --stdin)
- `--stdin, -s`: Read text from stdin instead
- `--voice, -v NAME`: Voice name or ID (default: rachel)
- `--model, -m ID`: Model ID (default: eleven_turbo_v2_5)
- `--output, -o PATH`: Save to file instead of playing
- `--format, -f FORMAT`: Output format (default: mp3_44100_128)

## Examples

```bash
# Basic usage
elevenlabs-tts-tool synthesize "Hello world"

# Different voice
elevenlabs-tts-tool synthesize "Hello" --voice adam

# Emotional expression (requires eleven_v3)
elevenlabs-tts-tool synthesize "[happy] Welcome!" --model eleven_v3

# Read from stdin
echo "Text" | elevenlabs-tts-tool synthesize --stdin

# Save to file
elevenlabs-tts-tool synthesize "Text" --output speech.mp3
```

## Output

Plays audio through speakers or saves to file in specified format.
