---
date: 2025-12-07T21:24:17Z
author: claude
git_commit: 46736547743b880e6a9569690f445dcb8df9d3be
branch: main
repository: ttrans
type: research
status: complete
tags: homebrew, packaging, distribution, python, macos
last_updated: 2025-12-07
---

# Research: Appropriate Mechanism for Homebrew Distribution

## Research Question

Review PACKAGING.md and research the appropriate mechanism for making ttrans available via Homebrew, focusing on:
- Current Homebrew best practices for Python applications (2024-2025)
- How to handle ML model downloads in Homebrew packages
- Platform-specific dependencies (macOS 12.3+, Apple Silicon)
- Personal tap distribution strategy

## Summary

The PACKAGING.md document contains a comprehensive and **accurate** plan for Homebrew distribution of ttrans. The research confirms that:

1. **Personal tap distribution** (`homebrew-ttrans`) is the correct approach for third-party applications
2. **Model download on first run** is appropriate - Homebrew formulas should not package large ML models
3. **Platform restrictions** (macOS 12.3+, Apple Silicon) are well-supported via `depends_on` directives
4. **Python package structure** outlined in PACKAGING.md aligns with Homebrew's `virtualenv_install_with_resources` pattern
5. **PyObjC frameworks** (ScreenCaptureKit, CoreMedia) work as regular Python dependencies

The main finding is that the current project structure (monolithic `meeting_assistant.py`) needs refactoring into a proper Python package before Homebrew distribution is possible.

## Detailed Findings

### 1. Current Project Structure

**Location:** `/Users/anichols/code/ttrans/`

**Current state:**
- No `ttrans/` package directory exists
- Application is a single 2,329-line file: `meeting_assistant.py`
- `main.py` is a 7-line stub
- No CLI entry points defined in `pyproject.toml`
- No build system configured

**Key files:**
- `meeting_assistant.py:1452` - `MeetingAssistantApp` class (main TUI)
- `meeting_assistant.py:553-560` - Whisper model repository definitions
- `meeting_assistant.py:1619-1699` - Config loading/saving (uses `~/.ttrans` TOML file)
- `pyproject.toml:1-24` - Minimal project metadata, no entry points or build backend

**Dependencies (from pyproject.toml:7-16):**
```toml
dependencies = [
    "mlx-whisper>=0.4.0",      # Local ML transcription
    "numpy>=2.3.5",
    "openai>=2.8.1",           # LLM API client
    "pyobjc>=12.1",            # macOS integration
    "scipy>=1.11.0",           # Signal processing
    "sounddevice>=0.5.3",      # Audio capture
    "textual>=6.7.1",          # TUI framework
    "tomli-w>=1.2.0",          # TOML config writing
]
```

### 2. Whisper Model Handling (Current Implementation)

**Model definitions:** `meeting_assistant.py:553-560`

```python
HF_MODEL_REPOS = {
    "tiny": "mlx-community/whisper-tiny-mlx",
    "base": "mlx-community/whisper-base-mlx",
    "small": "mlx-community/whisper-small-mlx",
    "medium": "mlx-community/whisper-medium-mlx",
    "large": "mlx-community/whisper-large-v3-mlx",
    "turbo": "mlx-community/whisper-turbo",
}
```

**Model loading:** `meeting_assistant.py:594-609` (`_warmup_model()`)
- Downloads model on first use via `mlx_whisper.transcribe()`
- Uses HuggingFace Hub's implicit caching (`~/.cache/huggingface/hub/`)
- No explicit first-run setup code exists
- Model size configurable via `~/.ttrans` config file (`WHISPER_MODEL` key)

**Model sizes:**
- tiny: ~75MB
- base: ~150MB (default)
- small: ~500MB
- medium: ~1.5GB
- large: ~3GB
- turbo: ~150MB

### 3. Homebrew Python Package Best Practices (2024-2025)

**Standard formula pattern:**
```ruby
class Ttrans < Formula
  include Language::Python::Virtualenv

  desc "macOS meeting transcription assistant with TUI"
  homepage "https://github.com/USERNAME/ttrans"
  url "https://github.com/USERNAME/ttrans/archive/refs/tags/v0.1.0.tar.gz"
  sha256 "PLACEHOLDER"
  license "MIT"

  depends_on "python@3.12"
  depends_on macos: :monterey  # macOS 12.3+
  depends_on arch: :arm64      # Apple Silicon only
  depends_on "portaudio"       # Required by sounddevice

  def install
    virtualenv_install_with_resources
  end

  test do
    assert_match version.to_s, shell_output("#{bin}/ttrans --version")
  end
end
```

