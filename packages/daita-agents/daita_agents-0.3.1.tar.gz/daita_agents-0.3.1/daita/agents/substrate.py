"""
Substrate Agent - The foundational agent for Daita Agents.

This agent provides a blank slate that users can build upon to create
custom agents for any task, with simplified error handling and retry capabilities.
All operations are automatically traced without any configuration required.
"""
import asyncio
import logging
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, Optional, List, Union, Callable

from ..config.base import AgentConfig, AgentType
from ..core.interfaces import LLMProvider
from ..core.exceptions import (
    DaitaError, AgentError, LLMError, PluginError,
    ValidationError, InvalidDataError, NotFoundError
)
from ..core.tracing import TraceStatus
from .base import BaseAgent

logger = logging.getLogger(__name__)

# Import unified plugin access
from ..plugins import PluginAccess
from ..llm.factory import create_llm_provider
from ..config.settings import settings
from ..core.tools import AgentTool, ToolRegistry


class FocusedTool:
    """
    Wrapper that applies focus filtering to tool results.

    This reduces token usage and latency by filtering tool outputs
    BEFORE they reach the LLM. This is critical for DAITA's data
    operations efficiency.

    Example:
        Original tool returns 10KB of data -> Focus filters to 1KB
        -> LLM only processes 1KB (90% token reduction!)
    """

    def __init__(self, tool: AgentTool, focus_config):
        """
        Wrap a tool with focus filtering.

        Args:
            tool: The original AgentTool to wrap
            focus_config: Focus configuration (JSONPath, columns, etc.)
        """
        self._tool = tool
        self._focus = focus_config

    async def handler(self, arguments: Dict[str, Any]) -> Any:
        """
        Execute tool handler and apply focus to result.

        This is where the magic happens - tool results are filtered
        before being sent to the LLM, reducing tokens and latency.

        The LLM layer calls tool.handler() to execute tools.
        """
        # Execute original tool handler
        result = await self._tool.handler(arguments)

        # Apply focus to result (if applicable)
        if self._focus and result is not None:
            try:
                from ..core.focus import apply_focus
                from ..config.base import FocusConfig

                # Convert FocusConfig to format apply_focus expects
                focus_param = self._focus
                if isinstance(self._focus, FocusConfig):
                    # Convert FocusConfig to dict/str/list format
                    if self._focus.type == "column":
                        focus_param = self._focus.columns or []
                    elif self._focus.type == "jsonpath":
                        focus_param = self._focus.path
                    elif self._focus.type == "xpath":
                        focus_param = self._focus.path
                    elif self._focus.type == "css":
                        focus_param = self._focus.selector
                    elif self._focus.type == "regex":
                        focus_param = self._focus.pattern
                    else:
                        # For other types, convert to dict
                        focus_param = self._focus.dict()

                focused_result = apply_focus(result, focus_param)
                logger.debug(
                    f"Applied focus to {self.name} result: "
                    f"{type(result).__name__} -> {type(focused_result).__name__}"
                )
                return focused_result
            except Exception as e:
                logger.warning(f"Focus application failed for {self.name}: {e}")
                # Return original result if focus fails
                return result

        return result

    def __getattr__(self, name):
        """Delegate all other attributes to the wrapped tool."""
        return getattr(self._tool, name)

    def __repr__(self):
        return f"FocusedTool({self._tool.name}, focus={self._focus})"


@dataclass
class LLMResult:
    """
    Unified LLM response format for both streaming and non-streaming.

    This dataclass normalizes responses from different execution modes
    into a consistent format for processing tool calls and final answers.
    """
    text: str
    tool_calls: List[Dict[str, Any]]

    @classmethod
    def from_stream(cls, thinking_text: str, tool_calls: List[Dict]) -> 'LLMResult':
        """Create LLMResult from streaming chunks."""
        return cls(text=thinking_text, tool_calls=tool_calls)

    @classmethod
    def from_response(cls, response: Any) -> 'LLMResult':
        """
        Create LLMResult from non-streaming response.

        Handles both string responses (final answers) and dict responses
        (with tool_calls or structured content).
        """
        if isinstance(response, str):
            return cls(text=response, tool_calls=[])
        elif isinstance(response, dict):
            return cls(
                text=response.get('content', ''),
                tool_calls=response.get('tool_calls', [])
            )
        else:
            logger.warning(f"Unexpected response type: {type(response)}")
            return cls(text=str(response), tool_calls=[])


