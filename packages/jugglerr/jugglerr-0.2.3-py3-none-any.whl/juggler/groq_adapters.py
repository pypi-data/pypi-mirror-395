"""
Groq-specific adapters for audio APIs.

This module provides adapters for Groq's audio endpoints:
- Transcription API (whisper-large-v3, whisper-large-v3-turbo)
- Translation API (whisper models - translates to English)
- Text-to-Speech API (playai-tts, playai-tts-arabic)
"""

import os
from typing import Optional, Union, BinaryIO
from dataclasses import dataclass


@dataclass
class TranscriptionResponse:
    """Response from transcription API."""
    text: str
    model: str = None
    language: str = None
    duration: float = None
    segments: list = None


@dataclass
class TranslationResponse:
    """Response from translation API."""
    text: str
    model: str = None


@dataclass
class SpeechResponse:
    """Response from text-to-speech API."""
    audio_data: bytes
    
    def write_to_file(self, file_path: str):
        """Write audio data to file."""
        with open(file_path, 'wb') as f:
            f.write(self.audio_data)


class GroqTranscriptionAdapter:
    """
    Adapter for Groq transcription models.
    
    Supports:
    - whisper-large-v3: High-quality speech transcription
    - whisper-large-v3-turbo: Faster speech transcription
    
    Uses Groq's audio transcription API endpoint.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Groq transcription adapter.
        
        Args:
            api_key: Groq API key (or set GROQ_API_KEY env var)
        """
        self.api_key = api_key or os.getenv('GROQ_API_KEY') or os.getenv('GROQ_API_KEYS', '').split(',')[0].strip()
        if not self.api_key:
            raise ValueError("Groq API key required. Set GROQ_API_KEY or GROQ_API_KEYS or pass api_key parameter.")
        
        try:
            from groq import Groq
            self.client = Groq(api_key=self.api_key)
        except ImportError:
            raise ImportError(
                "groq package required for Groq audio. "
                "Install with: pip install groq"
            )
    
    def transcribe(
        self,
        file: Union[str, BinaryIO],
        model: str = "whisper-large-v3",
        language: Optional[str] = None,
        prompt: Optional[str] = None,
        response_format: str = "json",
        temperature: float = 0.0,
        **kwargs
    ) -> TranscriptionResponse:
        """
        Transcribe audio file.
        
        Args:
            file: Path to audio file or file-like object
            model: Model to use ("whisper-large-v3" or "whisper-large-v3-turbo")
            language: Language code (ISO-639-1) for better accuracy
            prompt: Optional text to guide the model's style
            response_format: Output format ("json", "text", "verbose_json")
            temperature: Sampling temperature (0-1)
            **kwargs: Additional parameters
        
        Returns:
            TranscriptionResponse with transcribed text
        
        Example:
            >>> adapter = GroqTranscriptionAdapter()
            >>> response = adapter.transcribe("audio.mp3", language="en")
            >>> print(response.text)
        """
        # Handle file path vs file object
        if isinstance(file, str):
            with open(file, 'rb') as f:
                file_data = (os.path.basename(file), f.read())
        else:
            file_data = file
        
        # Make API call
        transcription = self.client.audio.transcriptions.create(
            file=file_data,
            model=model,
            language=language,
            prompt=prompt,
            response_format=response_format,
            temperature=temperature,
            **kwargs
        )
        
        # Parse response based on format
        if response_format == "verbose_json":
            return TranscriptionResponse(
                text=transcription.text,
                model=getattr(transcription, 'model', model),
                language=getattr(transcription, 'language', language),
                duration=getattr(transcription, 'duration', None),
                segments=getattr(transcription, 'segments', None)
            )
        elif response_format == "text":
            return TranscriptionResponse(text=str(transcription))
        else:  # json
            return TranscriptionResponse(
                text=transcription.text,
                model=getattr(transcription, 'model', model)
            )


