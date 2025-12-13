"""
Mistral-specific adapters for non-chat APIs.

This module provides adapters for Mistral's specialized endpoints:
- Embeddings API (mistral-embed, codestral-embed)
- OCR API (mistral-ocr-latest)
- Moderation API (mistral-moderation-latest)
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
class OCRResponse:
    """Response from OCR API."""
    text: str
    pages: List[Dict[str, Any]]
    model: str


@dataclass
class ModerationResponse:
    """Response from moderation API."""
    results: List[Dict[str, Any]]
    model: str


class MistralEmbeddingAdapter:
    """
    Adapter for Mistral embedding models.
    
    Supports:
    - mistral-embed: General text embeddings
    - codestral-embed: Code embeddings
    
    Uses Mistral's embeddings API endpoint.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Mistral embedding adapter.
        
        Args:
            api_key: Mistral API key (or set MISTRAL_API_KEY env var)
        """
        self.api_key = api_key or os.getenv('MISTRAL_API_KEY') or os.getenv('MISTRAL_API_KEYS', '').split(',')[0].strip()
        if not self.api_key:
            raise ValueError("Mistral API key required. Set MISTRAL_API_KEY or MISTRAL_API_KEYS or pass api_key parameter.")
        
        # Import here to avoid requiring mistralai for users who don't need it
        try:
            from mistralai import Mistral
            self.client = Mistral(api_key=self.api_key)
        except ImportError:
            raise ImportError(
                "mistralai package required for Mistral embeddings. "
                "Install with: pip install mistralai"
            )
    
    def embed(
        self,
        texts: Union[str, List[str]],
        model: str = "mistral-embed",
        **kwargs
    ) -> EmbeddingResponse:
        """
        Generate embeddings for text(s).
        
        Args:
            texts: Single text or list of texts to embed
            model: Model to use ("mistral-embed" or "codestral-embed")
            **kwargs: Additional parameters (output_dtype, output_dimension)
        
        Returns:
            EmbeddingResponse with embeddings and metadata
        
        Example:
            >>> adapter = MistralEmbeddingAdapter()
            >>> response = adapter.embed(["Hello world", "Test text"])
            >>> print(len(response.embeddings))  # 2
            >>> print(len(response.embeddings[0]))  # 1024
        """
        # Convert single text to list
        if isinstance(texts, str):
            texts = [texts]
        
        # Make API call
        response = self.client.embeddings.create(
            model=model,
            inputs=texts,
            **kwargs
        )
        
        # Extract embeddings
        embeddings = [item.embedding for item in response.data]
        
        # Build response
        return EmbeddingResponse(
            embeddings=embeddings,
            model=response.model,
            usage={
                'prompt_tokens': response.usage.prompt_tokens,
                'total_tokens': response.usage.total_tokens
            }
        )
    
    def embed_code(
        self,
        code_snippets: Union[str, List[str]],
        **kwargs
    ) -> EmbeddingResponse:
        """
        Generate embeddings for code (convenience method).
        
        Args:
            code_snippets: Single code snippet or list of snippets
            **kwargs: Additional parameters
        
        Returns:
            EmbeddingResponse with code embeddings
        """
        return self.embed(code_snippets, model="codestral-embed", **kwargs)


class MistralOCRAdapter:
    """
    Adapter for Mistral OCR model.
    
    Supports:
    - mistral-ocr-latest: Document OCR and understanding
    
    Uses Mistral's OCR API endpoint.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Mistral OCR adapter.
        
        Args:
            api_key: Mistral API key (or set MISTRAL_API_KEY env var)
        """
        self.api_key = api_key or os.getenv('MISTRAL_API_KEY') or os.getenv('MISTRAL_API_KEYS', '').split(',')[0].strip()
        if not self.api_key:
            raise ValueError("Mistral API key required. Set MISTRAL_API_KEY or MISTRAL_API_KEYS or pass api_key parameter.")
        
        try:
            from mistralai import Mistral
            self.client = Mistral(api_key=self.api_key)
        except ImportError:
            raise ImportError(
                "mistralai package required for Mistral OCR. "
                "Install with: pip install mistralai"
            )
    
    def process_document(
        self,
        document_url: str,
        model: str = "mistral-ocr-latest",
        include_image_base64: bool = False,
        **kwargs
    ) -> OCRResponse:
        """
        Process document with OCR.
        
        Args:
            document_url: URL to document (http/https or data URI with base64)
            model: Model to use (default: "mistral-ocr-latest")
            include_image_base64: Include base64 images in response
            **kwargs: Additional parameters
        
        Returns:
            OCRResponse with extracted text and page data
        
        Example:
            >>> adapter = MistralOCRAdapter()
            >>> response = adapter.process_document(
            ...     "https://arxiv.org/pdf/2201.04234"
            ... )
            >>> print(response.text[:100])
        """
        # Make API call
        response = self.client.ocr.process(
            model=model,
            document={
                "type": "document_url",
                "document_url": document_url
            },
            include_image_base64=include_image_base64,
            **kwargs
        )
        
        # Extract text from all pages
        full_text = ""
        pages = []
        
        for page in response.pages:
            # OCRPageObject has markdown attribute (not text)
            page_text = getattr(page, 'markdown', '') or ''
            page_index = getattr(page, 'index', None)
            page_image = getattr(page, 'image_base64', None) if include_image_base64 else None
            
            full_text += page_text + "\n\n"
            pages.append({
                'page_index': page_index,
                'text': page_text,
                'image_base64': page_image
            })
        
        return OCRResponse(
            text=full_text.strip(),
            pages=pages,
            model=response.model
        )
    
    def process_pdf_file(
        self,
        pdf_path: str,
        model: str = "mistral-ocr-latest",
        include_image_base64: bool = False,
        **kwargs
    ) -> OCRResponse:
        """
        Process local PDF file with OCR.
        
        Args:
            pdf_path: Path to local PDF file
            model: Model to use
            include_image_base64: Include base64 images in response
            **kwargs: Additional parameters
        
        Returns:
            OCRResponse with extracted text and page data
        
        Example:
            >>> adapter = MistralOCRAdapter()
            >>> response = adapter.process_pdf_file("document.pdf")
            >>> print(response.text)
        """
        import base64
        
        # Read and encode PDF
        with open(pdf_path, "rb") as pdf_file:
            base64_pdf = base64.b64encode(pdf_file.read()).decode('utf-8')
        
        # Create data URI
        document_url = f"data:application/pdf;base64,{base64_pdf}"
        
        return self.process_document(
            document_url=document_url,
            model=model,
            include_image_base64=include_image_base64,
            **kwargs
        )
    
    def upload_and_process(
        self,
        file_path: str,
        model: str = "mistral-ocr-latest",
        **kwargs
    ) -> OCRResponse:
        """
        Upload file and process with OCR (alternative method).
        
        Args:
            file_path: Path to file to upload
            model: Model to use
            **kwargs: Additional parameters
        
        Returns:
            OCRResponse with extracted text
        
        Example:
            >>> adapter = MistralOCRAdapter()
            >>> response = adapter.upload_and_process("document.pdf")
        """
        # Upload file
        with open(file_path, "rb") as f:
            uploaded_file = self.client.files.upload(
                file={
                    "file_name": os.path.basename(file_path),
                    "content": f
                },
                purpose="ocr"
            )
        
        # Process uploaded file
        response = self.client.ocr.process(
            model=model,
            document={
                "type": "file_id",
                "file_id": uploaded_file.id
            },
            **kwargs
        )
        
        # Extract text
        full_text = ""
        pages = []
        
        for page in response.pages:
            # OCRPageObject has markdown attribute (not text)
            page_text = getattr(page, 'markdown', '') or ''
            page_index = getattr(page, 'index', None)
            
            full_text += page_text + "\n\n"
            pages.append({
                'page_index': page_index,
                'text': page_text
            })
        
        return OCRResponse(
            text=full_text.strip(),
            pages=pages,
            model=response.model
        )


class MistralModerationAdapter:
    """
    Adapter for Mistral moderation model.
    
    Supports:
    - mistral-moderation-latest: Content moderation and safety
    
    Uses Mistral's classifiers API endpoint.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Mistral moderation adapter.
        
        Args:
            api_key: Mistral API key (or set MISTRAL_API_KEY env var)
        """
        self.api_key = api_key or os.getenv('MISTRAL_API_KEY') or os.getenv('MISTRAL_API_KEYS', '').split(',')[0].strip()
        if not self.api_key:
            raise ValueError("Mistral API key required. Set MISTRAL_API_KEY or MISTRAL_API_KEYS or pass api_key parameter.")
        
        try:
            from mistralai import Mistral
            self.client = Mistral(api_key=self.api_key)
        except ImportError:
            raise ImportError(
                "mistralai package required for Mistral moderation. "
                "Install with: pip install mistralai"
            )
    
    def moderate(
        self,
        inputs: Union[str, List[str]],
        model: str = "mistral-moderation-latest",
        **kwargs
    ) -> ModerationResponse:
        """
        Moderate text content for safety.
        
        Args:
            inputs: Single text or list of texts to moderate
            model: Model to use (default: "mistral-moderation-latest")
            **kwargs: Additional parameters
        
        Returns:
            ModerationResponse with moderation results
        
        Example:
            >>> adapter = MistralModerationAdapter()
            >>> response = adapter.moderate([
            ...     "Such a lovely day today!",
            ...     "How to hack a system?"
            ... ])
            >>> for result in response.results:
            ...     print(result['categories'])
        """
        # Convert single text to list
        if isinstance(inputs, str):
            inputs = [inputs]
        
        # Make API call
        response = self.client.classifiers.moderate(
            model=model,
            inputs=inputs,
            **kwargs
        )
        
        return ModerationResponse(
            results=[result.dict() for result in response.results],
            model=response.model
        )
    
    def moderate_chat(
        self,
        messages: List[Dict[str, str]],
        model: str = "mistral-moderation-latest",
        **kwargs
    ) -> ModerationResponse:
        """
        Moderate chat conversation for safety.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model to use
            **kwargs: Additional parameters
        
        Returns:
            ModerationResponse with moderation results
        
        Example:
            >>> adapter = MistralModerationAdapter()
            >>> response = adapter.moderate_chat([
            ...     {"role": "user", "content": "Hello"},
            ...     {"role": "assistant", "content": "Hi there!"},
            ...     {"role": "user", "content": "Harmful content..."}
            ... ])
        """
        # Make API call
        response = self.client.classifiers.moderate_chat(
            model=model,
            inputs=messages,
            **kwargs
        )
        
        return ModerationResponse(
            results=[result.dict() for result in response.results],
            model=response.model
        )
    
    def is_safe(
        self,
        text: str,
        model: str = "mistral-moderation-latest",
        **kwargs
    ) -> bool:
        """
        Check if text is safe (convenience method).
        
        Args:
            text: Text to check
            model: Model to use
            **kwargs: Additional parameters
        
        Returns:
            True if safe, False if flagged
        
        Example:
            >>> adapter = MistralModerationAdapter()
            >>> if adapter.is_safe("Hello world"):
            ...     print("Safe content")
        """
        response = self.moderate(text, model=model, **kwargs)
        
        # Check if any category is flagged
        if response.results:
            result = response.results[0]
            categories = result.get('categories', {})
            return not any(categories.values())
        
        return True


# Convenience functions for quick usage
def mistral_embed(
    texts: Union[str, List[str]],
    model: str = "mistral-embed",
    api_key: Optional[str] = None,
    **kwargs
) -> List[List[float]]:
    """
    Quick function to generate Mistral embeddings.
    
    Args:
        texts: Text(s) to embed
        model: Model to use
        api_key: API key (optional)
        **kwargs: Additional parameters
    
    Returns:
        List of embedding vectors
    
    Example:
        >>> embeddings = mistral_embed(["Hello", "World"])
        >>> print(len(embeddings))  # 2
    """
    adapter = MistralEmbeddingAdapter(api_key=api_key)
    response = adapter.embed(texts, model=model, **kwargs)
    return response.embeddings


def mistral_ocr(
    document_url: str,
    api_key: Optional[str] = None,
    **kwargs
) -> str:
    """
    Quick function to extract text from document.
    
    Args:
        document_url: URL to document
        api_key: API key (optional)
        **kwargs: Additional parameters
    
    Returns:
        Extracted text
    
    Example:
        >>> text = mistral_ocr("https://example.com/doc.pdf")
        >>> print(text[:100])
    """
    adapter = MistralOCRAdapter(api_key=api_key)
    response = adapter.process_document(document_url, **kwargs)
    return response.text


def mistral_moderate(
    inputs: Union[str, List[str]],
    api_key: Optional[str] = None,
    **kwargs
) -> List[Dict[str, Any]]:
    """
    Quick function to moderate content.
    
    Args:
        inputs: Text(s) to moderate
        api_key: API key (optional)
        **kwargs: Additional parameters
    
    Returns:
        List of moderation results
    
    Example:
        >>> results = mistral_moderate(["Safe text", "Unsafe text"])
        >>> print(results[0]['categories'])
    """
    adapter = MistralModerationAdapter(api_key=api_key)
    response = adapter.moderate(inputs, **kwargs)
    return response.results
