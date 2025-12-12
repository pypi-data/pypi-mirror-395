from typing import Literal

from pydantic import BaseModel

from .types import ClientMsgType, MsgOrigin, ServerMsgType


class MsgBase(BaseModel):
    """Base class for all msgs."""

    timestamp: float


class ClientMsgBase(MsgBase):
    """Base class for all client msgs."""

    origin: Literal[MsgOrigin.CLIENT] = MsgOrigin.CLIENT
    type: ClientMsgType


class ServerMsgBase(MsgBase):
    """Base class for all server msgs."""

    origin: Literal[MsgOrigin.SERVER] = MsgOrigin.SERVER
    type: ServerMsgType
