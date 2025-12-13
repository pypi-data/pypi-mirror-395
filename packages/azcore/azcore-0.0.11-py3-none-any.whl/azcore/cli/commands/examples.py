"""Browse and run example Az-Core projects."""

import click
import subprocess
import sys
from pathlib import Path
from typing import Optional, List, Dict, Any


EXAMPLES = {
    "basic-agent": {
        "name": "Basic Agent",
        "description": "Simple ReAct agent that answers questions",
        "difficulty": "Beginner",
        "time": "5 min",
        "tags": ["react", "basics", "getting-started"],
        "code": """
from azcore.agents import ReactAgent
from azcore.config import Config

def main():
    config = Config.from_yaml("config.yml")
    agent = ReactAgent(
        llm=config.get_llm(),
        name="BasicAgent",
        tools=[]
    )
    
    result = agent.run("What is 2 + 2?")
    print(result)

if __name__ == "__main__":
    main()
"""
    },
    "team-workflow": {
        "name": "Team Workflow",
        "description": "Multiple agents collaborating on a research task",
        "difficulty": "Intermediate",
        "time": "15 min",
        "tags": ["team", "collaboration", "workflow"],
        "code": """
from azcore.agents import ReactAgent
from azcore.workflows import SequentialWorkflow
from azcore.config import Config

def main():
    config = Config.from_yaml("config.yml")
    llm = config.get_llm()
    
    researcher = ReactAgent(llm=llm, name="Researcher", tools=[])
    writer = ReactAgent(llm=llm, name="Writer", tools=[])
    
    workflow = SequentialWorkflow(agents=[researcher, writer])
    result = workflow.run("Research and write about AI agents")
    
    print(result)

if __name__ == "__main__":
    main()
"""
    },
    "rl-agent": {
        "name": "RL Tool Selector",
        "description": "Agent that learns optimal tool selection with RL",
        "difficulty": "Advanced",
        "time": "30 min",
        "tags": ["rl", "learning", "tools", "optimization"],
        "code": """
from azcore.agents import ReactAgent
from azcore.rl import RLManager
from azcore.config import Config

def main():
    config = Config.from_yaml("config.yml")
    
    # Initialize RL manager
    rl_manager = RLManager(
        tool_names=["search", "calculator", "code_executor"],
        q_table_path="./data/q_table.pkl"
    )
    
    # Create agent with RL
    agent = ReactAgent(
        llm=config.get_llm(),
        name="RLAgent",
        tools=[],
        rl_manager=rl_manager
    )
    
    result = agent.run("What is the square root of 144?")
    print(result)

if __name__ == "__main__":
    main()
"""
    },
    "hierarchical-team": {
        "name": "Hierarchical Team",
        "description": "Multi-level agent hierarchy with supervisor",
        "difficulty": "Advanced",
        "time": "20 min",
        "tags": ["hierarchical", "supervisor", "team"],
        "code": """
from azcore.core import Supervisor, GraphOrchestrator
from azcore.agents import ReactAgent
from azcore.config import Config

def main():
    config = Config.from_yaml("config.yml")
    llm = config.get_llm()
    
    # Create agents
    agent1 = ReactAgent(llm=llm, name="Analyst", tools=[])
    agent2 = ReactAgent(llm=llm, name="Writer", tools=[])
    
    # Create supervisor
    supervisor = Supervisor(
        llm=llm,
        agents=[agent1, agent2]
    )
    
    # Build orchestrator
    orchestrator = GraphOrchestrator()
    orchestrator.add_supervisor(supervisor)
    graph = orchestrator.build()
    
    result = graph.run("Analyze market trends")
    print(result)

if __name__ == "__main__":
    main()
"""
    },
    "caching": {
        "name": "Caching Example",
        "description": "Using LLM response caching for efficiency",
        "difficulty": "Beginner",
        "time": "10 min",
        "tags": ["caching", "performance", "optimization"],
        "code": """
from azcore.utils import CachedLLM
from azcore.config import Config

def main():
    config = Config.from_yaml("config.yml")
    
    # Create cached LLM
    cached_llm = CachedLLM(
        llm=config.get_llm(),
        cache_dir="./data/cache"
    )
    
    # First call - hits LLM
    result1 = cached_llm.invoke("What is Python?")
    print("First call:", result1)
    
    # Second call - uses cache
    result2 = cached_llm.invoke("What is Python?")
    print("Second call (cached):", result2)
    
    # Show cache stats
    print(f"Cache hits: {cached_llm.cache_hits}")
    print(f"Cache misses: {cached_llm.cache_misses}")

if __name__ == "__main__":
    main()
"""
    },
    "custom-node": {
        "name": "Custom Node",
        "description": "Creating custom workflow nodes",
        "difficulty": "Intermediate",
        "time": "15 min",
        "tags": ["custom", "nodes", "workflow"],
        "code": """
from azcore.core import BaseNode, State, GraphOrchestrator
from azcore.config import Config

class CustomProcessor(BaseNode):
    def __call__(self, state: State) -> State:
        # Custom processing logic
        messages = state.get("messages", [])
        processed = f"Processed: {messages[-1] if messages else 'empty'}"
        
        state["messages"].append({
            "role": "assistant",
            "content": processed
        })
        return state

def main():
    config = Config.from_yaml("config.yml")
    
    # Create orchestrator with custom node
    orchestrator = GraphOrchestrator()
    orchestrator.add_node("processor", CustomProcessor())
    orchestrator.add_edge("START", "processor")
    orchestrator.add_edge("processor", "END")
    
    graph = orchestrator.build()
    result = graph.run({"messages": [{"role": "user", "content": "Hello"}]})
    
    print(result)

if __name__ == "__main__":
    main()
"""
    }
}


