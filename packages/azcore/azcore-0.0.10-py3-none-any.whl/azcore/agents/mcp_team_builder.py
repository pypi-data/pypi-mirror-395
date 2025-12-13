"""
MCPTeamBuilder for constructing teams with Model Context Protocol (MCP) integration.

This module provides the MCPTeamBuilder class which extends BaseTeam to create
teams that can connect to MCP servers and use their tools dynamically. It supports
the same fluent interface as TeamBuilder and integrates seamlessly with MainSupervisor.

MCP (Model Context Protocol) allows agents to connect to external servers that provide
tools, resources, and capabilities beyond what's available in the local environment.
"""

from typing import Sequence, Optional, Callable, Any, Dict, List
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.tools import BaseTool
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START
from langgraph.types import Command
from azcore.core.agent_executor import create_thinkat_agent
from azcore.core.base import BaseTeam
from azcore.core.state import State
from azcore.core.supervisor import Supervisor
from azcore.exceptions import ConfigurationError, ValidationError, TeamError
import logging

logger = logging.getLogger(__name__)

# Import MCP adapter if available
try:
    from langchain_mcp_adapters.client import MultiServerMCPClient
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    convert_mcp_to_langchain_tools = None
    MultiServerMCPClient = None
    ClientSession = None
    StdioServerParameters = None
    stdio_client = None
    logger.warning("MCP components not available. Install with: pip install langchain-mcp-adapters")

# Import RL components if available
try:
    from azcore.rl.rl_manager import RLManager
    from azcore.rl.rewards import RewardCalculator
    RL_AVAILABLE = True
except ImportError:
    RL_AVAILABLE = False
    RLManager = None
    RewardCalculator = None
    logger.debug("RL components not available")


