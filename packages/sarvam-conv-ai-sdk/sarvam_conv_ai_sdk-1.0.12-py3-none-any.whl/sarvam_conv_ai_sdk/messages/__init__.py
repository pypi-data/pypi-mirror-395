"""Message types for SamvaadAgent SDK."""

from typing import Annotated, Any, Union

from pydantic import Field, TypeAdapter

from .actions import (
    ClientInteractionEndMsg,
    ClientInteractionStartMsg,
)
from .audio import (
    AudioEncoding,
    ClientAudioChunkMsg,
    ClientAudioMsg,
    ServerAudioChunkMsg,
)
from .base import ClientMsgBase, ServerMsgBase
from .config import CustomAppOverrides, InteractionConfig
from .events import (
    ServerEventBase,
    ServerInteractionConnectedEvent,
    ServerInteractionEndEvent,
    ServerUserInterruptEvent,
)
from .system import ClientPongMsg, ServerPingMsg
from .text import (
    ClientTextChunkMsg,
    ClientTextMsg,
    ClientTextMsgType,
    ServerTextChunkMsg,
    ServerTextMsg,
    ServerTextMsgType,
)
from .types import (
    SUPPORTED_SAMPLE_RATES,
    ClientMsgCategory,
    ClientMsgType,
    InteractionType,
    MsgStatus,
    ServerMsgCategory,
    ServerMsgType,
)

ServerMsg = Annotated[
    Union[
        ServerTextChunkMsg,
        ServerTextMsg,
        ServerAudioChunkMsg,
        ServerUserInterruptEvent,
        ServerInteractionConnectedEvent,
        ServerInteractionEndEvent,
        ServerPingMsg,
    ],
    Field(discriminator="type"),
]

ClientMsg = Annotated[
    Union[
        ClientTextChunkMsg,
        ClientTextMsg,
        ClientAudioChunkMsg,
        ClientAudioMsg,
        ClientInteractionStartMsg,
        ClientInteractionEndMsg,
        ClientPongMsg,
    ],
    Field(discriminator="type"),
]

_server_msg_adapter: TypeAdapter[ServerMsg] = TypeAdapter(ServerMsg)
_client_msg_adapter: TypeAdapter[ClientMsg] = TypeAdapter(ClientMsg)


def parse_server_message(data: dict[str, Any]) -> ServerMsg:
    """Parse a server message from a raw JSON-like dict.

    Args:
        data: Raw message dictionary from WebSocket

    Returns:
        A typed server message instance

    Raises:
        ValueError: If message type is unknown or parsing fails
    """
    try:
        return _server_msg_adapter.validate_python(data)
    except Exception as e:
        raise ValueError(f"Failed to parse server message: {e}") from e


def parse_client_message(data: dict[str, Any]) -> ClientMsg:
    """Parse a client message from a raw JSON-like dict.

    Args:
        data: Raw message dictionary

    Returns:
        A typed client message instance

    Raises:
        ValueError: If message type is unknown or parsing fails
    """
    try:
        return _client_msg_adapter.validate_python(data)
    except Exception as e:
        raise ValueError(f"Failed to parse client message: {e}") from e


__all__ = [
    "ClientMsgBase",
    "ServerMsgBase",
    "ServerMsgType",
    "ClientMsgType",
    "ServerMsgCategory",
    "ClientMsgCategory",
    "parse_server_message",
    "parse_client_message",
    "ServerMsg",
    "ClientMsg",
    "InteractionType",
    "ServerTextChunkMsg",
    "ServerTextMsg",
    "ClientTextMsg",
    "ClientTextMsgType",
    "ServerTextMsgType",
    "ClientTextChunkMsg",
    "AudioEncoding",
    "ServerAudioChunkMsg",
    "ClientAudioChunkMsg",
    "ClientAudioMsg",
    "ClientInteractionStartMsg",
    "ClientInteractionEndMsg",
    "ServerUserInterruptEvent",
    "ServerInteractionEndEvent",
    "ServerPingMsg",
    "ClientPongMsg",
    "MsgStatus",
    "InteractionConfig",
    "CustomAppOverrides",
    "ServerEventBase",
    "SUPPORTED_SAMPLE_RATES",
    "InteractionType",
    "ServerInteractionConnectedEvent",
]
