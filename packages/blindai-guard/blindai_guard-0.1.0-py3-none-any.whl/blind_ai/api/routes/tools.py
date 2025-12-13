"""Tool registry API endpoints.

Provides endpoints for registering and managing tools with security metadata.

Endpoints:
    POST /v1/tools/register - Register or update tool metadata
    GET /v1/tools/{tool_name} - Get tool metadata
    DELETE /v1/tools/{tool_name} - Delete tool
    GET /v1/tools - List all tools
    GET /v1/tools/by-trust-level/{trust_level} - List tools by trust level
    GET /v1/tools/by-type/{tool_type} - List tools by type
"""

from typing import List, Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from ...core.registry import ToolMetadata, ToolRegistry, ToolType, TrustLevel

# Create router
router = APIRouter(prefix="/v1/tools", tags=["Tool Registry"])

# Global registry instance (initialized in app startup)
registry: Optional[ToolRegistry] = None


def set_registry(tool_registry: ToolRegistry) -> None:
    """Set global tool registry instance.

    Args:
        tool_registry: Initialized tool registry

    Note:
        This should be called during app startup.
    """
    global registry
    registry = tool_registry


# Request/Response models
class ToolMetadataRequest(BaseModel):
    """Request model for tool registration."""

    name: str = Field(..., description="Unique tool identifier", min_length=1)
    trust_level: str = Field(..., description="Trust level: HIGH, MEDIUM, or LOW")
    tool_type: str = Field(..., description="Tool type: DATABASE, API, EMAIL, etc.")
    description: str = Field(default="", description="Human-readable description")
    allowed_domains: List[str] = Field(
        default_factory=list, description="Allowed domains for external calls"
    )
    allowed_roles: List[str] = Field(
        default_factory=list, description="Roles permitted to use this tool"
    )
    rate_limit_per_minute: Optional[int] = Field(
        default=None, description="Max calls per minute", gt=0
    )
    require_approval: bool = Field(
        default=False, description="Whether calls require approval"
    )
    metadata: dict = Field(default_factory=dict, description="Custom metadata")

    class Config:
        """Pydantic config."""

        json_schema_extra = {
            "example": {
                "name": "send_email",
                "trust_level": "LOW",
                "tool_type": "EMAIL",
                "description": "Send email to external recipients",
                "allowed_domains": ["company.com", "partner.com"],
                "allowed_roles": ["user", "admin"],
                "rate_limit_per_minute": 100,
                "require_approval": False,
                "metadata": {"region": "us-east-1"},
            }
        }


class ToolMetadataResponse(BaseModel):
    """Response model for tool metadata."""

    name: str
    trust_level: str
    tool_type: str
    description: str
    allowed_domains: List[str]
    allowed_roles: List[str]
    rate_limit_per_minute: Optional[int]
    require_approval: bool
    metadata: dict

    @classmethod
    def from_metadata(cls, metadata: ToolMetadata) -> "ToolMetadataResponse":
        """Create from ToolMetadata instance."""
        return cls(
            name=metadata.name,
            trust_level=metadata.trust_level.value,
            tool_type=metadata.tool_type.value,
            description=metadata.description,
            allowed_domains=metadata.allowed_domains,
            allowed_roles=metadata.allowed_roles,
            rate_limit_per_minute=metadata.rate_limit_per_minute,
            require_approval=metadata.require_approval,
            metadata=metadata.metadata,
        )


class ToolListResponse(BaseModel):
    """Response model for tool list."""

    tools: List[ToolMetadataResponse]
    count: int


