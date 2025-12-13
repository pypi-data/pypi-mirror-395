"""FastAPI application for Blind AI threat detection API.

Provides REST API endpoints for real-time threat detection.
"""

import os
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from redis import Redis

from blind_ai import __version__

from ..core.models import OrchestrationConfig
from ..core.orchestrator import DetectionOrchestrator
from ..core.registry import ToolRegistry
from .models import ErrorResponse, HealthResponse
from .routes import protect, signup, tools

# Application state
app_state = {
    "start_time": time.time(),
    "orchestrator": None,
    "tool_registry": None,
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager.

    Handles startup and shutdown events.
    """
    # Startup: Initialize orchestrator
    config = OrchestrationConfig(
        enable_static=True,
        enable_ml=True,
        enable_policy=True,
        parallel_execution=True,
        fail_open=False,  # Fail closed for security
        timeout_ms=50,
    )
    app_state["orchestrator"] = DetectionOrchestrator(config=config)
    app_state["start_time"] = time.time()

    # Initialize tool registry (Redis is optional)
    redis_url = os.getenv("REDIS_URL")  # Railway provides this
    redis_host = os.getenv("REDIS_HOST", "localhost")
    redis_port = int(os.getenv("REDIS_PORT", "6379"))
    redis_db = int(os.getenv("REDIS_DB", "0"))

    try:
        if redis_url:
            # Railway-style Redis URL
            redis_client = Redis.from_url(redis_url, decode_responses=True)
        else:
            redis_client = Redis(
                host=redis_host, port=redis_port, db=redis_db, decode_responses=True
            )
        # Test connection
        redis_client.ping()
        app_state["tool_registry"] = ToolRegistry(redis_client)
        tools.set_registry(app_state["tool_registry"])
        print("✓ Redis connected")
    except Exception as e:
        # Redis is optional - app works without it
        print(f"⚠ Redis not available ({e}), tool registry disabled")
        app_state["tool_registry"] = None

    yield

    # Shutdown: Cleanup resources
    if app_state["orchestrator"]:
        app_state["orchestrator"].shutdown()


# Create FastAPI app
app = FastAPI(
    title="Blind AI API",
    description="Runtime security API for AI agents - detect threats in real-time",
    version=__version__,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error="http_error",
            message=exc.detail,
            detail={"status_code": exc.status_code},
        ).model_dump(),
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error="internal_error",
            message="An internal error occurred",
            detail={"exception": str(exc)},
        ).model_dump(),
    )


# Health check endpoint
@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint.

    Returns:
        Health status, version, and uptime
    """
    uptime = time.time() - app_state["start_time"]
    return HealthResponse(
        status="healthy",
        version=__version__,
        uptime_seconds=uptime,
    )


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Blind AI API",
        "version": __version__,
        "description": "Runtime security for AI agents",
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "protect": "/v1/protect",
        },
    }


# Include routers
app.include_router(protect.router, prefix="/v1", tags=["Detection"])
app.include_router(signup.router, tags=["Signup"])
app.include_router(tools.router)


# Get orchestrator
def get_orchestrator() -> DetectionOrchestrator:
    """Get the orchestrator instance.

    Returns:
        DetectionOrchestrator instance

    Raises:
        HTTPException: If orchestrator not initialized
    """
    orchestrator = app_state.get("orchestrator")
    if not orchestrator:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Detection service not available",
        )
    return orchestrator
