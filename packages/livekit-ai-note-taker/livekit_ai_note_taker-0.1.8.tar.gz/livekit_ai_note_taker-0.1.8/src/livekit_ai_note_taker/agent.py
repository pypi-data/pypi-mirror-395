from __future__ import annotations

import asyncio
import json
import logging
import os
import ssl
from datetime import datetime
from typing import Any, Dict, List

import aiohttp
from groq import AsyncGroq, Groq
from livekit import api, agents, rtc
from livekit.plugins import deepgram

from .config import config

logger = logging.getLogger(__name__)

_ssl_patch_applied = False
_original_tcp_connector_init = aiohttp.TCPConnector.__init__


def patch_aiohttp_ssl() -> None:
    """Disable SSL verification for aiohttp connectors (useful for dev)."""
    global _ssl_patch_applied
    if _ssl_patch_applied:
        return

    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    def patched_tcp_connector_init(self, *args, **kwargs):  # type: ignore[override]
        kwargs.setdefault("ssl", ssl_context)
        return _original_tcp_connector_init(self, *args, **kwargs)

    aiohttp.TCPConnector.__init__ = patched_tcp_connector_init  # type: ignore[assignment]
    _ssl_patch_applied = True
    logger.debug("aiohttp SSL verification disabled for connectors")