# Endpoints
@router.post(
    "/register",
    response_model=ToolMetadataResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register or update tool metadata",
    description="Register a new tool or update existing tool metadata. "
    "This enables tool-aware policy rules and authorization.",
)
async def register_tool(request: ToolMetadataRequest) -> ToolMetadataResponse:
    """Register or update tool metadata.

    Args:
        request: Tool metadata to register

    Returns:
        Registered tool metadata

    Raises:
        HTTPException: If validation fails or registry unavailable
    """
    if registry is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Tool registry not initialized",
        )

    try:
        # Create ToolMetadata instance (validates enums)
        metadata = ToolMetadata(
            name=request.name,
            trust_level=TrustLevel(request.trust_level),
            tool_type=ToolType(request.tool_type),
            description=request.description,
            allowed_domains=request.allowed_domains,
            allowed_roles=request.allowed_roles,
            rate_limit_per_minute=request.rate_limit_per_minute,
            require_approval=request.require_approval,
            metadata=request.metadata,
        )

        # Register
        registry.register(metadata)

        return ToolMetadataResponse.from_metadata(metadata)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to register tool: {str(e)}",
        ) from e


@router.get(
    "/{tool_name}",
    response_model=ToolMetadataResponse,
    summary="Get tool metadata",
    description="Retrieve metadata for a registered tool.",
)
async def get_tool(tool_name: str) -> ToolMetadataResponse:
    """Get tool metadata by name.

    Args:
        tool_name: Tool identifier

    Returns:
        Tool metadata

    Raises:
        HTTPException: If tool not found or registry unavailable
    """
    if registry is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Tool registry not initialized",
        )

    metadata = registry.get(tool_name)

    if metadata is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tool '{tool_name}' not found",
        )

    return ToolMetadataResponse.from_metadata(metadata)


@router.delete(
    "/{tool_name}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete tool",
    description="Remove a tool from the registry.",
)
async def delete_tool(tool_name: str) -> None:
    """Delete tool from registry.

    Args:
        tool_name: Tool identifier

    Raises:
        HTTPException: If tool not found or registry unavailable
    """
    if registry is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Tool registry not initialized",
        )

    deleted = registry.delete(tool_name)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tool '{tool_name}' not found",
        )


@router.get(
    "",
    response_model=ToolListResponse,
    summary="List all tools",
    description="Retrieve all registered tools.",
)
async def list_tools() -> ToolListResponse:
    """List all registered tools.

    Returns:
        List of all tools

    Raises:
        HTTPException: If registry unavailable
    """
    if registry is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Tool registry not initialized",
        )

    tools = registry.list_all()

    return ToolListResponse(
        tools=[ToolMetadataResponse.from_metadata(t) for t in tools], count=len(tools)
    )


@router.get(
    "/by-trust-level/{trust_level}",
    response_model=ToolListResponse,
    summary="List tools by trust level",
    description="Retrieve tools filtered by trust level (HIGH, MEDIUM, or LOW).",
)
async def list_tools_by_trust_level(trust_level: str) -> ToolListResponse:
    """List tools by trust level.

    Args:
        trust_level: Trust level filter (HIGH/MEDIUM/LOW)

    Returns:
        List of matching tools

    Raises:
        HTTPException: If invalid trust level or registry unavailable
    """
    if registry is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Tool registry not initialized",
        )

    # Validate trust level
    try:
        TrustLevel(trust_level.upper())
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid trust level: {trust_level}. Must be HIGH, MEDIUM, or LOW",
        ) from e

    tools = registry.list_by_trust_level(trust_level.upper())

    return ToolListResponse(
        tools=[ToolMetadataResponse.from_metadata(t) for t in tools], count=len(tools)
    )


@router.get(
    "/by-type/{tool_type}",
    response_model=ToolListResponse,
    summary="List tools by type",
    description="Retrieve tools filtered by type (DATABASE, API, EMAIL, etc.).",
)
async def list_tools_by_type(tool_type: str) -> ToolListResponse:
    """List tools by type.

    Args:
        tool_type: Tool type filter (DATABASE/API/EMAIL/etc.)

    Returns:
        List of matching tools

    Raises:
        HTTPException: If invalid tool type or registry unavailable
    """
    if registry is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Tool registry not initialized",
        )

    # Validate tool type
    try:
        ToolType(tool_type.upper())
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid tool type: {tool_type}. "
            f"Must be one of: {', '.join([t.value for t in ToolType])}",
        ) from e

    tools = registry.list_by_type(tool_type.upper())

    return ToolListResponse(
        tools=[ToolMetadataResponse.from_metadata(t) for t in tools], count=len(tools)
    )
