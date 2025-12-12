# Sarvam Conv AI SDK

The **Sarvam Conversational AI SDK** is a Python package that helps developers build and extend conversational agents. It provides core components to manage conversation flow, language preferences, and messaging, making it easier to develop interactive and context-aware AI experiences.

---

## Overview

The Sarvam Conv AI SDK enables developers to create tools that can:

* Facilitate agentic capabilities like API calling in the middle of a conversation
* Build real-time voice and text-based conversational experiences
* Send voice notes with automatic transcription in text conversations
* Manage agent-specific variables
* Control and modify the language used during conversations
* Send dynamic messages to both the user and the underlying language model (LLM)

---

## Installation

### Basic Installation

Install the SDK via pip:

```bash
pip install sarvam-conv-ai-sdk
```

### Audio Support (Optional)

If you want to use audio streaming features (microphone input and speaker output), you need to install PyAudio. This requires system-level dependencies:

#### Option 1: Install with audio support

```bash
pip install sarvam-conv-ai-sdk[all]
```

**Note:** You'll need to install PortAudio first:

- **macOS**: `brew install portaudio`
- **Ubuntu/Debian**: `sudo apt-get install portaudio19-dev`
- **Windows**: Download from [http://www.portaudio.com/download.html](http://www.portaudio.com/download.html)

#### Option 2: Use without PyAudio

The SDK works without PyAudio for non-playback environments; audio capture/playback features will not be available. You can still:
- Use the WebSocket client for real-time voice conversations (provide your own audio I/O)
- Build backend proxies for frontend applications

---

## AsyncSamvaadAgent

Build real-time voice and text conversations with a small set of inputs.

- You provide InteractionConfig: who the user is, which app to talk to, interaction type (voice or text), and audio sample rate; optionally include overrides like agent_variables and initial language/state.
- You create AsyncSamvaadAgent with your API key, config, and optional audio interface plus callbacks for text/audio/events.
- Start the agent: it fetches a signed WebSocket URL, sends interaction_start, and streams audio/text both ways.

### Key features

* Real-time voice and text interaction — support both voice calls and text chat
* Automatic audio management — built-in microphone input and speaker output (for voice mode)
* Async/await support — non-blocking operations
* Callback handling — process text/audio/events asynchronously
* Connection management — robust WebSocket handling
* Flexible deployment — works with or without audio hardware

Minimal example:

```python
import asyncio
from pydantic import SecretStr
from sarvam_conv_ai_sdk import AsyncSamvaadAgent, AsyncDefaultAudioInterface, InteractionConfig, InteractionType, ServerTextChunkMsg, SarvamToolLanguageName
from sarvam_conv_ai_sdk.messages.types import UserIdentifierType

async def handle_text(msg: ServerTextChunkMsg):
    print("Agent:", msg.text)

async def main(app_id: str, api_key: str):
    config = InteractionConfig(
        user_identifier_type=UserIdentifierType.CUSTOM,
        user_identifier="demo_user",
        org_id="org_ai",
        workspace_id="workspace_id",
        app_id=app_id,
        interaction_type=InteractionType.CALL,
        agent_variables={"agent_variable_1": "value"},
        initial_language_name=SarvamToolLanguageName.HINDI,
        sample_rate=16000,
    )

    agent = AsyncSamvaadAgent(
        api_key=SecretStr(api_key),
        config=config,
        audio_interface=AsyncDefaultAudioInterface(input_sample_rate=16000),
        text_callback=handle_text,
    )

    await agent.start()
    try:
        # Wait until the WebSocket disconnects or the agent is stopped
        await agent.wait_for_disconnect()
    finally:
        await agent.stop()

if __name__ == "__main__":
    asyncio.run(main(app_id="your_app_id", api_key="your_api_key"))
```

### AsyncSamvaadAgent parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| api_key | SecretStr | Yes | API key used to fetch a signed WebSocket URL |
| config | InteractionConfig | Yes | Interaction start configuration (user id, app id, sample rate, overrides) |
| audio_interface | AsyncAudioInterface or None | No | Automatic mic capture and speaker playback. Omit for headless usage (use `send_audio`) |
| text_callback | Callable[[ServerTextChunkMsg], Awaitable[None]] or None | No | Receives streaming text chunks from the agent |
| audio_callback | Callable[[ServerAudioChunkMsg], Awaitable[None]] or None | No | Receives audio chunks if not using `audio_interface` for playback |
| event_callback | Callable[[ServerEventBase], Awaitable[None]] or None | No | Receives events like interaction_connected, user_interrupt, interaction_end |
| base_url | str | No | Override base URL. Default: `https://apps.sarvam.ai/api/app-runtime/` |

Methods:
- `await agent.start()` — start and connect
- `await agent.stop()` — stop and cleanup
- `await agent.wait_for_connect(timeout: float | None = 5.0)` — wait until connected
- `await agent.wait_for_disconnect()` — wait until disconnected or stopped
- `agent.is_connected()` — connection status
- `await agent.send_audio(audio_bytes: bytes)` — send raw 16‑bit PCM audio (for audio mode)
- `await agent.send_text(text: str)` — send text message (for text mode)
- `agent.get_interaction_id()` — current interaction id or `None`

Audio interface (optional): `AsyncDefaultAudioInterface(input_sample_rate: int = 16000)`
- Methods: `start(input_callback)`, `output(audio: bytes, sample_rate?: int)`, `interrupt()`, `stop()`
- Audio: LINEAR16 (16‑bit PCM mono). Supported sample rates: 8000, 16000

### What you must provide: InteractionConfig

Required fields:

- user_identifier_type: One of CUSTOM, EMAIL, PHONE_NUMBER, UNKNOWN
- user_identifier: The identifier value (string; phone/email/custom id) # This id can be used to see logs in the log analyser
- org_id: Your organization, e.g., "sarvamai"
- workspace_id: Your workspace, e.g., "default"
- app_id: The target application id
- interaction_type: InteractionType.CALL (voice) or InteractionType.CHAT (chat)
- sample_rate: 8000 or 16000 (16-bit PCM mono, required for both voice and text)
- version: int (Optional)

> **Important**  
> If `version` is not provided, the SDK uses the latest committed version of the app.  
> The connection will fail if the provided `app_id` has no committed version.

Optional overrides (applied server-side at start):

- agent_variables: dict of key/value to seed the agent context
- initial_language_name: e.g., "English", "Hindi" (must be allowed by app)
- initial_state_name: starting state name, if your app uses states
- initial_bot_message: first message from the agent

Example config:

```python
from sarvam_conv_ai_sdk import InteractionConfig, InteractionType, SarvamToolLanguageName
from sarvam_conv_ai_sdk.messages.types import UserIdentifierType

config = InteractionConfig(
    user_identifier_type=UserIdentifierType.CUSTOM,
    user_identifier="demo_user_async",
    org_id="sarvamai",
    workspace_id="default",
    app_id="your_app_id",
    interaction_type=InteractionType.CALL,
    agent_variables={"user_language": "Hindi"},
    initial_language_name=SarvamToolLanguageName.HINDI,
    initial_state_name="greeting",
    sample_rate=16000,
)
```

### Quick start: local voice test

1) Install dependencies

