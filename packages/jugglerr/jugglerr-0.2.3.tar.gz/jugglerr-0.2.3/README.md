# 🤹 Juggler

**Juggle multiple LLM providers like a pro.** Smart routing, multi-key rotation, and automatic fallbacks across Cerebras, Groq, NVIDIA, Mistral, and Cohere.

[![PyPI version](https://badge.fury.io/py/jugglerr.svg)](https://badge.fury.io/py/jugglerr)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Why Juggler?

Access powerful LLMs across multiple providers with automatic fallbacks, smart routing, and response tracking. Juggler maximizes free tier usage while ensuring reliability.

### Key Features

- 🤹 **Multi-Provider Routing**: Cerebras, Groq, NVIDIA, Mistral, Cohere
- 🆓 **Free-Tier Optimized**: Prioritizes providers with generous free tiers
- 🔄 **Multi-Key Rotation**: Multiple API keys per provider for maximum throughput
- 🎯 **Capability-Based Routing**: Chat, vision, embeddings, reranking, TTS, STT
- ⚡ **Smart Rate Limiting**: Parses headers from Cerebras/Groq to avoid 429s
- 🔀 **Automatic Fallbacks**: Complete fallback chains for all request types
- � ***Response Tracking**: Track which models/providers were used for each request
- � ***Real-Time Streaming**: Token-by-token streaming for chat
- 🎤 **Specialized Models**: Embeddings, reranking, transcription, text-to-speech
- 📦 **Zero Config**: Auto-loads from .env file

## Installation

```bash
pip install jugglerr
```

## Quick Start

```python
from juggler import Juggler

# Auto-loads from .env file
juggler = Juggler()

# Simple chat request
response = juggler.chat("Hello, world!")
print(response)  # "Hello! How can I help you today?"

# Access tracking info
print(response.models_used)  # [{'provider': 'cerebras', 'model': 'llama3.1-8b', ...}]
```

### Setup with .env

Create a `.env` file in your project root:

```bash
# Free tier providers (tried first)
CEREBRAS_API_KEYS=csk_key1,csk_key2,csk_key3
GROQ_API_KEYS=gsk_key1,gsk_key2
NVIDIA_API_KEYS=nvapi_key1

# Additional providers with free tiers (fallback)
MISTRAL_API_KEYS=mistral_key1
COHERE_API_KEYS=cohere_key1
```

```python
# Keys loaded automatically
juggler = Juggler()

# Or pass keys directly
juggler = Juggler(
    cerebras_keys=["csk_..."],
    groq_keys=["gsk_..."],
    nvidia_keys=["nvapi_..."]
)
```

## Core Features

### 1. Chat with Automatic Fallbacks

```python
from juggler import Juggler

juggler = Juggler()

# Simple chat - automatically selects best model
response = juggler.chat("Explain quantum computing")
print(response)

# With conversation history
response = juggler.chat([
    {"role": "user", "content": "What's 2+2?"},
    {"role": "assistant", "content": "4"},
    {"role": "user", "content": "What about 2+3?"}
])

# Track which models were used
print(response.models_used)
# [{'provider': 'cerebras', 'model': 'llama3.1-8b', 'success': True, ...}]
```

### 2. Streaming Responses

```python
# Stream tokens in real-time
for chunk in juggler.chat_stream("Tell me a story"):
    print(chunk, end='', flush=True)

# With parameters
for chunk in juggler.chat_stream(
    "Explain AI",
    power="super",
    temperature=0.7
):
    print(chunk, end='', flush=True)
```

### 3. Embeddings with Fallback Chain

```python
# Generate embeddings (NVIDIA → Cohere → Mistral fallback)
embedding = juggler.embed("Hello, world!")
print(embedding)  # [0.123, -0.456, ...]
print(embedding.models_used)  # Track which provider was used
print(embedding.dimensions)  # 1024

# Batch embeddings
embeddings = juggler.embed([
    "First document",
    "Second document",
    "Third document"
])
```

### 4. Reranking for RAG

```python
# Rerank search results (NVIDIA → Cohere fallback)
results = juggler.rerank(
    query="What is machine learning?",
    documents=[
        "ML is a subset of AI...",
        "Python is a programming language...",
        "Neural networks are..."
    ]
)

# Results sorted by relevance
for doc in results:
    print(f"Score: {doc['relevance_score']:.3f} - {doc['text'][:50]}")

print(results.models_used)  # Track provider
print(results.scores)  # [0.95, 0.12, 0.87]
```

### 5. Speech-to-Text (Transcription)

```python
# Transcribe audio file
result = juggler.transcribe("audio.mp3")
print(result)  # "Hello, this is a test..."
print(result.language)  # "en"
print(result.duration)  # 5.2
print(result.models_used)

# With language hint
result = juggler.transcribe("spanish.mp3", language="es")
```

### 6. Text-to-Speech

```python
# Generate speech
audio = juggler.speak("Hello, world!")
audio.write_to_file("output.mp3")
print(audio.models_used)

# With voice selection
audio = juggler.speak(
    "This is a test",
    voice="alloy",
    speed=1.2
)
```

### 7. Power Levels & Capabilities

```python
# Use smaller, faster models (7B-32B)
response = juggler.chat(
    "Quick question",
    power="regular"
)

# Use larger, more capable models (70B+)
response = juggler.chat(
    "Complex analysis needed",
    power="super"
)

# Request specific capabilities
response = juggler.chat(
    "Analyze this image",
    capabilities=["vision"]
)

# Large context window
response = juggler.chat(
    "Analyze this long document...",
    context_window="large"
)
```

### 8. Response Tracking

All responses include `models_used` attribute:

```python
response = juggler.chat("Hello")

# See which models were tried
for attempt in response.models_used:
    print(f"{attempt['provider']}/{attempt['model']}: {attempt['success']}")
    if not attempt['success']:
        print(f"  Error: {attempt['error']}")

# Example output:
# cerebras/llama3.1-8b: True
```

## Fallback Chains

Juggler automatically falls back to alternative providers if one fails:

| Request Type | Fallback Chain |
|--------------|----------------|
| **Chat** | Cerebras → Groq → NVIDIA → Mistral → Cohere |
| **Embeddings** | NVIDIA → Cohere → Mistral |
| **Reranking** | NVIDIA → Cohere |
| **Transcription** | Groq |
| **Text-to-Speech** | Groq |

See [FALLBACK_CHAINS.md](https://github.com/spanDevOps/jugglerrr/blob/main/docs/FALLBACK_CHAINS.md) for complete details.

## Supported Providers & Models

### Chat Models

| Provider | Models | Notes |
|----------|--------|-------|
| **Cerebras** | Llama 3.1/3.3, Qwen3, GLM 4.6, GPT-OSS | Ultra-fast inference (~1000-1700 tok/s) |
| **Groq** | Llama 3.1/3.3/4, Qwen3, GPT-OSS, Kimi K2 | Vision support (Llama 4) |
| **NVIDIA** | Llama 3.1/3.3, Mistral, Qwen, Gemma, GPT-OSS | Hosted on NVIDIA NIM |
| **Mistral** | Large, Medium, Pixtral, Magistral, Codestral | Vision & reasoning models |
| **Cohere** | Command R/R+ | Enterprise-grade |

### Specialized Models

| Type | Providers | Models |
|------|-----------|--------|
| **Embeddings** | NVIDIA, Cohere, Mistral | NV-Embed-v2, embed-english-v3.0, mistral-embed |
| **Reranking** | NVIDIA, Cohere | nv-rerankqa-mistral-4b-v3, rerank-english-v3.0 |
| **Transcription** | Groq | whisper-large-v3, distil-whisper-large-v3 |
| **Text-to-Speech** | Groq | whisper-large-v3-turbo |

See [MODEL_LIST.md](https://github.com/spanDevOps/jugglerr/blob/main/docs/MODEL_LIST.md) for complete model catalog.

## How It Works

1. **Smart Provider Selection**: Providers with generous free tiers (Cerebras, Groq, NVIDIA) tried first, others (Mistral, Cohere) as fallback
2. **Model Matching**: Finds best model based on your requirements (power, capabilities, context)
3. **Key Rotation**: Cycles through multiple API keys per provider to maximize throughput
4. **Rate Limit Awareness**: Parses headers from Cerebras/Groq to avoid hitting limits
5. **Automatic Fallback**: If one provider fails, tries the next automatically
6. **Response Tracking**: Every response includes which models/providers were attempted

## Comparison with Alternatives

| Feature | LiteLLM | OpenRouter | **Juggler** |
|---------|---------|------------|-------------|
| Open source | ✅ | ❌ | ✅ |
| Multi-key rotation | ❌ | ❌ | ✅ |
| Rate limit parsing | ❌ | ❌ | ✅ |
| Response tracking | ❌ | ❌ | ✅ |
| Embeddings/Reranking | ✅ | ❌ | ✅ |
| Free-tier optimized | ❌ | ❌ | ✅ |

## API Reference

### Initialization

```python
from juggler import Juggler

# Auto-load from .env
juggler = Juggler()

# Or pass keys directly
juggler = Juggler(
    cerebras_keys=["key1", "key2"],
    groq_keys=["key1", "key2"],
    nvidia_keys=["key1"],
    mistral_keys=["key1"],
    cohere_keys=["key1"]
)
```

### Chat Methods

```python
# chat(messages, power="regular", capabilities=None, context_window=None, 
#      temperature=0.7, max_tokens=None, preferred_provider=None, 
#      preferred_model=None, **kwargs) -> ChatResponse

response = juggler.chat(
    "Hello",                    # String or list of message dicts
    power="regular",            # "regular" or "super"
    capabilities=["vision"],    # List of required capabilities
    context_window="large",     # "small", "medium", or "large"
    temperature=0.7,            # 0.0 to 2.0
    max_tokens=2000,            # Max tokens to generate
    preferred_provider="groq"   # Try this provider first
)

# chat_stream(...) -> Generator[str]
for chunk in juggler.chat_stream("Hello"):
    print(chunk, end='')
```

### Specialized Methods

```python
# Embeddings
embedding = juggler.embed("text")  # Returns EmbeddingResponse (list subclass)
embeddings = juggler.embed(["text1", "text2"])

# Reranking
results = juggler.rerank(
    query="search query",
    documents=["doc1", "doc2", "doc3"],
    top_n=3  # Optional
)  # Returns RerankResponse (list subclass)

# Transcription
text = juggler.transcribe(
    "audio.mp3",
    language="en"  # Optional
)  # Returns TranscriptionResponse (str subclass)

# Text-to-Speech
audio = juggler.speak(
    "Hello, world!",
    voice="alloy",  # Optional
    speed=1.0       # Optional
)  # Returns SpeechResponse
audio.write_to_file("output.mp3")
```

### Response Objects

All responses include `models_used` attribute:

```python
response = juggler.chat("Hello")
print(response.models_used)
# [{'provider': 'cerebras', 'model': 'llama3.1-8b', 'success': True, 
#   'timestamp': '2025-12-07T...', 'latency_ms': 234}]

# Response types behave like their base types
isinstance(response, str)  # True for ChatResponse
isinstance(embedding, list)  # True for EmbeddingResponse
isinstance(results, list)  # True for RerankResponse
```



## Examples

See the `examples/` directory for complete examples:

- `naive_user_style.py` - Simple, user-friendly examples
- `test_tracking.py` - Response tracking demonstration
- `models_used_tracking.py` - Detailed tracking examples
- `test_new_api.py` - Complete API test suite

## What's Implemented

✅ **Core Features**
- Multi-provider routing (Cerebras, Groq, NVIDIA, Mistral, Cohere)
- Capability-based model selection
- Rate limit parsing (Cerebras, Groq)
- Multi-key rotation per provider
- Automatic fallback chains
- Response tracking (`models_used`)

✅ **Request Types**
- Chat (with streaming)
- Embeddings (with fallback chain)
- Reranking (with fallback chain)
- Transcription (speech-to-text)
- Text-to-speech

✅ **Developer Experience**
- Auto-load from .env file
- Simple API (`chat()`, `embed()`, `rerank()`, etc.)
- Response objects behave like native types (str, list)
- Comprehensive documentation

## Roadmap

🔮 **Future Enhancements**
- Async support
- Cost tracking per request
- Caching layer
- More providers (Anthropic, DeepSeek)
- Vision model support
- Tool calling examples

## Documentation

📚 **[Complete Documentation](https://github.com/spanDevOps/jugglerr/tree/main/docs)** - All guides, references, and implementation details

**Quick Links:**
- 📖 [User Guide](https://github.com/spanDevOps/jugglerr/blob/main/docs/USER_GUIDE.md) - Complete usage guide
- 🔄 [Fallback Chains](https://github.com/spanDevOps/jugglerr/blob/main/docs/FALLBACK_CHAINS.md) - Provider fallback mapping
- 📊 [Response Tracking](https://github.com/spanDevOps/jugglerr/blob/main/docs/MODELS_USED_TRACKING.md) - Track model usage
- 🗂️ [Model List](https://github.com/spanDevOps/jugglerr/blob/main/docs/MODEL_LIST.md) - All available models

## Contributing

Contributions welcome! Please read [CONTRIBUTING.md](https://github.com/spanDevOps/jugglerr/blob/main/CONTRIBUTING.md) first.

## License

MIT License - see [LICENSE](https://github.com/spanDevOps/jugglerr/blob/main/LICENSE) file for details.

## Support & Sponsorship

### Get Help

- 📖 [Documentation](https://github.com/spanDevOps/jugglerr/tree/main/docs)
- 🐛 [Issue Tracker](https://github.com/spanDevOps/jugglerr/issues)
- 💬 [Discussions](https://github.com/spanDevOps/jugglerr/discussions)

### Support This Project

If Juggler helps you save time and money, consider supporting its development:

☕ **[Buy Me a Coffee](https://buymeacoffee.com/spancoder)** - One-time support

### Consulting & Enterprise Support

Need help integrating Juggler into your production systems? I offer:

- Custom integration support
- Enterprise deployment assistance
- Performance optimization
- Custom feature development
- Training for your team

📧 **Contact:** spandankb@gmail.com

---

**Built with ❤️ by [Spandan Bhol](https://github.com/spanDevOps)**

---

**Keep all your LLMs in the air!** 🤹
