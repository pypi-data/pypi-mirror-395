"""Example of using the async client with automatic audio handling.

This example demonstrates:
1. Using AsyncSamvaadAgent with AsyncDefaultAudioInterface
2. Automatic audio input/output management at 16000 Hz
3. Handling callbacks in async context
4. Clean, simple API design

Requirements:
    pip install "sarvam-conv-ai-sdk[audio]"

Usage:
    python async_audio_example.py
"""

import asyncio
import logging
import os
import sys

from pydantic import SecretStr

from sarvam_conv_ai_sdk import (
    AsyncDefaultAudioInterface,
    AsyncSamvaadAgent,
    InteractionConfig,
    InteractionType,
)
from sarvam_conv_ai_sdk.messages.types import UserIdentifierType
from sarvam_conv_ai_sdk.tool import SarvamToolLanguageName

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # noqa
)
logger = logging.getLogger(__name__)


async def main(api_key: SecretStr):
    """Main async function demonstrating voice conversation."""

    logger.info("=" * 60)
    logger.info("Async Audio Example - Voice Conversation")
    logger.info("=" * 60)

    # Configure the conversation
    config = InteractionConfig(
        user_identifier="demo_user_async",
        user_identifier_type=UserIdentifierType.CUSTOM,
        app_id="app_id",
        org_id="org_id",
        workspace_id="workspace_id",
        interaction_type=InteractionType.CALL,
        agent_variables={
            "agent_variable1": "value",
            "agent_variable2": "value",
        },
        initial_language_name=SarvamToolLanguageName.HINDI,
        initial_state_name="initial_state_name",
        sample_rate=16000,
        version=1,
    )

    # Create async agent with automatic audio handling
    logger.info("Creating agent...")
    agent = AsyncSamvaadAgent(
        api_key=api_key,
        config=config,
        audio_interface=AsyncDefaultAudioInterface(input_sample_rate=16000),
    )

    try:
        # Start agent (connection happens asynchronously in background)
        logger.info("Starting agent...")
        await agent.start()
        logger.info("✅ Agent started! Connection establishing in background...")  # noqa

        # Wait for connection to be established
        logger.info("Waiting for WebSocket connection...")
        await agent.wait_for_connect(timeout=5.0)
        logger.info(f"✅ Connected! Interaction ID: {agent.get_interaction_id()}")  # noqa
        print_text = "\n" + "=" * 60 + "\n"
        print_text += "🎉 Voice conversation active!\n"
        print_text += "   Speak into your microphone to interact with the agent.\n"  # noqa
        print_text += "   Press Ctrl+C to stop.\n"
        print_text += "=" * 60 + "\n"
        logger.info(print_text)

        # Block until disconnected or interrupted
        await agent.wait_for_disconnect()
        logger.warning("Connection closed!")

    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received. Stopping conversation...")

    except Exception as e:
        logger.error(f"❌ Error: {e}", exc_info=True)

    finally:
        # Cleanup
        logger.info("Stopping agent...")
        await agent.stop()
        logger.info("✅ Cleaned up successfully!")


if __name__ == "__main__":
    API_KEY_STR = os.getenv("SARVAM_API_KEY")
    if not API_KEY_STR:
        logger.error("API key not set. Set SARVAM_API_KEY in the environment.")
        sys.exit(1)

    asyncio.run(main(SecretStr(API_KEY_STR)))
