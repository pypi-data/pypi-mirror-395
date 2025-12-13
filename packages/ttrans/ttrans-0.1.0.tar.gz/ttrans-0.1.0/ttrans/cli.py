"""Command-line interface for ttrans."""

import argparse
import sys


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
