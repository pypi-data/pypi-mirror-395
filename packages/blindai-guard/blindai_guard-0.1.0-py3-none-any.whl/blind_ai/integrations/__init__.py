"""Blind AI framework integrations.

Provides secure wrappers for popular AI frameworks:
- LangChain
- LlamaIndex
- CrewAI
- AutoGen
- Semantic Kernel
- Haystack

Also provides observability utilities:
- Metrics (Prometheus, StatsD)
- Structured logging with correlation IDs
- Distributed tracing (OpenTelemetry)
"""

# Observability (always available - no external dependencies required)
from .observability import (
    ObservableGuard,
    SecurityMetrics,
    StructuredLogContext,
    get_metrics,
    init_tracing,
    logging_context,
    reset_metrics,
    trace_security_check,
)

# Tool Registry utilities (always available)
from .registry import (
    ConfidenceLevel,
    RegistryConfig,
    ToolRegistryMixin,
    auto_register_tool,
    get_registry_config,
    infer_tool_type,
    infer_trust_level,
    set_registry_config,
)

# Input utilities (always available)
from .utils import (
    MAX_INPUT_SIZE,
    InputSizeLimiter,
    extract_tool_input,
    safe_json_serialize,
    truncate_input,
)

__all_observability__ = [
    "SecurityMetrics",
    "StructuredLogContext",
    "ObservableGuard",
    "get_metrics",
    "reset_metrics",
    "logging_context",
    "init_tracing",
    "trace_security_check",
]

__all_registry__ = [
    "auto_register_tool",
    "infer_tool_type",
    "infer_trust_level",
    "ToolRegistryMixin",
    "RegistryConfig",
    "ConfidenceLevel",
    "get_registry_config",
    "set_registry_config",
]

__all_utils__ = [
    "MAX_INPUT_SIZE",
    "truncate_input",
    "safe_json_serialize",
    "extract_tool_input",
    "InputSizeLimiter",
]

# LangChain integration (optional dependency)
try:
    from .langchain import (
        BlindAICallbackHandler,
        BlindAIToolWrapper as LangChainToolWrapper,
        create_protected_tool as create_langchain_tool,
        protect_tool as protect_langchain_tool,
    )

    __all_langchain__ = [
        "LangChainToolWrapper",
        "BlindAICallbackHandler",
        "protect_langchain_tool",
        "create_langchain_tool",
    ]
except ImportError:
    __all_langchain__ = []

# LlamaIndex integration (optional dependency)
try:
    from .llamaindex import (
        BlindAIObserver as LlamaIndexObserver,
        BlindAIToolWrapper as LlamaIndexToolWrapper,
        create_protected_tool as create_llamaindex_tool,
        protect_tool as protect_llamaindex_tool,
    )

    __all_llamaindex__ = [
        "LlamaIndexToolWrapper",
        "LlamaIndexObserver",
        "protect_llamaindex_tool",
        "create_llamaindex_tool",
    ]
except ImportError:
    __all_llamaindex__ = []

# CrewAI integration (optional dependency)
try:
    from .crewai import (
        BlindAICrewCallback,
        BlindAICrewTool,
        protect_crew_tool,
        wrap_crew_tools,
    )

    __all_crewai__ = [
        "BlindAICrewTool",
        "BlindAICrewCallback",
        "protect_crew_tool",
        "wrap_crew_tools",
    ]
except ImportError:
    __all_crewai__ = []

# AutoGen integration (optional dependency)
try:
    from .autogen import (
        BlindAIAutoGenMonitor,
        create_safe_autogen_agent,
        protect_autogen_function,
        wrap_autogen_functions,
    )

    __all_autogen__ = [
        "BlindAIAutoGenMonitor",
        "protect_autogen_function",
        "wrap_autogen_functions",
        "create_safe_autogen_agent",
    ]
except ImportError:
    __all_autogen__ = []

# Semantic Kernel integration (optional dependency)
try:
    from .semantic_kernel import (
        BlindAIKernelFilter,
        create_protected_plugin,
        protect_kernel_function,
        wrap_kernel_functions,
    )

    __all_semantic_kernel__ = [
        "BlindAIKernelFilter",
        "protect_kernel_function",
        "wrap_kernel_functions",
        "create_protected_plugin",
    ]
except ImportError:
    __all_semantic_kernel__ = []

# Haystack integration (optional dependency)
try:
    from .haystack import (
        BlindAIHaystackComponent,
        BlindAIPipelineMonitor,
        protect_haystack_component,
        wrap_haystack_components,
    )

    __all_haystack__ = [
        "BlindAIHaystackComponent",
        "BlindAIPipelineMonitor",
        "protect_haystack_component",
        "wrap_haystack_components",
    ]
except ImportError:
    __all_haystack__ = []

__all__ = (
    __all_observability__
    + __all_registry__
    + __all_utils__
    + __all_langchain__
    + __all_llamaindex__
    + __all_crewai__
    + __all_autogen__
    + __all_semantic_kernel__
    + __all_haystack__
)
