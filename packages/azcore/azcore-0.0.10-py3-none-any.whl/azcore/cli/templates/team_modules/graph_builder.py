"""Hierarchical graph builder for team collaboration.

This module builds the complete hierarchical graph with all teams,
coordinator, planner, supervisor, and generator nodes.

Author: Az-Core Framework
Date: 2025
"""

import logging
from langgraph.graph import StateGraph

from azcore.config import load_config
from azcore.agents.team_builder import TeamBuilder
from azcore.core.orchestrator import GraphOrchestrator
from azcore.core.supervisor import MainSupervisor
from azcore.nodes import (
    ResponseGeneratorNode,
    PlannerNode,
    CoordinatorNode
)
from azcore.rl import RLManager, HeuristicRewardCalculator

# Import team modules
from .research_tools import research_tools, research_team_config
from .data_tools import data_tools, data_team_config
from .communication_tools import communication_tools, communication_team_config
from .file_tools import file_tools, file_team_config

logger = logging.getLogger(__name__)


def build_graph(config_path: str = "config.yml") -> StateGraph:
    """Build RL-enabled hierarchical graph with modular teams.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        StateGraph: Compiled graph ready for execution
    """
    logger.info("\nLoading configuration...")
    config = load_config(config_path)
    llm = config.get_llm()
    response_generator_llm = config.get_llm("response_generator_llm")

    logger.info("\nSetting up RL managers...")

    # Research team with RL
    research_rl = RLManager(
        tool_names=[t.name for t in research_tools],
        q_table_path=research_team_config["rl_config"]["q_table_path"],
        exploration_rate=research_team_config["rl_config"]["exploration_rate"],
        use_embeddings=research_team_config["rl_config"]["use_embeddings"]
    )
    
    research_reward = HeuristicRewardCalculator(
        success_reward=research_team_config["rl_config"]["success_reward"],
        failure_reward=research_team_config["rl_config"]["failure_reward"],
        empty_penalty=research_team_config["rl_config"]["empty_penalty"]
    )

    # Data team with RL
    data_rl = RLManager(
        tool_names=[t.name for t in data_tools],
        q_table_path=data_team_config["rl_config"]["q_table_path"],
        exploration_rate=data_team_config["rl_config"]["exploration_rate"],
        use_embeddings=data_team_config["rl_config"]["use_embeddings"]
    )
    
    data_reward = HeuristicRewardCalculator(
        success_reward=data_team_config["rl_config"]["success_reward"],
        failure_reward=data_team_config["rl_config"]["failure_reward"],
        empty_penalty=data_team_config["rl_config"]["empty_penalty"]
    )

    # Communication team with RL
    communication_rl = RLManager(
        tool_names=[t.name for t in communication_tools],
        q_table_path=communication_team_config["rl_config"]["q_table_path"],
        exploration_rate=communication_team_config["rl_config"]["exploration_rate"],
        use_embeddings=communication_team_config["rl_config"]["use_embeddings"]
    )
    
    communication_reward = HeuristicRewardCalculator(
        success_reward=communication_team_config["rl_config"]["success_reward"],
        failure_reward=communication_team_config["rl_config"]["failure_reward"],
        empty_penalty=communication_team_config["rl_config"]["empty_penalty"]
    )

    # File team with RL
    file_rl = RLManager(
        tool_names=[t.name for t in file_tools],
        q_table_path=file_team_config["rl_config"]["q_table_path"],
        exploration_rate=file_team_config["rl_config"]["exploration_rate"],
        use_embeddings=file_team_config["rl_config"]["use_embeddings"]
    )
    
    file_reward = HeuristicRewardCalculator(
        success_reward=file_team_config["rl_config"]["success_reward"],
        failure_reward=file_team_config["rl_config"]["failure_reward"],
        empty_penalty=file_team_config["rl_config"]["empty_penalty"]
    )
    
    logger.info("✓ RL managers created")

    logger.info("\nCreating RL-enabled teams with TeamBuilder...")

    # Research team
    research_team = (TeamBuilder(research_team_config["name"])
        .with_llm(llm)
        .with_tools(research_tools)
        .with_prompt(research_team_config["prompt"])
        .with_rl(research_rl, research_reward)
        .with_description(research_team_config["description"])
    )
    logger.info("✓ Research team created with RL")

    # Data analysis team
    data_team = (TeamBuilder(data_team_config["name"])
        .with_llm(llm)
        .with_tools(data_tools)
        .with_prompt(data_team_config["prompt"])
        .with_rl(data_rl, data_reward)
        .with_description(data_team_config["description"])
    )
    logger.info("✓ Data analysis team created with RL")

    # Communication team
    communication_team = (TeamBuilder(communication_team_config["name"])
        .with_llm(llm)
        .with_tools(communication_tools)
        .with_prompt(communication_team_config["prompt"])
        .with_rl(communication_rl, communication_reward)
        .with_description(communication_team_config["description"])
    )
    logger.info("✓ Communication team created with RL")

    # File management team
    file_team = (TeamBuilder(file_team_config["name"])
        .with_llm(llm)
        .with_tools(file_tools)
        .with_prompt(file_team_config["prompt"])
        .with_rl(file_rl, file_reward)
        .with_description(file_team_config["description"])
    )
    logger.info("✓ File management team created with RL")

    logger.info("\nBuilding hierarchical graph...")
    
    # Create supervisor
    supervisor = MainSupervisor(
        llm=llm,
        members=[
            "research_team",
            "data_team",
            "communication_team",
            "file_team"
        ],
    )
    
    # Get tool names for planner context
    research_tool_names = [t.name for t in research_tools]
    data_tool_names = [t.name for t in data_tools]
    communication_tool_names = [t.name for t in communication_tools]
    file_tool_names = [t.name for t in file_tools]
    
    # Build planner system prompt
    planner_prompt = f"""You have the following teams and their capabilities:

1. **research_team**
   - Tools: {', '.join(research_tool_names)}
   - Capabilities: Web search, webpage scraping, content summarization
   - Use for: Information gathering, research tasks, web content analysis

2. **data_team**
   - Tools: {', '.join(data_tool_names)}
   - Capabilities: CSV analysis, JSON conversion, data filtering, statistics, aggregation
   - Use for: Data processing, analysis, transformation, statistical calculations

3. **communication_team**
   - Tools: {', '.join(communication_tool_names)}
   - Capabilities: Email sending, Slack messages, notifications, reminders, activity logging
   - Use for: Sending messages, creating notifications, logging events, scheduling reminders

4. **file_team**
   - Tools: {', '.join(file_tool_names)}
   - Capabilities: File reading/writing, directory listing, file operations, file search
   - Use for: File management, content manipulation, file system operations

Note: Each team specializes in its domain. Route tasks to the appropriate team based on the query type.
For complex tasks requiring multiple teams, create a sequential plan that coordinates between teams.
"""
    
    # Build the orchestrated graph
    orchestrator = GraphOrchestrator()
    graph = orchestrator.build_hierarchical_graph(
        coordinator=CoordinatorNode(llm=llm),
        planner=PlannerNode(llm=llm, system_prompt=planner_prompt),
        supervisor=supervisor,
        teams=[
            research_team,
            data_team,
            communication_team,
            file_team
        ],
        generator=ResponseGeneratorNode(llm=response_generator_llm)
    )

    logger.info("✓ Hierarchical graph built successfully")
    return graph
