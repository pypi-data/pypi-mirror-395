"""
Agent components for the Azcore..

This module provides factories and builders for creating agents and teams,
along with advanced agent patterns for sophisticated reasoning and evaluation,
and agent routing/handoff capabilities.
"""

from azcore.agents.team_builder import TeamBuilder
from azcore.agents.mcp_team_builder import MCPTeamBuilder
from azcore.agents.agent_factory import AgentFactory
from azcore.agents.react_agent import ReactAgent
from azcore.agents.enhanced_agent import (
    create_enhanced_agent,
    create_simple_agent,
    BASE_ENHANCED_PROMPT,
)

# Advanced Agent Patterns
from azcore.agents.self_consistency_agent import SelfConsistencyAgent
from azcore.agents.reflexion_agent import ReflexionAgent
from azcore.agents.reasoning_duo_agent import ReasoningDuoAgent
from azcore.agents.agent_judge import AgentJudge
from azcore.agents.agent_pattern_router import (
    AgentPatternRouter,
    create_agent,
    AgentPattern,
)

# Agent Routing & Handoffs
from azcore.agents.agent_router import AgentRouter, HandoffAgent

# Agent Registry (NEW)
from azcore.agents.agent_registry import (
    AgentRegistry,
    AgentMetadata,
    get_global_registry,
    register_agent_globally,
    find_agent
)

__all__ = [
    # Core Agent Components
    "TeamBuilder",
    "MCPTeamBuilder",
    "AgentFactory",
    "ReactAgent",
    
    # Enhanced Agent Factory
    "create_enhanced_agent",
    "create_simple_agent",
    "BASE_ENHANCED_PROMPT",

    # Advanced Agent Patterns
    "SelfConsistencyAgent",
    "ReflexionAgent",
    "ReasoningDuoAgent",
    "AgentJudge",

    # Agent Pattern Router
    "AgentPatternRouter",
    "create_agent",
    "AgentPattern",

    # Agent Routing & Handoffs
    "AgentRouter",
    "HandoffAgent",
    
    # Agent Registry (NEW)
    "AgentRegistry",
    "AgentMetadata",
    "get_global_registry",
    "register_agent_globally",
    "find_agent",
]
