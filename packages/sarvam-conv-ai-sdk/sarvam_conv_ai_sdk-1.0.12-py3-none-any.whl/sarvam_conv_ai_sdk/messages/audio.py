from typing import Literal, Optional

from pydantic import Field

from .base import ClientMsgBase, ServerMsgBase
from .types import (
    AudioEncoding,
    ClientMsgType,
    MsgStatus,
    SampleRate,
    ServerMsgType,
)


class ClientAudioChunkMsg(ClientMsgBase):
    type: Literal[ClientMsgType.AUDIO_CHUNK] = ClientMsgType.AUDIO_CHUNK
    audio_base64: str
    format: AudioEncoding
    sample_rate: SampleRate


class ClientAudioMsg(ClientMsgBase):
    type: Literal[ClientMsgType.AUDIO] = ClientMsgType.AUDIO
    audio_base64: str
    format: AudioEncoding
    sample_rate: SampleRate
    transcribe: bool = False


class ServerAudioChunkMsg(ServerMsgBase):
    type: Literal[ServerMsgType.AUDIO_CHUNK] = ServerMsgType.AUDIO_CHUNK
    audio_base64: str = Field(default="")
    format: AudioEncoding
    sample_rate: Optional[SampleRate] = Field(default=None)
    status: MsgStatus