```bash
brew install portaudio               # macOS
pip install "sarvam-conv-ai-sdk[all]"
```

2) Set credentials (or pass directly in code)

```bash
export SARVAM_APP_ID="your_app_id"
export SARVAM_API_KEY="your_api_key"
```

3) Run the example

```bash
python -m sarvam_conv_ai_sdk.examples.async_audio_example
```

The example uses AsyncDefaultAudioInterface to capture mic at 16kHz and play responses. You can override base_url in AsyncSamvaadAgent if you use a different environment.

### Headless mode (no PyAudio)

Use your own audio I/O. Create the agent without audio_interface and push raw 16‑bit PCM mono chunks that match config.sample_rate.

```python
agent = AsyncSamvaadAgent(api_key=SecretStr("your_api_key"), config=config, text_callback=handle_text)
await agent.start()

# Send raw audio bytes
await agent.send_audio(raw_pcm_bytes)  # LINEAR16 mono at 16kHz or 8kHz

await agent.stop()
```

### Connect your frontend (backend proxy pattern)

See the section above for AsyncSamvaadAgent usage. For a full backend bridge, follow the same pattern in your server. Message shapes:

- Frontend → backend (init):

```json
{
  "type": "init",
  "app_id": "your_app_id",
  "context": {"language": "English", "user_name": "Priya"}
}
```

- Frontend → backend (text):

```json
{ "type": "text", "data": { "text": "Hello" } }
```

- Frontend → backend (audio):

```json
{ "type": "audio", "data": "<base64-raw-pcm>" }
```

Bridge essentials on the backend:

- Build InteractionConfig from init context; create AsyncSamvaadAgent with callbacks.
- Decode base64 and forward audio via await agent.send_audio(audio_bytes).
- In text/audio/event callbacks, websocket.send_json back to the frontend.

Minimal sketch:

```python
session.agent = AsyncSamvaadAgent(
    api_key=SecretStr(api_key),
    config=config,
    text_callback=session._handle_text,
    audio_callback=session._handle_audio,
    event_callback=session._handle_event,
)
await session.agent.start()
```

### Requirements for Async Audio

1. PyAudio installation:
   ```bash
   pip install sarvam-conv-ai-sdk[all]
   ```

2. System dependencies:
   - macOS: `brew install portaudio`
   - Ubuntu/Debian: `sudo apt-get install portaudio19-dev`
   - Windows: download from `http://www.portaudio.com/download.html`

