"""Example using async client with text I/O over text channel.

This example demonstrates:
1. Using AsyncSamvaadAgent with text_callback for receiving text
2. Sending text messages using send_text() (supports both str and JSON)
3. Sending voice notes using send_voice_note() for transcription
4. Working with the TEXT interaction type
5. Handling both text and events in async context
6. Properly handling transcribed text from voice notes

Requirements:
    pip install sarvam-conv-ai-sdk
    pip install pyaudio  # Optional, for voice note functionality

Usage:
    python async_text_example.py

Features:
    - Text messages: Type any message and press Enter
    - Voice notes: Type '/voice' to start recording, then press Enter to stop
    - Exit: Type 'quit' or 'exit' to end the conversation

Voice Note Flow:
    When a voice note is sent with transcribe=True:
    1. User records audio until pressing Enter
    2. Audio is sent to the server for transcription
    3. Server sends back the transcribed text
       (displayed as "📝 Transcribed: ...")
    4. Server processes the transcribed text and sends agent's response
    5. Agent response is displayed as "🤖 Agent: ..."
"""

import asyncio
import logging
import os
import sys
import threading

import pyaudio
from pydantic import SecretStr

from sarvam_conv_ai_sdk import (
    AsyncSamvaadAgent,
    InteractionConfig,
    InteractionType,
    ServerEventBase,
    ServerTextMsgType,
)
from sarvam_conv_ai_sdk.messages.types import UserIdentifierType
from sarvam_conv_ai_sdk.tool import SarvamToolLanguageName

# Configure logging
logging.basicConfig(
    level=logging.WARNING,  # Reduce noise
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # But keep INFO for our logger


def record_audio_until_keypress(sample_rate: int = 16000) -> bytes:
    """Record audio from microphone until user presses any key.

    Args:
        sample_rate: Sample rate for recording (default: 16000 Hz)

    Returns:
        Raw PCM audio bytes (PCM16 format)
    """
    print("🎤 Recording... Press ENTER to stop recording.")

    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=sample_rate,
        input=True,
        frames_per_buffer=1024,
    )

    frames = []
    stop_recording = threading.Event()

    def wait_for_keypress():
        """Wait for user to press Enter."""
        input()
        stop_recording.set()

    # Start thread to wait for keypress
    keypress_thread = threading.Thread(target=wait_for_keypress, daemon=True)
    keypress_thread.start()

    # Record until keypress
    try:
        while not stop_recording.is_set():
            data = stream.read(1024, exception_on_overflow=False)
            frames.append(data)
    except Exception as e:
        logger.error(f"Error during recording: {e}")

    logger.info("✅ Recording finished!")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    return b"".join(frames)


