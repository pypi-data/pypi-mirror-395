# ElevenLabs API: Emotions and Pauses Control

## Emotion Control

### Audio Tags (v3 Models)

ElevenLabs v3 models support **Audio Tags** for emotional nuance control.

#### Available Emotion Tags

**Primary Emotions:**
- `[happy]` - Joyful, upbeat tone
- `[excited]` - Energetic, enthusiastic delivery
- `[sad]` - Melancholic, somber tone
- `[angry]` - Frustrated, aggressive delivery
- `[nervous]` - Anxious, uncertain tone
- `[curious]` - Inquisitive, wondering delivery

**Speech Characteristics:**
- `[sigh]` - Audible sigh
- `[laughs]` - Laughter
- `[gulps]` - Swallowing sound
- `[gasps]` - Sharp intake of breath
- `[whispers]` - Quiet, breathy speech
- `[pauses]` - Brief hesitation
- `[hesitates]` - Uncertain pause
- `[stammers]` - Speech disfluency

**Delivery Styles:**
- `[resigned tone]` - Accepting, defeated
- `[cheerfully]` - Bright, positive
- `[flatly]` - Monotone, emotionless
- `[deadpan]` - Dry, humorless
- `[playfully]` - Teasing, fun
- `[mischievously]` - Sly, impish

### Usage Patterns

#### Basic Placement
```python
text = "[happy] Welcome to our service! We're excited to help you today."
```

Place emotion tags at the **beginning** of phrases or sentences for best results.

#### Contextual Influence (Advanced)

Use the `next_text` API parameter to provide emotional context without speaking it aloud:

```python
# API request structure
{
  "text": "I can't believe this happened",
  "next_text": "she shouted, angrily",  # Influences prosody without speaking
  "voice_id": "21m00Tcm4TlvDq8ikWAM",
  "model_id": "eleven_turbo_v2_5"
}
```

The AI uses `next_text` to influence emotional delivery without synthesizing it.

### Future Development

**Director's Mode (Alpha):**
- Enhanced emotional control
- Fine-tuned expression parameters
- Currently in alpha testing
- Expected to provide granular control over emotional outputs

## Pause Control

### SSML Break Tags (Recommended)

The most reliable method for natural pauses:

```python
text = "Welcome <break time=\"1.0s\" /> to our service."
```

**Syntax:**
- `<break time=\"X.Xs\" />` where X.X is duration in seconds
- Maximum pause duration: **3.0 seconds**
- Creates natural pauses (not just silence)

**Example:**
```python
text = """
Good morning <break time=\"0.5s\" />
I hope you're having a great day <break time=\"1.0s\" />
Let's get started.
"""
```

### Alternative Methods

#### Dashes (Short Pauses)
```python
text = "Hello - welcome to our service - how can I help?"
```

**Characteristics:**
- Shorter pauses than `<break>`
- Less consistent than SSML
- Natural conversational feel

#### Ellipses (Hesitation)
```python
text = "I was thinking... maybe we could try something different."
```

**Characteristics:**
- Introduces pauses
- May add hesitation or nervousness to voice
- Less predictable than `<break>`

### SSML Limitations

**Caution:**
- ⚠️ Using **too many** `<break>` tags can cause:
  - AI speedup
  - Audio artifacts
  - Additional background noises
  - Generation instability

**Best Practice:**
- Use sparingly (2-4 breaks per generation)
- Keep pauses under 3 seconds
- Test with your specific voice

## SSML Support

### Supported Models

**SSML-Compatible Models:**
- Eleven English V1
- Eleven Flash V2
- Eleven Turbo V2
- Eleven Turbo V2.5

### SSML Features

#### Break Tags
```xml
<break time="1.5s" />
```

#### Phoneme Tags
```xml
<!-- CMU Arpabet -->
<phoneme alphabet="arp" ph="HH AH L OW">hello</phoneme>

<!-- International Phonetic Alphabet -->
<phoneme alphabet="ipa" ph="həˈloʊ">hello</phoneme>
```

#### Pronunciation Dictionaries

Available via API for unusual pronunciations:
- Phoneme replacements
- Alias replacements
- Custom pronunciation rules

### Enabling SSML

Ensure SSML parsing is enabled in API configuration:

```python
{
  "text": "Welcome <break time=\"1.0s\" /> to our service",
  "voice_id": "21m00Tcm4TlvDq8ikWAM",
  "model_id": "eleven_turbo_v2_5",
  "voice_settings": {
    "stability": 0.5,
    "similarity_boost": 0.75
  }
}
```

## Voice Settings Parameters

### API Endpoint

