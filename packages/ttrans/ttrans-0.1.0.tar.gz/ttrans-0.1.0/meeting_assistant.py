import time
import numpy as np
import sounddevice as sd
import queue
import os
import subprocess
import multiprocessing
import threading
from datetime import datetime
from pathlib import Path
import tomllib
import tomli_w
from scipy import signal

# ScreenCaptureKit imports for system audio capture
import ScreenCaptureKit as SCK
import CoreMedia
import objc
from Foundation import NSObject
from dispatch import dispatch_queue_create, DISPATCH_QUEUE_SERIAL

from textual.app import App, ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Header, Footer, Input, Button, Label, RichLog, Select, Checkbox, RadioButton, RadioSet, SelectionList, OptionList
from textual.widgets.option_list import Option
from textual.screen import Screen, ModalScreen
from textual.binding import Binding
from textual.command import Provider, Hit, DiscoveryHit
from textual import work

# Fix for multiprocessing error in TUI environments on macOS
try:
    multiprocessing.set_start_method("spawn", force=True)
except RuntimeError:
    pass

# Check if mlx-whisper is available
try:
    import mlx_whisper
except ImportError:
    print(
        "Error: mlx-whisper not installed. Please run 'uv add mlx-whisper'"
    )
    exit(1)

from openai import OpenAI

# --- Configuration Defaults ---
CONFIG_PATH = Path.home() / ".ttrans"


class AudioEngine:
    """Handles audio capture from a specific device."""

    def __init__(self, device_id, sample_rate=16000):
        self.device_id = device_id
        self.sample_rate = sample_rate
        self.queue = queue.Queue()
        self.stream = None
        self.running = False

    def callback(self, indata, frames, time, status):
        if status:
            pass  # In production, log status
        # Copy to queue to avoid blocking the audio thread
        self.queue.put(indata.copy())

    def start(self):
        self.running = True
        self.stream = sd.InputStream(
            device=self.device_id,
            channels=1,
            samplerate=self.sample_rate,
            callback=self.callback,
            dtype="float32",
        )
        self.stream.start()

    def stop(self):
        self.running = False
        if self.stream:
            self.stream.stop()
            self.stream.close()

    def get_audio_chunk(self):
        """Get all available audio from the queue."""
        data = []
        # Don't rely on queue.empty() - it's unreliable with cross-thread access
        # Just try get_nowait() until it raises Empty
        while True:
            try:
                chunk = self.queue.get_nowait()
                # Flatten each chunk to ensure consistent 1D arrays before concatenation
                data.append(np.asarray(chunk).flatten())
            except queue.Empty:
                break
        if not data:
            return None
        return np.concatenate(data, axis=0)


class SCStreamOutputDelegate(NSObject):
    """Delegate to receive audio sample buffers from ScreenCaptureKit."""

    def initWithCallback_(self, callback):
        self = objc.super(SCStreamOutputDelegate, self).init()
        if self is None:
            return None
        self._callback = callback
        return self

    def stream_didOutputSampleBuffer_ofType_(self, stream, sampleBuffer, outputType):
        """Called when a new sample buffer is available."""
        # SCStreamOutputType.audio = 1
        if outputType == 1:  # Audio
            self._callback(sampleBuffer)

    def stream_didStopWithError_(self, stream, error):
        """Called when the stream stops."""
        if error:
            print(f"Stream stopped with error: {error}")


class SystemAudioEngine:
    """Captures system audio using ScreenCaptureKit (macOS 12.3+)."""

    def __init__(self, sample_rate=48000, target_sample_rate=16000):
        self.sample_rate = sample_rate  # ScreenCaptureKit native rate
        self.target_sample_rate = target_sample_rate  # Whisper target rate
        self.queue = queue.Queue()
        self.stream = None
        self.running = False
        self.selected_apps = []  # Empty = all system audio
        self._delegate = None
        self._audio_queue = None
        self._content = None
        self._content_filter = None  # Keep reference to prevent GC
        self._stream_config = None   # Keep reference to prevent GC
        self._setup_complete = threading.Event()
        self._setup_error = None

    def get_available_apps(self, callback):
        """Asynchronously retrieve list of running applications with audio."""

        def completion_handler(content, error):
            if error:
                callback(None, str(error))
                return
            apps = []
            for app in content.applications():
                apps.append(
                    {
                        "bundle_id": app.bundleIdentifier(),
                        "name": app.applicationName(),
                        "process_id": app.processID(),
                    }
                )
            callback(apps, None)

        SCK.SCShareableContent.getShareableContentExcludingDesktopWindows_onScreenWindowsOnly_completionHandler_(
            True, False, completion_handler
        )

    def start(self, app_bundle_ids=None):
        """Start capturing system audio, optionally filtered to specific apps."""
        self.running = True
        self.selected_apps = app_bundle_ids or []
        self._setup_complete.clear()
        self._setup_error = None

        def on_content(content, error):
            if error:
                self._setup_error = str(error)
                self._setup_complete.set()
                return
            self._content = content
            self._setup_stream(content)

        SCK.SCShareableContent.getShareableContentWithCompletionHandler_(on_content)

        # Wait for async setup to complete (with timeout)
        self._setup_complete.wait(timeout=5.0)
        if self._setup_error:
            print(f"Error starting system audio capture: {self._setup_error}")
            self.running = False

    def _setup_stream(self, content):
        """Set up the SCStream with audio configuration."""
        try:
            # Get the first display (required even for audio-only)
            displays = content.displays()
            if not displays:
                self._setup_error = "No displays found"
                self._setup_complete.set()
                return
            display = displays[0]

            # Create content filter
            if self.selected_apps:
                # Filter to specific apps
                included_apps = [
                    app
                    for app in content.applications()
                    if app.bundleIdentifier() in self.selected_apps
                ]
                self._content_filter = SCK.SCContentFilter.alloc().initWithDisplay_includingApplications_exceptingWindows_(
                    display, included_apps, []
                )
            else:
                # Capture all system audio (exclude nothing)
                self._content_filter = (
                    SCK.SCContentFilter.alloc().initWithDisplay_excludingWindows_(
                        display, []
                    )
                )

            if self._content_filter is None:
                self._setup_error = "Failed to create content filter"
                self._setup_complete.set()
                return

            # Configure stream
            self._stream_config = SCK.SCStreamConfiguration.alloc().init()
            self._stream_config.setCapturesAudio_(True)
            self._stream_config.setExcludesCurrentProcessAudio_(True)  # Don't capture our own app
            self._stream_config.setSampleRate_(self.sample_rate)
            self._stream_config.setChannelCount_(2)  # Stereo

            # Minimize video capture (we only want audio)
            # Note: Some macOS versions require valid video dimensions
            self._stream_config.setWidth_(2)
            self._stream_config.setHeight_(2)
            self._stream_config.setMinimumFrameInterval_(CoreMedia.CMTimeMake(1, 1))  # 1 FPS
            self._stream_config.setShowsCursor_(False)
            self._stream_config.setPixelFormat_(0x42475241)  # 'BGRA' - kCVPixelFormatType_32BGRA

            # Create delegate BEFORE stream (need to pass to stream constructor)
            self._delegate = SCStreamOutputDelegate.alloc().initWithCallback_(
                self._handle_audio_buffer
            )

            # Create stream - pass delegate as 3rd param (required for callbacks to work!)
            self.stream = SCK.SCStream.alloc().initWithFilter_configuration_delegate_(
                self._content_filter, self._stream_config, self._delegate
            )

            if self.stream is None:
                self._setup_error = "Failed to create SCStream (stream is nil)"
                self._setup_complete.set()
                return

            # Create dispatch queue for audio
            self._audio_queue = dispatch_queue_create(
                b"com.ttrans.audio", DISPATCH_QUEUE_SERIAL
            )

            # Add audio output
            # Returns tuple: (success, error) in pyobjc
            result = self.stream.addStreamOutput_type_sampleHandlerQueue_error_(
                self._delegate,
                1,  # SCStreamOutputType.audio
                self._audio_queue,
                None,
            )

            # Handle tuple return from pyobjc
            success = result[0] if isinstance(result, tuple) else result
            if not success:
                self._setup_error = "Failed to add audio output to stream"
                self._setup_complete.set()
                return

            # Start capture
            def start_completion(error):
                if error:
                    self._setup_error = str(error)
                self._setup_complete.set()

            self.stream.startCaptureWithCompletionHandler_(start_completion)

        except Exception as e:
            self._setup_error = str(e)
            self._setup_complete.set()

    def _handle_audio_buffer(self, sample_buffer):
        """Process incoming CMSampleBuffer and extract audio data."""
        if not self.running:
            return

        audio_data = self._extract_audio_from_buffer(sample_buffer)
        if audio_data is not None:
            # Resample and convert to mono
            processed = self._process_audio(audio_data)
            if processed is not None and len(processed) > 0:
                self.queue.put(processed)

    def _extract_audio_from_buffer(self, sample_buffer):
        """Extract numpy array from CMSampleBuffer."""
        try:
            # Get the audio buffer list
            block_buffer = CoreMedia.CMSampleBufferGetDataBuffer(sample_buffer)
            if block_buffer is None:
                return None

            # Get data length
            length = CoreMedia.CMBlockBufferGetDataLength(block_buffer)
            if length == 0:
                return None

            # pyobjc handles output buffers automatically - pass None and it returns the data
            # Returns tuple: (status, data_bytes)
            result = CoreMedia.CMBlockBufferCopyDataBytes(
                block_buffer, 0, length, None
            )

            # Handle the result - could be (status, data) tuple or just status
            if isinstance(result, tuple):
                status, data = result[0], result[1]
                if status != 0:
                    return None
            else:
                # If result is just the status, the API didn't return data
                return None

            if data is None or len(data) == 0:
                return None

            # Convert bytes to numpy array (float32 stereo)
            audio_array = np.frombuffer(data, dtype=np.float32)
            return audio_array

        except Exception as e:
            # Log exception for debugging
            import sys
            print(f"Audio extraction error: {e}", file=sys.stderr)
            return None

    def _process_audio(self, audio_data):
        """Resample 48kHz stereo to 16kHz mono."""
        try:
            # Deinterleave stereo to mono by averaging channels
            if len(audio_data) >= 2:
                # Reshape to stereo and take mean
                if len(audio_data) % 2 == 0:
                    stereo = audio_data.reshape(-1, 2)
                    mono = stereo.mean(axis=1)
                else:
                    mono = audio_data
            else:
                mono = audio_data

            # Resample from 48kHz to 16kHz using scipy
            if self.sample_rate != self.target_sample_rate and len(mono) > 0:
                num_samples = int(len(mono) * self.target_sample_rate / self.sample_rate)
                if num_samples > 0:
                    resampled = signal.resample(mono, num_samples)
                else:
                    return None
            else:
                resampled = mono

            return resampled.astype("float32")

        except Exception:
            return None

    def stop(self):
        """Stop the capture stream."""
        self.running = False
        if self.stream:

            def stop_completion(error):
                pass

            try:
                self.stream.stopCaptureWithCompletionHandler_(stop_completion)
            except Exception:
                pass
            self.stream = None

    def get_audio_chunk(self):
        """Get all available audio from the queue."""
        data = []
        # Don't rely on queue.empty() - it's unreliable with cross-thread access
        # from pyobjc dispatch queues. Just try get_nowait() until Empty.
        while True:
            try:
                chunk = self.queue.get_nowait()
                # Flatten each chunk to ensure consistent 1D arrays before concatenation
                data.append(np.asarray(chunk).flatten())
            except queue.Empty:
                break
        if not data:
            return None
        return np.concatenate(data)


