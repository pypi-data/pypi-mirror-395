"""Blind AI SDK client implementation."""

import functools
import logging
import threading
import time
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any, Callable, Generator, Optional, Union

import httpx

logger = logging.getLogger(__name__)


@dataclass
class ProgressMetadata:
    """Metadata provided with progress callbacks.
    
    Attributes:
        threats_detected: Number of threats detected so far
        blocked_count: Number of items blocked so far
        avg_latency_ms: Average processing time per item
        total_latency_ms: Total processing time so far
        current_item_preview: Preview of current item text (truncated)
        current_index: Index of current item being processed
        errors_count: Number of errors encountered
    """
    threats_detected: int = 0
    blocked_count: int = 0
    avg_latency_ms: float = 0.0
    total_latency_ms: float = 0.0
    current_item_preview: Optional[str] = None
    current_index: Optional[int] = None
    errors_count: int = 0
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "threats_detected": self.threats_detected,
            "blocked_count": self.blocked_count,
            "avg_latency_ms": self.avg_latency_ms,
            "total_latency_ms": self.total_latency_ms,
            "current_item_preview": self.current_item_preview,
            "current_index": self.current_index,
            "errors_count": self.errors_count,
        }


# Type alias for progress callback
ProgressCallback = Union[
    Callable[[int, int], None],  # Simple: (completed, total)
    Callable[[int, int, Optional[ProgressMetadata]], None],  # With metadata
]

from ..core.rbac import UserContext
from .circuit_breaker import CircuitBreaker, CircuitBreakerConfig, CircuitBreakerOpen
from .exceptions import (
    APIError,
    ConfigurationError,
    RetryExhaustedError,
    ThreatBlockedError,
    TimeoutError,
)
from .hooks import (
    EventHooks,
    EventType,
    SecurityEvent,
    create_error_event,
    create_event_from_result,
)
from .models import ProtectionResult, SDKConfig


class SessionContext:
    """Context object for session-scoped security checks.
    
    Holds session ID, user context, and metadata that apply to all checks
    within a guard.context() block.
    
    Attributes:
        session_id: Unique session identifier
        user: Optional user context for RBAC
        metadata: Additional metadata for all checks
    """
    
    def __init__(
        self,
        session_id: str,
        user: Optional["UserContext"] = None,
        metadata: Optional[dict[str, Any]] = None,
    ):
        self.session_id = session_id
        self.user = user
        self.metadata = metadata or {}
    
    def __repr__(self) -> str:
        return (
            f"SessionContext(session_id={self.session_id!r}, "
            f"user={self.user!r}, metadata={self.metadata!r})"
        )