@click.group()
def examples():
    """Browse and run example Az-Core projects.
    
    Examples:
        azcore examples list
        azcore examples show basic-agent
        azcore examples run basic-agent
        azcore examples search rl
    """
    pass


@examples.command()
@click.option(
    "--tag",
    "-t",
    multiple=True,
    help="Filter by tag",
)
@click.option(
    "--difficulty",
    "-d",
    type=click.Choice(["Beginner", "Intermediate", "Advanced"]),
    help="Filter by difficulty",
)
def list(tag: tuple, difficulty: Optional[str]):
    """List all available examples.
    
    Examples:
        azcore examples list
        azcore examples list --tag rl
        azcore examples list --difficulty Beginner
    """
    click.secho("\n📚 Az-Core Examples\n", fg="cyan", bold=True)
    click.echo("=" * 70)
    
    filtered_examples = _filter_examples(tag, difficulty)
    
    if not filtered_examples:
        click.secho("No examples match your filters.", fg="yellow")
        return
    
    for key, example in filtered_examples.items():
        click.echo()
        click.secho(f"  {example['name']}", fg="green", bold=True)
        click.echo(f"  ID: {key}")
        click.echo(f"  {example['description']}")
        click.secho(f"  Difficulty: {example['difficulty']}", fg="blue")
        click.secho(f"  Time: {example['time']}", fg="blue")
        click.secho(f"  Tags: {', '.join(example['tags'])}", fg="bright_black")
    
    click.echo("\n" + "=" * 70)
    click.echo(f"\nTotal: {len(filtered_examples)} example(s)")
    click.echo("\nTo view an example: azcore examples show <id>")
    click.echo("To run an example:  azcore examples run <id>\n")


@examples.command()
@click.argument("example_id")
def show(example_id: str):
    """Show detailed information about an example.
    
    Examples:
        azcore examples show basic-agent
        azcore examples show rl-agent
    """
    if example_id not in EXAMPLES:
        click.secho(f"Error: Example '{example_id}' not found.", fg="red")
        click.echo("\nRun 'azcore examples list' to see available examples.")
        return
    
    example = EXAMPLES[example_id]
    
    click.echo("\n" + "=" * 70)
    click.secho(f"  {example['name']}", fg="cyan", bold=True)
    click.echo("=" * 70 + "\n")
    
    click.echo(f"Description:  {example['description']}")
    click.echo(f"Difficulty:   {example['difficulty']}")
    click.echo(f"Est. Time:    {example['time']}")
    click.echo(f"Tags:         {', '.join(example['tags'])}")
    
    click.echo("\n" + "-" * 70)
    click.secho("Code:", fg="yellow", bold=True)
    click.echo("-" * 70)
    click.echo(example['code'])
    click.echo("-" * 70 + "\n")
    
    click.echo("To run this example:")
    click.secho(f"  azcore examples run {example_id}", fg="green")
    click.echo()


