"""Conversational AI agent implementation with WebSocket management.

This module provides the main AsyncSamvaadAgent class for managing real-time
conversations with voice using WebSocket connections.
"""

import asyncio
import base64
import json
import logging
import time
import urllib.parse
from typing import Any, Awaitable, Callable, Optional
from urllib.parse import parse_qsl, urlencode, urljoin, urlparse, urlunparse

import httpx
import websockets
from pydantic import SecretStr
from websockets.legacy.client import WebSocketClientProtocol
from websockets.protocol import State

from .audio_interface import AsyncAudioInterface
from .messages import (
    AudioEncoding,
    ClientAudioChunkMsg,
    ClientAudioMsg,
    ClientInteractionStartMsg,
    ClientMsgBase,
    ClientPongMsg,
    ClientTextMsg,
    InteractionConfig,
    ServerAudioChunkMsg,
    ServerEventBase,
    ServerInteractionConnectedEvent,
    ServerInteractionEndEvent,
    ServerPingMsg,
    ServerTextChunkMsg,
    ServerTextMsg,
    ServerTextMsgType,
    ServerUserInterruptEvent,
    parse_server_message,
)

logger = logging.getLogger(__name__)


class AsyncSamvaadAgent:
    """Main conversational agent class for real-time voice and text interactions.

    This class manages WebSocket connections, handles message routing, and provides
    callbacks for various conversation events. Simplified for v1 with server-side
    tool execution.

    Example:
        ```python
        async def handle_event(event: ServerEventBase):
            print(f"Event received: {event}")

        config = ClientInteractionStartMsg.create_config(
            app_id="support_agent_v1",
            interaction_type=InteractionType.CALL,
            agent_variables={"user_name": "Rahul"},
            initial_language="Hindi",
            initial_state="greeting"
        )

        agent = AsyncSamvaadAgent(
            app_id="support_agent_v1",
            api_key="sk_...",
            config=config,
        )

        await agent.start()
        # Conversation runs...
        await agent.stop()
        ```
    """  # noqa

    def __init__(
        self,
        *,
        api_key: SecretStr,
        config: InteractionConfig,
        audio_interface: Optional["AsyncAudioInterface"] = None,
        audio_callback: Optional[
            Callable[[ServerAudioChunkMsg], Awaitable[None]]
        ] = None,
        text_callback: Optional[Callable[[ServerTextMsgType], Awaitable[None]]] = None,
        event_callback: Optional[Callable[[ServerEventBase], Awaitable[None]]] = None,
        base_url: str = "https://apps.sarvam.ai/api/app-runtime/",
    ):
        """Initialize the conversational agent.

        Args:
            api_key: API key used to fetch a signed WebSocket URL
            config: Interaction start configuration
            audio_interface: Optional audio interface for automatic audio handling
            audio_callback: Optional callback for audio messages
            text_callback: Optional callback for text messages
            event_callback: Optional callback for event messages
            base_url: Base URL for HTTP API endpoints
        """  # noqa

        assert isinstance(config, InteractionConfig), (
            "config must be an instance of InteractionConfig"
        )

        self.api_key = api_key
        self.config = config
        self.base_url = base_url
        self.audio_interface = audio_interface
        self._interaction_id: Optional[str] = None

        # Callbacks
        self._audio_callback = audio_callback
        self._text_callback = text_callback
        self._event_callback = event_callback

        # Internal state
        # WebSocket connection
        self._ws: Optional[WebSocketClientProtocol] = None
        self._reference_id: Optional[str] = None
        self._should_stop = False
        self._ws_task: Optional[asyncio.Task] = None
        self.timestamp: float | None = None
        self._websocket_send_queue: asyncio.Queue[ClientMsgBase] = asyncio.Queue()
        # Receive-side audio queue and task
        self._audio_receive_queue: asyncio.Queue[ServerAudioChunkMsg] = asyncio.Queue()
        self._audio_receive_task: Optional[asyncio.Task] = None
        # Disconnection signaling
        self._disconnected_event: asyncio.Event | None = None
        # Connection signaling (set when WebSocket is open or interaction acked)
        self._connected_event: asyncio.Event | None = None

    @property
    def reference_id(self) -> str:
        if self._reference_id is None:
            raise Exception("Call SID is not set")
        return self._reference_id

    @reference_id.setter
    def reference_id(self, reference_id: str) -> None:
        self._reference_id = reference_id

    def _is_ws_closed(self) -> bool:
        """Check if the WebSocket connection is closed.

        Returns:
            True if the WebSocket is None or in CLOSED state, False otherwise
        """
        return self._ws is None or self._ws.state == State.CLOSED

    async def start(self) -> None:
        """Start the conversation session.

        This method:
        1. Gets a signed WebSocket URL via HTTP GET
        2. Connects to the WebSocket
        3. Sends the interaction_start message
        4. Starts the message receive loop

        Raises:
            Exception: If connection or initialization fails
        """
        logger.debug("Starting conversation session...")

        # Get signed URL for secure WebSocket connection
        signed_url, reference_id = await self._get_signed_url()
        self.reference_id = reference_id

        self._should_stop = False
        # Reset and create a new disconnected event for this session
        self._disconnected_event = asyncio.Event()
        # Reset and create a new connected event for this session
        self._connected_event = asyncio.Event()
        ws_url = self._augment_ws_url_with_params(signed_url)
        self._ws_task = asyncio.create_task(self._run_websocket_loop(ws_url))

        logger.debug(
            "Conversation session started - WebSocket connecting in background"
        )

    async def stop(self) -> None:
        """Stop the conversation session.

        This method:
        - Closes the WebSocket connection
        - Cancels background tasks
        - Cleans up resources
        """
        logger.debug("Stopping conversation session...")

        self._should_stop = True

        # Stop audio interface if provided
        if self.audio_interface:
            await self.audio_interface.stop()
            logger.debug("Audio interface stopped")

        if not self._is_ws_closed() and self._ws:
            await self._ws.close()

        if self._ws_task and not self._ws_task.done():
            self._ws_task.cancel()
            try:
                await self._ws_task
            except asyncio.CancelledError:
                pass
        # Signal disconnected
        if self._disconnected_event and not self._disconnected_event.is_set():
            self._disconnected_event.set()

    async def wait_for_disconnect(self) -> None:
        """Wait until the WebSocket disconnects or the agent is stopped."""
        if self._disconnected_event is None:
            # Not started yet; treat as already disconnected
            return
        await self._disconnected_event.wait()

    async def wait_for_connect(self, timeout: float | None = 5.0) -> bool:
        """Wait until the WebSocket connection is established.

        Args:
            timeout: Maximum seconds to wait. If None, wait indefinitely.

        Returns:
            True if the connection is established within the timeout, False otherwise.
        """
        # If already connected, return immediately
        if self.is_connected():
            return True
        if self._connected_event is None:
            # Not started or event not initialized
            self._connected_event = asyncio.Event()
        try:
            if timeout is None:
                await self._connected_event.wait()
            else:
                await asyncio.wait_for(self._connected_event.wait(), timeout)
        except asyncio.TimeoutError:
            return self.is_connected()
        return self.is_connected()

    async def send_audio(
        self,
        audio_data: bytes,
    ) -> None:
        """Send an audio chunk to the agent.

        Args:
            audio_data: Raw 16-bit PCM mono audio bytes at ``config.sample_rate``

        Raises:
            Exception: If WebSocket is not connected
        """
        if self._is_ws_closed():
            raise Exception("WebSocket is not connected")

        audio_base64 = base64.b64encode(audio_data).decode("utf-8")

        message = ClientAudioChunkMsg(
            audio_base64=audio_base64,
            format=AudioEncoding.LINEAR16,
            sample_rate=self.config.sample_rate,
            timestamp=time.time(),
        )
        self._websocket_send_queue.put_nowait(message)

    async def send_voice_note(
        self,
        audio_data: bytes,
        transcribe: bool = True,
    ) -> None:
        """Send a voice note to the agent for transcription.

        Args:
            audio_data: Raw 16-bit PCM mono audio bytes
            transcribe: Whether to transcribe the audio (default: True)

        Raises:
            Exception: If WebSocket is not connected
        """
        if self._is_ws_closed():
            raise Exception("WebSocket is not connected")

        audio_base64 = base64.b64encode(audio_data).decode("utf-8")

        message = ClientAudioMsg(
            audio_base64=audio_base64,
            format=AudioEncoding.LINEAR16,
            sample_rate=self.config.sample_rate,
            transcribe=transcribe,
            timestamp=time.time(),
        )
        self._websocket_send_queue.put_nowait(message)

    async def send_text(
        self,
        text: str,
    ) -> None:
        """Send a text message to the agent.

        Args:
            text: The text message to send.

        Raises:
            Exception: If WebSocket is not connected
        """
        if self._is_ws_closed():
            raise Exception("WebSocket is not connected")

        message = ClientTextMsg(
            text=text,
            timestamp=time.time(),
        )
        self._websocket_send_queue.put_nowait(message)

    def is_connected(self) -> bool:
        """Check if the WebSocket is currently connected.

        Returns:
            True if connected, False otherwise
        """
        return not self._is_ws_closed()

    def _construct_url(self) -> str:
        return urljoin(
            self.base_url,
            f"orgs/{self.config.org_id}/workspaces/{self.config.workspace_id}/apps/{self.config.app_id}/url",
        )

    def _augment_ws_url_with_params(self, ws_url: str) -> str:
        """Append required query params for the WebSocket connect URL."""
        parsed = urlparse(ws_url)
        existing_params = dict(parse_qsl(parsed.query))

        # Include required/optional params expected by server
        existing_params["user_identifier"] = self.config.user_identifier
        existing_params["user_identifier_type"] = self.config.user_identifier_type
        try:
            existing_params["sample_rate"] = str(int(self.config.sample_rate))
        except Exception:
            pass

        new_query = urlencode(existing_params)
        return urlunparse(
            (
                parsed.scheme,
                parsed.netloc,
                parsed.path,
                parsed.params,
                new_query,
                parsed.fragment,
            )
        )

    def get_interaction_id(self) -> Optional[str]:
        """Return the current interaction identifier for clients.

        In this SDK, the server associates the interaction with a server-side
        call session identifier. We expose the same value for client reference.
        """
        return self._interaction_id

    async def _get_signed_url(self) -> tuple[str, str]:
        """Get authenticated WebSocket URL and reference id from the API.

        Makes an HTTP GET request to get a time-limited signed URL for
        secure WebSocket connections without exposing the API key.
        Appends user identifier parameters to the signed URL.

        Returns:
            A tuple of (signed_websocket_url, reference_id)

        Raises:
            Exception: If the HTTP request fails
        """
        user_identifier = self.config.user_identifier
        user_identifier_type = self.config.user_identifier_type
        api_key = self.api_key
        url = self._construct_url()

        async with httpx.AsyncClient() as client:
            try:
                version = self.config.version
                if version:
                    params = {
                        "version": version,
                        "interaction_type": self.config.interaction_type.value,
                    }
                else:
                    params = {
                        "interaction_type": self.config.interaction_type.value,
                    }

                headers = {"X-API-Key": api_key.get_secret_value()}

                response = await client.get(
                    url,
                    params=params,
                    headers=headers,
                    timeout=30.0,
                )

                response.raise_for_status()

                data = response.json()

                signed_url = data["url"]
                reference_id = data["reference_id"]

                # add additional query parameters

                # Parse the signed URL and add user identifier params
                parsed_url = urllib.parse.urlparse(signed_url)
                query_params = urllib.parse.parse_qs(parsed_url.query)

                # Add additional query parameters
                query_params["user_identifier"] = [user_identifier]
                query_params["user_identifier_type"] = [user_identifier_type]
                query_params["sample_rate"] = [str(self.config.sample_rate)]
                query_params["interaction_type"] = [self.config.interaction_type.value]

                # Reconstruct the URL with updated query params
                new_query = urllib.parse.urlencode(query_params, doseq=True)
                modified_url = urllib.parse.urlunparse(
                    (
                        parsed_url.scheme,
                        parsed_url.netloc,
                        parsed_url.path,
                        parsed_url.params,
                        new_query,
                        parsed_url.fragment,
                    )
                )

                return modified_url, reference_id
            except httpx.HTTPStatusError as e:
                status_code = e.response.status_code
                logger.error(f"Failed to get signed URL: {status_code}")
                raise Exception(f"Failed to get signed URL: {status_code}")
            except Exception as e:
                logger.error(f"Error getting signed URL: {e}")
                raise

    async def _send_websocket_messages(self) -> None:
        """Send messages to the WebSocket."""
        while not self._should_stop:
            try:
                message = await self._websocket_send_queue.get()
                if self._ws is None or self._ws.state != State.OPEN:
                    continue
                message_json = message.model_dump_json()
                await self._ws.send(message_json)
            except websockets.exceptions.ConnectionClosed:
                logger.warning("WebSocket closed while sending; stopping sender")
                self._should_stop = True
                break
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.exception(f"Error sending websocket message: {e}")

    async def _process_audio_receive_queue(self) -> None:
        """Process audio messages received from the server via a queue."""
        while not self._should_stop:
            try:
                audio_msg = await self._audio_receive_queue.get()
                try:
                    await self._handle_audio(audio_msg)
                except Exception as e:
                    logger.exception(f"Error processing received audio: {e}")
            except asyncio.CancelledError:
                break

    async def _run_websocket_loop(self, ws_url: str) -> None:
        """Main WebSocket loop for receiving and processing messages.

        This method:
        1. Connects to the WebSocket
        2. Sends interaction_start
        3. Receives messages in a loop
        4. Routes messages to appropriate handlers
        5. Handles disconnections and errors

        Args:
            ws_url: The signed WebSocket URL to connect to
        """
        send_task: Optional[asyncio.Task] = None
        audio_recv_task: Optional[asyncio.Task] = None
        try:
            async with websockets.connect(ws_url) as ws:
                self._ws = ws
                logger.debug("WebSocket connected")
                # Signal connected as soon as WS is open
                try:
                    if self._connected_event and not self._connected_event.is_set():
                        self._connected_event.set()
                except Exception:
                    pass

                # Send interaction start
                await self._send_interaction_start()

                # Start audio interface if provided
                if self.audio_interface:
                    # Track chunks sent for periodic logging
                    self._client_audio_chunks_sent = 0
                    self._server_audio_chunks_received = 0

                    async def input_callback(
                        audio_data: bytes, frame_count: int
                    ) -> None:  # noqa
                        """Callback for audio input - sends directly to WebSocket."""  # noqa
                        try:
                            # Check if WebSocket is still open before sending
                            if ws.state != State.OPEN:
                                return

                            self._client_audio_chunks_sent += 1
                            await self.send_audio(audio_data)

                        except websockets.exceptions.ConnectionClosedOK:
                            # Connection closed gracefully, stop trying to send
                            pass
                        except websockets.exceptions.ConnectionClosedError:
                            # Connection closed with error, stop trying to send
                            pass
                        except Exception as e:
                            logger.error(
                                f"❌ Error in audio input callback: {e}",
                                exc_info=True,
                            )

                    await self.audio_interface.start(input_callback)

                send_task = asyncio.create_task(self._send_websocket_messages())
                audio_recv_task = asyncio.create_task(
                    self._process_audio_receive_queue()
                )
                self._audio_receive_task = audio_recv_task

                def _on_send_done(task: asyncio.Task) -> None:
                    try:
                        task.result()
                    except Exception:
                        logger.error(
                            "Send task failed; initiating shutdown", exc_info=True
                        )
                        try:
                            self._should_stop = True
                            if not self._is_ws_closed() and self._ws:
                                # schedule async close; cannot await in callback
                                asyncio.create_task(self._ws.close())
                        except Exception:
                            pass

                send_task.add_done_callback(_on_send_done)

                # Main receive loop
                while not self._should_stop:
                    try:
                        message_str = await asyncio.wait_for(ws.recv(), timeout=60.0)  # noqa

                        # Parse JSON string to dict
                        message = json.loads(message_str)

                        # Route message (parse_server_message expects dict)
                        await self._route_message(message)

                    except asyncio.TimeoutError:
                        # No message received in 60 seconds, continue
                        logger.debug("WebSocket receive timeout, continuing...")  # noqa
                        continue
                    except websockets.exceptions.ConnectionClosed:
                        self._should_stop = True
                        logger.warning("WebSocket connection closed")
                        break

        except Exception as e:
            logger.error(f"WebSocket loop error: {e}", exc_info=True)
            raise
        finally:
            self._ws = None
            logger.debug("WebSocket loop ended")
            # Signal disconnection at loop end
            if self._disconnected_event and not self._disconnected_event.is_set():
                self._disconnected_event.set()
            if send_task and not send_task.done():
                send_task.cancel()
                try:
                    await send_task
                except asyncio.CancelledError:
                    pass
            if audio_recv_task and not audio_recv_task.done():
                audio_recv_task.cancel()
                try:
                    await audio_recv_task
                except asyncio.CancelledError:
                    pass
            # Drain any pending audio messages
            try:
                while True:
                    self._audio_receive_queue.get_nowait()
            except asyncio.QueueEmpty:
                pass
            self._audio_receive_task = None

    async def _send_interaction_start(self) -> None:
        """Send the interaction start message.

        This is the first message sent after connecting to establish
        the conversation session with initial configuration.
        """
        if not self._ws:
            raise Exception("WebSocket not connected")

        # Update timestamp before sending
        # (config is already a ClientInteractionStartMsg)
        self.timestamp = time.time()

        message = ClientInteractionStartMsg.create_message_from_config(self.config)

        if not self._is_ws_closed():
            message_json = message.model_dump_json()
            await self._ws.send(message_json)

    async def _route_message(self, message: dict[str, Any]) -> None:
        """Route incoming messages to appropriate handlers using smart parser.

        Args:
            message: Raw JSON message from the server
        """
        try:
            # Parse message using smart parser
            parsed = parse_server_message(message)

            if isinstance(parsed, ServerTextChunkMsg):
                await self._handle_text(parsed)
            elif isinstance(parsed, ServerTextMsg):
                await self._handle_text(parsed)
            elif isinstance(parsed, ServerAudioChunkMsg):
                self._audio_receive_queue.put_nowait(parsed)
            elif isinstance(parsed, ServerInteractionEndEvent):
                await self._handle_interaction_end(parsed)
            elif isinstance(parsed, ServerPingMsg):
                await self._handle_ping(parsed)
            elif isinstance(parsed, ServerEventBase):
                await self._handle_event(parsed)
            else:
                logger.warning(f"Unknown message type: {parsed.type}")

        except ValueError as e:
            logger.error(f"Failed to parse server message: {e}")

    async def _handle_text(self, text_msg: ServerTextMsgType) -> None:
        """Handle text message from the agent.

        Args:
            text_msg: Parsed text message
        """
        try:
            logger.debug(f"Received text: {text_msg.text[:50]}...")

            # Call text callback if provided
            if self._text_callback:
                await self._text_callback(text_msg)

        except Exception as e:
            logger.error(f"Error handling text message: {e}", exc_info=True)

    async def _handle_audio(self, audio_msg: ServerAudioChunkMsg) -> None:
        """Handle audio message from the agent.

        Args:
            audio_msg: Parsed audio message
        """
        try:
            # Play through audio_interface if provided
            if not self.audio_interface and not self._audio_callback:
                logger.warning(
                    "No audio interface or callback provided - ignoring audio"
                )

            if self.audio_interface and audio_msg.audio_base64:
                audio_bytes = base64.b64decode(audio_msg.audio_base64)

                # Pass sample rate to audio interface for dynamic handling
                await self.audio_interface.output(
                    audio_bytes, sample_rate=audio_msg.sample_rate
                )

            elif self._audio_callback:
                await self._audio_callback(audio_msg)

        except Exception as e:
            logger.error(f"❌ Error handling audio message: {e}", exc_info=True)

    async def _handle_event(self, event: ServerEventBase) -> None:
        """Handle event message from the agent.

        Args:
            event: Parsed event message
        """
        if isinstance(event, ServerUserInterruptEvent) and self.audio_interface:
            self.audio_interface.interrupt()
        elif isinstance(event, ServerInteractionEndEvent):
            await self._handle_interaction_end(event)
        elif isinstance(event, ServerInteractionConnectedEvent):
            await self._handle_interaction_start_acknowledgement(event)
        if self._event_callback:
            await self._event_callback(event)

    async def _handle_interaction_start_acknowledgement(
        self, event: ServerInteractionConnectedEvent
    ) -> None:
        """Handle interaction connected event from server.

        Args:
            event: Parsed interaction connected message
        """
        self._interaction_id = event.interaction_id
        logger.debug(
            f"Interaction started with ID: {self._interaction_id}\n"
            f"Initial state: {event.initial_state_name}\n"
            f"Initial language: {event.initial_language_name}\n"
            f"Agent variables: {event.agent_variables}"
        )
        # Consider the session ready; ensure connected event is set
        try:
            if self._connected_event and not self._connected_event.is_set():
                self._connected_event.set()
        except Exception:
            pass

    async def _handle_interaction_end(self, end_msg: ServerInteractionEndEvent) -> None:
        """Handle interaction end message.

        Args:
            end_msg: Parsed interaction end message
        """
        pass

    async def _handle_ping(self, ping_msg: ServerPingMsg) -> None:
        """Handle ping message and send pong response.

        Implements latency measurement by tracking ping event times
        and responding immediately with pong.

        Args:
            ping_msg: Parsed ping message
        """
        try:
            # Send pong response immediately
            if not self._is_ws_closed():
                pong = ClientPongMsg(
                    event_id=ping_msg.event_id,
                    timestamp=time.time(),
                )
                pong_json = pong.model_dump_json()
                if not self._is_ws_closed() and self._ws:
                    await self._ws.send(pong_json)

        except Exception as e:
            logger.error(f"Error handling ping: {e}", exc_info=True)


