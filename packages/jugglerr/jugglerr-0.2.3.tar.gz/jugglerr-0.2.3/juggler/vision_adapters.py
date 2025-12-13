"""
NVIDIA Vision Language Models (VLM) Adapters

Implementation of NVIDIA vision models using Vision Language Models (VLMs).
Based on Perplexity's guidance (Dec 4, 2025) that CV models (ocdrnet, retail-object-detection)
are TAO Toolkit models for self-hosted deployment, not cloud APIs.

VLMs use the standard chat completions format and are available as managed cloud APIs.
"""
import os
import base64
import requests
from typing import Optional, Dict, Any, Union, List
from pathlib import Path


class VisionAdapter:
    """
    Base adapter for NVIDIA vision models with asset upload support.
    
    Workflow:
    1. Create asset → get UUID and pre-signed S3 URL
    2. Upload image to S3 URL
    3. Use UUID with vision model
    """
    
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://ai.api.nvidia.com"):
        """
        Initialize vision adapter.
        
        Args:
            api_key: NVIDIA API key (nvapi-...)
            base_url: Base URL for NVIDIA API
        """
        self.api_key = api_key or os.getenv("NVIDIA_API_KEY") or os.getenv("NVIDIA_API_KEYS", "").split(",")[0]
        self.base_url = base_url
        self.assets_url = "https://api.nvcf.nvidia.com/v2/nvcf/assets"
        
        if not self.api_key:
            raise ValueError("NVIDIA API key required. Set NVIDIA_API_KEY environment variable.")
    
    def _create_asset(self, content_type: str = "image/jpeg", description: str = "Vision model input") -> tuple:
        """
        Step 1: Create asset and get pre-signed upload URL.
        
        Args:
            content_type: MIME type (image/jpeg, image/png)
            description: Asset description
            
        Returns:
            tuple: (asset_id, upload_url)
        """
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        payload = {
            'contentType': content_type,
            'description': description
        }
        
        response = requests.post(self.assets_url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        return data['assetId'], data['uploadUrl']
    
    def _upload_to_s3(self, upload_url: str, image_data: bytes, content_type: str, description: str) -> None:
        """
        Step 2: Upload image to S3 pre-signed URL.
        
        CRITICAL: Headers must match the values from asset creation!
        
        Args:
            upload_url: Pre-signed S3 URL from _create_asset
            image_data: Binary image data
            content_type: Must match contentType from _create_asset
            description: Must match description from _create_asset
        """
        # Headers MUST match the asset creation payload
        s3_headers = {
            'content-type': content_type,
            'x-amz-meta-nvcf-asset-description': description
        }
        
        response = requests.put(upload_url, data=image_data, headers=s3_headers, timeout=300)
        response.raise_for_status()
    
    def upload_image(self, image_path: Union[str, Path], content_type: Optional[str] = None) -> str:
        """
        Upload image and get asset ID.
        
        Args:
            image_path: Path to image file
            content_type: MIME type (auto-detected if None)
            
        Returns:
            str: Asset ID (UUID) to use with vision models
        """
        image_path = Path(image_path)
        
        # Auto-detect content type
        if content_type is None:
            ext = image_path.suffix.lower()
            content_type = {
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.png': 'image/png',
                '.gif': 'image/gif',
                '.bmp': 'image/bmp'
            }.get(ext, 'image/jpeg')
        
        # Read image
        with open(image_path, 'rb') as f:
            image_data = f.read()
        
        return self.upload_image_bytes(image_data, content_type)
    
    def upload_image_bytes(self, image_data: bytes, content_type: str = "image/jpeg") -> str:
        """
        Upload image bytes and get asset ID.
        
        Args:
            image_data: Binary image data
            content_type: MIME type
            
        Returns:
            str: Asset ID (UUID) to use with vision models
        """
        description = f"Vision model input ({len(image_data)} bytes)"
        
        # Step 1: Create asset
        asset_id, upload_url = self._create_asset(content_type, description)
        
        # Step 2: Upload to S3
        self._upload_to_s3(upload_url, image_data, content_type, description)
        
        return asset_id


class VLMVisionAdapter(VisionAdapter):
    """
    Vision Language Model adapter for vision tasks.
    
    Uses VLMs (like Llama 4, Phi-3.5-Vision) with chat completions format
    instead of specialized CV models. More versatile and actually available
    as cloud APIs.
    
    Example:
        >>> vlm = VLMVisionAdapter(api_key="nvapi-...")
        >>> result = vlm.detect_objects("photo.jpg")
        >>> print(result)
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "meta/llama-4-maverick-17b-128e-instruct"):
        """
        Initialize VLM vision adapter.
        
        Args:
            api_key: NVIDIA API key
            model: VLM model to use (default: Llama 4 Maverick)
                   Options: meta/llama-4-maverick-17b-128e-instruct,
                           meta/llama-4-scout-17b-16e-instruct,
                           microsoft/phi-3.5-vision-instruct
        """
        super().__init__(api_key)
        self.model = model
        self.endpoint = f"{self.base_url}/v1/chat/completions"
    
    def analyze_image(
        self,
        image_path: Union[str, Path],
        prompt: str,
        max_tokens: int = 512,
        temperature: float = 0.7
    ) -> str:
        """
        Analyze image with custom prompt using VLM.
        
        Args:
            image_path: Path to image file
            prompt: Text prompt describing what to analyze
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature
            
        Returns:
            str: VLM's text response
        """
        # Upload image
        asset_id = self.upload_image(image_path)
        
        # Build chat completion request
        payload = {
            "model": self.model,
            "messages": [{
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;asset_id,{asset_id}"
                        }
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }],
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'NVCF-INPUT-ASSET-REFERENCES': asset_id
        }
        
        response = requests.post(self.endpoint, headers=headers, json=payload, timeout=300)
        response.raise_for_status()
        
        return response.json()['choices'][0]['message']['content']
    
    def detect_objects(self, image_path: Union[str, Path]) -> str:
        """
        Detect objects in image.
        
        Args:
            image_path: Path to image file
            
        Returns:
            str: List of detected objects
        """
        return self.analyze_image(
            image_path,
            "List all objects visible in this image. Be specific and comprehensive."
        )
    
    def extract_text(self, image_path: Union[str, Path]) -> str:
        """
        Extract text from image (OCR).
        
        Args:
            image_path: Path to image file
            
        Returns:
            str: Extracted text
        """
        return self.analyze_image(
            image_path,
            "Extract all text from this image. Return only the text content, preserving formatting where possible."
        )
    
    def describe_image(self, image_path: Union[str, Path], detail_level: str = "detailed") -> str:
        """
        Get image description.
        
        Args:
            image_path: Path to image file
            detail_level: "brief", "detailed", or "comprehensive"
            
        Returns:
            str: Image description
        """
        prompts = {
            "brief": "Briefly describe this image in one sentence.",
            "detailed": "Provide a detailed description of this image.",
            "comprehensive": "Provide a comprehensive description of this image, including objects, people, setting, colors, mood, and any text visible."
        }
        
        return self.analyze_image(image_path, prompts.get(detail_level, prompts["detailed"]))
    
    def count_objects(self, image_path: Union[str, Path], object_type: str) -> str:
        """
        Count specific objects in image.
        
        Args:
            image_path: Path to image file
            object_type: Type of object to count (e.g., "people", "cars")
            
        Returns:
            str: Count result
        """
        return self.analyze_image(
            image_path,
            f"Count the number of {object_type} in this image. Provide just the number and a brief explanation."
        )
    
    def answer_question(self, image_path: Union[str, Path], question: str) -> str:
        """
        Answer question about image.
        
        Args:
            image_path: Path to image file
            question: Question to answer
            
        Returns:
            str: Answer
        """
        return self.analyze_image(image_path, question)
    
    def compare_images(self, image_path1: Union[str, Path], image_path2: Union[str, Path]) -> str:
        """
        Compare two images and describe differences.
        
        Args:
            image_path1: Path to first image
            image_path2: Path to second image
            
        Returns:
            str: Comparison result
        """
        # Upload both images
        asset_id1 = self.upload_image(image_path1)
        asset_id2 = self.upload_image(image_path2)
        
        # Build request with both images
        payload = {
            "model": self.model,
            "messages": [{
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;asset_id,{asset_id1}"}
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;asset_id,{asset_id2}"}
                    },
                    {
                        "type": "text",
                        "text": "Compare these two images. What are the differences and similarities?"
                    }
                ]
            }],
            "max_tokens": 512
        }
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'NVCF-INPUT-ASSET-REFERENCES': f"{asset_id1},{asset_id2}"
        }
        
        response = requests.post(self.endpoint, headers=headers, json=payload, timeout=300)
        response.raise_for_status()
        
        return response.json()['choices'][0]['message']['content']


# Convenience exports
__all__ = [
    'VisionAdapter',
    'VLMVisionAdapter'
]