**Key mechanisms:**

1. **`virtualenv_install_with_resources`**
   - Creates isolated virtualenv in formula's `libexec/`
   - Installs all declared resource blocks automatically
   - Symlinks executables from virtualenv to `bin/`
   - Prevents dependency conflicts between formulae

2. **Resource blocks** (generated via `brew update-python-resources`)
   - Each Python dependency requires a `resource` block
   - Contains PyPI URL and SHA256 hash
   - Auto-generated tool reads from `pyproject.toml` dependencies
   - Must have package published to PyPI

3. **Platform dependencies**
   - `depends_on macos: :monterey` - macOS 12.3+ (ScreenCaptureKit requirement)
   - `depends_on arch: :arm64` - Apple Silicon only (MLX/Metal requirement)
   - `depends_on "python@3.12"` - Specific Python version
   - `depends_on "portaudio"` - System library for sounddevice

### 4. Homebrew Tap Structure

**Repository naming requirement:** `homebrew-<tapname>`

For ttrans, create repository: `homebrew-ttrans`

**Structure:**
```
homebrew-ttrans/
├── README.md          # Installation instructions
└── Formula/
    └── ttrans.rb      # Homebrew formula
```

**User installation:**
```bash
brew tap USERNAME/ttrans
brew install ttrans
```

**Behind the scenes:**
- Clones `https://github.com/USERNAME/homebrew-ttrans`
- Formula name derived from filename: `ttrans.rb` → `ttrans`
- Tap name: `USERNAME/ttrans`

### 5. Model Download Strategy

**Research finding:** Homebrew's philosophy is "download everything during installation," BUT for ML models (75MB-3GB), the consensus is:

**Recommended approach:**
1. ✅ **Don't package models in formula** - too large for Homebrew ecosystem
2. ✅ **Download on first run** - let the application handle it
3. ✅ **Use `caveats` block** - inform users about first-run behavior
4. ✅ **Provide CLI option** - allow pre-download: `ttrans --download-model base`
5. ✅ **Use standard cache** - `~/.cache/huggingface/` is appropriate

**Example caveats block:**
```ruby
def caveats
  <<~EOS
    ttrans requires Screen Recording and Microphone permissions.

    Grant permissions in System Settings > Privacy & Security:
      1. Screen Recording - Add your terminal app
      2. Microphone - Add your terminal app

    On first run, ttrans will download the Whisper model (~150MB).
    This is stored in ~/.cache/huggingface/.

    Model sizes:
      tiny:   ~75MB   (fastest)
      base:   ~150MB  (default)
      small:  ~500MB
      medium: ~1.5GB
      large:  ~3GB

    To pre-download a model:
      ttrans --download-model base

    Config: ~/.ttrans
    Transcripts: ~/Documents/Transcripts/
  EOS
end
```

This approach is consistent with other ML tools in Homebrew (e.g., `whisper-cpp`).

### 6. Package Structure Requirements

**What needs to be created (per PACKAGING.md):**

```
ttrans/                      # New package directory
├── __init__.py              # Package marker with __version__ = "0.1.0"
├── cli.py                   # CLI entry point with main()
└── first_run.py             # Model download with progress
```

**What needs to be updated:**

`pyproject.toml` additions:
```toml
[project.scripts]
ttrans = "ttrans.cli:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["ttrans"]
include = ["meeting_assistant.py"]
```

**Entry point implementation:** `ttrans/cli.py`
```python
def main():
    import argparse
    parser = argparse.ArgumentParser(description="ttrans - macOS meeting transcription assistant")
    parser.add_argument("--version", "-v", action="store_true", help="Show version and exit")
    parser.add_argument("--download-model", choices=["tiny", "base", "small", "medium", "large", "turbo"])
    args = parser.parse_args()

    if args.version:
        from ttrans import __version__
        print(f"ttrans {__version__}")
        return

    if args.download_model:
        from ttrans.first_run import download_model_with_progress
        download_model_with_progress(args.download_model)
        return

    # First-run check and model download
    from ttrans.first_run import run_first_setup
    run_first_setup()

    # Launch TUI
    from meeting_assistant import MeetingAssistantApp
    app = MeetingAssistantApp()
    app.run()
```

### 7. Release Process

**Steps for first release:**

