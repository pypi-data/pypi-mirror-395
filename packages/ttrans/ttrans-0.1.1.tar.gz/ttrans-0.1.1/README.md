# ttrans

A macOS meeting transcription assistant with a Terminal User Interface (TUI). Captures audio from microphone and/or system audio, transcribes speech using local ML models (Whisper via MLX), and generates AI-powered meeting summaries.

## Requirements

- macOS 12.3+ (Monterey or later)
- Apple Silicon (M1, M2, M3, etc.)
- Python 3.11+

## Installation

### From Homebrew (recommended)
```bash
brew tap adnichols/ttrans
brew install ttrans
```

### From Source
```bash
git clone https://github.com/adnichols/ttrans
cd ttrans
uv sync
uv run ttrans
```

## Usage

```bash
# Launch the TUI
ttrans

# Show version
ttrans --version

# Pre-download a specific model
ttrans --download-model small
```

## Permissions

ttrans requires the following macOS permissions:

1. **Screen Recording** - Add your terminal app (Terminal.app, iTerm2, etc.) in System Settings > Privacy & Security > Screen Recording
2. **Microphone** - Add your terminal app in System Settings > Privacy & Security > Microphone

## First Run

On first run, ttrans will download the default Whisper model (base, ~150MB). This is stored in `~/.cache/huggingface/`.

### Available Models

- `tiny`: ~75MB (fastest, less accurate)
- `base`: ~150MB (default, balanced)
- `small`: ~500MB
- `medium`: ~1.5GB
- `large`: ~3GB (slowest, most accurate)
- `turbo`: ~150MB

To pre-download a specific model:
```bash
ttrans --download-model small
```

## Configuration

- Configuration file: `~/.ttrans` (TOML format)
- Transcripts directory: `~/Documents/Transcripts/`

## Key Bindings

- `r` - Start recording
- `space` - Stop recording
- `s` - Settings
- `a` - Audio sources
- `t` - Transcript browser
- `d` - Focus device selector
- `j/k` - Scroll transcript
- `q` - Quit

## License

MIT License - see LICENSE file for details