3. Environment variables (optional convenience):
   ```bash
   export SARVAM_APP_ID="your_app_id"
   export SARVAM_API_KEY="your_api_key"
   ```

### Complete Example

See `sarvam_conv_ai_sdk/examples/async_audio_example.py` for a full, runnable script with mic capture, callbacks, and clean shutdown.

---

## Text-Based Conversations

In addition to voice interactions, the SDK supports text-based conversations for chat applications, messaging platforms, and other text-only use cases.

### Key Features

* Real-time text conversation — send and receive text messages asynchronously
* Voice note support — send audio recordings with automatic transcription
* Same callback pattern — consistent API with audio mode
* Event handling — track conversation state and transitions
* Async/await support — non-blocking text I/O

### Basic Text Example

```python
import asyncio
from pydantic import SecretStr
from sarvam_conv_ai_sdk import AsyncSamvaadAgent, InteractionConfig, InteractionType, ServerTextMsgType, SarvamToolLanguageName
from sarvam_conv_ai_sdk.messages.types import UserIdentifierType

async def handle_text(msg: ServerTextMsgType):
    print(f"Agent: {msg.text}")

async def main(app_id: str, api_key: str):
    config = InteractionConfig(
        user_identifier_type=UserIdentifierType.CUSTOM,
        user_identifier="text_user_123",
        org_id="org_ai",
        workspace_id="workspace_id",
        app_id=app_id,
        interaction_type=InteractionType.CHAT,  # CHAT mode for chat
        agent_variables={"user_name": "Alice"},
        initial_language_name=SarvamToolLanguageName.ENGLISH,
        sample_rate=16000,  # Still required in config
    )

    agent = AsyncSamvaadAgent(
        api_key=SecretStr(api_key),
        config=config,
        # No audio_interface needed for text mode
        text_callback=handle_text,
    )

    await agent.start()
    await agent.wait_for_connect(timeout=5.0)
    
    # Send text messages
    await agent.send_text("Hello! I need help with my booking.")
    await asyncio.sleep(2)  # Wait for response
    
    await agent.send_text("Can you check my reservation?")
    await asyncio.sleep(2)
    
    await agent.stop()

if __name__ == "__main__":
    asyncio.run(main(app_id="your_app_id", api_key="your_api_key"))
```

### Text vs Audio Configuration

The main differences between text and audio modes:

| Aspect | Audio Mode | Text Mode |
| --- | --- | --- |
| interaction_type | `InteractionType.CALL` | `InteractionType.CHAT` |
| audio_interface | Required for mic/speaker | Not needed (omit) |
| Input method | `send_audio(bytes)` | `send_text(str)` or `send_voice_note(bytes, transcribe=bool)` |
| Output | Audio chunks via audio_callback | Text via text_callback |
| Dependencies | PyAudio + PortAudio | None (base SDK only, PyAudio optional for voice notes) |

### Text-Specific Methods

* `await agent.send_text(text: str)` — Send a text message to the agent
  - Accepts plain string messages
  - Non-blocking, returns immediately
  - Messages are queued and sent over WebSocket

* `await agent.send_voice_note(audio_data: bytes, transcribe: bool = False)` — Send a voice note in text conversations
  - Accepts raw PCM audio bytes (16-bit PCM mono at the sample_rate of 48000)
  - When `transcribe=True`, the server transcribes the audio to text before processing
  - The transcribed text is returned via the `text_callback`
  - Non-blocking, returns immediately
  - The default sample rate for text interaction type is 48000
  - Useful for adding voice input to text-based conversations

### Interactive Text Loop

For continuous chat experiences, use an input loop:

```python
async def chat_loop(agent: AsyncSamvaadAgent):
    """Interactive text conversation loop."""
    loop = asyncio.get_event_loop()
    
    while agent.is_connected():
        try:
            # Get user input asynchronously
            user_input = await loop.run_in_executor(None, input, "You: ")
            
            if user_input.lower() in ["quit", "exit", "bye"]:
                print("Ending conversation...")
                break
            
            if user_input.strip():
                await agent.send_text(user_input)
                await asyncio.sleep(0.5)  # Brief pause for agent response
                
        except (EOFError, KeyboardInterrupt):
            break
```

### Voice Notes in Text Conversations

Text mode now supports **voice notes** — users can send audio recordings that are transcribed and processed by the agent.

#### Key Features

* **Audio recording** — Capture voice input using a microphone
* **Automatic transcription** — Server-side speech-to-text conversion
* **Seamless integration** — Voice notes work alongside regular text messages
* **Same conversation flow** — Transcribed text is processed just like typed text

#### Voice Note Flow

When a voice note is sent with `transcribe=True`:

