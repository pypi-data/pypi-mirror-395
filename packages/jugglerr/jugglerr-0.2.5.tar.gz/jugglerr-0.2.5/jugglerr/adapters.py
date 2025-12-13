"""
Provider adapters for non-standard APIs.

This module provides adapters to convert between standard format
and provider-specific formats for Cohere.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class RateLimitInfo:
    """Rate limit information from provider."""
    requests_remaining: Optional[int] = None
    tokens_remaining: Optional[int] = None
    reset_time: Optional[float] = None
    retry_after: Optional[int] = None


@dataclass
class CompletionResponse:
    """Standardized completion response."""
    content: str
    tokens_used: int
    finish_reason: str
    rate_limits: Optional[RateLimitInfo] = None


class ProviderAdapter(ABC):
    """Base class for all provider adapters."""
    
    @abstractmethod
    def request_to_provider_format(self, messages: List[Dict], **kwargs) -> Dict:
        """Convert standard format to provider format."""
        pass
    
    @abstractmethod
    def response_from_provider_format(self, response: Dict) -> CompletionResponse:
        """Convert provider response back to standard format."""
        pass
    
    @abstractmethod
    def extract_rate_limits(self, headers: Dict) -> RateLimitInfo:
        """Parse rate limit info from response headers."""
        pass
    
    @abstractmethod
    def build_headers(self, api_key: str) -> Dict:
        """Build provider-specific headers."""
        pass


class CohereAdapter(ProviderAdapter):
    """Cohere API adapter - requires format conversion."""
    
    def build_headers(self, api_key: str) -> Dict:
        return {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
    
    def request_to_provider_format(self, messages: List[Dict], **kwargs) -> Dict:
        """Convert standard messages to Cohere format."""
        # Ensure messages is a list
        if not isinstance(messages, list):
            raise ValueError(f"messages must be a list, got {type(messages)}: {messages}")
        
        # Cohere uses different role names: "User" and "Chatbot"
        chat_history = []
        message = None
        
        for msg in messages:
            if not isinstance(msg, dict):
                raise ValueError(f"Each message must be a dict, got {type(msg)}: {msg}")
            role = msg["role"]
            content = msg["content"]
            
            if role == "system":
                # Cohere handles system via preamble
                continue
            elif role == "user":
                if message is None:
                    message = content  # Last user message
                else:
                    chat_history.append({"role": "User", "message": content})
            elif role == "assistant":
                chat_history.append({"role": "Chatbot", "message": content})
        
        payload = {
            "message": message or "Hello",
            "chat_history": chat_history if chat_history else [],
            "temperature": kwargs.get('temperature', 0.7),
            "max_tokens": kwargs.get('max_tokens', 1024)
        }
        
        # Add streaming if requested
        if kwargs.get('stream'):
            payload['stream'] = True
        
        return payload
    
    def response_from_provider_format(self, response: Dict) -> CompletionResponse:
        """Convert Cohere response to standard format."""
        try:
            # Handle case where response might be a string (error case)
            if isinstance(response, str):
                raise ValueError(f"Expected dict but got string: {response[:100]}")
            
            content = response.get("text", "")
            
            meta = response.get("meta", {})
            tokens = meta.get("billed_units", {})
            tokens_used = tokens.get("input_tokens", 0) + tokens.get("output_tokens", 0)
            
            finish_reason = "stop" if response.get("finish_reason") == "COMPLETE" else "length"
            
            return CompletionResponse(
                content=content,
                tokens_used=tokens_used,
                finish_reason=finish_reason
            )
        except Exception as e:
            raise ValueError(f"Failed to parse Cohere response: {e}. Response type: {type(response)}, Response: {str(response)[:200]}")
    
    def extract_rate_limits(self, headers: Dict) -> RateLimitInfo:
        """Extract rate limit info from Cohere headers."""
        return RateLimitInfo(
            requests_remaining=int(headers.get('x-ratelimit-remaining', 0)) if headers.get('x-ratelimit-remaining') else None,
            retry_after=int(headers.get('retry-after', 0)) if headers.get('retry-after') else None
        )
    
    def parse_stream_chunk(self, chunk_data: Dict) -> Optional[str]:
        """
        Parse a Cohere streaming chunk and extract text content.
        
        Cohere streaming format:
        - event_type: "stream-start", "text-generation", "stream-end"
        - text: The generated text chunk
        
        Args:
            chunk_data: Parsed JSON chunk from Cohere stream
        
        Returns:
            Text content or None if no text in chunk
        """
        event_type = chunk_data.get('event_type')
        
        # Only extract text from text-generation events
        if event_type == 'text-generation':
            return chunk_data.get('text', '')
        
        return None



