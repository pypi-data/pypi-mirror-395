"""Workflow templates."""


def get_workflow_template(project_name: str) -> str:
    """Get workflow template."""
    return f'''"""
{project_name} - Custom Workflow
Created with Az-Core CLI
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from azcore.core.orchestrator import GraphOrchestrator
from azcore.core.state import State
from azcore.nodes.planner import PlannerNode
from azcore.nodes.generator import GeneratorNode

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
    
    # Create workflow nodes
    planner = PlannerNode(llm=llm)
    generator = GeneratorNode(llm=llm)
    
    # Build workflow graph
    orchestrator = GraphOrchestrator()
    
    # Add nodes
    orchestrator.add_node("planner", planner.execute)
    orchestrator.add_node("generator", generator.execute)
    
    # Define edges
    orchestrator.add_edge("planner", "generator")
    orchestrator.add_edge("generator", "__end__")
    
    # Set entry point
    orchestrator.set_entry_point("planner")
    
    # Compile workflow
    workflow = orchestrator.compile()
    
    # Get input query
    query = os.getenv("AZCORE_INPUT_QUERY") or input("Enter your query: ")
    
    # Initialize state
    state = State(messages=[{{"role": "user", "content": query}}])
    
    # Run workflow
    print("\\nRunning workflow...\\n")
    result = workflow.invoke(state)
    
    # Display result
    print("\\nResult:")
    print("-" * 60)
    if result.get("messages"):
        last_message = result["messages"][-1]
        print(last_message.get("content", "No response"))
    print("-" * 60)


if __name__ == "__main__":
    main()
'''
