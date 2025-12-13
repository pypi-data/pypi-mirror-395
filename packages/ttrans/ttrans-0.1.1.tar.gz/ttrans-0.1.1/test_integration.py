"""
Integration tests for the transcription pipeline.

These tests use real audio files and the actual Whisper model to verify
that transcription is working correctly. They are slower than unit tests
and require the MLX models to be downloaded.

Run with: uv run pytest test_integration.py -v
         (run separately from unit tests to avoid mock conflicts)
"""

import sys
import pytest
import numpy as np
from pathlib import Path
import scipy.io.wavfile as wavfile

# Remove any mocks from unit tests to ensure we use real modules
for mod_name in list(sys.modules.keys()):
    if 'mlx_whisper' in mod_name:
        if hasattr(sys.modules[mod_name], '_mock_name'):
            del sys.modules[mod_name]

# Skip all tests if we can't import the required modules
pytest.importorskip("mlx_whisper")


class TestTranscriptionPipeline:
    """Integration tests for the full transcription pipeline."""

    @pytest.fixture(scope="class")
    def test_audio_path(self):
        """Path to the test audio file."""
        path = Path(__file__).parent / "test_data" / "test_speech.wav"
        if not path.exists():
            pytest.skip(f"Test audio file not found: {path}")
        return path

    @pytest.fixture(scope="class")
    def transcriber(self):
        """Create a real transcriber instance (cached for the class)."""
        # Ensure we have the real module, not a mock from unit tests
        for mod_name in list(sys.modules.keys()):
            if 'mlx_whisper' in mod_name:
                if hasattr(sys.modules[mod_name], '_mock_name'):
                    del sys.modules[mod_name]

        import mlx_whisper

        # Return a wrapper that mimics the Transcriber API
        class MLXWhisperWrapper:
            def __init__(self):
                self.model_repo = "mlx-community/whisper-tiny-mlx"

            def transcribe(self, audio_data):
                return mlx_whisper.transcribe(
                    audio_data,
                    path_or_hf_repo=self.model_repo,
                    word_timestamps=True,
                )

        return MLXWhisperWrapper()

    def load_audio_file(self, path: Path) -> np.ndarray:
        """Load audio file and convert to float32 normalized array."""
        sample_rate, audio_data = wavfile.read(path)

        # Convert to float32 and normalize
        if audio_data.dtype == np.int16:
            audio_data = audio_data.astype(np.float32) / 32768.0
        elif audio_data.dtype == np.int32:
            audio_data = audio_data.astype(np.float32) / 2147483648.0
        elif audio_data.dtype != np.float32:
            audio_data = audio_data.astype(np.float32)

        # Convert stereo to mono if needed
        if len(audio_data.shape) > 1:
            audio_data = audio_data.mean(axis=1)

        return audio_data, sample_rate

    def test_audio_file_exists_and_valid(self, test_audio_path):
        """Verify the test audio file exists and has valid content."""
        audio_data, sample_rate = self.load_audio_file(test_audio_path)

        assert sample_rate == 16000, f"Expected 16kHz, got {sample_rate}Hz"
        assert len(audio_data) > 0, "Audio file is empty"
        assert audio_data.dtype == np.float32, "Audio should be float32"

        # Check audio is normalized
        assert np.abs(audio_data).max() <= 1.0, "Audio should be normalized to [-1, 1]"

        # Should be at least 1 second of audio
        duration = len(audio_data) / sample_rate
        assert duration >= 1.0, f"Audio too short: {duration}s"

        print(f"\nTest audio: {duration:.2f}s, {sample_rate}Hz, max amplitude: {np.abs(audio_data).max():.3f}")

    def test_transcription_produces_output(self, test_audio_path, transcriber):
        """Test that transcription produces non-empty output."""
        audio_data, _ = self.load_audio_file(test_audio_path)

        result = transcriber.transcribe(audio_data)

        assert result is not None, "Transcription returned None"
        assert "text" in result, "Result missing 'text' field"
        assert len(result["text"].strip()) > 0, "Transcription is empty"

        print(f"\nTranscribed text: {result['text']}")

    def test_transcription_contains_expected_words(self, test_audio_path, transcriber):
        """Test that transcription contains expected words from the test audio."""
        audio_data, _ = self.load_audio_file(test_audio_path)

        result = transcriber.transcribe(audio_data)
        text = result["text"].lower()

        # The test audio says: "Hello, this is a test of the transcription system.
        # The quick brown fox jumps over the lazy dog."
        expected_words = ["hello", "test", "transcription", "quick", "brown", "fox", "dog"]

        found_words = [word for word in expected_words if word in text]
        missing_words = [word for word in expected_words if word not in text]

        print(f"\nTranscribed: {result['text']}")
        print(f"Found words: {found_words}")
        print(f"Missing words: {missing_words}")

        # Should find at least 5 of the 7 expected words
        assert len(found_words) >= 5, f"Only found {len(found_words)}/7 expected words: {found_words}"

    def test_audio_processing_pipeline(self, test_audio_path):
        """Test the audio processing functions used in SystemAudioEngine."""
        from scipy import signal

        audio_data, sample_rate = self.load_audio_file(test_audio_path)

        # Simulate what SystemAudioEngine._process_audio does
        # (it receives 48kHz stereo and converts to 16kHz mono)

        # First, let's create fake 48kHz stereo from our 16kHz mono
        upsampled = signal.resample(audio_data, len(audio_data) * 3)  # 16k -> 48k
        stereo = np.column_stack([upsampled, upsampled])  # Make stereo
        interleaved = stereo.flatten()  # Interleave channels

        # Now process it like SystemAudioEngine would
        # Deinterleave stereo to mono
        stereo_reshaped = interleaved.reshape(-1, 2)
        mono = stereo_reshaped.mean(axis=1)

        # Resample from 48kHz to 16kHz
        num_samples = int(len(mono) * 16000 / 48000)
        resampled = signal.resample(mono, num_samples).astype("float32")

        # Verify the processed audio is similar to original
        # (not exact due to resampling artifacts)
        assert len(resampled) > 0, "Processed audio is empty"
        assert resampled.dtype == np.float32, "Should be float32"

        # Length should be approximately the same as original
        length_ratio = len(resampled) / len(audio_data)
        assert 0.9 < length_ratio < 1.1, f"Length changed too much: {length_ratio}"

        print(f"\nOriginal: {len(audio_data)} samples")
        print(f"After processing: {len(resampled)} samples")
        print(f"Length ratio: {length_ratio:.3f}")