class ToolGuard:
    """Blind AI SDK client for protecting tool calls.

    Provides easy integration for protecting tool/function calls from threats
    like SQL injection, prompt injection, and PII disclosure.

    Example:
        ```python
        guard = ToolGuard(api_key="your-api-key")

        # Protect a function
        @guard.protect
        def execute_sql(query: str):
            return db.execute(query)

        # This will be blocked
        try:
            result = execute_sql("DROP TABLE users")
        except ThreatBlockedError as e:
            print(f"Blocked: {e}")

        # Register event hooks
        @guard.on_block
        def handle_blocked(event):
            send_alert(event.threat_level)
        ```

    Attributes:
        config: SDK configuration
        client: HTTP client for API requests
        hooks: Event hooks for callbacks
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://web-production-b14fb.up.railway.app",
        timeout: float = 10.0,
        max_retries: int = 3,
        retry_backoff: float = 0.5,
        fail_open: bool = False,
        verify_ssl: bool = True,
        circuit_breaker: Optional[CircuitBreakerConfig] = None,
    ):
        """Initialize ToolGuard client.

        Args:
            api_key: API key for authentication (optional for now)
            base_url: Base URL for Blind AI API
            timeout: Request timeout in seconds
            max_retries: Maximum retry attempts
            retry_backoff: Backoff multiplier for retries
            fail_open: Allow on error (True) or block on error (False)
            verify_ssl: Verify SSL certificates
            circuit_breaker: Optional circuit breaker configuration for resilience

        Raises:
            ConfigurationError: If configuration is invalid
        """
        try:
            self.config = SDKConfig(
                api_key=api_key,
                base_url=base_url,
                timeout=timeout,
                max_retries=max_retries,
                retry_backoff=retry_backoff,
                fail_open=fail_open,
                verify_ssl=verify_ssl,
            )
        except ValueError as e:
            raise ConfigurationError(f"Invalid configuration: {e}") from e

        # Build headers with authentication
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "blind-ai-sdk/0.1.0",
        }
        if self.config.api_key:
            headers["Authorization"] = f"Bearer {self.config.api_key}"

        # Create HTTP client with authentication headers
        self.client = httpx.Client(
            base_url=self.config.base_url,
            timeout=self.config.timeout,
            verify=self.config.verify_ssl,
            headers=headers,
        )

        # Initialize event hooks
        self.hooks = EventHooks()

        # Initialize circuit breaker if configured
        if circuit_breaker:
            self._circuit_breaker = CircuitBreaker(circuit_breaker)
        else:
            self._circuit_breaker = None
        
        # Thread-local storage for session context
        self._local = threading.local()

    @property
    def circuit_breaker(self) -> Optional[CircuitBreaker]:
        """Get circuit breaker instance for monitoring.

        Returns:
            CircuitBreaker instance or None if not configured

        Example:
            ```python
            guard = ToolGuard(circuit_breaker=CircuitBreakerConfig())
            print(f"Circuit state: {guard.circuit_breaker.state}")
            print(f"Health: {guard.circuit_breaker.health}")
            ```
        """
        return self._circuit_breaker

    # Event hook decorators
    def on_block(self, handler: Callable[[SecurityEvent], None]) -> Callable:
        """Register a handler for blocked requests.

        Args:
            handler: Callback function that receives SecurityEvent

        Returns:
            The handler (for use as decorator)

        Example:
            ```python
            @guard.on_block
            def handle_blocked(event):
                send_security_alert(event.threat_level, event.threats_detected)
            ```
        """
        return self.hooks.on_block(handler)

    def on_challenge(self, handler: Callable[[SecurityEvent], Optional[bool]]) -> Callable:
        """Register a handler for challenged requests.

        Challenge handlers can return True to approve or False to deny.

        Args:
            handler: Callback function that receives SecurityEvent

        Returns:
            The handler (for use as decorator)

        Example:
            ```python
            @guard.on_challenge
            def handle_challenge(event):
                return get_user_approval(event.text)
            ```
        """
        return self.hooks.on_challenge(handler)

    def on_allow(self, handler: Callable[[SecurityEvent], None]) -> Callable:
        """Register a handler for allowed requests.

        Args:
            handler: Callback function that receives SecurityEvent

        Returns:
            The handler (for use as decorator)

        Example:
            ```python
            @guard.on_allow
            def handle_allow(event):
                log_access(event.user_id, event.tool_name)
            ```
        """
        return self.hooks.on_allow(handler)

    def on_error(self, handler: Callable[[SecurityEvent], None]) -> Callable:
        """Register a handler for errors.

        Args:
            handler: Callback function that receives SecurityEvent

        Returns:
            The handler (for use as decorator)

        Example:
            ```python
            @guard.on_error
            def handle_error(event):
                log_error(event.error)
            ```
        """
        return self.hooks.on_error(handler)

    # Session/Context Management
    @contextmanager
    def session(self, session_id: Optional[str] = None) -> Generator[str, None, None]:
        """Context manager for automatic session tracking.
        
        All checks within this context automatically use the session ID
        for multi-turn conversation tracking and chain pattern detection.
        
        Args:
            session_id: Optional session ID (auto-generated if not provided)
            
        Yields:
            The session ID being used
            
        Example:
            ```python
            with guard.session() as session_id:
                # All checks automatically use this session
                result1 = guard.check("query 1")  # Uses session_id
                result2 = guard.check("query 2")  # Uses same session_id
                
            # Or with explicit session ID
            with guard.session("user-123-conversation") as sid:
                guard.check("SELECT * FROM users")
            ```
        """
        sid = session_id or str(uuid.uuid4())
        old_session = getattr(self._local, 'session_id', None)
        self._local.session_id = sid
        try:
            yield sid
        finally:
            self._local.session_id = old_session
    
    @contextmanager
    def context(
        self,
        context_id: Optional[str] = None,
        user: Optional[UserContext] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> Generator["SessionContext", None, None]:
        """Context manager for full request context.
        
        Sets session ID, user context, and metadata for all checks within the block.
        
        Args:
            context_id: Optional context/session ID (auto-generated if not provided)
            user: Optional user context for RBAC
            metadata: Optional metadata to include with all checks
            
        Yields:
            SessionContext object with the active context details
            
        Example:
            ```python
            user = UserContext(user_id="user-123", roles=["analyst"])
            
            with guard.context(user=user, metadata={"source": "web"}) as ctx:
                print(f"Session: {ctx.session_id}")
                
                # All checks include user and metadata automatically
                guard.check("SELECT * FROM users")
                guard.check("DELETE FROM logs")
            ```
        """
        ctx = SessionContext(
            session_id=context_id or str(uuid.uuid4()),
            user=user,
            metadata=metadata or {},
        )
        
        # Save old context
        old_session = getattr(self._local, 'session_id', None)
        old_user = getattr(self._local, 'user', None)
        old_metadata = getattr(self._local, 'metadata', None)
        
        # Set new context
        self._local.session_id = ctx.session_id
        self._local.user = ctx.user
        self._local.metadata = ctx.metadata
        
        try:
            yield ctx
        finally:
            # Restore old context
            self._local.session_id = old_session
            self._local.user = old_user
            self._local.metadata = old_metadata
    
    def _get_effective_context(
        self,
        context_id: Optional[str],
        user: Optional[UserContext],
        metadata: Optional[dict[str, Any]],
    ) -> tuple[Optional[str], Optional[UserContext], dict[str, Any]]:
        """Get effective context by merging explicit args with thread-local context.
        
        Explicit arguments take precedence over thread-local context.
        """
        effective_context_id = context_id or getattr(self._local, 'session_id', None)
        effective_user = user or getattr(self._local, 'user', None)
        
        # Merge metadata (thread-local as base, explicit overwrites)
        effective_metadata = dict(getattr(self._local, 'metadata', None) or {})
        if metadata:
            effective_metadata.update(metadata)
        
        return effective_context_id, effective_user, effective_metadata

    def check(
        self,
        text: str,
        context_id: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None,
        user: Optional[UserContext] = None,
    ) -> ProtectionResult:
        """Check text for threats.

        Args:
            text: Text to check
            context_id: Optional context ID for multi-turn tracking
                       (uses session context if within guard.session() or guard.context())
            metadata: Optional metadata (merged with context metadata if within guard.context())
            user: Optional user context for RBAC (uses context user if within guard.context())

        Returns:
            ProtectionResult with detection details

        Raises:
            ThreatBlockedError: If threat detected and action is BLOCK
            APIError: If API request fails
            TimeoutError: If request times out
            RetryExhaustedError: If all retries exhausted
        """
        # Get effective context (merge explicit args with thread-local context)
        effective_context_id, effective_user, effective_metadata = self._get_effective_context(
            context_id, user, metadata
        )
        
        # Prepare request
        request_data = {
            "text": text,
        }
        if effective_context_id:
            request_data["context_id"] = effective_context_id
        if effective_metadata:
            request_data["metadata"] = effective_metadata
        if effective_user:
            request_data["user"] = effective_user.to_dict()

        # Track timing for events
        start_time = time.perf_counter()

        # Dispatch before_check event
        before_event = SecurityEvent(
            event_type=EventType.BEFORE_CHECK,
            text=text,
            context_id=effective_context_id,
            user_id=effective_user.user_id if effective_user else None,
            metadata=effective_metadata,
        )
        self.hooks.dispatch(EventType.BEFORE_CHECK, before_event)

        try:
            # Make request with retries
            response_data = self._request_with_retry(
                method="POST",
                url="/v1/protect",
                json=request_data,
            )

            # Parse response
            result = ProtectionResult.from_api_response(response_data)

            # Calculate latency
            latency_ms = (time.perf_counter() - start_time) * 1000

            # Create event from result
            event = create_event_from_result(
                result=result,
                text=text,
                latency_ms=latency_ms,
                context_id=effective_context_id,
                user_id=effective_user.user_id if effective_user else None,
                metadata=effective_metadata,
            )

            # Dispatch appropriate event based on action
            if result.final_action == "block":
                self.hooks.dispatch(EventType.BLOCK, event)
                raise ThreatBlockedError(
                    message=f"Threat detected: {result.threat_level}",
                    threat_level=result.threat_level,
                    threats=result.threats_detected,
                    response=response_data,
                )
            elif result.final_action == "challenge":
                # Dispatch challenge event and check if approved
                challenge_results = self.hooks.dispatch(EventType.CHALLENGE, event)
                # If any handler returns False, treat as blocked
                if any(r is False for r in challenge_results):
                    raise ThreatBlockedError(
                        message=f"Challenge denied: {result.threat_level}",
                        threat_level=result.threat_level,
                        threats=result.threats_detected,
                        response=response_data,
                    )
            else:
                self.hooks.dispatch(EventType.ALLOW, event)

            # Dispatch after_check event
            self.hooks.dispatch(EventType.AFTER_CHECK, event)

            return result

        except ThreatBlockedError:
            # Re-raise threat blocked errors
            raise

        except Exception as e:
            # Dispatch error event
            latency_ms = (time.perf_counter() - start_time) * 1000
            error_event = create_error_event(
                error=e,
                text=text,
                context_id=effective_context_id,
                user_id=effective_user.user_id if effective_user else None,
                metadata=effective_metadata,
            )
            self.hooks.dispatch(EventType.ERROR, error_event)
            raise

    def check_batch(
        self,
        items: list[dict[str, Any]],
        fail_fast: bool = False,
        parallel: bool = True,
        on_progress: Optional[ProgressCallback] = None,
    ) -> list[ProtectionResult]:
        """Check multiple texts for threats in a batch.
        
        More efficient than calling check() multiple times, especially
        when the API supports batch processing.
        
        Args:
            items: List of check items, each containing:
                - text (required): Text to check
                - context_id (optional): Context ID for multi-turn tracking
                - metadata (optional): Additional metadata
                - user (optional): UserContext for RBAC
            fail_fast: If True, stop on first threat and raise ThreatBlockedError
            parallel: If True, process items in parallel (when not using batch API)
            on_progress: Optional callback for progress updates. Can be:
                - Simple: func(completed: int, total: int)
                - With metadata: func(completed: int, total: int, metadata: ProgressMetadata)
            
        Returns:
            List of ProtectionResult objects in same order as input
            
        Raises:
            ThreatBlockedError: If fail_fast=True and a threat is detected
            ValueError: If items list is empty or invalid
            
        Example:
            ```python
            # Check multiple inputs at once
            results = guard.check_batch([
                {"text": "SELECT * FROM users", "context_id": "session-1"},
                {"text": "DELETE FROM logs", "context_id": "session-1"},
                {"text": "DROP TABLE users"},
            ])
            
            # Process results
            for i, result in enumerate(results):
                if result.is_threat:
                    print(f"Item {i} blocked: {result.threat_level}")
                    
            # Fail fast mode - raises on first threat
            try:
                results = guard.check_batch(items, fail_fast=True)
            except ThreatBlockedError as e:
                print(f"Batch aborted: {e}")
            
            # Simple progress callback
            def on_progress(completed, total):
                print(f"{completed}/{total} checks complete")
            
            results = guard.check_batch(items, on_progress=on_progress)
            
            # Progress callback with metadata
            def on_progress_detailed(completed, total, metadata=None):
                if metadata:
                    print(f"{completed}/{total} - {metadata.threats_detected} threats, "
                          f"avg {metadata.avg_latency_ms:.1f}ms")
            
            results = guard.check_batch(items, on_progress=on_progress_detailed)
            ```
        """
        if not items:
            raise ValueError("Items list cannot be empty")
        
        # Validate items
        for i, item in enumerate(items):
            if not isinstance(item, dict):
                raise ValueError(f"Item {i} must be a dictionary")
            if "text" not in item:
                raise ValueError(f"Item {i} missing required 'text' field")
        
        # Try batch API first
        try:
            return self._check_batch_api(items, fail_fast, on_progress)
        except APIError as e:
            # If batch endpoint not available, fall back to individual checks
            if "404" in str(e) or "not found" in str(e).lower():
                logger.debug("Batch API not available, falling back to individual checks")
                return self._check_batch_fallback(items, fail_fast, parallel, on_progress)
            raise
    
    def _check_batch_api(
        self,
        items: list[dict[str, Any]],
        fail_fast: bool,
        on_progress: Optional[Callable[[int, int], None]] = None,
    ) -> list[ProtectionResult]:
        """Check batch using dedicated batch API endpoint."""
        # Build batch request
        batch_items = []
        for item in items:
            # Get effective context for each item
            effective_context_id, effective_user, effective_metadata = self._get_effective_context(
                item.get("context_id"),
                item.get("user"),
                item.get("metadata"),
            )
            
            batch_item = {"text": item["text"]}
            if effective_context_id:
                batch_item["context_id"] = effective_context_id
            if effective_metadata:
                batch_item["metadata"] = effective_metadata
            if effective_user:
                batch_item["user"] = effective_user.to_dict()
            
            batch_items.append(batch_item)
        
        request_data = {
            "items": batch_items,
            "fail_fast": fail_fast,
        }
        
        start_time = time.perf_counter()
        
        try:
            response_data = self._request_with_retry(
                method="POST",
                url="/v1/protect/batch",
                json=request_data,
            )
            
            latency_ms = (time.perf_counter() - start_time) * 1000
            
            # Parse results
            results = []
            for i, result_data in enumerate(response_data.get("results", [])):
                result = ProtectionResult.from_api_response(result_data)
                results.append(result)
                
                # Check for threats if fail_fast
                if fail_fast and result.final_action == "block":
                    raise ThreatBlockedError(
                        message=f"Batch item {i} blocked: {result.threat_level}",
                        threat_level=result.threat_level,
                        threats=result.threats_detected,
                        response=result_data,
                    )
            
            logger.debug(f"Batch check completed: {len(results)} items in {latency_ms:.1f}ms")
            
            # Call progress callback with completion
            if on_progress:
                on_progress(len(results), len(items))
            
            return results
            
        except ThreatBlockedError:
            raise
        except Exception as e:
            logger.error(f"Batch API check failed: {e}")
            raise
    
    def _check_batch_fallback(
        self,
        items: list[dict[str, Any]],
        fail_fast: bool,
        parallel: bool,
        on_progress: Optional[ProgressCallback] = None,
    ) -> list[ProtectionResult]:
        """Fallback: check items individually (optionally in parallel)."""
        import concurrent.futures
        import inspect
        
        results: list[Optional[ProtectionResult]] = [None] * len(items)
        errors: list[Optional[Exception]] = [None] * len(items)
        completed_count = 0
        total = len(items)
        progress_lock = threading.Lock()
        
        # Track metadata for progress reporting
        threats_detected = 0
        blocked_count = 0
        total_latency_ms = 0.0
        errors_count = 0
        start_time = time.perf_counter()
        
        # Check if callback accepts metadata parameter
        accepts_metadata = False
        if on_progress:
            try:
                sig = inspect.signature(on_progress)
                accepts_metadata = len(sig.parameters) >= 3
            except (ValueError, TypeError):
                pass
        
        def build_metadata(current_index: Optional[int] = None) -> ProgressMetadata:
            """Build current progress metadata."""
            current_preview = None
            if current_index is not None and current_index < len(items):
                text = items[current_index].get("text", "")
                current_preview = text[:50] + "..." if len(text) > 50 else text
            
            return ProgressMetadata(
                threats_detected=threats_detected,
                blocked_count=blocked_count,
                avg_latency_ms=total_latency_ms / completed_count if completed_count > 0 else 0.0,
                total_latency_ms=total_latency_ms,
                current_item_preview=current_preview,
                current_index=current_index,
                errors_count=errors_count,
            )
        
        def report_progress(current_index: Optional[int] = None) -> None:
            """Thread-safe progress reporting with metadata."""
            if not on_progress:
                return
            
            with progress_lock:
                if accepts_metadata:
                    metadata = build_metadata(current_index)
                    on_progress(completed_count, total, metadata)
                else:
                    on_progress(completed_count, total)
        
        def check_item(index: int, item: dict) -> tuple[int, ProtectionResult, float]:
            item_start = time.perf_counter()
            result = self.check(
                text=item["text"],
                context_id=item.get("context_id"),
                metadata=item.get("metadata"),
                user=item.get("user"),
            )
            item_latency = (time.perf_counter() - item_start) * 1000
            return index, result, item_latency
        
        if parallel and len(items) > 1:
            # Parallel execution using thread pool
            with concurrent.futures.ThreadPoolExecutor(max_workers=min(len(items), 10)) as executor:
                futures = {
                    executor.submit(check_item, i, item): i
                    for i, item in enumerate(items)
                }
                
                for future in concurrent.futures.as_completed(futures):
                    try:
                        index, result, item_latency = future.result()
                        results[index] = result
                        
                        # Update stats
                        with progress_lock:
                            completed_count += 1
                            total_latency_ms += item_latency
                            if result.is_threat:
                                threats_detected += 1
                            if result.final_action == "block":
                                blocked_count += 1
                        
                        report_progress(index)
                        
                        if fail_fast and result.final_action == "block":
                            # Cancel remaining futures
                            for f in futures:
                                f.cancel()
                            raise ThreatBlockedError(
                                message=f"Batch item {index} blocked: {result.threat_level}",
                                threat_level=result.threat_level,
                                threats=result.threats_detected,
                                response={},
                            )
                    except ThreatBlockedError:
                        raise
                    except Exception as e:
                        index = futures[future]
                        errors[index] = e
                        # Still count as completed for progress
                        with progress_lock:
                            completed_count += 1
                            errors_count += 1
                        report_progress(index)
                        if fail_fast:
                            raise
        else:
            # Sequential execution
            for i, item in enumerate(items):
                try:
                    _, result, item_latency = check_item(i, item)
                    results[i] = result
                    
                    # Update stats
                    completed_count += 1
                    total_latency_ms += item_latency
                    if result.is_threat:
                        threats_detected += 1
                    if result.final_action == "block":
                        blocked_count += 1
                    
                    # Report progress with metadata
                    if on_progress:
                        if accepts_metadata:
                            metadata = build_metadata(i)
                            on_progress(completed_count, total, metadata)
                        else:
                            on_progress(completed_count, total)
                    
                    if fail_fast and result.final_action == "block":
                        raise ThreatBlockedError(
                            message=f"Batch item {i} blocked: {result.threat_level}",
                            threat_level=result.threat_level,
                            threats=result.threats_detected,
                            response={},
                        )
                except ThreatBlockedError:
                    raise
                except Exception as e:
                    errors[i] = e
                    # Still count as completed for progress
                    completed_count += 1
                    errors_count += 1
                    if on_progress:
                        if accepts_metadata:
                            metadata = build_metadata(i)
                            on_progress(completed_count, total, metadata)
                        else:
                            on_progress(completed_count, total)
                    if fail_fast:
                        raise
        
        # Check for any errors
        for i, error in enumerate(errors):
            if error is not None:
                logger.warning(f"Batch item {i} failed: {error}")
        
        # Filter out None results (shouldn't happen unless there were errors)
        return [r for r in results if r is not None]

    def protect(
        self,
        func: Callable = None,
        *,
        context_id: Optional[str] = None,
        param: Optional[str] = None,
    ):
        """Decorator to protect a function from threats.

        Can be used with or without arguments:
        - @guard.protect
        - @guard.protect(context_id="session-123")
        - @guard.protect(param="query")

        Args:
            func: Function to protect
            context_id: Optional context ID
            param: Specific parameter name to check (if not specified, uses first string arg)

        Returns:
            Decorated function

        Example:
            ```python
            @guard.protect
            def execute_sql(query: str):
                return db.execute(query)

            @guard.protect(context_id="session-123")
            def call_api(endpoint: str):
                return requests.get(endpoint)

            # Specify which parameter to check
            @guard.protect(param="query")
            def process_user(user_id: str, query: str):
                return db.execute(query)
            ```
        """

        def decorator(f: Callable) -> Callable:
            @functools.wraps(f)
            def wrapper(*args, **kwargs):
                # Extract text from arguments
                text = None

                if param:
                    # Use specified parameter
                    if param in kwargs:
                        text = kwargs[param]
                    else:
                        # Try to find in args using function signature
                        import inspect

                        sig = inspect.signature(f)
                        param_names = list(sig.parameters.keys())
                        if param in param_names:
                            param_index = param_names.index(param)
                            if param_index < len(args):
                                text = args[param_index]

                    if text is None:
                        raise ValueError(f"Parameter '{param}' not found in function call")
                else:
                    # Auto-detect: use first string argument
                    for arg in args:
                        if isinstance(arg, str):
                            text = arg
                            break
                    if text is None:
                        for value in kwargs.values():
                            if isinstance(value, str):
                                text = value
                                break

                if text is None:
                    raise ValueError("No text argument found to protect")

                # Check for threats
                self.check(text, context_id=context_id)

                # If no threat, call original function
                return f(*args, **kwargs)

            return wrapper

        # Handle both @protect and @protect()
        if func is None:
            return decorator
        else:
            return decorator(func)

    def call_tool(
        self,
        tool_func: Callable,
        *args,
        context_id: Optional[str] = None,
        **kwargs,
    ) -> Any:
        """Call a tool with protection.

        Alternative to decorator approach for dynamic tool calls.

        Args:
            tool_func: Tool function to call
            *args: Arguments to pass to tool
            context_id: Optional context ID
            **kwargs: Keyword arguments to pass to tool

        Returns:
            Result from tool function

        Raises:
            ThreatBlockedError: If threat detected
            ValueError: If no text argument found

        Example:
            ```python
            result = guard.call_tool(
                execute_sql,
                "SELECT * FROM users",
                context_id="session-123"
            )
            ```
        """
        # Extract text from arguments
        text = None
        for arg in args:
            if isinstance(arg, str):
                text = arg
                break
        if text is None:
            for value in kwargs.values():
                if isinstance(value, str):
                    text = value
                    break

        if text is None:
            raise ValueError("No text argument found to protect")

        # Check for threats
        self.check(text, context_id=context_id)

        # If no threat, call tool
        return tool_func(*args, **kwargs)

    # Tool Registry Methods (Layer 2)
    def register_tool(
        self,
        name: str,
        trust_level: str,
        tool_type: str,
        description: str = "",
        allowed_domains: Optional[list[str]] = None,
        allowed_roles: Optional[list[str]] = None,
        rate_limit_per_minute: Optional[int] = None,
        require_approval: bool = False,
        metadata: Optional[dict] = None,
    ) -> dict:
        """Register a tool with security metadata.

        This enables tool-aware policy rules and authorization checks.

        Args:
            name: Unique tool identifier
            trust_level: Trust level (HIGH, MEDIUM, or LOW)
            tool_type: Tool type (DATABASE, API, EMAIL, COMMUNICATION, FILE, COMMAND, etc.)
            description: Human-readable description
            allowed_domains: List of allowed domains for external calls
            allowed_roles: List of roles permitted to use this tool
            rate_limit_per_minute: Maximum calls per minute
            require_approval: Whether calls require human approval
            metadata: Additional custom metadata

        Returns:
            Registered tool metadata

        Raises:
            APIError: If registration fails
            ConfigurationError: If parameters are invalid

        Example:
            ```python
            guard.register_tool(
                name="send_email",
                trust_level="LOW",
                tool_type="EMAIL",
                description="Send email to external recipients",
                allowed_domains=["company.com", "partner.com"],
                allowed_roles=["user", "admin"],
                rate_limit_per_minute=100
            )
            ```
        """
        payload = {
            "name": name,
            "trust_level": trust_level.upper(),
            "tool_type": tool_type.upper(),
            "description": description,
            "allowed_domains": allowed_domains or [],
            "allowed_roles": allowed_roles or [],
            "rate_limit_per_minute": rate_limit_per_minute,
            "require_approval": require_approval,
            "metadata": metadata or {},
        }

        try:
            response = self._request_with_retry(
                "POST", "/v1/tools/register", json=payload
            )
            return response
        except Exception as e:
            if self.config.fail_open:
                # Log error but don't raise
                print(f"Warning: Tool registration failed: {e}")
                return {"name": name, "status": "failed"}
            raise

    def get_tool(self, tool_name: str) -> Optional[dict]:
        """Get tool metadata by name.

        Args:
            tool_name: Tool identifier

        Returns:
            Tool metadata if found, None otherwise

        Raises:
            APIError: If request fails

        Example:
            ```python
            tool = guard.get_tool("send_email")
            if tool and tool["trust_level"] == "LOW":
                print("Low trust tool - extra validation required")
            ```
        """
        try:
            response = self._request_with_retry("GET", f"/v1/tools/{tool_name}")
            return response
        except APIError as e:
            if "404" in str(e):
                return None
            raise

    def list_tools(self) -> list[dict]:
        """List all registered tools.

        Returns:
            List of tool metadata

        Raises:
            APIError: If request fails

        Example:
            ```python
            tools = guard.list_tools()
            for tool in tools:
                print(f"{tool['name']}: {tool['trust_level']}")
            ```
        """
        response = self._request_with_retry("GET", "/v1/tools")
        return response.get("tools", [])

    def list_tools_by_trust_level(self, trust_level: str) -> list[dict]:
        """List tools by trust level.

        Args:
            trust_level: Trust level filter (HIGH, MEDIUM, or LOW)

        Returns:
            List of matching tools

        Raises:
            APIError: If request fails

        Example:
            ```python
            low_trust_tools = guard.list_tools_by_trust_level("LOW")
            for tool in low_trust_tools:
                print(f"Low trust: {tool['name']}")
            ```
        """
        response = self._request_with_retry(
            "GET", f"/v1/tools/by-trust-level/{trust_level.upper()}"
        )
        return response.get("tools", [])

    def list_tools_by_type(self, tool_type: str) -> list[dict]:
        """List tools by type.

        Args:
            tool_type: Tool type filter (DATABASE, API, EMAIL, etc.)

        Returns:
            List of matching tools

        Raises:
            APIError: If request fails

        Example:
            ```python
            db_tools = guard.list_tools_by_type("DATABASE")
            for tool in db_tools:
                print(f"Database tool: {tool['name']}")
            ```
        """
        response = self._request_with_retry(
            "GET", f"/v1/tools/by-type/{tool_type.upper()}"
        )
        return response.get("tools", [])

    def delete_tool(self, tool_name: str) -> bool:
        """Delete a tool from the registry.

        Args:
            tool_name: Tool identifier

        Returns:
            True if deleted, False if not found

        Raises:
            APIError: If request fails

        Example:
            ```python
            deleted = guard.delete_tool("deprecated_tool")
            if deleted:
                print("Tool removed from registry")
            ```
        """
        try:
            self._request_with_retry("DELETE", f"/v1/tools/{tool_name}")
            return True
        except APIError as e:
            if "404" in str(e):
                return False
            raise

    def _request_with_retry(
        self,
        method: str,
        url: str,
        **kwargs,
    ) -> dict:
        """Make HTTP request with retry logic and circuit breaker.

        Args:
            method: HTTP method
            url: URL path
            **kwargs: Additional request arguments

        Returns:
            Response JSON data

        Raises:
            APIError: If request fails
            TimeoutError: If request times out
            RetryExhaustedError: If all retries exhausted
            CircuitBreakerOpen: If circuit breaker is open
        """
        # If circuit breaker is configured, use it
        if self._circuit_breaker:
            # Define fallback for fail_open mode
            def fallback(error: Exception) -> dict:
                return {
                    "is_threat": False,
                    "threat_level": "none",
                    "final_action": "allow",
                    "confidence": 0.0,
                    "threats_detected": [],
                    "processing_time_ms": 0.0,
                    "metadata": {
                        "error": str(error),
                        "fail_mode": "circuit_breaker",
                        "circuit_state": self._circuit_breaker.state.value,
                    },
                }

            return self._circuit_breaker.execute_with_fallback(
                lambda: self._do_request_with_retry(method, url, **kwargs),
                fallback=fallback if self.config.fail_open else None,
            )
        else:
            return self._do_request_with_retry(method, url, **kwargs)

    def _do_request_with_retry(
        self,
        method: str,
        url: str,
        **kwargs,
    ) -> dict:
        """Internal method to make HTTP request with retry logic.

        Args:
            method: HTTP method
            url: URL path
            **kwargs: Additional request arguments

        Returns:
            Response JSON data

        Raises:
            APIError: If request fails
            TimeoutError: If request times out
            RetryExhaustedError: If all retries exhausted
        """
        last_error = None
        attempts = 0

        for attempt in range(self.config.max_retries + 1):
            attempts = attempt + 1

            try:
                response = self.client.request(method, url, **kwargs)
                response.raise_for_status()
                return response.json()

            except httpx.TimeoutException as e:
                last_error = e
                if attempt == self.config.max_retries:
                    if self.config.fail_open:
                        # Return safe default
                        return {
                            "is_threat": False,
                            "threat_level": "none",
                            "final_action": "allow",
                            "confidence": 0.0,
                            "threats_detected": [],
                            "processing_time_ms": 0.0,
                            "metadata": {"error": "timeout", "fail_mode": "open"},
                        }
                    raise TimeoutError("Request timed out") from e

            except httpx.HTTPStatusError as e:
                last_error = e
                if attempt == self.config.max_retries:
                    if self.config.fail_open and e.response.status_code >= 500:
                        # Return safe default for server errors
                        return {
                            "is_threat": False,
                            "threat_level": "none",
                            "final_action": "allow",
                            "confidence": 0.0,
                            "threats_detected": [],
                            "processing_time_ms": 0.0,
                            "metadata": {
                                "error": f"HTTP {e.response.status_code}",
                                "fail_mode": "open",
                            },
                        }
                    raise APIError(
                        message=f"API request failed: {e.response.status_code}",
                        status_code=e.response.status_code,
                        response=e.response.json() if e.response.text else None,
                    ) from e

            except httpx.RequestError as e:
                last_error = e
                if attempt == self.config.max_retries:
                    if self.config.fail_open:
                        # Return safe default
                        return {
                            "is_threat": False,
                            "threat_level": "none",
                            "final_action": "allow",
                            "confidence": 0.0,
                            "threats_detected": [],
                            "processing_time_ms": 0.0,
                            "metadata": {"error": str(e), "fail_mode": "open"},
                        }
                    raise APIError(f"Request failed: {e}") from e

            # Exponential backoff
            if attempt < self.config.max_retries:
                sleep_time = self.config.retry_backoff * (2**attempt)
                time.sleep(sleep_time)

        # Should not reach here, but handle gracefully
        raise RetryExhaustedError(
            message=f"All {attempts} retry attempts exhausted",
            attempts=attempts,
            last_error=last_error,
        )

    def close(self):
        """Close HTTP client and cleanup resources.

        Important: Always call close() when done or use context manager.

        Example:
            ```python
            # Manual cleanup
            guard = ToolGuard()
            try:
                guard.check("some text")
            finally:
                guard.close()

            # Better: use context manager
            with ToolGuard() as guard:
                guard.check("some text")
            ```
        """
        if hasattr(self, 'client') and self.client:
            self.client.close()
            self._closed = True

    def __enter__(self):
        """Context manager entry."""
        self._closed = False
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

    def __del__(self):
        """Destructor - warn if client not properly closed."""
        if hasattr(self, '_closed') and not self._closed:
            import warnings
            warnings.warn(
                "ToolGuard client was not properly closed. "
                "Use 'with ToolGuard() as guard:' or call guard.close()",
                ResourceWarning,
                stacklevel=2
            )
        if hasattr(self, 'client'):
            try:
                self.client.close()
            except Exception:
                pass
