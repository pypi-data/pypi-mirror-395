"""
Response objects for Juggler with models_used tracking.

These objects behave like their simple types (str, list) but include
a models_used attribute for debugging and transparency.
"""

from typing import List, Dict, Any, Optional


class ModelAttempt(dict):
    """
    Single model attempt in the fallback chain.
    
    Behaves like a dict for easy serialization.
    """
    def __init__(
        self,
        provider: str,
        model: str,
        success: bool,
        attempt: int,
        status_code: Optional[int] = None,
        error: Optional[str] = None,
        error_type: Optional[str] = None,
        elapsed_ms: Optional[float] = None
    ):
        super().__init__(
            provider=provider,
            model=model,
            success=success,
            attempt=attempt,
            status_code=status_code,
            error=error,
            error_type=error_type,
            elapsed_ms=elapsed_ms
        )
        # Also set as attributes for easy access
        self.provider = provider
        self.model = model
        self.success = success
        self.attempt = attempt
        self.status_code = status_code
        self.error = error
        self.error_type = error_type
        self.elapsed_ms = elapsed_ms


class ChatResponse(str):
    """
    Response from chat() method.
    
    Behaves like a string but has models_used attribute.
    """
    def __new__(cls, content: str, models_used: List[ModelAttempt] = None):
        instance = super().__new__(cls, content)
        instance.models_used = models_used or []
        return instance


class EmbeddingResponse(list):
    """
    Response from embed() method.
    
    Behaves like a list of embeddings but has models_used attribute.
    """
    def __init__(self, embeddings: List[List[float]], models_used: List[ModelAttempt] = None):
        super().__init__(embeddings)
        self.models_used = models_used or []
        self.dimensions = len(embeddings[0]) if embeddings and len(embeddings) > 0 else 0


class RerankResponse(list):
    """
    Response from rerank() method.
    
    Behaves like a list of documents but has models_used attribute.
    """
    def __init__(self, documents: List[str], models_used: List[ModelAttempt] = None, scores: List[float] = None):
        super().__init__(documents)
        self.models_used = models_used or []
        self.scores = scores


class TranscriptionResponse(str):
    """
    Response from transcribe() method.
    
    Behaves like a string but has models_used attribute.
    """
    def __new__(cls, text: str, models_used: List[ModelAttempt] = None, language: str = None, duration: float = None):
        instance = super().__new__(cls, text)
        instance.models_used = models_used or []
        instance.language = language
        instance.duration = duration
        return instance


class SpeechResponse:
    """
    Response from speak() method.
    
    Contains audio data and models_used tracking.
    """
    def __init__(self, audio_data: bytes, models_used: List[ModelAttempt] = None):
        self.audio_data = audio_data
        self.models_used = models_used or []
    
    def write_to_file(self, file_path: str):
        """Write audio data to file."""
        with open(file_path, 'wb') as f:
            f.write(self.audio_data)
    
    def __len__(self) -> int:
        """Return size of audio data in bytes."""
        return len(self.audio_data)
