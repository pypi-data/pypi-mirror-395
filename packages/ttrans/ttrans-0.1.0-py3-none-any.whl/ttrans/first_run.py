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
        print("  Cached in: ~/.cache/huggingface/hub/")
        return True

    except Exception as e:
        print(f"Error downloading model: {e}", file=sys.stderr)
        return False
