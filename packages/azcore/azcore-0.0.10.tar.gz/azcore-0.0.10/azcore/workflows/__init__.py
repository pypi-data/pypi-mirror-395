"""
Azcore. Workflows Module

This module provides various workflow patterns for multi-agent orchestration:
- SequentialWorkflow: Linear chain execution
- ConcurrentWorkflow: Parallel execution
- AgentRearrange: Dynamic routing
- GraphWorkflow: DAG orchestration
- MixtureOfAgents: Expert synthesis
- GroupChat: Conversational collaboration
- ForestSwarm: Dynamic tree selection
- HierarchicalSwarm: Director-worker architecture
- HeavySwarm: Five-phase comprehensive analysis
- SwarmRouter: Universal workflow orchestrator
"""

from azcore.workflows.sequential_workflow import SequentialWorkflow
from azcore.workflows.concurrent_workflow import ConcurrentWorkflow
from azcore.workflows.agent_rearrange import AgentRearrange
from azcore.workflows.graph_workflow import GraphWorkflow
from azcore.workflows.mixture_of_agents import MixtureOfAgents
from azcore.workflows.group_chat import GroupChat
from azcore.workflows.forest_swarm import ForestSwarm, AgentTree
from azcore.workflows.hierarchical_swarm import HierarchicalSwarm
from azcore.workflows.heavy_swarm import HeavySwarm
from azcore.workflows.swarm_router import SwarmRouter

__all__ = [
    "SequentialWorkflow",
    "ConcurrentWorkflow",
    "AgentRearrange",
    "GraphWorkflow",
    "MixtureOfAgents",
    "GroupChat",
    "ForestSwarm",
    "AgentTree",
    "HierarchicalSwarm",
    "HeavySwarm",
    "SwarmRouter",
]
