"""
Task-specific adapters for non-chat model types.

Supports:
- Embeddings
- Vision/Multimodal
- Text-to-Speech (TTS)
- Reranking
- Translation
- Safety/Moderation
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class EmbeddingResponse:
    """Standardized embedding response."""
    embeddings: List[List[float]]
    model: str
    usage: Dict[str, int]


@dataclass
class VisionResponse:
    """Standardized vision/multimodal response."""
    content: str
    model: str
    usage: Dict[str, int]


@dataclass
class TTSResponse:
    """Standardized TTS response."""
    audio_url: Optional[str]
    audio_data: Optional[bytes]
    model: str


@dataclass
class RerankResponse:
    """Standardized rerank response."""
    results: List[Dict[str, Any]]
    model: str


class EmbeddingAdapter:
    """Adapter for embedding models."""
    
    def request_to_provider_format(self, texts: List[str], **kwargs) -> Dict:
        """Convert texts to embedding request format."""
        return {
            "input": texts,
            "model": kwargs.get('model'),
            "encoding_format": kwargs.get('encoding_format', 'float')
        }
    
    def response_from_provider_format(self, response: Dict) -> EmbeddingResponse:
        """Convert provider response to standard format."""
        embeddings = [item['embedding'] for item in response.get('data', [])]
        return EmbeddingResponse(
            embeddings=embeddings,
            model=response.get('model', ''),
            usage=response.get('usage', {})
        )


class VisionAdapter:
    """Adapter for vision/multimodal models."""
    
    def request_to_provider_format(
        self,
        messages: List[Dict],
        images: Optional[List[str]] = None,
        **kwargs
    ) -> Dict:
        """Convert messages + images to vision request format."""
        # For vision models, images can be URLs or base64
        formatted_messages = []
        
        for msg in messages:
            content = msg.get('content', '')
            role = msg.get('role', 'user')
            
            # If images provided, add them to user messages
            if role == 'user' and images:
                content_parts = [{"type": "text", "text": content}]
                for img in images:
                    if img.startswith('http'):
                        content_parts.append({"type": "image_url", "image_url": {"url": img}})
                    else:
                        # Assume base64
                        content_parts.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img}"}})
                
                formatted_messages.append({
                    "role": role,
                    "content": content_parts
                })
            else:
                formatted_messages.append(msg)
        
        return {
            "model": kwargs.get('model'),
            "messages": formatted_messages,
            "max_tokens": kwargs.get('max_tokens', 1024),
            "temperature": kwargs.get('temperature', 0.7)
        }
    
    def response_from_provider_format(self, response: Dict) -> VisionResponse:
        """Convert provider response to standard format."""
        content = response['choices'][0]['message']['content']
        return VisionResponse(
            content=content,
            model=response.get('model', ''),
            usage=response.get('usage', {})
        )


class TTSAdapter:
    """Adapter for Text-to-Speech models."""
    
    def request_to_provider_format(self, text: str, **kwargs) -> Dict:
        """Convert text to TTS request format."""
        return {
            "model": kwargs.get('model'),
            "input": text,
            "voice": kwargs.get('voice', 'alloy'),
            "response_format": kwargs.get('response_format', 'mp3'),
            "speed": kwargs.get('speed', 1.0)
        }
    
    def response_from_provider_format(self, response: Any) -> TTSResponse:
        """Convert provider response to standard format."""
        # TTS typically returns audio data directly
        if isinstance(response, bytes):
            return TTSResponse(
                audio_url=None,
                audio_data=response,
                model=''
            )
        elif isinstance(response, dict) and 'audio_url' in response:
            return TTSResponse(
                audio_url=response['audio_url'],
                audio_data=None,
                model=response.get('model', '')
            )
        else:
            raise ValueError("Unknown TTS response format")


class RerankAdapter:
    """Adapter for reranking models."""
    
    def request_to_provider_format(
        self,
        query: str,
        documents: List[str],
        **kwargs
    ) -> Dict:
        """Convert query + documents to rerank request format."""
        return {
            "model": kwargs.get('model'),
            "query": query,
            "documents": documents,
            "top_n": kwargs.get('top_n', len(documents)),
            "return_documents": kwargs.get('return_documents', True)
        }
    
    def response_from_provider_format(self, response: Dict) -> RerankResponse:
        """Convert provider response to standard format."""
        return RerankResponse(
            results=response.get('results', []),
            model=response.get('model', '')
        )


class TranslationAdapter:
    """Adapter for translation models."""
    
    def request_to_provider_format(
        self,
        text: str,
        source_lang: str,
        target_lang: str,
        **kwargs
    ) -> Dict:
        """Convert text + languages to translation request format."""
        # Format as chat message for instruct models
        prompt = f"Translate the following text from {source_lang} to {target_lang}:\n\n{text}"
        
        return {
            "model": kwargs.get('model'),
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": kwargs.get('max_tokens', 2048),
            "temperature": kwargs.get('temperature', 0.3)  # Lower temp for translation
        }
    
    def response_from_provider_format(self, response: Dict) -> str:
        """Convert provider response to translated text."""
        return response['choices'][0]['message']['content']


class SafetyAdapter:
    """Adapter for safety/moderation models."""
    
    def request_to_provider_format(self, text: str, **kwargs) -> Dict:
        """Convert text to safety check request format."""
        return {
            "model": kwargs.get('model'),
            "messages": [
                {"role": "user", "content": text}
            ],
            "max_tokens": kwargs.get('max_tokens', 512),
            "temperature": 0.0  # Deterministic for safety checks
        }
    
    def response_from_provider_format(self, response: Dict) -> Dict[str, Any]:
        """Convert provider response to safety assessment."""
        content = response['choices'][0]['message']['content']
        
        # Parse safety response (model-specific format)
        # This is a simplified version - actual implementation depends on model
        return {
            "safe": "safe" in content.lower(),
            "categories": [],  # Would parse from response
            "scores": {},  # Would parse from response
            "raw_response": content
        }


# Task type detection
TASK_TYPES = {
    'embedding': [
        'embed', 'embedding', 'nemoretriever', 'bge-m3'
    ],
    'vision': [
        'vision', 'multimodal', 'vila', 'paligemma', 'phi-4-multimodal'
    ],
    'tts': [
        'tts', 'magpie', 'speech'
    ],
    'rerank': [
        'rerank'
    ],
    'translation': [
        'translate', 'riva-translate'
    ],
    'safety': [
        'guard', 'safety', 'shield', 'moderation'
    ]
}


def detect_task_type(model_id: str) -> Optional[str]:
    """Detect task type from model ID."""
    model_lower = model_id.lower()
    
    for task_type, keywords in TASK_TYPES.items():
        if any(keyword in model_lower for keyword in keywords):
            return task_type
    
    return None  # Default to chat/completion


def get_task_adapter(task_type: str):
    """Get appropriate adapter for task type."""
    adapters = {
        'embedding': EmbeddingAdapter(),
        'vision': VisionAdapter(),
        'tts': TTSAdapter(),
        'rerank': RerankAdapter(),
        'translation': TranslationAdapter(),
        'safety': SafetyAdapter()
    }
    
    return adapters.get(task_type)
