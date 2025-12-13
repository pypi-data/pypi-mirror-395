#!/usr/bin/env python3
"""
Diagnostic test for system audio capture.

This test monitors the ScreenCaptureKit audio capture over time to identify
why recording stops after a few seconds.

Run with: uv run python test_system_audio_capture.py
"""

import time
import threading
import queue
import numpy as np
import objc
from Foundation import NSObject
import ScreenCaptureKit as SCK
import CoreMedia
from dispatch import dispatch_queue_create, DISPATCH_QUEUE_SERIAL
from scipy import signal


class DiagnosticDelegate(NSObject):
    """Delegate that tracks audio frame reception with detailed diagnostics."""

    def initWithQueue_(self, audio_queue):
        self = objc.super(DiagnosticDelegate, self).init()
        if self is None:
            return None
        self._audio_queue = audio_queue
        self._frame_count = 0
        self._error_count = 0
        self._last_frame_time = None
        self._start_time = time.time()
        return self

    def stream_didOutputSampleBuffer_ofType_(self, stream, sampleBuffer, outputType):
        """Called when a new sample buffer is available."""
        current_time = time.time()

        # Log all callbacks for debugging (more verbose)
        elapsed = current_time - self._start_time
        if self._frame_count < 10 or self._frame_count % 100 == 0:
            print(f"[DELEGATE] t={elapsed:.2f}s frame={self._frame_count} type={outputType}", flush=True)

        if outputType == 1:  # Audio
            self._frame_count += 1
            self._last_frame_time = current_time

            # Extract audio data
            try:
                block_buffer = CoreMedia.CMSampleBufferGetDataBuffer(sampleBuffer)
                if block_buffer is None:
                    print(f"[DELEGATE] block_buffer is None", flush=True)
                    self._audio_queue.put(('error', 'block_buffer is None'))
                    return

                length = CoreMedia.CMBlockBufferGetDataLength(block_buffer)
                if length == 0:
                    print(f"[DELEGATE] length is 0", flush=True)
                    self._audio_queue.put(('error', 'length is 0'))
                    return

                result = CoreMedia.CMBlockBufferCopyDataBytes(block_buffer, 0, length, None)

                if self._frame_count <= 5:
                    print(f"[DELEGATE] CopyDataBytes result type: {type(result).__name__}", flush=True)

                if isinstance(result, tuple) and len(result) > 1:
                    status, data = result[0], result[1]
                    if status == 0 and data is not None:
                        audio_array = np.frombuffer(data, dtype=np.float32)
                        event = ('audio', {
                            'frame': self._frame_count,
                            'time': current_time - self._start_time,
                            'samples': len(audio_array),
                            'max_amplitude': float(np.abs(audio_array).max()),
                            'mean_amplitude': float(np.abs(audio_array).mean()),
                        })
                        self._audio_queue.put(event)
                        if self._frame_count <= 5:
                            print(f"[DELEGATE] Queued event: samples={len(audio_array)}, queue_size={self._audio_queue.qsize()}", flush=True)
                    else:
                        print(f"[DELEGATE] CopyDataBytes failed: status={status}", flush=True)
                        self._audio_queue.put(('error', f'CopyDataBytes failed: status={status}'))
                else:
                    print(f"[DELEGATE] Unexpected result: {type(result)}", flush=True)
                    self._audio_queue.put(('error', f'Unexpected result type: {type(result)}'))

            except Exception as e:
                self._error_count += 1
                print(f"[DELEGATE] Exception: {e}", flush=True)
                self._audio_queue.put(('error', str(e)))

    def stream_didStopWithError_(self, stream, error):
        """Called when the stream stops."""
        if error:
            self._audio_queue.put(('stream_stopped', str(error)))
        else:
            self._audio_queue.put(('stream_stopped', 'no error'))


