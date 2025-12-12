"""IndusLabs Voice API SDK."""

from .client import (
    Client,
    TTS,
    STT,
    Voices,
    Voice,
    TTSResponse,
    TTSStreamResponse,
    AsyncTTSStreamResponse,
    STTResponse,
    STTResponse,
    STTStreamResponse,
    STTSegment,
    STTMetrics,
    VoiceResponse,
)

__version__ = "0.0.6"
__all__ = [
    "Client",
    "TTS",
    "STT",
    "Voices",
    "Voice",
    "TTSResponse",
    "TTSStreamResponse",
    "AsyncTTSStreamResponse",
    "STTResponse",
    "VoiceResponse",
]