class AudioMixer:
    """Mixes audio from multiple sources into a single stream."""

    def __init__(self, sample_rate=16000):
        self.sample_rate = sample_rate
        self.sources = {}  # name -> {'engine': engine, 'gain': gain}
        self._lock = threading.Lock()

    def add_source(self, name, engine, gain=1.0):
        """Add an audio source (AudioEngine or SystemAudioEngine)."""
        with self._lock:
            self.sources[name] = {"engine": engine, "gain": gain}

    def remove_source(self, name):
        """Remove an audio source."""
        with self._lock:
            if name in self.sources:
                del self.sources[name]

    def get_mixed_audio(self):
        """Get mixed audio from all active sources."""
        chunks = []

        with self._lock:
            for name, source_data in self.sources.items():
                engine = source_data["engine"]
                gain = source_data["gain"]

                if engine.running:
                    chunk = engine.get_audio_chunk()
                    if chunk is not None and len(chunk) > 0:
                        # Apply gain
                        if gain != 1.0:
                            chunk = chunk * gain
                        chunks.append(chunk)

        if not chunks:
            return None

        # Find the maximum length
        max_len = max(len(c) for c in chunks)

        # Pad shorter chunks and mix
        mixed = np.zeros(max_len, dtype="float32")
        for chunk in chunks:
            padded = np.pad(chunk, (0, max_len - len(chunk)), mode="constant")
            mixed += padded

        # Use simple clipping instead of averaging to preserve volume
        # Averaging (div by N) attenuates signals when other sources are silent
        mixed = np.clip(mixed, -1.0, 1.0)

        return mixed


class PermissionManager:
    """Handles macOS permission requests for screen/audio capture."""

    @staticmethod
    def check_screen_recording_permission():
        """Check if screen recording permission is granted."""
        result = {"granted": False, "checked": False}

        def completion_handler(content, error):
            result["checked"] = True
            if error:
                # -3801 = SCStreamErrorUserDeclined
                error_code = error.code() if hasattr(error, "code") else -1
                result["granted"] = error_code != -3801
            else:
                result["granted"] = content is not None

        SCK.SCShareableContent.getShareableContentWithCompletionHandler_(
            completion_handler
        )

        # Wait for async completion (with timeout)
        for _ in range(50):  # 5 second timeout
            if result["checked"]:
                break
            time.sleep(0.1)

        return result["granted"]

    @staticmethod
    def request_screen_recording_permission():
        """Open System Preferences to Screen Recording permission pane."""
        subprocess.run(
            [
                "open",
                "x-apple.systempreferences:com.apple.preference.security?Privacy_ScreenCapture",
            ]
        )


class VADProcessor:
    """Voice Activity Detection for smart transcription triggering."""

    def __init__(self, threshold: float = 0.01, min_speech_ms: int = 250, min_silence_ms: int = 500):
        """
        Args:
            threshold: RMS threshold to detect speech
            min_speech_ms: Minimum speech duration to trigger processing
            min_silence_ms: Silence duration to finalize segment
        """
        self.threshold = threshold
        self.min_speech_samples = int(min_speech_ms * 16)  # 16 samples/ms at 16kHz
        self.min_silence_samples = int(min_silence_ms * 16)
        self.speech_samples = 0
        self.silence_samples = 0
        self.is_speaking = False

    def process_chunk(self, audio_chunk: np.ndarray) -> tuple[bool, bool]:
        """
        Process audio chunk and determine transcription triggers.

        Returns:
            (should_transcribe, should_commit):
                - should_transcribe: Start/continue transcription
                - should_commit: Finalize and commit current segment
        """
        rms = np.sqrt(np.mean(audio_chunk ** 2))
        has_speech = rms > self.threshold

        should_transcribe = False
        should_commit = False

        if has_speech:
            self.speech_samples += len(audio_chunk)
            self.silence_samples = 0
            if self.speech_samples >= self.min_speech_samples:
                self.is_speaking = True
                should_transcribe = True
        else:
            if self.is_speaking:
                self.silence_samples += len(audio_chunk)
                if self.silence_samples >= self.min_silence_samples:
                    should_commit = True
                    self.reset()
                else:
                    # Still in speech segment, keep transcribing
                    should_transcribe = True

        return should_transcribe, should_commit

    def reset(self):
        """Reset VAD state for new segment."""
        self.speech_samples = 0
        self.silence_samples = 0
        self.is_speaking = False