1. User records audio
2. Audio is sent to the server via `send_voice_note()`
3. Server transcribes the audio to text
4. Transcribed text is returned via the `text_callback`
5. Server processes the transcription and generates agent response
6. Agent response is delivered via `text_callback`

#### Example: Voice Note in Text Conversation

```python
import asyncio
from pydantic import SecretStr
from sarvam_conv_ai_sdk import AsyncSamvaadAgent, InteractionConfig, InteractionType

async def handle_text(msg):
    """Handle both transcriptions and agent responses."""
    print(f"Agent: {msg.text}")

async def main():
    config = InteractionConfig(
        user_identifier_type=UserIdentifierType.CUSTOM,
        user_identifier="user_123",
        org_id="org_ai",
        workspace_id="workspace_id",
        app_id="your_app_id",
        interaction_type=InteractionType.CHAT,  # CHAT mode supports voice notes
        sample_rate=16000,
    )
    
    agent = AsyncSamvaadAgent(
        api_key=SecretStr("your_api_key"),
        config=config,
        text_callback=handle_text,
    )
    
    await agent.start()
    await agent.wait_for_connect()
    
    # Send a voice note with transcription
    audio_data = record_audio_from_mic()  # Your recording logic
    await agent.send_voice_note(audio_data, transcribe=True)
    
    # Wait for transcription and agent response
    await asyncio.sleep(2.0)
    
    await agent.stop()

asyncio.run(main())
```

#### Recording Audio for Voice Notes

To capture audio from the microphone, you can use PyAudio:

```python
import pyaudio
import threading

def record_audio_until_keypress(sample_rate: int = 48000) -> bytes:
    """Record audio until user presses Enter."""
    print("Recording... Press ENTER to stop.")
    
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=pyaudio.paInt16,  # 16-bit PCM
        channels=1,               # Mono
        rate=sample_rate,         # 48kHz
        input=True,
        frames_per_buffer=1024,
    )
    
    frames = []
    stop_recording = threading.Event()
    
    def wait_for_keypress():
        input()
        stop_recording.set()
    
    threading.Thread(target=wait_for_keypress, daemon=True).start()
    
    while not stop_recording.is_set():
        data = stream.read(1024, exception_on_overflow=False)
        frames.append(data)
    
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    return b"".join(frames)

# Use in async context
async def record_audio_async(sample_rate: int = 16000) -> bytes:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, record_audio_until_keypress, sample_rate)
```

#### Audio Format Requirements

* **Format**: LINEAR16 (16-bit PCM mono)
* **Sample Rate**: 48000Hz (must match `config.sample_rate`)
* **Channels**: Mono (single channel)
* **Encoding**: Raw PCM bytes (no headers)

#### Interactive Voice Note Example

Combine text and voice input in an interactive loop:

```python
async def interactive_conversation(agent: AsyncSamvaadAgent):
    """Support both text and voice notes."""
    loop = asyncio.get_event_loop()
    
    print("Commands: type text, '/voice' for voice note, 'quit' to exit")
    
    while agent.is_connected():
        user_input = await loop.run_in_executor(None, input, "You: ")
        
        if user_input.lower() in ["quit", "exit"]:
            break
        
        if user_input.strip().lower() == "/voice":
            # Record and send voice note
            audio_data = await record_audio_async(sample_rate=16000)
            await agent.send_voice_note(audio_data, transcribe=True)
            await asyncio.sleep(2.0)  # Wait for transcription + response
        
        elif user_input.strip():
            # Send regular text message
            await agent.send_text(user_input)
            await asyncio.sleep(0.5)
```

#### Voice Note Dependencies

Voice note recording requires PyAudio:

```bash
# Install with audio support
pip install sarvam-conv-ai-sdk[all]

# Or install PyAudio separately
pip install pyaudio
```

**System dependencies:**
- **macOS**: `brew install portaudio`
- **Ubuntu/Debian**: `sudo apt-get install portaudio19-dev`
- **Windows**: Download from [http://www.portaudio.com/download.html](http://www.portaudio.com/download.html)

**Note:** PyAudio is only needed for recording audio. If you have audio from another source (e.g., web upload, mobile app), you can send it directly via `send_voice_note()` without PyAudio.

### Text Message Types

The `text_callback` receives `ServerTextMsgType` which can be:

* `ServerTextChunkMsg` — Streaming text chunks (status: pending/completed/failed)
* `ServerTextMsg` — Complete text messages

Both contain:
* `text: str` — The text content
* `type: ServerMsgType` — Message type identifier

### Quick Start: Text Chat Test

1) Install SDK

For text-only (no voice notes):
```bash
pip install sarvam-conv-ai-sdk
```

For text + voice notes:
```bash
pip install sarvam-conv-ai-sdk[all]
# Also install system dependencies (see Voice Note Dependencies section)
```

2) Set credentials

```bash
export SARVAM_APP_ID="your_app_id"
export SARVAM_API_KEY="your_api_key"
```

