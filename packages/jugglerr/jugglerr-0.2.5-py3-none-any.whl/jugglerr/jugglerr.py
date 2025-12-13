"""
Jugglerr - Multi-provider routing with intelligent key selection.

Features:
- Power-based routing (super vs regular)
- Capability-based routing (streaming, vision, tool_calling, etc.)
- Context window routing (large, medium, small)
- Smart key selection with rate limit awareness
- Automatic fallbacks across providers
"""

import os
import time
import random
import logging
import requests
from typing import List, Dict, Optional, Any
from tenacity import retry, stop_after_attempt, wait_exponential
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from .models import (
    MODEL_DATABASE,
    CAP_STREAMING,
    CAP_STRUCTURED_OUTPUTS,
    CAP_TOOL_CALLING,
    CAP_TOOL_CALLING_STRUCTURED,
    CAP_PARALLEL_TOOL_CALLING,
    CAP_BROWSER_SEARCH,
    CAP_CODE_EXECUTION,
    CAP_JSON_OBJECT,
    CAP_JSON_SCHEMA,
    CAP_REASONING,
    CAP_VISION,
    CAP_MULTILINGUAL,
    CONTEXT_LARGE,
    CONTEXT_MEDIUM,
    CONTEXT_SMALL,
    POWER_SUPER,
    POWER_REGULAR
)
from .exceptions import NoProvidersAvailableError
from .response import (
    ModelAttempt,
    ChatResponse,
    EmbeddingResponse,
    RerankResponse,
    TranscriptionResponse,
    SpeechResponse
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API endpoints
API_ENDPOINTS = {
    # v0.1.0 providers
    'cerebras': 'https://api.cerebras.ai/v1/chat/completions',
    'groq': 'https://api.groq.com/openai/v1/chat/completions',
    'mistral': 'https://api.mistral.ai/v1/chat/completions',
    # v0.2.0 providers
    'nvidia': 'https://integrate.api.nvidia.com/v1/chat/completions',
    'cohere': 'https://api.cohere.ai/v1/chat'
}

# Provider priority (free first, paid last)
PROVIDER_PRIORITY = [
    'cerebras', 'groq', 'nvidia',  # Free tiers
    'mistral', 'cohere'  # Paid
]


class Jugglerr:
    """
    Jugglerr - Multi-provider intelligent routing for LLMs and specialized models.
    
    Features:
    - Smart provider selection (free first)
    - Rate limit header parsing (Cerebras, Groq)
    - In-memory state cache for key selection
    - Automatic key rotation
    - Reactive 429 handling (Mistral)
    - Automatic fallback for chat, embeddings, reranking, TTS, STT
    
    Example:
        >>> from jugglerr import Jugglerr
        >>> 
        >>> jugglerr = Jugglerr()  # Auto-loads from .env
        >>> response = jugglerr.chat("Hello, world!")
        >>> print(response)
    """
    
    def __init__(
        self,
        groq_keys: Optional[List[str]] = None,
        cerebras_keys: Optional[List[str]] = None,
        mistral_keys: Optional[List[str]] = None,
        nvidia_keys: Optional[List[str]] = None,
        cohere_keys: Optional[List[str]] = None
    ):
        """
        Initialize Jugglerr with API keys.
        
        API keys can be provided directly or loaded from environment variables.
        Environment variables should be comma-separated lists.
        
        Args:
            groq_keys: List of Groq API keys (or loads from GROQ_API_KEYS)
            cerebras_keys: List of Cerebras API keys (or loads from CEREBRAS_API_KEYS)
            mistral_keys: List of Mistral API keys (or loads from MISTRAL_API_KEYS)
            nvidia_keys: List of NVIDIA API keys (or loads from NVIDIA_API_KEYS)
            cohere_keys: List of Cohere API keys (or loads from COHERE_API_KEYS)
            
        Example:
            >>> # Auto-load from .env file
            >>> jugglerr = Jugglerr()
            
            >>> # Or pass keys directly
            >>> jugglerr = Jugglerr(
            ...     cerebras_keys=["csk_key1", "csk_key2"],
            ...     groq_keys=["gsk_key1"]
            ... )
        """
        # Load API keys (from args or environment)
        self.cerebras_keys = cerebras_keys or self._load_keys('CEREBRAS_API_KEYS')
        self.groq_keys = groq_keys or self._load_keys('GROQ_API_KEYS')
        self.mistral_keys = mistral_keys or self._load_keys('MISTRAL_API_KEYS')
        self.nvidia_keys = nvidia_keys or self._load_keys('NVIDIA_API_KEYS')
        self.cohere_keys = cohere_keys or self._load_keys('COHERE_API_KEYS')
        
        # In-memory state cache: {provider_key: {remaining_requests, remaining_tokens, reset_at, ...}}
        self.key_state = {}
        
        logger.info("🤹 Jugglerr initialized")
        logger.info(f"  Cerebras keys: {len(self.cerebras_keys)}")
        logger.info(f"  Groq keys: {len(self.groq_keys)}")
        logger.info(f"  Mistral keys: {len(self.mistral_keys)}")
        logger.info(f"  NVIDIA keys: {len(self.nvidia_keys)}")
        logger.info(f"  Cohere keys: {len(self.cohere_keys)}")
    
    def _load_keys(self, env_var: str) -> List[str]:
        """
        Load API keys from environment variable.
        
        Args:
            env_var: Environment variable name (e.g., 'GROQ_API_KEYS')
            
        Returns:
            List of API keys (comma-separated values from env var)
            
        Example:
            GROQ_API_KEYS="key1,key2,key3" -> ["key1", "key2", "key3"]
        """
        keys_str = os.getenv(env_var, '')
        keys = [k.strip() for k in keys_str.split(',') if k.strip()]
        return keys
    
    def _find_matching_model(
        self,
        provider: str,
        llm_power: str,
        llm_capabilities: Optional[List[str]] = None,
        llm_context_window: Optional[str] = None
    ) -> Optional[str]:
        """
        Find best matching model for given requirements.
        
        Args:
            provider: Provider name
            llm_power: "super" or "regular"
            llm_capabilities: List of required capabilities
            llm_context_window: Required context window (large, medium, small)
        
        Returns:
            Model name or None if no match found
        """
        provider_models = MODEL_DATABASE.get(provider, {})
        if not provider_models:
            logger.warning(f"No models configured for provider: {provider}")
            return None
        
        # Filter models by requirements
        matching_models = []
        
        for model_name, model_info in provider_models.items():
            # Check power level
            if model_info.get('power') != llm_power:
                continue
            
            # Check capabilities (if specified)
            if llm_capabilities:
                model_capabilities = model_info.get('capabilities', [])
                if not all(cap in model_capabilities for cap in llm_capabilities):
                    continue
            
            # Check context window (if specified)
            if llm_context_window:
                if model_info.get('context_window') != llm_context_window:
                    continue
            
            matching_models.append(model_name)
        
        if not matching_models:
            # Fallback: try without context window requirement
            if llm_context_window:
                logger.warning(f"No models found with context_window={llm_context_window}, trying without")
                return self._find_matching_model(provider, llm_power, llm_capabilities, None)
            
            # Fallback: try without capabilities requirement
            if llm_capabilities:
                logger.warning(f"No models found with capabilities={llm_capabilities}, trying without")
                return self._find_matching_model(provider, llm_power, None, llm_context_window)
            
            # Fallback: try regular power if super not available
            if llm_power == 'super':
                logger.warning(f"No super models found, trying regular")
                return self._find_matching_model(provider, 'regular', llm_capabilities, llm_context_window)
            
            logger.warning(f"No matching models found for {provider}")
            return None
        
        # Return first matching model
        return matching_models[0]
    
    def _mask_key(self, api_key: str) -> str:
        """Mask API key for logging."""
        if len(api_key) <= 14:
            return api_key[:4] + '...' + api_key[-2:]
        return api_key[:10] + '...' + api_key[-4:]
    
    def _parse_rate_limit_headers(self, provider: str, response: requests.Response) -> Optional[Dict[str, Any]]:
        """
        Parse rate limit headers from response.
        
        Cerebras headers (day-level requests, minute-level tokens):
        - x-ratelimit-remaining-requests-day
        - x-ratelimit-remaining-tokens-minute
        - x-ratelimit-reset-requests-day (seconds)
        - x-ratelimit-reset-tokens-minute (seconds)
        
        OpenAI/Groq/Mistral headers (standard format):
        - x-ratelimit-remaining-requests
        - x-ratelimit-remaining-tokens
        - x-ratelimit-reset-requests (timestamp or seconds)
        - x-ratelimit-reset-tokens (timestamp or seconds)
        - retry-after (seconds, only on 429)
        """
        if provider == 'cerebras':
            # Cerebras: Day-level request tracking, minute-level token tracking
            remaining_requests = response.headers.get('x-ratelimit-remaining-requests-day')
            remaining_tokens = response.headers.get('x-ratelimit-remaining-tokens-minute')
            reset_requests = response.headers.get('x-ratelimit-reset-requests-day')
            reset_tokens = response.headers.get('x-ratelimit-reset-tokens-minute')
            
            if remaining_requests is not None:
                try:
                    return {
                        'remaining_requests': int(float(remaining_requests)),
                        'remaining_tokens': int(float(remaining_tokens)) if remaining_tokens else 0,
                        'reset_requests_at': time.time() + int(float(reset_requests)) if reset_requests else 0,
                        'reset_tokens_at': time.time() + int(float(reset_tokens)) if reset_tokens else 0
                    }
                except (ValueError, TypeError):
                    # If parsing fails, skip rate limit tracking
                    pass
        
        elif provider in ['groq', 'mistral']:
            # Standard format for Groq/Mistral
            remaining_requests = response.headers.get('x-ratelimit-remaining-requests')
            remaining_tokens = response.headers.get('x-ratelimit-remaining-tokens')
            reset_requests = response.headers.get('x-ratelimit-reset-requests')
            reset_tokens = response.headers.get('x-ratelimit-reset-tokens')
            retry_after = response.headers.get('retry-after')
            
            if remaining_requests is not None:
                try:
                    # Parse reset times - can be timestamps or durations like "4m19.2s"
                    def parse_time(val):
                        if not val:
                            return 0
                        # If it contains time format like "4m19.2s", skip it
                        if 'm' in str(val) or 's' in str(val):
                            return 0
                        return int(float(val))
                    
                    return {
                        'remaining_requests': int(float(remaining_requests)),
                        'remaining_tokens': int(float(remaining_tokens)) if remaining_tokens else 0,
                        'reset_requests_at': parse_time(reset_requests),
                        'reset_tokens_at': parse_time(reset_tokens),
                        'retry_after': parse_time(retry_after)
                    }
                except (ValueError, TypeError):
                    # If parsing fails, skip rate limit tracking
                    pass
        
        return None
    
    def _update_key_state(self, provider: str, api_key: str, state: Dict[str, Any]):
        """Update in-memory state for a key."""
        cache_key = f"{provider}:{self._mask_key(api_key)}"
        self.key_state[cache_key] = {
            **state,
            'updated_at': time.time()
        }
        
        logger.debug(f"Updated state for {cache_key}: {state}")
    
    def _get_key_state(self, provider: str, api_key: str) -> Optional[Dict[str, Any]]:
        """Get cached state for a key."""
        cache_key = f"{provider}:{self._mask_key(api_key)}"
        return self.key_state.get(cache_key)
    
    def _select_best_key(self, provider: str, api_keys: List[str]) -> str:
        """
        Select best key based on cached rate limit state.
        
        For Cerebras/Groq: Use cached state to pick key with most remaining capacity.
        For Mistral: Random selection (no header info).
        """
        if not api_keys:
            return None
        
        if provider in ['cerebras', 'groq']:
            # Smart selection based on cached state
            best_key = None
            best_score = -1
            now = time.time()
            
            for key in api_keys:
                state = self._get_key_state(provider, key)
                
                if state:
                    # Check if reset times have passed
                    if state.get('reset_requests_at', 0) < now:
                        # Reset has passed, assume full capacity
                        score = 1000000
                    else:
                        # Use remaining capacity as score
                        score = state.get('remaining_requests', 0) + (state.get('remaining_tokens', 0) / 1000)
                    
                    # Skip keys with zero remaining
                    if score <= 0:
                        continue
                    
                    if score > best_score:
                        best_score = score
                        best_key = key
                else:
                    # No state yet, try this key
                    return key
            
            return best_key or api_keys[0]  # Fallback to first key
        else:
            # Random selection for Mistral
            return random.choice(api_keys)
    
    def _make_request(
        self,
        provider: str,
        api_key: str,
        model: str,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Make LLM API request and parse rate limit headers.
        
        Returns:
            dict: {'success': bool, 'response': dict|None, 'error': str|None, 'rate_limited': bool}
        """
        # Handle providers that need adapters
        if provider in ['cohere']:
            return self._make_adapter_request(provider, api_key, model, messages, temperature, max_tokens, **kwargs)
        
        # Get endpoint
        endpoint = API_ENDPOINTS.get(provider)
        if not endpoint:
            return {'success': False, 'response': None, 'error': f'Unknown provider: {provider}', 'rate_limited': False}
        
        # Build headers
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        

        
        # Build payload with provider-specific parameters
        if provider == 'cerebras':
            # CRITICAL: Cerebras uses max_completion_tokens instead of max_tokens
            payload = {
                'model': model,
                'messages': messages,
                'temperature': temperature,
                'max_completion_tokens': max_tokens,
                **kwargs
            }
        else:
            payload = {
                'model': model,
                'messages': messages,
                'temperature': temperature,
                'max_tokens': max_tokens,
                **kwargs
            }
        
        masked_key = self._mask_key(api_key)
        logger.info(f"📤 {provider} request: model={model}, key={masked_key}, messages={len(messages)}")
        
        # Retry logic for rate limits
        max_retries = 2 if provider == 'mistral' else 1
        
        try:
            for attempt in range(max_retries):
                # Exponential backoff for retries (only after first attempt)
                if attempt > 0:
                    backoff_time = min(2 ** attempt, 4)  # Max 4 seconds
                    time.sleep(backoff_time)
                
                response = requests.post(endpoint, headers=headers, json=payload, timeout=60)
                
                # Parse rate limit headers
                rate_limit_info = self._parse_rate_limit_headers(provider, response)
                if rate_limit_info:
                    self._update_key_state(provider, api_key, rate_limit_info)
                    logger.info(f"  Rate limits: requests={rate_limit_info.get('remaining_requests')}, tokens={rate_limit_info.get('remaining_tokens')}")
                
                if response.status_code == 200:
                    logger.info(f"✅ {provider} success")
                    return {'success': True, 'response': response.json(), 'error': None, 'rate_limited': False}
                elif response.status_code == 429:
                    # Rate limited - check if we should retry
                    if attempt < max_retries - 1:
                        retry_after = int(response.headers.get('retry-after', 2))
                        # Add random jitter to avoid thundering herd (Perplexity Dec 2025 guidance)
                        jitter = random.uniform(0, 2)
                        total_wait = retry_after + jitter
                        logger.warning(f"⏱️  {provider} rate limited, retrying after {total_wait:.1f}s (attempt {attempt + 1}/{max_retries})")
                        time.sleep(total_wait)
                        continue
                    else:
                        logger.warning(f"⏱️  {provider} rate limited (key={masked_key})")
                        return {'success': False, 'response': None, 'error': 'Rate limited', 'rate_limited': True}
                else:
                    error_msg = f'HTTP {response.status_code}: {response.text[:200]}'
                    logger.error(f"❌ {provider} failed: {error_msg}")
                    return {'success': False, 'response': None, 'error': error_msg, 'rate_limited': False}
        
        except requests.exceptions.Timeout:
            logger.error(f"❌ {provider} timeout")
            return {'success': False, 'response': None, 'error': 'Request timeout', 'rate_limited': False}
        except Exception as e:
            logger.error(f"❌ {provider} exception: {e}")
            return {'success': False, 'response': None, 'error': str(e), 'rate_limited': False}
    
    def _make_adapter_request(
        self,
        provider: str,
        api_key: str,
        model: str,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Make request using provider adapter for non-standard APIs.
        
        Returns:
            dict: {'success': bool, 'response': dict|None, 'error': str|None, 'rate_limited': bool}
        """
        from .adapters import CohereAdapter
        
        masked_key = self._mask_key(api_key)
        logger.info(f"📤 {provider} adapter request: model={model}, key={masked_key}, messages={len(messages)}")
        
        try:
            # Select adapter
            if provider == 'cohere':
                adapter = CohereAdapter()
                endpoint = API_ENDPOINTS[provider]
            else:
                return {'success': False, 'response': None, 'error': f'No adapter for {provider}', 'rate_limited': False}
            
            # Build request
            headers = adapter.build_headers(api_key)
            payload = adapter.request_to_provider_format(
                messages,
                temperature=temperature,
                max_tokens=max_tokens,
                model=model,  # Pass model to adapter
                **kwargs
            )
            
            # Make request with retry logic
            max_retries = 1
            last_error = None
            
            for attempt in range(max_retries):
                # Exponential backoff for retries (only after first attempt)
                if attempt > 0:
                    backoff_time = min(2 ** attempt, 8)  # Max 8 seconds
                    time.sleep(backoff_time)
                
                response = requests.post(endpoint, headers=headers, json=payload, timeout=60)
                
                if response.status_code == 200:
                    try:
                        # Convert response to standard format
                        completion = adapter.response_from_provider_format(response.json())
                        
                        # Build standard response format
                        standard_response = {
                            'choices': [{
                                'message': {
                                    'role': 'assistant',
                                    'content': completion.content
                                },
                                'finish_reason': completion.finish_reason
                            }],
                            'usage': {
                                'total_tokens': completion.tokens_used
                            }
                        }
                        
                        logger.info(f"✅ {provider} adapter success")
                        return {'success': True, 'response': standard_response, 'error': None, 'rate_limited': False}
                    
                    except ValueError as e:
                        # Check if it's a retry-able error (empty response or safety block)
                        error_str = str(e)
                        is_retryable = ("Empty response" in error_str or "intermittent" in error_str)
                        
                        if is_retryable and attempt < max_retries - 1:
                            logger.warning(f"⚠️  {provider} {error_str[:50]}, retrying (attempt {attempt + 1}/{max_retries})")
                            last_error = error_str
                            continue
                        else:
                            # Not retry-able or out of retries
                            raise
                
                elif response.status_code == 429:
                    logger.warning(f"⏱️  {provider} rate limited (key={masked_key})")
                    return {'success': False, 'response': None, 'error': 'Rate limited', 'rate_limited': True}
                else:
                    error_msg = f'HTTP {response.status_code}: {response.text[:200]}'
                    logger.error(f"❌ {provider} adapter failed: {error_msg}")
                    return {'success': False, 'response': None, 'error': error_msg, 'rate_limited': False}
            
            # If we get here, all retries failed
            if last_error:
                logger.error(f"❌ {provider} adapter failed after {max_retries} retries: {last_error}")
                return {'success': False, 'response': None, 'error': last_error, 'rate_limited': False}
            elif response.status_code == 429:
                logger.warning(f"⏱️  {provider} rate limited (key={masked_key})")
                return {'success': False, 'response': None, 'error': 'Rate limited', 'rate_limited': True}
            else:
                error_msg = f'HTTP {response.status_code}: {response.text[:200]}'
                logger.error(f"❌ {provider} adapter failed: {error_msg}")
                return {'success': False, 'response': None, 'error': error_msg, 'rate_limited': False}
        
        except Exception as e:
            logger.error(f"❌ {provider} adapter exception: {e}")
            return {'success': False, 'response': None, 'error': str(e), 'rate_limited': False}
    
    def _try_provider(
        self,
        provider: str,
        api_keys: List[str],
        llm_power: str,
        llm_capabilities: Optional[List[str]],
        llm_context_window: Optional[str],
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000,
        preferred_model: Optional[str] = None,
        **kwargs
    ) -> Optional[Dict[str, Any]]:
        """
        Try all keys for a provider until one works.
        
        Returns:
            dict: {'provider': str, 'model': str, 'response': dict} or None
        """
        if not api_keys:
            logger.debug(f"No API keys configured for {provider}")
            return None
        
        # Use preferred_model if specified, otherwise find matching model
        if preferred_model:
            model = preferred_model
        else:
            model = self._find_matching_model(provider, llm_power, llm_capabilities, llm_context_window)
            if not model:
                logger.warning(f"No matching model found for {provider} (power={llm_power}, capabilities={llm_capabilities}, context={llm_context_window})")
                return None
        
        logger.info(f"🎯 Trying {provider} with {len(api_keys)} keys, model={model}, power={llm_power}")
        if llm_capabilities:
            logger.info(f"  Required capabilities: {llm_capabilities}")
        if llm_context_window:
            logger.info(f"  Required context: {llm_context_window}")
        
        # Try keys in smart order
        for attempt in range(len(api_keys)):
            # Select best key based on cached state
            api_key = self._select_best_key(provider, api_keys)
            if not api_key:
                logger.warning(f"No available keys for {provider}")
                break
            
            result = self._make_request(provider, api_key, model, messages, temperature, max_tokens, **kwargs)
            
            if result['success']:
                return {
                    'provider': provider,
                    'model': model,
                    'response': result['response']
                }
            elif result['rate_limited']:
                # Try next key
                logger.info(f"Key rate limited, trying next key...")
                continue
            else:
                # Other error, try next key
                logger.info(f"Key failed: {result['error']}, trying next key...")
                continue
        
        logger.warning(f"All {provider} keys exhausted")
        return None
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True
    )
    def chat(
        self,
        messages: str | List[Dict[str, str]],
        power: str = "regular",
        capabilities: Optional[List[str]] = None,
        context_window: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        preferred_provider: Optional[str] = None,
        preferred_model: Optional[str] = None,
        **kwargs
    ) -> ChatResponse:
        """
        Make chat completion request with intelligent provider routing.
        
        Automatically selects the best model based on requirements and falls back
        to alternative providers if one fails. Tracks all attempts in response.
        
        Args:
            messages: String for simple queries, or list of message dicts with 'role' and 'content'
            power: "super" for large models (70B+), "regular" for smaller models (7B-32B)
            capabilities: List of required capabilities (streaming, vision, tool_calling, etc.)
            context_window: Required context window - "large" (100K+), "medium" (30K-100K), "small" (<30K)
            temperature: Sampling temperature (0.0 to 2.0). Lower = more focused, higher = more creative
            max_tokens: Maximum tokens to generate
            preferred_provider: Preferred provider ("cerebras", "groq", "nvidia", "mistral", "cohere")
            preferred_model: Specific model ID to use (overrides automatic model selection)
            **kwargs: Additional provider-specific parameters
        
        Returns:
            ChatResponse: Response text with models_used tracking (behaves like str)
        
        Raises:
            NoProvidersAvailableError: If all providers fail
        
        Example:
            >>> # Simple string query
            >>> response = jugglerr.chat("What is 2+2?")
            >>> print(response)  # "4"
            >>> 
            >>> # With conversation history
            >>> response = jugglerr.chat([
            ...     {"role": "user", "content": "Hello!"},
            ...     {"role": "assistant", "content": "Hi there!"},
            ...     {"role": "user", "content": "How are you?"}
            ... ])
            >>> 
            >>> # Access tracking info
            >>> print(response.models_used)
            >>> # [{'provider': 'cerebras', 'model': 'llama3.1-8b', 'success': True, ...}]
        """
        # Convert string to message list if needed
        if isinstance(messages, str):
            messages = [{"role": "user", "content": messages}]
        
        logger.info("=" * 60)
        logger.info(f"🤹 Juggling request: power={power}, messages={len(messages)}, temp={temperature}")
        if capabilities:
            logger.info(f"  Required capabilities: {capabilities}")
        if context_window:
            logger.info(f"  Required context: {context_window}")
        
        # Track all attempts
        models_used = []
        attempt_num = 0
        
        # Determine provider priority
        # If a specific model is requested, find its provider and use ONLY that provider
        if preferred_model:
            model_provider = None
            for provider_name, provider_models in MODEL_DATABASE.items():
                if preferred_model in provider_models:
                    model_provider = provider_name
                    break
            
            if model_provider:
                priority = [model_provider]
                logger.info(f"Specific model '{preferred_model}' requested - using ONLY provider: {model_provider}")
            else:
                # Model not found in database, use normal priority
                logger.warning(f"Model '{preferred_model}' not found in database, using normal provider priority")
                if preferred_provider and preferred_provider in PROVIDER_PRIORITY:
                    priority = [preferred_provider] + [p for p in PROVIDER_PRIORITY if p != preferred_provider]
                else:
                    priority = PROVIDER_PRIORITY
        elif preferred_provider and preferred_provider in PROVIDER_PRIORITY:
            priority = [preferred_provider] + [p for p in PROVIDER_PRIORITY if p != preferred_provider]
        else:
            priority = PROVIDER_PRIORITY
        
        logger.info(f"Provider priority: {priority}")
        
        # Try providers in order
        for provider in priority:
            # Get API keys for provider
            if provider == 'cerebras':
                api_keys = self.cerebras_keys
            elif provider == 'groq':
                api_keys = self.groq_keys
            elif provider == 'mistral':
                api_keys = self.mistral_keys
            elif provider == 'nvidia':
                api_keys = self.nvidia_keys
            elif provider == 'cohere':
                api_keys = self.cohere_keys
            else:
                continue
            
            if not api_keys:
                logger.debug(f"Skipping {provider}: No API keys configured")
                continue
            
            attempt_num += 1
            start_time = time.time()
            
            result = self._try_provider(
                provider, api_keys, power, capabilities, context_window,
                messages, temperature, max_tokens, preferred_model, **kwargs
            )
            
            elapsed_ms = (time.time() - start_time) * 1000
            
            if result:
                # Success - record attempt
                models_used.append(ModelAttempt(
                    provider=result['provider'],
                    model=result['model'],
                    success=True,
                    attempt=attempt_num,
                    status_code=200,
                    elapsed_ms=elapsed_ms
                ))
                
                logger.info("=" * 60)
                logger.info(f"✅ SUCCESS: {result['provider']} / {result['model']}")
                logger.info("=" * 60)
                
                # Extract text from response and return with tracking
                content = result['response']['choices'][0]['message']['content']
                return ChatResponse(content, models_used)
            else:
                # Failed - record attempt (result is None, so we don't have detailed error info)
                # The _try_provider method should be updated to return error details
                models_used.append(ModelAttempt(
                    provider=provider,
                    model="unknown",
                    success=False,
                    attempt=attempt_num,
                    error="Provider failed",
                    elapsed_ms=elapsed_ms
                ))
        
        # All providers failed
        error_msg = f"All providers exhausted. Tried: {', '.join(priority)}"
        logger.error("=" * 60)
        logger.error(f"❌ FAILURE: {error_msg}")
        logger.error("=" * 60)
        
        # Raise error with tracking info attached
        error = NoProvidersAvailableError(error_msg)
        error.models_used = models_used
        raise error
    
    def chat_stream(
        self,
        messages: str | List[Dict[str, str]],
        power: str = "regular",
        capabilities: Optional[List[str]] = None,
        context_window: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        preferred_provider: Optional[str] = None,
        preferred_model: Optional[str] = None,
        **kwargs
    ):
        """
        Make streaming chat completion request with intelligent provider routing.
        
        Yields tokens as they arrive from the LLM in real-time, similar to ChatGPT's
        streaming interface. Useful for building interactive chat applications.
        
        Args:
            messages: String for simple queries, or list of message dicts with 'role' and 'content'
            power: "super" for large models (70B+), "regular" for smaller models (7B-32B)
            capabilities: List of required capabilities (streaming, vision, tool_calling, etc.)
            context_window: Required context window - "large" (100K+), "medium" (30K-100K), "small" (<30K)
            temperature: Sampling temperature (0.0 to 2.0). Lower = more focused, higher = more creative
            max_tokens: Maximum tokens to generate
            preferred_provider: Preferred provider ("cerebras", "groq", "mistral", "nvidia", "cohere")
            preferred_model: Specific model ID to use
            **kwargs: Additional provider-specific parameters
        
        Yields:
            str: Individual tokens/chunks as they arrive from the model
        
        Raises:
            NoProvidersAvailableError: If all providers fail
        
        Example:
            >>> # Stream a response
            >>> for chunk in jugglerr.chat_stream("Tell me a story"):
            ...     print(chunk, end='', flush=True)
            >>> 
            >>> # With parameters
            >>> for chunk in jugglerr.chat_stream(
            ...     "Explain quantum physics",
            ...     power="super",
            ...     temperature=0.3
            ... ):
            ...     print(chunk, end='', flush=True)
        """
        # Convert string to message list if needed
        if isinstance(messages, str):
            messages = [{"role": "user", "content": messages}]
        
        logger.info("=" * 60)
        logger.info(f"🤹 Streaming request: power={power}, messages={len(messages)}, temp={temperature}")
        if capabilities:
            logger.info(f"  Required capabilities: {capabilities}")
        if context_window:
            logger.info(f"  Required context: {context_window}")
        
        # Determine provider priority
        # If a specific model is requested, find its provider and use ONLY that provider
        if preferred_model:
            model_provider = None
            for provider_name, provider_models in MODEL_DATABASE.items():
                if preferred_model in provider_models:
                    model_provider = provider_name
                    break
            
            if model_provider:
                priority = [model_provider]
                logger.info(f"Specific model '{preferred_model}' requested - using ONLY provider: {model_provider}")
            else:
                # Model not found in database, use normal priority
                logger.warning(f"Model '{preferred_model}' not found in database, using normal provider priority")
                if preferred_provider and preferred_provider in PROVIDER_PRIORITY:
                    priority = [preferred_provider] + [p for p in PROVIDER_PRIORITY if p != preferred_provider]
                else:
                    priority = PROVIDER_PRIORITY
        elif preferred_provider and preferred_provider in PROVIDER_PRIORITY:
            priority = [preferred_provider] + [p for p in PROVIDER_PRIORITY if p != preferred_provider]
        else:
            priority = PROVIDER_PRIORITY
        
        logger.info(f"Provider priority: {priority}")
        
        # Try providers in order
        for provider in priority:
            # Get API keys for provider
            if provider == 'cerebras':
                api_keys = self.cerebras_keys
            elif provider == 'groq':
                api_keys = self.groq_keys
            elif provider == 'mistral':
                api_keys = self.mistral_keys
            elif provider == 'nvidia':
                api_keys = self.nvidia_keys
            elif provider == 'cohere':
                api_keys = self.cohere_keys
            else:
                continue
            
            if not api_keys:
                logger.debug(f"Skipping {provider}: No API keys configured")
                continue
            
            # Try streaming with this provider
            try:
                for chunk in self._try_provider_stream(
                    provider, api_keys, power, capabilities, context_window,
                    messages, temperature, max_tokens, preferred_model, **kwargs
                ):
                    yield chunk
                
                # If we got here, streaming succeeded
                logger.info("=" * 60)
                logger.info(f"✅ STREAMING SUCCESS: {provider}")
                logger.info("=" * 60)
                return
                
            except Exception as e:
                logger.warning(f"⚠️  {provider} streaming failed: {e}")
                continue
        
        # All providers failed
        error_msg = f"All providers exhausted for streaming. Tried: {', '.join(priority)}"
        logger.error("=" * 60)
        logger.error(f"❌ STREAMING FAILURE: {error_msg}")
        logger.error("=" * 60)
        raise NoProvidersAvailableError(error_msg)
    
    def _try_provider_stream(
        self,
        provider: str,
        api_keys: List[str],
        power: str,
        capabilities: Optional[List[str]],
        context_window: Optional[str],
        messages: List[Dict[str, str]],
        temperature: float,
        max_tokens: int,
        preferred_model: Optional[str],
        **kwargs
    ):
        """Try streaming with a specific provider."""
        # Find matching model
        if preferred_model:
            model = preferred_model
        else:
            model = self._find_matching_model(provider, power, capabilities, context_window)
        
        if not model:
            raise Exception(f"No matching model found for {provider}")
        
        # Select best API key
        api_key = self._select_best_key(provider, api_keys)
        if not api_key:
            raise Exception(f"No available API key for {provider}")
        
        # Handle Cohere separately (different API format)
        if provider == 'cohere':
            yield from self._cohere_stream(api_key, model, messages, temperature, max_tokens, **kwargs)
            return
        
        # Make streaming request for standard providers
        endpoint = API_ENDPOINTS.get(provider)
        if not endpoint:
            raise Exception(f"Unknown provider: {provider}")
        
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        # Build payload with streaming enabled
        if provider == 'cerebras':
            payload = {
                'model': model,
                'messages': messages,
                'temperature': temperature,
                'max_completion_tokens': max_tokens,
                'stream': True,
                **kwargs
            }
        else:
            payload = {
                'model': model,
                'messages': messages,
                'temperature': temperature,
                'max_tokens': max_tokens,
                'stream': True,
                **kwargs
            }
        
        masked_key = self._mask_key(api_key)
        logger.info(f"📤 {provider} streaming: model={model}, key={masked_key}")
        
        # Make streaming request
        response = requests.post(endpoint, headers=headers, json=payload, stream=True, timeout=60)
        
        if response.status_code != 200:
            raise Exception(f"HTTP {response.status_code}: {response.text[:200]}")
        
        # Parse SSE stream
        import json
        
        for line in response.iter_lines():
            if not line:
                continue
            
            line = line.decode('utf-8')
            
            # Skip empty lines and comments
            if not line.strip() or line.startswith(':'):
                continue
            
            # Parse SSE format: "data: {...}"
            if line.startswith('data: '):
                data_str = line[6:]  # Remove "data: " prefix
                
                # Check for stream end
                if data_str.strip() == '[DONE]':
                    break
                
                try:
                    data = json.loads(data_str)
                    
                    # Extract content from chunk
                    if 'choices' in data and len(data['choices']) > 0:
                        choice = data['choices'][0]
                        
                        # Handle different response formats
                        if 'delta' in choice:
                            delta = choice['delta']
                            if 'content' in delta and delta['content']:
                                yield delta['content']
                        elif 'text' in choice:
                            # Some providers use 'text' instead of 'delta'
                            if choice['text']:
                                yield choice['text']
                
                except json.JSONDecodeError:
                    # Skip malformed JSON
                    continue
    
    def _cohere_stream(
        self,
        api_key: str,
        model: str,
        messages: List[Dict[str, str]],
        temperature: float,
        max_tokens: int,
        **kwargs
    ):
        """
        Handle Cohere streaming (different format from standard providers).
        
        Cohere uses JSON lines format with event_type field:
        - event_type: "stream-start", "text-generation", "stream-end"
        - text: The generated text chunk
        """
        from .adapters import CohereAdapter
        import json
        
        adapter = CohereAdapter()
        endpoint = API_ENDPOINTS['cohere']
        
        # Build headers and payload
        headers = adapter.build_headers(api_key)
        payload = adapter.request_to_provider_format(
            messages,
            temperature=temperature,
            max_tokens=max_tokens,
            model=model,
            stream=True,
            **kwargs
        )
        
        masked_key = self._mask_key(api_key)
        logger.info(f"📤 cohere streaming: model={model}, key={masked_key}")
        
        # Make streaming request
        response = requests.post(endpoint, headers=headers, json=payload, stream=True, timeout=60)
        
        if response.status_code != 200:
            raise Exception(f"HTTP {response.status_code}: {response.text[:200]}")
        
        # Parse Cohere's JSON lines stream
        for line in response.iter_lines():
            if not line:
                continue
            
            try:
                chunk_data = json.loads(line.decode('utf-8'))
                
                # Use adapter to parse chunk
                text = adapter.parse_stream_chunk(chunk_data)
                if text:
                    yield text
            
            except json.JSONDecodeError:
                # Skip malformed JSON
                continue

    def embed(
        self,
        texts: List[str] | str,
        model: Optional[str] = None,
        input_type: Optional[str] = None,
        **kwargs
    ) -> EmbeddingResponse:
        """
        Generate embeddings for text(s) with automatic provider fallback.
        
        Fallback chain: NVIDIA (free) → Cohere (paid) → Mistral (paid)
        
        Args:
            texts: Single text string or list of texts to embed
            model: Specific model ID (e.g., "nvidia/nv-embed-v1")
                   If None, uses default model for each provider
            input_type: For retrieval models: "query" or "passage"
            **kwargs: Additional parameters
        
        Returns:
            EmbeddingResponse: List of embeddings with models_used tracking
        
        Example:
            >>> embeddings = jugglerr.embed(["Hello world", "Test text"])
            >>> print(len(embeddings))  # 2
            >>> print(embeddings.dimensions)  # 4096
            >>> print(embeddings.models_used)  # Tracking info
        """
        logger.info(f"🔢 Generating embeddings")
        
        # Track all attempts
        models_used = []
        attempt_num = 0
        
        # Try NVIDIA first (free)
        if self.nvidia_keys:
            attempt_num += 1
            start_time = time.time()
            
            try:
                from .embedding_adapter import EmbeddingAdapter
                
                api_key = self._select_best_key('nvidia', self.nvidia_keys)
                adapter = EmbeddingAdapter(api_key=api_key)
                
                nvidia_model = model or "nvidia/nv-embed-v1"
                logger.info(f"🎯 Trying NVIDIA embeddings: {nvidia_model}")
                
                embeddings = adapter.embed(
                    texts=texts,
                    model=nvidia_model,
                    input_type=input_type,
                    **kwargs
                )
                
                elapsed_ms = (time.time() - start_time) * 1000
                models_used.append(ModelAttempt(
                    provider="nvidia",
                    model=nvidia_model,
                    success=True,
                    attempt=attempt_num,
                    status_code=200,
                    elapsed_ms=elapsed_ms
                ))
                
                logger.info(f"✅ NVIDIA embeddings success: {len(embeddings)} embeddings")
                return EmbeddingResponse(embeddings, models_used)
                
            except Exception as e:
                elapsed_ms = (time.time() - start_time) * 1000
                models_used.append(ModelAttempt(
                    provider="nvidia",
                    model=model or "nvidia/nv-embed-v1",
                    success=False,
                    attempt=attempt_num,
                    error=str(e),
                    error_type=type(e).__name__,
                    elapsed_ms=elapsed_ms
                ))
                logger.warning(f"⚠️  NVIDIA embeddings failed: {e}")
        
        # Try Cohere (paid)
        if self.cohere_keys:
            attempt_num += 1
            start_time = time.time()
            
            try:
                from .cohere_adapters import CohereEmbeddingAdapter
                
                api_key = self._select_best_key('cohere', self.cohere_keys)
                adapter = CohereEmbeddingAdapter(api_key=api_key)
                
                cohere_model = model or "embed-v4.0"
                logger.info(f"🎯 Trying Cohere embeddings: {cohere_model}")
                
                embeddings = adapter.embed(
                    texts=texts,
                    model=cohere_model,
                    input_type=input_type,
                    **kwargs
                )
                
                elapsed_ms = (time.time() - start_time) * 1000
                models_used.append(ModelAttempt(
                    provider="cohere",
                    model=cohere_model,
                    success=True,
                    attempt=attempt_num,
                    status_code=200,
                    elapsed_ms=elapsed_ms
                ))
                
                logger.info(f"✅ Cohere embeddings success: {len(embeddings)} embeddings")
                return EmbeddingResponse(embeddings, models_used)
                
            except Exception as e:
                elapsed_ms = (time.time() - start_time) * 1000
                models_used.append(ModelAttempt(
                    provider="cohere",
                    model=model or "embed-v4.0",
                    success=False,
                    attempt=attempt_num,
                    error=str(e),
                    error_type=type(e).__name__,
                    elapsed_ms=elapsed_ms
                ))
                logger.warning(f"⚠️  Cohere embeddings failed: {e}")
        
        # Try Mistral (paid)
        if self.mistral_keys:
            attempt_num += 1
            start_time = time.time()
            
            try:
                from .mistral_adapters import MistralEmbeddingAdapter
                
                api_key = self._select_best_key('mistral', self.mistral_keys)
                adapter = MistralEmbeddingAdapter(api_key=api_key)
                
                mistral_model = model or "mistral-embed"
                logger.info(f"🎯 Trying Mistral embeddings: {mistral_model}")
                
                embeddings = adapter.embed(
                    texts=texts,
                    model=mistral_model,
                    **kwargs
                )
                
                elapsed_ms = (time.time() - start_time) * 1000
                models_used.append(ModelAttempt(
                    provider="mistral",
                    model=mistral_model,
                    success=True,
                    attempt=attempt_num,
                    status_code=200,
                    elapsed_ms=elapsed_ms
                ))
                
                logger.info(f"✅ Mistral embeddings success: {len(embeddings)} embeddings")
                return EmbeddingResponse(embeddings, models_used)
                
            except Exception as e:
                elapsed_ms = (time.time() - start_time) * 1000
                models_used.append(ModelAttempt(
                    provider="mistral",
                    model=model or "mistral-embed",
                    success=False,
                    attempt=attempt_num,
                    error=str(e),
                    error_type=type(e).__name__,
                    elapsed_ms=elapsed_ms
                ))
                logger.warning(f"⚠️  Mistral embeddings failed: {e}")
        
        # All providers failed
        error_msg = "All embedding providers exhausted. Tried: "
        tried = []
        if self.nvidia_keys:
            tried.append("NVIDIA")
        if self.cohere_keys:
            tried.append("Cohere")
        if self.mistral_keys:
            tried.append("Mistral")
        error_msg += ", ".join(tried) if tried else "none (no API keys configured)"
        
        logger.error(f"❌ {error_msg}")
        
        error = NoProvidersAvailableError(error_msg)
        error.models_used = models_used
        raise error
    
    def embed_query(
        self,
        query: str,
        model: Optional[str] = None,
        **kwargs
    ) -> List[float]:
        """
        Embed a search query (convenience method for retrieval).
        
        Args:
            query: Query text
            model: Model ID (default: nvidia/nv-embed-v1)
            **kwargs: Additional parameters
        
        Returns:
            Single embedding vector
        """
        embeddings = self.embed(
            texts=[query],
            model=model,
            input_type="query",
            **kwargs
        )
        return embeddings[0]
    
    def embed_documents(
        self,
        documents: List[str],
        model: Optional[str] = None,
        **kwargs
    ) -> List[List[float]]:
        """
        Embed documents/passages (convenience method for retrieval).
        
        Args:
            documents: List of document texts
            model: Model ID (default: nvidia/nv-embed-v1)
            **kwargs: Additional parameters
        
        Returns:
            List of embedding vectors
        """
        return self.embed(
            texts=documents,
            model=model,
            input_type="passage",
            **kwargs
        )

    def rerank(
        self,
        query: str,
        documents: List[str],
        top_k: Optional[int] = None,
        model: Optional[str] = None,
        **kwargs
    ) -> RerankResponse:
        """
        Rerank documents by relevance to query with automatic provider fallback.
        
        Tries providers in order: NVIDIA → Cohere
        
        Args:
            query: Search query
            documents: List of documents to rerank
            top_k: Number of top results to return (None = all)
            model: Specific model to use (overrides automatic selection)
            **kwargs: Additional provider-specific parameters
        
        Returns:
            RerankResponse: Reranked documents with models_used tracking (behaves like list)
        
        Raises:
            NoProvidersAvailableError: If all providers fail
        
        Example:
            >>> docs = ["Doc 1", "Doc 2", "Doc 3"]
            >>> top_docs = jugglerr.rerank("What is AI?", docs, top_k=2)
            >>> print(top_docs)  # Works like a list
            >>> print(top_docs.models_used)  # Access tracking info
        """
        logger.info("🔄 Reranking documents")
        logger.info(f"  Query: {query[:50]}...")
        logger.info(f"  Documents: {len(documents)}")
        
        # Track all attempts
        models_used = []
        attempt_num = 0
        
        # Try NVIDIA first (free)
        if self.nvidia_keys:
            attempt_num += 1
            start_time = time.time()
            
            try:
                from .rerank_adapter import RerankAdapter
                
                api_key = self._select_best_key('nvidia', self.nvidia_keys)
                adapter = RerankAdapter(api_key=api_key)
                
                nvidia_model = model or "nvidia/llama-3.2-nv-rerankqa-1b-v2"
                logger.info(f"🎯 Trying NVIDIA reranking: {nvidia_model}")
                
                results = adapter.rerank(
                    query=query,
                    documents=documents,
                    model=nvidia_model,
                    **kwargs
                )
                
                # Extract top-k documents and scores
                reranked = [r.text for r in results.results]
                scores = [r.score for r in results.results]
                if top_k:
                    reranked = reranked[:top_k]
                    scores = scores[:top_k]
                
                elapsed_ms = (time.time() - start_time) * 1000
                models_used.append(ModelAttempt(
                    provider="nvidia",
                    model=nvidia_model,
                    success=True,
                    attempt=attempt_num,
                    status_code=200,
                    elapsed_ms=elapsed_ms
                ))
                
                logger.info(f"✅ NVIDIA reranking success")
                return RerankResponse(reranked, models_used, scores)
                
            except Exception as e:
                elapsed_ms = (time.time() - start_time) * 1000
                models_used.append(ModelAttempt(
                    provider="nvidia",
                    model=model or "nvidia/llama-3.2-nv-rerankqa-1b-v2",
                    success=False,
                    attempt=attempt_num,
                    error=str(e),
                    error_type=type(e).__name__,
                    elapsed_ms=elapsed_ms
                ))
                logger.warning(f"⚠️  NVIDIA reranking failed: {e}")
        
        # Try Cohere (paid)
        if self.cohere_keys:
            attempt_num += 1
            start_time = time.time()
            
            try:
                from .cohere_adapters import CohereRerankAdapter
                
                api_key = self._select_best_key('cohere', self.cohere_keys)
                adapter = CohereRerankAdapter(api_key=api_key)
                
                cohere_model = model or "rerank-v3.5"
                logger.info(f"🎯 Trying Cohere reranking: {cohere_model}")
                
                results = adapter.rerank(
                    query=query,
                    documents=documents,
                    model=cohere_model,
                    top_n=top_k,
                    **kwargs
                )
                
                # Extract documents and scores
                reranked = [documents[r.index] for r in results.results]
                scores = [r.relevance_score for r in results.results]
                
                elapsed_ms = (time.time() - start_time) * 1000
                models_used.append(ModelAttempt(
                    provider="cohere",
                    model=cohere_model,
                    success=True,
                    attempt=attempt_num,
                    status_code=200,
                    elapsed_ms=elapsed_ms
                ))
                
                logger.info(f"✅ Cohere reranking success")
                return RerankResponse(reranked, models_used, scores)
                
            except Exception as e:
                elapsed_ms = (time.time() - start_time) * 1000
                models_used.append(ModelAttempt(
                    provider="cohere",
                    model=model or "rerank-v3.5",
                    success=False,
                    attempt=attempt_num,
                    error=str(e),
                    error_type=type(e).__name__,
                    elapsed_ms=elapsed_ms
                ))
                logger.warning(f"⚠️  Cohere reranking failed: {e}")
        
        # All providers failed
        error_msg = "All reranking providers exhausted. Tried: "
        tried = []
        if self.nvidia_keys:
            tried.append("NVIDIA")
        if self.cohere_keys:
            tried.append("Cohere")
        error_msg += ", ".join(tried) if tried else "none (no API keys configured)"
        
        logger.error(f"❌ {error_msg}")
        
        error = NoProvidersAvailableError(error_msg)
        error.models_used = models_used
        raise error
    
    def transcribe(
        self,
        file,
        model: Optional[str] = None,
        language: Optional[str] = None,
        **kwargs
    ) -> TranscriptionResponse:
        """
        Transcribe audio to text with automatic provider fallback.
        
        Currently only supports Groq (Whisper models).
        
        Args:
            file: Audio file path or file object
            model: Specific model to use (default: whisper-large-v3)
            language: Force specific language (e.g., "en", "es")
            **kwargs: Additional provider-specific parameters
        
        Returns:
            TranscriptionResponse: Transcribed text with models_used tracking (behaves like str)
        
        Raises:
            NoProvidersAvailableError: If all providers fail
        
        Example:
            >>> text = jugglerr.transcribe("audio.mp3")
            >>> print(text)  # Works like a string
            >>> print(text.models_used)  # Access tracking info
            >>> print(text.language)  # Detected language
        """
        logger.info("🎤 Transcribing audio")
        
        # Track all attempts
        models_used = []
        attempt_num = 0
        
        # Try Groq (free)
        if self.groq_keys:
            attempt_num += 1
            start_time = time.time()
            
            try:
                from .groq_adapters import GroqTranscriptionAdapter
                
                api_key = self._select_best_key('groq', self.groq_keys)
                adapter = GroqTranscriptionAdapter(api_key=api_key)
                
                groq_model = model or "whisper-large-v3"
                logger.info(f"🎯 Trying Groq transcription: {groq_model}")
                
                result = adapter.transcribe(
                    file=file,
                    model=groq_model,
                    language=language,
                    **kwargs
                )
                
                elapsed_ms = (time.time() - start_time) * 1000
                models_used.append(ModelAttempt(
                    provider="groq",
                    model=groq_model,
                    success=True,
                    attempt=attempt_num,
                    status_code=200,
                    elapsed_ms=elapsed_ms
                ))
                
                logger.info(f"✅ Groq transcription success")
                return TranscriptionResponse(
                    text=result.text,
                    models_used=models_used,
                    language=result.language,
                    duration=result.duration
                )
                
            except Exception as e:
                elapsed_ms = (time.time() - start_time) * 1000
                models_used.append(ModelAttempt(
                    provider="groq",
                    model=model or "whisper-large-v3",
                    success=False,
                    attempt=attempt_num,
                    error=str(e),
                    error_type=type(e).__name__,
                    elapsed_ms=elapsed_ms
                ))
                logger.warning(f"⚠️  Groq transcription failed: {e}")
        
        # All providers failed
        error_msg = "All transcription providers exhausted. Tried: "
        tried = []
        if self.groq_keys:
            tried.append("Groq")
        error_msg += ", ".join(tried) if tried else "none (no API keys configured)"
        
        logger.error(f"❌ {error_msg}")
        
        error = NoProvidersAvailableError(error_msg)
        error.models_used = models_used
        raise error
    
    def speak(
        self,
        text: str,
        voice: Optional[str] = None,
        model: Optional[str] = None,
        output_file: Optional[str] = None,
        **kwargs
    ) -> SpeechResponse:
        """
        Convert text to speech with automatic provider fallback.
        
        Currently only supports Groq (PlayAI TTS).
        
        Args:
            text: Text to convert to speech
            voice: Voice name (e.g., "Aria", "Clyde")
            model: Specific model to use (default: playai-tts)
            output_file: Optional file path to save audio
            **kwargs: Additional provider-specific parameters
        
        Returns:
            SpeechResponse: Object with audio_data, models_used, and write_to_file() method
        
        Raises:
            NoProvidersAvailableError: If all providers fail
        
        Example:
            >>> audio = jugglerr.speak("Hello world", voice="Aria")
            >>> audio.write_to_file("hello.mp3")
            >>> print(audio.models_used)  # Access tracking info
            
            >>> # Or save directly
            >>> jugglerr.speak("Hello", voice="Aria", output_file="hello.mp3")
        """
        logger.info("🔊 Generating speech")
        logger.info(f"  Text: {text[:50]}...")
        
        # Track all attempts
        models_used = []
        attempt_num = 0
        
        # Try Groq (free)
        if self.groq_keys:
            attempt_num += 1
            start_time = time.time()
            
            try:
                from .groq_adapters import GroqTTSAdapter
                
                api_key = self._select_best_key('groq', self.groq_keys)
                adapter = GroqTTSAdapter(api_key=api_key)
                
                groq_model = model or "playai-tts"
                logger.info(f"🎯 Trying Groq TTS: {groq_model}")
                
                result = adapter.speak(
                    text=text,
                    model=groq_model,
                    voice=voice or "Aria",
                    **kwargs
                )
                
                elapsed_ms = (time.time() - start_time) * 1000
                models_used.append(ModelAttempt(
                    provider="groq",
                    model=groq_model,
                    success=True,
                    attempt=attempt_num,
                    status_code=200,
                    elapsed_ms=elapsed_ms
                ))
                
                # Create response with tracking
                speech_response = SpeechResponse(result.audio_data, models_used)
                
                # Save to file if requested
                if output_file:
                    speech_response.write_to_file(output_file)
                    logger.info(f"💾 Saved to: {output_file}")
                
                logger.info(f"✅ Groq TTS success")
                return speech_response
                
            except Exception as e:
                elapsed_ms = (time.time() - start_time) * 1000
                models_used.append(ModelAttempt(
                    provider="groq",
                    model=model or "playai-tts",
                    success=False,
                    attempt=attempt_num,
                    error=str(e),
                    error_type=type(e).__name__,
                    elapsed_ms=elapsed_ms
                ))
                logger.warning(f"⚠️  Groq TTS failed: {e}")
        
        # All providers failed
        error_msg = "All TTS providers exhausted. Tried: "
        tried = []
        if self.groq_keys:
            tried.append("Groq")
        error_msg += ", ".join(tried) if tried else "none (no API keys configured)"
        
        logger.error(f"❌ {error_msg}")
        
        error = NoProvidersAvailableError(error_msg)
        error.models_used = models_used
        raise error
    

