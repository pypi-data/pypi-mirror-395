"""
NVIDIA Reranking Adapter

Implementation of NVIDIA NeMo Retriever reranking model for RAG pipelines.
Based on Perplexity AI research (December 5, 2025).

Model: nvidia/llama-3.2-nv-rerankqa-1b-v2
Purpose: Multilingual text reranking for improved RAG accuracy
Impact: ~24% improvement in recall@5 (0.5699 → 0.7070)
"""

import os
import requests
from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass


@dataclass
class RerankResult:
    """Single reranking result."""
    index: int
    text: str
    score: float
    relevance_score: float


@dataclass
class RerankResponse:
    """Complete reranking response."""
    results: List[RerankResult]
    model: str
    query: str


class RerankAdapter:
    """
    Adapter for NVIDIA reranking models.
    
    CRITICAL: Reranking uses a different base URL than chat models!
    - Chat/Embeddings: https://integrate.api.nvidia.com/v1/
    - Reranking: https://ai.api.nvidia.com/v1/
    
    Example:
        >>> reranker = RerankAdapter(api_key="nvapi-...")
        >>> results = reranker.rerank(
        ...     query="What is machine learning?",
        ...     documents=["Doc 1", "Doc 2", "Doc 3"]
        ... )
        >>> print(results.results[0].text)  # Best match
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "nvidia/llama-3.2-nv-rerankqa-1b-v2",
        base_url: str = "https://ai.api.nvidia.com/v1"
    ):
        """
        Initialize reranking adapter.
        
        Args:
            api_key: NVIDIA API key (nvapi-...)
            model: Reranking model ID
            base_url: Base URL for reranking API (default: ai.api.nvidia.com)
        """
        self.api_key = api_key or os.getenv("NVIDIA_API_KEY") or os.getenv("NVIDIA_API_KEYS", "").split(",")[0]
        self.model = model
        self.base_url = base_url.rstrip('/')
        
        if not self.api_key:
            raise ValueError("NVIDIA API key required. Set NVIDIA_API_KEY environment variable.")
        
        # Build endpoint URL
        # Pattern: /v1/retrieval/nvidia/llama-3_2-nv-rerankqa-1b-v2/reranking
        # Note: Use underscores in model path, not slashes
        model_path = model.replace('/', '/').replace('.', '_')
        self.endpoint = f"{self.base_url}/retrieval/{model_path}/reranking"
    
    def rerank(
        self,
        query: str,
        documents: List[Union[str, Dict[str, str]]],
        top_n: Optional[int] = None,
        return_documents: bool = True,
        **kwargs
    ) -> RerankResponse:
        """
        Rerank documents based on relevance to query.
        
        Args:
            query: Search query
            documents: List of documents (strings or dicts with 'text' key)
            top_n: Number of top results to return (default: all)
            return_documents: Whether to return document text
            **kwargs: Additional parameters
        
        Returns:
            RerankResponse with ranked results
        
        Example:
            >>> reranker = RerankAdapter(api_key="nvapi-...")
            >>> results = reranker.rerank(
            ...     query="What is machine learning?",
            ...     documents=[
            ...         "Machine learning is a subset of AI...",
            ...         "Python is a programming language...",
            ...         "Deep learning uses neural networks..."
            ...     ],
            ...     top_n=2
            ... )
            >>> for result in results.results:
            ...     print(f"Score: {result.score:.3f} - {result.text[:50]}")
        """
        # Normalize documents to list of dicts
        passages = []
        for doc in documents:
            if isinstance(doc, str):
                passages.append({"text": doc})
            elif isinstance(doc, dict) and "text" in doc:
                passages.append(doc)
            else:
                raise ValueError(f"Document must be string or dict with 'text' key: {doc}")
        
        # Build request
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        payload = {
            "model": self.model,
            "query": {"text": query},  # Query must be an object with 'text' field
            "passages": passages
        }
        
        # Add optional parameters
        if top_n is not None:
            payload["top_n"] = top_n
        
        # Make request
        response = requests.post(
            self.endpoint,
            headers=headers,
            json=payload,
            timeout=kwargs.get('timeout', 30)
        )
        
        if response.status_code != 200:
            raise Exception(f"Reranking failed: HTTP {response.status_code}: {response.text}")
        
        data = response.json()
        
        # Parse response
        results = []
        for item in data.get('rankings', []):
            results.append(RerankResult(
                index=item.get('index', 0),
                text=passages[item.get('index', 0)]['text'] if return_documents else "",
                score=item.get('logit', 0.0),
                relevance_score=item.get('logit', 0.0)
            ))
        
        return RerankResponse(
            results=results,
            model=self.model,
            query=query
        )
    
    def rerank_with_scores(
        self,
        query: str,
        documents: List[str],
        top_n: Optional[int] = None
    ) -> List[tuple[str, float]]:
        """
        Rerank documents and return (document, score) tuples.
        
        Args:
            query: Search query
            documents: List of document strings
            top_n: Number of top results to return
        
        Returns:
            List of (document, score) tuples, sorted by relevance
        
        Example:
            >>> reranker = RerankAdapter(api_key="nvapi-...")
            >>> results = reranker.rerank_with_scores(
            ...     query="What is AI?",
            ...     documents=["Doc 1", "Doc 2", "Doc 3"],
            ...     top_n=2
            ... )
            >>> for doc, score in results:
            ...     print(f"{score:.3f}: {doc[:50]}")
        """
        response = self.rerank(query, documents, top_n=top_n)
        return [(result.text, result.score) for result in response.results]
    
    def rerank_indices(
        self,
        query: str,
        documents: List[str],
        top_n: Optional[int] = None
    ) -> List[int]:
        """
        Rerank documents and return indices of top results.
        
        Useful when you want to reorder an existing list without copying data.
        
        Args:
            query: Search query
            documents: List of document strings
            top_n: Number of top results to return
        
        Returns:
            List of indices, sorted by relevance
        
        Example:
            >>> reranker = RerankAdapter(api_key="nvapi-...")
            >>> docs = ["Doc 1", "Doc 2", "Doc 3"]
            >>> indices = reranker.rerank_indices("query", docs, top_n=2)
            >>> top_docs = [docs[i] for i in indices]
        """
        response = self.rerank(query, documents, top_n=top_n, return_documents=False)
        return [result.index for result in response.results]


# Convenience function
def rerank(
    query: str,
    documents: List[str],
    api_key: Optional[str] = None,
    top_n: Optional[int] = None,
    model: str = "nvidia/llama-3.2-nv-rerankqa-1b-v2"
) -> List[str]:
    """
    Quick reranking function.
    
    Args:
        query: Search query
        documents: List of documents
        api_key: NVIDIA API key (optional, uses env var if not provided)
        top_n: Number of top results
        model: Reranking model ID
    
    Returns:
        List of reranked documents
    
    Example:
        >>> from jugglerr import rerank
        >>> docs = ["Doc 1", "Doc 2", "Doc 3"]
        >>> ranked = rerank("query", docs, top_n=2)
        >>> print(ranked[0])  # Best match
    """
    adapter = RerankAdapter(api_key=api_key, model=model)
    response = adapter.rerank(query, documents, top_n=top_n)
    return [result.text for result in response.results]


# Export
__all__ = [
    'RerankAdapter',
    'RerankResponse',
    'RerankResult',
    'rerank'
]
