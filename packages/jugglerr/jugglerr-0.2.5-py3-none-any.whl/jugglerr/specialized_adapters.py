"""
Specialized model adapters for NVIDIA NIM.

This module provides adapters for NVIDIA specialized models:
- Safety/Moderation models
- Translation models
- Vision models (future)
- TTS models (future)
- Reranking models (future)
"""

from typing import List, Optional, Dict, Any
import requests
import base64


class SafetyAdapter:
    """
    Adapter for NVIDIA safety and content moderation models.
    
    Working models:
    - meta/llama-guard-4-12b
    - (others may require special access)
    """
    
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://integrate.api.nvidia.com/v1"
    ):
        """
        Initialize safety adapter.
        
        Args:
            api_key: NVIDIA API key
            base_url: Base URL for NVIDIA API
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    
    def check_safety(
        self,
        text: str,
        model: str = "meta/llama-guard-4-12b",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Check content safety.
        
        Args:
            text: Text to check for safety issues
            model: Safety model ID
            **kwargs: Additional parameters
        
        Returns:
            Dictionary with safety assessment
        
        Example:
            >>> adapter = SafetyAdapter(api_key="...")
            >>> result = adapter.check_safety("This is a test message")
            >>> print(result['safe'])  # True or False
        """
        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": text}
            ],
            "max_tokens": kwargs.get('max_tokens', 100),
            **kwargs
        }
        
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=self.headers,
            json=payload,
            timeout=kwargs.get('timeout', 30)
        )
        
        if response.status_code != 200:
            raise Exception(f"HTTP {response.status_code}: {response.text}")
        
        data = response.json()
        
        # Parse safety response
        content = data.get('choices', [{}])[0].get('message', {}).get('content', '')
        
        # Different models have different response formats
        is_safe = self._parse_safety_response(content, model)
        
        return {
            'safe': is_safe,
            'content': content,
            'raw_response': data
        }
    
    def _parse_safety_response(self, content: str, model: str) -> bool:
        """
        Parse safety response based on model type.
        
        Different models return different formats:
        - Llama Guard 4: "safe" or "unsafe\nS1"
        - Nemotron/NemoGuard: JSON with "User Safety": "safe"/"unsafe"
        - Topic Control: "on-topic" or "off-topic"
        """
        content_lower = content.lower().strip()
        
        # Llama Guard 4 format
        if content_lower.startswith('safe'):
            return True
        if content_lower.startswith('unsafe'):
            return False
        
        # Nemotron/NemoGuard JSON format
        if '"user safety": "safe"' in content_lower or '"user safety":"safe"' in content_lower:
            return True
        if '"user safety": "unsafe"' in content_lower or '"user safety":"unsafe"' in content_lower:
            return False
        
        # Topic Control format
        if content_lower.startswith('on-topic'):
            return True
        if content_lower.startswith('off-topic'):
            return False
        
        # Default: assume unsafe if we can't parse
        return False
    
    def moderate_content(
        self,
        text: str,
        model: str = "meta/llama-guard-4-12b",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Moderate content (alias for check_safety).
        
        Args:
            text: Text to moderate
            model: Safety model ID
            **kwargs: Additional parameters
        
        Returns:
            Dictionary with moderation results
        """
        return self.check_safety(text, model, **kwargs)
class TranslationAdapter:
    """
    Adapter for NVIDIA translation models.
    
    Working models:
    - nvidia/riva-translate-4b-instruct
    """
    
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://integrate.api.nvidia.com/v1"
    ):
        """
        Initialize translation adapter.
        
        Args:
            api_key: NVIDIA API key
            base_url: Base URL for NVIDIA API
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    
    def translate(
        self,
        text: str,
        target_language: str,
        source_language: Optional[str] = None,
        model: str = "nvidia/riva-translate-4b-instruct",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Translate text to target language.
        
        Args:
            text: Text to translate
            target_language: Target language (e.g., "Spanish", "French", "es", "fr")
            source_language: Source language (optional, auto-detected if not provided)
            model: Translation model ID
            **kwargs: Additional parameters
        
        Returns:
            Dictionary with translation results
        
        Example:
            >>> adapter = TranslationAdapter(api_key="...")
            >>> result = adapter.translate("Hello", "Spanish")
            >>> print(result['translation'])  # "Hola"
        """
        # Build prompt
        if source_language:
            prompt = f"Translate from {source_language} to {target_language}: {text}"
        else:
            prompt = f"Translate to {target_language}: {text}"
        
        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": kwargs.get('max_tokens', 500),
            "temperature": kwargs.get('temperature', 0.3),  # Lower temp for translation
            **kwargs
        }
        
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=self.headers,
            json=payload,
            timeout=kwargs.get('timeout', 30)
        )
        
        if response.status_code != 200:
            raise Exception(f"HTTP {response.status_code}: {response.text}")
        
        data = response.json()
        
        # Extract translation
        translation = data.get('choices', [{}])[0].get('message', {}).get('content', '')
        
        return {
            'translation': translation.strip(),
            'source_text': text,
            'target_language': target_language,
            'source_language': source_language,
            'raw_response': data
        }
    
    def batch_translate(
        self,
        texts: List[str],
        target_language: str,
        source_language: Optional[str] = None,
        model: str = "nvidia/riva-translate-4b-instruct",
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Translate multiple texts.
        
        Args:
            texts: List of texts to translate
            target_language: Target language
            source_language: Source language (optional)
            model: Translation model ID
            **kwargs: Additional parameters
        
        Returns:
            List of translation results
        """
        results = []
        for text in texts:
            result = self.translate(
                text=text,
                target_language=target_language,
                source_language=source_language,
                model=model,
                **kwargs
            )
            results.append(result)
        
        return results


class VisionAdapter:
    """
    Adapter for NVIDIA vision models using NVCF Asset API.
    
    Working models:
    - nvidia/ocdrnet (OCR)
    - nvidia/retail-object-detection (Object detection)
    - nvidia/nv-grounding-dino (Grounding)
    - nvidia/visual-changenet (Change detection)
    
    Note: Vision models use ai.api.nvidia.com and require asset upload workflow.
    """
    
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://ai.api.nvidia.com/v1"
    ):
        """
        Initialize vision adapter.
        
        Args:
            api_key: NVIDIA API key
            base_url: Base URL for NVIDIA vision API (default: ai.api.nvidia.com)
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    
    def upload_asset(self, file_path: str, content_type: str = "image/jpeg") -> str:
        """
        Upload image asset to NVCF and get asset ID.
        
        Args:
            file_path: Path to image file
            content_type: MIME type of the file
        
        Returns:
            Asset ID (UUID)
        
        Reference: https://docs.api.nvidia.com/cloud-functions/reference/createasset
        """
        # Step 1: Create asset and get presigned URL
        create_url = "https://api.nvcf.nvidia.com/v2/nvcf/assets"
        create_headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        create_payload = {
            "contentType": content_type,
            "description": f"Image upload from {file_path}"
        }
        
        response = requests.post(
            create_url,
            headers=create_headers,
            json=create_payload,
            timeout=30
        )
        
        if response.status_code not in [200, 201]:
            raise Exception(f"Asset creation failed: HTTP {response.status_code}: {response.text}")
        
        asset_data = response.json()
        asset_id = asset_data.get('assetId')
        upload_url = asset_data.get('uploadUrl')
        
        if not asset_id or not upload_url:
            raise Exception(f"Invalid asset response: {asset_data}")
        
        # Step 2: Upload file to presigned URL
        with open(file_path, 'rb') as f:
            file_data = f.read()
        
        upload_headers = {
            'Content-Type': content_type,
            'x-amz-meta-nvcf-asset-description': f"Image from {file_path}"
        }
        
        upload_response = requests.put(
            upload_url,
            headers=upload_headers,
            data=file_data,
            timeout=60
        )
        
        if upload_response.status_code not in [200, 201]:
            raise Exception(f"Asset upload failed: HTTP {upload_response.status_code}")
        
        return asset_id
    
    def _call_vision_model(
        self,
        model: str,
        asset_id: str,
        payload: Dict[str, Any],
        **kwargs
    ) -> Dict[str, Any]:
        """
        Internal method to call vision models with asset ID.
        
        Args:
            model: Model ID (e.g., "nvidia/ocdrnet")
            asset_id: Asset ID from upload_asset()
            payload: Request payload
            **kwargs: Additional parameters
        
        Returns:
            Model response (may be async with requestId)
        """
        # Extract publisher and model name
        if '/' in model:
            publisher, model_name = model.split('/', 1)
        else:
            publisher = 'nvidia'
            model_name = model
        
        # Build endpoint URL
        endpoint = f"{self.base_url}/cv/{publisher}/{model_name}"
        
        # Add asset ID to headers (CRITICAL!)
        headers = self.headers.copy()
        headers['NVCF-INPUT-ASSET-REFERENCES'] = asset_id
        
        response = requests.post(
            endpoint,
            headers=headers,
            json=payload,
            timeout=kwargs.get('timeout', 60)
        )
        
        # Handle async responses (202)
        if response.status_code == 202:
            # Get requestId and poll for results
            result = response.json()
            request_id = result.get('requestId')
            
            if not request_id:
                raise Exception(f"Async response missing requestId: {result}")
            
            # Poll for results
            return self._poll_results(request_id, **kwargs)
        
        if response.status_code != 200:
            raise Exception(f"HTTP {response.status_code}: {response.text}")
        
        return response.json()
    
    def _poll_results(
        self,
        request_id: str,
        max_attempts: int = 30,
        poll_interval: int = 2,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Poll for async inference results.
        
        Args:
            request_id: Request ID from async response
            max_attempts: Maximum polling attempts
            poll_interval: Seconds between polls
        
        Returns:
            Final result
        """
        import time
        
        poll_url = f"{self.base_url}/v2/nvcf/pexec/status/{request_id}"
        poll_headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Accept': 'application/json'
        }
        
        for attempt in range(max_attempts):
            response = requests.get(
                poll_url,
                headers=poll_headers,
                timeout=30
            )
            
            if response.status_code == 200:
                # Result ready
                return response.json()
            
            if response.status_code == 202:
                # Still processing
                time.sleep(poll_interval)
                continue
            
            # Error
            raise Exception(f"Polling failed: HTTP {response.status_code}: {response.text}")
        
        raise Exception(f"Polling timeout after {max_attempts} attempts")
    
    def ocr(
        self,
        image_path: str,
        model: str = "nvidia/ocdrnet",
        render_label: bool = True,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Extract text from image using OCR.
        
        Args:
            image_path: Path to image file
            model: OCR model ID (default: nvidia/ocdrnet)
            render_label: Whether to render labels in output
            **kwargs: Additional parameters
        
        Returns:
            Dictionary with OCR results
        
        Example:
            >>> adapter = VisionAdapter(api_key="...")
            >>> result = adapter.ocr("document.jpg")
            >>> print(result['texts'])
        """
        # Upload image and get asset ID
        asset_id = self.upload_asset(image_path)
        
        # Build payload
        payload = {
            "image": asset_id,
            "render_label": render_label
        }
        
        # Call model
        result = self._call_vision_model(model, asset_id, payload, **kwargs)
        
        return {
            'texts': result.get('texts', []),
            'asset_id': asset_id,
            'raw_response': result
        }
    
    def detect_objects(
        self,
        image_path: str,
        model: str = "nvidia/retail-object-detection",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Detect objects in image.
        
        Args:
            image_path: Path to image file
            model: Detection model ID
            **kwargs: Additional parameters
        
        Returns:
            Dictionary with detection results
        
        Example:
            >>> adapter = VisionAdapter(api_key="...")
            >>> result = adapter.detect_objects("store.jpg")
            >>> print(result['detections'])
        """
        # Upload image and get asset ID
        asset_id = self.upload_asset(image_path)
        
        # Build payload
        payload = {
            "image": asset_id
        }
        
        # Call model
        result = self._call_vision_model(model, asset_id, payload, **kwargs)
        
        return {
            'detections': result.get('detections', []),
            'asset_id': asset_id,
            'raw_response': result
        }
    
    def ground_objects(
        self,
        image_path: str,
        prompt: str,
        model: str = "nvidia/nv-grounding-dino",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Ground objects in image based on text prompt.
        
        Args:
            image_path: Path to image file
            prompt: Text prompt describing objects to find
            model: Grounding model ID
            **kwargs: Additional parameters
        
        Returns:
            Dictionary with grounding results
        
        Example:
            >>> adapter = VisionAdapter(api_key="...")
            >>> result = adapter.ground_objects("scene.jpg", "red car")
            >>> print(result['groundings'])
        """
        # Upload image and get asset ID
        asset_id = self.upload_asset(image_path)
        
        # Build payload
        payload = {
            "image": asset_id,
            "prompt": prompt
        }
        
        # Call model
        result = self._call_vision_model(model, asset_id, payload, **kwargs)
        
        return {
            'groundings': result.get('groundings', []),
            'asset_id': asset_id,
            'raw_response': result
        }
    
    def detect_changes(
        self,
        before_image_path: str,
        after_image_path: str,
        model: str = "nvidia/visual-changenet",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Detect changes between two images.
        
        Args:
            before_image_path: Path to "before" image
            after_image_path: Path to "after" image
            model: Change detection model ID
            **kwargs: Additional parameters
        
        Returns:
            Dictionary with change detection results
        
        Example:
            >>> adapter = VisionAdapter(api_key="...")
            >>> result = adapter.detect_changes("before.jpg", "after.jpg")
            >>> print(result['changes'])
        """
        # Upload both images
        before_asset_id = self.upload_asset(before_image_path)
        after_asset_id = self.upload_asset(after_image_path)
        
        # Build payload
        payload = {
            "before_image": before_asset_id,
            "after_image": after_asset_id
        }
        
        # Use comma-separated asset IDs in header
        combined_asset_id = f"{before_asset_id},{after_asset_id}"
        
        # Call model
        result = self._call_vision_model(model, combined_asset_id, payload, **kwargs)
        
        return {
            'changes': result.get('changes', []),
            'before_asset_id': before_asset_id,
            'after_asset_id': after_asset_id,
            'raw_response': result
        }


class RivaTTSAdapter:
    """
    Adapter for NVIDIA Riva TTS NIM (self-hosted only).
    
    IMPORTANT: Magpie TTS models are NOT available via cloud API.
    They require self-hosted deployment using Docker containers.
    
    Models:
    - nvidia/magpie-tts-flow (English, offline only)
    - nvidia/magpie-tts-zeroshot (Multilingual, supports streaming)
    
    Deployment:
    - Container: nvcr.io/nim/nvidia/magpie-tts-zeroshot:latest
    - Container: nvcr.io/nim/nvidia/magpie-tts-flow:latest
    - Default port: 9000 (HTTP), 50051 (gRPC)
    
    Documentation:
    - https://docs.nvidia.com/nim/riva/tts/latest/getting-started.html
    
    Note: Requires NVIDIA AI Enterprise license
    """
    
    def __init__(self, base_url: str = "http://localhost:9000"):
        """
        Initialize Riva TTS adapter for self-hosted deployment.
        
        Args:
            base_url: Base URL of self-hosted Riva TTS NIM (default: http://localhost:9000)
        
        Example:
            >>> tts = RivaTTSAdapter(base_url="http://your-server:9000")
        """
        self.base_url = base_url.rstrip('/')
    
    def list_voices(self) -> Dict[str, Any]:
        """
        List available voices.
        
        Returns:
            Dictionary mapping language codes to voice IDs
        
        Example:
            >>> voices = tts.list_voices()
            >>> print(voices['en-US']['voices'])
            ['Magpie-Multilingual.EN-US.Aria', ...]
        """
        response = requests.get(f"{self.base_url}/v1/audio/list_voices")
        
        if response.status_code != 200:
            raise Exception(f"HTTP {response.status_code}: {response.text}")
        
        return response.json()
    
    def synthesize(
        self,
        text: str,
        language: str = "en-US",
        voice: Optional[str] = None,
        audio_prompt_path: Optional[str] = None,
        audio_prompt_transcript: Optional[str] = None,
        sample_rate_hz: int = 22050
    ) -> bytes:
        """
        Convert text to speech (non-streaming).
        
        Args:
            text: Text to synthesize
            language: Language code (e.g., "en-US", "es-ES")
            voice: Voice ID (for multilingual model)
            audio_prompt_path: Path to WAV file for voice cloning (zeroshot/flow)
            audio_prompt_transcript: Transcript of audio prompt (flow only)
            sample_rate_hz: Output sample rate (default: 22050)
        
        Returns:
            WAV audio bytes
        
        Example:
            >>> audio = tts.synthesize("Hello world", language="en-US")
            >>> with open("output.wav", "wb") as f:
            ...     f.write(audio)
        """
        files = {
            'language': (None, language),
            'text': (None, text),
            'sample_rate_hz': (None, str(sample_rate_hz))
        }
        
        if voice:
            files['voice'] = (None, voice)
        
        if audio_prompt_path:
            files['audio_prompt'] = (
                'prompt.wav',
                open(audio_prompt_path, 'rb'),
                'audio/wav'
            )
        
        if audio_prompt_transcript:
            files['audio_prompt_transcript'] = (None, audio_prompt_transcript)
        
        response = requests.post(
            f"{self.base_url}/v1/audio/synthesize",
            files=files,
            timeout=60
        )
        
        if response.status_code != 200:
            raise Exception(f"HTTP {response.status_code}: {response.text}")
        
        return response.content
    
    def synthesize_stream(
        self,
        text: str,
        language: str = "en-US",
        voice: Optional[str] = None,
        audio_prompt_path: Optional[str] = None,
        sample_rate_hz: int = 22050,
        chunk_size: int = 1024
    ):
        """
        Convert text to speech with streaming (raw PCM).
        
        Note: Only works with magpie-tts-zeroshot, not magpie-tts-flow.
        
        Args:
            text: Text to synthesize
            language: Language code
            voice: Voice ID (for multilingual model)
            audio_prompt_path: Path to WAV file for voice cloning
            sample_rate_hz: Output sample rate
            chunk_size: Bytes per chunk (default: 1024)
        
        Yields:
            Raw 16-bit PCM audio chunks (no WAV header)
        
        Example:
            >>> for chunk in tts.synthesize_stream("Hello world"):
            ...     # Process or play chunk
            ...     audio_player.write(chunk)
        """
        files = {
            'language': (None, language),
            'text': (None, text),
            'sample_rate_hz': (None, str(sample_rate_hz))
        }
        
        if voice:
            files['voice'] = (None, voice)
        
        if audio_prompt_path:
            files['audio_prompt'] = (
                'prompt.wav',
                open(audio_prompt_path, 'rb'),
                'audio/wav'
            )
        
        response = requests.post(
            f"{self.base_url}/v1/audio/synthesize_online",
            files=files,
            stream=True,
            timeout=60
        )
        
        if response.status_code != 200:
            raise Exception(f"HTTP {response.status_code}: {response.text}")
        
        # Yield raw PCM chunks
        for chunk in response.iter_content(chunk_size=chunk_size):
            if chunk:
                yield chunk
    
    def health_check(self) -> bool:
        """
        Check if TTS service is ready.
        
        Returns:
            True if service is ready, False otherwise
        """
        try:
            response = requests.get(f"{self.base_url}/v1/health/ready", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return data.get('status') == 'ready'
            return False
        except:
            return False


# Helper functions

def get_available_safety_models() -> List[str]:
    """Get list of available safety models (chat endpoint)."""
    return [
        "meta/llama-guard-4-12b",
        "nvidia/llama-3.1-nemotron-safety-guard-8b-v3",
        "nvidia/llama-3.1-nemoguard-8b-content-safety",
        "nvidia/llama-3.1-nemoguard-8b-topic-control",
    ]


def get_available_translation_models() -> List[str]:
    """Get list of available translation models."""
    return [
        "nvidia/riva-translate-4b-instruct",
    ]


def get_available_vision_models() -> List[str]:
    """Get list of vision models (pending implementation)."""
    return [
        "nvidia/retail-object-detection",
        "nvidia/ocdrnet",
        "nvidia/nv-grounding-dino",
        "stabilityai/stable-diffusion-3-medium",
    ]


def get_available_tts_models() -> List[str]:
    """Get list of TTS models (pending implementation)."""
    return [
        "nvidia/magpie-tts-flow",
        "nvidia/magpie-tts-zeroshot",
    ]