class Transcriber:
    """Handles local transcription using mlx-whisper with word-level timestamps."""

    HF_MODEL_REPOS = {
        "tiny": "mlx-community/whisper-tiny-mlx",
        "base": "mlx-community/whisper-base-mlx",
        "small": "mlx-community/whisper-small-mlx",
        "medium": "mlx-community/whisper-medium-mlx",
        "large": "mlx-community/whisper-large-v3-mlx",
        "turbo": "mlx-community/whisper-turbo",
    }

    def __init__(
        self,
        model_size: str = "base",
        model_path: str | None = None,
        word_timestamps: bool = True,
        max_buffer_seconds: float = 10.0,
    ):
        """
        Initialize transcriber with mlx-whisper.

        Args:
            model_size: One of "tiny", "base", "small", "medium", "large", "turbo"
            model_path: Optional local path to model directory (overrides model_size)
            word_timestamps: Enable word-level timestamp extraction
            max_buffer_seconds: Maximum buffer duration before forced transcription
        """
        if model_path:
            self.model_repo = model_path
        else:
            self.model_repo = self.HF_MODEL_REPOS.get(model_size, self.HF_MODEL_REPOS["base"])

        self.word_timestamps = word_timestamps
        self.max_buffer_seconds = max_buffer_seconds
        self.buffer = np.array([], dtype="float32")
        self.sample_rate = 16000
        self.model_ready = False
        self.model_error: str | None = None

        # Pre-download and load the model during initialization
        # This ensures the model is ready before recording starts
        self._warmup_model()

    def _warmup_model(self):
        """Download and load the model by running a minimal transcription."""
        self.model_ready = False
        self.model_error = None
        # Create 0.1 seconds of silence - enough to trigger model load
        dummy_audio = np.zeros(int(self.sample_rate * 0.1), dtype="float32")
        try:
            mlx_whisper.transcribe(
                dummy_audio,
                path_or_hf_repo=self.model_repo,
                word_timestamps=False,  # Faster for warmup
            )
            self.model_ready = True
        except Exception as e:
            self.model_error = str(e)
            self.model_ready = False

    def process_audio(self, new_data):
        """Append new audio to buffer with configurable max duration."""
        if new_data is None:
            return None

        self.buffer = np.concatenate((self.buffer, new_data))

        # Buffer limit based on max_buffer_seconds
        max_buffer = int(self.max_buffer_seconds * self.sample_rate)
        if len(self.buffer) > max_buffer:
            self.buffer = self.buffer[-max_buffer:]

        return self.buffer

    def transcribe_segment(self, audio_data: np.ndarray) -> dict:
        """
        Transcribe audio segment with word-level timestamps.

        Returns:
            dict with keys:
                - "text": Full transcribed text
                - "words": List of {"word": str, "start": float, "end": float}
                - "segments": Raw segment data from mlx-whisper
        """
        result = mlx_whisper.transcribe(
            audio_data,
            path_or_hf_repo=self.model_repo,
            word_timestamps=self.word_timestamps,
        )

        # Extract word-level data
        words = []
        if self.word_timestamps and "segments" in result:
            for segment in result["segments"]:
                for word_info in segment.get("words", []):
                    words.append({
                        "word": word_info.get("word", ""),
                        "start": word_info.get("start", 0.0),
                        "end": word_info.get("end", 0.0),
                    })

        return {
            "text": result.get("text", "").strip(),
            "words": words,
            "segments": result.get("segments", []),
        }

    def transcribe_text_only(self, audio_data: np.ndarray) -> str:
        """Legacy compatibility: return just the text."""
        result = self.transcribe_segment(audio_data)
        return result["text"]

    def clear_buffer(self):
        """Reset the audio buffer."""
        self.buffer = np.array([], dtype="float32")


class SettingsScreen(ModalScreen):
    CSS = """
    SettingsScreen {
        align: center middle;
    }

    #dialog {
        grid-size: 2;
        grid-gutter: 1 2;
        grid-rows: auto;
        padding: 0 1;
        width: 60;
        height: auto;
        border: thick $background 80%;
        background: $surface;
        overflow-y: auto;
    }

    #dialog_title {
        column-span: 2;
        height: 1;
        width: 100%;
        content-align: center middle;
        text-style: bold;
    }

    Label {
        column-span: 2;
        height: 1;
        margin-top: 1;
    }

    Input {
        column-span: 2;
        width: 100%;
    }

    Select {
        column-span: 2;
        width: 100%;
    }

    Button {
        width: 100%;
        margin-top: 1;
    }
    """

    BINDINGS = [
        Binding("escape", "cancel", "Cancel"),
    ]

    def __init__(self, api_key, base_url, model, transcript_dir, whisper_model, transcribe_interval, vad_threshold, whisper_model_path="", max_buffer_seconds=10.0):
        super().__init__()
        self.initial_api_key = api_key
        self.initial_base_url = base_url or ""
        self.initial_model = model
        self.initial_transcript_dir = str(transcript_dir) if transcript_dir else ""
        self.initial_whisper_model = whisper_model
        self.initial_transcribe_interval = str(transcribe_interval)
        self.initial_vad_threshold = str(vad_threshold)
        self.initial_whisper_model_path = whisper_model_path or ""
        self.initial_max_buffer_seconds = str(max_buffer_seconds)

    def compose(self) -> ComposeResult:
        with Container(id="dialog"):
            yield Label("Settings", id="dialog_title")

            yield Label("OpenAI API Key")
            yield Input(self.initial_api_key, password=True, id="api_key")

            yield Label("LLM Base URL (optional)")
            yield Input(self.initial_base_url, placeholder="http://localhost:11434/v1", id="base_url")

            yield Label("LLM Model Name")
            yield Input(self.initial_model, id="model")

            yield Label("Transcript Directory")
            yield Input(self.initial_transcript_dir, placeholder="~/Documents/Transcripts", id="transcript_dir")

            yield Label("Whisper Model Size (Requires Restart)")
            yield Select(
                [(x, x) for x in ["tiny", "small", "base", "medium", "large", "turbo"]],
                value=self.initial_whisper_model,
                id="whisper_model"
            )

            yield Label("Whisper Model Path (optional, overrides size)")
            yield Input(self.initial_whisper_model_path, placeholder="/path/to/local/model or HF repo", id="whisper_model_path")

            yield Label("Max Buffer Duration (seconds, lower = faster)")
            yield Input(self.initial_max_buffer_seconds, placeholder="10.0", id="max_buffer_seconds")

            yield Label("Transcribe Interval (seconds)")
            yield Input(self.initial_transcribe_interval, placeholder="2.0", id="transcribe_interval")

            yield Label("Voice Activity Threshold (higher = less sensitive)")
            yield Input(self.initial_vad_threshold, placeholder="0.01", id="vad_threshold")

            yield Button("Save", variant="primary", id="save")
            yield Button("Cancel", variant="default", id="cancel")

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "save":
            api_key = self.query_one("#api_key").value
            base_url = self.query_one("#base_url").value or None
            model = self.query_one("#model").value
            transcript_dir = self.query_one("#transcript_dir").value or None
            whisper_model = self.query_one("#whisper_model", Select).value
            whisper_model_path = self.query_one("#whisper_model_path").value or ""

            try:
                max_buffer_seconds = float(self.query_one("#max_buffer_seconds").value)
            except ValueError:
                max_buffer_seconds = 10.0

            try:
                transcribe_interval = float(self.query_one("#transcribe_interval").value)
            except ValueError:
                transcribe_interval = 2.0

            try:
                vad_threshold = float(self.query_one("#vad_threshold").value)
            except ValueError:
                vad_threshold = 0.01

            self.dismiss((api_key, base_url, model, transcript_dir, whisper_model, transcribe_interval, vad_threshold, whisper_model_path, max_buffer_seconds))
        else:
            self.dismiss(None)

    def action_cancel(self):
        self.dismiss(None)

    def key_escape(self):
        """Ensure Escape always closes the dialog."""
        self.dismiss(None)


class AudioSourceScreen(ModalScreen):
    """Modal for configuring audio sources (microphone and system audio)."""

    CSS = """
    AudioSourceScreen {
        align: center middle;
    }

    #audio_dialog {
        width: 55;
        height: auto;
        max-height: 20;
        border: solid $primary;
        background: $surface;
        padding: 0 1;
        overflow-y: auto;
    }

    #audio_dialog Label {
        height: 1;
    }

    .button-row {
        height: 3;
        dock: bottom;
    }

    .button-row Button {
        width: 1fr;
    }
    """

    BINDINGS = [
        Binding("escape", "cancel", "Cancel"),
    ]

    def __init__(self, current_config, input_devices):
        super().__init__()
        self.current_config = current_config
        self.input_devices = input_devices

    def compose(self) -> ComposeResult:
        with Vertical(id="audio_dialog"):
            yield Label("[b]Audio Sources[/b]")
            yield Checkbox("Microphone (use device selector on main screen)", id="mic_enabled", value=self.current_config.get("mic_enabled", True))
            yield Checkbox("System Audio (captures app audio output)", id="system_enabled", value=self.current_config.get("system_enabled", True))
            yield Label("", id="permission_status")
            with Horizontal(classes="button-row"):
                yield Button("Apply", variant="primary", id="btn_apply")
                yield Button("Cancel", id="btn_cancel")

    def on_mount(self):
        self._check_permission()

    def _check_permission(self):
        granted = PermissionManager.check_screen_recording_permission()
        status = self.query_one("#permission_status")
        if granted:
            status.update("[green]Screen Recording Permission: OK[/green]")
        else:
            status.update("[yellow]Screen Recording permission required for System Audio[/yellow]")

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "btn_apply":
            config = {
                "mic_enabled": self.query_one("#mic_enabled", Checkbox).value,
                "mic_device": self.current_config.get("mic_device"),  # Preserve existing device selection
                "system_enabled": self.query_one("#system_enabled", Checkbox).value,
                "app_filter": "all",
                "selected_apps": [],
            }
            self.dismiss(config)
        elif event.button.id == "btn_cancel":
            self.dismiss(None)

    def action_cancel(self):
        self.dismiss(None)


