"""MCP client plugin system."""

from .base import MCPClientPlugin, ScopeHandler
from .claude_code import ClaudeCodePlugin
from .manager import MCPManager
from .registry import ClientRegistry
from .types import OperationResult, ScopeConfig, ServerConfig, ServerInfo, ServerState

__all__ = [
    "ServerInfo",
    "ServerConfig",
    "ServerState",
    "ScopeConfig",
    "OperationResult",
    "MCPClientPlugin",
    "ScopeHandler",
    "ClaudeCodePlugin",
    "ClientRegistry",
    "MCPManager",
]
