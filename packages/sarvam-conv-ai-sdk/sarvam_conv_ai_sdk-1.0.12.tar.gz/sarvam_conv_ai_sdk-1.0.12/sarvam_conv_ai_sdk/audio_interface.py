"""Audio interface abstractions for handling audio input and output."""

from abc import ABC, abstractmethod
from typing import Awaitable, Callable, Optional


class AsyncAudioInterface(ABC):
    """Asynchronous AudioInterface for handling audio input and output.

    Use this interface with AsyncSamvaadAgent (asynchronous conversation).
    """

    input_callback: Callable[
        [bytes, int], Awaitable[None]
    ]  # Defined by the AsyncSamvaadAgent Class

    @abstractmethod
    async def start(self, input_callback: Callable[[bytes, int], Awaitable[None]]):  # noqa
        """Starts the audio interface.

        Called one time before the conversation starts.
        The `input_callback` should be called regularly with input audio chunks from
        the user. The audio should be in 16-bit PCM mono format. Recommended
        chunk size is around 20 milliseconds.

        Args:
            input_callback: Asynchronous callback to send audio chunks to the server.
                Takes audio data (bytes) and frame count (int) as parameters.
                This callback is provided by the AsyncSamvaadAgent Class.
                This callback takes the bytes and sends it to the server
        """  # noqa
        pass

    @abstractmethod
    async def stop(self):
        """Stops the audio interface.

        Called one time after the conversation ends. Should clean up any resources
        used by the audio interface and stop any audio streams. Do not call the
        `input_callback` from `start` after this method is called.
        """  # noqa
        pass

    @abstractmethod
    async def output(self, audio: bytes, sample_rate: Optional[int] = None):
        """Output audio to the user.

        The `audio` input is in 16-bit PCM mono format. Implementations can
        choose to do additional buffering. This method should return quickly and must
        not block the event loop.

        Args:
            audio: Audio data in 16-bit PCM mono format
            sample_rate: Sample rate of the audio in Hz (e.g., 16000, 8000)
        """  # noqa
        pass

    @abstractmethod
    def interrupt(self):
        """Interruption signal to stop any audio output.

        User has interrupted the agent and all previously buffered audio output should
        be stopped.
        """  # noqa
        pass
