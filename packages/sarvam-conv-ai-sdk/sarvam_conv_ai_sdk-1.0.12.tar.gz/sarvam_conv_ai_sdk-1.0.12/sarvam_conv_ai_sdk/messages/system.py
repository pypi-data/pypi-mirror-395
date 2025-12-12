"""System messages for heartbeat and latency measurement."""

from typing import Literal

from pydantic import Field

from .base import ClientMsgBase, ServerMsgBase
from .types import ClientMsgType, ServerMsgType


class ServerPingMsg(ServerMsgBase):
    """Latency measurement ping from server."""

    type: Literal[ServerMsgType.PING] = ServerMsgType.PING
    event_id: int = Field(description="Ping event id sent by the server to the client")


class ClientPongMsg(ClientMsgBase):
    """Response to latency ping."""

    type: Literal[ClientMsgType.PONG] = ClientMsgType.PONG
    event_id: int = Field(
        description=(
            "Use the same event id as the Ping "
            "Event id sent by the server in `ServerPingMsg`"
        )
    )
