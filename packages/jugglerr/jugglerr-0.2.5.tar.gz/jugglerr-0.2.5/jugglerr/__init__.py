"""
🤹 Jugglerr - Juggle multiple LLM providers like a pro.

Smart routing, multi-key rotation, and automatic fallbacks for
chat, embeddings, reranking, TTS, and STT across multiple providers.

Example:
    >>> from jugglerr import Jugglerr
    >>> 
    >>> jugglerr = Jugglerr()  # Auto-loads from .env
    >>> 
    >>> # Chat
    >>> response = jugglerr.chat([{"role": "user", "content": "Hello!"}])
    >>> 
    >>> # Embeddings
    >>> embeddings = jugglerr.embed(["text1", "text2"])
    >>> 
    >>> # Reranking
    >>> top_docs = jugglerr.rerank("query", ["doc1", "doc2", "doc3"])
    >>> 
    >>> # Speech-to-Text
    >>> text = jugglerr.transcribe("audio.mp3")
    >>> 
    >>> # Text-to-Speech
    >>> audio = jugglerr.speak("Hello world", voice="Aria")
"""

from .jugglerr import Jugglerr
from .capabilities import Capabilities
from .response import (
    ModelAttempt,
    ChatResponse,
    EmbeddingResponse,
    RerankResponse,
    TranscriptionResponse,
    SpeechResponse
)
from .embedding_adapter import EmbeddingAdapter
from .specialized_adapters import (
    SafetyAdapter,
    TranslationAdapter,
    RivaTTSAdapter
)
from .vision_adapters import (
    VisionAdapter,
    VLMVisionAdapter
)
from .rerank_adapter import (
    RerankAdapter,
    RerankResponse,
    RerankResult,
    rerank
)
from .mistral_adapters import (
    MistralEmbeddingAdapter,
    MistralOCRAdapter,
    MistralModerationAdapter,
    mistral_embed,
    mistral_ocr,
    mistral_moderate
)
from .groq_adapters import (
    GroqTranscriptionAdapter,
    GroqTranslationAdapter,
    GroqTTSAdapter,
    groq_transcribe,
    groq_translate,
    groq_speak
)
from .cohere_adapters import (
    CohereEmbeddingAdapter,
    CohereRerankAdapter,
    cohere_embed,
    cohere_rerank
)
from .exceptions import (
    LLMJugglerError,
    NoProvidersAvailableError,
    RateLimitError,
    InvalidCapabilityError,
    ModelNotFoundError
)
from .version import __version__

__all__ = [
    'Jugglerr',
    'Capabilities',
    'ModelAttempt',
    'ChatResponse',
    'EmbeddingResponse',
    'RerankResponse',
    'TranscriptionResponse',
    'SpeechResponse',
    'EmbeddingAdapter',
    'SafetyAdapter',
    'RivaTTSAdapter',
    'TranslationAdapter',
    'TTSAdapter',
    'VisionAdapter',
    'VLMVisionAdapter',
    'RerankAdapter',
    'RerankResponse',
    'RerankResult',
    'rerank',
    'MistralEmbeddingAdapter',
    'MistralOCRAdapter',
    'MistralModerationAdapter',
    'mistral_embed',
    'mistral_ocr',
    'mistral_moderate',
    'GroqTranscriptionAdapter',
    'GroqTranslationAdapter',
    'GroqTTSAdapter',
    'groq_transcribe',
    'groq_translate',
    'groq_speak',
    'CohereEmbeddingAdapter',
    'CohereRerankAdapter',
    'cohere_embed',
    'cohere_rerank',
    'LLMJugglerError',
    'NoProvidersAvailableError',
    'RateLimitError',
    'InvalidCapabilityError',
    'ModelNotFoundError',
    '__version__'
]
