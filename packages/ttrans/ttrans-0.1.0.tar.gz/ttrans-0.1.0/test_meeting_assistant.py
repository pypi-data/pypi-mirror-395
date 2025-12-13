import pytest
import numpy as np
from unittest.mock import MagicMock, patch
import sys
import queue

# Mock dependencies before importing the app
sys.modules["sounddevice"] = MagicMock()

# Mock mlx_whisper module with transcribe function
mock_mlx_whisper = MagicMock()
mock_mlx_whisper.transcribe = MagicMock(return_value={
    "text": "Test transcription",
    "segments": [{"words": [{"word": "Test", "start": 0.0, "end": 0.5}]}]
})
sys.modules["mlx_whisper"] = mock_mlx_whisper

sys.modules["openai"] = MagicMock()

# Mock ScreenCaptureKit and related pyobjc modules
mock_sck = MagicMock()
mock_coremedia = MagicMock()
mock_objc = MagicMock()
mock_foundation = MagicMock()
mock_dispatch = MagicMock()

sys.modules["ScreenCaptureKit"] = mock_sck
sys.modules["CoreMedia"] = mock_coremedia
sys.modules["objc"] = mock_objc
sys.modules["Foundation"] = mock_foundation
sys.modules["dispatch"] = mock_dispatch

# Make NSObject a proper class for inheritance
class MockNSObject:
    def init(self):
        return self

mock_foundation.NSObject = MockNSObject
mock_objc.super = lambda *args: MagicMock()

# Now import the application
import meeting_assistant  # noqa: E402

class TestAudioEngine:
    def test_initialization(self):
        engine = meeting_assistant.AudioEngine(device_id=1, sample_rate=16000)
        assert engine.device_id == 1
        assert engine.sample_rate == 16000
        assert isinstance(engine.queue, queue.Queue)
        assert engine.running is False

    def test_start_stop(self):
        engine = meeting_assistant.AudioEngine(device_id=1)

        # Mock InputStream
        with patch("meeting_assistant.sd.InputStream") as mock_stream:
            engine.start()
            assert engine.running is True
            mock_stream.assert_called_once()
            engine.stream.start.assert_called_once()

            engine.stop()
            assert engine.running is False
            engine.stream.stop.assert_called_once()
            engine.stream.close.assert_called_once()

    def test_callback_adds_to_queue(self):
        engine = meeting_assistant.AudioEngine(device_id=1)
        input_data = np.array([1.0, 2.0, 3.0])

        # Simulate callback
        engine.callback(input_data, None, None, None)

        assert not engine.queue.empty()
        item = engine.queue.get()
        np.testing.assert_array_equal(item, input_data)

    def test_get_audio_chunk_concatenates(self):
        engine = meeting_assistant.AudioEngine(device_id=1)
        chunk1 = np.array([1.0, 2.0])
        chunk2 = np.array([3.0, 4.0])

        engine.queue.put(chunk1)
        engine.queue.put(chunk2)

        result = engine.get_audio_chunk()
        expected = np.array([1.0, 2.0, 3.0, 4.0])

        np.testing.assert_array_equal(result, expected)

    def test_get_audio_chunk_empty(self):
        engine = meeting_assistant.AudioEngine(device_id=1)
        result = engine.get_audio_chunk()
        assert result is None


