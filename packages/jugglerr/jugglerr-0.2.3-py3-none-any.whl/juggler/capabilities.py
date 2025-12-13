"""Capability constants for model selection."""


class Capabilities:
    """Model capabilities for intelligent routing.
    
    Use these constants when specifying required capabilities for your requests.
    
    Example:
        >>> juggler.juggle(
        ...     "Analyze this image",
        ...     capabilities=[Capabilities.VISION]
        ... )
    """
    
    # Core capabilities
    STREAMING = 'streaming'
    STRUCTURED_OUTPUTS = 'structured_outputs'
    
    # Tool calling
    TOOL_CALLING = 'tool_calling'
    TOOL_CALLING_STRUCTURED = 'tool_calling_structured'
    PARALLEL_TOOL_CALLING = 'parallel_tool_calling'
    
    # Advanced features
    BROWSER_SEARCH = 'browser_search'
    CODE_EXECUTION = 'code_execution'
    
    # Output formats
    JSON_OBJECT = 'json_object'
    JSON_SCHEMA = 'json_schema'
    
    # Special capabilities
    REASONING = 'reasoning'
    VISION = 'vision'
    MULTILINGUAL = 'multilingual'
    
    @classmethod
    def all(cls):
        """Get all available capabilities."""
        return [
            cls.STREAMING,
            cls.STRUCTURED_OUTPUTS,
            cls.TOOL_CALLING,
            cls.TOOL_CALLING_STRUCTURED,
            cls.PARALLEL_TOOL_CALLING,
            cls.BROWSER_SEARCH,
            cls.CODE_EXECUTION,
            cls.JSON_OBJECT,
            cls.JSON_SCHEMA,
            cls.REASONING,
            cls.VISION,
            cls.MULTILINGUAL
        ]
