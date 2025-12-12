"""MCP Server lifecycle management - Reusing core MCP modules to avoid duplication."""

import asyncio
import hashlib
import logging
import os
import subprocess
from typing import Optional, Any
from dataclasses import dataclass

from fastmcp import Client as MCPClient

# Reuse core MCP modules to avoid duplication
try:
    from spoon_ai.tools.mcp_tool import MCPTool
except ImportError as _e:
    logging.getLogger(__name__).warning(f"Core MCP tool not available: {_e}")
    MCPTool = None

try:
    from spoon_ai.agents.mcp_client_mixin import MCPClientMixin
except ImportError as _e:
    logging.getLogger(__name__).warning(f"Core MCP client mixin not available: {_e}")
    MCPClientMixin = None

try:
    from spoon_ai.tools.mcp_tools_collection import MCPToolsCollection
except ImportError:
    # Optional helper module; CLI can operate without it
    MCPToolsCollection = None

from .models import MCPServerConfig
from .errors import MCPServerError

logger = logging.getLogger(__name__)


@dataclass
class MCPServerInstance:
    """Represents a running MCP server instance."""

    server_id: str
    config: MCPServerConfig
    process: subprocess.Popen | None = None
    mcp_tool: Any | None = None  # Reuse MCPTool from core
    reference_count: int = 0
    status: str = "stopped"  # stopped, starting, running, error
    error_message: str | None = None
    available_tools: list | None = None  # Cache of available tools


