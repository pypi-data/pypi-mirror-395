---
description: List ElevenLabs TTS models
---

List all available ElevenLabs TTS models with characteristics.

## Usage

```bash
elevenlabs-tts-tool list-models
```

## Examples

```bash
# List all models
elevenlabs-tts-tool list-models

# Filter by status
elevenlabs-tts-tool list-models | grep stable

# Find specific features
elevenlabs-tts-tool list-models | grep -i "ultra-low"
```

## Output

Detailed model information with IDs, features, languages, and use cases.