3) Run the text example

```bash
python -m sarvam_conv_ai_sdk.examples.async_text_example
```

### Complete Text Example

See `sarvam_conv_ai_sdk/examples/async_text_example.py` for a full, runnable script demonstrating:
* Interactive text chat with user input loop
* Voice note recording and transcription
* Conversation tracking and message history
* Event handling and clean shutdown

### Use Cases for Text Mode

* **Chat applications** — Web chat widgets, mobile messaging
* **Messaging platforms** — WhatsApp, Telegram, Slack bots
* **Backend proxies** — Bridge between your frontend and Sarvam AI
* **Headless environments** — Servers without audio hardware
* **Testing & development** — Faster iteration without audio setup
* **Multi-modal apps** — Support both voice and text channels
* **Voice messaging** — Text conversations with voice note transcription
* **Accessibility** — Enable users to choose between typing and speaking

---

# Custom Tools
## Example Usage

```python
import httpx
from pydantic import Field

from sarvam_conv_ai_sdk import (
    SarvamInteractionTurnRole,
    SarvamOnEndTool,
    SarvamOnEndToolContext,
    SarvamOnStartTool,
    SarvamOnStartToolContext,
    SarvamTool,
    SarvamToolContext,
    SarvamToolLanguageName,
    SarvamToolOutput,
)

class OnStart(SarvamOnStartTool): #Name of the class has to be OnStart
    async def run(self, context: SarvamOnStartToolContext):
        user_id = context.get_user_identifier()
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://sarvam-flights.com/users/{user_id}")
            response.raise_for_status()
            user_data = response.json()

        source_destination = user_data.get("home_city")
        context.set_agent_variable("source_destination", source_destination)
        context.set_agent_variable("passenger_name", user_data.get("name"))
        
        # Store telephony call SID if available (for telephony channels)
        if context.provider_ref_id:
            context.set_agent_variable("call_sid", context.provider_ref_id)
        
        context.set_initial_language_name(SarvamToolLanguageName.ENGLISH)
        context.set_initial_bot_message(
            f"Hello! Would you like to book a flight from {source_destination}? Where would you like to go?",
        )
        return context


class BookFlight(SarvamTool):
    """Book a flight based on the user's travel preferences."""
    pre_run_message: str = Field(
        default="Processing your flight booking, please wait...",
        description="Message shown to user before tool execution"
    )
    destination: str = Field(description="City of destination")
    travel_date: str = Field(description="Date of travel (YYYY-MM-DD)")

    async def run(self, context: SarvamToolContext) -> SarvamToolOutput:
        source_destination = context.get_agent_variable("source_destination")
        booking_data = {
            "source": source_destination,
            "destination": self.destination,
            "travel_date": self.travel_date,
            "passenger_name": context.get_agent_variable("passenger_name"),
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://sarvam-flights.com/book", json=booking_data
            )
            response.raise_for_status()
            booking_result = response.json()

        if booking_result.get("status") == "confirmed":
            context.set_agent_variable("booking_id", booking_result.get("booking_id"))
            context.set_end_conversation()
            return SarvamToolOutput(
                message_to_user=f"Flight booked successfully to {self.destination}!",
                context=context,
            )
        else:
            context.change_state("recommend_destinations")
            return SarvamToolOutput(
                message_to_llm="Booking failed. Please suggest similar destinations.",
                context=context,
            )


class OnEnd(SarvamOnEndTool):  #Name of the class has to be OnEnd
    async def run(self, context: SarvamOnEndToolContext):
        feedback = context.get_agent_variable("feedback")
        negative_words = ["bad", "poor", "disappointed", "unhappy", "problem"]
        interaction_transcript = context.get_interaction_transcript()
        if interaction_transcript.interaction_transcript:
            for turn in interaction_transcript.interaction_transcript:
                if turn.role == SarvamInteractionTurnRole.USER:
                    is_negative = any(word in feedback.lower() for word in negative_words)
            context.set_agent_variable("feedback_sentiment", is_negative)
        
        # Log call details if telephony SID is available
        if context.provider_ref_id:
            async with httpx.AsyncClient() as client:
                await client.post(
                    "https://sarvam-flights.com/analytics/call-logs",
                    json={
                        "call_sid": context.provider_ref_id,
                        "user_id": context.get_user_identifier(),
                        "sentiment": is_negative,
                        "duration": (
                            interaction_transcript.interaction_end_time 
                            - interaction_transcript.interaction_start_time
                        ).total_seconds()
                    }
                )

        return context

```

---

## Base Classes

The SDK exposes three base classes for tool development:

### 1. `SarvamTool`

Primary base class for all operational tools invoked during conversation flow.

**Features:**

* `pre_run_message: Optional[str]` - Optional message to the user before tool execution. This is useful for providing feedback to users while the tool is processing (e.g., "Processing your request, please wait..."). If not provided, defaults to `None`.

