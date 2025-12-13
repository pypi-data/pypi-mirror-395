---
description: List available ElevenLabs voices
---

List all available ElevenLabs voices with characteristics.

## Usage

```bash
elevenlabs-tts-tool list-voices
```

## Examples

```bash
# List all voices
elevenlabs-tts-tool list-voices

# Filter by gender
elevenlabs-tts-tool list-voices | grep female

# Filter by accent
elevenlabs-tts-tool list-voices | grep British
```

## Output

Table format with voice name, gender, age, accent, and description.
