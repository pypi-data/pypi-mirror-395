# TTS Pipeline Architecture

## AWS Polly TTS Pipeline

### Step 1: Text → Compressed Audio (AWS Polly)
```
Text → boto3.synthesize_speech() → audio_bytes (mp3/ogg_vorbis)
```
- **What happens**: AWS Polly converts text to speech and returns compressed audio data
- **Format**: Compressed audio stream (mp3 by default) as raw bytes
- **Dependencies**: Only requires boto3

### Step 2: Audio Bytes → Playback (pydub + ffmpeg)

#### For FILE OUTPUT (--output file.mp3):
```
audio_bytes → write to disk → Done! ✅
```
- **No pydub/ffmpeg needed**: Just write bytes directly to file
- **Works on Python 3.13+**: No playback libraries required

#### For SPEAKER PLAYBACK (default):
```
audio_bytes (compressed mp3)
  → pydub.AudioSegment (wrapper)
  → ffmpeg/ffplay (actual decoder)
  → PCM audio data
  → System audio device
  → Speakers 🔊
```

## Why We Need These Tools

### Why pydub?
- **Python has NO built-in audio playback** for compressed formats (mp3, ogg)
- pydub provides `play()` function for cross-platform audio playback
- It's a **wrapper/abstraction** - doesn't do the actual decoding

### Why ffmpeg?
- **Does the actual work**:
  1. Decodes compressed mp3 → raw PCM audio
  2. Sends PCM to system audio device (speakers)
- pydub calls `ffplay` (part of ffmpeg suite) behind the scenes
- Must be installed on system (`brew install ffmpeg` on macOS)

## The Problem
- **pydub uses Python's `audioop` module** (removed in Python 3.13)
- That's why we're stuck on Python 3.12
- The audio **playback** specifically requires this, not Polly synthesis

## Alternatives (for Python 3.13+ compatibility)

Could replace pydub with:
- **pygame**: Game library with audio support
- **sounddevice**: Professional audio I/O library
- **pyaudio**: Lower-level audio streaming
- **simpleaudio**: Minimal, but less cross-platform

All require **some system audio library** because Python has no native audio playback.

## Summary

### Why the complexity?
- Polly gives us compressed audio (efficient for network transfer)
- Playing compressed audio requires:
  1. Decoder (ffmpeg)
  2. Audio output interface (pydub/pygame/sounddevice)
- Python has neither built-in

### The simple path (no dependencies):
```bash
# This needs nothing except boto3 - no ffmpeg/pydub
aws-polly-tts-tool synthesize "Hello" --output speech.mp3
```

### The complex path (speaker playback):
```bash
# This needs boto3 + pydub + ffmpeg
aws-polly-tts-tool synthesize "Hello"  # plays through speakers
```

**Key Insight**: File output works everywhere, but speaker playback requires system audio dependencies.

## Component Responsibilities

| Component | Role | Required For |
|-----------|------|--------------|
| boto3 | AWS Polly API client | All operations |
| pydub | Audio playback abstraction | Speaker output only |
| ffmpeg/ffplay | Audio decoding & device I/O | Speaker output only |
| audioop (Python ≤3.12) | Audio operations for pydub | Speaker output only |

## Future Direction

To support Python 3.13+, we could:
1. Replace pydub with pygame/sounddevice
2. Add conditional imports based on Python version
3. Gracefully degrade to file-only output on Python 3.13+
