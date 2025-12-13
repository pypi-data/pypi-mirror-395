# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ttrans is a macOS meeting transcription assistant with a TUI (Terminal User Interface). It captures audio from microphone and/or system audio, transcribes speech using local ML models (Whisper via MLX), and generates AI-powered meeting summaries.

## Commands

### Run the app
```bash
uv run python meeting_assistant.py
```

### Run tests
```bash
uv run pytest
uv run pytest test_meeting_assistant.py::TestAudioEngine  # specific test class
uv run pytest -k "test_initialization"  # pattern match
```

### Lint and format
```bash
uv run ruff check .
uv run ruff format .
```

### Install dependencies
```bash
uv sync
```

## Architecture

### Main Components (meeting_assistant.py)

**Audio Capture Layer:**
- `AudioEngine` - Captures microphone input via sounddevice
- `SystemAudioEngine` - Captures system/app audio via ScreenCaptureKit (macOS 12.3+)
- `AudioMixer` - Combines multiple audio sources into single stream for transcription

**Transcription:**
- `Transcriber` - Wraps lightning-whisper-mlx for on-device speech-to-text
- Uses a 30-second sliding buffer, transcribes periodically
- Includes hallucination detection for common Whisper artifacts

**TUI Screens (Textual framework):**
- `MeetingAssistantApp` - Main app with transcript view, controls, AI chat
- `SettingsScreen` - Configure API keys, LLM settings, transcript directory
- `AudioSourceScreen` - Toggle mic/system audio sources
- `TranscriptsScreen` - Browse, view, delete, move saved transcripts
- `TranscriptViewerScreen` - Full-screen markdown transcript viewer

**Configuration:**
- Config stored in `~/.ttrans` (TOML format)
- Supports: `OPENAI_API_KEY`, `LLM_BASE_URL`, `LLM_MODEL`, `TRANSCRIPT_DIR`, `LAST_DEVICE`
- Environment variables override file config

## Key Bindings (in main app)
- `r` - Start recording
- `space` - Stop recording
- `s` - Settings
- `a` - Audio sources
- `t` - Transcript browser
- `d` - Focus device selector
- `j/k` - Scroll transcript
- `q` - Quit

## Platform Requirements

- macOS only (uses ScreenCaptureKit, pyobjc)
- Screen Recording permission required for system audio capture
- Python 3.11+

## Testing Notes

Tests mock macOS-specific dependencies (ScreenCaptureKit, CoreMedia, pyobjc) to run on any platform. See `test_meeting_assistant.py` for mocking patterns.
