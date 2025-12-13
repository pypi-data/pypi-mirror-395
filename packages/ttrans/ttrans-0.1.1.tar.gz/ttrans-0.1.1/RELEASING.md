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

# Publish to PyPI (credentials from ~/.pypirc or UV_PUBLISH_* env vars)
export UV_PUBLISH_USERNAME="__token__"
export UV_PUBLISH_PASSWORD="your-pypi-token"
uv publish
```

### 6. Create GitHub Release

```bash
gh release create v0.2.0 \
    --title "v0.2.0" \
    --notes-file <(grep -A 20 "## \\[0.2.0\\]" CHANGELOG.md | head -n -1)
```

Or create release manually on GitHub with the CHANGELOG content.

### 7. Update Homebrew Formula

```bash
# Calculate new tarball SHA from PyPI
SHA=$(curl -sL https://files.pythonhosted.org/packages/source/t/ttrans/ttrans-0.2.0.tar.gz | shasum -a 256 | cut -d' ' -f1)
echo "New SHA256: $SHA"

# Clone homebrew-ttrans repo
cd ~/projects
git clone https://github.com/adnichols/homebrew-ttrans.git
cd homebrew-ttrans

# Update formula
# Edit Formula/ttrans.rb and update:
#   - url line to ttrans-0.2.0.tar.gz
#   - sha256 to the new SHA
# Use sed or edit manually

# Example with sed:
sed -i '' 's|ttrans-[0-9.]*\.tar\.gz|ttrans-0.2.0.tar.gz|' Formula/ttrans.rb
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

On a test system or clean environment:
```bash
brew update
brew upgrade ttrans
ttrans --version  # Should show 0.2.0
```

## Post-Release

- [ ] Announce release (GitHub Discussions, social media, etc.)
- [ ] Monitor for installation issues
- [ ] Update documentation if needed

## Troubleshooting

### PyPI Upload Fails

If upload fails with "File already exists":
- You cannot re-upload the same version
- Increment the version number and release again

### Homebrew Formula Fails to Install

1. Check the SHA256 matches: `shasum -a 256 dist/ttrans-X.Y.Z.tar.gz`
2. Verify the PyPI URL is accessible: `curl -I https://files.pythonhosted.org/packages/source/t/ttrans/ttrans-X.Y.Z.tar.gz`
3. Test locally: `brew install --build-from-source --verbose ./Formula/ttrans.rb`
4. Check logs: `brew install --build-from-source --debug ./Formula/ttrans.rb`

### Version Mismatch

If `ttrans --version` shows wrong version:
- Ensure `ttrans/__init__.py` and `pyproject.toml` match
- Clear build artifacts: `rm -rf dist/ build/ *.egg-info`
- Rebuild: `uv build`

## Quick Reference

```bash
# Full release in one go (after version bump and changelog)
git add . && git commit -m "Bump version to X.Y.Z"
git push origin main
git tag -a vX.Y.Z -m "Release vX.Y.Z"
git push origin vX.Y.Z
rm -rf dist/ && uv build && uv publish
gh release create vX.Y.Z --title "vX.Y.Z" --notes "Release notes here"

# Then update Homebrew formula in homebrew-ttrans repo
```