async def create_conversation(
    config: InteractionConfig,
    api_key: SecretStr,
    audio_interface: Optional["AsyncAudioInterface"] = None,
    audio_callback: Optional[Callable[[ServerAudioChunkMsg], Awaitable[None]]] = None,
    text_callback: Optional[Callable[[ServerTextMsgType], Awaitable[None]]] = None,
) -> "AsyncSamvaadAgent":
    """Create and start an async conversation session.

    This is a convenience function that creates an AsyncSamvaadAgent instance
    and starts it immediately.

    Args:
        config: Interaction start configuration
        api_key: API key for authentication
        audio_interface: Optional audio interface for automatic audio handling
        audio_callback: Optional callback for audio messages
        text_callback: Optional callback for text messages

    Returns:
        Started AsyncSamvaadAgent instance

    Example:
        ```python
        config = InteractionConfig(...)
        agent = await create_conversation(
            config=config,
            api_key=SecretStr("sk_..."),
            audio_interface=audio_interface,
            audio_callback=audio_callback,
            text_callback=text_callback,
        )
        ```
    """
    agent = AsyncSamvaadAgent(
        api_key=api_key,
        config=config,
        audio_interface=audio_interface,
        audio_callback=audio_callback,
        text_callback=text_callback,
    )

    await agent.start()
    return agent
