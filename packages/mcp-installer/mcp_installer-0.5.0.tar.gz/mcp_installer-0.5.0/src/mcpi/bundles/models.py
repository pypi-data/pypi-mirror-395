"""Pydantic models for bundle data structures."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class BundleServer(BaseModel):
    """Server reference in a bundle.

    Attributes:
        id: Server ID from catalog (e.g., 'filesystem', 'github')
        config: Optional configuration overrides for this server
    """

    id: str = Field(..., description="Server ID from catalog")
    config: Optional[Dict[str, Any]] = Field(
        None, description="Optional config overrides"
    )


class Bundle(BaseModel):
    """A curated set of MCP servers.

    Bundles provide pre-configured sets of servers for common use cases
    (e.g., web-dev, data-science, devops).

    Attributes:
        name: Bundle identifier (used as bundle ID)
        description: Human-readable description of bundle purpose
        version: Bundle version (semver format)
        author: Optional bundle author/maintainer
        servers: List of servers included in bundle (minimum 1)
        suggested_scope: Recommended installation scope
    """

    name: str = Field(..., description="Bundle identifier (e.g., 'web-dev')")
    description: str = Field(..., description="Human-readable description")
    version: str = Field(default="1.0.0", description="Bundle version")
    author: Optional[str] = Field(None, description="Bundle author")
    servers: List[BundleServer] = Field(
        ..., min_length=1, description="List of servers in bundle"
    )
    suggested_scope: str = Field(
        default="user-global", description="Recommended installation scope"
    )
