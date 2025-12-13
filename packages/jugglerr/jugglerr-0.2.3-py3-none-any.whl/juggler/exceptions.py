"""Custom exceptions for LLM Juggler."""


class LLMJugglerError(Exception):
    """Base exception for LLM Juggler."""
    pass


class NoProvidersAvailableError(LLMJugglerError):
    """Raised when all providers are exhausted."""
    pass


class RateLimitError(LLMJugglerError):
    """Raised when rate limit is hit."""
    pass


class InvalidCapabilityError(LLMJugglerError):
    """Raised when invalid capability is specified."""
    pass


class ModelNotFoundError(LLMJugglerError):
    """Raised when no matching model is found."""
    pass