class SubstrateAgent(BaseAgent):
    """
    Substrate Agent - DAITA's primary agent implementation.

    A flexible, tool-enabled agent for data operations with autonomous
    LLM-driven task execution.

    ## Quick Start

    ```python
    from daita import SubstrateAgent
    from daita.core.tools import tool

    # Define tools for your agent
    @tool
    async def query_database(sql: str) -> list:
        '''Execute SQL query and return results.'''
        return await db.execute(sql)

    # Create agent with tools
    agent = SubstrateAgent(
        name="Data Analyst",
        model="gpt-4o-mini",
        prompt="You are a data analyst. Help users query and analyze data."
    )
    agent.register_tool(query_database)

    # Use the clean API
    await agent.start()

    # Simple execution - just get the answer
    answer = await agent.run("What were total sales last month?")
    print(answer)

    # Detailed execution - get full metadata
    result = await agent.run_detailed("Show me top 10 customers")
    print(f"Answer: {result['result']}")
    print(f"Time: {result['processing_time_ms']}ms")
    print(f"Cost: ${result['cost']}")
    ```

    ## Architecture

    SubstrateAgent uses autonomous tool calling:
    1. You give the agent tools and a natural language instruction
    2. The LLM autonomously decides which tools to use and when
    3. Tools are executed and results fed back to the LLM
    4. The LLM produces a final answer

    This is the modern agent paradigm - autonomous, tool-driven execution.

    ## Extending with Tools

    Tools are the primary way to extend agent capabilities:

    ```python
    from daita.core.tools import tool

    @tool
    async def calculate_metrics(data: list) -> dict:
        '''Calculate statistical metrics for data.'''
        return {
            'mean': sum(data) / len(data),
            'max': max(data),
            'min': min(data)
        }

    agent.register_tool(calculate_metrics)
    ```

    ## Focus System (Data Filtering)

    DAITA's unique focus system filters tool results BEFORE they reach the LLM,
    reducing token usage and latency:

    ```python
    from daita.config.base import FocusConfig

    agent = SubstrateAgent(
        name="Sales Analyzer",
        focus=FocusConfig(
            type="jsonpath",
            path="$.sales[*].amount"  # Only extract amounts
        )
    )
    ```

    Focus types: jsonpath, column, xpath, css, regex

    ## System Integration

    SubstrateAgent integrates with workflows, webhooks, and schedules:

    - `receive_message()` - Handle workflow communication
    - `on_webhook()` - Handle webhook triggers
    - `on_schedule()` - Handle scheduled tasks

    These are called automatically by the DAITA infrastructure.
    """
    
    # Class-level defaults for smart constructor
    _default_llm_provider = "openai"
    _default_model = "gpt-4"

    @classmethod
    def configure_defaults(cls, **kwargs):
        """Set global defaults for all SubstrateAgent instances."""
        for key, value in kwargs.items():
            setattr(cls, f'_default_{key}', value)

    def __new__(cls, name=None, **kwargs):
        """Smart constructor with auto-configuration."""
        # Auto-configuration from environment and defaults
        if not kwargs.get('llm_provider'):
            kwargs['llm_provider'] = getattr(cls, '_default_llm_provider', 'openai')
        if not kwargs.get('model'):
            kwargs['model'] = getattr(cls, '_default_model', 'gpt-4')
        if not kwargs.get('api_key'):
            provider = kwargs.get('llm_provider', 'openai')
            # Only try to get API key if provider is a string (not an object)
            if isinstance(provider, str):
                kwargs['api_key'] = settings.get_llm_api_key(provider)

        return super().__new__(cls)
    
    def __init__(
        self,
        name: Optional[str] = None,
        llm_provider: Optional[Union[str, LLMProvider]] = None,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        config: Optional[AgentConfig] = None,
        agent_id: Optional[str] = None,
        prompt: Optional[Union[str, Dict[str, str]]] = None,
        focus: Optional[Union[List[str], str, Dict[str, Any]]] = None,
        relay: Optional[str] = None,
        mcp: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        display_reasoning: bool = False,
        **kwargs
    ):
        """
        Initialize the Substrate Agent with smart constructor pattern.

        This constructor auto-creates LLM providers and provides sensible
        defaults while preserving all functionality.

        Args:
            name: Agent name (required for direct instantiation)
            llm_provider: LLM provider name ("openai", "anthropic") or instance
            model: Model name ("gpt-4", "claude-3-sonnet-20240229")
            api_key: API key for LLM provider (auto-detected from env if not provided)
            config: Agent configuration (auto-generated if not provided)
            agent_id: Unique identifier for the agent
            prompt: Custom prompt or prompt templates
            focus: Default focus configuration for data processing
            relay: Name of relay channel for publishing results
            mcp: MCP server(s) for tool integration - single dict or list of dicts
            display_reasoning: Enable minimal decision display in console
            **kwargs: Additional configuration options (can include 'tools' parameter)
        """
        # Auto-create LLM provider if needed
        if isinstance(llm_provider, str) or llm_provider is None:
            provider_name = llm_provider or self._default_llm_provider
            model_name = model or self._default_model
            api_key_to_use = api_key or settings.get_llm_api_key(provider_name)
            
            if api_key_to_use:
                llm_provider = create_llm_provider(
                    provider=provider_name,
                    model=model_name,
                    api_key=api_key_to_use,
                    agent_id=agent_id
                )
            else:
                logger.warning(f"No API key found for {provider_name}. LLM functionality will be disabled.")
                llm_provider = None
        # Create default config if none provided
        if config is None:
            config = AgentConfig(
                name=name or "Substrate Agent",
                type=AgentType.SUBSTRATE,
                **kwargs
            )
        
        # Initialize base agent (which handles automatic tracing)
        super().__init__(config, llm_provider, agent_id, name)
        
        # Store customization options
        self.prompt = prompt
        self.default_focus = focus
        self.relay = relay
        
        # Decision display setup
        self.display_reasoning = display_reasoning
        self._decision_display = None
        
        if display_reasoning:
            self._setup_decision_display()

        # Tool management (unified system)
        self.tool_registry = ToolRegistry()
        self.tool_sources = kwargs.get('tools', [])  # Plugins, AgentTool instances, or callables
        self._tools_setup = False

        # MCP server integration
        self.mcp_registry = None
        self.mcp_tools = []
        if mcp is not None:
            # Normalize to list
            mcp_servers = [mcp] if isinstance(mcp, dict) else mcp
            self._mcp_server_configs = mcp_servers
            # MCP setup happens lazily on first use to avoid blocking init
        else:
            self._mcp_server_configs = []

        # Plugin access for direct plugin usage
        self.plugins = PluginAccess()

        logger.debug(f"Substrate Agent {self.name} initialized")
    
    
    def _setup_decision_display(self):
        """Setup minimal decision display for local development."""
        try:
            from ..display.console import create_console_decision_display
            from ..core.decision_tracing import register_agent_decision_stream

            # Create display
            self._decision_display = create_console_decision_display(
                agent_name=self.name,
                agent_id=self.agent_id
            )

            # Register with decision streaming system
            register_agent_decision_stream(
                agent_id=self.agent_id,
                callback=self._decision_display.handle_event
            )

            logger.debug(f"Decision display enabled for agent {self.name}")

        except Exception as e:
            logger.warning(f"Failed to setup decision display: {e}")
            self.display_reasoning = False
            self._decision_display = None

    async def _setup_mcp_tools(self):
        """
        Setup MCP servers and discover available tools.

        This is called lazily on first agent.process() to avoid blocking
        agent initialization with MCP server connections.
        """
        if self.mcp_registry is not None:
            # Already setup
            return

        if not self._mcp_server_configs:
            # No MCP servers configured
            return

        try:
            from ..plugins.mcp import MCPServer, MCPToolRegistry

            logger.info(f"Setting up {len(self._mcp_server_configs)} MCP server(s) for {self.name}")

            # Create registry
            self.mcp_registry = MCPToolRegistry()

            # Connect to each server and register tools
            for server_config in self._mcp_server_configs:
                server = MCPServer(
                    command=server_config.get("command"),
                    args=server_config.get("args", []),
                    env=server_config.get("env", {}),
                    server_name=server_config.get("name")
                )

                # Add to registry (automatically connects and discovers tools)
                await self.mcp_registry.add_server(server)

            # Get all tools from registry
            self.mcp_tools = self.mcp_registry.get_all_tools()

            logger.info(f"MCP setup complete: {self.mcp_registry.tool_count} tools from {self.mcp_registry.server_count} server(s)")

        except ImportError:
            logger.error(
                "MCP SDK not installed. Install with: pip install mcp\n"
                "See: https://github.com/modelcontextprotocol/python-sdk"
            )
            raise

        except Exception as e:
            logger.error(f"Failed to setup MCP servers: {str(e)}")
            raise

    async def _setup_tools(self):
        """
        Discover and register tools from all sources.

        Called lazily on first process() call to avoid blocking initialization.
        Sources can be:
        - Plugin instances with get_tools() method
        - AgentTool instances directly
        - MCP server configurations
        """
        if self._tools_setup:
            return  # Already setup

        # 1. Setup MCP tools first
        if self._mcp_server_configs and self.mcp_registry is None:
            await self._setup_mcp_tools()
            # Convert MCP tools to AgentTool format
            for mcp_tool in self.mcp_tools:
                agent_tool = AgentTool.from_mcp_tool(mcp_tool, self.mcp_registry)
                self.tool_registry.register(agent_tool)

        # 2. Register plugin tools
        for source in self.tool_sources:
            if isinstance(source, AgentTool):
                # Direct AgentTool registration
                self.tool_registry.register(source)
                logger.debug(f"Registered tool: {source.name}")

            elif hasattr(source, 'get_tools'):
                # Plugin with get_tools() method
                plugin_tools = source.get_tools()
                if plugin_tools:
                    self.tool_registry.register_many(plugin_tools)
                    logger.info(
                        f"Registered {len(plugin_tools)} tools from "
                        f"{source.__class__.__name__}"
                    )
            else:
                logger.warning(
                    f"Invalid tool source: {source}. "
                    f"Expected AgentTool or plugin with get_tools() method."
                )

        self._tools_setup = True
        logger.info(
            f"Agent {self.name} initialized with {self.tool_registry.tool_count} tools"
        )

    # ========================================================================
    # USER API - What developers call directly
    # ========================================================================

    async def run(
        self,
        prompt: str,
        tools: Optional[List[Union[str, AgentTool]]] = None,
        max_iterations: int = 5,
        on_event: Optional[Callable] = None,
        **kwargs
    ) -> str:
        """
        Run an instruction or query with autonomous tool calling.

        This is the simplest way to use the agent - give it an instruction
        and let it figure out which tools to use.

        All execution is automatically traced without any user configuration.

        Args:
            prompt: The instruction or question
            tools: Optional list of tool names or AgentTool instances.
                   If None, uses all registered tools.
            max_iterations: Max number of tool calling iterations
            on_event: Optional callback for real-time execution events.
                     Called with AgentEvent objects as execution progresses.
            **kwargs: Additional LLM parameters (temperature, etc.)

        Returns:
            The agent's final answer as a string

        Examples:
            Simple execution:
            ```python
            answer = await agent.run("What's the weather in Seattle?")
            # "It's 55°F and rainy in Seattle."
            ```

            With real-time events:
            ```python
            def handle_event(event: AgentEvent):
                if event.type == EventType.THINKING:
                    print(f"AI: {event.content}", flush=True)
                elif event.type == EventType.TOOL_CALL:
                    print(f"🔧 Calling {event.tool_name}...")

            answer = await agent.run(
                "Build a platform",
                on_event=handle_event
            )
            ```

            With specific tools:
            ```python
            answer = await agent.run(
                "Calculate 127 times 45",
                tools=["calculator"]
            )
            ```

            With LLM parameters:
            ```python
            answer = await agent.run(
                "Write a creative story",
                temperature=0.9,
                max_tokens=500
            )
            ```
        """
        result = await self._run_traced(prompt, tools, max_iterations, on_event, **kwargs)
        return result['result']

    async def run_detailed(
        self,
        prompt: str,
        tools: Optional[List[Union[str, AgentTool]]] = None,
        max_iterations: int = 5,
        on_event: Optional[Callable] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Like run(), but returns full execution details.

        All execution is automatically traced without any user configuration.

        Args:
            prompt: The instruction or question
            tools: Optional list of tool names or AgentTool instances
            max_iterations: Max number of tool calling iterations
            on_event: Optional callback for real-time execution events
            **kwargs: Additional LLM parameters

        Returns:
            {
                "result": str,           # Final answer
                "tool_calls": [...],     # All tools called
                "iterations": int,       # Number of iterations
                "tokens": {...},         # Token usage
                "cost": float,           # Estimated cost
                "processing_time_ms": float,  # Execution time
                "agent_id": str,         # Agent identifier
                "agent_name": str        # Agent name
            }

        Examples:
            Basic usage:
            ```python
            result = await agent.run_detailed("Complex calculation task")

            print(f"Answer: {result['result']}")
            print(f"Used {len(result['tool_calls'])} tools")
            print(f"Cost: ${result['cost']:.4f}")
            print(f"Time: {result['processing_time_ms']:.0f}ms")
            ```

            With streaming events:
            ```python
            def show_progress(event: AgentEvent):
                if event.type == EventType.TOOL_CALL:
                    print(f"Calling {event.tool_name}...")

            result = await agent.run_detailed(
                "Build platform",
                on_event=show_progress
            )
            ```
        """
        return await self._run_traced(prompt, tools, max_iterations, on_event, **kwargs)

    async def _run_traced(
        self,
        prompt: str,
        tools: Optional[List[Union[str, AgentTool]]],
        max_iterations: int,
        on_event: Optional[Callable],
        **kwargs
    ) -> Dict[str, Any]:
        """
        Internal helper: Execute with automatic tracing and optional event streaming.

        This method handles all tracing automatically - users never call this directly.
        Creates an AGENT_EXECUTION trace span that encompasses the entire operation,
        with nested LLM_CALL spans for individual LLM interactions.

        If on_event callback is provided, emits AgentEvent objects during execution.
        """
        import time
        from ..core.tracing import TraceType

        start_time = time.time()

        # Create agent-level trace span (automatic, invisible to users)
        async with self.trace_manager.span(
            operation_name="agent_run",
            trace_type=TraceType.AGENT_EXECUTION,
            agent_id=self.agent_id,
            agent_name=self.name,
            prompt=prompt[:200],  # Truncate for storage
            tools_requested=tools,
            max_iterations=max_iterations,
            entry_point="run"  # Distinguishes from _process() calls
        ):
            # Execute using unified autonomous path
            # Handles both streaming (with on_event) and non-streaming (without)
            result = await self._execute_autonomous(
                prompt=prompt,
                tools=tools,
                max_iterations=max_iterations,
                on_event=on_event,
                **kwargs
            )

            # Enrich result with metadata
            result['processing_time_ms'] = (time.time() - start_time) * 1000
            result['agent_id'] = self.agent_id
            result['agent_name'] = self.name

            return result

    def _resolve_tools(self, tools: Optional[List[Union[str, AgentTool]]]) -> List[AgentTool]:
        """
        Resolve tool names to AgentTool instances.

        Args:
            tools: List of tool names (strings) or AgentTool instances.
                   If None, uses all registered tools.

        Returns:
            List of AgentTool instances
        """
        if tools is None:
            # Use all registered tools
            return list(self.tool_registry.tools)

        tool_list = []
        for t in tools:
            if isinstance(t, str):
                # Tool name - look up in registry
                tool = self.tool_registry.get(t)
                if not tool:
                    raise ValueError(f"Tool '{t}' not found in registry")
                tool_list.append(tool)
            else:
                # Already an AgentTool instance
                tool_list.append(t)

        return tool_list

    def _emit_event(self, on_event: Optional[Callable], event_type, **kwargs):
        """
        Emit event only if callback provided. Zero overhead when None.

        This allows the unified execution path to support both streaming
        and non-streaming modes without code duplication.
        """
        if on_event:
            from ..core.streaming import AgentEvent
            on_event(AgentEvent(type=event_type, **kwargs))

    def _prepare_tools_with_focus(
        self,
        tools: Optional[List[Union[str, 'AgentTool']]]
    ) -> List['AgentTool']:
        """
        Resolve tools and wrap with FocusedTool if focus configured.

        This consolidates tool resolution and focus wrapping logic that
        was previously duplicated across execution paths.

        Args:
            tools: List of tool names or AgentTool objects, or None for all tools

        Returns:
            List of AgentTool instances, wrapped with FocusedTool if focus enabled
        """
        resolved_tools = self._resolve_tools(tools)

        if self.default_focus and resolved_tools:
            resolved_tools = [
                FocusedTool(tool, self.default_focus)
                for tool in resolved_tools
            ]
            logger.debug(
                f"Wrapped {len(resolved_tools)} tools with focus filter: "
                f"{self.default_focus}"
            )

        return resolved_tools

    async def _stream_llm_turn(
        self,
        conversation: List[Dict],
        tools: List['AgentTool'],
        on_event: Callable,
        **kwargs
    ) -> LLMResult:
        """
        Execute streaming LLM turn with event emission.

        Args:
            conversation: Message history
            tools: Available tools (may include FocusedTool wrappers)
            on_event: Callback for streaming events
            **kwargs: Additional LLM parameters

        Returns:
            LLMResult with text and tool_calls
        """
        from ..core.streaming import EventType

        thinking_text = ""
        tool_calls = []

        async for chunk in await self.llm.generate(
            messages=conversation,
            tools=tools,
            stream=True,
            **kwargs
        ):
            if chunk.type == "text":
                thinking_text += chunk.content
                self._emit_event(on_event, EventType.THINKING, content=chunk.content)

            elif chunk.type == "tool_call_complete":
                tool_calls.append({
                    "id": chunk.tool_call_id,
                    "name": chunk.tool_name,
                    "arguments": chunk.tool_args
                })
                self._emit_event(
                    on_event,
                    EventType.TOOL_CALL,
                    tool_name=chunk.tool_name,
                    tool_args=chunk.tool_args
                )

        return LLMResult.from_stream(thinking_text, tool_calls)

    async def _nonstream_llm_turn(
        self,
        conversation: List[Dict],
        tools: List['AgentTool'],
        **kwargs
    ) -> LLMResult:
        """
        Execute non-streaming LLM turn.

        Args:
            conversation: Message history
            tools: Available tools (may include FocusedTool wrappers)
            **kwargs: Additional LLM parameters

        Returns:
            LLMResult with text and tool_calls
        """
        response = await self.llm.generate(
            messages=conversation,
            tools=tools,
            stream=False,
            **kwargs
        )

        return LLMResult.from_response(response)

    async def _execute_and_track_tool(
        self,
        tool_call: Dict[str, Any],
        tools: List['AgentTool'],
        on_event: Optional[Callable]
    ) -> Dict[str, Any]:
        """
        Execute tool and emit result event.

        The tool execution happens via the LLM provider's _execute_tool_call
        method, which calls tool.handler(). If the tool is wrapped with
        FocusedTool, the focus filtering happens automatically in the handler.

        Args:
            tool_call: Tool call dict with id, name, arguments
            tools: List of available tools
            on_event: Optional callback for result event

        Returns:
            Dict with tool, arguments, and result
        """
        from ..core.streaming import EventType

        # Execute via LLM provider (handles focus filtering via FocusedTool.handler)
        result = await self.llm._execute_tool_call(
            tool_call=tool_call,
            tools=tools
        )

        # Emit result event
        self._emit_event(
            on_event,
            EventType.TOOL_RESULT,
            tool_name=tool_call["name"],
            result=result
        )

        return {
            "tool": tool_call["name"],
            "arguments": tool_call["arguments"],
            "result": result
        }

    def _append_tool_messages(
        self,
        conversation: List[Dict],
        tool_calls: List[Dict],
        results: List[Any]
    ):
        """
        Add tool calls and results to conversation history.

        This updates the conversation in-place with:
        1. Assistant message containing tool calls
        2. Tool result messages for each tool call

        Args:
            conversation: Message history to update
            tool_calls: List of tool call dicts with id, name, arguments
            results: List of result dicts from _execute_and_track_tool
        """
        import json

        # Add assistant message with tool calls
        conversation.append({
            "role": "assistant",
            "tool_calls": tool_calls
        })

        # Add tool result messages
        for tool_call, result in zip(tool_calls, results):
            conversation.append({
                "role": "tool",
                "tool_call_id": tool_call["id"],
                "name": tool_call["name"],
                "content": json.dumps(result["result"])
            })

    def _build_final_result(
        self,
        final_text: str,
        tools_called: List[Dict],
        iterations: int,
        on_event: Optional[Callable]
    ) -> Dict[str, Any]:
        """
        Build final result dictionary with metadata.

        Args:
            final_text: The LLM's final answer
            tools_called: List of tool execution records
            iterations: Number of iterations used
            on_event: Optional callback for completion event

        Returns:
            Result dict with result, tool_calls, iterations, tokens, cost
        """
        from ..core.streaming import EventType

        token_stats = self.llm.get_token_stats()

        result = {
            "result": final_text,
            "tool_calls": tools_called,
            "iterations": iterations,
            "tokens": token_stats,
            "cost": token_stats.get("estimated_cost", 0.0)
        }

        # Emit completion event with all metadata
        self._emit_event(
            on_event,
            EventType.COMPLETE,
            final_result=final_text,
            iterations=iterations,
            token_usage=token_stats,
            cost=token_stats.get("estimated_cost", 0.0)
        )

        return result

    async def _execute_autonomous(
        self,
        prompt: str,
        tools: Optional[List[Union[str, 'AgentTool']]],
        max_iterations: int,
        on_event: Optional[Callable],
        **kwargs
    ) -> Dict[str, Any]:
        """
        Unified autonomous execution path for both streaming and non-streaming.

        This method handles the tool calling loop for both modes:
        - Streaming: Emits events via on_event callback
        - Non-streaming: Silent execution, same logic

        The focus system (FocusedTool wrapper) automatically reduces tokens
        by filtering tool results before they reach the LLM.

        Args:
            prompt: User instruction
            tools: Tool names or AgentTool objects, or None for all tools
            max_iterations: Maximum tool calling rounds
            on_event: Optional callback for streaming events
            **kwargs: Additional LLM parameters

        Returns:
            Dict with result, tool_calls, iterations, tokens, cost
        """
        from ..core.streaming import EventType

        # Prepare tools with focus wrapping
        resolved_tools = self._prepare_tools_with_focus(tools)

        # Build conversation
        conversation = [{"role": "user", "content": prompt}]
        tools_called = []

        # Autonomous tool calling loop
        for iteration in range(max_iterations):
            # Emit iteration event
            self._emit_event(
                on_event,
                EventType.ITERATION,
                iteration=iteration + 1,
                max_iterations=max_iterations
            )

            # Get LLM response (streaming or non-streaming based on on_event)
            if on_event:
                llm_result = await self._stream_llm_turn(
                    conversation, resolved_tools, on_event, **kwargs
                )
            else:
                llm_result = await self._nonstream_llm_turn(
                    conversation, resolved_tools, **kwargs
                )

            # Check if LLM wants to call tools
            if llm_result.tool_calls:
                # Execute each tool
                results = []
                for tool_call in llm_result.tool_calls:
                    result = await self._execute_and_track_tool(
                        tool_call, resolved_tools, on_event
                    )
                    tools_called.append(result)
                    results.append(result)

                # Add to conversation and continue loop
                self._append_tool_messages(
                    conversation, llm_result.tool_calls, results
                )
                continue

            # Final answer received
            return self._build_final_result(
                llm_result.text,
                tools_called,
                iteration + 1,
                on_event
            )

        # Max iterations reached without final answer
        raise AgentError(
            f"Max iterations ({max_iterations}) reached without final answer"
        )

    # ========================================================================
    # INTERNAL - Backward compatibility for system integration
    # ========================================================================

    async def _process(
        self,
        task: str,
        data: Any = None,
        context: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        INTERNAL: Process a task with data and context.

        This method is used internally by the framework for:
        - Workflow communication (receive_message calls this)
        - Lambda execution routing
        - System integration

        Users should NOT call this directly. Use:
        - run() for simple execution
        - run_detailed() for execution with metadata
        - receive_message() for workflow communication
        - on_webhook() for webhook triggers
        - on_schedule() for scheduled tasks

        Args:
            task: Task description or instruction
            data: Optional data payload
            context: Execution context metadata
            **kwargs: Additional parameters

        Returns:
            Execution result with metadata
        """
        # Convert task/data to prompt
        if data is not None:
            prompt = f"{task}: {data}"
        else:
            prompt = task

        # Use run_detailed as the core execution
        result = await self.run_detailed(
            prompt=prompt,
            **kwargs
        )

        # Merge context if provided (for internal tracking)
        if context:
            result['context'] = {**result.get('context', {}), **context}

        # Add legacy fields for backward compatibility with internal systems
        result['task'] = task
        result['status'] = 'success' if 'result' in result else 'error'

        return result

    # ========================================================================
    # SYSTEM INTEGRATION API - What infrastructure calls
    # ========================================================================

    async def receive_message(
        self,
        data: Any,
        source_agent: str,
        channel: str,
        workflow_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Handle workflow relay message from another agent.

        This method is called automatically by the workflow system when
        this agent receives a message from another agent via a relay channel.

        DO NOT call this directly unless you're building workflow infrastructure.
        For direct agent execution, use run() or run_detailed().

        Args:
            data: Message data from source agent
            source_agent: Name of the sending agent
            channel: Relay channel name
            workflow_name: Name of the workflow

        Returns:
            Execution result with workflow metadata

        Examples:
            Custom routing:
            ```python
            class MyAgent(SubstrateAgent):
                async def receive_message(self, data, source, channel, workflow=None):
                    if channel == "urgent":
                        return await self.run(
                            "URGENT: Process this immediately",
                            tools=["priority_handler"]
                        )
                    elif channel == "batch":
                        return await self.run(
                            "Batch process these records",
                            tools=["batch_processor"]
                        )
                    else:
                        return await super().receive_message(data, source, channel, workflow)
            ```
        """
        # Default implementation: autonomous processing with context
        prompt = f"Process message from {source_agent} via {channel}"

        # If data is structured, include it in context
        if isinstance(data, dict):
            prompt = f"{prompt}. Data: {data}"
        elif isinstance(data, list):
            prompt = f"{prompt}. Processing {len(data)} items."

        result = await self.run_detailed(prompt)

        # Add workflow metadata to result
        result['workflow_metadata'] = {
            'source_agent': source_agent,
            'channel': channel,
            'workflow': workflow_name,
            'entry_point': 'receive_message'
        }

        return result

    async def on_webhook(
        self,
        payload: Dict[str, Any],
        webhook_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Handle webhook trigger from external service.

        This method is called automatically by the webhook system when an
        external service (GitHub, Slack, etc.) triggers this agent.

        DO NOT call this directly unless you're building webhook infrastructure.
        For direct agent execution, use run() or run_detailed().

        Args:
            payload: Webhook payload from external service
            webhook_config: Webhook configuration (instructions, field mapping, etc.)

        Returns:
            Processing result with webhook metadata

        Examples:
            Custom webhook handling:
            ```python
            class MyAgent(SubstrateAgent):
                async def on_webhook(self, payload, webhook_config):
                    event_type = payload.get('event')

                    if event_type == 'push':
                        return await self.run(
                            f"Analyze code push: {payload['commits']}",
                            tools=["code_analyzer", "lint"]
                        )
                    elif event_type == 'issue':
                        return await self.run(
                            f"Triage issue: {payload['issue']['title']}",
                            tools=["issue_classifier"]
                        )
            ```
        """
        instructions = webhook_config.get('instructions', 'Process webhook data')

        result = await self.run_detailed(instructions)

        result['webhook_metadata'] = {
            'webhook_id': webhook_config.get('webhook_id'),
            'webhook_slug': webhook_config.get('webhook_slug'),
            'entry_point': 'on_webhook'
        }

        return result

    async def on_schedule(
        self,
        schedule_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Handle scheduled task execution (cron jobs).

        This method is called automatically by the scheduler when a
        scheduled task triggers.

        DO NOT call this directly unless you're building scheduler infrastructure.
        For direct agent execution, use run() or run_detailed().

        Args:
            schedule_config: Schedule configuration (task, cron, etc.)

        Returns:
            Processing result with schedule metadata

        Examples:
            Custom schedule handling:
            ```python
            class MyAgent(SubstrateAgent):
                async def on_schedule(self, schedule_config):
                    task = schedule_config['task']

                    if 'daily' in task.lower():
                        return await self.run(
                            "Run daily reports",
                            tools=["report_generator", "email"]
                        )
                    elif 'hourly' in task.lower():
                        return await self.run(
                            "Quick health check",
                            tools=["monitor"]
                        )
            ```
        """
        task = schedule_config.get('task', 'Execute scheduled task')

        result = await self.run_detailed(task)

        result['schedule_metadata'] = {
            'schedule_id': schedule_config.get('schedule_id'),
            'cron': schedule_config.get('cron'),
            'entry_point': 'on_schedule'
        }

        return result

    async def call_mcp_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Manually call an MCP tool.

        This allows users to explicitly call MCP tools for testing purposes.

        Args:
            tool_name: Name of the MCP tool to call
            arguments: Arguments for the tool

        Returns:
            Tool execution result

        Example:
            ```python
            result = await agent.call_mcp_tool("read_file", {"path": "/data/file.txt"})
            ```
        """
        if not self.mcp_registry:
            raise RuntimeError("No MCP servers configured. Add mcp parameter to SubstrateAgent.")

        return await self.mcp_registry.call_tool(tool_name, arguments)

    # User customization methods

    def add_plugin(self, plugin: Any):
        """
        Add a plugin to the agent's tool sources.

        The plugin's tools will be registered on next tool setup.
        """
        self.tool_sources.append(plugin)
        logger.debug(f"Added plugin: {plugin.__class__.__name__}")

    def register_tool(self, tool: AgentTool) -> None:
        """
        Register a single tool manually.

        Useful for adding custom tools after agent initialization.

        Args:
            tool: AgentTool instance to register

        Example:
            ```python
            from daita import tool
            agent = SubstrateAgent(name="my_agent")

            custom_tool = tool(my_custom_function)
            agent.register_tool(custom_tool)
            ```
        """
        self.tool_registry.register(tool)

    def register_tools(self, tools: List[AgentTool]) -> None:
        """
        Register multiple tools manually.

        Args:
            tools: List of AgentTool instances
        """
        self.tool_registry.register_many(tools)

    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        """
        Execute a tool by name.

        Provides manual tool execution for testing or custom handlers.

        Args:
            name: Tool name
            arguments: Tool arguments dict

        Returns:
            Tool execution result

        Example:
            ```python
            result = await agent.call_tool("query_database", {"sql": "SELECT 1"})
            ```
        """
        await self._setup_tools()
        return await self.tool_registry.execute(name, arguments)

    @property
    def available_tools(self) -> List[AgentTool]:
        """
        Get list of all available tools.

        Returns:
            List of AgentTool instances
        """
        return self.tool_registry.tools.copy()

    @property
    def tool_names(self) -> List[str]:
        """Get list of all tool names"""
        return self.tool_registry.tool_names

    async def stop(self) -> None:
        """Stop agent and clean up all resources including MCP connections."""
        # Clean up MCP connections first
        if self.mcp_registry:
            try:
                await self.mcp_registry.disconnect_all()
                logger.info(f"Cleaned up MCP connections for agent {self.name}")
            except Exception as e:
                logger.warning(f"Error cleaning up MCP connections: {e}")

        # Call parent stop for standard cleanup
        await super().stop()

    def get_token_usage(self) -> Dict[str, int]:
        """
        Get token usage for this agent using automatic tracing.

        Returns comprehensive token statistics from the unified tracing system.
        """
        if not self.llm or not hasattr(self.llm, 'get_token_stats'):
            # Fallback for agents without LLM or tracing
            return {
                'total_tokens': 0,
                'prompt_tokens': 0,
                'completion_tokens': 0,
                'requests': 0
            }

        return self.llm.get_token_stats()
    
    async def _publish_to_relay(self, result: Dict[str, Any], context: Dict[str, Any]):
        """Publish result to relay channel."""
        try:
            from ..core.relay import publish
            
            await publish(
                channel=self.relay,
                agent_response=result,
                publisher=self.name
            )
            logger.debug(f"Published result to relay channel: {self.relay}")
        except Exception as e:
            logger.warning(f"Failed to publish to relay channel {self.relay}: {str(e)}")
            # Don't re-raise - relay failures shouldn't break main processing
    
    @property
    def health(self) -> Dict[str, Any]:
        """Enhanced health information for SubstrateAgent."""
        base_health = super().health

        # Add SubstrateAgent-specific health info
        base_health.update({
            'tools': {
                'count': self.tool_registry.tool_count,
                'setup': self._tools_setup,
                'names': self.tool_registry.tool_names if self._tools_setup else []
            },
            'relay': {
                'enabled': self.relay is not None,
                'channel': self.relay
            },
            'llm': {
                'available': self.llm is not None,
                'provider': self.llm.provider_name if self.llm and hasattr(self.llm, 'provider_name') else None
            }
        })

        return base_health