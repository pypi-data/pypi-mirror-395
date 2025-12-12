"""
Pytest configuration and common fixtures for sarvam-conv-ai-sdk tests.
"""

from typing import Any, Dict

import pytest

from sarvam_conv_ai_sdk.tool import (
    SarvamInteractionTranscript,
    SarvamInteractionTurn,
    SarvamInteractionTurnRole,
    SarvamOnEndToolContext,
    SarvamOnStartToolContext,
    SarvamToolContext,
    SarvamToolLanguageName,
)


@pytest.fixture
def sample_agent_variables() -> Dict[str, Any]:
    """Sample agent variables for testing."""
    return {
        "user_id": "test_user_123",
        "session_id": "session_abc",
        "user_name": "Test User",
        "location": "Mumbai",
        "preferences": {"language": "English", "theme": "dark"},
    }


@pytest.fixture
def sample_tool_context(sample_agent_variables) -> SarvamToolContext:
    """Sample tool context for testing."""
    return SarvamToolContext(
        language=SarvamToolLanguageName.ENGLISH, agent_variables=sample_agent_variables
    )


@pytest.fixture
def sample_on_start_context() -> SarvamOnStartToolContext:
    """Sample on-start tool context for testing."""
    return SarvamOnStartToolContext(
        user_identifier="test_user_456",
        initial_state_name="welcome",
        initial_language_name=SarvamToolLanguageName.HINDI,
    )


@pytest.fixture
def sample_on_end_context() -> SarvamOnEndToolContext:
    """Sample on-end tool context for testing."""
    return SarvamOnEndToolContext(user_identifier="test_user_789")


@pytest.fixture
def sample_interaction_transcript() -> SarvamInteractionTranscript:
    """Sample interaction transcript for testing."""
    return SarvamInteractionTranscript(
        app_id="test_app",
        app_version=1,
        interaction_transcript=[
            SarvamInteractionTurn(
                role=SarvamInteractionTurnRole.USER, en_text="Hello, how are you?"
            ),
            SarvamInteractionTurn(
                role=SarvamInteractionTurnRole.AGENT,
                en_text="I'm doing well, thank you! How can I help you today?",
            ),
            SarvamInteractionTurn(
                role=SarvamInteractionTurnRole.USER, en_text="What's the weather like?"
            ),
            SarvamInteractionTurn(
                role=SarvamInteractionTurnRole.AGENT,
                en_text="The weather is sunny with a temperature of 25°C.",
            ),
        ],
    )


@pytest.fixture
def sample_on_end_context_with_transcript(
    sample_interaction_transcript,
) -> SarvamOnEndToolContext:
    """Sample on-end tool context with transcript for testing."""
    return SarvamOnEndToolContext(
        user_identifier="test_user_789",
        interaction_transcript=sample_interaction_transcript,
    )


@pytest.fixture
def all_languages():
    """All available languages for testing."""
    return [
        SarvamToolLanguageName.BENGALI,
        SarvamToolLanguageName.GUJARATI,
        SarvamToolLanguageName.KANNADA,
        SarvamToolLanguageName.MALAYALAM,
        SarvamToolLanguageName.TAMIL,
        SarvamToolLanguageName.TELUGU,
        SarvamToolLanguageName.PUNJABI,
        SarvamToolLanguageName.ODIA,
        SarvamToolLanguageName.MARATHI,
        SarvamToolLanguageName.HINDI,
        SarvamToolLanguageName.ENGLISH,
    ]


@pytest.fixture
def sample_greetings():
    """Sample greetings in different languages for testing."""
    return {
        SarvamToolLanguageName.ENGLISH: "Hello",
        SarvamToolLanguageName.HINDI: "नमस्ते",
        SarvamToolLanguageName.MARATHI: "नमस्कार",
        SarvamToolLanguageName.BENGALI: "নমস্কার",
        SarvamToolLanguageName.GUJARATI: "નમસ્તે",
        SarvamToolLanguageName.KANNADA: "ನಮಸ್ಕಾರ",
        SarvamToolLanguageName.MALAYALAM: "നമസ്കാരം",
        SarvamToolLanguageName.TAMIL: "வணக்கம்",
        SarvamToolLanguageName.TELUGU: "నమస్కారం",
        SarvamToolLanguageName.PUNJABI: "ਸਤ ਸ੍ਰੀ ਅਕਾਲ",
        SarvamToolLanguageName.ODIA: "ନମସ୍କାର",
    }


@pytest.fixture
def sample_farewells():
    """Sample farewell messages in different languages for testing."""
    return {
        SarvamToolLanguageName.ENGLISH: "Goodbye!",
        SarvamToolLanguageName.HINDI: "अलविदा!",
        SarvamToolLanguageName.MARATHI: "पुन्हा भेटू!",
        SarvamToolLanguageName.BENGALI: "বিদায়!",
        SarvamToolLanguageName.GUJARATI: "આવજો!",
        SarvamToolLanguageName.KANNADA: "ಬೀಗಿ ಬನ್ನಿ!",
        SarvamToolLanguageName.MALAYALAM: "വിട!",
        SarvamToolLanguageName.TAMIL: "பிரியாவிடை!",
        SarvamToolLanguageName.TELUGU: "వీడ్కోలు!",
        SarvamToolLanguageName.PUNJABI: "ਫਿਰ ਮਿਲਾਂਗੇ!",
        SarvamToolLanguageName.ODIA: "ବିଦାୟ!",
    }
