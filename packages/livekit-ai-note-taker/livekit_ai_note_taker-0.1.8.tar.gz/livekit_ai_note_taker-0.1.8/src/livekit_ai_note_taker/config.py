import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


def _get_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y"}


@dataclass
class AppConfig:
    """Simple settings container for the meeting summarizer agent."""

    LIVEKIT_URL: str = os.getenv("LIVEKIT_URL", "")
    LIVEKIT_API_KEY: str = os.getenv("LIVEKIT_API_KEY", "")
    LIVEKIT_API_SECRET: str = os.getenv("LIVEKIT_API_SECRET", "")

    DEEPGRAM_API_KEY: str = os.getenv("DEEPGRAM_API_KEY", "your_deepgram_api_key")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "your_groq_api_key")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")
    OPENROUTER_MODEL_NAME: str = os.getenv("OPENROUTER_MODEL_NAME", "llama-3.3-70b-versatile")
    GROQ_MODEL_NAME: str = os.getenv("GROQ_MODEL_NAME", "llama-3.3-70b-versatile")
    BACKEND_URL: str = os.getenv("BACKEND_URL", "http://localhost:8000") + "/meetings/meeting-note-webhook"
    SUMMARY_INTERVAL: int = int(os.getenv("SUMMARY_INTERVAL", 150))
    PROVIDER: str = os.getenv("PROVIDER", "groq")  # Options: 'groq', 'openai', 'openrouter'
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    OPENROUTER_BASE_URL: str = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    PROMPT_TYPE: str = os.getenv("PROMPT_TYPE", "small")
    AGENT_NAME: str = os.getenv("AGENT_NAME", "meeting_summarizer")
    DISABLE_SSL_VERIFY: bool = _get_bool("LIVEKIT_SUMMARIZER_DISABLE_SSL_VERIFY", False)

    def validate(self) -> None:
        """Raise if any required LiveKit credentials are missing."""
        required = ["LIVEKIT_URL", "LIVEKIT_API_KEY", "LIVEKIT_API_SECRET"]
        missing = [name for name in required if not getattr(self, name)]
        if missing:
            raise ValueError(f"Missing required configuration fields: {', '.join(missing)}")


config = AppConfig()

__all__ = ["AppConfig", "config"]
