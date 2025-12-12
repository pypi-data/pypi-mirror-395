from typing import Literal

from .base import ClientMsgBase, ServerMsgBase
from .types import ClientMsgType, MsgStatus, ServerMsgType


class ServerTextMsg(ServerMsgBase):
    type: Literal[ServerMsgType.TEXT] = ServerMsgType.TEXT
    text: str


class ServerTextChunkMsg(ServerMsgBase):
    type: Literal[ServerMsgType.TEXT_CHUNK] = ServerMsgType.TEXT_CHUNK
    text: str
    status: MsgStatus


class ClientTextMsg(ClientMsgBase):
    type: Literal[ClientMsgType.TEXT] = ClientMsgType.TEXT
    text: str


class ClientTextChunkMsg(ClientMsgBase):
    type: Literal[ClientMsgType.TEXT_CHUNK] = ClientMsgType.TEXT_CHUNK
    text: str
    status: MsgStatus


ServerTextMsgType = ServerTextChunkMsg | ServerTextMsg
ClientTextMsgType = ClientTextChunkMsg | ClientTextMsg
