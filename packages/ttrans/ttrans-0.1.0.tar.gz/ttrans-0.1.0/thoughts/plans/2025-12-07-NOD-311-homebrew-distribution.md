# Homebrew Distribution for ttrans Implementation Plan

## Overview

Transform ttrans from a monolithic Python script into a properly packaged Python application distributed via Homebrew. This involves creating a Python package structure with CLI entry points, publishing to PyPI, and creating a Homebrew tap for easy installation via `brew install adnichols/ttrans/ttrans`.

## Current State Analysis

### What Exists Now:
- **Monolithic application**: `meeting_assistant.py` (2,329 lines) contains all functionality
- **Stub entry point**: `main.py:1-7` just prints "Hello from ttrans!"
- **Basic pyproject.toml**: Has dependencies but no build backend, entry points, or package metadata
- **No package structure**: No `ttrans/` directory exists
- **No CLI arguments**: No `--version` or `--download-model` flags
- **Model download**: Happens implicitly during `Transcriber.__init__()` via mlx-whisper
- **Configuration**: Already uses `~/.ttrans` TOML file with proper loading/saving

### Key Constraints:
- macOS-only (ScreenCaptureKit, PyObjC dependencies)
- Apple Silicon only (MLX requires Metal)
- macOS 12.3+ required (ScreenCaptureKit API)
- Python 3.11+ (uses tomllib)
- Models are 75MB-3GB (too large to bundle in Homebrew formula)

### Key Discoveries:
- **Model download already works**: `meeting_assistant.py:594-609` (`_warmup_model()`) triggers download
- **Config system is solid**: `meeting_assistant.py:1619-1699` handles TOML loading/saving properly
- **No argparse exists**: Need to add CLI argument handling from scratch
- **Research document is accurate**: PACKAGING.md referenced in research doesn't exist yet, but the plan outlined in the research doc is sound

## Desired End State

A user can install ttrans via Homebrew and run it as a CLI application:

```bash
# Installation
brew tap adnichols/ttrans
brew install ttrans

# Usage
ttrans                    # Launch TUI
ttrans --version          # Show version
ttrans --download-model base  # Pre-download a model
```

### How to Verify:
1. Fresh macOS system with Homebrew installed
2. Run `brew tap adnichols/ttrans`
3. Run `brew install ttrans`
4. Run `ttrans --version` → shows version number
5. Run `ttrans` → launches TUI with first-run model download
6. Models cached in `~/.cache/huggingface/`
7. Config created at `~/.ttrans`

## What We're NOT Doing

**Explicitly out of scope:**
- macOS `.app` bundle creation (cask distribution)
- Distribution to Homebrew core (this is a personal tap)
- Intel Mac support (Apple Silicon only)
- Support for older macOS versions (<12.3)
- Bundling ML models in the package/formula
- Windows/Linux support
- GUI first-run wizard (keeping console-based)
- PyPI package metadata optimization (basic metadata only)
- Automated version bumping via semantic-release (manual versioning)
- CI/CD for Homebrew formula updates (manual updates for now)

## Implementation Approach

We'll proceed in four phases:

1. **Package Restructuring**: Create Python package structure with CLI entry points
2. **PyPI Publication Setup**: Add metadata and publish to PyPI (needed for `brew update-python-resources`)
3. **Homebrew Tap Creation**: Create formula and tap repository
4. **Release & Testing**: Tag release, test installation, iterate

Each phase has clear success criteria (automated and manual) to ensure we can pause for validation before proceeding.

---

## Phase 1: Package Restructuring

### Overview
Create the `ttrans/` package directory with CLI entry points while keeping `meeting_assistant.py` as-is. Add build system configuration to `pyproject.toml`.

### Changes Required:

#### 1. Create Package Directory Structure
**New directory**: `ttrans/`

Create these files:

**File**: `ttrans/__init__.py`
```python
"""ttrans - macOS meeting transcription assistant with TUI."""

__version__ = "0.1.0"
```

