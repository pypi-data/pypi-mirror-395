"""
Embedding adapter for NVIDIA NIM embedding models.
Uses standard API format compatible with OpenAI-style endpoints.
"""

from typing import List, Optional, Dict, Any
import requests


class EmbeddingAdapter:
    """
    Adapter for NVIDIA embedding models using standard API format.
    
    Supports:
    - Text embeddings (nv-embed-v1, bge-m3)
    - Code embeddings (nv-embedcode-7b-v1)
    - Retrieval embeddings (nemoretriever models with input_type)
    - Vision embeddings (nv-dinov2)
    - Protein embeddings (esm2-650m)
    """
    
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://integrate.api.nvidia.com/v1"
    ):
        """
        Initialize embedding adapter.
        
        Args:
            api_key: NVIDIA API key
            base_url: Base URL for NVIDIA API (default: integrate.api.nvidia.com)
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    
    def embed(
        self,
        texts: List[str] | str,
        model: str = "nvidia/nv-embed-v1",
        input_type: Optional[str] = None,
        truncate: Optional[str] = None,
        encoding_format: str = "float",
        **kwargs
    ) -> List[List[float]]:
        """
        Generate embeddings for text(s).
        
        Args:
            texts: Single text string or list of texts to embed
            model: Model ID (e.g., "nvidia/nv-embed-v1")
            input_type: For retrieval models: "query" or "passage"
            truncate: Truncation strategy: "NONE", "START", "END"
            encoding_format: "float" or "base64"
            **kwargs: Additional model-specific parameters
        
        Returns:
            List of embedding vectors (list of floats)
        
        Example:
            >>> adapter = EmbeddingAdapter(api_key="...")
            >>> vectors = adapter.embed(["Hello world", "Test text"])
            >>> print(len(vectors))  # 2
            >>> print(len(vectors[0]))  # 1024 (dimension depends on model)
        """
        # Normalize input to list
        if isinstance(texts, str):
            texts = [texts]
        
        # Build request payload
        payload = {
            "model": model,
            "input": texts,
            "encoding_format": encoding_format,
        }
        
        # Add optional parameters
        if input_type:
            payload["input_type"] = input_type
        if truncate:
            payload["truncate"] = truncate
        
        # Add any extra parameters
        payload.update(kwargs)
        
        # Make request
        response = requests.post(
            f"{self.base_url}/embeddings",
            headers=self.headers,
            json=payload,
            timeout=60
        )
        
        # Check for errors
        if response.status_code != 200:
            error_detail = response.json() if response.text else {}
            raise Exception(f"HTTP {response.status_code}: {error_detail}")
        
        # Parse response
        data = response.json()
        
        # Extract embeddings
        embeddings = [item['embedding'] for item in data['data']]
        
        return embeddings
    
    def embed_query(
        self,
        query: str,
        model: str = "nvidia/nv-embed-v1",
        **kwargs
    ) -> List[float]:
        """
        Embed a search query (convenience method for retrieval models).
        
        Args:
            query: Query text
            model: Model ID
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
        model: str = "nvidia/nv-embed-v1",
        **kwargs
    ) -> List[List[float]]:
        """
        Embed documents/passages (convenience method for retrieval models).
        
        Args:
            documents: List of document texts
            model: Model ID
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


# Model-specific helpers

def get_embedding_dimension(model: str) -> int:
    """Get embedding dimension for a model."""
    dimensions = {
        "nvidia/nv-embed-v1": 1024,
        "nvidia/nv-embedcode-7b-v1": 1024,
        "nvidia/llama-3_2-nemoretriever-300m-embed-v1": 2048,
        "nvidia/llama-3_2-nemoretriever-1b-vlm-embed-v1": 1024,
        "nvidia/nv-dinov2": 1024,
        "meta/esm2-650m": 1280,
        "baai/bge-m3": 1024,
    }
    return dimensions.get(model, 1024)


def get_max_sequence_length(model: str) -> int:
    """Get maximum sequence length for a model."""
    max_lengths = {
        "nvidia/nv-embed-v1": 8192,
        "nvidia/nv-embedcode-7b-v1": 8192,
        "nvidia/llama-3_2-nemoretriever-300m-embed-v1": 8192,
        "nvidia/llama-3_2-nemoretriever-1b-vlm-embed-v1": 8192,
        "nvidia/nv-dinov2": 8192,
        "meta/esm2-650m": 1024,  # Protein sequences: 1-1024
        "baai/bge-m3": 8192,
    }
    return max_lengths.get(model, 8192)
