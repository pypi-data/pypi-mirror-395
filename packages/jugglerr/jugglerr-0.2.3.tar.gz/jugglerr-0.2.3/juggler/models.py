"""
LLM Model Database - Comprehensive model capabilities across all providers.

This file defines all available models with their capabilities:
- power: "super" (70B+) or "regular" (7B-8B)
- capabilities: List of supported capabilities (streaming, vision, tool_calling, etc.)
- context_window: "large" (100K+), "medium" (30K-100K), "small" (<30K)

Available Capabilities:
- streaming: Real-time token streaming
- structured_outputs: Reliable structured data generation
- tool_calling: Basic function calling
- tool_calling_structured: Function calling with schema compliance
- parallel_tool_calling: Multiple simultaneous tool calls
- browser_search: Built-in web search
- code_execution: Can run code
- json_object: Valid JSON output
- json_schema: Strict schema following
- reasoning: Advanced reasoning (like o1/o3)
- vision: Image processing
- multilingual: Strong multi-language support
"""

# Capability constants
CAP_STREAMING = 'streaming'
CAP_STRUCTURED_OUTPUTS = 'structured_outputs'
CAP_TOOL_CALLING = 'tool_calling'
CAP_TOOL_CALLING_STRUCTURED = 'tool_calling_structured'
CAP_PARALLEL_TOOL_CALLING = 'parallel_tool_calling'
CAP_BROWSER_SEARCH = 'browser_search'
CAP_CODE_EXECUTION = 'code_execution'
CAP_JSON_OBJECT = 'json_object'
CAP_JSON_SCHEMA = 'json_schema'
CAP_REASONING = 'reasoning'
CAP_VISION = 'vision'
CAP_MULTILINGUAL = 'multilingual'

# Context window constants
CONTEXT_LARGE = 'large'      # 100K+ tokens
CONTEXT_MEDIUM = 'medium'    # 30K-100K tokens
CONTEXT_SMALL = 'small'      # <30K tokens

# Power level constants
POWER_SUPER = 'super'        # 70B+ parameters
POWER_REGULAR = 'regular'    # 7B-8B parameters