**Example:**

```python
class MyCustomTool(SarvamTool):
    """Brief description of the tool's purpose."""

    pre_run_message: str = Field(
        default="Processing your request, please wait...",
        description="Message shown to user before tool execution"
    )
    tool_variable: type = Field(description="Description of this input parameter")

    async def run(self, context: SarvamToolContext) -> SarvamToolOutput:
        # Custom tool logic
        return SarvamToolOutput(
            message_to_user="Response to user",
            message_to_llm="Context for LLM",
            context=context
        )
```

### 2. `SarvamOnStartTool`

Executed at the beginning of a conversation, typically for initialization. The class **must** be named `OnStart`.

### 3. `SarvamOnEndTool`

Executed at the end of a conversation, typically for cleanup or post-processing. The class **must** be named `OnEnd`.

---

## Context Classes and Methods

### `SarvamToolContext`

The context object passed to `SarvamTool.run()` methods.

#### Variable Management

* `get_agent_variable(variable_name: str) -> Any`
  Retrieve the value of a variable.

* `set_agent_variable(variable_name: str, value: Any) -> None`
  Update a variable's value.

#### Language Control

* `get_current_language() -> SarvamToolLanguageName`
  Returns the current language of the agent.

* `change_language(language: SarvamToolLanguageName) -> None`
  Update the language preference.

#### Conversation Flow

* `set_end_conversation() -> None`
  Explicitly end the conversation.

#### State Management

* `get_current_state() -> str`
  Returns the current state of the conversation.

* `change_state(state: str) -> None`
  Transition to a new state. **Note:** The new state must be one of the next valid states defined in the agent configuration.

#### Engagement Metadata

* `get_engagement_metadata() -> EngagementMetadata`
  Retrieve the engagement metadata containing information about the current interaction. 

---

### `SarvamOnStartToolContext`

The context object passed to `SarvamOnStartTool.run()` methods.

#### Variable Management

* `get_agent_variable(variable_name: str) -> Any`
  Retrieve the value of a variable.

* `set_agent_variable(variable_name: str, value: Any) -> None`
  Update a variable's value.

#### User Information

* `get_user_identifier() -> str`
  Get the user identifier.

#### Telephony Information

* `provider_ref_id: Optional[str]`
  The reference ID from the channel provider. For telephony providers, this would contain the Call SID (Session ID) which uniquely identifies a specific phone call. For other channel providers, this would contain their respective reference IDs. Defaults to `None` for channels that don't provide reference IDs.

#### Initialization Methods

* `set_initial_bot_message(message: str) -> None`
  Set the first message sent by the agent when the conversation starts.

* `set_initial_state_name(state_name: str) -> None`
  Set the initial state from which the agent should start.

* `set_initial_language_name(language: SarvamToolLanguageName) -> None`
  Define the initial language preference for the user.

#### Engagement Metadata

* `get_engagement_metadata() -> EngagementMetadata`
  Retrieve the engagement metadata containing information about the current interaction.

---

### `SarvamOnEndToolContext`

The context object passed to `SarvamOnEndTool.run()` methods.

#### Variable Management

* `get_agent_variable(variable_name: str) -> Any`
  Retrieve the value of a variable.

* `set_agent_variable(variable_name: str, value: Any) -> None`
  Update a variable's value.

#### User Information

* `get_user_identifier() -> str`
  Get the user identifier.

#### Telephony Information

* `provider_ref_id: Optional[str]`
  The reference ID from the channel provider. For telephony providers, this would contain the Call SID (Session ID) which uniquely identifies a specific phone call. For other channel providers, this would contain their respective reference IDs. Defaults to `None` for channels that don't provide reference IDs.

#### Engagement Metadata

* `get_engagement_metadata() -> EngagementMetadata`
  Retrieve the engagement metadata containing information about the current interaction.


### Interaction Reattempt
* `set_retry_interaction`
  The user will be reattempted with the same agent. Useful when any business goal has not been met. 

#### Interaction Transcript

* `get_interaction_transcript() -> SarvamInteractionTranscript`
  Retrieve the conversation history containing user and agent messages in English and
 the timestamp when the conversation began and ended. Format: `yyyy-mm-dd hh:mm:ss`

**Example transcript:**
```python
[
    SarvamInteractionTurn(role=<SarvamInteractionTurnRole.AGENT: 'agent'>, en_text='Hello! How can I help you today?'),
    SarvamInteractionTurn(role=<SarvamInteractionTurnRole.USER: 'user'>, en_text='I need to book a flight'),
    SarvamInteractionTurn(role=<SarvamInteractionTurnRole.AGENT: 'agent'>, en_text='I can help you with that. Where would you like to go?'),
    SarvamInteractionTurn(role=<SarvamInteractionTurnRole.USER: 'user'>, en_text='I want to go to Mumbai'),
    SarvamInteractionTurn(role=<SarvamInteractionTurnRole.AGENT: 'agent'>, en_text='Great! When would you like to travel?')
]
```

