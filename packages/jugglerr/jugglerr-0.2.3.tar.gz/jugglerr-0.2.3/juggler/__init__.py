"""
🤹 Juggler - Juggle multiple LLM providers like a pro.

Smart routing, multi-key rotation, and automatic fallbacks for
chat, embeddings, reranking, TTS, and STT across multiple providers.

Example:
    >>> from juggler import Juggler
    >>> 
    >>> juggler = Juggler()  # Auto-loads from .env
    >>> 
    >>> # Chat
    >>> response = juggler.chat([{"role": "user", "content": "Hello!"}])
    >>> 
    >>> # Embeddings
    >>> embeddings = juggler.embed(["text1", "text2"])
    >>> 
    >>> # Reranking
    >>> top_docs = juggler.rerank("query", ["doc1", "doc2", "doc3"])
    >>> 
    >>> # Speech-to-Text
    >>> text = juggler.transcribe("audio.mp3")
    >>> 
    >>> # Text-to-Speech
    >>> audio = juggler.speak("Hello world", voice="Aria")
"""

from .juggler import Juggler
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
    'Juggler',
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