class TestTranscriber:
    @pytest.fixture
    def transcriber(self):
        with patch("meeting_assistant.mlx_whisper"):
            return meeting_assistant.Transcriber(model_size="tiny")

    def test_initialization(self, transcriber):
        assert transcriber.sample_rate == 16000
        assert len(transcriber.buffer) == 0
        assert transcriber.word_timestamps is True
        assert "tiny" in transcriber.model_repo

    def test_model_path_override(self):
        with patch("meeting_assistant.mlx_whisper"):
            t = meeting_assistant.Transcriber(model_path="/custom/model")
            assert t.model_repo == "/custom/model"

    def test_process_audio_appends_and_limits(self, transcriber):
        # Simulate 1 second of audio
        audio_chunk = np.zeros(16000, dtype="float32")

        # Test appending
        buffer = transcriber.process_audio(audio_chunk)
        assert len(buffer) == 16000
        np.testing.assert_array_equal(transcriber.buffer, audio_chunk)

        # Test limiting (default max_buffer_seconds is 10, so 160,000 samples)
        # Add 11 seconds of audio
        huge_chunk = np.zeros(11 * 16000, dtype="float32")
        buffer = transcriber.process_audio(huge_chunk)

        # Should only keep last 10 seconds (default max_buffer_seconds)
        assert len(buffer) == 10 * 16000
        assert len(transcriber.buffer) == 10 * 16000

    def test_process_audio_none(self, transcriber):
        result = transcriber.process_audio(None)
        assert result is None

    def test_transcribe_segment_returns_dict(self, transcriber):
        # Mock mlx_whisper.transcribe
        with patch("meeting_assistant.mlx_whisper.transcribe") as mock_transcribe:
            mock_transcribe.return_value = {
                "text": "Hello world",
                "segments": [{
                    "words": [
                        {"word": "Hello", "start": 0.0, "end": 0.5},
                        {"word": "world", "start": 0.6, "end": 1.0},
                    ]
                }]
            }

            audio = np.zeros(1000)
            result = transcriber.transcribe_segment(audio)

            assert isinstance(result, dict)
            assert result["text"] == "Hello world"
            assert len(result["words"]) == 2
            assert result["words"][0]["word"] == "Hello"
            assert result["words"][0]["start"] == 0.0

    def test_transcribe_text_only(self, transcriber):
        # Mock mlx_whisper.transcribe
        with patch("meeting_assistant.mlx_whisper.transcribe") as mock_transcribe:
            mock_transcribe.return_value = {"text": "Test", "segments": []}

            text = transcriber.transcribe_text_only(np.zeros(1000))
            assert text == "Test"

class TestMeetingAssistantApp:
    def test_app_structure(self):
        # We can instantiate the app but avoiding run() to not start TUI
        app = meeting_assistant.MeetingAssistantApp()
        assert app.audio_engine is None
        assert app.transcriber is not None
        assert app.is_recording is False
        assert app.transcript_history == []

    # Since Textual apps are complex to test without async pilot,
    # we'll stick to unit testing the logic parts invoked by the app
    # which are mostly covered in AudioEngine and Transcriber tests.

    @pytest.mark.asyncio
    async def test_app_startup(self):
        """Verifies the app can launch and reach the running state."""

        # Patch detect_meetings to prevent the background worker infinite loop
        with patch.object(meeting_assistant.MeetingAssistantApp, "detect_meetings"):
            app = meeting_assistant.MeetingAssistantApp()

            # We need to prevent the background worker from actually running forever or failing
            # inside the test environment if not mocked strictly.
            # However, we already mocked subprocess in logic, but detect_meetings calls it.
            # Let's mock subprocess.check_output to avoid actual shell calls.

            with patch("subprocess.check_output") as mock_subprocess:
                # Mock return value to simulate no zoom running
                mock_subprocess.return_value = "No meeting"

                async with app.run_test() as pilot:
                    # Verify app state
                    assert app.is_running
                    assert app.query_one("#transcript_log")
                    assert app.query_one("#btn_record")

                    # Allow the event loop to turn a bit to ensure on_mount completes
                    await pilot.pause()

                    # Ensure the worker didn't crash the app
                    assert app.is_running