---

## Return Types

### `SarvamToolOutput`

The return type for `SarvamTool.run()` methods. Contains:

* `message_to_user: Optional[str]` - Message that is sent directly to the user
* `message_to_llm: Optional[str]` - Message that is sent to the LLM, which then responds
* `context: SarvamToolContext` - The updated context object

**Note:** At least one of `message_to_llm` or `message_to_user` must be set.

**Important:** When both `message_to_user` and `message_to_llm` are set, only the `message_to_user` is actually sent to the user, but the `message_to_llm` overrides the `message_to_user` when adding to the chat thread for the LLM's context.

### `EngagementMetadata`

The engagement metadata object that can be retrieved from context objects using `get_engagement_metadata()`. Contains:

* `interaction_id: str` - Unique identifier for each conversation between user & agent.
* `attempt_id: Optional[str]` - Unique identifier for each attempt created on the platform
* `campaign_id: Optional[str]` - Campaign ID for the interaction
* `interaction_language: SarvamToolLanguageName` - The language used for the interaction (defaults to English)
* `app_id: str` - Application identifier of the agent for the interaction
* `app_version: int` - Version number of the agent
* `agent_phone_number: Optional[str]` - Phone number associated with the conversational agent application

---

## Supported Languages

The SDK supports multilingual conversations using the `SarvamToolLanguageName` enum. Available languages include:

* Bengali
* Gujarati
* Kannada
* Malayalam
* Tamil
* Telugu
* Punjabi
* Odia
* Marathi
* Hindi
* English

**Note:** The allowed languages are actually a subset that is preselected while defining the agent configurations.

---

## Best Practices