class TestAudioChunkHandling:
    """Test audio chunk handling with mixed dimensions."""

    def test_mixed_dimension_chunks(self):
        """Test that chunks with mixed dimensions are handled correctly."""
        # Simulate the issue from the error: some chunks 1D, some 2D
        chunk_1d = np.array([0.1, 0.2, 0.3, 0.4], dtype=np.float32)
        chunk_2d = np.array([[0.5], [0.6], [0.7]], dtype=np.float32)

        # This is what the fixed code does
        flattened_chunks = [
            np.asarray(chunk_1d).flatten(),
            np.asarray(chunk_2d).flatten(),
        ]

        result = np.concatenate(flattened_chunks)
        expected = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7], dtype=np.float32)

        np.testing.assert_array_almost_equal(result, expected)

    def test_stereo_to_mono_conversion(self):
        """Test stereo to mono conversion logic."""
        # Stereo interleaved audio (L R L R L R)
        stereo = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6], dtype=np.float32)

        # Convert to mono by averaging channels
        reshaped = stereo.reshape(-1, 2)
        mono = reshaped.mean(axis=1)

        expected = np.array([0.15, 0.35, 0.55], dtype=np.float32)
        np.testing.assert_array_almost_equal(mono, expected)


class TestSystemAudioSimulation:
    """Test system audio capture simulation."""

    def test_simulated_system_audio_flow(self, tmp_path):
        """Simulate the full system audio capture and transcription flow."""
        from scipy import signal
        import queue

        # Create a simple test tone (440Hz sine wave)
        sample_rate = 48000
        duration = 1.0
        t = np.linspace(0, duration, int(sample_rate * duration), dtype=np.float32)
        audio = 0.5 * np.sin(2 * np.pi * 440 * t)

        # Make stereo and interleave
        stereo = np.column_stack([audio, audio]).flatten()

        # Simulate chunks arriving (like from ScreenCaptureKit)
        chunk_size = 4800  # 0.1 seconds at 48kHz stereo
        audio_queue = queue.Queue()

        for i in range(0, len(stereo), chunk_size):
            chunk = stereo[i:i+chunk_size]

            # Process chunk (stereo -> mono, resample)
            if len(chunk) % 2 == 0:
                mono = chunk.reshape(-1, 2).mean(axis=1)
            else:
                mono = chunk

            # Resample 48kHz -> 16kHz
            target_samples = int(len(mono) * 16000 / 48000)
            if target_samples > 0:
                resampled = signal.resample(mono, target_samples).astype("float32")
                audio_queue.put(resampled)

        # Collect all chunks
        collected = []
        while not audio_queue.empty():
            chunk = audio_queue.get()
            collected.append(np.asarray(chunk).flatten())

        if collected:
            final_audio = np.concatenate(collected)

            # Verify we got roughly the right amount of audio
            expected_samples = int(duration * 16000)
            assert abs(len(final_audio) - expected_samples) < 100, \
                f"Expected ~{expected_samples} samples, got {len(final_audio)}"

            print(f"\nCollected {len(final_audio)} samples from {len(collected)} chunks")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
