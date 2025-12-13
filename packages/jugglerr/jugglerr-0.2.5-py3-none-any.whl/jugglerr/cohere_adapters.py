"""
Cohere-specific adapters for non-chat APIs.

This module provides adapters for Cohere's specialized endpoints:
- Embedding API (embed-v4.0, embed-v3.0 variants)
- Rerank API (rerank-v3.5, rerank-v3.0 variants)
"""

import os
from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass


@dataclass
class EmbeddingResponse:
    """Response from embedding API."""
    embeddings: List[List[float]]
    model: str
    usage: Dict[str, int]


@dataclass
class RerankResult:
    """Single rerank result."""
    index: int
    relevance_score: float
    document: Optional[str] = None


@dataclass
class RerankResponse:
    """Response from rerank API."""
    results: List[RerankResult]
    model: str


class CohereEmbeddingAdapter:
    """
    Adapter for Cohere embedding models.
    
    Supports:
    - embed-v4.0: Latest model (128K context, text+images)
    - embed-english-v3.0: English text embeddings
    - embed-english-light-v3.0: Faster English embeddings
    - embed-multilingual-v3.0: 100+ languages
    - embed-multilingual-light-v3.0: Faster multilingual
    
    Uses Cohere's v2/embed API endpoint.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Cohere embedding adapter.
        
        Args:
            api_key: Cohere API key (or set COHERE_API_KEY env var)
        """
        self.api_key = api_key or os.getenv('COHERE_API_KEY') or os.getenv('COHERE_API_KEYS', '').split(',')[0].strip()
        if not self.api_key:
            raise ValueError("Cohere API key required. Set COHERE_API_KEY or COHERE_API_KEYS or pass api_key parameter.")
        
        # Import here to avoid requiring cohere for users who don't need it
        try:
            from cohere import ClientV2
            self.client = ClientV2(api_key=self.api_key)
        except ImportError:
            raise ImportError(
                "cohere package required for Cohere embeddings. "
                "Install with: pip install cohere"
            )
    
    def embed(
        self,
        texts: Union[str, List[str]],
        model: str = "embed-english-v3.0",
        input_type: str = "search_document",
        embedding_types: Optional[List[str]] = None,
        **kwargs
    ) -> EmbeddingResponse:
        """
        Generate embeddings for text(s).
        
        Args:
            texts: Single text or list of texts to embed (max 96)
            model: Model to use (embed-v4.0, embed-english-v3.0, etc.)
            input_type: Type of input (search_document, search_query, classification, clustering)
            embedding_types: Types of embeddings (float, int8, uint8, binary, ubinary)
            **kwargs: Additional parameters (truncate, etc.)
        
        Returns:
            EmbeddingResponse with embeddings and metadata
        
        Example:
            >>> adapter = CohereEmbeddingAdapter()
            >>> response = adapter.embed(
            ...     ["Hello world", "Test text"],
            ...     model="embed-english-v3.0",
            ...     input_type="search_document"
            ... )
            >>> print(len(response.embeddings))  # 2
            >>> print(len(response.embeddings[0]))  # 1024
        """
        # Convert single text to list
        if isinstance(texts, str):
            texts = [texts]
        
        # Make API call
        response = self.client.embed(
            model=model,
            texts=texts,
            input_type=input_type,
            embedding_types=embedding_types or ["float"],
            **kwargs
        )
        
        # Extract embeddings (default to float type)
        embeddings = response.embeddings.float if hasattr(response.embeddings, 'float') else []
        
        # Build response
        return EmbeddingResponse(
            embeddings=embeddings,
            model=response.response_type or model,
            usage={
                'total_tokens': len(texts)  # Cohere doesn't provide detailed token counts in v2
            }
        )
    
    def embed_for_search(
        self,
        documents: List[str],
        model: str = "embed-english-v3.0",
        **kwargs
    ) -> EmbeddingResponse:
        """
        Generate embeddings for documents (for indexing).
        
        Args:
            documents: List of documents to embed
            model: Model to use
            **kwargs: Additional parameters
        
        Returns:
            EmbeddingResponse with document embeddings
        """
        return self.embed(documents, model=model, input_type="search_document", **kwargs)
    
    def embed_query(
        self,
        query: str,
        model: str = "embed-english-v3.0",
        **kwargs
    ) -> List[float]:
        """
        Generate embedding for a search query.
        
        Args:
            query: Search query text
            model: Model to use
            **kwargs: Additional parameters
        
        Returns:
            Single embedding vector
        """
        response = self.embed([query], model=model, input_type="search_query", **kwargs)
        return response.embeddings[0]