class MCPTeamBuilder(BaseTeam):
    """
    Builder for creating MCP-enabled agent teams.
    
    MCPTeamBuilder uses a fluent interface pattern to construct teams that can
    connect to Model Context Protocol (MCP) servers and dynamically use their tools.
    It extends the standard TeamBuilder functionality with MCP server management.
    
    Features:
    - Connect to MCP servers (local or remote)
    - Automatic tool discovery and conversion
    - Seamless integration with MainSupervisor
    - Optional Reinforcement Learning for tool selection
    - Fluent builder interface
    
    Example (Basic MCP Team):
        >>> mcp_team = (MCPTeamBuilder("mcp_research_team")
        ...     .with_llm(llm)
        ...     .with_mcp_server("python", ["path/to/mcp_server.py"])
        ...     .with_prompt("You are a research assistant with MCP tools...")
        ...     .with_description("Research team with MCP capabilities")
        ...     .build())
    
    Example (MCP Team with RL):
        >>> rl_manager = RLManager(
        ...     tool_names=["mcp_search", "mcp_analyze"],
        ...     q_table_path="rl_data/mcp_q_table.pkl"
        ... )
        >>> reward_calc = HeuristicRewardCalculator()
        >>> mcp_team = (MCPTeamBuilder("mcp_research_team")
        ...     .with_llm(llm)
        ...     .with_mcp_server("python", ["path/to/mcp_server.py"])
        ...     .with_rl(rl_manager, reward_calc)
        ...     .build())
    
    Example (Multiple MCP Servers):
        >>> mcp_team = (MCPTeamBuilder("multi_mcp_team")
        ...     .with_llm(llm)
        ...     .with_mcp_server("python", ["server1.py"])
        ...     .with_mcp_server("npx", ["-y", "@modelcontextprotocol/server-filesystem"])
        ...     .build())
    """
    
    def __init__(self, name: str):
        """
        Initialize an MCP team builder.
        
        Args:
            name: Unique identifier for the team
        """
        super().__init__(name=name)
        self._llm: Optional[BaseChatModel] = None
        self._tools: List[BaseTool] = []
        self._prompt: Optional[str] = None
        self._sub_agent: Optional[Any] = None
        self._sub_graph: Optional[Any] = None
        self._built = False
        
        # MCP-specific components
        self._mcp_servers: List[Dict[str, Any]] = []
        self._mcp_sessions: List[Any] = []  # ClientSession instances
        self._mcp_tools: List[BaseTool] = []
        self._mcp_enabled: bool = False
        self._mcp_client: Optional[Any] = None  # MultiServerMCPClient instance
        
        # RL components
        self._rl_enabled: bool = False
        self._rl_manager: Optional[Any] = None
        self._reward_calculator: Optional[Any] = None
        
        # Connection options
        self._skip_failed_servers: bool = False
        self._test_connection: bool = False
        
        self._logger = logging.getLogger(f"{self.__class__.__name__}.{name}")
    
    def with_llm(self, llm: BaseChatModel) -> 'MCPTeamBuilder':
        """
        Set the language model for the team.
        
        Args:
            llm: Language model to use
            
        Returns:
            Self for method chaining
        """
        self._llm = llm
        self._logger.debug(f"Set LLM for MCP team '{self.name}'")
        return self
    
    def with_tools(self, tools: Sequence[BaseTool]) -> 'MCPTeamBuilder':
        """
        Set additional non-MCP tools available to the team.
        
        These tools will be combined with any MCP tools discovered from servers.
        
        Args:
            tools: Sequence of tools
            
        Returns:
            Self for method chaining
        """
        self._tools = list(tools)
        tool_names = [tool.name for tool in tools]
        self._logger.info(f"Set {len(tools)} regular tools for MCP team '{self.name}': {tool_names}")
        return self
    
    def with_mcp_server(
        self,
        command: Optional[str] = None,
        args: Optional[List[str]] = None,
        env: Optional[Dict[str, str]] = None,
        url: Optional[str] = None,
        transport: str = "stdio",
        timeout: Optional[int] = None,
        sse_read_timeout: Optional[int] = None
    ) -> 'MCPTeamBuilder':
        """
        Add an MCP server connection to the team.
        
        The team will connect to this MCP server and discover available tools.
        Multiple MCP servers can be added to a single team.
        
        Args:
            command: Command to start the MCP server (e.g., "python", "npx", "node") - for stdio transport
            args: Arguments for the server command - for stdio transport
            env: Optional environment variables for the server
            url: URL for remote MCP server - for SSE transport
            transport: Transport type - "stdio" or "sse" (default: "stdio")
            timeout: Connection timeout in seconds (default: 30 for SSE, 10 for STDIO)
            sse_read_timeout: SSE read timeout in seconds (default: 60)
            
        Returns:
            Self for method chaining
            
        Example:
            >>> # Local Python MCP server (stdio)
            >>> team.with_mcp_server(command="python", args=["path/to/server.py"])
            
            >>> # NPX-based MCP server (stdio)
            >>> team.with_mcp_server(command="npx", args=["-y", "@modelcontextprotocol/server-filesystem"])
            
            >>> # Remote MCP server (SSE)
            >>> team.with_mcp_server(url="http://localhost:8000/sse", transport="sse")
            
            >>> # With environment variables
            >>> team.with_mcp_server(command="python", args=["server.py"], env={"API_KEY": "xxx"})
        """
        if not MCP_AVAILABLE:
            self._logger.error(
                "MCP components not available. "
                "Install with: pip install langchain-mcp-adapters"
            )
            raise ImportError("MCP support requires langchain-mcp-adapters package")
        
        # Validate configuration based on transport type
        if transport == "stdio":
            if not command or not args:
                self._logger.error("MCP stdio transport: Missing command or args")
                raise ConfigurationError(
                    "command and args are required for stdio transport",
                    details={"transport": transport, "command": command, "args": args}
                )
            server_config = {
                "command": command,
                "args": args,
                "env": env or {},
                "transport": "stdio",
                "timeout": timeout or 10  # Default 10 seconds for STDIO
            }
        elif transport == "sse":
            if not url:
                self._logger.error("MCP SSE transport: Missing URL")
                raise ConfigurationError(
                    "url is required for sse transport",
                    details={"transport": transport}
                )
            server_config = {
                "url": url,
                "transport": "sse",
                "env": env or {},
                "timeout": timeout or 30,  # Default 30 seconds for SSE
                "sse_read_timeout": sse_read_timeout or 60  # Default 60 seconds
            }
        else:
            self._logger.error(f"MCP: Unsupported transport type '{transport}'")
            raise ValidationError(
                f"Unsupported transport type: {transport}. Use 'stdio' or 'sse'",
                details={
                    "transport": transport,
                    "supported_transports": ["stdio", "sse"]
                }
            )
        
        self._mcp_servers.append(server_config)
        self._mcp_enabled = True
        
        if transport == "stdio":
            self._logger.info(
                f"Added MCP server to team '{self.name}': {command} {' '.join(args)}"
            )
        else:
            self._logger.info(
                f"Added SSE MCP server to team '{self.name}': {url}"
            )
        return self
    
    def with_prompt(self, prompt: str) -> 'MCPTeamBuilder':
        """
        Set the system prompt for the team.
        
        Args:
            prompt: System prompt
            
        Returns:
            Self for method chaining
        """
        self._prompt = prompt
        self._logger.debug(f"Set prompt for MCP team '{self.name}'")
        return self
    
    def with_description(self, description: str) -> 'MCPTeamBuilder':
        """
        Set the team description.
        
        Args:
            description: Description of the team's purpose
            
        Returns:
            Self for method chaining
        """
        self.description = description
        return self
    
    def skip_failed_servers(self, skip: bool = True) -> 'MCPTeamBuilder':
        """
        Configure whether to skip failed MCP servers or fail completely.
        
        If True, failed servers will be logged as warnings and the team will
        continue with remaining servers. If False (default), any server failure
        will cause the build to fail.
        
        Args:
            skip: Whether to skip failed servers
            
        Returns:
            Self for method chaining
        """
        self._skip_failed_servers = skip
        return self
    
    def test_connection_before_build(self, test: bool = True) -> 'MCPTeamBuilder':
        """
        Test SSE server connections before building.
        
        If True, will attempt a quick connection test to SSE servers before
        the full build process. This can help identify connection issues earlier.
        
        Args:
            test: Whether to test connections
            
        Returns:
            Self for method chaining
        """
        self._test_connection = test
        return self
    
    def with_rl(
        self,
        rl_manager: Any,
        reward_calculator: Any
    ) -> 'MCPTeamBuilder':
        """
        Enable Reinforcement Learning for intelligent tool selection.
        
        When RL is enabled, the team will use Q-learning to optimize
        which tools (including MCP tools) to select for different types of queries.
        
        Args:
            rl_manager: RLManager instance for Q-learning
            reward_calculator: RewardCalculator for computing rewards
            
        Returns:
            Self for method chaining
            
        Example:
            >>> rl_manager = RLManager(
            ...     tool_names=["mcp_tool1", "mcp_tool2"],
            ...     q_table_path="rl_data/mcp_q_table.pkl"
            ... )
            >>> reward_calc = HeuristicRewardCalculator()
            >>> team = (MCPTeamBuilder("mcp_team")
            ...     .with_llm(llm)
            ...     .with_mcp_server("python", ["server.py"])
            ...     .with_rl(rl_manager, reward_calc)
            ...     .build())
        """
        if not RL_AVAILABLE:
            self._logger.warning(
                "RL components not available. "
                "RL will be disabled for this MCP team."
            )
            return self
        
        self._rl_enabled = True
        self._rl_manager = rl_manager
        self._reward_calculator = reward_calculator
        
        self._logger.info(f"RL enabled for MCP team '{self.name}'")
        return self
    
    async def _test_sse_connection(self, url: str, timeout: int = 5) -> tuple[bool, str]:
        """
        Test if an SSE server is accessible.
        
        Args:
            url: URL to test
            timeout: Connection timeout in seconds
            
        Returns:
            Tuple of (success, message)
        """
        try:
            import httpx
            async with httpx.AsyncClient(timeout=timeout) as client:
                # Try a simple GET request to check if server is reachable
                response = await client.get(url, follow_redirects=True)
                if response.status_code < 500:
                    return True, f"✓ Server at {url} is reachable (status: {response.status_code})"
                else:
                    return False, f"✗ Server at {url} returned error: {response.status_code}"
        except Exception as e:
            return False, f"✗ Cannot reach server at {url}: {str(e)}"
    
    def _format_connection_error(self, error: Exception, server_configs: Dict) -> str:
        """
        Format a detailed error message for MCP connection failures.
        
        Args:
            error: The exception that occurred
            server_configs: Server configurations that failed
            
        Returns:
            Formatted error message with troubleshooting tips
        """
        error_str = str(error)
        
        # Check for common error types
        if "ConnectTimeout" in error_str or "timeout" in error_str.lower():
            message = "❌ MCP Server Connection Timeout\n\n"
            message += "The server did not respond within the timeout period.\n\n"
            message += "Possible causes:\n"
            for server_name, config in server_configs.items():
                if config["transport"] == "sse":
                    message += f"  • Server '{server_name}' at {config['url']} is not reachable\n"
                    message += f"    - Check if the server is running\n"
                    message += f"    - Verify the URL is correct\n"
                    message += f"    - Check firewall/network settings\n"
                    message += f"    - Try increasing timeout (current: {config.get('timeout', 30)}s)\n"
                else:
                    message += f"  • Server '{server_name}' ({config['command']}) did not start\n"
                    message += f"    - Check if the command is correct\n"
                    message += f"    - Verify all dependencies are installed\n"
            
            message += f"\nTo increase timeout, use:\n"
            message += f"  .with_mcp_server(..., timeout=60)  # 60 seconds\n"
            
        elif "Connection refused" in error_str or "ConnectionRefused" in error_str:
            message = "❌ MCP Server Connection Refused\n\n"
            message += "The server actively refused the connection.\n\n"
            message += "Possible causes:\n"
            message += "  • Server is not running\n"
            message += "  • Server is running on a different port\n"
            message += "  • Firewall is blocking the connection\n"
            
        else:
            message = f"❌ MCP Server Connection Failed\n\n"
            message += f"Error: {error_str}\n\n"
            message += "Please check:\n"
            message += "  • Server is running and accessible\n"
            message += "  • Configuration is correct\n"
            message += "  • Network connectivity\n"
        
        return message
    
    async def _connect_to_mcp_servers(self) -> List[BaseTool]:
        """
        Connect to all configured MCP servers and discover tools.
        
        This is an async method that establishes connections to MCP servers
        and converts their tools to LangChain format.
        Uses MultiServerMCPClient for managing multiple server connections.
        
        Returns:
            List of discovered MCP tools
        
        Raises:
            RuntimeError: If MCP connection fails
        """
        if not MCP_AVAILABLE:
            self._logger.error("MCP integration not available")
            raise ConfigurationError(
                "MCP not available. Install with: pip install langchain-mcp-adapters",
                details={"mcp_available": MCP_AVAILABLE}
            )
        
        # Build server configurations for MultiServerMCPClient
        server_configs = {}
        for idx, server_config in enumerate(self._mcp_servers):
            server_name = f"server_{idx}"
            
            if server_config["transport"] == "stdio":
                server_configs[server_name] = {
                    "command": server_config["command"],
                    "args": server_config["args"],
                    "env": server_config["env"],
                    "transport": "stdio",
                    "timeout": server_config.get("timeout", 10)
                }
                self._logger.info(
                    f"Preparing STDIO MCP server '{server_name}': "
                    f"{server_config['command']} {' '.join(server_config['args'])} "
                    f"(timeout: {server_config.get('timeout', 10)}s)"
                )
            elif server_config["transport"] == "sse":
                server_configs[server_name] = {
                    "url": server_config["url"],
                    "transport": "sse",
                    "timeout": server_config.get("timeout", 30),
                    "sse_read_timeout": server_config.get("sse_read_timeout", 60)
                }
                self._logger.info(
                    f"Preparing SSE MCP server '{server_name}': {server_config['url']} "
                    f"(timeout: {server_config.get('timeout', 30)}s, "
                    f"read_timeout: {server_config.get('sse_read_timeout', 60)}s)"
                )
        
        try:
            # Create MultiServerMCPClient
            self._logger.info(f"Connecting to {len(server_configs)} MCP server(s)...")
            client = MultiServerMCPClient(server_configs)
            
            # Get tools from all servers
            langchain_tools = await client.get_tools()
            
            self._mcp_tools.extend(langchain_tools)
            
            tool_names = [t.name for t in langchain_tools]
            self._logger.info(
                f"✓ Discovered {len(langchain_tools)} MCP tools from {len(server_configs)} server(s): {tool_names}"
            )
            
            # Store client for later use (if needed for cleanup)
            self._mcp_client = client
            
            return langchain_tools
            
        except Exception as e:
            # Provide detailed error message
            error_msg = self._format_connection_error(e, server_configs)
            self._logger.error(error_msg)
            raise TeamError(
                f"Failed to connect to MCP server",
                details={"error": str(e), "server_configs": list(server_configs.keys())}
            )
    
    def _connect_to_mcp_servers_sync(self) -> List[BaseTool]:
        """
        Synchronous wrapper for async MCP server connection.
        
        This allows the builder to be used in synchronous contexts.
        
        Returns:
            List of discovered MCP tools
        """
        import asyncio
        
        try:
            # Try to get existing event loop
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # If loop is already running, we need to create a task
                self._logger.warning(
                    "Event loop already running. MCP connection may need manual async setup."
                )
                return []
            else:
                return loop.run_until_complete(self._connect_to_mcp_servers())
        except RuntimeError:
            # No event loop, create a new one
            return asyncio.run(self._connect_to_mcp_servers())
    
    def build(self) -> Callable:
        """
        Build the MCP team and return a callable.
        
        This method:
        1. Connects to all configured MCP servers
        2. Discovers and converts MCP tools
        3. Creates an agent with combined tools (MCP + regular)
        4. Builds the internal sub-graph
        5. Returns a callable for use with MainSupervisor
        
        If RL is enabled, the team will use an RL-enabled ReactAgent
        for intelligent tool selection across all tools.
        
        Returns:
            Callable that represents the team's functionality
            
        Raises:
            ValueError: If required components are not set
            RuntimeError: If MCP connection fails
        """
        if self._built:
            self._logger.warning(f"MCP team '{self.name}' already built")
            return self._create_team_callable()
        
        if not self._llm:
            self._logger.error(f"Cannot build MCP team '{self.name}': LLM not configured")
            raise ConfigurationError(
                f"LLM not set for MCP team '{self.name}'. Use with_llm()",
                details={"team_name": self.name, "mcp_configured": self._mcp_server_configured}
            )
        
        # Connect to MCP servers and discover tools
        if self._mcp_enabled and self._mcp_servers:
            self._logger.info(f"Connecting to {len(self._mcp_servers)} MCP server(s)...")
            self._connect_to_mcp_servers_sync()
        
        # Combine regular tools with MCP tools
        all_tools = self._tools + self._mcp_tools
        
        if not all_tools:
            self._logger.warning(
                f"No tools available for MCP team '{self.name}'. "
                "Add tools with with_tools() or with_mcp_server()"
            )
        
        # Create agent based on RL configuration
        if self._rl_enabled and RL_AVAILABLE:
            self._logger.info(
                f"Building RL-enabled MCP agent for team '{self.name}' "
                f"with {len(all_tools)} tools ({len(self._mcp_tools)} from MCP)"
            )
            self._sub_agent = self._create_rl_agent(all_tools)
        else:
            self._logger.info(
                f"Building standard MCP agent for team '{self.name}' "
                f"with {len(all_tools)} tools ({len(self._mcp_tools)} from MCP)"
            )
            # Create standard agent
            self._sub_agent = create_thinkat_agent(
                model=self._llm,
                prompt=self._prompt or self._default_prompt(),
                tools=all_tools,
            )
        
        # Build the sub-graph
        self._build_sub_graph()
        self._built = True
        
        rl_status = " with RL" if self._rl_enabled else ""
        mcp_status = f" ({len(self._mcp_tools)} MCP tools)" if self._mcp_tools else ""
        self._logger.info(
            f"Built MCP team '{self.name}' with {len(all_tools)} tools{mcp_status}{rl_status}"
        )
        
        return self._create_team_callable()
    
    def _default_prompt(self) -> str:
        """
        Get default prompt for MCP team.
        
        Returns:
            Default system prompt
        """
        mcp_note = ""
        if self._mcp_tools:
            tool_names = [t.name for t in self._mcp_tools]
            mcp_note = (
                f"\n\nYou have access to MCP (Model Context Protocol) tools: {', '.join(tool_names)}. "
                "These tools provide extended capabilities from external servers."
            )
        
        return (
            f"You are a specialized agent on the {self.name} team. "
            "Use the available tools to complete tasks effectively. "
            "Choose the most appropriate tool for each situation."
            f"{mcp_note}"
        )
    
    def _create_rl_agent(self, tools: List[BaseTool]) -> Any:
        """
        Create an RL-enabled ReactAgent with MCP tools.
        
        Args:
            tools: Combined list of regular and MCP tools
            
        Returns:
            RL-enabled ReactAgent instance
        """
        from azcore.agents.agent_factory import AgentFactory
        
        factory = AgentFactory(default_llm=self._llm)
        
        rl_agent = factory.create_react_agent(
            name=f"{self.name}_agent",
            tools=tools,
            prompt=self._prompt or self._default_prompt(),
            description=self.description,
            rl_enabled=True,
            rl_manager=self._rl_manager,
            reward_calculator=self._reward_calculator
        )
        
        return rl_agent
    
    def _build_sub_graph(self) -> None:
        """Build the internal sub-graph for the MCP team."""
        import asyncio
        
        # Create async agent node for MCP tools (they require async invocation)
        async def agent_node_async(state: State) -> Command:
            """Async agent node for MCP agent."""
            result = await self._sub_agent.ainvoke(state)
            
            return Command(
                update={
                    "messages": [
                        HumanMessage(
                            content=result["messages"][-1].content,
                            name=f"{self.name}_supervisor"
                        )
                    ]
                },
                goto="supervisor"
            )
        
        # Wrap async node in sync wrapper
        def agent_node(state: State) -> Command:
            """Sync wrapper for async MCP agent node."""
            try:
                # Try to get existing event loop
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # If loop is already running, we can't use run_until_complete
                    # This case should be handled by the caller using async invocation
                    self._logger.warning(
                        "Event loop already running. Using synchronous fallback."
                    )
                    # Fall back to sync invocation if available
                    result = self._sub_agent.invoke(state)
                else:
                    result = loop.run_until_complete(agent_node_async(state))
            except RuntimeError:
                # No event loop, create a new one
                result = asyncio.run(agent_node_async(state))
            
            return result
        
        # Create supervisor for the sub-graph
        supervisor = Supervisor(
            llm=self._llm,
            members=[self.name]
        )
        supervisor_node = supervisor.create_node()
        
        # Build the sub-graph
        sub_graph_builder = StateGraph(State)
        sub_graph_builder.add_node("supervisor", supervisor_node)
        sub_graph_builder.add_node(self.name, agent_node)
        sub_graph_builder.add_edge(START, "supervisor")
        
        self._sub_graph = sub_graph_builder.compile()
        
        self._logger.debug(f"Built sub-graph for MCP team '{self.name}'")
    
    def _create_team_callable(self) -> Callable:
        """Create the callable that represents the MCP team."""
        import asyncio
        
        async def call_team_async(state: State) -> Command:
            """
            Async invoke the MCP team's sub-graph and return results.
            
            Args:
                state: Current workflow state
                
            Returns:
                Command with team's response
            """
            # Invoke the sub-graph with the last message
            response = await self._sub_graph.ainvoke({
                "messages": state["messages"][-1:]
            })
            
            # Handle Command return type vs State dict
            if isinstance(response, Command):
                # Extract messages from Command update
                messages = response.update.get("messages", [])
                if messages:
                    content = messages[-1].content
                else:
                    content = "No response from team"
            else:
                # Traditional state dict
                content = response["messages"][-1].content
            
            return Command(
                update={
                    "messages": [
                        HumanMessage(
                            content=content,
                            name=self.name
                        )
                    ]
                },
                goto="supervisor"
            )
        
        def call_team(state: State) -> Command:
            """
            Invoke the MCP team's sub-graph and return results.
            
            Args:
                state: Current workflow state
                
            Returns:
                Command with team's response
            """
            try:
                # Try to get existing event loop
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # If loop is already running, we can't use run_until_complete
                    self._logger.warning(
                        "Event loop already running. Using synchronous fallback for team callable."
                    )
                    # Invoke the sub-graph with the last message
                    response = self._sub_graph.invoke({
                        "messages": state["messages"][-1:]
                    })
                    
                    # Handle Command return type vs State dict
                    if isinstance(response, Command):
                        # Extract messages from Command update
                        messages = response.update.get("messages", [])
                        if messages:
                            content = messages[-1].content
                        else:
                            content = "No response from team"
                    else:
                        # Traditional state dict
                        content = response["messages"][-1].content
                    
                    return Command(
                        update={
                            "messages": [
                                HumanMessage(
                                    content=content,
                                    name=self.name
                                )
                            ]
                        },
                        goto="supervisor"
                    )
                else:
                    response = loop.run_until_complete(call_team_async(state))
            except RuntimeError:
                # No event loop, create a new one
                return asyncio.run(call_team_async(state))
            
            return response
        
        return call_team
    
    def get_team_callable(self) -> Callable:
        """
        Get the team callable (builds if not already built).
        
        Returns:
            Team callable
        """
        if not self._built:
            return self.build()
        return self._create_team_callable()
    
    def is_built(self) -> bool:
        """
        Check if the team has been built.
        
        Returns:
            True if built, False otherwise
        """
        return self._built
    
    def get_tool_names(self) -> List[str]:
        """
        Get the names of all tools in the team (regular + MCP).
        
        Returns:
            List of tool names
        """
        all_tools = self._tools + self._mcp_tools
        return [tool.name for tool in all_tools]
    
    def get_mcp_tool_names(self) -> List[str]:
        """
        Get the names of only MCP tools.
        
        Returns:
            List of MCP tool names
        """
        return [tool.name for tool in self._mcp_tools]
    
    def get_mcp_server_count(self) -> int:
        """
        Get the number of configured MCP servers.
        
        Returns:
            Number of MCP servers
        """
        return len(self._mcp_servers)
    
    async def fetch_mcp_tools(self) -> List[BaseTool]:
        """
        Fetch tools from configured MCP servers without building the team.
        
        This is useful when you want to inspect available MCP tools before
        building the team, or get tool information for planning purposes.
        
        Returns:
            List of discovered MCP tools
            
        Example:
            >>> builder = MCPTeamBuilder("wms_team").with_mcp_server(
            ...     url="http://localhost:8000/sse",
            ...     transport="sse"
            ... )
            >>> tools = await builder.fetch_mcp_tools()
            >>> print([t.name for t in tools])
        """
        if not self._mcp_servers:
            self._logger.warning("No MCP servers configured")
            return []
        
        if self._mcp_tools:
            # Tools already fetched
            self._logger.info(f"Returning cached {len(self._mcp_tools)} MCP tools")
            return self._mcp_tools
        
        # Connect and fetch tools
        return await self._connect_to_mcp_servers()
    
    def get_mcp_tools(self) -> List[BaseTool]:
        """
        Synchronously get tools from configured MCP servers.
        
        This is a synchronous wrapper around fetch_mcp_tools() for convenience.
        
        Returns:
            List of discovered MCP tools
            
        Example:
            >>> builder = MCPTeamBuilder("wms_team").with_mcp_server(
            ...     url="http://localhost:8000/sse",
            ...     transport="sse"
            ... )
            >>> tools = builder.get_mcp_tools()
            >>> print([t.name for t in tools])
        """
        import asyncio
        
        if not self._mcp_servers:
            self._logger.warning("No MCP servers configured")
            return []
        
        if self._mcp_tools:
            # Tools already fetched
            self._logger.info(f"Returning cached {len(self._mcp_tools)} MCP tools")
            return self._mcp_tools
        
        try:
            # Try to get existing event loop
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # If loop is already running, we can't use run_until_complete
                self._logger.warning(
                    "Event loop already running. Call fetch_mcp_tools() with await instead."
                )
                return []
            else:
                return loop.run_until_complete(self.fetch_mcp_tools())
        except RuntimeError:
            # No event loop, create a new one
            return asyncio.run(self.fetch_mcp_tools())
    
    def __repr__(self) -> str:
        status = "built" if self._built else "not built"
        rl_status = ", RL enabled" if self._rl_enabled else ""
        mcp_status = f", {len(self._mcp_servers)} MCP server(s)" if self._mcp_servers else ""
        tools_count = len(self._tools) + len(self._mcp_tools)
        return (
            f"MCPTeamBuilder(name='{self.name}', tools={tools_count}"
            f"{mcp_status}, {status}{rl_status})"
        )