1. **Always implement `run()`**: The `run()` method is the entry point for tool execution logic.
2. **Use `Field()` for parameters**: Ensures type safety and adds descriptive metadata necessary for LLM to use in the prompt.
3. **Gracefully handle errors**: Avoid accessing unset variables or using invalid types.
4. **Return the appropriate type**: `SarvamTool.run()` must return `SarvamToolOutput`, while `SarvamOnStartTool.run()` and `SarvamOnEndTool.run()` return their respective context objects.
5. **Write meaningful docstrings**: Clearly describe what each tool is intended to do as this directly impacts the performance of tool calling capabilities of the agent.
6. **Use async operations for I/O**: For the best performance, use `async/await` for external API calls to avoid blocking.
7. **Use context methods**: Use the provided context methods for variable management, language control, and messaging instead of directly accessing context attributes.
8. **Debugging with print statements**: Any `print()` statements in your tool code will be captured and displayed in the debug chat in the [Sarvam Agents UI](https://agents.sarvam.ai/build/my-agents). This is useful for debugging tool execution, inspecting variable values, and tracking the flow of your tools during development and testing.


---

## Testing Your Tools

After creating a tool, you can test it locally to ensure it works as expected. Here's how to test your tools:

> **Note:** When testing tools in the Sarvam platform, any `print()` statements in your tool code will be visible in the debug chat in the [Sarvam Agents UI](https://agents.sarvam.ai/build/my-agents). Use print statements to debug tool execution, inspect variable values, and track the flow of your tools.

### Testing Steps

1. **Create the ToolContext**: Initialize the appropriate context object with test data
2. **Instantiate the tool class**: Use `tool.model_validate(tool_args)` to create a tool instance
3. **Run the tool**: Call the tool's `run()` method with the context
4. **Observe the returned object**: Check if the necessary changes have been made to the context

### Example Test: SarvamTool

```python
# Test the BookFlight tool
async def test_book_flight():
    # 1. Create the ToolContext
    context = SarvamToolContext(
        language=SarvamToolLanguageName.ENGLISH,
        allowed_languages=[SarvamToolLanguageName.ENGLISH],
        state="booking",
        next_valid_states=["recommend_destinations", "end"],
        agent_variables={
            "source_destination": "Mumbai",
            "passenger_name": "John Doe",
            "booking_id": "123"
        },
        engagement_metadata=EngagementMetadata(
            interaction_id="123",
            attempt_id="456",
            campaign_id="789",
            interaction_language=SarvamToolLanguageName.ENGLISH,
            app_id="101",
            app_version=1,
            agent_phone_number="+1234567890",
        ),
    )
    
    # 2. Instantiate the tool class
    tool_args = {
        "destination": "Delhi",
        "travel_date": "2024-03-15"
    }
    tool_instance = BookFlight.model_validate(tool_args)
    
    # 3. Run the tool
    result = await tool_instance.run(context)
    
    # 4. Observe the returned object
    print(f"Message to user: {result.message_to_user}")
    print(f"Message to LLM: {result.message_to_llm}")
    print(f"End conversation: {result.context.end_conversation}")
    print(f"Current state: {result.context.get_current_state()}")
    print(f"Agent variables: {result.context.agent_variables}")
    print(f"Current Language: {result.context.get_current_language()}")

# Run the test
asyncio.run(test_book_flight())
```

### Example Test: OnStart Tool

For `SarvamOnStartTool`, the testing approach is similar but it returns the context object directly:

```python
# Testing OnStart tool
async def test_on_start():
    context = SarvamOnStartToolContext(
        user_identifier="user123",
        agent_variables={"source_destination": "Mumbai", "passenger_name": "John Doe"},
        engagement_metadata=EngagementMetadata(
            interaction_id="123",
            attempt_id="456",
            campaign_id="789",
            interaction_language=SarvamToolLanguageName.ENGLISH,
            app_id="101",
            app_version=1,
            agent_phone_number="+1234567890",
        ),
        initial_bot_message=None,
        initial_state_name="start",
        initial_language_name=SarvamToolLanguageName.ENGLISH,
        provider_ref_id="CA1234567890abcdef1234567890abcdef",  # Optional: for telephony channels
    )
    
    tool_instance = OnStart()
    result = await tool_instance.run(context)
    
    print(f"Initial bot message: {result.initial_bot_message}")
    print(f"Initial state: {result.initial_state_name}")
    print(f"Initial Language Name: {result.initial_language_name}")
    print(f"Agent variables: {result.agent_variables}")
    print(f"Telephony Call SID: {result.provider_ref_id}")

# Run the test
asyncio.run(test_on_start())
```

### Example Test: OnEnd Tool

```python
# Testing OnEnd tool
async def test_on_end():
    context = SarvamOnEndToolContext(
        user_identifier="user123",
        agent_variables={"feedback": "I had a bad experience", "feedback_sentiment": False},
        engagement_metadata=EngagementMetadata(
            interaction_id="123",
            attempt_id="456",
            campaign_id="789",
            interaction_language=SarvamToolLanguageName.ENGLISH,
            app_id="101",
            app_version=1,
            agent_phone_number="+1234567890",
        ),
        interaction_transcript=SarvamInteractionTranscript(
            interaction_transcript=[
                SarvamInteractionTurn(role=SarvamInteractionTurnRole.AGENT, en_text='Hello! How can I help you today?'),
                SarvamInteractionTurn(role=SarvamInteractionTurnRole.USER, en_text='I need to book a flight'),
                SarvamInteractionTurn(role=SarvamInteractionTurnRole.AGENT, en_text='I can help you with that. Where would you like to go?'),
                SarvamInteractionTurn(role=SarvamInteractionTurnRole.USER, en_text='I want to go to Mumbai'),
                SarvamInteractionTurn(role=SarvamInteractionTurnRole.AGENT, en_text='Great! When would you like to travel?')
            ],
            interaction_start_time=datetime.now() - timedelta(minutes=2),
            interaction_end_time=datetime.now(),
        ),
        retry_interaction=False,
        provider_ref_id="CA1234567890abcdef1234567890abcdef",  # Optional: for telephony channels
    )
    
    tool_instance = OnEnd()
    result = await tool_instance.run(context)
    
    print(f"Agent variables: {result.agent_variables}")
    print(f"Interaction Retry: {result.retry_interaction}")
    print(f"Telephony Call SID: {result.provider_ref_id}")

# Run the test
asyncio.run(test_on_end())
```


## Requirements for Async Audio

1. **PyAudio Installation:**
   ```bash
   pip install sarvam-conv-ai-sdk[all]
   ```

2. **System Dependencies:**
   - **macOS**: `brew install portaudio`
   - **Ubuntu/Debian**: `sudo apt-get install portaudio19-dev`
   - **Windows**: Download from [http://www.portaudio.com/download.html](http://www.portaudio.com/download.html)

3. **Environment Variables:**
   ```bash
   export SARVAM_APP_ID="your_app_id"
   export SARVAM_API_KEY="your_api_key"
   ```

## Best Practices for Async Audio

1. Use proper event loop setup for PyAudio compatibility:
   ```python
   loop = asyncio.new_event_loop()
   asyncio.set_event_loop(loop)
   ```

2. Handle connection states gracefully:
   ```python
   while agent.is_connected():
       await asyncio.sleep(1)
   ```

3. Implement proper cleanup in finally blocks:
   ```python
   finally:
       await agent.stop()
   ```

4. Use appropriate sample rates (typically 16000 Hz for input)

5. Handle interruptions with KeyboardInterrupt:
   ```python
   except KeyboardInterrupt:
       print("Stopping conversation...")
   ```

## Complete Example

See `sarvam_conv_ai_sdk/examples/async_audio_example.py` for a complete working script.

---