**File**: `ttrans/cli.py`
```python
"""Command-line interface for ttrans."""

import argparse
import sys
from pathlib import Path


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="ttrans - macOS meeting transcription assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version=f"%(prog)s {get_version()}",
        help="Show version and exit",
    )
    parser.add_argument(
        "--download-model",
        choices=["tiny", "base", "small", "medium", "large", "turbo"],
        metavar="MODEL",
        help="Pre-download a Whisper model (tiny/base/small/medium/large/turbo) and exit",
    )

    args = parser.parse_args()

    # Handle model download
    if args.download_model:
        from ttrans.first_run import download_model_with_progress
        success = download_model_with_progress(args.download_model)
        sys.exit(0 if success else 1)

    # Check for first run and download default model if needed
    from ttrans.first_run import ensure_default_model
    ensure_default_model()

    # Launch the TUI
    from meeting_assistant import MeetingAssistantApp
    app = MeetingAssistantApp()
    app.run()


def get_version():
    """Get version from package."""
    try:
        from ttrans import __version__
        return __version__
    except ImportError:
        return "unknown"


if __name__ == "__main__":
    main()
```

**File**: `ttrans/first_run.py`
```python
"""First-run setup and model download handling."""

import sys
from pathlib import Path


def get_config_path():
    """Get the config file path."""
    return Path.home() / ".ttrans"


def is_first_run():
    """Check if this is the first time running ttrans."""
    return not get_config_path().exists()


def ensure_default_model():
    """Ensure the default model is downloaded on first run."""
    if is_first_run():
        print("Welcome to ttrans!")
        print("Downloading default Whisper model (base, ~150MB)...")
        print("This is a one-time setup. Future model changes can be made in settings.")
        print()
        download_model_with_progress("base")
        print()


def download_model_with_progress(model_size: str):
    """
    Download a Whisper model with progress indication.

    Args:
        model_size: One of "tiny", "base", "small", "medium", "large", "turbo"

    Returns:
        bool: True if successful, False otherwise
    """
    # Import here to avoid loading heavy dependencies if not needed
    try:
        import numpy as np
        import mlx_whisper
    except ImportError as e:
        print(f"Error: Required dependency not found: {e}", file=sys.stderr)
        return False

    # Model repository mapping (same as Transcriber class)
    HF_MODEL_REPOS = {
        "tiny": "mlx-community/whisper-tiny-mlx",
        "base": "mlx-community/whisper-base-mlx",
        "small": "mlx-community/whisper-small-mlx",
        "medium": "mlx-community/whisper-medium-mlx",
        "large": "mlx-community/whisper-large-v3-mlx",
        "turbo": "mlx-community/whisper-turbo",
    }

    model_repo = HF_MODEL_REPOS.get(model_size)
    if not model_repo:
        print(f"Error: Unknown model size '{model_size}'", file=sys.stderr)
        print(f"Available models: {', '.join(HF_MODEL_REPOS.keys())}", file=sys.stderr)
        return False

    model_sizes = {
        "tiny": "~75MB",
        "base": "~150MB",
        "small": "~500MB",
        "medium": "~1.5GB",
        "large": "~3GB",
        "turbo": "~150MB",
    }

    print(f"Downloading Whisper model: {model_size} ({model_sizes.get(model_size, 'unknown size')})")
    print(f"Repository: {model_repo}")
    print("This may take a few minutes depending on your connection...")
    print()

    try:
        # Create dummy audio to trigger model download
        # mlx-whisper downloads models automatically on first transcribe() call
        sample_rate = 16000
        dummy_audio = np.zeros(int(sample_rate * 0.1), dtype="float32")

        # This will download the model if not cached
        mlx_whisper.transcribe(
            dummy_audio,
            path_or_hf_repo=model_repo,
            word_timestamps=False,
        )

        print(f"✓ Model '{model_size}' downloaded successfully!")
        print(f"  Cached in: ~/.cache/huggingface/hub/")
        return True

    except Exception as e:
        print(f"Error downloading model: {e}", file=sys.stderr)
        return False
```

#### 2. Update pyproject.toml
**File**: `pyproject.toml`

Add build system, entry points, and package metadata:

```toml
[build-system]
requires = ["hatchling >= 1.26"]
build-backend = "hatchling.build"

[project]
name = "ttrans"
version = "0.1.0"
description = "macOS meeting transcription assistant with TUI"
readme = "README.md"
requires-python = ">=3.11"
license = "MIT"
authors = [
    {name = "Andrew Nichols", email = "adnichols@users.noreply.github.com"}
]

dependencies = [
    "mlx-whisper>=0.4.0",
    "numpy>=2.3.5",
    "openai>=2.8.1",
    "pyobjc>=12.1",
    "scipy>=1.11.0",
    "sounddevice>=0.5.3",
    "textual>=6.7.1",
    "tomli-w>=1.2.0",
]

classifiers = [
    "Development Status :: 4 - Beta",
    "Environment :: Console",
    "Intended Audience :: End Users/Desktop",
    "License :: OSI Approved :: MIT License",
    "Operating System :: MacOS :: MacOS X",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Multimedia :: Sound/Audio :: Capture/Recording",
    "Topic :: Multimedia :: Sound/Audio :: Speech",
]

keywords = ["transcription", "whisper", "macos", "tui", "meeting", "audio"]

[project.urls]
Homepage = "https://github.com/adnichols/ttrans"
Repository = "https://github.com/adnichols/ttrans"
"Bug Tracker" = "https://github.com/adnichols/ttrans/issues"

[project.scripts]
ttrans = "ttrans.cli:main"

[tool.hatch.build.targets.wheel]
packages = ["ttrans"]
# Include meeting_assistant.py at the package root so it can be imported
include = ["meeting_assistant.py"]

[dependency-groups]
dev = [
    "pytest>=9.0.1",
    "pytest-asyncio>=1.3.0",
    "ruff>=0.14.7",
]
```

#### 3. Create LICENSE File
**File**: `LICENSE`

Add MIT license text (replace with actual copyright holder):

```
MIT License

Copyright (c) 2025 Andrew Nichols

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

#### 4. Update README.md (Optional but Recommended)
**File**: `README.md`

Add installation instructions and basic usage. Minimum additions:

```markdown
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

## Requirements

- macOS 12.3+ (Monterey or later)
- Apple Silicon (M1, M2, M3, etc.)
- Python 3.11+
```

### Success Criteria:

#### Automated Verification:
- [x] Package builds successfully: `uv build`
- [x] Package installs locally in editable mode: `uv pip install -e .`
- [x] CLI entry point works: `ttrans --version` shows "ttrans 0.1.0"
- [x] Linting passes: `uv run ruff check .`
- [x] Existing tests still pass: `uv run pytest`
- [x] Type checking passes (if enabled): `uv run pyright` or `mypy`

#### Manual Verification:
- [ ] Running `ttrans` launches the TUI successfully
- [ ] First-run experience works: Delete `~/.ttrans` and `~/.cache/huggingface/`, run `ttrans`, verify model downloads with progress messages
- [ ] `ttrans --download-model tiny` successfully downloads the tiny model
- [ ] All existing functionality works (recording, transcription, settings, etc.)
- [ ] No regressions in TUI behavior

**Implementation Note**: After completing this phase and all automated verification passes, pause here for manual confirmation from the human that the manual testing was successful before proceeding to Phase 2.

---

## Phase 2: PyPI Publication Setup

### Overview
Publish the package to PyPI so that `brew update-python-resources` can auto-generate dependency resource blocks for the Homebrew formula.

### Prerequisites:
- [ ] PyPI account created at https://pypi.org
- [ ] TestPyPI account created at https://test.pypi.org
- [ ] Two-factor authentication enabled on both accounts

### Changes Required:

#### 1. Test Publication to TestPyPI
No code changes needed - just commands to run:

```bash
# Build distributions
uv build

# Publish to TestPyPI
uv publish --index testpypi

# Test installation from TestPyPI (in a new virtual environment)
uv venv test-env
source test-env/bin/activate
pip install --index-url https://test.pypi.org/simple/ \
    --extra-index-url https://pypi.org/simple \
    ttrans