class CohereRerankAdapter:
    """
    Adapter for Cohere rerank models.
    
    Supports:
    - rerank-v3.5: Latest model (English + multilingual)
    - rerank-english-v3.0: English only
    - rerank-multilingual-v3.0: 100+ languages
    
    Uses Cohere's v2/rerank API endpoint.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Cohere rerank adapter.
        
        Args:
            api_key: Cohere API key (or set COHERE_API_KEY env var)
        """
        self.api_key = api_key or os.getenv('COHERE_API_KEY') or os.getenv('COHERE_API_KEYS', '').split(',')[0].strip()
        if not self.api_key:
            raise ValueError("Cohere API key required. Set COHERE_API_KEY or COHERE_API_KEYS or pass api_key parameter.")
        
        try:
            from cohere import ClientV2
            self.client = ClientV2(api_key=self.api_key)
        except ImportError:
            raise ImportError(
                "cohere package required for Cohere rerank. "
                "Install with: pip install cohere"
            )
    
    def rerank(
        self,
        query: str,
        documents: List[str],
        model: str = "rerank-v3.5",
        top_n: Optional[int] = None,
        **kwargs
    ) -> RerankResponse:
        """
        Rerank documents by relevance to query.
        
        Args:
            query: Search query
            documents: List of documents to rerank (max 1000 recommended)
            model: Model to use (rerank-v3.5, rerank-english-v3.0, rerank-multilingual-v3.0)
            top_n: Return only top N results (optional)
            **kwargs: Additional parameters (max_tokens_per_doc, etc.)
        
        Returns:
            RerankResponse with ranked results
        
        Example:
            >>> adapter = CohereRerankAdapter()
            >>> response = adapter.rerank(
            ...     query="What is Python?",
            ...     documents=[
            ...         "Python is a programming language",
            ...         "Snakes are reptiles",
            ...         "Java is also a programming language"
            ...     ],
            ...     model="rerank-v3.5",
            ...     top_n=2
            ... )
            >>> for result in response.results:
            ...     print(f"Index {result.index}: {result.relevance_score:.3f}")
        """
        # Make API call
        response = self.client.rerank(
            model=model,
            query=query,
            documents=documents,
            top_n=top_n,
            **kwargs
        )
        
        # Build results
        results = []
        for result in response.results:
            results.append(RerankResult(
                index=result.index,
                relevance_score=result.relevance_score,
                document=documents[result.index] if result.index < len(documents) else None
            ))
        
        return RerankResponse(
            results=results,
            model=model
        )
    
    def get_top_documents(
        self,
        query: str,
        documents: List[str],
        top_n: int = 5,
        model: str = "rerank-v3.5",
        **kwargs
    ) -> List[str]:
        """
        Get top N most relevant documents (convenience method).
        
        Args:
            query: Search query
            documents: List of documents
            top_n: Number of top documents to return
            model: Model to use
            **kwargs: Additional parameters
        
        Returns:
            List of top N documents
        """
        response = self.rerank(query, documents, model=model, top_n=top_n, **kwargs)
        return [result.document for result in response.results if result.document]


# Convenience functions
def cohere_embed(
    texts: Union[str, List[str]],
    model: str = "embed-english-v3.0",
    input_type: str = "search_document",
    api_key: Optional[str] = None,
    **kwargs
) -> List[List[float]]:
    """
    Quick function to generate Cohere embeddings.
    
    Args:
        texts: Text(s) to embed
        model: Model to use
        input_type: Type of input
        api_key: API key (optional)
        **kwargs: Additional parameters
    
    Returns:
        List of embedding vectors
    
    Example:
        >>> embeddings = cohere_embed(["Hello", "World"])
        >>> print(len(embeddings))  # 2
    """
    adapter = CohereEmbeddingAdapter(api_key=api_key)
    response = adapter.embed(texts, model=model, input_type=input_type, **kwargs)
    return response.embeddings


def cohere_rerank(
    query: str,
    documents: List[str],
    model: str = "rerank-v3.5",
    top_n: Optional[int] = None,
    api_key: Optional[str] = None,
    **kwargs
) -> List[Dict[str, Any]]:
    """
    Quick function to rerank documents.
    
    Args:
        query: Search query
        documents: List of documents
        model: Model to use
        top_n: Return only top N results
        api_key: API key (optional)
        **kwargs: Additional parameters
    
    Returns:
        List of result dicts with index and relevance_score
    
    Example:
        >>> results = cohere_rerank(
        ...     "Python programming",
        ...     ["Python is a language", "Snakes are reptiles"],
        ...     top_n=1
        ... )
        >>> print(results[0]['relevance_score'])
    """
    adapter = CohereRerankAdapter(api_key=api_key)
    response = adapter.rerank(query, documents, model=model, top_n=top_n, **kwargs)
    return [{'index': r.index, 'relevance_score': r.relevance_score, 'document': r.document} 
            for r in response.results]