class NoteTakerAgent:
    def __init__(self, room: rtc.Room):
        if config.DISABLE_SSL_VERIFY:
            patch_aiohttp_ssl()

        self.room: rtc.Room = room
        self.transcript_buffer: List[str] = []
        self.total_transcripts: List[str] = []
        self.interval_summaries: List[str] = []
        self.last_summary: str = ""

        logger.info("Initializing Deepgram STT...")
        self.stt = deepgram.STT()
        logger.info("Initializing LLM client...")

        provider = config.PROVIDER.lower()
        if provider == "openai":
            from livekit.plugins import openai

            self.llm = openai.AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        elif provider == "groq":
            self.llm = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))
        elif provider == "openrouter":
            import httpx

            self.openrouter_client = httpx.AsyncClient(
                base_url=config.OPENROUTER_BASE_URL,
                headers={"Authorization": f"Bearer {config.OPENROUTER_API_KEY}"},
            )
        else:
            raise ValueError(f"Unsupported provider: {config.PROVIDER}")

    async def start(self) -> None:
        logger.info("NoteTakerAgent starting for room: %s", self.room.name)
        asyncio.create_task(self.periodic_summary())

        @self.room.on("track_subscribed")
        def on_track_subscribed(track, publication, participant):  # noqa: ANN001
            if track.kind == rtc.TrackKind.KIND_AUDIO:
                asyncio.create_task(self.handle_audio_stream(track, participant))

        @self.room.on("participant_connected")
        def on_participant_connected(participant):  # noqa: ANN001
            logger.info("Participant connected: %s %s", participant.identity, participant.name)

    async def handle_audio_stream(self, track, participant):  # noqa: ANN001
        logger.info("Starting audio stream handler for %s", participant.name)
        try:
            stream = self.stt.stream()

            async def push_frames():
                try:
                    async for event in rtc.AudioStream(track):
                        stream.push_frame(event.frame)
                except Exception as exc:  # pragma: no cover - defensive logging
                    logger.error("Error pushing frames for %s: %s", participant.identity, exc, exc_info=True)

            push_task = asyncio.create_task(push_frames())

            try:
                async for event in stream:
                    if event.type == agents.stt.SpeechEventType.FINAL_TRANSCRIPT and event.alternatives:
                        text = event.alternatives[0].text
                        entry = f"[{datetime.now().strftime('%H:%M')}] {participant.name}: {text}"
                        self.transcript_buffer.append(entry)
                        self.total_transcripts.append(entry)
            finally:
                push_task.cancel()
                try:
                    await push_task
                except asyncio.CancelledError:
                    pass
        except Exception as exc:  # pragma: no cover - defensive logging
            logger.error("Error in handle_audio_stream for %s: %s", participant.identity, exc, exc_info=True)

    async def periodic_summary(self) -> None:
        logger.info("Periodic summary loop started")
        while True:
            try:
                await asyncio.sleep(int(config.SUMMARY_INTERVAL))

                if not self.transcript_buffer:
                    continue

                conversation_text = "\n".join(self.transcript_buffer)
                self.transcript_buffer = []

                asyncio.create_task(self._generate_and_broadcast_summary(conversation_text))
            except asyncio.CancelledError:
                break
            except Exception as exc:  # pragma: no cover - defensive logging
                logger.error("Unexpected error in periodic_summary: %s", exc, exc_info=True)

    def get_prompt(self) -> str:
        if config.PROMPT_TYPE == "big":
            return self.get_big_prompt()
        if config.PROMPT_TYPE == "small":
            return self.get_small_prompt()
        return self.get_small_prompt()

    def get_big_prompt(self) -> str:
        return """You are the UrCalls Meeting Notes Assistant. Your job is to produce a continuously updated meeting summary that preserves the entire meeting context, even though transcript text arrives in incremental time windows (e.g., 5
minutes, 3 minutes, 10 minutes, or any interval).
You will always receive:
1. The latest transcript window (new segment of conversation), and
2. The prior summary (your previously generated output) Use BOTH to maintain a stable, accurate, and complete summary of the meeting.
Your writing style must be neutral, professional, and adaptive regardless of meeting type (work meeting, coaching call, interview, personal discussion, etc.).

OUTPUT STRUCTURE (MANDATORY)
MEETING OVERVIEW
● A concise description of the entire meeting so far, combining new and previous context.
KEY DECISIONS
● New decisions from the latest transcript
● Persisted decisions from previous summary (if still valid)
● If none: — No Update
ACTION ITEMS
● Task — Assignee — Deadline
● Include new items and continue previous ones unless completed, cancelled, or contradicted
● If none: — No Update
NEXT STEPS
● Planned follow-ups or future actions (new + still-relevant previous items)
● If none: — No Update
IMPORTANT NOTES
● Critical clarifications, essential context, risks, constraints, or mentions
● Include new + previously relevant notes
● If none: — No Update
PREVIOUS HIGHLIGHTS
● Earlier important items that are no longer part of the current discussion but still matter for full
context
● Do NOT duplicate content already visible in other sections
● If none: — No Update

REQUIRED RULES & BEHAVIOUR
1. Information Use
Use ONLY the transcript window provided and the prior summary.
No assumptions, no guessing, no invented details.
2. Dynamic Interval Awareness
Your behavior must NOT assume a fixed refresh window.

Treat each incoming transcript as:
“the newest segment of the conversation since the last summary”
regardless of duration.
3. Continuity Preservation
If an item existed before, you MUST:
- keep it if still relevant
- move it to “Previous Highlights” if no longer active
- remove or correct it only when the new transcript clearly contradicts it
4. Correction Protocol
If new transcript content updates or contradicts previous information:
- Correct the item
- Add a clarification in “Important Notes”
- Remove the outdated version
- Do NOT keep conflicting information
5. Demotion Logic (When to Move to “Previous Highlights”)
Move an item to “Previous Highlights” if BOTH apply:
- it is not referenced in the latest transcript window
- it has already appeared in at least one previous cycle
This keeps summaries clean without losing context.
6. Avoid Duplication
Each decision, action, note, or highlight must appear in only one section.
Never repeat or restate the same point.
7. Wording Stability
Do NOT rewrite or rephrase prior items unless:
- new details modify them
- clarifications appear
- corrections are required
This prevents summary drift.
8. Concise but Comprehensive
Summaries must remain clear, structured, and readable.
If any section grows too long, compress older or lower-priority items and relocate them to
“Previous Highlights.
”
INTELLIGENT DIARISATION RULES (IMPORTANT)
A. Never invent participant names.
If the transcript does not provide a name or role, use:
- “Speaker”,
- “Participant”, or
- “A participant”
    as neutral references.

B. If the transcript includes diarisation IDs (e.g., “Speaker 1”, “Speaker 2”), use them exactly as provided.
Do NOT rename, combine, or infer identities.

C. If the transcript explicitly gives a name (e.g., “Sarah”, “Ahmed”), use the name as given.
Use exactly what appears in the transcript.

D. If diarisation is inconsistent or unclear, default to neutral language.

Example: “A participant suggested…”
Avoid assuming relationships, roles, genders, or intentions.

E. No role invention
Do NOT assign roles (“manager”, “team lead”, “client”) unless the transcript explicitly says so.
TONE & ADAPTATION RULES
- Maintain a neutral, professional tone, suitable for both formal and informal meetings.
- Do NOT assume the meeting’s purpose (e.g., business, therapy, personal).
- Let the transcript drive context.
- Keep summaries respectful, precise, and unbiased.

Do NOT Include
- Meta commentary
- Explanations
- Disclaimers
- “As an AI…” statements
- Format instructions
- Speculation or invented content

Only return the structured summary.
"""

    def get_small_prompt(self) -> str:
        return """You are the UrCalls Meeting Notes Assistant.
Your job is to maintain a continuously updated meeting summary using:
1. The latest transcript segment, and
2. The prior summary

—regardless of how long the refresh interval is.

Write neutrally, professionally, and adaptively for any meeting type.

OUTPUT FORMAT (MANDATORY)

 MEETING OVERVIEW
- Concise description of the full meeting so far (new + previous context).

 KEY DECISIONS
- New decisions
- Persist valid previous decisions
- If none: — No Update

ACTION ITEMS
- Include new + ongoing items
- Include only explicit tasks clearly assigned in the transcript
 - A task must have BOTH:
 – A clearly expressed obligation (not intention) or instruction 
 – A clearly identified assignee (name or speaker label)
- If either is missing, place it in NEXT STEPS, not ACTION ITEMS
- If none: — No Update

 NEXT STEPS
- New + still-relevant planned actions
- If none: — No Update

 IMPORTANT NOTES
- Critical context, clarifications, risks (new + relevant previous)
- If none: — No Update

 PREVIOUS HIGHLIGHTS
- Older but important items no longer active in the current discussion
- No duplication
- If none: — No Update

CORE RULES

1. Use Only Given Information - Use only the transcript + prior summary. No assumptions or invented facts.
2. Dynamic Window - Treat each transcript as simply "the newest segment" — time interval irrelevant.
3. Continuity - Keep prior items unless contradicted. Move inactive items to Previous Highlights. Remove only when corrected by new transcript.
4. Corrections - If new information changes or contradicts something:
     - Update it
     - Add clarification in Important Notes
     - Remove outdated version

5. No Duplication - Every item appears once in one section.
6. Stability - Do not rewrite earlier items unless new information requires it.
7. Clarity & Compression - Summaries must stay clear and compact. Older context can be compressed and shifted to Previous Highlights.
8. Do NOT convert statements of intent into tasks - A participant expressing intent is NOT a task unless:
     - Another participant explicitly assigns it to them, OR
     - The speaker explicitly commits to carry out an action as an obligation or confirms responsibility when asked.
     - When in doubt, place the item in NEXT STEPS, not ACTION ITEMS.

INTELLIGENT DIARISATION

A. Never invent names. Use neutral terms when unclear:
     - "Speaker"
     - "Participant"
     - "A participant"

B. Use diarisation labels exactly as given (e.g., "Speaker 1", "Speaker 2").
C. If names appear in the transcript, use them exactly as written.
D. If diarisation is unclear, default to neutral language.
E. Do not assign roles unless explicitly stated.

TONE

Neutral, precise, professional, and adaptive.
- Do not assume meeting purpose.
- Do not add meta text, explanations, or disclaimers.
- Return only the structured summary."""

    async def _generate_and_broadcast_summary(self, conversation_text: str, *, total: bool = False):
        try:
            if config.PROVIDER == "openrouter":
                final_summary = await self._generate_openrouter_summary(conversation_text)
            else:
                final_summary = await self._groq_generate_summary_from_transcript(conversation_text)

            self.last_summary = final_summary
            self.interval_summaries.append(final_summary)

            if total:
                return final_summary

            await self.broadcast_summary(final_summary)
        except asyncio.TimeoutError:  # pragma: no cover - network boundary
            logger.warning("Summary generation timed out (15s)")
        except Exception as exc:  # pragma: no cover - defensive logging
            logger.error("Error generating summary: %s", exc, exc_info=True)

    async def _groq_generate_summary_from_transcript(self, conversation_text: str) -> str:
        response = await asyncio.wait_for(
            self.llm.chat.completions.create(
                model=os.getenv("GROQ_MODEL_NAME") or config.GROQ_MODEL_NAME,
                messages=[
                    {"role": "system", "content": self.get_prompt()},
                    {"role": "user", "content": self.get_content(conversation_text)},
                ],
                max_tokens=2000,
                temperature=0.3,
            ),
            timeout=15.0,
        )
        return response.choices[0].message.content

    def get_content(self, conversation_text: str) -> str:
        return f"Here is the transcript: {conversation_text}\n Here is the prior summary: {self.last_summary}"

    async def _generate_openrouter_summary(self, conversation_text: str) -> str:
        try:
            import httpx
        except ImportError as exc:  # pragma: no cover - import guard
            raise RuntimeError("httpx is required for OpenRouter usage") from exc

        payload: Dict[str, Any] = {
            "model": config.OPENROUTER_MODEL_NAME,
            "messages": [
                {"role": "system", "content": self.get_prompt()},
                {"role": "user", "content": self.get_content(conversation_text)},
            ],
            "max_tokens": 2000,
            "temperature": 0.3,
        }

        response = await self.openrouter_client.post(
            "/chat/completions", json=payload, headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()

        result = response.json()
        return result["choices"][0]["message"]["content"]

    async def broadcast_summary(self, text: str) -> None:
        try:
            message = {"type": "meeting_summary", "message": f"{text}"}
            data = json.dumps(message).encode("utf-8")
            await self.room.local_participant.publish_data(
                payload=data, topic="periodic_summary", reliable=True
            )
            logger.info("Summary broadcasted to room")
        except Exception as exc:  # pragma: no cover - defensive logging
            logger.error("Error broadcasting summary: %s", exc, exc_info=True)


async def note_taker_agent(ctx: agents.JobContext):
    logger.info("Note taker agent dispatched - room %s", ctx.job.room.name)

    try:
        metadata = json.loads(ctx.job.metadata or "{}")
        display_name = metadata.get("display_name", "AI Meeting Assistant")
        identity = metadata.get("identity") or ctx.job.participant.identity or f"{ctx.job.room.name}_noteTaker"
    except Exception as exc:
        logger.warning("Could not parse metadata: %s", exc)
        display_name = "AI Meeting Assistant"
        identity = ctx.job.participant.identity or f"{ctx.job.room.name}_noteTaker"

    if not ctx.job.room.name:
        logger.error("No room name available")
        return

    ctx = generate_token(ctx, display_name, identity)

    logger.info("Connecting to room as '%s'...", display_name)
    await ctx.connect()
    logger.info("Connected as '%s'", display_name)

    room = ctx.room
    note_taker = NoteTakerAgent(room)
    await note_taker.start()

    disconnect_event = asyncio.Event()
    logger.info("Waiting for room '%s' to disconnect...", room.name)

    @room.on("disconnected")
    def on_disconnected():  # noqa: ANN001
        logger.info("Room disconnected")
        disconnect_event.set()

    await disconnect_event.wait()
    if note_taker.total_transcripts:
        try:
            final_sender = FinalSummarySender(
                room=room.name,
                total_transcripts=note_taker.total_transcripts,
                interval_summaries=note_taker.interval_summaries,
            )
            await final_sender.generate_and_send_final_summary()
        except Exception as exc:  # pragma: no cover - defensive logging
            logger.error("Error generating final summary: %s", exc, exc_info=True)


def generate_token(ctx: agents.JobContext, display_name: str, identity: str):
    api_key = config.LIVEKIT_API_KEY
    api_secret = config.LIVEKIT_API_SECRET

    try:
        token = api.AccessToken(api_key, api_secret)
        token.with_identity(identity)
        token.with_name(display_name)
        token.with_grants(api.VideoGrants(room_join=True, room=ctx.job.room.name))

        new_token = token.to_jwt()
        ctx._info.token = new_token
        logger.info("Token created successfully for '%s' (identity: %s)", display_name, identity)
        return ctx
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.error("Failed to create token: %s", exc)
        raise


class FinalSummarySender:
    def __init__(self, room: str, total_transcripts: List[str], interval_summaries: List[str]):
        self.room: str = room
        self.total_transcripts: List[str] = total_transcripts
        self.interval_summaries: List[str] = interval_summaries

        if config.PROVIDER == "groq":
            self.sync_llm = Groq(api_key=os.getenv("GROQ_API_KEY"))
            self.llm = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))
        elif config.PROVIDER == "openrouter":
            import httpx

            self.openrouter_client = httpx.AsyncClient(
                base_url=config.OPENROUTER_BASE_URL,
                headers={"Authorization": f"Bearer {config.OPENROUTER_API_KEY}"},
            )

        self.conversation_text = "\n".join(self.total_transcripts)
        logger.info("FinalSummarySender initialized")

    def get_prompt(self) -> str:
        return """You are UrCalls Meeting Notes Assistant. Your task is to synthesize multiple periodic summaries (generated at regular intervals throughout a meeting) into a single, comprehensive final meeting summary.

    You will receive a list of interval summaries. Your job is to:
    1. Consolidate all information without duplication
    2. Maintain chronological flow of decisions and action items
    3. Eliminate redundant points while preserving context
    4. Create a cohesive narrative of the entire meeting

    Always return the output in this structured format:

    MEETING OVERVIEW
    ● Comprehensive description of the entire meeting, combining all interval summaries into a unified narrative of topics discussed

    KEY DECISIONS
    ● All final decisions made throughout the meeting (consolidated from all intervals, no duplicates)
    ● Remove decisions that were later overridden or contradicted

    ACTION ITEMS
    ● Task — Assignee — Deadline
    ● Include all action items from all intervals
    ● Mark any completed or cancelled items as [COMPLETED] or [CANCELLED]
    ● Consolidate duplicate action items into single entries

    NEXT STEPS
    ● All planned follow-ups and future actions discussed in the meeting

    IMPORTANT NOTES
    ● Critical highlights, clarifications, risks, or emphasis points mentioned across all intervals
    ● Do not repeat notes already covered in other sections

    Rules:
    1. Use only information from the provided interval summaries — do not invent details
    2. Consolidate duplicate information: if the same point appears in multiple summaries, mention it once
    3. Maintain logical flow and coherence across all intervals
    4. Be concise but comprehensive
    5. Do not add preambles, explanations, or meta text. Only output the structured final summary
    6. Ensure the final summary reads as a single cohesive document, not a collection of fragments
    
    7. INTELLIGENT DIARISATION
    A. Never invent names.
    Use neutral terms when unclear:
    ● “Speaker”
    ● “Participant”
    ● “A participant”

    B. Use diarisation labels exactly as given (e.g., “Speaker 1”, “Speaker 2”).
    C. If names appear in the transcript, use them exactly as written.
    D. If diarisation is unclear, default to neutral language.
    E. Do not assign roles unless explicitly stated.
    """

    def _sync_generate_openrouter_summary(self) -> str:
        import requests

        response = requests.post(
            url=f"{config.OPENROUTER_BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {config.OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": config.OPENROUTER_MODEL_NAME,
                "messages": [
                    {"role": "system", "content": self.get_prompt()},
                    {"role": "user", "content": f"Here is the list of summaries: {self.interval_summaries}"},
                ],
                "max_tokens": 2000,
                "temperature": 0.3,
            },
        )
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]

    def _sync_groq_generate_summary_from_transcript(self) -> str:
        response = self.sync_llm.chat.completions.create(
            model=os.getenv("GROQ_MODEL_NAME") or config.GROQ_MODEL_NAME,
            messages=[
                {"role": "system", "content": self.get_prompt()},
                {"role": "user", "content": f"Here is the list of summaries: {self.interval_summaries}"},
            ],
            max_tokens=2000,
            temperature=0.3,
        )
        return response.choices[0].message.content

    def _sync_generate_and_broadcast_summary(self) -> str:
        logger.info("Generating final summary")
        if config.PROVIDER == "openrouter":
            final_summary = self._sync_generate_openrouter_summary()
        else:
            final_summary = self._sync_groq_generate_summary_from_transcript()

        logger.info("Final summary generated (%s chars)", len(final_summary))
        return final_summary

    async def generate_and_send_final_summary(self) -> None:
        if not self.total_transcripts:
            return
        try:
            summary = self._sync_generate_and_broadcast_summary()
            send_and_save_final_summary(summary, self.room)
            logger.info("Final summary generated and sent to backend")
        except Exception as exc:  # pragma: no cover - defensive logging
            logger.error("Error generating final summary: %s", exc, exc_info=True)

    def send_summary(self, summary: str, room_name: str) -> None:
        import requests

        try:
            response = requests.post(
                config.BACKEND_URL, json={"summary": summary, "room_sid": room_name}
            )
            logger.info("Sent summary to backend: %s", response.status_code)
        except Exception as exc:  # pragma: no cover - defensive logging
            logger.error("Error sending summary to backend: %s", exc, exc_info=True)


def send_and_save_final_summary(summary: str, room_name: str) -> None:
    import requests

    try:
        response = requests.post(
            config.BACKEND_URL, json={"summary": summary, "room_sid": room_name}
        )
        logger.info("sent summary to backend: %s", response.status_code)
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.error("Error sending summary to backend: %s", exc, exc_info=True)


server = agents.AgentServer()


@server.rtc_session(agent_name=config.AGENT_NAME)
async def rtc_session(ctx: agents.JobContext):
    await note_taker_agent(ctx)


__all__ = [
    "NoteTakerAgent",
    "FinalSummarySender",
    "note_taker_agent",
    "rtc_session",
    "server",
    "patch_aiohttp_ssl",
]