class TranscriptViewerScreen(ModalScreen):
    """Full-screen modal for viewing a transcript."""

    CSS = """
    TranscriptViewerScreen {
        align: center middle;
    }

    #viewer_dialog {
        width: 90%;
        height: 90%;
        border: solid $primary;
        background: $surface;
        padding: 0 1;
    }

    #viewer_title {
        dock: top;
        height: 1;
        text-style: bold;
        background: $primary;
        content-align: center middle;
    }

    #viewer_content {
        height: 1fr;
        overflow-y: auto;
    }

    #viewer_legend {
        dock: bottom;
        height: 1;
        background: $panel;
        content-align: center middle;
    }
    """

    BINDINGS = [
        Binding("j", "scroll_down", "Scroll Down", show=False),
        Binding("k", "scroll_up", "Scroll Up", show=False),
        Binding("q,escape", "close_viewer", "Close"),
    ]

    def __init__(self, filepath: Path, title: str = "Transcript"):
        super().__init__()
        self.filepath = filepath
        self.title_text = title

    def compose(self) -> ComposeResult:
        with Container(id="viewer_dialog"):
            yield Label(self.title_text, id="viewer_title")
            yield RichLog(id="viewer_content", wrap=True, markup=True)
            yield Label("[j/k] Scroll  [q] Close", id="viewer_legend")

    def on_mount(self):
        """Load and display transcript content."""
        log = self.query_one("#viewer_content", RichLog)
        try:
            content = self.filepath.read_text()
            log.write(content)
        except Exception as e:
            log.write(f"[red]Error reading file: {e}[/red]")

    def action_scroll_down(self):
        log = self.query_one("#viewer_content", RichLog)
        log.scroll_down()

    def action_scroll_up(self):
        log = self.query_one("#viewer_content", RichLog)
        log.scroll_up()

    def action_close_viewer(self):
        self.dismiss(None)


class ConfirmDeleteDialog(ModalScreen):
    """Confirmation dialog for transcript deletion."""

    CSS = """
    ConfirmDeleteDialog {
        align: center middle;
    }

    #confirm_dialog {
        width: 50;
        height: auto;
        border: thick $error;
        background: $surface;
        padding: 1 2;
    }

    #confirm_title {
        text-style: bold;
        color: $error;
    }

    #confirm_filename {
        margin: 1 0;
    }

    .confirm_buttons {
        margin-top: 1;
        height: 3;
    }

    .confirm_buttons Button {
        width: 1fr;
        margin: 0 1;
    }
    """

    BINDINGS = [
        Binding("y", "confirm", "Yes"),
        Binding("n,escape", "cancel", "No"),
    ]

    def __init__(self, filename: str):
        super().__init__()
        self.filename = filename

    def compose(self) -> ComposeResult:
        with Container(id="confirm_dialog"):
            yield Label("Delete Transcript?", id="confirm_title")
            yield Label(f"Are you sure you want to delete:\n{self.filename}", id="confirm_filename")
            with Horizontal(classes="confirm_buttons"):
                yield Button("Yes (y)", variant="error", id="btn_yes")
                yield Button("No (n)", variant="primary", id="btn_no")

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "btn_yes":
            self.dismiss(True)
        else:
            self.dismiss(False)

    def action_confirm(self):
        self.dismiss(True)

    def action_cancel(self):
        self.dismiss(False)


class MoveTranscriptDialog(ModalScreen):
    """Dialog for moving transcript to a new location."""

    CSS = """
    MoveTranscriptDialog {
        align: center middle;
    }

    #move_dialog {
        width: 60;
        height: auto;
        border: solid $primary;
        background: $surface;
        padding: 1 2;
    }

    #move_title {
        text-style: bold;
    }

    #dest_path {
        width: 100%;
        margin: 1 0;
    }

    .move_buttons {
        height: 3;
    }

    .move_buttons Button {
        width: 1fr;
        margin: 0 1;
    }
    """

    BINDINGS = [
        Binding("escape", "cancel", "Cancel"),
    ]

    def __init__(self, current_dir: str):
        super().__init__()
        self.current_dir = current_dir

    def compose(self) -> ComposeResult:
        with Container(id="move_dialog"):
            yield Label("Move Transcript", id="move_title")
            yield Label("Enter destination directory:")
            yield Input(self.current_dir, id="dest_path")
            with Horizontal(classes="move_buttons"):
                yield Button("Move", variant="primary", id="btn_move")
                yield Button("Cancel", id="btn_cancel")

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "btn_move":
            path = self.query_one("#dest_path", Input).value
            if path:
                self.dismiss(path)
            else:
                self.dismiss(None)
        else:
            self.dismiss(None)

    def on_input_submitted(self, event: Input.Submitted):
        path = event.value
        if path:
            self.dismiss(path)

    def action_cancel(self):
        self.dismiss(None)


