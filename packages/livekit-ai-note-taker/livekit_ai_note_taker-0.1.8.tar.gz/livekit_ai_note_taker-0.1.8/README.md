# AI Note Taker for LiveKit

An installable Python package that runs a LiveKit agent which listens to room audio, transcribes with Deepgram and AWS transcribe, and publishes concise meeting notes/summaries using Groq, OpenRouter(ollama), or OpenAI-compatible models.

## Installation

```bash
pip install .
# or once published:
pip install livekit-ai-note-taker
```

## Configuration

Set the following environment variables (a `.env` file is supported via `python-dotenv`):

- `LIVEKIT_URL` – LiveKit WebSocket URL (e.g. `wss://example.livekit.cloud`)
- `LIVEKIT_API_KEY` / `LIVEKIT_API_SECRET` – LiveKit credentials
- `DEEPGRAM_API_KEY` – Deepgram STT key
- `PROVIDER` – `groq`, `openrouter`, or `openai`
- `GROQ_API_KEY` / `GROQ_MODEL_NAME` – when `PROVIDER=groq`
- `OPENROUTER_API_KEY` / `OPENROUTER_MODEL_NAME` / `OPENROUTER_BASE_URL` – when `PROVIDER=openrouter`
- `OPENAI_API_KEY` – when `PROVIDER=openai`
- `SUMMARY_INTERVAL` – seconds between rolling summaries (default `150`)
- `PROMPT_TYPE` – `small` or `big` prompt template (default `small`)
- `AGENT_NAME` – LiveKit agent registration name (default `meeting_summarizer`)
- `BACKEND_URL` – webhook endpoint that receives the final meeting summary (default `http://localhost:8000/meetings/meeting-note-webhook`)
- `LIVEKIT_SUMMARIZER_DISABLE_SSL_VERIFY` – set to `true` to ignore TLS verification for aiohttp (development only)

## Running the worker

```bash

livekit-ai-note-taker
```

The command validates configuration, connects to LiveKit, and starts publishing summaries to the room via `publish_data` on the local participant.

## Using as a library

```python
import asyncio
from livekit_ai_note_taker import run_worker

asyncio.run(run_worker())
```

You can also import `NoteTakerAgent` if you want to wire custom events or prompts in your own application. Logging is left to the host application; configure it as needed (e.g. `logging.basicConfig(level=logging.INFO)`).