class GroqTranslationAdapter:
    """
    Adapter for Groq translation models.
    
    Supports:
    - whisper-large-v3: Translates audio to English
    - whisper-large-v3-turbo: Faster translation to English
    
    Uses Groq's audio translation API endpoint.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Groq translation adapter.
        
        Args:
            api_key: Groq API key (or set GROQ_API_KEY env var)
        """
        self.api_key = api_key or os.getenv('GROQ_API_KEY') or os.getenv('GROQ_API_KEYS', '').split(',')[0].strip()
        if not self.api_key:
            raise ValueError("Groq API key required. Set GROQ_API_KEY or GROQ_API_KEYS or pass api_key parameter.")
        
        try:
            from groq import Groq
            self.client = Groq(api_key=self.api_key)
        except ImportError:
            raise ImportError(
                "groq package required for Groq audio. "
                "Install with: pip install groq"
            )
    
    def translate(
        self,
        file: Union[str, BinaryIO],
        model: str = "whisper-large-v3",
        prompt: Optional[str] = None,
        response_format: str = "json",
        temperature: float = 0.0,
        **kwargs
    ) -> TranslationResponse:
        """
        Translate audio to English.
        
        Args:
            file: Path to audio file or file-like object
            model: Model to use ("whisper-large-v3" or "whisper-large-v3-turbo")
            prompt: Optional text to guide the model (should be in English)
            response_format: Output format ("json", "text", "verbose_json")
            temperature: Sampling temperature (0-1)
            **kwargs: Additional parameters
        
        Returns:
            TranslationResponse with translated text (in English)
        
        Example:
            >>> adapter = GroqTranslationAdapter()
            >>> response = adapter.translate("spanish_audio.mp3")
            >>> print(response.text)  # English translation
        """
        # Handle file path vs file object
        if isinstance(file, str):
            with open(file, 'rb') as f:
                file_data = (os.path.basename(file), f.read())
        else:
            file_data = file
        
        # Make API call
        translation = self.client.audio.translations.create(
            file=file_data,
            model=model,
            prompt=prompt,
            response_format=response_format,
            temperature=temperature,
            **kwargs
        )
        
        # Parse response
        if response_format == "text":
            return TranslationResponse(text=str(translation))
        else:
            return TranslationResponse(
                text=translation.text,
                model=getattr(translation, 'model', model)
            )


