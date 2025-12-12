from enum import IntEnum, StrEnum
from typing import Annotated

from pydantic import Field


class AudioEncoding(StrEnum):
    """Types of audio encoding allowed"""

    LINEAR16 = "audio/wav"


class SupportedSampleRate(IntEnum):
    RATE_8KHZ = 8000
    RATE_16KHZ = 16000
    RATE_48KHZ = 48000


# Keep for backward compatibility
SUPPORTED_SAMPLE_RATES = [rate.value for rate in SupportedSampleRate]


OUTPUT_SAMPLE_RATE = 16000


def validate_sample_rate(value_int: int) -> int:
    """Validate sample rate."""
    if value_int not in SUPPORTED_SAMPLE_RATES:
        raise ValueError(
            f"Sample rate {value_int} not supported. Supported rates: {SUPPORTED_SAMPLE_RATES}"  # noqa
        )
    return value_int


SampleRate = Annotated[int, Field(validate_call=validate_sample_rate)]


class ServerMsgCategory(StrEnum):
    """Types of msgs server can send."""

    MEDIA = "media"
    ACTION = "action"
    SYSTEM = "system"
    EVENT = "event"


class MsgStatus(StrEnum):
    """Status of the stream."""

    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class ClientMsgCategory(StrEnum):
    """Types of msgs client can send."""

    # Media msgs: audio, text, widget responses, etc.
    MEDIA = "media"
    # Client-side actions (tool run, UI action, etc.)
    ACTION = "action"
    # system msgs
    SYSTEM = "system"


class MsgOrigin(StrEnum):
    """Origin of the msg."""

    SERVER = "server"
    CLIENT = "client"


class ServerMsgType(StrEnum):
    """Types of msgs server can send."""

    # Media msgs
    AUDIO_CHUNK = "server.media.audio_chunk"
    AUDIO = "server.media.audio"
    TEXT = "server.media.text"
    TEXT_CHUNK = "server.media.text_chunk"

    PING = "server.system.ping"

    INTERACTION_END = "server.action.interaction_end"
    INTERACTION_CONNECTED = "server.action.interaction_connected"

    USER_SPEECH_START = "server.event.user_speech_start"
    USER_SPEECH_END = "server.event.user_speech_end"
    USER_INTERRUPT = "server.event.user_interrupt"
    VARIABLE_UPDATE = "server.event.variable_update"
    LANGUAGE_CHANGE = "server.event.language_change"
    STATE_TRANSITION = "server.event.state_transition"
    KB_QUERY = "server.event.kb_query"
    TOOL_CALL = "server.event.tool_call"


class ClientMsgType(StrEnum):
    """Types of msgs client can send."""

    # Media msgs
    AUDIO_CHUNK = "client.media.audio_chunk"
    TEXT = "client.media.text"
    TEXT_CHUNK = "client.media.text_chunk"
    AUDIO = "client.media.audio"

    # Action msgs
    INTERACTION_START = "client.action.interaction_start"
    INTERACTION_END = "client.action.interaction_end"
    VARIABLE_UPDATE = "client.action.variable_update"
    LANGUAGE_CHANGE = "client.action.language_change"
    STATE_TRANSITION = "client.action.state_transition"

    # System msgs
    PONG = "client.system.pong"


class InteractionType(StrEnum):
    """Type of interaction."""

    CALL = "call"
    CHAT = "chat"


class UserIdentifierType(StrEnum):
    """Type of user identifier."""

    PHONE_NUMBER = "phone_number"
    EMAIL = "email"
    CUSTOM = "custom"
    UNKNOWN = "unknown"