# Verify it works
ttrans --version
deactivate
rm -rf test-env
```

**Note**: The `--extra-index-url` allows pip to fetch dependencies from real PyPI while getting ttrans from TestPyPI.

#### 2. Publish to PyPI
Once TestPyPI installation is verified:

```bash
# Publish to production PyPI
uv publish
```

**Authentication Options:**
- Interactive (uv will prompt for username/token)
- Via `~/.pypirc` file (see research doc for format)
- Via environment variable: `export UV_PUBLISH_TOKEN="pypi-yourtoken"`

#### 3. Verify PyPI Listing
Check the package page:
- URL: https://pypi.org/project/ttrans/
- Verify README renders correctly
- Check classifiers appear properly
- Confirm all metadata is accurate

### Success Criteria:

#### Automated Verification:
- [ ] `uv build` completes without errors
- [ ] `twine check dist/*` passes validation
- [ ] TestPyPI upload succeeds: `uv publish --index testpypi`
- [ ] Package installs from TestPyPI: `pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple ttrans`
- [ ] Production PyPI upload succeeds: `uv publish`
- [ ] Package installs from PyPI: `pip install ttrans`

#### Manual Verification:
- [ ] Package page renders correctly on https://pypi.org/project/ttrans/
- [ ] README displays properly with formatting
- [ ] Classifiers and keywords are correct
- [ ] Installation from PyPI works in a clean environment
- [ ] Installed package runs correctly: `ttrans --version` and `ttrans`

**Implementation Note**: After completing this phase and all automated verification passes, pause here for manual confirmation from the human that the manual testing was successful before proceeding to Phase 3.

---

## Phase 3: Homebrew Tap Creation

### Overview
Create a separate GitHub repository (`homebrew-ttrans`) with the Homebrew formula for ttrans.

### Prerequisites:
- [ ] ttrans published to PyPI (from Phase 2)
- [ ] GitHub release created with tarball (see steps below)
- [ ] Tarball SHA256 calculated

### Changes Required:

#### 1. Create GitHub Release
**In ttrans repository** (not the tap):

```bash
# Tag the release
git tag -a v0.1.0 -m "Initial release for Homebrew distribution"
git push origin v0.1.0

# Create GitHub release (using gh CLI)
gh release create v0.1.0 \
    --title "v0.1.0 - Initial Release" \
    --notes "First release with Homebrew support. See README for installation instructions."
```

#### 2. Calculate Tarball SHA256
```bash
# Download and hash the release tarball
curl -sL https://github.com/adnichols/ttrans/archive/refs/tags/v0.1.0.tar.gz | shasum -a 256
```

Save this SHA256 hash - you'll need it for the formula.

#### 3. Create homebrew-ttrans Repository
**New GitHub repository**: `homebrew-ttrans`

Create these files:

**File**: `README.md`
```markdown
# Homebrew Tap for ttrans

This is a Homebrew tap for [ttrans](https://github.com/adnichols/ttrans), a macOS meeting transcription assistant with TUI.

## Installation

```bash
brew tap adnichols/ttrans
brew install ttrans
```

## Requirements

- macOS 12.3+ (Monterey or later)
- Apple Silicon (M1/M2/M3)
- Screen Recording permission (for system audio capture)
- Microphone permission

## Usage

After installation:

```bash
# Launch the TUI
ttrans

# Show version
ttrans --version

# Pre-download a specific Whisper model
ttrans --download-model base
```

## Permissions

Grant the following permissions in System Settings > Privacy & Security:

1. **Screen Recording** - Add your terminal app (Terminal.app, iTerm2, etc.)
2. **Microphone** - Add your terminal app

## Models

On first run, ttrans will download the default Whisper model (~150MB). This is stored in `~/.cache/huggingface/`.

Available models:
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

Configuration file: `~/.ttrans` (TOML format)
Transcripts directory: `~/Documents/Transcripts/`

## Uninstall

```bash
brew uninstall ttrans
brew untap adnichols/ttrans
```

To also remove cached models and config:
```bash
rm -rf ~/.cache/huggingface/
rm ~/.ttrans
```
```

**File**: `Formula/ttrans.rb`

```ruby
class Ttrans < Formula
  include Language::Python::Virtualenv

  desc "macOS meeting transcription assistant with TUI"
  homepage "https://github.com/adnichols/ttrans"
  url "https://github.com/adnichols/ttrans/archive/refs/tags/v0.1.0.tar.gz"
  sha256 "REPLACE_WITH_ACTUAL_SHA256_FROM_STEP_2"
  license "MIT"

  depends_on "python@3.12"
  depends_on macos: :monterey  # macOS 12.3+
  depends_on arch: :arm64      # Apple Silicon only
  depends_on "portaudio"       # Required by sounddevice

  # Python dependencies will be added here by `brew update-python-resources`
  # Run this command after creating the formula:
  # brew update-python-resources adnichols/ttrans/ttrans

  def install
    virtualenv_install_with_resources
  end

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

  test do
    assert_match version.to_s, shell_output("#{bin}/ttrans --version")
  end
end
```

#### 4. Generate Python Resource Blocks
After creating the formula skeleton above, run this command to auto-generate resource blocks for all Python dependencies:

```bash
# Install homebrew-pypi-poet if not already installed
brew install homebrew-pypi-poet

# Generate resources (this reads from PyPI)
brew update-python-resources adnichols/ttrans/ttrans
```

This will add `resource` blocks to the formula for each dependency (mlx-whisper, numpy, openai, etc.).

**Note**: You'll need to manually add the generated resource blocks to `Formula/ttrans.rb` between the `depends_on` section and the `def install` method.

#### 5. Test Formula Locally
Before pushing to GitHub:

```bash
# Install from local formula
brew install --build-from-source ./Formula/ttrans.rb

# Test the installation
ttrans --version
brew test ttrans

# Audit the formula
brew audit --strict ttrans

# Uninstall (for testing reinstallation)
brew uninstall ttrans
```

#### 6. Push to GitHub
```bash
git init
git add README.md Formula/ttrans.rb
git commit -m "Initial formula for ttrans v0.1.0"
git remote add origin https://github.com/adnichols/homebrew-ttrans.git
git push -u origin main
```

### Success Criteria:

#### Automated Verification:
- [ ] Repository created: `https://github.com/adnichols/homebrew-ttrans`
- [ ] Formula lints successfully: `brew audit --strict ttrans`
- [ ] Formula installs: `brew install --build-from-source ./Formula/ttrans.rb`
- [ ] Test passes: `brew test ttrans`
- [ ] CLI works after install: `ttrans --version`

#### Manual Verification:
- [ ] On a fresh macOS system, `brew tap adnichols/ttrans` works
- [ ] `brew install ttrans` completes without errors
- [ ] `ttrans --version` shows correct version
- [ ] `ttrans` launches the TUI
- [ ] First-run model download works
- [ ] Caveats message displays correctly
- [ ] All dependencies install correctly (no missing system libraries)

**Implementation Note**: After completing this phase and all automated verification passes, pause here for manual confirmation from the human that the manual testing was successful before proceeding to Phase 4.

---

## Phase 4: Release & Testing

### Overview
Document the release process and test the complete installation workflow on a fresh system.

### Changes Required:

#### 1. Create Release Documentation
**File**: `RELEASING.md` (in ttrans repository)

```markdown
# Release Process

This document outlines the steps for releasing a new version of ttrans.

## Prerequisites

- [ ] All changes merged to main branch
- [ ] Tests passing locally and in CI
- [ ] PyPI account configured (API token or Trusted Publishing)
- [ ] Access to adnichols/homebrew-ttrans repository

## Release Steps

### 1. Update Version Number
Edit `ttrans/__init__.py`:
```python
__version__ = "0.2.0"  # Bump version
```

Edit `pyproject.toml`:
```toml
version = "0.2.0"  # Match __init__.py
```

### 2. Update CHANGELOG
Add release notes to CHANGELOG.md (create if doesn't exist):
```markdown
## [0.2.0] - 2025-12-XX

### Added
- New feature X
- New feature Y

### Changed
- Improvement to Z

### Fixed
- Bug fix for A
```

### 3. Commit Version Bump
```bash
git add ttrans/__init__.py pyproject.toml CHANGELOG.md
git commit -m "Bump version to 0.2.0"
git push origin main
```

### 4. Create Git Tag
```bash
git tag -a v0.2.0 -m "Release v0.2.0"
git push origin v0.2.0
```

### 5. Publish to PyPI
```bash
# Build fresh distributions
rm -rf dist/
uv build

# Check build
twine check dist/*

# Publish to PyPI
uv publish
```

### 6. Create GitHub Release
```bash
gh release create v0.2.0 \
    --title "v0.2.0" \
    --notes-file <(grep -A 20 "## \[0.2.0\]" CHANGELOG.md | head -n -1)
```

### 7. Update Homebrew Formula
```bash
# Calculate new tarball SHA
SHA=$(curl -sL https://github.com/adnichols/ttrans/archive/refs/tags/v0.2.0.tar.gz | shasum -a 256 | cut -d' ' -f1)
echo "New SHA256: $SHA"

# Clone homebrew-ttrans repo
cd ~/projects
git clone https://github.com/adnichols/homebrew-ttrans.git
cd homebrew-ttrans

# Update formula
sed -i '' "s|archive/refs/tags/v.*\.tar\.gz|archive/refs/tags/v0.2.0.tar.gz|" Formula/ttrans.rb
sed -i '' "s|sha256 \".*\"|sha256 \"$SHA\"|" Formula/ttrans.rb

# Test formula
brew install --build-from-source ./Formula/ttrans.rb
brew test ttrans
brew audit --strict ttrans

# If tests pass, commit and push
git add Formula/ttrans.rb
git commit -m "Update ttrans to v0.2.0"
git push origin main
```

### 8. Verify Installation
On a test system:
```bash
brew update
brew upgrade ttrans
ttrans --version  # Should show 0.2.0
```

## Post-Release

- [ ] Announce release (GitHub Discussions, social media, etc.)
- [ ] Monitor for installation issues
- [ ] Update documentation if needed
```

#### 2. Test Complete Installation Workflow
**On a fresh macOS system** (or a clean VM):

1. Install Homebrew (if not already installed)
2. Run through the user installation process
3. Verify all permissions and first-run experience
4. Document any issues or improvements needed

**Test script** (save as `test_homebrew_install.sh` in thoughts/):

```bash
#!/bin/bash
# Test Homebrew installation of ttrans on a fresh system

set -e

echo "Testing ttrans Homebrew installation..."
echo

# Check prerequisites
echo "1. Checking macOS version..."
OS_VERSION=$(sw_vers -productVersion)
echo "   macOS version: $OS_VERSION"

echo "2. Checking architecture..."
ARCH=$(uname -m)
if [ "$ARCH" != "arm64" ]; then
    echo "   ERROR: ttrans requires Apple Silicon (arm64), found: $ARCH"
    exit 1
fi
echo "   Architecture: $ARCH (Apple Silicon) ✓"

echo "3. Installing ttrans..."
brew tap adnichols/ttrans
brew install ttrans

echo "4. Verifying installation..."
if ! command -v ttrans &> /dev/null; then
    echo "   ERROR: ttrans command not found"
    exit 1
fi
echo "   ttrans command found ✓"

echo "5. Checking version..."
VERSION=$(ttrans --version)
echo "   Version: $VERSION ✓"

echo "6. Testing model download..."
ttrans --download-model tiny

echo
echo "All tests passed! ✓"
echo
echo "To test the TUI:"
echo "  1. Grant Screen Recording and Microphone permissions"
echo "  2. Run: ttrans"
```

### Success Criteria:

#### Automated Verification:
- [ ] RELEASING.md document created
- [ ] Test script executes without errors
- [ ] Formula audit passes: `brew audit --strict ttrans`
- [ ] Installation from tap works: `brew install adnichols/ttrans/ttrans`
- [ ] Version check works: `ttrans --version`

#### Manual Verification:
- [ ] Complete installation flow tested on fresh macOS system
- [ ] Permissions workflow tested (Screen Recording, Microphone)
- [ ] First-run model download works and displays progress
- [ ] All TUI screens function correctly
- [ ] Recording and transcription work
- [ ] Settings can be saved and loaded
- [ ] Transcript browser works
- [ ] AI chat feature works (with API key configured)
- [ ] Uninstallation works cleanly

**Implementation Note**: After completing this phase and all verification passes, the implementation is complete. Document any issues found during testing and create follow-up tickets for improvements.

---

## Testing Strategy

### Unit Tests:
- No new unit tests required (existing tests cover core functionality)
- Existing tests must continue passing: `uv run pytest`
- Consider adding integration test for CLI argument parsing

### Integration Tests:
- Test complete installation workflow on macOS 12.3+, 13.x, 14.x
- Test both Intel (should fail gracefully) and Apple Silicon
- Test with and without prior `~/.ttrans` config
- Test model download for all model sizes

### Manual Testing Steps:
1. **Fresh Installation Test**:
   - Start with clean macOS system (or VM)
   - Follow README installation instructions exactly
   - Verify all steps work as documented
   - Note any confusing error messages

2. **Permissions Test**:
   - Deny Screen Recording permission → verify graceful error
   - Deny Microphone permission → verify graceful error
   - Grant permissions → verify functionality works

3. **Model Download Test**:
   - Delete `~/.cache/huggingface/`
   - Run `ttrans` → verify first-run download works
   - Try each model size with `--download-model`
   - Verify disk space usage is as expected

4. **Upgrade Test**:
   - Install v0.1.0
   - Upgrade to v0.2.0 (future release)
   - Verify config is preserved
   - Verify cached models are reused

## Performance Considerations

- **Model download time**: Varies by connection speed (2-30 minutes for large models)
- **First launch delay**: 5-10 seconds for model initialization
- **Installation size**: ~500MB-1GB (depends on dependencies)
- **Homebrew install time**: 3-5 minutes (builds virtualenv, installs all deps)

**Optimizations**:
- Models cached in `~/.cache/huggingface/` are reused across upgrades
- Homebrew virtualenv is separate from system Python (no conflicts)
- Build artifacts are minimal (no compilation needed for most deps)

## Migration Notes

**For existing users** (if any used the old `main.py` entry point):
- Old command: `uv run python meeting_assistant.py`
- New command: `ttrans`
- Config file location unchanged: `~/.ttrans`
- Transcript directory unchanged: `~/Documents/Transcripts/`
- Cached models unchanged: `~/.cache/huggingface/`

**Migration script** (if needed):
```bash
# None needed - all paths are compatible
# Users can simply switch to `brew install ttrans`
```

## References

- Original research: `thoughts/research/2025-12-07-homebrew-packaging-mechanism.md`
- Linear ticket: `thoughts/linear/nod-311.md`
- Homebrew Formula Cookbook: https://docs.brew.sh/Formula-Cookbook
- Python Packaging Guide: https://packaging.python.org/
- PyPI Publishing Guide: https://packaging.python.org/en/latest/tutorials/packaging-projects/
- Homebrew Python Guide: https://docs.brew.sh/Python-for-Formula-Authors

## Future Enhancements (Out of Scope for v0.1.0)

These are ideas for future releases, not blockers for this implementation:

1. **Automated releases**: GitHub Actions workflow to auto-publish to PyPI and update Homebrew formula on tag push
2. **CI/CD for formula**: Automated testing of formula changes
3. **Homebrew core submission**: Submit to official Homebrew repo (requires popularity)
4. **macOS app bundle**: Create `.app` bundle for Cask distribution (GUI users)
5. **Intel support**: Investigate Whisper alternatives that work on Intel Macs
6. **Linux support**: Port to Linux with PulseAudio/PipeWire support
7. **Model management UI**: TUI screen for downloading/deleting models
8. **Automatic updates**: Check for new versions in the TUI
9. **Telemetry**: Opt-in usage statistics to improve the tool