class SystemAudioCaptureTest:
    """Test harness for system audio capture diagnostics."""

    def __init__(self):
        self.audio_queue = queue.Queue()
        self.global_refs = {}  # Prevent garbage collection
        self.stream = None
        self.delegate = None
        self.running = False
        self.setup_error = None
        self.setup_complete = threading.Event()

    def start(self):
        """Start the audio capture."""
        self.running = True
        self.setup_complete.clear()
        self.setup_error = None

        def on_content(content, error):
            if error:
                self.setup_error = f"Failed to get shareable content: {error}"
                self.setup_complete.set()
                return

            try:
                self._setup_stream(content)
            except Exception as e:
                self.setup_error = f"Setup exception: {e}"
                self.setup_complete.set()

        SCK.SCShareableContent.getShareableContentWithCompletionHandler_(on_content)

        # Wait for setup
        self.setup_complete.wait(timeout=10)
        return self.setup_error is None

    def _setup_stream(self, content):
        """Set up the SCStream."""
        # Keep strong reference to content
        self.global_refs['content'] = content

        displays = content.displays()
        if not displays:
            self.setup_error = "No displays found"
            self.setup_complete.set()
            return

        display = displays[0]

        # Create content filter
        content_filter = SCK.SCContentFilter.alloc().initWithDisplay_excludingWindows_(
            display, []
        )
        self.global_refs['filter'] = content_filter

        # Configure stream
        config = SCK.SCStreamConfiguration.alloc().init()
        config.setCapturesAudio_(True)
        config.setExcludesCurrentProcessAudio_(True)
        config.setSampleRate_(48000)
        config.setChannelCount_(2)
        config.setWidth_(2)
        config.setHeight_(2)
        config.setMinimumFrameInterval_(CoreMedia.CMTimeMake(1, 1))
        config.setShowsCursor_(False)
        self.global_refs['config'] = config

        # Create delegate with audio queue
        self.delegate = DiagnosticDelegate.alloc().initWithQueue_(self.audio_queue)
        self.global_refs['delegate'] = self.delegate

        # Create stream - pass delegate to constructor!
        self.stream = SCK.SCStream.alloc().initWithFilter_configuration_delegate_(
            content_filter, config, self.delegate
        )
        self.global_refs['stream'] = self.stream

        if self.stream is None:
            self.setup_error = "Failed to create SCStream"
            self.setup_complete.set()
            return

        # Create dispatch queue
        dispatch_queue = dispatch_queue_create(b"test.audio", DISPATCH_QUEUE_SERIAL)
        self.global_refs['dispatch_queue'] = dispatch_queue

        # Add audio output
        result = self.stream.addStreamOutput_type_sampleHandlerQueue_error_(
            self.delegate, 1, dispatch_queue, None
        )
        success = result[0] if isinstance(result, tuple) else result
        if not success:
            self.setup_error = "Failed to add audio output"
            self.setup_complete.set()
            return

        # Start capture
        def start_completion(error):
            if error:
                self.setup_error = f"Start capture failed: {error}"
            self.setup_complete.set()

        self.stream.startCaptureWithCompletionHandler_(start_completion)

    def stop(self):
        """Stop the audio capture."""
        self.running = False
        if self.stream:
            def stop_completion(error):
                pass
            try:
                self.stream.stopCaptureWithCompletionHandler_(stop_completion)
            except Exception:
                pass
            self.stream = None

    def get_events(self, timeout=0.1):
        """Get all pending events from the queue."""
        events = []
        # Use non-blocking get with sleep to avoid GIL/threading issues
        # with pyobjc dispatch queues
        end_time = time.time() + timeout
        while time.time() < end_time:
            try:
                event = self.audio_queue.get_nowait()
                events.append(event)
            except queue.Empty:
                if not events:
                    # Only sleep if we haven't gotten any events yet
                    time.sleep(0.01)
                else:
                    break
        return events


def log(msg):
    """Print with flush for immediate output."""
    print(msg, flush=True)