class TranscriptsScreen(ModalScreen):
    """Modal screen for browsing and managing transcript files."""

    CSS = """
    TranscriptsScreen {
        align: center middle;
    }

    #transcripts_dialog {
        width: 80%;
        height: 80%;
        border: solid $primary;
        background: $surface;
    }

    #transcripts_title {
        dock: top;
        height: 1;
        text-style: bold;
        content-align: center middle;
        background: $primary;
    }

    #content_area {
        height: 1fr;
    }

    #transcript_list {
        width: 100%;
        height: 1fr;
    }

    #preview_pane {
        width: 40%;
        border-left: solid $accent;
        display: none;
    }

    #preview_content {
        height: 1fr;
    }

    #key_legend {
        dock: bottom;
        height: 1;
        background: $panel;
        content-align: center middle;
    }

    .with-preview #transcript_list {
        width: 60%;
    }

    .with-preview #preview_pane {
        display: block;
    }
    """

    BINDINGS = [
        Binding("j,down", "cursor_down", "Down", show=False),
        Binding("k,up", "cursor_up", "Up", show=False),
        Binding("h", "collapse_preview", "Collapse"),
        Binding("l", "expand_preview", "Preview"),
        Binding("enter,v", "view_transcript", "View"),
        Binding("d", "delete_transcript", "Delete"),
        Binding("m", "move_transcript", "Move"),
        Binding("q,escape", "close_screen", "Close"),
    ]

    def __init__(self, transcript_dir: Path):
        super().__init__()
        self.transcript_dir = transcript_dir
        self.transcripts: list[tuple[Path, str]] = []
        self.preview_visible = False

    def compose(self) -> ComposeResult:
        with Container(id="transcripts_dialog"):
            yield Label("Transcripts", id="transcripts_title")
            with Horizontal(id="content_area"):
                yield OptionList(id="transcript_list")
                with Container(id="preview_pane"):
                    yield RichLog(id="preview_content", wrap=True, markup=True)
            yield Label(
                "[j/k] Navigate  [l] Preview  [h] Collapse  [v/Enter] View  [d] Delete  [m] Move  [q] Close",
                id="key_legend"
            )

    def on_mount(self):
        """Load transcripts when screen mounts."""
        self.load_transcripts()

    def load_transcripts(self):
        """Scan transcript directory and populate list."""
        transcript_list = self.query_one("#transcript_list", OptionList)
        transcript_list.clear_options()
        self.transcripts = []

        # Find all Summary_*.md files
        files = sorted(self.transcript_dir.glob("Summary_*.md"), reverse=True)

        for filepath in files:
            preview = self._extract_preview(filepath)
            self.transcripts.append((filepath, preview))

            # Format display text
            display_text = self._format_list_item(filepath, preview)
            transcript_list.add_option(Option(display_text))

        if not self.transcripts:
            transcript_list.add_option(Option("[dim]No transcripts found[/dim]"))

    def _extract_preview(self, filepath: Path) -> str:
        """Extract summary preview from markdown file."""
        try:
            content = filepath.read_text()
            lines = content.split('\n')
            preview_lines = []
            in_summary = False
            for line in lines:
                if line.startswith('# Meeting Summary'):
                    in_summary = True
                    continue
                if line.startswith('## Transcript'):
                    break
                if in_summary and line.strip():
                    preview_lines.append(line.strip())
                    if len(preview_lines) >= 3:
                        break
            preview = ' '.join(preview_lines)
            if len(preview) > 150:
                preview = preview[:150] + '...'
            return preview
        except Exception:
            return "(Unable to read preview)"

    def _format_list_item(self, filepath: Path, preview: str) -> str:
        """Format a transcript for display in the list."""
        name = filepath.stem
        # Extract date from filename: Summary_2025-12-04_17-37-26
        date_str = name.replace("Summary_", "")
        parts = date_str.split("_")
        if len(parts) == 2:
            date_part = parts[0]
            time_part = parts[1].replace("-", ":")
            display_date = f"{date_part} {time_part}"
        else:
            display_date = date_str

        return f"[bold]{display_date}[/bold]\n{preview}"

    def action_cursor_down(self):
        """Move selection down."""
        option_list = self.query_one("#transcript_list", OptionList)
        if option_list.highlighted is not None and self.transcripts:
            new_index = min(option_list.highlighted + 1, len(self.transcripts) - 1)
            option_list.highlighted = new_index
            if self.preview_visible:
                self._update_preview()

    def action_cursor_up(self):
        """Move selection up."""
        option_list = self.query_one("#transcript_list", OptionList)
        if option_list.highlighted is not None and self.transcripts:
            new_index = max(option_list.highlighted - 1, 0)
            option_list.highlighted = new_index
            if self.preview_visible:
                self._update_preview()

    def action_expand_preview(self):
        """Show preview pane with full summary."""
        if not self.transcripts:
            return
        self.preview_visible = True
        self.query_one("#transcripts_dialog").add_class("with-preview")
        self._update_preview()

    def action_collapse_preview(self):
        """Hide preview pane."""
        self.preview_visible = False
        self.query_one("#transcripts_dialog").remove_class("with-preview")

    def _update_preview(self):
        """Update preview pane content."""
        option_list = self.query_one("#transcript_list", OptionList)
        if option_list.highlighted is None or not self.transcripts:
            return

        idx = option_list.highlighted
        if idx >= len(self.transcripts):
            return

        filepath, _ = self.transcripts[idx]
        preview_log = self.query_one("#preview_content", RichLog)
        preview_log.clear()

        try:
            content = filepath.read_text()
            # Show summary section only (up to Transcript header)
            if '## Transcript' in content:
                summary_part = content.split('## Transcript')[0]
            else:
                summary_part = content[:1000]
            preview_log.write(summary_part)
        except Exception as e:
            preview_log.write(f"[red]Error reading file: {e}[/red]")

    def action_view_transcript(self):
        """Open transcript in full-screen viewer."""
        option_list = self.query_one("#transcript_list", OptionList)
        if option_list.highlighted is None or not self.transcripts:
            return

        idx = option_list.highlighted
        if idx >= len(self.transcripts):
            return

        filepath, _ = self.transcripts[idx]
        self.app.push_screen(TranscriptViewerScreen(filepath, filepath.name))

    def action_delete_transcript(self):
        """Delete selected transcript after confirmation."""
        option_list = self.query_one("#transcript_list", OptionList)
        if option_list.highlighted is None or not self.transcripts:
            return

        idx = option_list.highlighted
        if idx >= len(self.transcripts):
            return

        filepath, _ = self.transcripts[idx]

        def handle_confirm(confirmed: bool):
            if confirmed:
                try:
                    filepath.unlink()
                    self.app.notify(f"Deleted {filepath.name}")
                    self.load_transcripts()
                except Exception as e:
                    self.app.notify(f"Error deleting: {e}", severity="error")

        self.app.push_screen(ConfirmDeleteDialog(filepath.name), handle_confirm)

    def action_move_transcript(self):
        """Move transcript to different location."""
        option_list = self.query_one("#transcript_list", OptionList)
        if option_list.highlighted is None or not self.transcripts:
            return

        idx = option_list.highlighted
        if idx >= len(self.transcripts):
            return

        filepath, _ = self.transcripts[idx]

        def handle_move(new_dir: str | None):
            if new_dir:
                try:
                    new_path = Path(new_dir).expanduser() / filepath.name
                    new_path.parent.mkdir(parents=True, exist_ok=True)
                    filepath.rename(new_path)
                    self.app.notify(f"Moved to {new_path}")
                    self.load_transcripts()
                except Exception as e:
                    self.app.notify(f"Error moving: {e}", severity="error")

        self.app.push_screen(MoveTranscriptDialog(str(self.transcript_dir)), handle_move)

    def action_close_screen(self):
        """Close the transcripts screen."""
        self.dismiss(None)

    def on_option_list_option_highlighted(self, event: OptionList.OptionHighlighted):
        """Update preview when selection changes."""
        if self.preview_visible:
            self._update_preview()



class DeviceSelect(Select):
    """Select widget that allows 'Escape' to blur focus back to the main app."""

    BINDINGS = [
        Binding("escape", "blur_input", "Back to Transcript"),
    ]

    def action_blur_input(self):
        self.app.query_one("#transcript_log").focus()


class AIInput(Input):
    """Input widget that allows 'Escape' to blur focus back to the main app."""
    
    BINDINGS = [
        Binding("escape", "blur_input", "Back to Transcript"),
    ]

    def action_blur_input(self):
        self.app.query_one("#transcript_log").focus()


class TranscriptLog(RichLog):
    """Transcript log that handles application-level command bindings."""

    BINDINGS = [
        Binding("r", "app.start_recording", "Record"),
        Binding("space", "app.stop_recording", "Stop"),
        Binding("s", "app.open_settings", "Settings"),
        Binding("a", "app.open_audio_sources", "Audio"),
        Binding("t", "app.open_transcripts", "Transcripts"),
        Binding("d", "app.focus_device", "Device"),
        Binding("/", "app.focus_input", "Ask AI"),
        Binding("j,down", "scroll_down", "Scroll Down"),
        Binding("k,up", "scroll_up", "Scroll Up"),
    ]




class NavigationProvider(Provider):
    """A command provider to open screens and trigger actions."""

    def _get_commands(self):
        app = self.screen.app
        return [
            ("Settings", "Open application settings (Keys)", lambda: app.open_settings()),
            ("Transcripts", "Browse and manage transcripts", lambda: app.open_transcripts()),
            ("Audio Sources", "Configure microphone and system audio", lambda: app.open_audio_sources()),
            ("Input Device Focus", "Focus input device selector", lambda: app.action_focus_device()),
            ("Ask AI", "Focus AI input", lambda: app.action_focus_input()),
            ("Record", "Start recording", lambda: app.start_recording()),
            ("Stop Recording", "Stop recording", lambda: app.stop_recording()),
        ]

    async def discover(self):
        """Called when the command palette is opened with no query."""
        for name, help_text, callback in self._get_commands():
            yield DiscoveryHit(
                name,
                callback,
                help=help_text,
            )

    async def search(self, query: str):
        matcher = self.matcher(query)
        for name, help_text, callback in self._get_commands():
            score = matcher.match(name)
            if score > 0:
                yield Hit(
                    score,
                    matcher.highlight(name),
                    callback,
                    help=help_text
                )