```
POST /v1/voices/{voice_id}/settings/edit
```

### Key Parameters

#### `stability` (0.0 - 1.0, default 0.5)
- **Lower values (0.0-0.4):** Broader emotional range, more variation
- **Higher values (0.6-1.0):** More consistent, potentially monotonous
- **Use case:** Adjust based on content type (expressive vs. neutral)

#### `similarity_boost` (0.0 - 1.0, default 0.75)
- **Lower values:** More creative interpretation
- **Higher values:** Closer adherence to original voice
- **Use case:** Balance authenticity vs. flexibility

#### `style` (0.0 - 1.0, default 0.0)
- **Higher values:** Exaggerate voice's natural style
- **Performance impact:** Increases computational cost and latency
- **Use case:** When vocal character is critical

#### `speed` (default 1.0)
- **< 1.0:** Slower speech (e.g., 0.8 = 80% speed)
- **> 1.0:** Faster speech (e.g., 1.2 = 120% speed)
- **Use case:** Adjust pacing for content type

#### `use_speaker_boost` (boolean, default true)
- **true:** Enhanced similarity to original speaker
- **false:** Reduced computational load
- **Performance impact:** Increases latency when enabled

### Example API Request

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(api_key="your-api-key")

audio = client.generate(
    text="[happy] Welcome to our service! <break time=\"0.5s\" /> How can I help you today?",
    voice="rachel",
    model="eleven_turbo_v2_5",
    voice_settings={
        "stability": 0.4,  # More emotional range
        "similarity_boost": 0.8,  # Stay close to voice
        "style": 0.2,  # Slight style exaggeration
        "speed": 1.0,  # Normal speed
        "use_speaker_boost": True
    }
)
```

## Code Examples

### Emotional Speech with Pauses

```python
#!/usr/bin/env python3
"""Example: Emotional TTS with pauses using elevenlabs-tty-tool."""

import subprocess

def synthesize_emotional_speech(text: str, voice: str = "rachel", output: str = None):
    """Synthesize emotional speech with pauses."""
    cmd = ["elevenlabs-tty-tool", "synthesize", text, "--voice", voice]

    if output:
        cmd.extend(["--output", output])

    subprocess.run(cmd, check=True)

# Example 1: Happy announcement with pauses
synthesize_emotional_speech(
    "[happy] Welcome to our platform! <break time=\"1.0s\" /> "
    "We're excited to have you here."
)

# Example 2: Sad message with hesitation
synthesize_emotional_speech(
    "[sad] I'm sorry to hear that... <break time=\"0.5s\" /> "
    "[resigned tone] We'll do our best to help.",
    output="sad_message.wav"
)

# Example 3: Excited announcement
synthesize_emotional_speech(
    "[excited] Amazing news! <break time=\"0.3s\" /> "
    "[cheerfully] Your project has been approved!",
    voice="adam"
)
```

### Voice Settings Control

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(api_key="your-api-key")

# Expressive narration (lower stability)
audio = client.generate(
    text="[curious] What could this mean? <break time=\"0.8s\" /> Let's find out.",
    voice="rachel",
    voice_settings={"stability": 0.3, "similarity_boost": 0.7}
)

# Calm, consistent voice (higher stability)
audio = client.generate(
    text="Please proceed to the main entrance.",
    voice="rachel",
    voice_settings={"stability": 0.8, "similarity_boost": 0.9}
)
```

## Best Practices

### Emotions
1. ✅ Place tags at phrase beginnings
2. ✅ Align text content with emotional intent
3. ✅ Use v3 models for best emotion support
4. ✅ Test combinations to find natural delivery
5. ❌ Don't overuse tags - let AI infer from context

### Pauses
1. ✅ Use SSML `<break>` for consistent results
2. ✅ Keep pauses under 3 seconds
3. ✅ Limit to 2-4 breaks per generation
4. ❌ Avoid excessive breaks (causes instability)
5. ❌ Don't rely solely on punctuation

### Voice Settings
1. ✅ Start with defaults, adjust incrementally
2. ✅ Lower stability for expressive content
3. ✅ Higher stability for professional narration
4. ✅ Test on target voice before production
5. ❌ Don't maximize all parameters (increases cost/latency)

## Sources

1. ElevenLabs Official Documentation (elevenlabs.io)
2. ElevenLabs API Reference (elevenlabs.io/docs/api-reference)
3. Community Best Practices (Reddit, Medium, jonathanmast.com)
4. SSML Specification (plushcap.com, vapi.ai)

## Updated: 2025-11-14

**Note:** Features and capabilities evolve. Check https://elevenlabs.io/docs for latest updates.