1. **Create package structure** (per PACKAGING.md)
2. **Tag version:**
   ```bash
   git tag -a v0.1.0 -m "Initial release"
   git push origin v0.1.0
   ```

3. **Create GitHub release** from the tag (with uploaded tarball for stable SHA)

4. **Get tarball SHA256:**
   ```bash
   curl -sL https://github.com/USERNAME/ttrans/archive/refs/tags/v0.1.0.tar.gz | shasum -a 256
   ```

5. **Create homebrew-ttrans repository** with formula

6. **Generate Python resources:**
   ```bash
   brew update-python-resources USERNAME/ttrans/ttrans
   ```

   This reads `pyproject.toml` and generates resource blocks for all dependencies.

7. **Test installation locally:**
   ```bash
   brew install --build-from-source ./Formula/ttrans.rb
   brew test ttrans
   brew audit --strict ttrans
   ```

8. **Push to tap repository**

### 8. Platform Restrictions Implementation

**For ttrans specifically:**

```ruby
# ScreenCaptureKit requires macOS 12.3+ (Monterey)
depends_on macos: :monterey

# MLX requires Apple Silicon (Metal acceleration)
depends_on arch: :arm64

# Python version
depends_on "python@3.12"

# System library for sounddevice
depends_on "portaudio"
```

**PyObjC frameworks:**
- Handled as regular Python dependencies in resource blocks
- `pyobjc-framework-ScreenCaptureKit`, `pyobjc-framework-CoreMedia`, etc.
- No special Homebrew handling required
- System compatibility checked at runtime

**User experience:**
- Users on Intel Macs get clear error: "ttrans is only supported on ARM architecture"
- Users on older macOS get clear error: "ttrans requires macOS 12.3 or later"

## Code References

### Current Implementation
- `meeting_assistant.py:1-2329` - Monolithic application (needs refactoring)
- `meeting_assistant.py:1452` - MeetingAssistantApp class
- `meeting_assistant.py:553-560` - HF_MODEL_REPOS dictionary
- `meeting_assistant.py:594-609` - _warmup_model() method (model download trigger)
- `meeting_assistant.py:1619-1699` - Config loading/saving methods
- `pyproject.toml:1-24` - Current minimal configuration
- `main.py:1-7` - Stub entry point (needs replacement)

### Configuration Files
- `~/.ttrans` - TOML config file (runtime)
- `~/.cache/huggingface/hub/` - Model cache directory (runtime)
- `~/Documents/Transcripts/` - Default transcript directory (runtime)

## Architecture Documentation

### Current Architecture
```
meeting_assistant.py (2,329 lines)
├── AudioEngine - Microphone capture via sounddevice
├── SystemAudioEngine - System audio via ScreenCaptureKit
├── AudioMixer - Combines audio sources
├── Transcriber - Wraps mlx-whisper
│   ├── HF_MODEL_REPOS (line 553)
│   ├── __init__() - Initialize model
│   ├── _warmup_model() - Trigger download (line 594)
│   └── transcribe_segment() - Run transcription
└── MeetingAssistantApp (line 1452) - Main TUI
    ├── SettingsScreen - Config UI
    ├── AudioSourceScreen - Source selection
    ├── TranscriptsScreen - Browse saved transcripts
    └── TranscriptViewerScreen - View individual transcripts
```

### Proposed Architecture (from PACKAGING.md)
```
ttrans/ (package)
├── __init__.py - Version info
├── cli.py - Entry point with argparse
│   ├── main() - CLI routing
│   ├── --version - Show version
│   ├── --download-model - Pre-download model
│   └── (default) - Launch TUI
└── first_run.py - Setup logic
    ├── check_first_run() - Check ~/.ttrans exists
    ├── download_model_with_progress() - Download with output
    └── run_first_setup() - Welcome message + model download

meeting_assistant.py - Imported by cli.py
└── (existing code unchanged)
```

### Homebrew Distribution Architecture
```
homebrew-ttrans/ (separate repository)
├── README.md - Installation instructions
└── Formula/
    └── ttrans.rb - Homebrew formula
        ├── url: GitHub release tarball
        ├── sha256: Tarball checksum
        ├── depends_on: Platform/system dependencies
        ├── resource blocks: Python dependencies (auto-generated)
        ├── install: virtualenv_install_with_resources
        ├── caveats: User guidance
        └── test: Version check
```

## Related Documents