class GroqTTSAdapter:
    """
    Adapter for Groq text-to-speech models.
    
    Supports:
    - playai-tts: English TTS with 19 voices
    - playai-tts-arabic: Arabic TTS with 4 voices
    
    Uses Groq's audio speech API endpoint.
    """
    
    # Available voices
    ENGLISH_VOICES = [
        "Arista-PlayAI", "Atlas-PlayAI", "Basil-PlayAI", "Briggs-PlayAI",
        "Calum-PlayAI", "Celeste-PlayAI", "Cheyenne-PlayAI", "Chip-PlayAI",
        "Cillian-PlayAI", "Deedee-PlayAI", "Fritz-PlayAI", "Gail-PlayAI",
        "Indigo-PlayAI", "Mamaw-PlayAI", "Mason-PlayAI", "Mikail-PlayAI",
        "Mitch-PlayAI", "Quinn-PlayAI", "Thunder-PlayAI"
    ]
    
    ARABIC_VOICES = [
        "Ahmad-PlayAI", "Amira-PlayAI", "Khalid-PlayAI", "Nasser-PlayAI"
    ]
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Groq TTS adapter.
        
        Args:
            api_key: Groq API key (or set GROQ_API_KEY env var)
        """
        self.api_key = api_key or os.getenv('GROQ_API_KEY') or os.getenv('GROQ_API_KEYS', '').split(',')[0].strip()
        if not self.api_key:
            raise ValueError("Groq API key required. Set GROQ_API_KEY or GROQ_API_KEYS or pass api_key parameter.")
        
        try:
            from groq import Groq
            self.client = Groq(api_key=self.api_key)
        except ImportError:
            raise ImportError(
                "groq package required for Groq audio. "
                "Install with: pip install groq"
            )
    
    def generate_speech(
        self,
        text: str,
        voice: str = "Fritz-PlayAI",
        model: str = "playai-tts",
        response_format: str = "wav",
        sample_rate: int = 48000,
        speed: float = 1.0,
        **kwargs
    ) -> SpeechResponse:
        """
        Generate speech from text.
        
        Args:
            text: Text to convert to speech (max 10K characters)
            voice: Voice to use (see ENGLISH_VOICES or ARABIC_VOICES)
            model: Model to use ("playai-tts" or "playai-tts-arabic")
            response_format: Audio format ("wav", "mp3", "flac", "ogg", "mulaw")
            sample_rate: Sample rate (8000, 16000, 22050, 24000, 32000, 44100, 48000)
            speed: Speech speed (0.5 - 5.0)
            **kwargs: Additional parameters
        
        Returns:
            SpeechResponse with audio data
        
        Example:
            >>> adapter = GroqTTSAdapter()
            >>> response = adapter.generate_speech(
            ...     "Hello world!",
            ...     voice="Fritz-PlayAI"
            ... )
            >>> response.write_to_file("output.wav")
        """
        # Validate text length
        if len(text) > 10000:
            raise ValueError("Text exceeds maximum length of 10,000 characters")
        
        # Make API call
        response = self.client.audio.speech.create(
            model=model,
            voice=voice,
            input=text,
            response_format=response_format,
            sample_rate=sample_rate,
            speed=speed,
            **kwargs
        )
        
        # Get audio data
        audio_data = response.read()
        
        return SpeechResponse(audio_data=audio_data)
    
    def list_voices(self, model: str = "playai-tts") -> list:
        """
        List available voices for a model.
        
        Args:
            model: Model to list voices for
        
        Returns:
            List of voice names
        """
        if model == "playai-tts-arabic":
            return self.ARABIC_VOICES.copy()
        else:
            return self.ENGLISH_VOICES.copy()


# Convenience functions
def groq_transcribe(
    file: Union[str, BinaryIO],
    model: str = "whisper-large-v3",
    api_key: Optional[str] = None,
    **kwargs
) -> str:
    """
    Quick function to transcribe audio.
    
    Args:
        file: Audio file path or file object
        model: Model to use
        api_key: API key (optional)
        **kwargs: Additional parameters
    
    Returns:
        Transcribed text
    
    Example:
        >>> text = groq_transcribe("audio.mp3", language="en")
        >>> print(text)
    """
    adapter = GroqTranscriptionAdapter(api_key=api_key)
    response = adapter.transcribe(file, model=model, **kwargs)
    return response.text


def groq_translate(
    file: Union[str, BinaryIO],
    model: str = "whisper-large-v3",
    api_key: Optional[str] = None,
    **kwargs
) -> str:
    """
    Quick function to translate audio to English.
    
    Args:
        file: Audio file path or file object
        model: Model to use
        api_key: API key (optional)
        **kwargs: Additional parameters
    
    Returns:
        Translated text (in English)
    
    Example:
        >>> text = groq_translate("spanish_audio.mp3")
        >>> print(text)
    """
    adapter = GroqTranslationAdapter(api_key=api_key)
    response = adapter.translate(file, model=model, **kwargs)
    return response.text


def groq_speak(
    text: str,
    voice: str = "Fritz-PlayAI",
    output_file: Optional[str] = None,
    api_key: Optional[str] = None,
    **kwargs
) -> bytes:
    """
    Quick function to generate speech.
    
    Args:
        text: Text to speak
        voice: Voice to use
        output_file: Optional file path to save audio
        api_key: API key (optional)
        **kwargs: Additional parameters
    
    Returns:
        Audio data as bytes
    
    Example:
        >>> audio = groq_speak("Hello world!", output_file="speech.wav")
    """
    adapter = GroqTTSAdapter(api_key=api_key)
    response = adapter.generate_speech(text, voice=voice, **kwargs)
    
    if output_file:
        response.write_to_file(output_file)
    
    return response.audio_data