class TestKeyboardNavigation:
    """Tests for keyboard shortcuts and navigation."""

    @pytest.mark.asyncio
    async def test_keyboard_shortcut_record(self):
        """Test that 'r' key triggers start_recording action."""
        with patch.object(meeting_assistant.MeetingAssistantApp, "detect_meetings"):
            with patch.object(meeting_assistant.PermissionManager, "check_screen_recording_permission", return_value=True):
                app = meeting_assistant.MeetingAssistantApp()

                with patch("subprocess.check_output") as mock_subprocess:
                    mock_subprocess.return_value = "No meeting"

                    async with app.run_test() as pilot:
                        # Mock start_recording to track if it was called
                        with patch.object(app, "start_recording") as mock_start:
                            await pilot.press("r")
                            await pilot.pause()

                            # Verify the action was triggered
                            mock_start.assert_called_once()

    @pytest.mark.asyncio
    async def test_keyboard_shortcut_stop(self):
        """Test that 'space' key triggers stop_recording when recording."""
        with patch.object(meeting_assistant.MeetingAssistantApp, "detect_meetings"):
            with patch.object(meeting_assistant.PermissionManager, "check_screen_recording_permission", return_value=True):
                app = meeting_assistant.MeetingAssistantApp()

                with patch("subprocess.check_output") as mock_subprocess:
                    mock_subprocess.return_value = "No meeting"

                    async with app.run_test() as pilot:
                        # Set recording state to true so stop action triggers
                        app.is_recording = True

                        # Mock stop_recording to track if it was called
                        with patch.object(app, "stop_recording") as mock_stop:
                            await pilot.press("space")
                            await pilot.pause()

                            # Verify the action was triggered
                            mock_stop.assert_called_once()

    @pytest.mark.asyncio
    async def test_keyboard_shortcut_settings(self):
        """Test that 's' key opens settings screen."""
        with patch.object(meeting_assistant.MeetingAssistantApp, "detect_meetings"):
            with patch.object(meeting_assistant.PermissionManager, "check_screen_recording_permission", return_value=True):
                app = meeting_assistant.MeetingAssistantApp()

                with patch("subprocess.check_output") as mock_subprocess:
                    mock_subprocess.return_value = "No meeting"

                    async with app.run_test() as pilot:
                        await pilot.press("s")
                        await pilot.pause()

                        # Settings screen should be open - check for settings-specific elements
                        api_key_input = app.screen.query_one("#api_key")
                        assert api_key_input is not None

    @pytest.mark.asyncio
    async def test_settings_screen_escape_behavior(self):
        """Test that Esc closes Settings Screen without stopping recording."""
        with patch.object(meeting_assistant.MeetingAssistantApp, "detect_meetings"):
            with patch.object(meeting_assistant.PermissionManager, "check_screen_recording_permission", return_value=True):
                app = meeting_assistant.MeetingAssistantApp()

                with patch("subprocess.check_output", return_value="No meeting"):
                    async with app.run_test() as pilot:
                        # Set recording state
                        app.is_recording = True
                        
                        # Open Settings
                        await pilot.press("s")
                        await pilot.pause()
                        assert isinstance(app.screen, meeting_assistant.SettingsScreen)

                        # Focus an input
                        app.screen.query_one("#api_key").focus()
                        
                        # Press Esc
                        await pilot.press("escape")
                        await pilot.pause()

                        # Verify Settings closed
                        assert not isinstance(app.screen, meeting_assistant.SettingsScreen)
                        
                        # Verify Recording still active
                        assert app.is_recording is True


    @pytest.mark.asyncio
    async def test_keyboard_shortcut_audio_sources(self):
        """Test that 'a' key opens audio sources screen."""
        with patch.object(meeting_assistant.MeetingAssistantApp, "detect_meetings"):
            with patch.object(meeting_assistant.PermissionManager, "check_screen_recording_permission", return_value=True):
                app = meeting_assistant.MeetingAssistantApp()

                with patch("subprocess.check_output") as mock_subprocess:
                    mock_subprocess.return_value = "No meeting"

                    async with app.run_test() as pilot:
                        await pilot.press("a")
                        await pilot.pause()

                        # Audio source screen should be open
                        mic_checkbox = app.screen.query_one("#mic_enabled")
                        assert mic_checkbox is not None

    @pytest.mark.asyncio
    async def test_keyboard_shortcut_transcripts(self):
        """Test that 't' key opens transcripts screen."""
        with patch.object(meeting_assistant.MeetingAssistantApp, "detect_meetings"):
            with patch.object(meeting_assistant.PermissionManager, "check_screen_recording_permission", return_value=True):
                app = meeting_assistant.MeetingAssistantApp()

                with patch("subprocess.check_output") as mock_subprocess:
                    mock_subprocess.return_value = "No meeting"

                    async with app.run_test() as pilot:
                        await pilot.press("t")
                        await pilot.pause()

                        # Transcripts screen should be open - check for transcript list
                        transcript_list = app.screen.query_one("#transcript_list")
                        assert transcript_list is not None

    @pytest.mark.asyncio
    async def test_keyboard_shortcut_focus_device(self):
        """Test that 'd' key focuses device selector."""
        with patch.object(meeting_assistant.MeetingAssistantApp, "detect_meetings"):
            with patch.object(meeting_assistant.PermissionManager, "check_screen_recording_permission", return_value=True):
                app = meeting_assistant.MeetingAssistantApp()

                with patch("subprocess.check_output") as mock_subprocess:
                    mock_subprocess.return_value = "No meeting"

                    async with app.run_test() as pilot:
                        await pilot.press("d")
                        await pilot.pause()

                        # Device selector should be focused
                        device_select = app.query_one("#device_select")
                        assert device_select.has_focus


