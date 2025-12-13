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
echo "   Note: This will download the tiny model (~75MB) for testing"
ttrans --download-model tiny

echo
echo "All tests passed! ✓"
echo
echo "To test the TUI:"
echo "  1. Grant Screen Recording and Microphone permissions"
echo "  2. Run: ttrans"
