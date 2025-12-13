# Fix Homebrew Formula for ttrans - Implementation Plan

## Overview

The ttrans Homebrew formula is currently non-functional because it's missing all Python dependency resource blocks. The `brew update-python-resources` command fails because MLX (and several other dependencies) only provide binary wheels on PyPI, not source distributions. This plan addresses how to fix the formula to properly install all dependencies.

## Current State Analysis

### What's Broken:
- The formula at `homebrew-ttrans/Formula/ttrans.rb` uses `virtualenv_install_with_resources` but has **zero resource blocks**
- Only ttrans itself is installed; none of its dependencies (numpy, mlx-whisper, textual, etc.) are present
- Any attempt to use ttrans beyond `--version` fails with `ModuleNotFoundError`

### Why It Broke:
- The plan (Phase 3, Step 4) called for running `brew update-python-resources` to generate resource blocks
- This command fails with: `Error: mlx exists on PyPI but lacks a suitable source distribution`
- MLX, torch, and other ML packages only distribute binary wheels, not source tarballs

### Key Discovery - mlx-lm Formula Pattern:
Homebrew core already has a working formula for an MLX-based Python app (`mlx-lm.rb`). Key patterns:
1. Uses `depends_on "mlx"` - MLX is available as a Homebrew formula that builds from source
2. Uses `depends_on "numpy"` - numpy is also a Homebrew formula
3. Uses `pypi_packages exclude_packages: %w[certifi mlx numpy]` to exclude formula-provided packages
4. Only includes resource blocks for packages that have source distributions
5. Does NOT require torch (mlx-lm uses pure MLX, unlike mlx-whisper)

### The Torch Problem:
ttrans depends on `mlx-whisper` which requires `torch`. Unlike MLX and numpy, torch is NOT available as a Homebrew formula for Python. The torch wheel is ~2GB and only available as binary wheels.

**Dependency chain:**
```
ttrans
└── mlx-whisper>=0.4.0
    ├── mlx>=0.11 (Homebrew formula exists ✓)
    ├── torch (NO source dist, NO Homebrew formula ✗)
    ├── numpy (Homebrew formula exists ✓)
    ├── scipy (has source dist ✓)
    ├── numba (has source dist ✓)
    └── ... other deps
```

## Desired End State

A user can install ttrans via Homebrew and have it fully functional:

```bash
brew tap adnichols/ttrans
brew install ttrans
ttrans --download-model base  # Works!
ttrans                        # Launches TUI!
```

### How to Verify:
1. Run `brew install adnichols/ttrans/ttrans` on a clean system
2. Run `ttrans --version` → shows "ttrans 0.1.0"
3. Run `ttrans --download-model tiny` → downloads model successfully
4. Run `ttrans` → launches TUI
5. Record and transcribe audio → works correctly

## What We're NOT Doing

**Explicitly out of scope:**
- Removing torch dependency from mlx-whisper (upstream project decision)
- Creating a Homebrew formula for torch (massive undertaking, not our project)
- Switching transcription engines to avoid torch (would break core functionality)
- Building from source on user machines (too slow, complex native deps)
- Adding all resource blocks manually (would need ~50+ blocks, maintenance nightmare)

## Implementation Approach

After researching options, the best approach is:

### Option A: Use `system` pip install (RECOMMENDED)

Instead of using `virtualenv_install_with_resources` (which requires source distributions), use Homebrew's virtualenv helper but let pip install dependencies from binary wheels:

```ruby
def install
  venv = virtualenv_create(libexec, "python3.12")
  venv.pip_install_and_link buildpath
end
```

This approach:
- Creates a virtualenv using Homebrew's Python
- Lets pip resolve and install all dependencies from PyPI (including binary wheels)
- Handles the ttrans package itself from the local build path
- Creates proper bin links

**Pros:**
- Works with binary-only packages (torch, mlx, etc.)
- No need to maintain 50+ resource blocks
- Uses pip's wheel cache for fast installs
- Same approach as non-Homebrew `pip install ttrans`

**Cons:**
- Less "pure" Homebrew approach (not fully reproducible from source)
- Homebrew auditor may complain (acceptable for personal tap)
- Network-dependent during install (pip downloads wheels)