class TestAudioSourceScreen:
    """Tests for the AudioSourceScreen modal."""

    @pytest.mark.asyncio
    async def test_audio_source_screen_opens(self):
        """Test that the AudioSourceScreen modal can be opened."""
        with patch.object(meeting_assistant.MeetingAssistantApp, "detect_meetings"):
            with patch.object(meeting_assistant.PermissionManager, "check_screen_recording_permission", return_value=True):
                app = meeting_assistant.MeetingAssistantApp()

                with patch("subprocess.check_output") as mock_subprocess:
                    mock_subprocess.return_value = "No meeting"

                    async with app.run_test() as pilot:
                        await pilot.press("a")  # Use keyboard shortcut
                        await pilot.pause()

                        # Query from the screen (modal), not the app
                        mic_checkbox = app.screen.query_one("#mic_enabled")
                        assert mic_checkbox is not None

    @pytest.mark.asyncio
    async def test_audio_source_screen_mic_checkbox(self):
        """Test toggling the microphone checkbox."""
        with patch.object(meeting_assistant.MeetingAssistantApp, "detect_meetings"):
            with patch.object(meeting_assistant.PermissionManager, "check_screen_recording_permission", return_value=True):
                app = meeting_assistant.MeetingAssistantApp()

                with patch("subprocess.check_output") as mock_subprocess:
                    mock_subprocess.return_value = "No meeting"

                    async with app.run_test() as pilot:
                        await pilot.press("a")  # Use keyboard shortcut
                        await pilot.pause()

                        mic_checkbox = app.screen.query_one("#mic_enabled")
                        assert mic_checkbox.value is True

                        await pilot.click("#mic_enabled")
                        await pilot.pause()

                        assert mic_checkbox.value is False

    @pytest.mark.asyncio
    async def test_audio_source_screen_system_audio_checkbox(self):
        """Test toggling the system audio checkbox."""
        with patch.object(meeting_assistant.MeetingAssistantApp, "detect_meetings"):
            with patch.object(meeting_assistant.PermissionManager, "check_screen_recording_permission", return_value=True):
                app = meeting_assistant.MeetingAssistantApp()

                with patch("subprocess.check_output") as mock_subprocess:
                    mock_subprocess.return_value = "No meeting"

                    async with app.run_test() as pilot:
                        await pilot.press("a")  # Use keyboard shortcut
                        await pilot.pause()

                        system_checkbox = app.screen.query_one("#system_enabled")
                        assert system_checkbox.value is True  # Default is now True

                        await pilot.click("#system_enabled")
                        await pilot.pause()

                        assert system_checkbox.value is False

    @pytest.mark.asyncio
    async def test_audio_source_screen_apply(self):
        """Test applying audio source configuration."""
        with patch.object(meeting_assistant.MeetingAssistantApp, "detect_meetings"):
            with patch.object(meeting_assistant.PermissionManager, "check_screen_recording_permission", return_value=True):
                app = meeting_assistant.MeetingAssistantApp()

                with patch("subprocess.check_output") as mock_subprocess:
                    mock_subprocess.return_value = "No meeting"

                    async with app.run_test() as pilot:
                        assert app.audio_config["system_enabled"] is True  # Default is now True

                        await pilot.press("a")  # Use keyboard shortcut
                        await pilot.pause()

                        await pilot.click("#system_enabled")  # Toggle to False
                        await pilot.pause()

                        await pilot.click("#btn_apply")
                        await pilot.pause()

                        assert app.audio_config["system_enabled"] is False

    @pytest.mark.asyncio
    async def test_audio_source_screen_cancel(self):
        """Test canceling audio source configuration."""
        with patch.object(meeting_assistant.MeetingAssistantApp, "detect_meetings"):
            with patch.object(meeting_assistant.PermissionManager, "check_screen_recording_permission", return_value=True):
                app = meeting_assistant.MeetingAssistantApp()

                with patch("subprocess.check_output") as mock_subprocess:
                    mock_subprocess.return_value = "No meeting"

                    async with app.run_test() as pilot:
                        assert app.audio_config["system_enabled"] is True  # Default is now True

                        await pilot.press("a")  # Use keyboard shortcut
                        await pilot.pause()

                        await pilot.click("#system_enabled")  # Toggle in dialog
                        await pilot.pause()

                        await pilot.click("#btn_cancel")  # Cancel should not apply changes
                        await pilot.pause()

                        assert app.audio_config["system_enabled"] is True  # Should remain unchanged


