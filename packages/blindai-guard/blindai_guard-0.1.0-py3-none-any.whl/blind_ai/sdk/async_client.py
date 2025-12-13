"""Async Blind AI SDK client implementation."""

import asyncio
import functools
import logging
import time
from typing import Any, Callable, Optional, Union

import httpx

logger = logging.getLogger(__name__)

from ..core.rbac import UserContext
from .circuit_breaker import CircuitBreaker, CircuitBreakerConfig, CircuitBreakerOpen
from .exceptions import (
    APIError,
    ConfigurationError,
    RetryExhaustedError,
    ThreatBlockedError,
    TimeoutError,
)
from .models import ProtectionResult, SDKConfig


class AsyncToolGuard:
    """Async Blind AI SDK client for protecting tool calls.

    Async version of ToolGuard for high-performance async applications.

    Example:
        ```python
        guard = AsyncToolGuard(api_key="...", base_url="http://localhost:8000")

        # Protect an async function
        @guard.protect
        async def fetch_data(query: str):
            return await db.execute(query)

        # Use with context manager
        async with AsyncToolGuard(...) as guard:
            result = await guard.check("DROP TABLE users")
        ```

    Attributes:
        config: SDK configuration
        client: Async HTTP client for API requests
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "http://localhost:8000",
        timeout: float = 10.0,
        max_retries: int = 3,
        retry_backoff: float = 0.5,
        fail_open: bool = False,
        verify_ssl: bool = True,
        max_connections: int = 100,
        max_keepalive_connections: int = 20,
        keepalive_expiry: float = 5.0,
        circuit_breaker: Optional[CircuitBreakerConfig] = None,
    ):
        """Initialize AsyncToolGuard client.

        Args:
            api_key: API key for authentication (optional for now)
            base_url: Base URL for Blind AI API
            timeout: Request timeout in seconds
            max_retries: Maximum retry attempts
            retry_backoff: Backoff multiplier for retries
            fail_open: Allow on error (True) or block on error (False)
            verify_ssl: Verify SSL certificates
            max_connections: Maximum number of concurrent connections
            max_keepalive_connections: Maximum number of keepalive connections
            keepalive_expiry: Keepalive connection expiry in seconds
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

        # Configure connection pooling for high-performance async operations
        limits = httpx.Limits(
            max_connections=max_connections,
            max_keepalive_connections=max_keepalive_connections,
            keepalive_expiry=keepalive_expiry,
        )

        # Build headers with authentication
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "blind-ai-sdk/0.1.0",
        }
        if self.config.api_key:
            headers["Authorization"] = f"Bearer {self.config.api_key}"

        # Create async HTTP client with connection pooling and authentication
        self.client = httpx.AsyncClient(
            base_url=self.config.base_url,
            timeout=self.config.timeout,
            verify=self.config.verify_ssl,
            limits=limits,
            headers=headers,
        )

        # Initialize circuit breaker if configured
        if circuit_breaker:
            self._circuit_breaker = CircuitBreaker(circuit_breaker)
        else:
            self._circuit_breaker = None

    @property
    def circuit_breaker(self) -> Optional[CircuitBreaker]:
        """Get circuit breaker instance for monitoring.

        Returns:
            CircuitBreaker instance or None if not configured

        Example:
            ```python
            guard = AsyncToolGuard(circuit_breaker=CircuitBreakerConfig())
            print(f"Circuit state: {guard.circuit_breaker.state}")
            print(f"Health: {guard.circuit_breaker.health}")
            ```
        """
        return self._circuit_breaker

    async def check(
        self,
        text: str,
        context_id: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None,
        user: Optional[UserContext] = None,
    ) -> ProtectionResult:
        """Check text for threats asynchronously.

        Args:
            text: Text to check
            context_id: Optional context ID for multi-turn tracking
            metadata: Optional metadata
            user: Optional user context for RBAC

        Returns:
            ProtectionResult with detection details

        Raises:
            ThreatBlockedError: If threat detected and action is BLOCK
            APIError: If API request fails
            TimeoutError: If request times out
            RetryExhaustedError: If all retries exhausted
        """
        # Prepare request
        request_data = {
            "text": text,
        }
        if context_id:
            request_data["context_id"] = context_id
        if metadata:
            request_data["metadata"] = metadata
        if user:
            request_data["user"] = user.to_dict()

        # Make request with retries
        response_data = await self._request_with_retry(
            method="POST",
            url="/v1/protect",
            json=request_data,
        )

        # Parse response
        result = ProtectionResult.from_api_response(response_data)

        # Handle blocking
        if result.final_action == "block":
            raise ThreatBlockedError(
                message=f"Threat detected: {result.threat_level}",
                threat_level=result.threat_level,
                threats=result.threats_detected,
                response=response_data,
            )

        return result

    async def check_batch(
        self,
        items: list[dict[str, Any]],
        fail_fast: bool = False,
        max_concurrency: int = 10,
        on_progress: Optional[Union[Callable[[int, int], None], Callable[[int, int], Any]]] = None,
    ) -> list[ProtectionResult]:
        """Check multiple texts for threats in a batch asynchronously.
        
        More efficient than calling check() multiple times. Uses concurrent
        async requests for maximum throughput.
        
        Args:
            items: List of check items, each containing:
                - text (required): Text to check
                - context_id (optional): Context ID for multi-turn tracking
                - metadata (optional): Additional metadata
                - user (optional): UserContext for RBAC
            fail_fast: If True, stop on first threat and raise ThreatBlockedError
            max_concurrency: Maximum number of concurrent checks (default 10)
            on_progress: Optional callback function(completed, total) for progress updates.
                        Can be sync or async function.
            
        Returns:
            List of ProtectionResult objects in same order as input
            
        Raises:
            ThreatBlockedError: If fail_fast=True and a threat is detected
            ValueError: If items list is empty or invalid
            
        Example:
            ```python
            # Check multiple inputs concurrently
            results = await guard.check_batch([
                {"text": "SELECT * FROM users", "context_id": "session-1"},
                {"text": "DELETE FROM logs", "context_id": "session-1"},
                {"text": "DROP TABLE users"},
            ])
            
            # Process results
            for i, result in enumerate(results):
                if result.is_threat:
                    print(f"Item {i} blocked: {result.threat_level}")
            
            # With progress callback (sync)
            def on_progress(completed, total):
                print(f"{completed}/{total} complete")
            
            results = await guard.check_batch(items, on_progress=on_progress)
            
            # With async progress callback
            async def async_progress(completed, total):
                await update_progress_bar(completed, total)
            
            results = await guard.check_batch(items, on_progress=async_progress)
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
            return await self._check_batch_api(items, fail_fast, on_progress)
        except APIError as e:
            # If batch endpoint not available, fall back to concurrent checks
            if "404" in str(e) or "not found" in str(e).lower():
                logger.debug("Batch API not available, falling back to concurrent checks")
                return await self._check_batch_concurrent(items, fail_fast, max_concurrency, on_progress)
            raise
    
    async def _call_progress(
        self,
        on_progress: Optional[Union[Callable[[int, int], None], Callable[[int, int], Any]]],
        completed: int,
        total: int,
    ) -> None:
        """Call progress callback, handling both sync and async callbacks."""
        if on_progress is None:
            return
        
        result = on_progress(completed, total)
        # If it's a coroutine, await it
        if asyncio.iscoroutine(result):
            await result
    
    async def _check_batch_api(
        self,
        items: list[dict[str, Any]],
        fail_fast: bool,
        on_progress: Optional[Union[Callable[[int, int], None], Callable[[int, int], Any]]] = None,
    ) -> list[ProtectionResult]:
        """Check batch using dedicated batch API endpoint."""
        batch_items = [
            {
                "text": item["text"],
                **({"context_id": item["context_id"]} if "context_id" in item else {}),
                **({"metadata": item["metadata"]} if "metadata" in item else {}),
                **({"user": item["user"].to_dict()} if "user" in item else {}),
            }
            for item in items
        ]
        
        request_data = {
            "items": batch_items,
            "fail_fast": fail_fast,
        }
        
        start_time = time.perf_counter()
        
        response_data = await self._request_with_retry(
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
            
            if fail_fast and result.final_action == "block":
                raise ThreatBlockedError(
                    message=f"Batch item {i} blocked: {result.threat_level}",
                    threat_level=result.threat_level,
                    threats=result.threats_detected,
                    response=result_data,
                )
        
        logger.debug(f"Async batch check completed: {len(results)} items in {latency_ms:.1f}ms")
        
        # Call progress callback with completion
        await self._call_progress(on_progress, len(results), len(items))
        
        return results
    
    async def _check_batch_concurrent(
        self,
        items: list[dict[str, Any]],
        fail_fast: bool,
        max_concurrency: int,
        on_progress: Optional[Union[Callable[[int, int], None], Callable[[int, int], Any]]] = None,
    ) -> list[ProtectionResult]:
        """Fallback: check items concurrently using semaphore."""
        semaphore = asyncio.Semaphore(max_concurrency)
        results: list[Optional[ProtectionResult]] = [None] * len(items)
        cancel_event = asyncio.Event() if fail_fast else None
        completed_count = 0
        total = len(items)
        progress_lock = asyncio.Lock()
        
        async def report_progress() -> None:
            """Report progress with lock."""
            nonlocal completed_count
            async with progress_lock:
                completed_count += 1
                await self._call_progress(on_progress, completed_count, total)
        
        async def check_item(index: int, item: dict) -> None:
            if cancel_event and cancel_event.is_set():
                return
            
            async with semaphore:
                if cancel_event and cancel_event.is_set():
                    return
                
                try:
                    result = await self.check(
                        text=item["text"],
                        context_id=item.get("context_id"),
                        metadata=item.get("metadata"),
                        user=item.get("user"),
                    )
                    results[index] = result
                    
                    # Report progress
                    await report_progress()
                    
                    if fail_fast and result.final_action == "block":
                        if cancel_event:
                            cancel_event.set()
                        raise ThreatBlockedError(
                            message=f"Batch item {index} blocked: {result.threat_level}",
                            threat_level=result.threat_level,
                            threats=result.threats_detected,
                            response={},
                        )
                except ThreatBlockedError:
                    raise
                except Exception:
                    # Still report progress on error
                    await report_progress()
                    raise
        
        # Create tasks for all items
        tasks = [
            asyncio.create_task(check_item(i, item))
            for i, item in enumerate(items)
        ]
        
        try:
            # Wait for all tasks (or until one raises)
            await asyncio.gather(*tasks, return_exceptions=not fail_fast)
        except ThreatBlockedError:
            # Cancel remaining tasks
            for task in tasks:
                task.cancel()
            raise
        
        # Filter out None results
        return [r for r in results if r is not None]

    def protect(self, func: Callable = None, *, context_id: Optional[str] = None):
        """Decorator to protect an async function from threats.

        Can be used with or without arguments:
        - @guard.protect
        - @guard.protect(context_id="session-123")

        Args:
            func: Async function to protect
            context_id: Optional context ID

        Returns:
            Decorated async function

        Raises:
            TypeError: If decorated function is not async

        Example:
            ```python
            @guard.protect
            async def fetch_data(query: str):
                return await db.execute(query)

            @guard.protect(context_id="session-123")
            async def call_api(endpoint: str):
                async with httpx.AsyncClient() as client:
                    return await client.get(endpoint)
            ```
        """

        def decorator(f: Callable) -> Callable:
            # Check if function is async
            if not asyncio.iscoroutinefunction(f):
                raise TypeError(
                    f"{f.__name__} must be an async function. "
                    f"Use @guard.protect with async def, or use sync ToolGuard for sync functions."
                )

            @functools.wraps(f)
            async def wrapper(*args, **kwargs):
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
                await self.check(text, context_id=context_id)

                # If no threat, call original function
                return await f(*args, **kwargs)

            return wrapper

        # Handle both @protect and @protect()
        if func is None:
            return decorator
        else:
            return decorator(func)

    async def call_tool(
        self,
        tool_func: Callable,
        *args,
        context_id: Optional[str] = None,
        **kwargs,
    ) -> Any:
        """Call a tool function with protection.

        Alternative to decorator approach for dynamic tool calls.
        Supports both sync and async tool functions.

        Args:
            tool_func: Tool function to call (sync or async)
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
            # Async tool
            result = await guard.call_tool(
                fetch_data,
                "SELECT * FROM users",
                context_id="session-123"
            )

            # Sync tool (will run in executor)
            result = await guard.call_tool(
                sync_function,
                "some input"
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
        await self.check(text, context_id=context_id)

        # If no threat, call tool
        # Handle both sync and async functions
        if asyncio.iscoroutinefunction(tool_func):
            # Async function - await it
            return await tool_func(*args, **kwargs)
        else:
            # Sync function - run in executor to avoid blocking
            # Use get_running_loop() instead of deprecated get_event_loop()
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(None, lambda: tool_func(*args, **kwargs))

    async def _request_with_retry(
        self,
        method: str,
        url: str,
        **kwargs,
    ) -> dict:
        """Make async HTTP request with retry logic and circuit breaker.

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

            # For async, we need to wrap the coroutine in a sync function
            # The circuit breaker will run in the same event loop
            return await self._circuit_breaker.execute_async(
                self._do_request_with_retry(method, url, **kwargs),
                fallback=fallback if self.config.fail_open else None,
            )
        else:
            return await self._do_request_with_retry(method, url, **kwargs)

    async def _do_request_with_retry(
        self,
        method: str,
        url: str,
        **kwargs,
    ) -> dict:
        """Internal method to make async HTTP request with retry logic.

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
                response = await self.client.request(method, url, **kwargs)
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
                await asyncio.sleep(sleep_time)

        # Should not reach here, but handle gracefully
        raise RetryExhaustedError(
            message=f"All {attempts} retry attempts exhausted",
            attempts=attempts,
            last_error=last_error,
        )

    async def close(self):
        """Close async HTTP client and cleanup resources."""
        await self.client.aclose()

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
