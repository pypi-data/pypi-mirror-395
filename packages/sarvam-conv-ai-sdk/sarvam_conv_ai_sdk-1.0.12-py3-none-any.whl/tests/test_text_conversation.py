"""
Minimal test cases for text-based conversation functionality.
"""

import time

import pytest

from sarvam_conv_ai_sdk import (
    InteractionConfig,
    InteractionType,
    ServerTextChunkMsg,
    ServerTextMsg,
)
from sarvam_conv_ai_sdk.messages.text import ClientTextMsg
from sarvam_conv_ai_sdk.messages.types import (
    ClientMsgType,
    MsgStatus,
    ServerMsgType,
    UserIdentifierType,
)
from sarvam_conv_ai_sdk.tool import SarvamToolLanguageName


class TestClientTextMessage:
    """Test client text message creation and serialization."""

    def test_create_text_message(self):
        """Test creating a simple text message."""
        message = ClientTextMsg(text="Hello", timestamp=time.time())

        assert message.text == "Hello"
        assert message.type == ClientMsgType.TEXT
        assert message.origin == "client"

    def test_serialize_text_message(self):
        """Test serializing text message to JSON."""
        message = ClientTextMsg(text="Test", timestamp=1234567890.0)
        json_data = message.model_dump()

        assert json_data["text"] == "Test"
        assert json_data["type"] == "client.media.text"
        assert json_data["origin"] == "client"
        assert json_data["timestamp"] == 1234567890.0


class TestServerTextMessage:
    """Test server text message parsing."""

    def test_parse_server_text_message(self):
        """Test parsing ServerTextMsg from JSON."""
        json_data = {
            "type": "server.media.text",
            "origin": "server",
            "timestamp": 1234567890.0,
            "text": "Hello from agent",
            "events": None,
        }

        message = ServerTextMsg(**json_data)

        assert message.text == "Hello from agent"
        assert message.type == ServerMsgType.TEXT
        assert message.origin == "server"

    def test_server_text_with_events(self):
        """Test ServerTextMsg with bundled events."""
        json_data = {
            "type": "server.media.text",
            "origin": "server",
            "timestamp": 1234567890.0,
            "text": "Booking confirmed",
            "events": [
                {
                    "type": "server.event.variable_update",
                    "variable_name": "booking_id",
                    "variable_value": "ABC123",
                }
            ],
        }

        message = ServerTextMsg(**json_data)

        assert message.text == "Booking confirmed"
        assert len(message.events) == 1
        assert message.events[0]["variable_name"] == "booking_id"


class TestServerTextChunk:
    """Test streaming text chunks."""

    def test_text_chunk_pending(self):
        """Test text chunk with pending status."""
        chunk = ServerTextChunkMsg(
            text="Hello",
            timestamp=time.time(),
            status=MsgStatus.PENDING,
        )

        assert chunk.text == "Hello"
        assert chunk.status == MsgStatus.PENDING
        assert chunk.type == ServerMsgType.TEXT_CHUNK

    def test_text_chunk_completed(self):
        """Test text chunk with completed status."""
        chunk = ServerTextChunkMsg(
            text=" World!",
            timestamp=time.time(),
            status=MsgStatus.COMPLETED,
        )

        assert chunk.text == " World!"
        assert chunk.status == MsgStatus.COMPLETED


class TestTextInteractionConfig:
    """Test text conversation configuration."""

    def test_text_mode_config(self):
        """Test creating config for text mode."""
        config = InteractionConfig(
            user_identifier="test_user",
            user_identifier_type=UserIdentifierType.CUSTOM,
            org_id="test_org",
            workspace_id="test_workspace",
            app_id="test_app",
            interaction_type=InteractionType.CHAT,
            sample_rate=16000,
        )

        assert config.interaction_type == InteractionType.CHAT
        assert config.user_identifier == "test_user"

    def test_text_config_with_language(self):
        """Test text config with initial language."""
        config = InteractionConfig(
            user_identifier="test_user",
            user_identifier_type=UserIdentifierType.CUSTOM,
            org_id="test_org",
            workspace_id="test_workspace",
            app_id="test_app",
            interaction_type=InteractionType.CHAT,
            initial_language_name=SarvamToolLanguageName.HINDI,
            sample_rate=16000,
        )

        assert config.interaction_type == InteractionType.CHAT
        assert config.initial_language_name == SarvamToolLanguageName.HINDI


class TestMessageTypes:
    """Test message type enums."""

    def test_client_text_type(self):
        """Test client text message type."""
        assert ClientMsgType.TEXT == "client.media.text"

    def test_server_text_type(self):
        """Test server text message type."""
        assert ServerMsgType.TEXT == "server.media.text"

    def test_interaction_type(self):
        """Test interaction type enum."""
        assert InteractionType.CHAT == "chat"
        assert InteractionType.CALL == "call"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