class MCPServerManager:
    """Manages MCP server lifecycle and reuse."""

    def __init__(self):
        self.active_servers: dict[str, MCPServerInstance] = {}
        self.server_configs: dict[str, MCPServerConfig] = {}
        self._lock = asyncio.Lock()

    def _generate_server_id(self, config: MCPServerConfig) -> str:
        """Generate a unique server ID based on configuration."""
        # Include URL if present; otherwise fall back to command+args+cwd
        if getattr(config, 'url', None):
            config_str = f"url:{config.url}"
        else:
            config_str = f"cmd:{config.command}:{':'.join(config.args)}:{config.cwd or ''}"
        return hashlib.md5(config_str.encode()).hexdigest()[:8]

    async def get_or_create_server(self, config: MCPServerConfig) -> MCPServerInstance:
        """Get existing server or create a new one."""
        server_id = self._generate_server_id(config)

        async with self._lock:
            # Check if server already exists and is compatible
            if server_id in self.active_servers:
                server = self.active_servers[server_id]
                if self._is_config_compatible(server.config, config):
                    server.reference_count += 1
                    logger.info(f"Reusing MCP server {server_id} (refs: {server.reference_count})")
                    return server
                else:
                    # Configuration changed, need to restart
                    await self._stop_server_internal(server_id)

            # Create new server
            server = MCPServerInstance(
                server_id=server_id,
                config=config,
                reference_count=1
            )

            self.active_servers[server_id] = server
            self.server_configs[server_id] = config

            try:
                await self._start_server_internal(server)
                logger.info(f"Started MCP server {server_id}")
                return server
            except Exception as e:
                # Clean up on failure
                self.active_servers.pop(server_id, None)
                self.server_configs.pop(server_id, None)
                raise MCPServerError(server_id, f"Failed to start server: {str(e)}")

    async def release_server(self, server_id: str) -> None:
        """Release a reference to a server, stopping it if no more references."""
        async with self._lock:
            if server_id not in self.active_servers:
                logger.warning(f"Attempted to release unknown server {server_id}")
                return

            server = self.active_servers[server_id]
            server.reference_count -= 1

            logger.info(f"Released MCP server {server_id} (refs: {server.reference_count})")

            if server.reference_count <= 0:
                await self._stop_server_internal(server_id)
                logger.info(f"Stopped MCP server {server_id} (no more references)")

    async def stop_all_servers(self) -> None:
        """Stop all running servers."""
        async with self._lock:
            server_ids = list(self.active_servers.keys())
            for server_id in server_ids:
                await self._stop_server_internal(server_id)

    async def restart_server(self, server_id: str) -> None:
        """Restart a specific server."""
        async with self._lock:
            if server_id not in self.active_servers:
                raise MCPServerError(server_id, "Server not found")

            server = self.active_servers[server_id]
            await self._stop_server_internal(server_id, keep_instance=True)
            await self._start_server_internal(server)

    def get_server_for_tool(self, tool_name: str) -> MCPServerInstance | None:
        """Get the MCP server instance for a specific tool."""
        # This would need to be implemented based on tool-to-server mapping
        # For now, return the first running server that has the tool in autoApprove
        for server in self.active_servers.values():
            if server.status == "running" and (
                not server.config.autoApprove or tool_name in server.config.autoApprove
            ):
                return server
        return None

    def get_server_status(self, server_id: str) -> dict[str, any]:
        """Get status information for a server."""
        if server_id not in self.active_servers:
            return {"status": "not_found"}

        server = self.active_servers[server_id]
        return {
            "status": server.status,
            "reference_count": server.reference_count,
            "error_message": server.error_message,
            "config": server.config.model_dump()
        }

    def list_servers(self) -> dict[str, dict[str, any]]:
        """List all servers and their status."""
        return {
            server_id: self.get_server_status(server_id)
            for server_id in self.active_servers
        }

    def _is_config_compatible(self, existing: MCPServerConfig, new: MCPServerConfig) -> bool:
        """Check if two configurations are compatible (can reuse server)."""
        # URL-based transports: URLs must match exactly
        if getattr(existing, 'url', None) or getattr(new, 'url', None):
            return existing.url == new.url

        # Stdio-based: core command and args must match
        if existing.command != new.command or existing.args != new.args:
            return False

        # Working directory must match
        if existing.cwd != new.cwd:
            return False

        # Environment variables must be compatible
        # New config can add variables, but can't change existing ones
        for key, value in existing.env.items():
            if key in new.env and new.env[key] != value:
                return False

        return True

    def _create_mcp_tool(self, config: MCPServerConfig) -> Any:
        """Create MCPTool instance using core MCP modules."""
        if MCPTool is None:
            raise MCPServerError("unknown", "Core MCP modules not available")

        # Convert MCPServerConfig to MCPTool config format
        mcp_config = {
            "url": getattr(config, 'url', None),
            "command": getattr(config, 'command', None),
            "args": getattr(config, 'args', []),
            "env": getattr(config, 'env', {}),
            "cwd": getattr(config, 'cwd', None),
            "transport": getattr(config, 'transport', None),
            "headers": getattr(config, 'headers', {}),
            "connection_timeout": getattr(config, 'timeout', 30),
            "health_check_interval": 300,
            "max_retries": 3
        }

        try:
            # Use MCPTool's transport creation and initialization
            mcp_tool = MCPTool(
                name=f"mcp_server_{hashlib.md5(str(config).encode()).hexdigest()[:8]}",
                description="MCP server tool",
                mcp_config=mcp_config
            )
            return mcp_tool
        except Exception as e:
            raise MCPServerError("unknown", f"Failed to create MCPTool: {e}")

    async def _start_server_internal(self, server: MCPServerInstance) -> None:
        """Internal method to start a server using core MCP modules."""
        config = server.config

        if config.disabled:
            server.status = "disabled"
            return

        try:
            server.status = "starting"
            if config.url:
                logger.info(f"Connecting to remote MCP server {server.server_id} at {config.url}")
            else:
                logger.info(f"Starting MCP server {server.server_id} with command: {config.command} {' '.join(config.args)}")

            # Use core MCPTool to handle transport and connection
            server.mcp_tool = self._create_mcp_tool(config)

            # Test connection and cache available tools using MCPTool
            try:
                # Use MCPTool's list_available_tools method
                tools = await server.mcp_tool.list_available_tools()
                server.available_tools = tools
                logger.info(f"MCP server {server.server_id} has {len(tools)} tools available")
            except Exception as e:
                logger.warning(f"Could not list tools for server {server.server_id}: {e}")
                server.available_tools = []

            server.status = "running"
            server.error_message = None
            logger.info(f"MCP server {server.server_id} started successfully")

        except Exception as e:
            server.status = "error"
            server.error_message = str(e)
            logger.error(f"Failed to start MCP server {server.server_id}: {e}")
            logger.debug(f"Server config: command={getattr(config, 'command', None)}, args={getattr(config, 'args', [])}, env_keys={list(getattr(config, 'env', {}).keys())}")

            # Clean up on failure
            if server.mcp_tool:
                server.mcp_tool = None

            raise

    async def _stop_server_internal(self, server_id: str, keep_instance: bool = False) -> None:
        """Internal method to stop a server using core MCP modules."""
        if server_id not in self.active_servers:
            return

        server = self.active_servers[server_id]

        try:
            # Use MCPTool's cleanup if available
            if server.mcp_tool and MCPClientMixin:
                try:
                    await server.mcp_tool.cleanup()
                except Exception as e:
                    logger.warning(f"Error cleaning up MCP tool for {server_id}: {e}")

            # Clear cached tools and reset state
            server.available_tools = None
            server.mcp_tool = None
            server.status = "stopped"
            server.error_message = None

        except Exception as e:
            logger.error(f"Error stopping server {server_id}: {e}")
            server.status = "error"
            server.error_message = str(e)

        finally:
            if not keep_instance:
                self.active_servers.pop(server_id, None)
                self.server_configs.pop(server_id, None)

    async def get_server_tools(self, server_id: str) -> list:
        """Get available tools for a specific server using core MCP modules."""
        if server_id not in self.active_servers:
            return []

        server = self.active_servers[server_id]
        if server.status != "running":
            return []

        # Return cached tools if available
        if server.available_tools is not None:
            return server.available_tools

        # Try to refresh tools list using MCPTool
        try:
            if server.mcp_tool:
                tools = await server.mcp_tool.list_available_tools()
                server.available_tools = tools
                return tools
        except Exception as e:
            logger.error(f"Failed to get tools for server {server_id}: {e}")

        return []

    async def call_tool(self, server_id: str, tool_name: str, **kwargs) -> Any:
        """Call a tool on a specific MCP server using core MCP modules."""
        if server_id not in self.active_servers:
            raise MCPServerError(server_id, "Server not found")

        server = self.active_servers[server_id]
        if server.status != "running":
            raise MCPServerError(server_id, f"Server is not running (status: {server.status})")

        if not server.mcp_tool:
            raise MCPServerError(server_id, "No MCP tool available")

        try:
            # Use MCPTool's execute method which handles all the complex logic
            # Temporarily set the tool name for this call
            original_name = server.mcp_tool.name
            server.mcp_tool.name = tool_name

            try:
                logger.debug(f"Calling tool {tool_name} on server {server_id} with args: {kwargs}")
                result = await server.mcp_tool.execute(**kwargs)
                return result
            finally:
                # Restore original name
                server.mcp_tool.name = original_name

        except Exception as e:
            logger.error(f"Tool call failed on server {server_id}: {e}")
            raise MCPServerError(server_id, f"Tool call failed: {str(e)}")
