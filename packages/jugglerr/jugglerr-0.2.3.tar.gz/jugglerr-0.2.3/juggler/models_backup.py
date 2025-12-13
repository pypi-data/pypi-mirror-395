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
    },
    
    # ========================================================================
    # MISTRAL
    # ========================================================================
    'mistral': {
        # Mistral Large 2.1 - 123B, top-tier production model
        'mistral-large-2411': {
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
        
        # Mistral Medium 3.1 - ~100B, frontier multimodal with vision
        'mistral-medium-2508': {
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
        
        # Pixtral Large - ~100B, frontier multimodal vision model
        'pixtral-large-2411': {
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
        
        # Magistral Medium - 70B+, transparent reasoning (like o1/o3)
        'magistral-medium-2507': {
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
        
        # Devstral Medium - ~70B, enterprise software engineering
        'devstral-medium-2506': {
            'power': POWER_SUPER,
            'capabilities': [
                CAP_STREAMING,
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_MEDIUM  # 40K tokens (128K max)
        },
        
        # Mistral Small 3.2 - 24B, cost-effective general purpose
        'mistral-small-2409': {
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
        
        # Codestral 2501 - 32B, 256K context code specialist
        'codestral-2501': {
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
        
        # Pixtral 12B - 12B, lightweight multimodal with vision
        'pixtral-12b-2410': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_STREAMING,
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_VISION,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE  # 128K tokens
        },
        
        # Magistral Small - 24B, reasoning with transparency
        'magistral-small-2507': {
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
        
        # Ministral 8B - 8B, efficient inference
        'ministral-8b-2410': {
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
        
        # Ministral 3B - 3B, edge/on-device deployment
        'ministral-3b-2410': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_STREAMING,
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE  # 128K tokens
        },
        
        # Devstral Small - 24B, SWE-focused
        'devstral-small-2505': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_STREAMING,
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_MEDIUM  # 40K tokens
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
    

    
    # ========================================================================
    # GOOGLE GEMINI
    # ========================================================================
    'google': {
        # Gemini 2.5 Pro - Latest flagship with 2M context
        'gemini-2.5-pro': {
            'power': POWER_SUPER,
            'capabilities': [
                CAP_STREAMING,
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_VISION,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE  # 2M tokens
        },
        
        # Gemini 2.5 Flash - Fast with 2M context
        'gemini-2.5-flash': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_STREAMING,
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_VISION,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE  # 2M tokens
        },
        
        # Gemini 2.0 Flash Exp - Experimental 1M context
        'gemini-2.0-flash-exp': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_STREAMING,
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_VISION,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE  # 1M tokens
        },
        
        # Gemini 2.0 Flash Thinking - Reasoning model
        'gemini-2.0-flash-thinking-exp': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_STREAMING,
                CAP_REASONING,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE  # 1M tokens
        },
        
        # Gemini 1.5 Pro - Established 2M context
        'gemini-1.5-pro': {
            'power': POWER_SUPER,
            'capabilities': [
                CAP_STREAMING,
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_VISION,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE  # 2M tokens
        },
        
        # Gemini 1.5 Flash - Fast established model
        'gemini-1.5-flash': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_STREAMING,
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_VISION,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE  # 1M tokens
        },
        
        # Gemini 1.5 Flash 8B - Lightweight efficient
        'gemini-1.5-flash-8b': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_STREAMING,
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_VISION,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE  # 1M tokens
        },
    },
    
    # ========================================================================
    # OPENROUTER (FREE MODELS ONLY)
    # ========================================================================
    'openrouter': {
        # KAT-Coder-Pro V1 - Agentic coding specialist, 73.4% SWE-Bench
        'kwaipilot/kat-coder-pro-v1': {
            'power': POWER_SUPER,
            'capabilities': [
                CAP_STREAMING,
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE  # 256K tokens
        },
        
        # Nemotron Nano 12B 2 VL - Multimodal video/document understanding
        'nvidia/nemotron-nano-12b-2-vl': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_STREAMING,
                CAP_VISION,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE  # 128K tokens
        },
        
        # Tongyi DeepResearch 30B - Agentic research specialist
        'alibaba/tongyi-deepresearch-30b-a3b': {
            'power': POWER_SUPER,
            'capabilities': [
                CAP_STREAMING,
                CAP_TOOL_CALLING,
                CAP_REASONING,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE  # 131K tokens
        },
        
        # LongCat Flash Chat - 560B MoE, 27B active
        'meituan/longcat-flash-chat': {
            'power': POWER_SUPER,
            'capabilities': [
                CAP_STREAMING,
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE  # 131K tokens
        },
        
        # Nemotron Nano 9B V2 - Unified reasoning model
        'nvidia/nemotron-nano-9b-v2': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_STREAMING,
                CAP_REASONING,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE  # 128K tokens
        },
        
        # GPT-OSS-20B - OpenAI's open-weight MoE
        'openai/gpt-oss-20b': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_STREAMING,
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_REASONING,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE  # 131K tokens
        },
        
        # Llama 3.3 70B - Meta's flagship multilingual
        'meta-llama/llama-3.3-70b-instruct': {
            'power': POWER_SUPER,
            'capabilities': [
                CAP_STREAMING,
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE  # 131K tokens
        },
        
        # Llama 3.2 3B - Lightweight multilingual
        'meta-llama/llama-3.2-3b-instruct': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_STREAMING,
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE  # 131K tokens
        },
        
        # Hermes 3 405B - Frontier agentic model
        'nousresearch/hermes-3-405b-instruct': {
            'power': POWER_SUPER,
            'capabilities': [
                CAP_STREAMING,
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_REASONING,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE  # 131K tokens
        },
        
        # Mistral 7B Instruct - Fast industry standard
        'mistralai/mistral-7b-instruct': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_STREAMING,
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_MEDIUM  # 33K tokens
        },
    },
    
    # ========================================================================
    # NVIDIA NIM
    # ========================================================================
    'nvidia': {
        # Llama 3.1 405B - Largest model
        'meta/llama-3.1-405b-instruct': {
            'power': POWER_SUPER,
            'capabilities': [
                CAP_STREAMING,
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE  # 128K tokens
        },
        
        # Llama 3.1 70B
        'meta/llama-3.1-70b-instruct': {
            'power': POWER_SUPER,
            'capabilities': [
                CAP_STREAMING,
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE  # 128K tokens
        },
        
        # Llama 3.1 8B
        'meta/llama-3.1-8b-instruct': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_STREAMING,
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE  # 128K tokens
        },
        
        # Nemotron 70B - NVIDIA's flagship
        'nvidia/llama-3.1-nemotron-70b-instruct': {
            'power': POWER_SUPER,
            'capabilities': [
                CAP_STREAMING,
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE  # 128K tokens
        },
        
        # Nemotron 51B
        'nvidia/llama-3.1-nemotron-51b-instruct': {
            'power': POWER_SUPER,
            'capabilities': [
                CAP_STREAMING,
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE  # 128K tokens
        },
        
        # Nemotron 340B - Largest NVIDIA model
        'nvidia/nemotron-4-340b-instruct': {
            'power': POWER_SUPER,
            'capabilities': [
                CAP_STREAMING,
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_MEDIUM  # 32K tokens
        },
        
        # Mistral Large via NVIDIA
        'mistralai/mistral-large-2-instruct': {
            'power': POWER_SUPER,
            'capabilities': [
                CAP_STREAMING,
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE  # 128K tokens
        },
        
        # Mixtral 8x7B via NVIDIA
        'mistralai/mixtral-8x7b-instruct': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_STREAMING,
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_MEDIUM  # 32K tokens
        },
    },
    
    # ========================================================================
    # HUGGING FACE
    # ========================================================================
    'huggingface': {
        # DeepSeek R1 - Reasoning model
        'deepseek-ai/DeepSeek-R1': {
            'power': POWER_SUPER,
            'capabilities': [
                CAP_STREAMING,
                CAP_REASONING,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE  # 128K tokens
        },
        
        # Llama 3.3 70B
        'meta-llama/Llama-3.3-70B-Instruct': {
            'power': POWER_SUPER,
            'capabilities': [
                CAP_STREAMING,
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE  # 128K tokens
        },
        
        # Qwen 2.5 72B
        'Qwen/Qwen2.5-72B-Instruct': {
            'power': POWER_SUPER,
            'capabilities': [
                CAP_STREAMING,
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE  # 128K tokens
        },
        
        # Mistral Large
        'mistralai/Mistral-Large-Instruct-2411': {
            'power': POWER_SUPER,
            'capabilities': [
                CAP_STREAMING,
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE  # 128K tokens
        },
        
        # Mixtral 8x7B
        'mistralai/Mixtral-8x7B-Instruct-v0.1': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_STREAMING,
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_MEDIUM  # 32K tokens
        },
        
        # Llama 3.1 8B
        'meta-llama/Llama-3.1-8B-Instruct': {
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
    
    # ========================================================================
    # COHERE
    # ========================================================================
    'cohere': {
        # Command R+ 08-2024 - Latest flagship
        'command-r-plus-08-2024': {
            'power': POWER_SUPER,
            'capabilities': [
                CAP_STREAMING,
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE  # 128K tokens
        },
        
        # Command R 08-2024 - Latest efficient
        'command-r-08-2024': {
            'power': POWER_REGULAR,
            'capabilities': [
                CAP_STREAMING,
                CAP_TOOL_CALLING,
                CAP_JSON_OBJECT,
                CAP_MULTILINGUAL
            ],
            'context_window': CONTEXT_LARGE  # 128K tokens
        },
        
        # Command R+ - Established flagship
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
        
        # Command R - Established efficient
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
        
        # Command - Basic model
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
