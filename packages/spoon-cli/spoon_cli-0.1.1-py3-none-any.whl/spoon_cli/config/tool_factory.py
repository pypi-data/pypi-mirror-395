"""Tool factory for creating tool instances from configuration."""

import logging
import os
import asyncio
import inspect
from typing import Any, Optional

from fastmcp import Client as MCPClient

from .base_tool import BaseTool
from .models import ToolConfig
from .mcp_manager import MCPServerManager, MCPServerInstance
from .errors import ToolConfigurationError

logger = logging.getLogger(__name__)


class ToolFactory:
    """Factory for creating tool instances from configuration."""

    def __init__(self, mcp_manager: MCPServerManager):
        self.mcp_manager = mcp_manager
        self._builtin_tools: dict[str, type] = {}
        self._external_tools: dict[str, type] = {}

    def register_builtin_tool(self, name: str, tool_class: type) -> None:
        """Register a built-in tool class."""
        self._builtin_tools[name] = tool_class

    def register_external_tool(self, name: str, tool_class: type) -> None:
        """Register an external tool class."""
        self._external_tools[name] = tool_class

    async def create_tool(self, tool_config: ToolConfig) -> BaseTool:
        """Create a tool instance from configuration."""
        if not tool_config.enabled:
            logger.info(f"Tool {tool_config.name} is disabled, skipping creation")
            return None

        try:
            if tool_config.type == "builtin":
                return self._create_builtin_tool(tool_config)
            elif tool_config.type == "mcp":
                return await self._create_mcp_tool(tool_config)
            elif tool_config.type == "external":
                return self._create_external_tool(tool_config)
            else:
                raise ToolConfigurationError(
                    tool_config.name,
                    f"Unknown tool type: {tool_config.type}"
                )

        except Exception as e:
            if isinstance(e, ToolConfigurationError):
                raise
            raise ToolConfigurationError(
                tool_config.name,
                f"Failed to create tool: {str(e)}"
            )

    def _create_builtin_tool(self, tool_config: ToolConfig) -> BaseTool:
        """Create a built-in tool instance."""
        tool_class = self._builtin_tools.get(tool_config.name)

        if not tool_class:
            # Try to dynamically import the tool
            tool_class = self._import_builtin_tool(tool_config.name)

        # Fallback to aggregator to get an instance if class not found
        aggregator_instance: BaseTool | None = None
        if not tool_class:
            aggregator_instance = self._create_builtin_tool_via_aggregator(tool_config)
            if aggregator_instance is None:
                raise ToolConfigurationError(
                    tool_config.name,
                    f"Built-in tool not found: {tool_config.name}"
                )

        try:
            # Apply tool-specific environment variables
            self._apply_environment_variables(tool_config.env)

            # Create tool instance with configuration
            if aggregator_instance is not None:
                tool_instance = aggregator_instance
                if tool_config.config:
                    try:
                        tool_instance = type(aggregator_instance)(**tool_config.config)
                    except Exception:
                        # Keep aggregator instance if re-instantiation not supported
                        pass
            else:
                tool_instance = tool_class(**tool_config.config)

            # Set tool metadata
            if hasattr(tool_instance, 'name'):
                tool_instance.name = tool_config.name
            if hasattr(tool_instance, 'description') and tool_config.description:
                tool_instance.description = tool_config.description

            return tool_instance

        except Exception as e:
            raise ToolConfigurationError(
                tool_config.name,
                f"Failed to initialize built-in tool: {str(e)}"
            )

    def _create_builtin_tool_via_aggregator(self, tool_config: ToolConfig) -> BaseTool | None:
        """Try to obtain a builtin tool instance using core aggregator without hardcoding names."""
        try:
            import importlib
            # Use core aggregator that enumerates toolkit tools
            crypto_mod = importlib.import_module("spoon_ai.tools.crypto_tools")
            get_tools = getattr(crypto_mod, "get_crypto_tools", None)
            if callable(get_tools):
                for inst in get_tools():
                    try:
                        if getattr(inst, "name", None) == tool_config.name:
                            return inst
                    except Exception:
                        continue
        except Exception:
            return None
        return None

    async def _create_mcp_tool(self, tool_config: ToolConfig) -> BaseTool:
        """Create an MCP tool instance."""
        if not tool_config.mcp_server:
            raise ToolConfigurationError(
                tool_config.name,
                "MCP tool configuration missing mcp_server section"
            )

        try:
            # Apply tool-specific environment variables
            self._apply_environment_variables(tool_config.env)

            # Merge tool env vars with MCP server env vars
            merged_server_config = tool_config.mcp_server.model_copy()
            if tool_config.env:
                merged_server_config.env.update(tool_config.env)

            # Get or create MCP server
            server_instance = await self.mcp_manager.get_or_create_server(
                merged_server_config
            )

            # Create MCP tool wrapper
            mcp_tool = MCPToolWrapper(
                name=tool_config.name,
                description=tool_config.description or f"MCP tool: {tool_config.name}",
                server_instance=server_instance,
                config=tool_config.config
            )

            # Initialize tool schema before returning
            await mcp_tool._initialize_tool_schema()

            return mcp_tool

        except Exception as e:
            raise ToolConfigurationError(
                tool_config.name,
                f"Failed to create MCP tool: {str(e)}"
            )

    def _create_external_tool(self, tool_config: ToolConfig) -> BaseTool:
        """Create an external tool instance."""
        tool_class = self._external_tools.get(tool_config.name)

        if not tool_class:
            raise ToolConfigurationError(
                tool_config.name,
                f"External tool not found: {tool_config.name}"
            )

        try:
            # Apply tool-specific environment variables
            self._apply_environment_variables(tool_config.env)

            tool_instance = tool_class(**tool_config.config)

            # Set tool metadata
            if hasattr(tool_instance, 'name'):
                tool_instance.name = tool_config.name
            if hasattr(tool_instance, 'description') and tool_config.description:
                tool_instance.description = tool_config.description

            return tool_instance

        except Exception as e:
            raise ToolConfigurationError(
                tool_config.name,
                f"Failed to initialize external tool: {str(e)}"
            )

    def _import_builtin_tool(self, tool_name: str) -> type | None:
        """Dynamically import a built-in tool class."""
        try:
            def _declared_name(cls) -> str | None:
                name = getattr(cls, "name", None)
                if not name and hasattr(cls, "model_fields"):
                    try:
                        field = getattr(cls, "model_fields", {}).get("name")
                        if field is not None:
                            name = getattr(field, "default", None)
                    except Exception:
                        pass
                return name

            # Try common tool locations
            import_paths = [
                f"spoon_ai.tools.{tool_name}",
                f"spoon_ai.tools.{tool_name}.{tool_name}",
                f"spoon_ai.tools.{tool_name}_tool",
                # Generic aggregator/toolkit locations
                "spoon_ai.tools.crypto_tools",
                "spoon_toolkits.crypto.crypto_powerdata",
                "spoon_toolkits.crypto.crypto_powerdata.tools",
                "spoon_toolkits.crypto.crypto_data_tools",
            ]

            for import_path in import_paths:
                try:
                    module = __import__(import_path, fromlist=[tool_name])

                    # Look for tool class in module
                    class_names = [
                        tool_name,
                        f"{tool_name.title()}Tool",
                        f"{tool_name.replace('_', '').title()}Tool",
                    ]

                    for class_name in class_names:
                        if hasattr(module, class_name):
                            tool_class = getattr(module, class_name)
                            if isinstance(tool_class, type):
                                # Accept classes that subclass our BaseTool OR look tool-like
                                if self._is_tool_like_class(tool_class):
                                    self._builtin_tools[tool_name] = tool_class
                                    return tool_class

                    # Fallback: inspect module for any tool-like class declaring matching name
                    for _attr, obj in inspect.getmembers(module, inspect.isclass):
                        try:
                            if self._is_tool_like_class(obj) and _declared_name(obj) == tool_name:
                                self._builtin_tools[tool_name] = obj
                                return obj
                        except Exception:
                            continue

                except ImportError:
                    continue

            # Global fallback: scan spoon_toolkits namespace for matching tool name
            try:
                import spoon_toolkits  # type: ignore

                for _attr, obj in inspect.getmembers(spoon_toolkits, inspect.isclass):
                    try:
                        if self._is_tool_like_class(obj) and _declared_name(obj) == tool_name:
                            self._builtin_tools[tool_name] = obj
                            return obj
                    except Exception:
                        continue
            except Exception:
                pass

            logger.warning(f"Could not import built-in tool: {tool_name}")
            return None

        except Exception as e:
            logger.error(f"Error importing built-in tool {tool_name}: {e}")
            return None

    def _is_tool_like_class(self, cls: type) -> bool:
        """Heuristic to accept tool classes from either core or toolkit.

        We can't rely on issubclass against our BaseTool because toolkit tools
        may subclass core's BaseTool. Treat a class as tool-like if it provides
        an async 'execute' method and has name/description attributes or accepts
        kwargs in its constructor.
        """
        try:
            # Must be a class
            if not isinstance(cls, type):
                return False
            # Has an execute attribute that is callable (ideally async)
            execute_fn = getattr(cls, 'execute', None)
            if execute_fn is None:
                return False
            # Prefer coroutine functions, but accept any callable
            # to avoid import-time inspection complexities
            has_metadata = any(hasattr(cls, attr) for attr in ('name', 'description', 'parameters'))
            if not has_metadata and hasattr(cls, "model_fields"):
                fields = getattr(cls, "model_fields", {})
                has_metadata = any(key in fields for key in ("name", "description", "parameters"))
            return callable(execute_fn) and has_metadata
        except Exception:
            return False

    def _apply_environment_variables(self, env_vars: dict[str, str]) -> None:
        """Apply environment variables for tool configuration."""
        if not env_vars:
            return

        for key, value in env_vars.items():
            # Set environment variable for this process
            os.environ[key] = value
            logger.debug(f"Set environment variable {key} for tool configuration")


