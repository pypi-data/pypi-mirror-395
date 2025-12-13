"""Agent templates for project initialization."""


def get_basic_agent_template(project_name: str) -> str:
    """Get basic agent template."""
    return f'''"""
{project_name} - Basic Agent
Created with Az-Core CLI
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from azcore.agents.react_agent import ReactAgent
from azcore.core.state import State

# Load environment variables
load_dotenv()


def main():
    """Main application entry point."""
    print("=" * 60)
    print(f"{project_name}")
    print("=" * 60 + "\\n")
    
    # Initialize LLM
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Create agent
    agent = ReactAgent(
        name="basic_agent",
        llm=llm,
        tools=[],  # Add your tools here
        prompt="You are a helpful AI assistant."
    )
    
    # Get input query
    query = os.getenv("AZCORE_INPUT_QUERY") or input("Enter your query: ")
    
    # Initialize state
    state = State(messages=[{{"role": "user", "content": query}}])
    
    # Run agent
    print("\\nProcessing...\\n")
    result = agent.invoke(state)
    
    # Display result
    print("\\nResult:")
    print("-" * 60)
    if result.get("messages"):
        last_message = result["messages"][-1]
        print(last_message.content if hasattr(last_message, 'content') else str(last_message))
    print("-" * 60)


if __name__ == "__main__":
    main()
'''


def get_team_agent_template(project_name: str) -> str:
    """Get team agent template."""
    return f'''"""
{project_name} - Team Agent Collaboration
Created with Az-Core CLI
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from azcore.agents.team_builder import TeamBuilder
from azcore.workflows.sequential_workflow import SequentialWorkflow
from azcore.core.state import State

# Load environment variables
load_dotenv()


def main():
    """Main application entry point."""
    print("=" * 60)
    print(f"{project_name}")
    print("=" * 60 + "\\n")
    
    # Initialize LLM
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Create team builder with specialized agents
    from azcore.agents.team_builder import TeamBuilder
    
    # Define example tools (replace with your actual tools)
    from langchain_core.tools import tool
    
    @tool
    def research_tool(query: str) -> str:
        """Research tool for gathering information."""
        return f"Research results for: {{query}}"
    
    @tool
    def analyze_tool(query: str) -> str:
        """Analysis tool for data insights."""
        return f"Analysis of: {{query}}"
    
    tools = [research_tool, analyze_tool]
    
    # Build team with fluent interface
    team = (TeamBuilder("research_team")
        .with_llm(llm)
        .with_tools(tools)
        .with_prompt("You are a helpful research and analysis team.")
        .with_description("Handles research and analysis tasks")
        .build())
    
    # Get input query
    query = os.getenv("AZCORE_INPUT_QUERY") or input("Enter your query: ")
    
    # Initialize state
    from langchain_core.messages import HumanMessage
    state = State(messages=[HumanMessage(content=query)])
    
    # Run team (invoke the callable)
    print("\\nProcessing through team...\\n")
    result = team(state)
    
    # Display result
    print("\\nFinal Result:")
    print("-" * 60)
    # Handle Command object
    from langgraph.types import Command
    if isinstance(result, Command):
        messages = result.update.get("messages", [])
        if messages:
            last_message = messages[-1]
            print(last_message.content if hasattr(last_message, 'content') else str(last_message))
        else:
            print("No response messages")
    elif isinstance(result, dict) and result.get("update"):
        messages = result["update"].get("messages", [])
        if messages:
            last_message = messages[-1]
            print(last_message.content if hasattr(last_message, 'content') else str(last_message))
    else:
        print(str(result))
    print("-" * 60)


if __name__ == "__main__":
    main()
'''


def get_modular_team_agent_template(project_name: str) -> str:
    """Get modular team agent template with separate tool files."""
    return f'''"""
{project_name} - Modular Team Agent System
Created with Az-Core CLI

This demonstrates a modular approach with:
- Separate tool modules for each team
- Centralized graph builder
- Easy team management and scaling

Author: Az-Core Framework
Date: 2025
"""

import logging
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

# Import the modular graph builder
from team_modules.graph_builder import build_graph

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main application entry point."""
    logger.info("Starting RL-enabled hierarchical team system...")
    
    # Build the graph with all teams
    graph = build_graph("configs/config.yml")
    
    # Get input query
    query = os.getenv("AZCORE_INPUT_QUERY") or input("\\nEnter your query: ")
    
    # Initialize state with user message
    initial_state = {{
        "messages": [HumanMessage(content=query)]
    }}
    
    logger.info(f"\\nProcessing query: {{query}}\\n")
    
    # Run the graph
    result = graph.invoke(initial_state)
    
    # Display result
    print("\\n" + "=" * 70)
    print("FINAL RESULT")
    print("=" * 70)
    
    if result.get("messages"):
        last_message = result["messages"][-1]
        content = last_message.content if hasattr(last_message, 'content') else str(last_message)
        print(content)
    else:
        print("No result generated")
    
    print("=" * 70 + "\\n")
    
    logger.info("Process completed successfully")


if __name__ == "__main__":
    main()
'''


def get_rl_agent_template(project_name: str) -> str:
    """Get RL agent template."""
    return f'''"""
{project_name} - RL-Optimized Agent
Created with Az-Core CLI
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from azcore.agents.react_agent import ReactAgent
from azcore.rl.rl_manager import RLManager
from azcore.core.state import State

# Load environment variables
load_dotenv()


@tool
def calculator_tool(query: str) -> str:
    """Simple calculator tool. Useful for mathematical calculations."""
    try:
        result = eval(query)
        return f"Result: {{result}}"
    except Exception as e:
        return f"Error: {{str(e)}}"


@tool
def search_tool(query: str) -> str:
    """Simulated search tool. Useful for searching information."""
    return f"Search results for: {{query}}"


def main():
    """Main application entry point."""
    print("=" * 60)
    print(f"{project_name}")
    print("=" * 60 + "\\n")

    # Initialize LLM
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )

    # Define tools
    tools = [calculator_tool, search_tool]
    
    # Initialize RL Manager
    rl_manager = RLManager(
        tools=tools,
        learning_rate=0.1,
        discount_factor=0.9,
        exploration_strategy="epsilon_greedy",
        epsilon=0.2,
        q_table_path="./rl_data/q_table.pkl"
    )
    
    # Create RL-optimized agent
    agent = ReactAgent(
        name="rl_agent",
        llm=llm,
        tools=tools,
        prompt="You are an AI assistant with RL-optimized tool selection."
    )
    
    # Get input query
    query = os.getenv("AZCORE_INPUT_QUERY") or input("Enter your query: ")
    
    # Use RL Manager to select optimal tools
    print("\\nSelecting optimal tools with RL...\\n")
    selected_tools = rl_manager.select_tools(query, top_n=2)
    print(f"Selected tools: {{[t.name for t in selected_tools]}}\\n")
    
    # Initialize state
    state = State(messages=[{{"role": "user", "content": query}}])
    
    # Run agent
    print("Processing...\\n")
    result = agent.invoke(state)
    
    # Update RL with reward (placeholder - implement your reward logic)
    reward = 1.0 if result.get("messages") else 0.0
    rl_manager.update(query, selected_tools, reward)
    
    # Save Q-table
    rl_manager.save_q_table()
    
    # Display result
    print("\\nResult:")
    print("-" * 60)
    if result.get("messages"):
        last_message = result["messages"][-1]
        print(last_message.content if hasattr(last_message, 'content') else str(last_message))
    print("-" * 60)
    print(f"\\nRL Stats: {{rl_manager.get_stats()}}")


if __name__ == "__main__":
    main()
'''
