"""
RL Test: Using TeamBuilder with built-in RL support

This demonstrates the NEW simplified API where TeamBuilder directly
supports RL without needing custom wrapper classes.

Author: Az-Core Framework
Date: 2025
"""

import logging
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

# Import the modular graph builder
from graph_builder import build_graph

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
    graph = build_graph("config.yml")
    
    # Get input query
    query = os.getenv("AZCORE_INPUT_QUERY") or input("\nEnter your query: ")
    
    # Initialize state with user message
    initial_state = {
        "messages": [HumanMessage(content=query)]
    }
    
    logger.info(f"\nProcessing query: {query}\n")
    
    # Run the graph
    result = graph.invoke(initial_state)
    
    # Display result
    print("\n" + "=" * 70)
    print("FINAL RESULT")
    print("=" * 70)
    
    if result.get("messages"):
        last_message = result["messages"][-1]
        content = last_message.content if hasattr(last_message, 'content') else str(last_message)
        print(content)
    else:
        print("No result generated")
    
    print("=" * 70 + "\n")
    
    logger.info("Process completed successfully")


if __name__ == "__main__":
    main()
