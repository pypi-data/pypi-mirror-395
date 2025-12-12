"""Default audio interface implementations using PyAudio."""

import asyncio
import logging
from typing import Any, Awaitable, Callable, Optional

from .audio_interface import AsyncAudioInterface
from .messages.types import OUTPUT_SAMPLE_RATE

logger = logging.getLogger(__name__)

try:
    import pyaudio  # type: ignore[import-untyped]

    PYAUDIO_AVAILABLE = True
except ImportError:
    PYAUDIO_AVAILABLE = False
    logger.warning("PyAudio not available. Local audio streaming will not work.")


class AsyncDefaultAudioInterface(AsyncAudioInterface):
    """Default async audio interface using PyAudio.

    Handles audio input from microphone and output to speakers automatically.
    Uses PyAudio for cross-platform audio support.

    Args:
        input_sample_rate: Microphone input
            sample rate in Hz (default: 16000)
        input_frame_buffer_duration_ms: Input buffer duration
            in milliseconds (default: 20)
        output_frame_buffer_duration_ms: Output buffer duration
            in milliseconds (default: 62.5)
    """

    def __init__(
        self,
        input_sample_rate: int = 16000,
        input_frame_buffer_duration_ms: float = 20,
        output_frame_buffer_duration_ms: float = 62.5,
    ):  # noqa
        if not PYAUDIO_AVAILABLE:
            raise ImportError("To use DefaultAudioInterface you must install pyaudio.")

        self.input_sample_rate = input_sample_rate
        self.output_sample_rate = OUTPUT_SAMPLE_RATE
        self.input_frame_buffer_duration_ms = input_frame_buffer_duration_ms
        self.output_frame_buffer_duration_ms = output_frame_buffer_duration_ms
        # The frame buffer defines the amount of audio we should store in
        # the buffer we send audio to the server.
        self.INPUT_FRAMES_PER_BUFFER = int(
            input_frame_buffer_duration_ms * 0.001 * input_sample_rate
        )
        self.OUTPUT_FRAMES_PER_BUFFER = int(
            output_frame_buffer_duration_ms * 0.001 * OUTPUT_SAMPLE_RATE
        )

        self.output_queue: Optional[asyncio.Queue] = None
        self.should_stop: Optional[asyncio.Event] = None
        self.output_task: Optional[asyncio.Task] = None
        self.p: Optional[Any] = None  # PyAudio instance
        self.input_stream: Optional[Any] = None  # PyAudio input stream
        self.output_stream: Optional[Any] = None  # PyAudio output stream
        # Will capture the event loop during start()
        self.loop: Optional[asyncio.AbstractEventLoop] = None
        # Track number of input frames
        self.input_frame_count = 0
        # Track current output stream sample rate
        self.current_output_sample_rate = OUTPUT_SAMPLE_RATE

    async def start(self, input_callback: Callable[[bytes, int], Awaitable[None]]):  # noqa
        """Start audio input and output streams."""
        self.loop = asyncio.get_running_loop()

        self.input_callback = input_callback
        self.output_queue = asyncio.Queue()  # (audio_data, sample_rate)
        self.should_stop = asyncio.Event()

        self.p = pyaudio.PyAudio()
        self.input_stream = self.p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.input_sample_rate,
            input=True,
            stream_callback=self._pyaudio_input_callback,
            frames_per_buffer=self.INPUT_FRAMES_PER_BUFFER,
            start=True,
        )
        self.output_stream = self.p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.output_sample_rate,
            output=True,
            frames_per_buffer=self.OUTPUT_FRAMES_PER_BUFFER,
            start=True,
        )

        # Start the output task
        self.output_task = asyncio.create_task(self._output_task())

    async def stop(self):
        """Stop audio streams and cleanup resources."""
        # Check if audio interface was actually started
        if self.should_stop is None:
            return  # Never started, nothing to stop

        self.should_stop.set()
        if self.output_task:
            self.output_task.cancel()
            try:
                await self.output_task
            except asyncio.CancelledError:
                pass
        self.input_stream.stop_stream()
        self.input_stream.close()
        self.output_stream.close()
        self.p.terminate()

    async def output(self, audio: bytes, sample_rate: Optional[int] = None):
        """Queue audio for playback.

        Args:
            audio: Audio data bytes
            sample_rate: Sample rate of the audio. If different from current
                output stream, the stream will be recreated with the new
                sample rate.
        """
        if sample_rate is None:
            sample_rate = self.output_sample_rate

        # Check if we need to change sample rate
        if sample_rate != self.current_output_sample_rate:
            await self._recreate_output_stream(sample_rate)

        if self.output_queue:
            await self.output_queue.put((audio, sample_rate))

    def interrupt(self):
        """
        Stop current playback by removing one queued audio chunk if present.
        """
        if not self.output_queue:
            return
        try:
            _ = self.output_queue.get_nowait()
        except asyncio.QueueEmpty:
            pass

    async def _recreate_output_stream(self, new_sample_rate: int):
        """Recreate the output stream with a new sample rate.

        Args:
            new_sample_rate: New sample rate in Hz
        """
        # Close the old stream
        if self.output_stream:
            self.output_stream.stop_stream()
            self.output_stream.close()

        # Calculate new buffer size based on configured duration (ms)
        new_buffer_size = max(
            1,
            int(new_sample_rate * (self.output_frame_buffer_duration_ms * 0.001)),
        )

        # Create new stream with new sample rate
        if self.p:
            self.output_stream = self.p.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=new_sample_rate,
                output=True,
                frames_per_buffer=new_buffer_size,
                start=True,
            )

        self.current_output_sample_rate = new_sample_rate

    async def _output_task(self):
        """Background task that writes audio from queue to output stream."""
        try:
            while self.should_stop and not self.should_stop.is_set():
                audio_data, sample_rate = await self.output_queue.get()
                # Check if we need to recreate stream for this sample rate
                if sample_rate != self.current_output_sample_rate:
                    await self._recreate_output_stream(sample_rate)

                self.output_stream.write(audio_data)
        except asyncio.CancelledError:
            pass

    def _pyaudio_input_callback(self, in_data, frame_count, time_info, status):
        """PyAudio callback for input audio. Runs in PyAudio's thread."""
        self.input_frame_count += 1

        if self.input_callback and self.loop:
            # Schedule the async callback to run in the event loop
            # We use the captured loop from start()
            # and run_coroutine_threadsafe
            # to schedule the coroutine from this thread
            try:
                future = asyncio.run_coroutine_threadsafe(
                    self.input_callback(in_data, self.input_frame_count),
                    self.loop,
                )
                # Check if the future completed with an exception
                # (non-blocking)
                # This helps us catch errors in send_audio_chunk
                try:
                    # Wait briefly to catch immediate exceptions
                    future.result(timeout=0.001)
                except TimeoutError:
                    # Normal case - coroutine is still running
                    pass
                except Exception as e:
                    logger.error(
                        f"❌ Error in input callback: {e}",
                        exc_info=True,
                    )

            except Exception as e:
                # If scheduling fails, log but don't crash
                logger.error(
                    f"❌ Failed to schedule audio input: {e}",
                    exc_info=True,
                )
        elif not self.loop:
            if self.input_frame_count == 1:
                logger.warning(
                    "⚠️  No event loop captured yet- audio input will not be sent"  # noqa
                )
        return (None, pyaudio.paContinue)