- `/Users/anichols/code/ttrans/PACKAGING.md` - Complete packaging specification (already exists)
- `/Users/anichols/code/ttrans/CLAUDE.md` - Project overview and commands
- HOMEBREW_RESEARCH.md - Detailed Homebrew best practices (created during this research)

## Validation of PACKAGING.md

The existing PACKAGING.md document is **accurate and well-researched**. All recommendations align with current Homebrew best practices (2024-2025):

✅ **Correct:**
- Personal tap distribution strategy
- Python package structure (ttrans/ directory)
- Entry point configuration in pyproject.toml
- Model download on first run (not during brew install)
- Use of caveats block for user guidance
- Platform restrictions (depends_on macos:, arch:)
- virtualenv_install_with_resources pattern
- Resource block generation with brew update-python-resources
- CLI options (--version, --download-model)

❌ **Minor updates needed:**
- Python version: Formula shows `python@3.12` but pyproject.toml shows `>=3.11`
  - Recommendation: Use `python@3.12` in formula for consistency
- Build backend: PACKAGING.md suggests `hatchling`, which is appropriate
- PyObjC: Formula should depend on `pyobjc` package, which includes all frameworks

## Implementation Checklist

Based on this research, here's what needs to happen:

### Phase 1: Package Restructuring (in ttrans repository)
- [ ] Create `ttrans/` directory
- [ ] Create `ttrans/__init__.py` with `__version__ = "0.1.0"`
- [ ] Create `ttrans/cli.py` with `main()` function
- [ ] Create `ttrans/first_run.py` with model download logic
- [ ] Update `pyproject.toml` with entry points and build system
- [ ] Test package installation locally: `uv pip install -e .`
- [ ] Test CLI entry point: `ttrans --version`
- [ ] Update tests if needed

### Phase 2: Homebrew Tap Creation (new repository: homebrew-ttrans)
- [ ] Create GitHub repository: `homebrew-ttrans`
- [ ] Create `Formula/` directory
- [ ] Create `Formula/ttrans.rb` with formula skeleton
- [ ] Create README.md with installation instructions

### Phase 3: Release Process
- [ ] Tag version: `git tag -a v0.1.0 -m "Initial release"`
- [ ] Create GitHub release with tarball
- [ ] Calculate SHA256 of release tarball
- [ ] Update formula with URL and SHA256
- [ ] Generate resource blocks: `brew update-python-resources`
- [ ] Test local installation: `brew install --build-from-source`
- [ ] Test functionality: `ttrans --version`, `ttrans --download-model base`, `ttrans`
- [ ] Push to homebrew-ttrans repository

### Phase 4: User Testing
- [ ] Document installation process
- [ ] Test on fresh macOS system
- [ ] Verify permissions workflow
- [ ] Verify model download on first run
- [ ] Collect feedback

## Open Questions

1. **Python version:** Should formula use `python@3.12` or `python@3.11`?
   - pyproject.toml says `>=3.11`
   - PACKAGING.md formula shows `python@3.12`
   - **Recommendation:** Use `python@3.12` for stability (Homebrew norm)

2. **First-run UX:** Should model download block app launch or happen in background?
   - Current: Blocks during `_warmup_model()`
   - PACKAGING.md: Shows blocking with progress
   - **Research finding:** Blocking with progress is clearer UX

3. **Model selection:** Should users be able to change model after first run?
   - Current: Yes, via settings screen
   - PACKAGING.md: Doesn't address
   - **Current implementation:** Already supports this via `~/.ttrans` config

4. **PyPI publication:** Is PyPI publication required?
   - For `brew update-python-resources`: Yes, it reads from PyPI
   - For Homebrew distribution: No, can use GitHub tarball
   - **Decision needed:** Publish to PyPI for easier resource generation

5. **CI/CD:** Should formula be auto-updated on releases?
   - GitHub Actions can auto-update formula SHA256 on new releases
   - **Future enhancement:** Set up automation after manual process works

## Conclusion

The mechanism outlined in PACKAGING.md is **correct and ready for implementation**. The research confirms:

1. Personal tap (`homebrew-ttrans`) is the appropriate distribution method
2. Model download on first run is the right approach (not during brew install)
3. Platform restrictions are well-supported in Homebrew
4. The package structure is properly designed

**Blocker:** The current monolithic structure (`meeting_assistant.py`) must be refactored into a proper Python package with CLI entry points before Homebrew distribution is possible.

**Next step:** Implement Phase 1 (Package Restructuring) to create the `ttrans/` package structure as specified in PACKAGING.md.