class TestAudioMixer:
    """Tests for the AudioMixer class."""

    def test_initialization(self):
        mixer = meeting_assistant.AudioMixer(sample_rate=16000)
        assert mixer.sample_rate == 16000
        assert mixer.sources == {}

    def test_add_remove_source(self):
        mixer = meeting_assistant.AudioMixer()
        mock_engine = MagicMock()
        mock_engine.running = True

        mixer.add_source("test", mock_engine)
        assert "test" in mixer.sources

        mixer.remove_source("test")
        assert "test" not in mixer.sources

    def test_get_mixed_audio_empty(self):
        mixer = meeting_assistant.AudioMixer()
        result = mixer.get_mixed_audio()
        assert result is None

from textual.command import Provider, Hit

class TestCommandPalette:

    @pytest.mark.asyncio
    async def test_navigation_provider_discover(self):
        """Verify that NavigationProvider.discover yields expected hits."""
        with patch.object(meeting_assistant.MeetingAssistantApp, "detect_meetings"), \
             patch.object(meeting_assistant.PermissionManager, "check_screen_recording_permission", return_value=True), \
             patch("subprocess.check_output", return_value="No meeting"):
            
            app = meeting_assistant.MeetingAssistantApp()
            screen = MagicMock()
            screen.app = app
            
            provider = meeting_assistant.NavigationProvider(screen)
            
            # Test discover (called when empty)
            hits = []
            async for hit in provider.discover():
                hits.append(hit)
            
            titles = [h.text for h in hits]
            assert "Settings" in titles
            assert "Transcripts" in titles
            assert "Record" in titles

    @pytest.mark.asyncio
    async def test_navigation_provider_search(self):
        """Verify that NavigationProvider returns expected hits."""
        
        # Patch detect_meetings and permissions
        with patch.object(meeting_assistant.MeetingAssistantApp, "detect_meetings"), \
             patch.object(meeting_assistant.PermissionManager, "check_screen_recording_permission", return_value=True), \
             patch("subprocess.check_output", return_value="No meeting"):
            
            app = meeting_assistant.MeetingAssistantApp()
            screen = MagicMock()
            screen.app = app
            
            # Instantiate provider directly - Provider(screen)
            provider = meeting_assistant.NavigationProvider(screen)
            
            # Search for "Settings"
            hits = []
            async for hit in provider.search("Settings"):
                hits.append(hit)
            assert any(hit.score > 0 for hit in hits), "Settings command not found"

    @pytest.mark.asyncio
    async def test_command_execution(self):
        """Verify that executing a command triggers the correct action."""
        with patch.object(meeting_assistant.MeetingAssistantApp, "detect_meetings"), \
             patch.object(meeting_assistant.PermissionManager, "check_screen_recording_permission", return_value=True), \
             patch("subprocess.check_output", return_value="No meeting"):
            
            app = meeting_assistant.MeetingAssistantApp()
            
            async with app.run_test() as pilot:
                screen = app.screen
                provider = meeting_assistant.NavigationProvider(screen)
                
                # Get the Settings command hit
                hits = []
                async for h in provider.search("Settings"):
                    hits.append(h)
                # Filter for the exact hit we want if fuzzy matching returns multiple
                # In this simple case, we just grab the first valid one
                settings_hit = next(h for h in hits if "Settings" in h.text)
                
                # Execute the callback
                settings_hit.command()
                
                await pilot.pause()
                
                # Verify Settings Screen opened
                assert isinstance(app.screen, meeting_assistant.SettingsScreen)

    def test_get_mixed_audio_single_source(self):
        mixer = meeting_assistant.AudioMixer()
        mock_engine = MagicMock()
        mock_engine.running = True
        mock_engine.get_audio_chunk.return_value = np.array([0.5, 0.5, 0.5], dtype="float32")

        mixer.add_source("test", mock_engine)
        result = mixer.get_mixed_audio()

        np.testing.assert_array_almost_equal(result, np.array([0.5, 0.5, 0.5]))

    def test_get_mixed_audio_multiple_sources(self):
        mixer = meeting_assistant.AudioMixer()

        mock_engine1 = MagicMock()
        mock_engine1.running = True
        mock_engine1.get_audio_chunk.return_value = np.array([0.4, 0.4], dtype="float32")

        mock_engine2 = MagicMock()
        mock_engine2.running = True
        mock_engine2.get_audio_chunk.return_value = np.array([0.6, 0.6], dtype="float32")

        mixer.add_source("mic", mock_engine1)
        mixer.add_source("system", mock_engine2)

        result = mixer.get_mixed_audio()

        # Should sum the two sources: 0.4 + 0.6 = 1.0
        np.testing.assert_array_almost_equal(result, np.array([1.0, 1.0]))
