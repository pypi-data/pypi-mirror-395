# ElevenLabs TTS Models - Complete Guide

This guide provides comprehensive information about all available ElevenLabs text-to-speech models, their capabilities, use cases, and recommendations for selecting the right model for your needs.

**Last Updated:** November 2025

## Table of Contents

- [Model Overview](#model-overview)
- [Current Generation Models](#current-generation-models)
- [Legacy Models (Deprecated)](#legacy-models-deprecated)
- [Model Comparison](#model-comparison)
- [Selection Guide](#selection-guide)
- [Pricing Considerations](#pricing-considerations)
- [Best Practices](#best-practices)

## Model Overview

ElevenLabs offers 8 TTS models across multiple generations:
- **4 Current Generation Models:** Actively developed, recommended for new projects
- **4 Legacy Models:** Deprecated, migrate to current generation for better performance

All models are available on the Free tier, though they have different character limits per generation.

## Current Generation Models

### 1. Eleven Turbo v2.5 (Default)

**Model ID:** `eleven_turbo_v2_5`

**Key Characteristics:**
- ⚡ Low latency: ~250ms
- 🌍 32 languages
- 📝 40,000 character limit per generation
- 💰 50% lower price per character
- ⭐ Current default model

**Technical Specs:**
- Response time: ~250-300ms
- Languages: All Multilingual v2 languages PLUS Hungarian, Norwegian, Vietnamese
- Max generation length: ~40 minutes of audio
- Pricing multiplier: 1x (standard)

**Best For:**
- General-purpose text-to-speech
- Developer applications prioritizing balanced quality and speed
- Projects requiring good quality without extreme low latency
- Cost-conscious projects with quality requirements

**Not Recommended For:**
- Real-time conversational AI (use Flash v2.5)
- Professional audiobooks (use Multilingual v2)
- Emotional expression (use v3)

**Usage:**
```bash
# Default - no need to specify model
elevenlabs-tty-tool synthesize "General purpose speech"

# Explicit usage
elevenlabs-tty-tool synthesize "Your text" --model eleven_turbo_v2_5
```

---

### 2. Eleven Multilingual v2

**Model ID:** `eleven_multilingual_v2`

**Key Characteristics:**
- 🎯 Highest production quality
- 🌍 29 languages
- 📝 10,000 character limit per generation
- 🏆 SDK-recommended default for professional use

**Technical Specs:**
- Response time: Medium latency (higher than Flash/Turbo)
- Languages: 29 including all major world languages
- Max generation length: ~10 minutes of audio
- Pricing multiplier: 1x (standard)

**Best For:**
- Professional content creation
- High-quality audiobooks and narration
- E-learning materials
- Marketing and promotional content
- Gaming voiceovers
- Multilingual projects requiring consistent quality

**Not Recommended For:**
- Real-time applications (use Flash v2.5)
- High-volume bulk processing (use Flash/Turbo v2.5)
- Emotional expression (use v3)

**Usage:**
```bash
elevenlabs-tty-tool synthesize "Professional presentation script" \
    --model eleven_multilingual_v2 \
    --voice rachel \
    --output professional.mp3
```

---

### 3. Eleven Flash v2.5

**Model ID:** `eleven_flash_v2_5`

**Key Characteristics:**
- ⚡⚡⚡ Ultra-low latency: ~75ms
- 🌍 32 languages (most of any model)
- 📝 40,000 character limit (largest)
- 💰 50% lower price per character

**Technical Specs:**
- Response time: ~75ms (excluding network/app latency)
- Languages: All Multilingual v2 languages PLUS Hungarian, Norwegian, Vietnamese
- Max generation length: ~40 minutes of audio
- Pricing multiplier: 1x (standard)

**Best For:**
- Real-time conversational AI agents
- Interactive voice applications
- Live customer service bots
- High-volume bulk processing
- Cost-sensitive projects requiring high throughput
- Applications where latency is critical

**Not Recommended For:**
- Professional audiobooks requiring highest quality (use Multilingual v2)
- Emotional expression (use v3)

**Special Considerations:**
- Requires text normalization workaround for phone numbers
- Enterprise customers can enable built-in normalization
- Slightly lower quality than Multilingual v2 (optimized for speed)

**Usage:**
```bash
# Real-time agent
elevenlabs-tty-tool synthesize "Quick response needed" \
    --model eleven_flash_v2_5 \
    --voice adam

# Bulk processing
cat large_text_file.txt | elevenlabs-tty-tool synthesize --stdin \
    --model eleven_flash_v2_5 \
    --output bulk_output.mp3
```

---

### 4. Eleven v3 (Alpha)

**Model ID:** `eleven_v3`

**Key Characteristics:**
- 🎭 Most emotionally expressive model
- 🌍 70+ languages (most language support)
- 📝 5,000 character limit
- 🔬 Alpha release (may have inconsistencies)
- 💰 2x cost (50% of normal minutes/tokens)

**Technical Specs:**
- Response time: Higher latency (not optimized for real-time)
- Languages: 70+ including all Multilingual v2 languages plus many more
- Max generation length: ~3 minutes of audio
- Pricing multiplier: 2x (double cost)

**Unique Features:**
- **Emotional Tags:** `[happy]`, `[sad]`, `[excited]`, `[angry]`, `[nervous]`, `[curious]`
- **Speech Characteristics:** `[whispers]`, `[laughs]`, `[gasps]`, `[sighs]`, `[pauses]`
- **Advanced Emotional Nuance:** `[cheerfully]`, `[playfully]`, `[mischievously]`, `[resigned tone]`, `[flatly]`, `[deadpan]`

**Best For:**
- Character dialogue with emotional depth
- Audiobooks requiring emotional expression
- Multi-speaker interactions
- Content where emotional nuance is critical
- Storytelling and narrative content

**Not Recommended For:**
- Real-time applications (high latency)
- High-volume processing (2x cost)
- Budget-conscious projects (unless emotional expression is essential)

**Important Notes:**
- Alpha status: May produce inconsistent results
- Generate multiple options and select the best one
- Higher latency than other models
- Emotional tags ONLY work with v3 (ignored on other models)

**Usage:**
```bash
# Basic emotional expression
elevenlabs-tty-tool synthesize "[happy] Welcome to our service!" \
    --model eleven_v3 \
    --voice rachel

# Complex emotional scene
elevenlabs-tty-tool synthesize \
    "[nervous] I don't know about this... [pauses] [resigned tone] But I guess we have no choice." \
    --model eleven_v3 \
    --voice charlotte \
    --output emotional_scene.mp3
```

---

## Legacy Models (Deprecated)

### Eleven Turbo v2
**Model ID:** `eleven_turbo_v2`
**Status:** Deprecated
**Replacement:** `eleven_turbo_v2_5`
**Migration Benefit:** 50% cost savings, larger character limit

### Eleven Flash v2
**Model ID:** `eleven_flash_v2`
**Status:** Deprecated
**Replacement:** `eleven_flash_v2_5`
**Migration Benefit:** 50% cost savings, more languages, larger character limit

### Eleven English v1 (Monolingual)
**Model ID:** `eleven_monolingual_v1`
**Status:** Deprecated
**Replacement:** `eleven_multilingual_v2`
**Migration Benefit:** Better quality, multilingual support

### Eleven Multilingual v1
**Model ID:** `eleven_multilingual_v1`
**Status:** Deprecated
**Replacement:** `eleven_multilingual_v2`
**Migration Benefit:** Better quality, more languages, more features

**Warning:** Legacy models will show deprecation warnings when used. Migrate to current generation models to ensure future compatibility and take advantage of improvements.

---

## Model Comparison

| Model | Latency | Languages | Char Limit | Price | Best For |
|-------|---------|-----------|------------|-------|----------|
| **v3 (Alpha)** | High | 70+ | 5,000 | 2x | Emotional expression |
| **Multilingual v2** | Medium | 29 | 10,000 | 1x | Highest quality |
| **Flash v2.5** | Ultra-low | 32 | 40,000 | 0.5x | Real-time, bulk |
| **Turbo v2.5** ⭐ | Low | 32 | 40,000 | 0.5x | General-purpose |

### Quality Ranking
1. **Multilingual v2** - Highest quality, most consistent
2. **Turbo v2.5** - High quality, balanced
3. **Flash v2.5** - Good quality, optimized for speed
4. **v3 (Alpha)** - Highest emotional quality, but inconsistent

### Speed Ranking
1. **Flash v2.5** - ~75ms (fastest)
2. **Turbo v2.5** - ~250ms (fast)
3. **Multilingual v2** - Medium
4. **v3 (Alpha)** - High latency (slowest)

### Cost Efficiency Ranking
1. **Flash v2.5** - 50% discount + largest char limit
2. **Turbo v2.5** - 50% discount + large char limit
3. **Multilingual v2** - Standard pricing
4. **v3 (Alpha)** - 2x cost (least cost-efficient)

---

## Selection Guide

### By Use Case

**Real-Time Conversational AI:**
- ✅ Primary: `eleven_flash_v2_5` (ultra-low latency)
- 🔄 Alternative: `eleven_turbo_v2_5` (if quality is more important)

**Professional Audiobooks:**
- ✅ Primary: `eleven_multilingual_v2` (highest quality)
- 🔄 Alternative: `eleven_v3` (if emotional expression is critical)

**E-Learning & Training:**
- ✅ Primary: `eleven_multilingual_v2` (professional quality)
- 🔄 Alternative: `eleven_turbo_v2_5` (if budget is a concern)

**Gaming & Character Dialogue:**
- ✅ Primary: `eleven_v3` (emotional expression)
- 🔄 Alternative: `eleven_multilingual_v2` (if emotions not critical)

**Claude Code Integration:**
- ✅ Primary: `eleven_flash_v2_5` (cost + speed)
- 🔄 Alternative: `eleven_turbo_v2_5` (default, balanced)

**Bulk Processing:**
- ✅ Primary: `eleven_flash_v2_5` (cost + throughput)
- 🔄 Alternative: `eleven_turbo_v2_5` (if quality is more important)

**Marketing & Promotional:**
- ✅ Primary: `eleven_multilingual_v2` (professional quality)
- 🔄 Alternative: `eleven_turbo_v2_5` (if budget is tight)

### By Priority

**Prioritize Quality:**
1. `eleven_multilingual_v2`
2. `eleven_turbo_v2_5`
3. `eleven_flash_v2_5`

**Prioritize Speed:**
1. `eleven_flash_v2_5`
2. `eleven_turbo_v2_5`
3. `eleven_multilingual_v2`

**Prioritize Cost:**
1. `eleven_flash_v2_5`
2. `eleven_turbo_v2_5`
3. `eleven_multilingual_v2`
4. `eleven_v3` (most expensive)

**Prioritize Emotion:**
1. `eleven_v3` (only model with emotional tags)
2. All other models (infer emotion from text)

---

## Pricing Considerations

### Model Cost Multipliers

| Model | Cost Multiplier | Minutes on Free Tier |
|-------|-----------------|----------------------|
| Flash v2.5 | 1x (50% discount) | ~20 minutes |
| Turbo v2.5 | 1x (50% discount) | ~20 minutes |
| Multilingual v2 | 1x (standard) | ~10 minutes |
| v3 (Alpha) | 2x (double cost) | ~5 minutes |

**Important:** v3 models consume characters/tokens at 2x the rate of other models. If you have 10,000 characters on the free tier:
- Flash/Turbo v2.5: ~10,000 characters usable
- Multilingual v2: ~10,000 characters usable
- v3: ~5,000 characters usable (same character count costs 2x)

### Cost Optimization Tips

1. **Use Flash v2.5 for high-volume work:**
   - 50% discount + largest char limit
   - Best price-to-performance ratio

2. **Reserve v3 for content that truly needs emotion:**
   - 2x cost means you get half the usage
   - Use Flash/Turbo for non-emotional content

3. **Default to Turbo v2.5 for general use:**
   - Balanced quality, speed, and cost
   - Good for most applications

4. **Use Multilingual v2 for professional deliverables:**
   - Worth the standard pricing for quality
   - Best for client-facing content

5. **Batch processing saves money:**
   - Use largest char limits (Flash/Turbo: 40K chars)
   - Fewer API calls = more efficient

---

## Best Practices

### Model Selection Best Practices

1. **Start with the default (Turbo v2.5):**
   - Good quality and speed for most use cases
   - Switch only if specific needs arise

2. **Test with your actual content:**
   - Different models may perform better with different text styles
   - Voice selection also affects output quality

3. **Use v3 sparingly:**
   - 2x cost means use only when emotional expression is essential
   - Generate multiple options due to alpha inconsistencies

4. **Consider latency requirements:**
   - Real-time: Flash v2.5 (<100ms critical)
   - Interactive: Turbo v2.5 (<500ms acceptable)
   - Batch: Multilingual v2 (latency not critical)

5. **Factor in language requirements:**
   - 70+ languages: v3 only
   - 32 languages: Flash/Turbo v2.5
   - 29 languages: Multilingual v2

### Emotional Expression Best Practices

**When using v3 with emotional tags:**

1. Place tags at the beginning of phrases
2. Align text content with emotional intent
3. Don't overuse - let AI infer when possible
4. Test with different voices
5. Generate multiple options (alpha inconsistencies)

**Example:**
```bash
# Good
elevenlabs-tty-tool synthesize "[happy] What wonderful news!" --model eleven_v3

# Avoid overuse
elevenlabs-tty-tool synthesize "[happy] What [excited] wonderful [cheerfully] news!" --model eleven_v3
```

### Migration from Legacy Models

If currently using deprecated models:

1. **From Turbo v2 → Turbo v2.5:**
   - Direct replacement, no functionality changes
   - 50% cost savings
   - Larger character limits

2. **From Flash v2 → Flash v2.5:**
   - Direct replacement, same use case
   - 50% cost savings
   - More languages

3. **From Monolingual v1 → Multilingual v2:**
   - Better quality
   - Multilingual support (even if only using English)
   - Modern feature support

4. **From Multilingual v1 → Multilingual v2:**
   - Significant quality improvement
   - More languages
   - Better consistency

**Migration is strongly recommended** - legacy models may be removed in future versions.

---

## Additional Resources

- **ElevenLabs Documentation:** https://elevenlabs.io/docs
- **Model API Reference:** https://elevenlabs.io/docs/api-reference/text-to-speech
- **Pricing Details:** https://elevenlabs.io/pricing
- **Voice Library:** https://elevenlabs.io/voice-library

**View models in CLI:**
```bash
elevenlabs-tty-tool list-models
```

**View pricing in CLI:**
```bash
elevenlabs-tty-tool pricing
```

---

**Last Updated:** November 2025
**Tool Version:** 0.2.0

For the latest model information, run `elevenlabs-tty-tool list-models` or visit https://elevenlabs.io/docs