### Option B: Hybrid approach with core dependencies as formulas

Use Homebrew formulas for packages that have them, pip for the rest:

```ruby
depends_on "mlx"
depends_on "numpy"

def install
  venv = virtualenv_create(libexec, "python3.12", system_site_packages: true)
  venv.pip_install_and_link buildpath
end
```

**Problem:** This doesn't work because:
- Homebrew's `mlx` formula provides C++ libraries, not Python bindings
- The Python `mlx` package needs to be installed in the virtualenv
- `system_site_packages: true` could cause conflicts

### Decision: Option A

We'll use the simple pip-based approach. This is acceptable for a personal tap and matches how users would install via pip.

---

## Phase 1: Update Homebrew Formula

### Overview
Replace the broken `virtualenv_install_with_resources` approach with a pip-based installation that handles binary wheels correctly.

### Changes Required:

#### 1. Update Formula
**Repository**: `homebrew-ttrans`
**File**: `Formula/ttrans.rb`

- [x] Updated formula to use `pip_install_and_link` approach

Replace the current formula with:

```ruby
class Ttrans < Formula
  include Language::Python::Virtualenv

  desc "macOS meeting transcription assistant with TUI"
  homepage "https://github.com/adnichols/ttrans"
  url "https://files.pythonhosted.org/packages/4b/92/3815fc1d250d8724088a645fcfb7fdcaa038de324be3bda91fb1304d01f0/ttrans-0.1.0.tar.gz"
  sha256 "5e3e6951a5585a110f9b938382178f2f998321bad7c844fecefdfe1e0587d90c"
  license "MIT"

  depends_on arch: :arm64      # Apple Silicon only (MLX requirement)
  depends_on macos: :monterey  # macOS 12.3+ (ScreenCaptureKit requirement)
  depends_on "portaudio"       # Required by sounddevice for audio capture
  depends_on "python@3.12"

  def install
    # Create virtualenv with Homebrew's Python
    venv = virtualenv_create(libexec, "python3.12")

    # Install ttrans and all dependencies via pip
    # This handles binary wheels (mlx, torch, etc.) that lack source distributions
    venv.pip_install_and_link buildpath
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
    # Test version output (doesn't require heavy dependencies)
    assert_match version.to_s, shell_output("#{bin}/ttrans --version")
  end
end
```

### Success Criteria:

#### Automated Verification:
- [x] Formula lints: `brew audit --strict adnichols/ttrans/ttrans` (may have warnings, should not have errors)
- [x] Formula installs: `brew install adnichols/ttrans/ttrans --build-from-source`
- [x] Test passes: `brew test adnichols/ttrans/ttrans`
- [x] Version check works: `ttrans --version` shows "ttrans 0.1.0"
- [x] Dependencies installed: `/opt/homebrew/Cellar/ttrans/0.1.0/libexec/bin/python -c "import numpy; import mlx_whisper; import textual; print('OK')"`

#### Manual Verification:
- [ ] `ttrans --download-model tiny` successfully downloads model
- [ ] `ttrans` launches TUI
- [ ] Recording and transcription work (requires permissions)

**Implementation Note**: After completing this phase and all automated verification passes, pause here for manual confirmation that the installation works correctly before proceeding to Phase 2.

---

## Phase 2: Test and Push Updated Formula

### Overview
Test the updated formula locally, then push to the homebrew-ttrans repository.

### Changes Required:

#### 1. Test Locally
```bash
# Uninstall current broken installation
brew uninstall ttrans

# Edit the formula
cd /opt/homebrew/Library/Taps/adnichols/homebrew-ttrans
# Apply changes from Phase 1

# Reinstall from local formula
brew install --build-from-source ./Formula/ttrans.rb

# Run tests
brew test ttrans
ttrans --version
ttrans --download-model tiny
```

#### 2. Push Changes
```bash
cd /opt/homebrew/Library/Taps/adnichols/homebrew-ttrans
git add Formula/ttrans.rb
git commit -m "Fix formula to use pip for binary wheel dependencies

The previous formula used virtualenv_install_with_resources without
any resource blocks, causing all dependencies to be missing.

brew update-python-resources fails because mlx and torch only provide
binary wheels, not source distributions.

This fix uses pip_install_and_link to let pip handle dependencies
from binary wheels, similar to a standard 'pip install ttrans'."

git push origin main
```