class MCPToolWrapper(BaseTool):
    """Wrapper for MCP tools to integrate with SpoonAI tool system."""

    def __init__(
        self,
        name: str,
        description: str,
        server_instance: MCPServerInstance,
        config: dict[str, Any] = None
    ):
        super().__init__(
            name=name,
            description=description,
            parameters={
                "type": "object",
                "properties": {},  # Will be populated from MCP server schema
                "required": []
            }
        )
        # Use object.__setattr__ to bypass Pydantic validation for custom attributes
        object.__setattr__(self, 'server_instance', server_instance)
        object.__setattr__(self, 'config', config or {})
        object.__setattr__(self, '_tool_schema', None)
        object.__setattr__(self, 'mcp_config', config or {})
        # Mark this as an MCP tool by adding mcp_transport attribute
        object.__setattr__(self, 'mcp_transport', server_instance)



    async def _initialize_tool_schema(self):
        """Initialize tool schema from MCP server."""
        if self._tool_schema is not None:
            return

        try:
            # Use the server instance's MCPTool if available (core integration)
            if self.server_instance and getattr(self.server_instance, 'mcp_tool', None):
                tools = await self.server_instance.mcp_tool.list_available_tools()

                # tools is a list of dicts with keys like name, description, inputSchema
                for tool in tools:
                    t_name = tool.get('name') if isinstance(tool, dict) else getattr(tool, 'name', None)
                    if t_name == self.name:
                        # Update our parameters with the actual schema
                        schema = None
                        if isinstance(tool, dict):
                            schema = tool.get('inputSchema') or tool.get('schema')
                            description = tool.get('description')
                        else:
                            schema = getattr(tool, 'inputSchema', None)
                            description = getattr(tool, 'description', None)

                        if schema:
                            object.__setattr__(self, 'parameters', schema)

                        # Update description if not set
                        if description and not self.description:
                            object.__setattr__(self, 'description', description)

                        object.__setattr__(self, '_tool_schema', tool)
                        logger.info(f"Initialized schema for MCP tool {self.name}")
                        break
                else:
                    logger.warning(f"Tool {self.name} not found in MCP server tools list")
            else:
                logger.warning(f"No MCP tool available on server instance for {self.name}")

        except Exception as e:
            logger.error(f"Failed to initialize tool schema for {self.name}: {e}")

    async def execute(self, **kwargs) -> Any:
        """Execute the MCP tool."""
        if self.server_instance.status != "running":
            raise ToolConfigurationError(
                self.name,
                f"MCP server is not running (status: {self.server_instance.status})"
            )

        try:
            # Initialize tool schema if not done yet
            await self._initialize_tool_schema()

            # Use the server instance's MCPTool for execution
            if self.server_instance and getattr(self.server_instance, 'mcp_tool', None):
                logger.debug(f"Calling MCP tool {self.name} with parameters: {kwargs}")
                result = await self.server_instance.mcp_tool.call_mcp_tool(self.name, **kwargs)
            else:
                raise ToolConfigurationError(
                    self.name,
                    "No MCP tool available for execution"
                )

            # Process the result
            if hasattr(result, 'data') and result.data is not None:
                # FastMCP provides structured data
                logger.debug(f"MCP tool {self.name} returned structured data: {result.data}")
                return result.data
            elif hasattr(result, 'content') and result.content:
                # Fall back to content blocks
                text_results = []
                for content in result.content:
                    if hasattr(content, 'text') and content.text:
                        text_results.append(content.text)

                if text_results:
                    combined_result = '\n'.join(text_results)
                    logger.debug(f"MCP tool {self.name} returned text content: {combined_result[:100]}...")
                    return combined_result
                else:
                    logger.warning(f"MCP tool {self.name} returned no usable content")
                    return ""
            elif isinstance(result, list):
                # Handle direct list of content blocks (as seen in our test)
                text_results = []
                for content in result:
                    if hasattr(content, 'text') and content.text:
                        text_results.append(content.text)

                if text_results:
                    combined_result = '\n'.join(text_results)
                    logger.debug(f"MCP tool {self.name} returned text content: {combined_result[:100]}...")
                    return combined_result
                else:
                    logger.warning(f"MCP tool {self.name} returned no usable content")
                    return ""
            else:
                logger.warning(f"MCP tool {self.name} returned unexpected result format: {type(result)}")
                return str(result)

        except Exception as e:
            logger.error(f"MCP tool {self.name} execution failed: {e}")
            raise ToolConfigurationError(
                self.name,
                f"MCP tool execution failed: {str(e)}"
            )

    async def list_available_tools(self) -> list:
        """List all available tools from the MCP server."""
        try:
            if self.server_instance and getattr(self.server_instance, 'mcp_tool', None):
                tools = await self.server_instance.mcp_tool.list_available_tools()
                # Normalize keys to include 'schema' for compatibility
                normalized = []
                for tool in tools:
                    if isinstance(tool, dict):
                        normalized.append({
                            "name": tool.get('name'),
                            "description": tool.get('description'),
                            "schema": tool.get('inputSchema') or tool.get('schema')
                        })
                    else:
                        normalized.append({
                            "name": getattr(tool, 'name', None),
                            "description": getattr(tool, 'description', None),
                            "schema": getattr(tool, 'inputSchema', None)
                        })
                return normalized
            else:
                logger.warning(f"No MCP tool available for {self.name}")
                return []
        except Exception as e:
            logger.error(f"Failed to list MCP tools: {e}")
            return []

    async def cleanup(self):
        """Clean up MCP client resources."""
        # FastMCP clients are cleaned up automatically with context managers
        # No explicit cleanup needed for server instance client
        logger.debug(f"MCP tool {self.name} cleanup completed")