@examples.command()
@click.argument("example_id")
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Save example to file instead of running",
)
@click.option(
    "--with-config",
    is_flag=True,
    help="Also create a sample config.yml",
)
def run(example_id: str, output: Optional[str], with_config: bool):
    """Run an example or save it to a file.
    
    Examples:
        azcore examples run basic-agent
        azcore examples run basic-agent --output my_agent.py
        azcore examples run basic-agent --with-config
    """
    if example_id not in EXAMPLES:
        click.secho(f"Error: Example '{example_id}' not found.", fg="red")
        click.echo("\nRun 'azcore examples list' to see available examples.")
        return
    
    example = EXAMPLES[example_id]
    
    if output:
        # Save to file
        output_path = Path(output)
        output_path.write_text(example['code'])
        
        click.secho(f"✓ Example saved to: {output_path}", fg="green")
        
        if with_config:
            config_path = output_path.parent / "config.yml"
            if not config_path.exists():
                config_content = _get_sample_config()
                config_path.write_text(config_content)
                click.secho(f"✓ Config saved to: {config_path}", fg="green")
        
        click.echo("\nNext steps:")
        click.echo(f"  1. Edit config.yml and add your API keys")
        click.echo(f"  2. python {output_path}")
    else:
        # Run directly
        click.secho(f"\n▶ Running example: {example['name']}\n", fg="cyan", bold=True)
        click.echo("=" * 70 + "\n")
        
        try:
            # Create temporary file and run it
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(example['code'])
                temp_path = f.name
            
            # Check for config.yml
            if not Path("config.yml").exists():
                click.secho("Warning: config.yml not found!", fg="yellow")
                click.echo("The example may fail without proper configuration.\n")
            
            # Run the example
            result = subprocess.run(
                [sys.executable, temp_path],
                capture_output=True,
                text=True
            )
            
            if result.stdout:
                click.echo(result.stdout)
            if result.stderr:
                click.secho(result.stderr, fg="red")
            
            # Cleanup
            Path(temp_path).unlink()
            
            if result.returncode == 0:
                click.secho("\n✓ Example completed successfully!", fg="green")
            else:
                click.secho(f"\n✗ Example failed with exit code {result.returncode}", fg="red")
        
        except Exception as e:
            click.secho(f"\n✗ Error running example: {str(e)}", fg="red")
            raise click.Abort()


@examples.command()
@click.argument("query")
def search(query: str):
    """Search examples by keyword.
    
    Examples:
        azcore examples search rl
        azcore examples search team
        azcore examples search cache
    """
    query = query.lower()
    matches = []
    
    for key, example in EXAMPLES.items():
        # Search in name, description, and tags
        searchable = (
            example['name'].lower() + " " +
            example['description'].lower() + " " +
            " ".join(example['tags'])
        )
        
        if query in searchable:
            matches.append((key, example))
    
    if not matches:
        click.secho(f"No examples found matching '{query}'", fg="yellow")
        click.echo("\nTry: azcore examples list")
        return
    
    click.secho(f"\n🔍 Found {len(matches)} example(s) matching '{query}':\n", fg="cyan", bold=True)
    
    for key, example in matches:
        click.secho(f"  • {example['name']}", fg="green", bold=True)
        click.echo(f"    ID: {key}")
        click.echo(f"    {example['description']}")
        click.echo()
    
    click.echo("To view: azcore examples show <id>")
    click.echo("To run:  azcore examples run <id>\n")


def _filter_examples(tags: tuple, difficulty: Optional[str]) -> Dict[str, Any]:
    """Filter examples by tags and difficulty."""
    filtered = {}
    
    for key, example in EXAMPLES.items():
        # Filter by difficulty
        if difficulty and example['difficulty'] != difficulty:
            continue
        
        # Filter by tags
        if tags:
            example_tags = set(example['tags'])
            if not any(tag in example_tags for tag in tags):
                continue
        
        filtered[key] = example
    
    return filtered


def _get_sample_config() -> str:
    """Get a sample configuration file."""
    return """# Az-Core Configuration

llm:
  model: gpt-4o-mini
  temperature: 0.7

fast_llm:
  model: gpt-4o-mini
  temperature: 0.5

coordinator_llm:
  model: gpt-4o-mini
  temperature: 0

embedding_model: text-embedding-3-large

# Add your API keys in .env file:
# OPENAI_API_KEY=your-key-here
"""