### Success Criteria:

#### Automated Verification:
- [ ] Changes committed to homebrew-ttrans repository
- [ ] Fresh `brew tap adnichols/ttrans && brew install ttrans` works on clean system
- [ ] `brew upgrade ttrans` works for users with old broken install

#### Manual Verification:
- [ ] Full TUI functionality verified on fresh install
- [ ] Recording and transcription work
- [ ] Settings persist across restarts

**Implementation Note**: After completing this phase and verification passes, proceed to update the original implementation plan to mark Phase 3 items as complete with notes about the fix.

---

## Phase 3: Update Original Plan Documentation

### Overview
Update the original implementation plan to document what was learned and the solution applied.

### Changes Required:

#### 1. Update Original Plan
**File**: `thoughts/plans/2025-12-07-NOD-311-homebrew-distribution.md`

Add a section after Phase 3 documenting:
- The issue encountered with `brew update-python-resources`
- The solution applied (pip-based installation)
- Updated manual verification results

### Success Criteria:

#### Automated Verification:
- [ ] Plan file updated with resolution notes

#### Manual Verification:
- [ ] Documentation accurately reflects what was done

---

## Testing Strategy

### Unit Tests:
- No new unit tests required
- Existing tests continue to work: `uv run pytest`

### Integration Tests:
The Homebrew formula test verifies basic functionality:
```ruby
test do
  assert_match version.to_s, shell_output("#{bin}/ttrans --version")
end
```

### Manual Testing Steps:
1. **Clean Install Test**:
   - Remove all ttrans files: `brew uninstall ttrans; brew untap adnichols/ttrans`
   - Fresh install: `brew tap adnichols/ttrans && brew install ttrans`
   - Verify: `ttrans --version`, `ttrans --download-model tiny`, `ttrans`

2. **Dependency Verification**:
   ```bash
   /opt/homebrew/Cellar/ttrans/0.1.0/libexec/bin/python -c "
   import numpy
   import mlx_whisper
   import textual
   import sounddevice
   import scipy
   import openai
   print('All dependencies installed correctly!')
   "
   ```

3. **Functional Test**:
   - Launch `ttrans`
   - Grant Screen Recording and Microphone permissions
   - Start recording
   - Speak some test audio
   - Stop recording
   - Verify transcript appears

## Performance Considerations

- **Installation time**: ~3-5 minutes (pip downloads ~2GB of wheels for torch, etc.)
- **Disk space**: ~2-3GB for all dependencies
- **First run**: Additional ~150MB model download (cached in `~/.cache/huggingface/`)

## Migration Notes

For users who installed the broken formula:
```bash
# Upgrade will reinstall with proper dependencies
brew upgrade ttrans

# Or if that fails, clean reinstall:
brew uninstall ttrans
brew install ttrans
```

## Alternative Approaches Considered

### 1. Manual Resource Blocks
**Rejected**: Would require 50+ resource blocks, high maintenance burden, still can't handle torch.

### 2. Depend on Homebrew MLX Formula
**Rejected**: Homebrew's `mlx` formula provides C++ libraries, not Python bindings. Would need custom install logic to bridge them.

### 3. Wait for Homebrew Python Wheel Support
**Rejected**: No timeline for this feature. Users need working formula now.

### 4. Switch to Different Transcription Engine
**Rejected**: Would require significant code changes, potentially worse performance.

### 5. Distribute as Cask (macOS app bundle)
**Future option**: Could bundle Python + all dependencies as a `.app`. More work but better user experience. Out of scope for v0.1.0.

## References

- Original implementation plan: `thoughts/plans/2025-12-07-NOD-311-homebrew-distribution.md`
- Working MLX formula example: https://github.com/Homebrew/homebrew-core/blob/master/Formula/m/mlx-lm.rb
- Homebrew Python virtualenv docs: https://docs.brew.sh/Python-for-Formula-Authors
- homebrew-ttrans repository: https://github.com/adnichols/homebrew-ttrans