MODEL_DATABASE = {
    # ========================================================================
    # CEREBRAS
    # ========================================================================
    'cerebras': {
        # Z.ai GLM 4.6 - 357B total (32B active), dual-mode reasoning, ~1000 tok/s
        'zai-glm-4.6': {
            'power': POWER_SUPER,
            'capabilities': [
                CAP_STREAMING,
                CAP_STRUCTURED_OUTPUTS,
                CAP_TOOL_CALLING,
                CAP_TOOL_CALLING_STRUCTURED,
                CAP_PARALLEL_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_JSON_SCHEMA,
                CAP_REASONING,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_MEDIUM  # 64K tokens (200K max)
        },
        
        # Qwen3 235B - World's fastest frontier reasoning at ~1400-1700 tok/s
        'qwen-3-235b-a22b-instruct-2507': {
            'power': POWER_SUPER,
            'capabilities': [
                CAP_STREAMING,
                CAP_STRUCTURED_OUTPUTS,
                CAP_TOOL_CALLING,
                CAP_TOOL_CALLING_STRUCTURED,
                CAP_PARALLEL_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_JSON_SCHEMA,
                CAP_REASONING,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_MEDIUM  # 65,536 tokens (256K max)
        },
        
        # GPT-OSS 120B on Cerebras - No browser/code execution (Groq-only features)
        'gpt-oss-120b': {
            'power': POWER_SUPER,
            'capabilities': [
                CAP_STREAMING,
                CAP_STRUCTURED_OUTPUTS,
                CAP_TOOL_CALLING,
                CAP_TOOL_CALLING_STRUCTURED,
                CAP_PARALLEL_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_JSON_SCHEMA,
                CAP_REASONING,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_MEDIUM  # 65,536 tokens
        },
        
        # Llama 3.3 70B - WARNING: Multi-turn tool calling NOT supported!
        'llama-3.3-70b': {
            'power': POWER_SUPER,
            'capabilities': [
                CAP_STREAMING,
                CAP_STRUCTURED_OUTPUTS,
                CAP_TOOL_CALLING,
                CAP_PARALLEL_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_JSON_SCHEMA,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_MEDIUM  # 65,536 tokens
        },
        
        # Qwen3 32B - Thinking/non-thinking mode, 100+ languages
        'qwen-3-32b': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_STREAMING,
                CAP_STRUCTURED_OUTPUTS,
                CAP_TOOL_CALLING,
                CAP_TOOL_CALLING_STRUCTURED,
                CAP_PARALLEL_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_JSON_SCHEMA,
                CAP_REASONING,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_MEDIUM  # 65,536 tokens
        },
        
        # Llama 3.1 8B - Fastest inference on Cerebras
        'llama3.1-8b': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_STREAMING,
                CAP_STRUCTURED_OUTPUTS,
                CAP_TOOL_CALLING,
                CAP_TOOL_CALLING_STRUCTURED,
                CAP_PARALLEL_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_JSON_SCHEMA,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_SMALL  # 8,192 tokens
        },
    },
    
    # ========================================================================
    # GROQ
    # ========================================================================
    'groq': {
        # Kimi K2 - Trillion-parameter MoE, 32B active, exceptional tool calling
        'moonshotai/kimi-k2-instruct-0905': {
            'power': POWER_SUPER,
            'capabilities': [
                CAP_STREAMING,
                CAP_STRUCTURED_OUTPUTS,
                CAP_TOOL_CALLING,
                CAP_TOOL_CALLING_STRUCTURED,
                CAP_PARALLEL_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_JSON_SCHEMA,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE  # 262,144 tokens
        },
        
        # GPT-OSS 120B - OpenAI's reasoning model with built-in browser & code execution
        'openai/gpt-oss-120b': {
            'power': POWER_SUPER,
            'capabilities': [
                CAP_STREAMING,
                CAP_STRUCTURED_OUTPUTS,
                CAP_TOOL_CALLING,
                CAP_TOOL_CALLING_STRUCTURED,
                CAP_BROWSER_SEARCH,  # Built-in on Groq
                CAP_CODE_EXECUTION,  # Built-in on Groq
                CAP_JSON_OBJECT,
                CAP_JSON_SCHEMA,
                CAP_REASONING,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE  # 131,072 tokens
            # Note: No parallel tool calling support
        },
        
        # Llama 3.3 70B - Meta's advanced multilingual model, 8 languages
        'llama-3.3-70b-versatile': {
            'power': POWER_SUPER,
            'capabilities': [
                CAP_STREAMING,
                CAP_STRUCTURED_OUTPUTS,
                CAP_TOOL_CALLING,
                CAP_TOOL_CALLING_STRUCTURED,
                CAP_PARALLEL_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_JSON_SCHEMA,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE  # 131,072 tokens
        },
        
        # Qwen3 32B - Thinking/non-thinking mode, 100+ languages
        'qwen/qwen3-32b': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_STREAMING,
                CAP_STRUCTURED_OUTPUTS,
                CAP_TOOL_CALLING,
                CAP_TOOL_CALLING_STRUCTURED,
                CAP_PARALLEL_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_JSON_SCHEMA,
                CAP_REASONING,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE  # 131,072 tokens
        },
        
        # GPT-OSS 20B - Compact reasoning model with built-in tools
        'openai/gpt-oss-20b': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_STREAMING,
                CAP_STRUCTURED_OUTPUTS,
                CAP_TOOL_CALLING,
                CAP_TOOL_CALLING_STRUCTURED,
                CAP_BROWSER_SEARCH,  # Built-in on Groq
                CAP_CODE_EXECUTION,  # Built-in on Groq
                CAP_JSON_OBJECT,
                CAP_JSON_SCHEMA,
                CAP_REASONING,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE  # 131,072 tokens
            # Note: No parallel tool calling support
        },
        
        # Llama 4 Maverick - MULTIMODAL with vision, 128 experts, 12 languages
        'meta-llama/llama-4-maverick-17b-128e-instruct': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_STREAMING,
                CAP_STRUCTURED_OUTPUTS,
                CAP_TOOL_CALLING,
                CAP_TOOL_CALLING_STRUCTURED,
                CAP_PARALLEL_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_JSON_SCHEMA,
                CAP_VISION,  # Native multimodal!
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE  # 131,072 tokens
        },
        
        # Llama 4 Scout - MULTIMODAL with vision, 16 experts, 12 languages
        'meta-llama/llama-4-scout-17b-16e-instruct': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_STREAMING,
                CAP_STRUCTURED_OUTPUTS,
                CAP_TOOL_CALLING,
                CAP_TOOL_CALLING_STRUCTURED,
                CAP_PARALLEL_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_JSON_SCHEMA,
                CAP_VISION,  # Native multimodal!
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE  # 131,072 tokens
        },
        
        # Llama 3.1 8B - Fastest inference at ~560 tok/s, 8 languages
        'llama-3.1-8b-instant': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_STREAMING,
                CAP_STRUCTURED_OUTPUTS,
                CAP_TOOL_CALLING,
                CAP_TOOL_CALLING_STRUCTURED,
                CAP_PARALLEL_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_JSON_SCHEMA,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE  # 131,072 tokens
        },
        
        # Llama Guard 4 - 12B safety/moderation model
        'meta-llama/llama-guard-4-12b': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_STREAMING,
                CAP_STRUCTURED_OUTPUTS,
                CAP_JSON_OBJECT,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE  # 128K tokens
        },
        
        # Whisper Large V3 - Speech-to-text transcription
        'whisper-large-v3': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_MEDIUM  # Audio transcription
        },
        
        # Whisper Large V3 Turbo - Faster speech-to-text
        'whisper-large-v3-turbo': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_MEDIUM  # Audio transcription
        },
        
        # Llama Prompt Guard 2 22M - Prompt injection detection (22M params)
        'meta-llama/llama-prompt-guard-2-22m': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_STREAMING,
                CAP_JSON_OBJECT
            ],
            'context_window': CONTEXT_SMALL
        },
        
        # Llama Prompt Guard 2 86M - Prompt injection detection (86M params)
        'meta-llama/llama-prompt-guard-2-86m': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_STREAMING,
                CAP_JSON_OBJECT
            ],
            'context_window': CONTEXT_SMALL
        },
        
        # GPT-OSS Safeguard 20B - Safety/moderation model
        'openai/gpt-oss-safeguard-20b': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_STREAMING,
                CAP_STRUCTURED_OUTPUTS,
                CAP_JSON_OBJECT,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE  # 128K tokens
        },
        
        # PlayAI TTS - Text-to-speech model
        'playai-tts': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_SMALL  # TTS
        },
        
        # PlayAI TTS Arabic - Arabic text-to-speech model
        'playai-tts-arabic': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_SMALL  # TTS
        },
        
        # Groq Compound - Agentic system with built-in web search & code execution
        'groq/compound': {
            'power': POWER_SUPER,
            'capabilities': [
                CAP_STREAMING,
                CAP_STRUCTURED_OUTPUTS,
                CAP_BROWSER_SEARCH,  # Built-in
                CAP_CODE_EXECUTION,  # Built-in
                CAP_JSON_OBJECT,
                CAP_JSON_SCHEMA,
                CAP_REASONING,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE  # 131,072 tokens
            # Note: No custom tool calling support (only built-in tools)
        },
        
        # Groq Compound Mini - Smaller agentic system with built-in tools
        'groq/compound-mini': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_STREAMING,
                CAP_STRUCTURED_OUTPUTS,
                CAP_BROWSER_SEARCH,  # Built-in
                CAP_CODE_EXECUTION,  # Built-in
                CAP_JSON_OBJECT,
                CAP_JSON_SCHEMA,
                CAP_REASONING,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE  # 131,072 tokens
            # Note: No custom tool calling support (only built-in tools)
        },
    },
    
    # ========================================================================
    # MISTRAL
    # ========================================================================
    'mistral': {
        # Mistral Large Latest - 123B, top-tier production model (always latest)
        'mistral-large-latest': {
            'power': POWER_SUPER,
            'capabilities': [
                CAP_STREAMING,
                CAP_STRUCTURED_OUTPUTS,
                CAP_TOOL_CALLING,
                CAP_TOOL_CALLING_STRUCTURED,
                CAP_PARALLEL_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_JSON_SCHEMA,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE  # 128K tokens
        },
        
        # Mistral Medium Latest - ~100B, frontier multimodal with vision (always latest)
        'mistral-medium-latest': {
            'power': POWER_SUPER,
            'capabilities': [
                CAP_STREAMING,
                CAP_STRUCTURED_OUTPUTS,
                CAP_TOOL_CALLING,
                CAP_TOOL_CALLING_STRUCTURED,
                CAP_PARALLEL_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_JSON_SCHEMA,
                CAP_VISION,
                CAP_REASONING,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE  # 131.1K tokens
        },
        
        # Pixtral Large Latest - ~100B, frontier multimodal vision model (always latest)
        'pixtral-large-latest': {
            'power': POWER_SUPER,
            'capabilities': [
                CAP_STREAMING,
                CAP_STRUCTURED_OUTPUTS,
                CAP_TOOL_CALLING,
                CAP_TOOL_CALLING_STRUCTURED,
                CAP_PARALLEL_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_JSON_SCHEMA,
                CAP_VISION,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE  # 128K tokens
        },
        
        # Magistral Medium Latest - 70B+, transparent reasoning (always latest)
        'magistral-medium-latest': {
            'power': POWER_SUPER,
            'capabilities': [
                CAP_STREAMING,
                CAP_TOOL_CALLING,
                CAP_TOOL_CALLING_STRUCTURED,
                CAP_JSON_OBJECT,
                CAP_JSON_SCHEMA,
                CAP_REASONING,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE  # 128K tokens (optimal: 40K)
        },
        
        # Devstral Medium Latest - ~70B, enterprise software engineering (always latest)
        'devstral-medium-latest': {
            'power': POWER_SUPER,
            'capabilities': [
                CAP_STREAMING,
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_MEDIUM  # 40K tokens (128K max)
        },
        
        # Mistral Small Latest - 24B, cost-effective general purpose (always latest)
        'mistral-small-latest': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_STREAMING,
                CAP_TOOL_CALLING,
                CAP_TOOL_CALLING_STRUCTURED,
                CAP_PARALLEL_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_JSON_SCHEMA,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE  # 128K tokens
        },
        
        # Codestral Latest - 32B, 256K context code specialist (always latest)
        'codestral-latest': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_STREAMING,
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_JSON_SCHEMA,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE  # 256K tokens (largest code model)
        },
        
        # Magistral Small Latest - 24B, reasoning with transparency (always latest)
        'magistral-small-latest': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_STREAMING,
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_JSON_SCHEMA,
                CAP_REASONING,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE  # 128K tokens
        },
        
        # Ministral 14B Latest - 14B, efficient inference (always latest)
        'ministral-14b-latest': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_STREAMING,
                CAP_TOOL_CALLING,
                CAP_PARALLEL_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE  # 128K tokens
        },
        
        # Ministral 8B Latest - 8B, efficient inference (always latest)
        'ministral-8b-latest': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_STREAMING,
                CAP_TOOL_CALLING,
                CAP_PARALLEL_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE  # 128K tokens
        },
        
        # Ministral 3B Latest - 3B, edge/on-device deployment (always latest)
        'ministral-3b-latest': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_STREAMING,
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE  # 128K tokens
        },
        
        # Devstral Small Latest - 24B, SWE-focused (always latest)
        'devstral-small-latest': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_STREAMING,
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_MEDIUM  # 40K tokens
        },
        
        # Mistral OCR Latest - OCR/document understanding (always latest)
        'mistral-ocr-latest': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_STREAMING,
                CAP_VISION,
                CAP_JSON_OBJECT,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE  # 128K tokens
        },
        
        # Voxtral Mini Latest - Voice/audio model (always latest)
        'voxtral-mini-latest': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_STREAMING,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_MEDIUM
        },
        
        # Voxtral Small Latest - Voice/audio model (always latest)
        'voxtral-small-latest': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_STREAMING,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_MEDIUM
        },
        
        # Mistral Moderation Latest - Content moderation (always latest)
        'mistral-moderation-latest': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_STREAMING,
                CAP_JSON_OBJECT,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_MEDIUM
        },
        
        # Codestral Embed - Code embeddings
        'codestral-embed': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_MEDIUM
        },
        
        # Mistral Embed - Text embeddings
        'mistral-embed': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_MEDIUM
        },
        
        # Mistral Nemo 12B - 12B, best multilingual open-source
        'open-mistral-nemo': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_STREAMING,
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE  # 128K tokens
        },
    },
    

    
    # ============================================================================
    # NVIDIA NIM (42 working models - ALL FREE)
    # ============================================================================
    'nvidia': {
        # Total: 56 working models (up from 42)
        # Recovered 4 models from timeout issues
        # Recovered 14 models from naming issues (dots not underscores, correct prefixes)
        # Last verified: December 2, 2025
        
        # DeepSeek reasoning models (recovered - correct naming with dots)
        'deepseek-ai/deepseek-v3.1-terminus': {
            'power': POWER_SUPER,
            'capabilities': [
                CAP_REASONING,
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE
        },
        'deepseek-ai/deepseek-v3.1': {
            'power': POWER_SUPER,
            'capabilities': [
                CAP_REASONING,
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE
        },
        
        # IBM Granite models (recovered - correct naming with dots)
        'ibm/granite-3.3-8b-instruct': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE
        },
        'ibm/granite-guardian-3.0-8b': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT
            ],
            'context_window': CONTEXT_LARGE
        },
        
        # Mistral models (recovered - correct naming with dots)
        'mistralai/mistral-small-3.1-24b-instruct-2503': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE
        },
        'mistralai/mamba-codestral-7b-v0.1': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT
            ],
            'context_window': CONTEXT_LARGE
        },
        
        # Microsoft Phi models (recovered - correct naming with dots)
        'microsoft/phi-3.5-vision-instruct': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_VISION,
                CAP_TOOL_CALLING,
                CAP_REASONING
            ],
            'context_window': CONTEXT_LARGE
        },
        'microsoft/phi-3.5-mini-instruct': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_TOOL_CALLING,
                CAP_REASONING,
                CAP_JSON_OBJECT
            ],
            'context_window': CONTEXT_LARGE
        },
        
        # Qwen coder model (recovered - correct naming with dots)
        'qwen/qwen2.5-coder-7b-instruct': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_TOOL_CALLING,
                CAP_CODE_EXECUTION,
                CAP_JSON_OBJECT
            ],
            'context_window': CONTEXT_LARGE
        },
        
        # AI21 Jamba model (recovered - correct naming with dots)
        'ai21labs/jamba-1.5-mini-instruct': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE
        },
        
        # Abacus AI model (recovered - correct naming with dots)
        'abacusai/dracarys-llama-3.1-70b-instruct': {
            'power': POWER_SUPER,
            'capabilities': [
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE
        },
        
        # Upstage Solar model (recovered - correct naming with dots)
        'upstage/solar-10.7b-instruct': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE
        },
        
        # Speakleash Bielik model (recovered - correct naming with dots)
        'speakleash/bielik-11b-v2.6-instruct': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE
        },
        
        # NVIDIA ChatQA model (recovered - correct naming)
        'nvidia/llama3-chatqa-1.5-8b': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_REASONING
            ],
            'context_window': CONTEXT_LARGE
        },
        
        # Recovered models (previously had timeout issues)
        'minimaxai/minimax-m2': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_VISION,
                CAP_TOOL_CALLING,
                CAP_REASONING,
                CAP_CODE_EXECUTION,
            ],
            'context_window': CONTEXT_LARGE
        },
        'marin/marin-8b-instruct': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_VISION,
                CAP_TOOL_CALLING,
                CAP_REASONING,
            ],
            'context_window': CONTEXT_LARGE
        },
        'microsoft/phi-3-small-128k-instruct': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_VISION,
            ],
            'context_window': CONTEXT_LARGE
        },
        'mistralai/mistral-nemotron': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_VISION,
                CAP_TOOL_CALLING,
                CAP_CODE_EXECUTION,
            ],
            'context_window': CONTEXT_LARGE
        },
        
        # Original working models
        'stockmark/stockmark-2-100b-instruct': {
            'power': POWER_SUPER,
            'capabilities': [
                CAP_TOOL_CALLING,
            ],
            'context_window': CONTEXT_LARGE
        },
        'qwen/qwen3-next-80b-a3b-instruct': {
            'power': POWER_SUPER,
            'capabilities': [
                CAP_VISION,
                CAP_TOOL_CALLING,
            ],
            'context_window': CONTEXT_LARGE
        },
        'moonshotai/kimi-k2-instruct-0905': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_VISION,
                CAP_TOOL_CALLING,
                CAP_REASONING,
            ],
            'context_window': CONTEXT_LARGE
        },
        'bytedance/seed-oss-36b-instruct': {
            'power': POWER_SUPER,
            'capabilities': [
                CAP_TOOL_CALLING,
                CAP_REASONING,
            ],
            'context_window': CONTEXT_LARGE
        },
        'qwen/qwen3-coder-480b-a35b-instruct': {
            'power': POWER_SUPER,
            'capabilities': [
                CAP_TOOL_CALLING,
                CAP_CODE_EXECUTION,
            ],
            'context_window': CONTEXT_LARGE
        },
        'microsoft/phi-4-mini-flash-reasoning': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_VISION,
                CAP_TOOL_CALLING,
                CAP_REASONING,
            ],
            'context_window': CONTEXT_LARGE
        },
        'moonshotai/kimi-k2-instruct': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_VISION,
                CAP_TOOL_CALLING,
                CAP_REASONING,
                CAP_CODE_EXECUTION,
            ],
            'context_window': CONTEXT_LARGE
        },
        'mistralai/magistral-small-2506': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_VISION,
                CAP_TOOL_CALLING,
                CAP_REASONING,
            ],
            'context_window': CONTEXT_LARGE
        },
        'google/gemma-3n-e4b-it': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_VISION,
                CAP_CODE_EXECUTION,
            ],
            'context_window': CONTEXT_LARGE
        },
        'google/gemma-3n-e2b-it': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_VISION,
                CAP_TOOL_CALLING,
            ],
            'context_window': CONTEXT_LARGE
        },
        'deepseek-ai/deepseek-r1-0528': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_VISION,
                CAP_TOOL_CALLING,
                CAP_REASONING,
                CAP_CODE_EXECUTION,
            ],
            'context_window': CONTEXT_LARGE
        },
        'qwen/qwen3-235b-a22b': {
            'power': POWER_SUPER,
            'capabilities': [
                CAP_VISION,
                CAP_TOOL_CALLING,
                CAP_REASONING,
                CAP_MULTILINGUAL,
            ],
            'context_window': CONTEXT_LARGE
        },
        'mistralai/mistral-medium-3-instruct': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_VISION,
                CAP_TOOL_CALLING,
                CAP_REASONING,
            ],
            'context_window': CONTEXT_LARGE
        },
        'meta/llama-4-maverick-17b-128e-instruct': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_VISION,
                CAP_TOOL_CALLING,
                CAP_MULTILINGUAL,
            ],
            'context_window': CONTEXT_LARGE
        },
        'meta/llama-4-scout-17b-16e-instruct': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_VISION,
                CAP_TOOL_CALLING,
                CAP_MULTILINGUAL,
            ],
            'context_window': CONTEXT_LARGE
        },
        'qwen/qwq-32b': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_STREAMING,
                CAP_VISION,
                CAP_REASONING,
            ],
            'context_window': CONTEXT_LARGE
        },
        'google/gemma-3-27b-it': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_VISION,
                CAP_TOOL_CALLING,
                CAP_REASONING,
            ],
            'context_window': CONTEXT_LARGE
        },
        'microsoft/phi-4-multimodal-instruct': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_VISION,
                CAP_TOOL_CALLING,
                CAP_REASONING,
            ],
            'context_window': CONTEXT_LARGE
        },
        'tiiuae/falcon3-7b-instruct': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_VISION,
                CAP_TOOL_CALLING,
                CAP_REASONING,
            ],
            'context_window': CONTEXT_LARGE
        },
        'igenius/italia_10b_instruct_16k': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_VISION,
                CAP_TOOL_CALLING,
                CAP_MULTILINGUAL,
            ],
            'context_window': CONTEXT_LARGE
        },
        'nvidia/nemotron-4-mini-hindi-4b-instruct': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_VISION,
                CAP_TOOL_CALLING,
            ],
            'context_window': CONTEXT_LARGE
        },
        'qwen/qwen2-7b-instruct': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_TOOL_CALLING,
                CAP_REASONING,
                CAP_CODE_EXECUTION,
            ],
            'context_window': CONTEXT_LARGE
        },
        'nvidia/nemotron-mini-4b-instruct': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_TOOL_CALLING,
            ],
            'context_window': CONTEXT_LARGE
        },
        'rakuten/rakutenai-7b-instruct': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_VISION,
                CAP_TOOL_CALLING,
                CAP_REASONING,
            ],
            'context_window': CONTEXT_LARGE
        },
        'rakuten/rakutenai-7b-chat': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_VISION,
                CAP_TOOL_CALLING,
                CAP_REASONING,
            ],
            'context_window': CONTEXT_LARGE
        },
        'google/gemma-2-2b-it': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_TOOL_CALLING,
            ],
            'context_window': CONTEXT_LARGE
        },
        'thudm/chatglm3-6b': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_VISION,
                CAP_TOOL_CALLING,
                CAP_CODE_EXECUTION,
                CAP_MULTILINGUAL,
            ],
            'context_window': CONTEXT_LARGE
        },
        'baichuan-inc/baichuan2-13b-chat': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_TOOL_CALLING,
                CAP_CODE_EXECUTION,
            ],
            'context_window': CONTEXT_LARGE
        },
        'microsoft/phi-3-medium-128k-instruct': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_VISION,
                CAP_TOOL_CALLING,
                CAP_REASONING,
            ],
            'context_window': CONTEXT_LARGE
        },
        'google/gemma-2-27b-it': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_VISION,
                CAP_TOOL_CALLING,
                CAP_CODE_EXECUTION,
            ],
            'context_window': CONTEXT_LARGE
        },
        'mediatek/breeze-7b-instruct': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_VISION,
                CAP_TOOL_CALLING,
            ],
            'context_window': CONTEXT_LARGE
        },
        'microsoft/phi-3-small-8k-instruct': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_VISION,
                CAP_TOOL_CALLING,
                CAP_REASONING,
            ],
            'context_window': CONTEXT_LARGE
        },
        'microsoft/phi-3-medium-4k-instruct': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_VISION,
                CAP_TOOL_CALLING,
                CAP_REASONING,
            ],
            'context_window': CONTEXT_LARGE
        },
        'google/gemma-7b': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_VISION,
                CAP_TOOL_CALLING,
                CAP_CODE_EXECUTION,
            ],
            'context_window': CONTEXT_LARGE
        },
        'nvidia/riva-translate-4b-instruct': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_VISION,
                CAP_TOOL_CALLING,
                CAP_MULTILINGUAL,
            ],
            'context_window': CONTEXT_LARGE
        },
        'meta/llama-guard-4-12b': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_VISION,
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT,
            ],
            'context_window': CONTEXT_LARGE
        },
        'nvidia/vila': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_VISION,
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT,
            ],
            'context_window': CONTEXT_LARGE
        },
        'google/shieldgemma-9b': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_VISION,
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT,
            ],
            'context_window': CONTEXT_LARGE
        },
    },
    
    # ========================================================================
    # NVIDIA EMBEDDINGS
    # ========================================================================
    'nvidia-embed': {
        # Text embeddings
        'nvidia/nv-embed-v1': {
            'power': POWER_REGULAR,
            'capabilities': [CAP_MULTILINGUAL],
            'context_window': CONTEXT_LARGE,
            'task': 'embedding',
            'dimension': 4096
        },
        
        # Code embeddings
        'nvidia/nv-embedcode-7b-v1': {
            'power': POWER_REGULAR,
            'capabilities': [CAP_CODE_EXECUTION],
            'context_window': CONTEXT_LARGE,
            'task': 'embedding',
            'dimension': 4096,
            'requires_input_type': True
        },
        
        # Retrieval embeddings
        'nvidia/llama-3_2-nemoretriever-300m-embed-v1': {
            'power': POWER_REGULAR,
            'capabilities': [CAP_MULTILINGUAL],
            'context_window': CONTEXT_LARGE,
            'task': 'embedding',
            'dimension': 2048,
            'requires_input_type': True
        },
        
        # Vision-language embeddings
        'nvidia/llama-3_2-nemoretriever-1b-vlm-embed-v1': {
            'power': POWER_REGULAR,
            'capabilities': [CAP_VISION, CAP_MULTILINGUAL],
            'context_window': CONTEXT_LARGE,
            'task': 'embedding',
            'dimension': 1024
        },
        
        # Vision embeddings
        'nvidia/nv-dinov2': {
            'power': POWER_REGULAR,
            'capabilities': [CAP_VISION],
            'context_window': CONTEXT_LARGE,
            'task': 'embedding',
            'dimension': 1024
        },
        
        # Multilingual embeddings
        'baai/bge-m3': {
            'power': POWER_REGULAR,
            'capabilities': [CAP_MULTILINGUAL],
            'context_window': CONTEXT_LARGE,
            'task': 'embedding',
            'dimension': 1024
        },
    },
    
    # ========================================================================
    # COHERE
    # ========================================================================
    'cohere': {
        # ====================================================================
        # COMMAND A FAMILY (Latest Flagship - 111B params)
        # ====================================================================
        
        # Command A 03-2025 - Main flagship
        'command-a-03-2025': {
            'power': POWER_SUPER,
            'capabilities': [
                CAP_STREAMING,
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_MULTILINGUAL,
                CAP_VISION
            ],
            'context_window': 256000  # 256K tokens
        },
        
        # Command A Reasoning 08-2025 - Reasoning model
        'command-a-reasoning-08-2025': {
            'power': POWER_SUPER,
            'capabilities': [
                CAP_STREAMING,
                CAP_TOOL_CALLING,
                CAP_MULTILINGUAL
            ],
            'context_window': 256000  # 256K tokens, 32K max output
        },
        
        # Command A Translate 08-2025 - Translation specialist
        'command-a-translate-08-2025': {
            'power': POWER_SUPER,
            'capabilities': [
                CAP_STREAMING,
                CAP_MULTILINGUAL
            ],
            'context_window': 16000  # 8K input + 8K output
        },
        
        # Command A Vision 07-2025 - Multimodal (up to 20 images)
        'command-a-vision-07-2025': {
            'power': POWER_SUPER,
            'capabilities': [
                CAP_STREAMING,
                CAP_VISION,
                CAP_MULTILINGUAL,
                CAP_JSON_OBJECT
            ],
            'context_window': CONTEXT_LARGE  # 128K tokens
        },
        
        # ====================================================================
        # COMMAND R FAMILY
        # ====================================================================
        
        # Command R7B 12-2024 - Compact 7B model
        'command-r7b-12-2024': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_STREAMING,
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_MULTILINGUAL,
                CAP_VISION
            ],
            'context_window': CONTEXT_LARGE  # 128K tokens
        },
        
        # Command R+ 08-2024 - R+ flagship
        'command-r-plus-08-2024': {
            'power': POWER_SUPER,
            'capabilities': [
                CAP_STREAMING,
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_MULTILINGUAL,
                CAP_VISION
            ],
            'context_window': CONTEXT_LARGE  # 128K tokens
        },
        
        # Command R 08-2024 - R efficient
        'command-r-08-2024': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_STREAMING,
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_MULTILINGUAL,
                CAP_VISION
            ],
            'context_window': CONTEXT_LARGE  # 128K tokens
        },
        
        # ====================================================================
        # LEGACY COMMAND MODELS
        # ====================================================================
        
        # Command R+ - Legacy flagship
        'command-r-plus': {
            'power': POWER_SUPER,
            'capabilities': [
                CAP_STREAMING,
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE  # 128K tokens
        },
        
        # Command R - Legacy efficient
        'command-r': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_STREAMING,
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE  # 128K tokens
        },
        
        # Command - Basic legacy model
        'command': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_STREAMING,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_MEDIUM  # 4K tokens
        },
    }
}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_models_by_power(provider: str, power: str) -> list:
    """Get all models for a provider with given power level."""
    provider_models = MODEL_DATABASE.get(provider, {})
    return [
        model_name
        for model_name, model_info in provider_models.items()
        if model_info.get('power') == power
    ]


def get_models_by_capability(provider: str, capability: str) -> list:
    """Get all models for a provider with given capability."""
    provider_models = MODEL_DATABASE.get(provider, {})
    return [
        model_name
        for model_name, model_info in provider_models.items()
        if capability in model_info.get('capabilities', [])
    ]


def get_models_by_context(provider: str, context_window: str) -> list:
    """Get all models for a provider with given context window."""
    provider_models = MODEL_DATABASE.get(provider, {})
    return [
        model_name
        for model_name, model_info in provider_models.items()
        if model_info.get('context_window') == context_window
    ]


def get_model_info(provider: str, model_name: str) -> dict:
    """Get full info for a specific model."""
    return MODEL_DATABASE.get(provider, {}).get(model_name, {})


def list_all_models(provider: str = None) -> dict:
    """List all models, optionally filtered by provider."""
    if provider:
        return {provider: MODEL_DATABASE.get(provider, {})}
    return MODEL_DATABASE
