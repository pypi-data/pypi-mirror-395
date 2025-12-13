"""Scaffolding commands for creating agents and workflows."""

import click
from pathlib import Path
from typing import Optional

from azcore.cli.scaffolding import (
    create_agent_file,
    create_workflow_file,
    create_node_file,
)


@click.group()
def create():
    """Create new agents, workflows, and components.
    
    Examples:
        azcore create agent MyAgent --pattern react
        azcore create workflow MyWorkflow --type sequential
        azcore create node CustomNode
    """
    pass


@create.command()
@click.argument("name")
@click.option(
    "--pattern",
    "-p",
    type=click.Choice([
        "react",
        "reflexion",
        "reasoning-duo",
        "self-consistency",
        "basic",
    ]),
    default="react",
    help="Agent pattern to use",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Output file path",
)
@click.option(
    "--with-rl",
    is_flag=True,
    help="Include RL optimization",
)
@click.option(
    "--with-tools",
    is_flag=True,
    help="Include tool integration",
)
def agent(name: str, pattern: str, output: Optional[str], with_rl: bool, with_tools: bool):
    """Create a new agent.
    
    Examples:
        azcore create agent MyAgent --pattern react
        azcore create agent ResearchAgent -p reasoning-duo --with-rl
        azcore create agent ToolAgent --pattern basic --with-tools
    """
    output_path = Path(output) if output else Path(f"{name.lower()}_agent.py")
    
    click.echo(f"Creating {pattern} agent: {name}")
    click.echo(f"Output: {output_path}\n")
    
    try:
        content = create_agent_file(
            name=name,
            pattern=pattern,
            with_rl=with_rl,
            with_tools=with_tools,
        )
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        click.secho(f"✓ Agent created successfully: {output_path}", fg="green")
        click.echo("\nNext steps:")
        click.echo(f"  1. Edit {output_path} to customize your agent")
        click.echo(f"  2. Run with: azcore run {output_path}")
        
    except Exception as e:
        click.secho(f"✗ Failed to create agent: {str(e)}", fg="red")
        raise click.Abort()


@create.command()
@click.argument("name")
@click.option(
    "--type",
    "-t",
    type=click.Choice([
        "sequential",
        "concurrent",
        "graph",
        "hierarchical",
        "swarm",
        "forest",
    ]),
    default="sequential",
    help="Workflow type",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Output file path",
)
@click.option(
    "--num-agents",
    "-n",
    type=int,
    default=3,
    help="Number of agents in workflow",
)
def workflow(name: str, type: str, output: Optional[str], num_agents: int):
    """Create a new workflow.
    
    Examples:
        azcore create workflow MyWorkflow --type sequential
        azcore create workflow TeamWorkflow -t hierarchical -n 5
        azcore create workflow SwarmWorkflow --type swarm
    """
    output_path = Path(output) if output else Path(f"{name.lower()}_workflow.py")
    
    click.echo(f"Creating {type} workflow: {name}")
    click.echo(f"Agents: {num_agents}")
    click.echo(f"Output: {output_path}\n")
    
    try:
        content = create_workflow_file(
            name=name,
            workflow_type=type,
            num_agents=num_agents,
        )
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        click.secho(f"✓ Workflow created successfully: {output_path}", fg="green")
        click.echo("\nNext steps:")
        click.echo(f"  1. Edit {output_path} to customize your workflow")
        click.echo(f"  2. Add your agent logic")
        click.echo(f"  3. Run with: azcore run {output_path}")
        
    except Exception as e:
        click.secho(f"✗ Failed to create workflow: {str(e)}", fg="red")
        raise click.Abort()


@create.command()
@click.argument("name")
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Output file path",
)
@click.option(
    "--base",
    "-b",
    type=click.Choice(["base", "planner", "generator", "validator"]),
    default="base",
    help="Base node type",
)
def node(name: str, output: Optional[str], base: str):
    """Create a new custom node.
    
    Examples:
        azcore create node CustomNode
        azcore create node DataProcessor --base generator
        azcore create node Validator --base validator
    """
    output_path = Path(output) if output else Path(f"{name.lower()}_node.py")
    
    click.echo(f"Creating custom node: {name}")
    click.echo(f"Base type: {base}")
    click.echo(f"Output: {output_path}\n")
    
    try:
        content = create_node_file(
            name=name,
            base_type=base,
        )
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        click.secho(f"✓ Node created successfully: {output_path}", fg="green")
        click.echo("\nNext steps:")
        click.echo(f"  1. Edit {output_path} to implement your node logic")
        click.echo(f"  2. Integrate into your workflow")
        
    except Exception as e:
        click.secho(f"✗ Failed to create node: {str(e)}", fg="red")
        raise click.Abort()
