"""Shared utilities for Blind AI integrations.

Provides common functionality for input extraction, size limits, and sanitization.
"""

import json
import logging
from typing import Any, Dict, List, Optional, Tuple, Union

logger = logging.getLogger(__name__)

# Input size limits
MAX_INPUT_SIZE = 100_000  # 100KB default limit
MAX_INPUT_SIZE_WARNING = 50_000  # Warn at 50KB

# Truncation settings
TRUNCATION_SUFFIX = "... [TRUNCATED]"


def truncate_input(
    text: str,
    max_size: int = MAX_INPUT_SIZE,
    warn_size: int = MAX_INPUT_SIZE_WARNING,
    suffix: str = TRUNCATION_SUFFIX,
) -> Tuple[str, bool]:
    """Truncate input text if it exceeds size limits.
    
    Args:
        text: Input text to potentially truncate
        max_size: Maximum allowed size in characters
        warn_size: Size at which to log a warning
        suffix: Suffix to append when truncating
        
    Returns:
        Tuple of (processed_text, was_truncated)
        
    Example:
        ```python
        text, truncated = truncate_input(large_text)
        if truncated:
            logger.warning("Input was truncated")
        ```
    """
    if not text:
        return text, False
    
    text_len = len(text)
    
    if text_len > max_size:
        logger.warning(
            f"Input size ({text_len:,} chars) exceeds limit ({max_size:,}). "
            f"Truncating to {max_size:,} characters."
        )
        # Leave room for suffix
        truncate_at = max_size - len(suffix)
        return text[:truncate_at] + suffix, True
    
    if text_len > warn_size:
        logger.info(
            f"Large input detected ({text_len:,} chars). "
            f"Consider chunking for better performance."
        )
    
    return text, False


def safe_json_serialize(
    data: Any,
    max_size: int = MAX_INPUT_SIZE,
    fallback_to_str: bool = True,
) -> str:
    """Safely serialize data to JSON with size limits.
    
    Args:
        data: Data to serialize
        max_size: Maximum output size
        fallback_to_str: If True, fall back to str() on JSON errors
        
    Returns:
        JSON string (possibly truncated)
        
    Example:
        ```python
        json_str = safe_json_serialize({"query": large_query, "params": params})
        ```
    """
    try:
        json_str = json.dumps(data, ensure_ascii=False, default=str)
    except (TypeError, ValueError) as e:
        if fallback_to_str:
            logger.debug(f"JSON serialization failed ({e}), falling back to str()")
            json_str = str(data)
        else:
            raise
    
    result, truncated = truncate_input(json_str, max_size)
    return result


def extract_string_args(
    args: tuple,
    kwargs: dict,
    max_size: int = MAX_INPUT_SIZE,
) -> str:
    """Extract and serialize string arguments from args/kwargs.
    
    Preserves structure using JSON serialization with size limits.
    
    Args:
        args: Positional arguments
        kwargs: Keyword arguments
        max_size: Maximum output size
        
    Returns:
        JSON-serialized string of arguments
        
    Example:
        ```python
        input_text = extract_string_args(args, kwargs)
        result = guard.check(input_text)
        ```
    """
    # Strategy 1: If single string arg, use it directly
    if len(args) == 1 and isinstance(args[0], str) and not kwargs:
        text, _ = truncate_input(args[0], max_size)
        return text
    
    # Strategy 2: Build structured representation
    extracted = {}
    
    # Extract from args
    for i, arg in enumerate(args):
        if isinstance(arg, str):
            extracted[f"arg_{i}"] = arg
        elif isinstance(arg, (dict, list)):
            extracted[f"arg_{i}"] = arg
    
    # Extract from kwargs (prefer named params)
    for key, value in kwargs.items():
        if isinstance(value, str):
            extracted[key] = value
        elif isinstance(value, (dict, list)):
            extracted[key] = value
    
    if not extracted:
        # Fallback: convert all args to strings
        if args:
            extracted["args"] = [str(a) for a in args]
        if kwargs:
            extracted["kwargs"] = {k: str(v) for k, v in kwargs.items()}
    
    return safe_json_serialize(extracted, max_size)