def run_diagnostic_test(duration=15):
    """
    Run a diagnostic test for the specified duration.

    Args:
        duration: How long to capture audio in seconds
    """
    log("=" * 60)
    log("System Audio Capture Diagnostic Test")
    log("=" * 60)
    log(f"Test duration: {duration} seconds")
    log("Make sure Screen Recording permission is granted.")
    log("Play some audio during this test for best results.")
    log("")

    test = SystemAudioCaptureTest()

    log("Starting capture...")
    if not test.start():
        log(f"ERROR: Failed to start capture: {test.setup_error}")
        return False

    log("Capture started successfully!")
    log(f"Delegate: {test.delegate}")
    log(f"Stream: {test.stream}")
    log("")
    log("Monitoring audio frames...")
    log("-" * 60)

    start_time = time.time()
    last_report_time = start_time
    total_frames = 0
    total_errors = 0
    frames_per_second = []
    current_second_frames = 0
    current_second_start = start_time
    last_frame_time = None
    gap_detected = False
    stream_stopped = False

    try:
        iteration = 0
        while time.time() - start_time < duration:
            iteration += 1
            events = test.get_events(timeout=0.5)

            if iteration <= 3 or events:
                log(f"  [LOOP] iter={iteration} events={len(events)} queue_size={test.audio_queue.qsize()}")

            for event_type, event_data in events:
                if event_type == 'audio':
                    total_frames += 1
                    current_second_frames += 1
                    last_frame_time = time.time()

                    # Check for gaps
                    if gap_detected:
                        log(f"  [RESUMED] Audio resumed after gap at t={event_data['time']:.1f}s")
                        gap_detected = False

                elif event_type == 'error':
                    total_errors += 1
                    log(f"  [ERROR] {event_data}")

                elif event_type == 'stream_stopped':
                    stream_stopped = True
                    log(f"  [STREAM STOPPED] {event_data}")

            # Per-second reporting
            current_time = time.time()
            if current_time - current_second_start >= 1.0:
                elapsed = current_time - start_time
                frames_per_second.append(current_second_frames)

                # Check for frame gap
                if last_frame_time and current_time - last_frame_time > 1.0:
                    gap_detected = True
                    log(f"  [GAP DETECTED] No frames for {current_time - last_frame_time:.1f}s")

                status = "OK" if current_second_frames > 0 else "NO FRAMES"
                log(f"  t={elapsed:5.1f}s | frames={current_second_frames:3d} | total={total_frames:5d} | errors={total_errors} | {status}")

                current_second_frames = 0
                current_second_start = current_time

            # Early exit if stream stopped
            if stream_stopped:
                log("\nStream stopped unexpectedly!")
                break

    except KeyboardInterrupt:
        log("\nTest interrupted by user")

    finally:
        test.stop()

    # Summary
    log("-" * 60)
    log("\nTest Summary:")
    log(f"  Total duration: {time.time() - start_time:.1f}s")
    log(f"  Total frames received: {total_frames}")
    log(f"  Total errors: {total_errors}")
    log(f"  Stream stopped unexpectedly: {stream_stopped}")

    if frames_per_second:
        log(f"  Avg frames/sec: {np.mean(frames_per_second):.1f}")
        log(f"  Min frames/sec: {min(frames_per_second)}")
        log(f"  Max frames/sec: {max(frames_per_second)}")

        # Detect drop-off pattern
        if len(frames_per_second) >= 3:
            first_half = frames_per_second[:len(frames_per_second)//2]
            second_half = frames_per_second[len(frames_per_second)//2:]

            first_avg = np.mean(first_half) if first_half else 0
            second_avg = np.mean(second_half) if second_half else 0

            if first_avg > 0 and second_avg < first_avg * 0.5:
                log(f"\n  WARNING: Frame rate dropped significantly!")
                log(f"    First half avg: {first_avg:.1f} frames/sec")
                log(f"    Second half avg: {second_avg:.1f} frames/sec")

        # Check for complete stops
        zero_seconds = sum(1 for f in frames_per_second if f == 0)
        if zero_seconds > 0:
            log(f"\n  WARNING: {zero_seconds} second(s) with zero frames!")

    log("=" * 60)

    return total_frames > 0 and not stream_stopped


if __name__ == "__main__":
    import sys

    duration = 10
    if len(sys.argv) > 1:
        try:
            duration = int(sys.argv[1])
        except ValueError:
            log(f"Usage: {sys.argv[0]} [duration_seconds]")
            sys.exit(1)

    success = run_diagnostic_test(duration)
    sys.exit(0 if success else 1)
