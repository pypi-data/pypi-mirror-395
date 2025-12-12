from typing import Literal

from .base import ServerMsgBase
from .config import CustomAppOverrides
from .types import ServerMsgType


class ServerEventBase(ServerMsgBase):
    """Base class for all server events."""

    pass


class ServerUserInterruptEvent(ServerEventBase):
    """Signals that the user interrupted the agent (e.g., barge-in).

    Clients should stop any ongoing playback immediately.
    """

    type: Literal[ServerMsgType.USER_INTERRUPT] = ServerMsgType.USER_INTERRUPT


class ServerInteractionEndEvent(ServerEventBase):
    """Conversation session has ended."""

    type: Literal[ServerMsgType.INTERACTION_END] = ServerMsgType.INTERACTION_END  # noqa


class ServerInteractionConnectedEvent(ServerEventBase, CustomAppOverrides):
    """Conversation session has started."""

    type: Literal[ServerMsgType.INTERACTION_CONNECTED] = (
        ServerMsgType.INTERACTION_CONNECTED
    )
    reference_id: str
    interaction_id: str