class MeetingAssistantApp(App):
    CSS = """
    Screen {
        layout: vertical;
        background: $surface;
    }

    #transcript_box {
        height: 2fr;
        width: 100%;
        background: $background;
        border: solid $primary;
        margin: 0 0 1 0;
        padding: 0 1;
    }

    #controls_area {
        layout: horizontal;
        height: 3;
        width: 100%;
        background: $panel;
        border-top: solid $accent;
        border-bottom: solid $accent;
        align: center middle;
        padding: 0 1;
    }

    .meter-group {
        width: 1fr;
        height: 1;
        layout: horizontal;
        align: center middle;
    }

    .meter-label {
        width: auto;
        padding-right: 1;
        text-style: bold;
    }

    .meter-bar {
        width: 20;
    }

    #controls_buttons {
        width: auto;
        height: 1;
        layout: horizontal;
    }

    Button {
        height: 1;
        border: none;
        min-width: 10;
        margin: 0 1;
    }

    #bottom_area {
        height: 1fr;
        width: 100%;
        layout: horizontal;
    }

    #device_panel {
        width: 1fr;
        height: 100%;
        padding: 1;
    }

    #ai_panel {
        width: 2fr;
        height: 100%;
        layout: vertical;
        border-left: solid $secondary;
        padding: 1;
    }

    .box-title {
        background: $primary;
        color: $text;
        padding: 0 1;
        text-align: center;
        text-style: bold;
        width: 100%;
    }

    #transcript_log {
        width: 100%;
        height: 1fr;
        overflow-y: auto;
    }

    #pending_text {
        width: 100%;
        height: auto;
        min-height: 1;
        max-height: 10;
        background: $background;
        color: $text-muted;
        padding: 0 1;
        border-top: solid $accent;
    }

    RichLog {
        min-height: 1;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("ctrl+q", "quit", "Quit"),
    ]

    COMMANDS = {NavigationProvider}

    def __init__(self):
        super().__init__()
        self.audio_engine = None  # Legacy single-source (kept for compatibility)
        self.is_recording = False
        self.transcript_history = []  # List of confirmed segments
        self.current_buffer_text = ""
        self.full_transcript_text = ""

        # Multi-source audio infrastructure
        self.audio_mixer = AudioMixer(sample_rate=16000)
        self.mic_engine = None
        self.system_audio_engine = None

        # Audio source configuration
        self.audio_config = {
            "mic_enabled": True,
            "mic_device": None,
            "system_enabled": True,  # Enable system audio by default
            "app_filter": "all",  # "all" or "specific"
            "selected_apps": [],  # Bundle IDs
        }

        # Load Configuration
        self.load_config()

        # Initialize Transcriber early to avoid multiprocessing issues in TUI
        # This triggers the resource_tracker spawn before Textual takes over stdio
        model_info = self.whisper_model_path or self.whisper_model
        print(f"Initializing Whisper Model ({model_info})...")
        self.transcriber = Transcriber(
            model_size=self.whisper_model,
            model_path=self.whisper_model_path or None,
            max_buffer_seconds=self.max_buffer_seconds,
        )

        # Initialize VAD processor
        self.vad_processor = VADProcessor(threshold=self.vad_threshold)

        # Audio Selection
        try:
            self.devices = sd.query_devices()
            self.input_devices = [
                (d["name"], i)
                for i, d in enumerate(self.devices)
                if d["max_input_channels"] > 0
            ]
        except Exception:
            self.input_devices = [("Error detecting devices", -1)]

        # Initialize LLM Client
        self.update_llm_client()

    def load_config(self):
        file_config = {}
        if CONFIG_PATH.exists() and CONFIG_PATH.is_file():
            try:
                with open(CONFIG_PATH, "rb") as f:
                    file_config = tomllib.load(f)
            except Exception as e:
                print(f"Warning: Failed to load config from {CONFIG_PATH}: {e}")

        self.openai_api_key = os.getenv("OPENAI_API_KEY", file_config.get("OPENAI_API_KEY", ""))
        self.llm_base_url = os.getenv("LLM_BASE_URL", file_config.get("LLM_BASE_URL", None))
        self.llm_model = os.getenv("LLM_MODEL", file_config.get("LLM_MODEL", "gpt-4o"))

        # Whisper settings
        self.whisper_model = os.getenv("WHISPER_MODEL", file_config.get("WHISPER_MODEL", "base"))
        self.whisper_model_path = file_config.get("WHISPER_MODEL_PATH", "")  # Optional local model path
        self.max_buffer_seconds = float(file_config.get("MAX_BUFFER_SECONDS", 10.0))  # Reduced from 30s for lower latency

        self.transcribe_interval = float(os.getenv("TRANSCRIBE_INTERVAL", file_config.get("TRANSCRIBE_INTERVAL", 2.0)))
        self.vad_threshold = float(os.getenv("VAD_THRESHOLD", file_config.get("VAD_THRESHOLD", 0.01)))

        # Transcript directory configuration
        default_transcript_dir = Path.home() / "Documents" / "Transcripts"
        self.transcript_dir = Path(
            os.getenv("TRANSCRIPT_DIR", file_config.get("TRANSCRIPT_DIR", str(default_transcript_dir)))
        )
        self.transcript_dir.mkdir(parents=True, exist_ok=True)

        # Last selected input device
        self.last_device_name = file_config.get("LAST_DEVICE", None)

    def save_config(self, api_key, base_url, model, transcript_dir=None, whisper_model="base", transcribe_interval=2.0, vad_threshold=0.01, whisper_model_path="", max_buffer_seconds=10.0):
        # Check if whisper model changed
        model_changed = (
            whisper_model != self.whisper_model or
            whisper_model_path != self.whisper_model_path or
            max_buffer_seconds != self.max_buffer_seconds
        )

        self.openai_api_key = api_key
        self.llm_base_url = base_url
        self.llm_model = model
        self.whisper_model = whisper_model
        self.transcribe_interval = transcribe_interval
        self.vad_threshold = vad_threshold
        self.whisper_model_path = whisper_model_path
        self.max_buffer_seconds = max_buffer_seconds

        if transcript_dir:
            self.transcript_dir = Path(transcript_dir)
            self.transcript_dir.mkdir(parents=True, exist_ok=True)

        config_data = {
            "OPENAI_API_KEY": api_key,
            "LLM_MODEL": model,
            "WHISPER_MODEL": whisper_model,
            "TRANSCRIBE_INTERVAL": transcribe_interval,
            "VAD_THRESHOLD": vad_threshold,
            "MAX_BUFFER_SECONDS": max_buffer_seconds,
        }
        if base_url:
            config_data["LLM_BASE_URL"] = base_url
        if transcript_dir:
            config_data["TRANSCRIPT_DIR"] = str(self.transcript_dir)
        if whisper_model_path:
            config_data["WHISPER_MODEL_PATH"] = whisper_model_path
        # Preserve last device setting
        if self.last_device_name:
            config_data["LAST_DEVICE"] = self.last_device_name

        try:
            with open(CONFIG_PATH, "wb") as f:
                tomli_w.dump(config_data, f)
            self.notify("Settings saved!")
            self.update_llm_client()

            # Reinitialize transcriber if model settings changed
            if model_changed:
                self._reinitialize_transcriber()
        except Exception as e:
            self.notify(f"Error saving settings: {e}", severity="error")

    def _reinitialize_transcriber(self):
        """Reinitialize the transcriber with current settings (runs in background)."""
        # Mark model as not ready while loading
        self.transcriber.model_ready = False
        self.notify("Loading Whisper model...", severity="information")
        self.run_worker(self._load_transcriber_async, exclusive=True, thread=True)

    def _load_transcriber_async(self):
        """Background worker to load the transcriber model."""
        try:
            self.transcriber = Transcriber(
                model_size=self.whisper_model,
                model_path=self.whisper_model_path or None,
                max_buffer_seconds=self.max_buffer_seconds,
            )
            if self.transcriber.model_ready:
                self.call_from_thread(self.notify, "Whisper model loaded!", severity="information")
            else:
                error = self.transcriber.model_error or "Unknown error"
                self.call_from_thread(self.notify, f"Failed to load model: {error}", severity="error")
        except Exception as e:
            self.call_from_thread(self.notify, f"Failed to load model: {e}", severity="error")

    def save_last_device(self, device_name: str):
        """Save just the last selected device to config."""
        self.last_device_name = device_name

        # Load existing config to preserve other settings
        file_config = {}
        if CONFIG_PATH.exists() and CONFIG_PATH.is_file():
            try:
                with open(CONFIG_PATH, "rb") as f:
                    file_config = tomllib.load(f)
            except Exception:
                pass

        file_config["LAST_DEVICE"] = device_name

        try:
            with open(CONFIG_PATH, "wb") as f:
                tomli_w.dump(file_config, f)
        except Exception:
            pass  # Silent fail for device preference

    def update_llm_client(self):
        self.llm_client = OpenAI(
            api_key=self.openai_api_key,
            base_url=self.llm_base_url
        )

    def compose(self) -> ComposeResult:
        yield Header()

        # 1. Main Transcript Area (Top, takes most space)
        with Vertical(id="transcript_box"):
            yield Label("Live Transcript", classes="box-title")
            # auto_scroll=True to keep view at bottom
            yield TranscriptLog(id="transcript_log", wrap=True, markup=True, auto_scroll=True)
            yield Label("", id="pending_text")

        # 2. Controls Area (Middle strip)
        with Container(id="controls_area"):
            # Meters
            with Container(classes="meter-group"):
                yield Label("Mic:", classes="meter-label")
                yield Label("....................", id="mic_meter", classes="meter-bar")
            
            with Container(classes="meter-group"):
                yield Label("Sys:", classes="meter-label")
                yield Label("....................", id="sys_meter", classes="meter-bar")

            # Buttons
            with Container(id="controls_buttons"):
                yield Button("Rec", id="btn_record", variant="success")
                yield Button("Stop", id="btn_stop", variant="error", disabled=True)

        # 3. Bottom Area (Device + AI)
        with Container(id="bottom_area"):
            # Left: Device Selection
            with Container(id="device_panel"):
                yield Label("Input Device", classes="box-title")
                yield DeviceSelect(
                    self.input_devices, prompt="Select Device", id="device_select"
                )
            
            # Right: AI Assistant
            with Container(id="ai_panel"):
                yield Label("AI Assistant", classes="box-title")
                yield RichLog(id="ai_log", wrap=True, markup=True)
                yield AIInput(
                    placeholder="Ask AI about the meeting... (Press '/' to focus)", id="ai_input"
                )

        yield Footer()

    def on_mount(self):
        log = self.query_one("#transcript_log")
        log.write("Waiting to start...")
        log.focus()  # Initial focus on transcript to enable command bindings
        
        # Start background meeting detector
        self.detect_meetings()

        # Restore last selected device if available
        if self.last_device_name:
            device_select = self.query_one("#device_select", Select)
            # Find the device ID by name
            for name, device_id in self.input_devices:
                if name == self.last_device_name:
                    device_select.value = device_id
                    self.audio_config["mic_device"] = device_id
                    break
        
    def on_unmount(self):
        """Ensure all resources are cleaned up when the app exits."""
        self.is_recording = False
        if self.audio_engine:
            self.audio_engine.stop()
        if self.mic_engine:
            self.mic_engine.stop()
        if self.system_audio_engine:
            self.system_audio_engine.stop()

    @work(exclusive=True, thread=True)
    def detect_meetings(self):
        """Background worker to auto-detect meetings."""
        # Use self.app.is_running to ensure we exit when the app closes
        while self.app.is_running:
            if not self.is_recording:
                # Check Zoom (pmset method)
                try:
                    pmset = subprocess.check_output(
                        ["pmset", "-g"], 
                        text=True, 
                        stdin=subprocess.DEVNULL
                    )
                    if "zoom.us" in pmset and "Sleep" in pmset:
                        self.app.call_from_thread(
                            self.notify, "Zoom Detected! Ready to record."
                        )
                except Exception:
                    pass
            time.sleep(5)

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "btn_record":
            self.start_recording()
        elif event.button.id == "btn_stop":
            self.stop_recording()

    def on_select_changed(self, event: Select.Changed):
        """Save device selection when changed."""
        if event.select.id == "device_select" and event.value != Select.BLANK:
            # Find device name by ID and save it
            for name, device_id in self.input_devices:
                if device_id == event.value:
                    self.save_last_device(name)
                    self.audio_config["mic_device"] = device_id
                    break

    def open_audio_sources(self):
        def apply_callback(config):
            if config:
                self.apply_audio_config(config)

        self.push_screen(
            AudioSourceScreen(self.audio_config, self.input_devices),
            apply_callback,
        )

    def apply_audio_config(self, config):
        """Apply audio source configuration."""
        self.audio_config = config

        # Update device select if mic device changed
        if config.get("mic_device") is not None:
            try:
                self.query_one("#device_select", Select).value = config["mic_device"]
            except Exception:
                pass

        # Show notification about configuration
        sources = []
        if config.get("mic_enabled"):
            sources.append("Microphone")
        if config.get("system_enabled"):
            if config.get("app_filter") == "specific" and config.get("selected_apps"):
                sources.append(f"System Audio ({len(config['selected_apps'])} apps)")
            else:
                sources.append("System Audio (all apps)")

        if sources:
            self.notify(f"Audio sources: {', '.join(sources)}")
        else:
            self.notify("No audio sources enabled!", severity="warning")

    def open_settings(self):
        def save_callback(result):
            if result:
                self.save_config(*result)

        self.push_screen(
            SettingsScreen(
                self.openai_api_key,
                self.llm_base_url,
                self.llm_model,
                self.transcript_dir,
                self.whisper_model,
                self.transcribe_interval,
                self.vad_threshold,
                self.whisper_model_path,
                self.max_buffer_seconds,
            ),
            save_callback
        )

    def action_open_transcripts(self):
        """Action handler for 't' keybinding."""
        self.open_transcripts()

    def action_start_recording(self):
        """Action handler for 'r' keybinding."""
        if not self.is_recording:
            self.start_recording()

    def action_stop_recording(self):
        """Action handler for 'space' keybinding."""
        if self.is_recording:
            self.stop_recording()

    def action_open_settings(self):
        """Action handler for 's' keybinding."""
        self.open_settings()

    def action_open_audio_sources(self):
        """Action handler for 'a' keybinding."""
        self.open_audio_sources()

    def action_focus_device(self):
        """Action handler for 'd' keybinding."""
        self.query_one("#device_select").focus()

    def action_focus_input(self):
        """Action to focus the AI input box."""
        self.query_one("#ai_input").focus()

    def action_scroll_transcript_down(self):
        """Scroll the transcript log down."""
        log = self.query_one("#transcript_log")
        log.scroll_down()

    def action_scroll_transcript_up(self):
        """Scroll the transcript log up."""
        log = self.query_one("#transcript_log")
        log.scroll_up()

    def open_transcripts(self):
        """Open the transcripts browser screen."""
        self.push_screen(TranscriptsScreen(self.transcript_dir))

    def start_recording(self):
        device_id = self.query_one("#device_select").value

        # Check if transcription model is ready
        if not self.transcriber.model_ready:
            error_msg = self.transcriber.model_error or "Model not loaded"
            self.notify(f"Whisper model not ready: {error_msg}", severity="error")
            return

        # Check if we have any audio source configured
        mic_enabled = self.audio_config.get("mic_enabled", True)
        system_enabled = self.audio_config.get("system_enabled", True)

        if mic_enabled and (device_id is None or device_id == Select.BLANK):
            self.notify("Please select an audio device first!", severity="error")
            return

        if not mic_enabled and not system_enabled:
            self.notify("No audio sources enabled! Configure in Audio Sources.", severity="error")
            return

        self.is_recording = True
        self.query_one("#btn_record").disabled = True
        self.query_one("#btn_stop").disabled = False
        self.query_one("#device_select").disabled = True
        self.query_one("#transcript_log").clear()
        self.update_pending_ui("")

        # Clear any existing sources from mixer
        self.audio_mixer = AudioMixer(sample_rate=16000)

        sources_started = []
        log = self.query_one("#transcript_log")

        # Set up microphone if enabled
        if mic_enabled and device_id is not None:
            self.mic_engine = AudioEngine(device_id=device_id)
            # Apply 3x gain to mic to balance with system audio
            self.audio_mixer.add_source("mic", self.mic_engine, gain=3.0)
            self.mic_engine.start()
            sources_started.append("Mic")
            # Also keep legacy audio_engine for compatibility
            self.audio_engine = self.mic_engine

        # Set up system audio if enabled
        if system_enabled:
            # Check Screen Recording permission first
            if not PermissionManager.check_screen_recording_permission():
                log.write("[yellow]⚠ System Audio: Screen Recording permission required[/yellow]")
                log.write("[dim]Grant permission in System Settings > Privacy > Screen Recording[/dim]")
            else:
                self.system_audio_engine = SystemAudioEngine(
                    sample_rate=48000, target_sample_rate=16000
                )
                self.audio_mixer.add_source("system", self.system_audio_engine, gain=1.0)

                # Determine app filtering
                app_bundle_ids = None
                if self.audio_config.get("app_filter") == "specific":
                    app_bundle_ids = self.audio_config.get("selected_apps", [])

                self.system_audio_engine.start(app_bundle_ids=app_bundle_ids)
                if self.system_audio_engine.running:
                    sources_started.append("System")
                else:
                    error_msg = self.system_audio_engine._setup_error
                    log.write(f"[red]✗ System Audio failed: {error_msg or 'Unknown error'}[/red]")

        if sources_started:
            log.write(f"[green]● Recording: {' + '.join(sources_started)}[/green]")
            log.write("[dim]Waiting for speech...[/dim]")
        else:
            log.write("[yellow]⚠ Recording started but no sources active[/yellow]")

        self.process_audio_loop()

    def stop_recording(self):
        self.is_recording = False

        # Stop all audio engines
        if self.mic_engine:
            self.mic_engine.stop()
            self.audio_mixer.remove_source("mic")
        if self.system_audio_engine:
            self.system_audio_engine.stop()
            self.audio_mixer.remove_source("system")
        if self.audio_engine and self.audio_engine != self.mic_engine:
            self.audio_engine.stop()

        self.query_one("#btn_record").disabled = False
        self.query_one("#btn_stop").disabled = True
        self.query_one("#device_select").disabled = False

        # Trigger Summarization
        self.generate_summary()

    def _is_audio_silent(self, audio_data, threshold=0.01):
        """Check if audio is below silence threshold using RMS."""
        if audio_data is None or len(audio_data) == 0:
            return True
        rms = np.sqrt(np.mean(audio_data ** 2))
        return rms < threshold

    def _is_hallucination(self, text):
        """Detect common Whisper hallucination patterns."""
        if not text:
            return True
        text_lower = text.lower().strip()
        # Common Whisper hallucinations when given silence
        hallucination_patterns = [
            "1.5%", "2%", "3%",  # Percentage hallucinations
            "♪", "♫", "[music]", "(music)",  # Music symbols
            "thank you", "thanks for watching",  # YouTube-style outros
            "subscribe", "like and subscribe",
            "...", ". . .",  # Just dots
            "[silence]", "(silence)",
            "you", "the", "a",  # Single common words
        ]
        # Check if text is just repeated patterns
        words = text_lower.split()
        if len(words) > 2 and len(set(words)) == 1:
            return True  # All words are the same
        # Check for known hallucination patterns
        for pattern in hallucination_patterns:
            if text_lower == pattern or text_lower.replace(" ", "") == pattern.replace(" ", ""):
                return True
            # Check if text is just repetitions of the pattern
            if pattern in text_lower and text_lower.replace(pattern, "").strip() == "":
                return True
        return False

    @work(exclusive=True, thread=True)
    def process_audio_loop(self):
        """Main loop with VAD-triggered transcription and word streaming."""
        last_transcribe_time = 0
        meter_update_interval = 0.05  # 50ms for responsiveness

        # Reset VAD processor for this recording session
        self.vad_processor = VADProcessor(threshold=self.vad_threshold)

        # Word streaming state
        last_word_count = 0

        while self.is_recording and self.app.is_running:
            current_time = time.time()

            # Check individual source levels for the visual meters
            mic_level = 0.0
            system_level = 0.0

            # Collect chunks for VAD processing
            combined_chunk = None

            if self.mic_engine and self.mic_engine.running:
                mic_chunk = self.mic_engine.get_audio_chunk()
                if mic_chunk is not None and len(mic_chunk) > 0:
                    mic_level = np.sqrt(np.mean(mic_chunk ** 2))
                    # Put it back for the mixer (we peeked at it)
                    self.mic_engine.queue.put(mic_chunk)
                    combined_chunk = mic_chunk

            if self.system_audio_engine and self.system_audio_engine.running:
                sys_chunk = self.system_audio_engine.get_audio_chunk()
                if sys_chunk is not None and len(sys_chunk) > 0:
                    system_level = np.sqrt(np.mean(sys_chunk ** 2))
                    # Put it back for the mixer
                    self.system_audio_engine.queue.put(sys_chunk)
                    if combined_chunk is not None:
                        # Combine chunks for VAD
                        max_len = max(len(combined_chunk), len(sys_chunk))
                        combined_chunk = np.pad(combined_chunk, (0, max_len - len(combined_chunk)))
                        sys_chunk_padded = np.pad(sys_chunk, (0, max_len - len(sys_chunk)))
                        combined_chunk = combined_chunk + sys_chunk_padded
                    else:
                        combined_chunk = sys_chunk

            # Update visual level meters
            self.app.call_from_thread(self._update_level_meters, mic_level, system_level)

            # Process audio through VAD
            should_transcribe = False
            should_commit = False

            if combined_chunk is not None and len(combined_chunk) > 0:
                should_transcribe, should_commit = self.vad_processor.process_chunk(combined_chunk)

            # Get mixed audio from all active sources
            chunk = self.audio_mixer.get_mixed_audio()

            if chunk is not None and len(chunk) > 0:
                # Add audio to buffer
                buffer = self.transcriber.process_audio(chunk)
                buffer_duration = len(buffer) / self.transcriber.sample_rate

                # Force commit if buffer is getting too long
                if buffer_duration > self.max_buffer_seconds * 0.9:
                    should_commit = True
                    should_transcribe = True

                # Transcribe on interval OR when VAD triggers
                interval_trigger = current_time - last_transcribe_time >= self.transcribe_interval

                if (should_transcribe or interval_trigger) and buffer_duration > 0.5:
                    last_transcribe_time = current_time

                    result = self.transcriber.transcribe_segment(buffer)
                    text = result["text"]
                    words = result["words"]

                    valid_text = text.strip() and not self._is_hallucination(text)

                    if valid_text:
                        # Stream new words to UI
                        if words and len(words) > last_word_count:
                            new_words = words[last_word_count:]
                            self.app.call_from_thread(self.stream_words_to_ui, new_words)
                            last_word_count = len(words)

                        self.current_buffer_text = text
                        self.app.call_from_thread(self.update_pending_ui, text)

                    if should_commit:
                        if valid_text:
                            # Commit the text
                            self.app.call_from_thread(self.commit_transcript_segment, text)
                            self.full_transcript_text += " " + text

                        # Reset state
                        self.transcriber.clear_buffer()
                        self.current_buffer_text = ""
                        last_word_count = 0
                        self.vad_processor.reset()

                        # Clear pending UI
                        self.app.call_from_thread(self.update_pending_ui, "")

            time.sleep(meter_update_interval)

    def _update_level_meters(self, mic_level: float, sys_level: float):
        """Update visual level meters with current audio levels."""
        # Generate bar visualization (max 30 chars wide)
        bar_width = 30

        def make_bar(level: float) -> str:
            # Scale level (0.0-1.0 ish, typically 0-0.3 for speech)
            # Multiply by 3 to make it more visible, cap at 1.0
            normalized = min(level * 3, 1.0)
            filled = int(normalized * bar_width)

            # Color gradient: green for low, yellow for medium, red for high
            if normalized < 0.3:
                color = "green"
            elif normalized < 0.7:
                color = "yellow"
            else:
                color = "red"

            # Use block characters for the bar
            bar = "█" * filled + "░" * (bar_width - filled)
            return f"[{color}]{bar}[/{color}]"

        try:
            mic_meter = self.query_one("#mic_meter", Label)
            sys_meter = self.query_one("#sys_meter", Label)
            mic_meter.update(make_bar(mic_level))
            sys_meter.update(make_bar(sys_level))
        except Exception:
            pass  # Meters may not exist if not recording

    def stream_words_to_ui(self, words: list[dict]):
        """Stream new words incrementally to pending text display."""
        try:
            pending_label = self.query_one("#pending_text", Label)
            formatted = " ".join(w["word"].strip() for w in words if w.get("word", "").strip())
            if formatted:
                pending_label.update(f"[dim italic]{formatted}[/dim italic]")
        except Exception:
            pass

    def update_pending_ui(self, text):
        """Update the pending text label."""
        try:
            lbl = self.query_one("#pending_text", Label)
            lbl.update(text)
        except Exception:
            pass

    def commit_transcript_segment(self, text):
        """Add a confirmed segment to the main transcript log."""
        try:
            log = self.query_one("#transcript_log", RichLog)
            log.write(text)
        except Exception:
            pass

    def on_input_submitted(self, event: Input.Submitted):
        query = event.value
        if not query:
            return

        event.input.value = ""
        self.ask_llm(query)

    @work(thread=True)
    def ask_llm(self, query):
        log = self.query_one("#ai_log")
        log.write(f"[bold cyan]You:[/bold cyan] {query}")

        # Prepare Context
        # We combine the "history" (if we implemented committing) plus the current buffer
        context = self.full_transcript_text + " " + self.current_buffer_text

        try:
            response = self.llm_client.chat.completions.create(
                model=self.llm_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful meeting assistant. Answer briefly based on the transcript provided.",
                    },
                    {
                        "role": "user",
                        "content": f"Transcript:\n{context}\n\nQuestion: {query}",
                    },
                ],
            )
            answer = response.choices[0].message.content
            log.write(f"[bold green]AI:[/bold green] {answer}")
        except Exception as e:
            log.write(f"[red]Error:[/red] {str(e)}")

    @work(thread=True)
    def generate_summary(self):
        log = self.query_one("#transcript_log")
        log.write("\n[bold yellow]Generating Summary...[/bold yellow]")

        context = self.full_transcript_text + " " + self.current_buffer_text

        try:
            response = self.llm_client.chat.completions.create(
                model=self.llm_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert note-taker. Summarize the following meeting transcript into bullet points, capturing action items and key decisions.",
                    },
                    {"role": "user", "content": context},
                ],
            )
            summary = response.choices[0].message.content

            # Save to file in transcript directory
            filename = f"Summary_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.md"
            filepath = self.transcript_dir / filename
            filepath.parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, "w") as f:
                f.write(f"# Meeting Summary\n\n{summary}\n\n## Transcript\n{context}")

            log.write("\n[bold green]--- SUMMARY ---[/bold green]")
            log.write(summary)
            log.write(f"\n[italic]Saved to {filepath}[/italic]")

        except Exception as e:
            log.write(f"[red]Summary Error:[/red] {str(e)}")


if __name__ == "__main__":
    app = MeetingAssistantApp()
    app.run()