async def record_audio_async(sample_rate: int = 16000) -> bytes:
    """Async wrapper for audio recording until keypress.

    This wraps the synchronous pyaudio recording in an executor
    to avoid blocking the async event loop. Recording continues
    until the user presses Enter.

    Args:
        sample_rate: Sample rate for recording (default: 16000 Hz)

    Returns:
        Raw PCM audio bytes (PCM16 format)
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, record_audio_until_keypress, sample_rate)


async def main(api_key: SecretStr):
    """Main async function demonstrating text conversation with voice.

    This example shows:
    1. How to set up an AsyncSamvaadAgent with TEXT interaction type
    2. How to send text messages using send_text()
    3. How to send voice notes using send_voice_note() with
       transcription
    4. How to handle callbacks for text responses and events
    5. Interactive conversation loop with user input

    Args:
        api_key: Sarvam API key
    """

    logger.info("=" * 60)
    logger.info("Async Text Example - Text Conversation with Voice Notes")
    logger.info("=" * 60)

    # Configure the conversation
    # InteractionConfig defines how the agent will interact with the user
    config = InteractionConfig(
        # User identification
        user_identifier="demo_user_async",
        user_identifier_type=UserIdentifierType.CUSTOM,
        # Organization/workspace details
        app_id="app_id",
        org_id="org_id",
        workspace_id="workspace_id",
        # Interaction type: TEXT means text-based communication
        # (as opposed to AUDIO for voice-to-voice)
        interaction_type=InteractionType.CHAT,
        # Custom variables that can be used by the agent
        agent_variables={
            "agent_variable1": "value",
            "agent_variable2": "value",
        },
        # Initial conversation settings
        initial_language_name=SarvamToolLanguageName.HINDI,
        initial_state_name="initial_state_name",
        # Audio settings (required for voice notes)
        sample_rate=48000,  # 48kHz is standard for speech
    )

    # Track conversation state
    conversation_messages = []
    waiting_for_transcription = False

    # Define text callback to handle incoming text
    async def handle_text(text_msg: ServerTextMsgType):
        """Handle text messages from the agent.

        This callback is invoked for both:
        1. Transcribed text from voice notes (user's speech)
        2. Agent's text responses

        Args:
            text_msg: Server text message containing either transcription
                     or agent's response
        """
        nonlocal waiting_for_transcription

        # If we're waiting for transcription, this is the user's
        # transcribed text
        if waiting_for_transcription:
            print(f"\n📝 Transcribed: {text_msg.text}")
            conversation_messages.append({"role": "user", "content": text_msg.text})
            waiting_for_transcription = False
        else:
            # This is the agent's response
            print(f"\n🤖 Agent: {text_msg.text}")
            conversation_messages.append({"role": "agent", "content": text_msg.text})

    # Define event callback to handle events
    async def handle_event(event: ServerEventBase):
        """Handle events from the agent.

        This callback is invoked for various agent events like:
        - conversation_started
        - conversation_ended
        - tool_call_started
        - tool_call_completed

        Args:
            event: Server event containing event type and metadata
        """
        logger.info(f"📢 Event: {event.type}")

    # Create async agent with callbacks
    # The agent handles the WebSocket connection and message routing
    logger.info("Creating agent...")
    agent = AsyncSamvaadAgent(
        api_key=api_key,
        config=config,
        text_callback=handle_text,  # Called when agent sends text
        event_callback=handle_event,  # Called for agent events
        base_url="https://apps.sarvam.ai/api/app-runtime/",
    )

    try:
        # Start the agent
        # This initiates the WebSocket connection in the background
        logger.info("Starting agent...")
        await agent.start()
        logger.info("✅ Agent started! Connection establishing in background...")

        # Wait for WebSocket connection to be established
        # The timeout ensures we don't wait indefinitely
        logger.info("Waiting for WebSocket connection...")
        connected = await agent.wait_for_connect(timeout=5.0)
        if not connected:
            logger.error("Failed to connect within timeout")
            return

        # Connection successful - we can now send and receive messages
        interaction_id = agent.get_interaction_id()
        logger.info(f"✅ Connected! Interaction ID: {interaction_id}")
        print("🎉 TEXT CONVERSATION ACTIVE - Ready to interact!")
        print("\n📝 HOW TO USE:")
        print("   • Text Messages: Type any message and press Enter")
        print("   • Voice Notes:   Type '/voice', then press Enter to stop recording")
        print("   • Exit:          Type 'quit' or 'exit' to end conversation")
        print("\n💡 VOICE NOTE FLOW:")
        print("   1. Type '/voice' and start speaking")
        print("   2. Press Enter when done speaking")
        print("   3. Your transcribed text will be displayed")
        print("   4. Agent's response will follow")
        print("\n⚙️  TECHNICAL:")
        print("   • Sample rate: 48000 Hz")
        print("   • Press Enter to stop recording")

        # Interactive loop for continuous text conversation
        # This loop runs until the user types 'quit' or 'exit'
        loop = asyncio.get_event_loop()

        while True:
            try:
                # Get user input asynchronously to avoid blocking
                user_input = await loop.run_in_executor(None, input, "👤 You: ")

                # Check for exit commands
                if user_input.lower() in ["quit", "exit"]:
                    logger.info("Exiting conversation...")
                    break

                # Skip empty inputs
                if not user_input.strip():
                    continue

                # Handle voice note command
                if user_input.strip().lower() == "/voice":
                    try:
                        # Record audio from microphone until Enter is pressed
                        # This runs in a separate thread to avoid blocking
                        audio_data = await record_audio_async(
                            sample_rate=config.sample_rate
                        )

                        # Send voice note with transcribe=True
                        # The server will:
                        # 1. Transcribe the audio
                        # 2. Send back the transcribed text
                        #    (handled by text_callback)
                        # 3. Process it and send the agent's response
                        logger.info("📤 Sending voice note for transcription...")
                        waiting_for_transcription = True
                        await agent.send_voice_note(audio_data, transcribe=True)

                        # Wait longer for voice note processing
                        # (transcription + agent response)
                        await asyncio.sleep(2.0)

                    except Exception as e:
                        logger.error(f"❌ Error recording/sending audio: {e}")
                        waiting_for_transcription = False
                        continue

                else:
                    # Send as regular text message
                    # The agent will receive and process the text
                    conversation_messages.append(
                        {"role": "user", "content": user_input}
                    )
                    await agent.send_text(user_input)

                    # Brief pause to allow agent response to be received
                    # and displayed
                    await asyncio.sleep(1.0)

            except EOFError:
                logger.info("Input stream closed. Exiting...")
                break

        # Print conversation summary
        if conversation_messages:
            print("📊 CONVERSATION SUMMARY")
            print(f"Total messages: {len(conversation_messages)}")
            user_msgs = len([m for m in conversation_messages if m["role"] == "user"])
            agent_msgs = len([m for m in conversation_messages if m["role"] == "agent"])
            print(f"User messages: {user_msgs} | Agent messages: {agent_msgs}")
            for i, msg in enumerate(conversation_messages, 1):
                role = "🤖 Agent" if msg["role"] == "agent" else "👤 User"
                print(f"{i}. {role}: {msg['content']}")
            print("=" * 70)

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