def extract_tool_input(
    args: tuple,
    kwargs: dict,
    tool_input_key: Optional[str] = None,
    max_size: int = MAX_INPUT_SIZE,
) -> str:
    """Extract tool input with common patterns and size limits.
    
    Handles common tool input patterns:
    - Single string argument
    - Named 'input', 'query', 'text' parameters
    - Structured dict/list arguments
    
    Args:
        args: Positional arguments
        kwargs: Keyword arguments
        tool_input_key: Specific key to look for in kwargs
        max_size: Maximum output size
        
    Returns:
        Extracted input string (JSON-serialized if structured)
    """
    # Strategy 1: Specific key provided
    if tool_input_key and tool_input_key in kwargs:
        value = kwargs[tool_input_key]
        if isinstance(value, str):
            text, _ = truncate_input(value, max_size)
            return text
        return safe_json_serialize(value, max_size)
    
    # Strategy 2: Common input key names
    common_keys = ['input', 'query', 'text', 'prompt', 'question', 'command', 'sql']
    for key in common_keys:
        if key in kwargs:
            value = kwargs[key]
            if isinstance(value, str):
                text, _ = truncate_input(value, max_size)
                return text
            return safe_json_serialize(value, max_size)
    
    # Strategy 3: Single string positional arg
    if len(args) == 1 and isinstance(args[0], str):
        text, _ = truncate_input(args[0], max_size)
        return text
    
    # Strategy 4: First string in args
    for arg in args:
        if isinstance(arg, str):
            text, _ = truncate_input(arg, max_size)
            return text
    
    # Strategy 5: First string in kwargs
    for value in kwargs.values():
        if isinstance(value, str):
            text, _ = truncate_input(value, max_size)
            return text
    
    # Strategy 6: Serialize all string kwargs
    string_kwargs = {k: v for k, v in kwargs.items() if isinstance(v, str)}
    if string_kwargs:
        return safe_json_serialize(string_kwargs, max_size)
    
    # Fallback: serialize everything
    return extract_string_args(args, kwargs, max_size)


class InputSizeLimiter:
    """Configurable input size limiter.
    
    Example:
        ```python
        limiter = InputSizeLimiter(max_size=50_000, warn_size=25_000)
        
        text = limiter.process("large input...")
        
        # Or use as context manager for temporary limits
        with InputSizeLimiter.temporary(max_size=10_000):
            text = extract_tool_input(args, kwargs)
        ```
    """
    
    _default_max_size = MAX_INPUT_SIZE
    _default_warn_size = MAX_INPUT_SIZE_WARNING
    
    def __init__(
        self,
        max_size: Optional[int] = None,
        warn_size: Optional[int] = None,
    ):
        self.max_size = max_size or self._default_max_size
        self.warn_size = warn_size or self._default_warn_size
    
    def process(self, text: str) -> str:
        """Process text with size limits."""
        result, _ = truncate_input(text, self.max_size, self.warn_size)
        return result
    
    def serialize(self, data: Any) -> str:
        """Serialize data with size limits."""
        return safe_json_serialize(data, self.max_size)
    
    @classmethod
    def set_defaults(cls, max_size: int, warn_size: Optional[int] = None) -> None:
        """Set default size limits globally.
        
        Args:
            max_size: New default max size
            warn_size: New default warning size (defaults to max_size / 2)
        """
        cls._default_max_size = max_size
        cls._default_warn_size = warn_size or (max_size // 2)
        
        # Also update module-level constants
        global MAX_INPUT_SIZE, MAX_INPUT_SIZE_WARNING
        MAX_INPUT_SIZE = max_size
        MAX_INPUT_SIZE_WARNING = cls._default_warn_size
        
        logger.info(f"Input size limits updated: max={max_size:,}, warn={cls._default_warn_size:,}")
    
    @classmethod
    def get_defaults(cls) -> Dict[str, int]:
        """Get current default size limits."""
        return {
            "max_size": cls._default_max_size,
            "warn_size": cls._default_warn_size,
        }
