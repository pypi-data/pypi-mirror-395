"""
Enhanced agent management CLI commands.

Provides interactive commands for creating, managing, and monitoring agents
with better UX including colored output, progress indicators, and token tracking.
"""

import click
import json
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime
import sys

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.prompt import Prompt, Confirm
    from rich.syntax import Syntax
    from rich import print as rprint
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    Console = None

from azcore.utils.agent_persistence import AgentPersistence
from azcore.agents import create_enhanced_agent, create_simple_agent
from azcore.middleware import SubAgentSpec


# Agent registry file
AGENT_REGISTRY_FILE = Path.home() / ".azcore" / "agent_registry.json"


class AgentRegistry:
    """Manage registered agents."""
    
    def __init__(self):
        self.registry_file = AGENT_REGISTRY_FILE
        self.registry_file.parent.mkdir(parents=True, exist_ok=True)
        
    def load(self) -> Dict[str, Any]:
        """Load agent registry."""
        if not self.registry_file.exists():
            return {"agents": {}, "created_at": datetime.now().isoformat()}
        
        with open(self.registry_file) as f:
            return json.load(f)
    
    def save(self, data: Dict[str, Any]) -> None:
        """Save agent registry."""
        data["updated_at"] = datetime.now().isoformat()
        with open(self.registry_file, "w") as f:
            json.dump(data, f, indent=2)
    
    def add_agent(self, name: str, config: Dict[str, Any]) -> None:
        """Add agent to registry."""
        registry = self.load()
        registry["agents"][name] = {
            **config,
            "created_at": datetime.now().isoformat(),
            "last_used": None,
            "run_count": 0,
            "total_tokens": 0
        }
        self.save(registry)
    
    def remove_agent(self, name: str) -> bool:
        """Remove agent from registry."""
        registry = self.load()
        if name in registry["agents"]:
            del registry["agents"][name]
            self.save(registry)
            return True
        return False
    
    def get_agent(self, name: str) -> Optional[Dict[str, Any]]:
        """Get agent configuration."""
        registry = self.load()
        return registry["agents"].get(name)
    
    def list_agents(self) -> List[Dict[str, Any]]:
        """List all agents."""
        registry = self.load()
        agents = []
        for name, config in registry["agents"].items():
            agents.append({"name": name, **config})
        return agents
    
    def update_stats(self, name: str, tokens: int = 0) -> None:
        """Update agent usage statistics."""
        registry = self.load()
        if name in registry["agents"]:
            registry["agents"][name]["last_used"] = datetime.now().isoformat()
            registry["agents"][name]["run_count"] += 1
            registry["agents"][name]["total_tokens"] += tokens
            self.save(registry)


def get_console():
    """Get Rich console or fallback."""
    if RICH_AVAILABLE:
        return Console()
    return None


@click.group(name="agent")
def agent():
    """Manage agents: create, list, reset, and monitor.
    
    Enhanced commands with interactive prompts, colored output,
    and token tracking for better agent management.
    
    Examples:
        azcore agent create --interactive
        azcore agent list
        azcore agent show my_agent
        azcore agent reset my_agent
        azcore agent stats
    """
    pass


@agent.command()
@click.option("--name", "-n", help="Agent name")
@click.option("--type", "-t", 
              type=click.Choice(["enhanced", "simple"]),
              default="enhanced",
              help="Agent type")
@click.option("--model", "-m", help="LLM model name")
@click.option("--prompt", "-p", help="System prompt")
@click.option("--interactive", "-i", is_flag=True, 
              help="Interactive creation with prompts")
@click.option("--enable-filesystem/--no-filesystem", default=True,
              help="Enable file operations")
@click.option("--enable-memory/--no-memory", default=True,
              help="Enable long-term memory")
@click.option("--enable-subagents/--no-subagents", default=True,
              help="Enable subagent delegation")
@click.option("--enable-shell/--no-shell", default=True,
              help="Enable shell commands")
@click.option("--enable-hitl/--no-hitl", default=False,
              help="Enable human-in-the-loop")
@click.option("--workspace", "-w", type=click.Path(),
              help="Workspace root directory")
@click.option("--output", "-o", type=click.Path(),
              help="Output configuration file")
def create(
    name: Optional[str],
    type: str,
    model: Optional[str],
    prompt: Optional[str],
    interactive: bool,
    enable_filesystem: bool,
    enable_memory: bool,
    enable_subagents: bool,
    enable_shell: bool,
    enable_hitl: bool,
    workspace: Optional[str],
    output: Optional[str]
):
    """Create a new agent with configuration.
    
    Examples:
        azcore agent create -i                    # Interactive mode
        azcore agent create -n my_agent -m gpt-4  # Quick creation
        azcore agent create -n secure --enable-hitl  # With HITL
    """
    console = get_console()
    registry = AgentRegistry()
    
    # Interactive mode
    if interactive:
        if RICH_AVAILABLE:
            _interactive_create(console, registry)
        else:
            click.echo("⚠️  Rich library not installed. Using basic mode.")
            _basic_interactive_create(registry)
        return
    
    # Validate required options
    if not name:
        click.secho("❌ Error: --name is required (or use --interactive)", fg="red")
        raise click.Abort()
    
    if not model:
        click.secho("❌ Error: --model is required (or use --interactive)", fg="red")
        raise click.Abort()
    
    # Create agent configuration
    config = {
        "type": type,
        "model": model,
        "prompt": prompt or "You are a helpful AI assistant.",
        "features": {
            "filesystem": enable_filesystem,
            "memory": enable_memory,
            "subagents": enable_subagents,
            "shell": enable_shell,
            "hitl": enable_hitl
        },
        "workspace": workspace or str(Path.cwd())
    }
    
    # Save to registry
    registry.add_agent(name, config)
    
    # Display success
    if console:
        console.print(f"\n[green]✓[/green] Agent '{name}' created successfully!")
        console.print(f"[dim]Type: {type}[/dim]")
        console.print(f"[dim]Model: {model}[/dim]")
        console.print(f"[dim]Features: {', '.join(k for k, v in config['features'].items() if v)}[/dim]")
    else:
        click.secho(f"\n✓ Agent '{name}' created successfully!", fg="green")
        click.echo(f"Type: {type}")
        click.echo(f"Model: {model}")
    
    # Export configuration if requested
    if output:
        output_path = Path(output)
        with open(output_path, "w") as f:
            json.dump(config, f, indent=2)
        
        if console:
            console.print(f"[dim]Configuration saved to: {output_path}[/dim]")
        else:
            click.echo(f"Configuration saved to: {output_path}")


@agent.command(name="list")
@click.option("--format", "-f",
              type=click.Choice(["table", "json", "simple"]),
              default="table",
              help="Output format")
@click.option("--filter", "-F", help="Filter by agent type or feature")
def list_agents(format: str, filter: Optional[str]):
    """List all registered agents.
    
    Examples:
        azcore agent list                 # Table view
        azcore agent list -f json         # JSON output
        azcore agent list --filter hitl   # Filter agents with HITL
    """
    console = get_console()
    registry = AgentRegistry()
    agents = registry.list_agents()
    
    if not agents:
        if console:
            console.print("[yellow]No agents registered yet.[/yellow]")
            console.print("\nCreate one with: [cyan]azcore agent create -i[/cyan]")
        else:
            click.echo("No agents registered yet.")
            click.echo("\nCreate one with: azcore agent create -i")
        return
    
    # Apply filter
    if filter:
        filter_lower = filter.lower()
        agents = [
            a for a in agents
            if filter_lower in a.get("type", "").lower()
            or filter_lower in str(a.get("features", {})).lower()
        ]
    
    # Output based on format
    if format == "json":
        click.echo(json.dumps(agents, indent=2))
    elif format == "table" and console:
        _display_agents_table(console, agents)
    else:
        _display_agents_simple(agents)


@agent.command()
@click.argument("name")
def show(name: str):
    """Show detailed agent information.
    
    Examples:
        azcore agent show my_agent
    """
    console = get_console()
    registry = AgentRegistry()
    agent_config = registry.get_agent(name)
    
    if not agent_config:
        if console:
            console.print(f"[red]❌ Agent '{name}' not found[/red]")
        else:
            click.secho(f"❌ Agent '{name}' not found", fg="red")
        return
    
    if console:
        _display_agent_details(console, name, agent_config)
    else:
        _display_agent_details_simple(name, agent_config)


@agent.command()
@click.argument("name")
@click.option("--confirm/--no-confirm", default=True,
              help="Ask for confirmation")
def reset(name: str, confirm: bool):
    """Reset agent state and statistics.
    
    This clears the agent's conversation history, checkpoints,
    and usage statistics while keeping the configuration.
    
    Examples:
        azcore agent reset my_agent
        azcore agent reset my_agent --no-confirm
    """
    console = get_console()
    registry = AgentRegistry()
    agent_config = registry.get_agent(name)
    
    if not agent_config:
        if console:
            console.print(f"[red]❌ Agent '{name}' not found[/red]")
        else:
            click.secho(f"❌ Agent '{name}' not found", fg="red")
        return
    
    # Confirm reset
    if confirm:
        if console:
            confirmed = Confirm.ask(
                f"[yellow]Reset agent '{name}'? This will clear all history and statistics.[/yellow]"
            )
        else:
            confirmed = click.confirm(
                f"Reset agent '{name}'? This will clear all history and statistics.",
                default=False
            )
        
        if not confirmed:
            click.echo("Reset cancelled.")
            return
    
    # Reset statistics
    agent_config["run_count"] = 0
    agent_config["total_tokens"] = 0
    agent_config["last_used"] = None
    
    # Update registry
    reg_data = registry.load()
    reg_data["agents"][name] = agent_config
    registry.save(reg_data)
    
    # Clean up state files
    state_dir = Path.home() / ".azcore" / "agent_states" / name
    if state_dir.exists():
        import shutil
        shutil.rmtree(state_dir)
        state_dir.mkdir(parents=True, exist_ok=True)
    
    if console:
        console.print(f"[green]✓ Agent '{name}' reset successfully[/green]")
    else:
        click.secho(f"✓ Agent '{name}' reset successfully", fg="green")


@agent.command()
@click.argument("name")
@click.option("--confirm/--no-confirm", default=True,
              help="Ask for confirmation")
def delete(name: str, confirm: bool):
    """Delete an agent from the registry.
    
    Examples:
        azcore agent delete my_agent
        azcore agent delete old_agent --no-confirm
    """
    console = get_console()
    registry = AgentRegistry()
    agent_config = registry.get_agent(name)
    
    if not agent_config:
        if console:
            console.print(f"[red]❌ Agent '{name}' not found[/red]")
        else:
            click.secho(f"❌ Agent '{name}' not found", fg="red")
        return
    
    # Confirm deletion
    if confirm:
        if console:
            confirmed = Confirm.ask(
                f"[red]Delete agent '{name}'? This cannot be undone.[/red]"
            )
        else:
            confirmed = click.confirm(
                f"Delete agent '{name}'? This cannot be undone.",
                default=False
            )
        
        if not confirmed:
            click.echo("Deletion cancelled.")
            return
    
    # Remove from registry
    registry.remove_agent(name)
    
    # Clean up state files
    state_dir = Path.home() / ".azcore" / "agent_states" / name
    if state_dir.exists():
        import shutil
        shutil.rmtree(state_dir)
    
    if console:
        console.print(f"[green]✓ Agent '{name}' deleted successfully[/green]")
    else:
        click.secho(f"✓ Agent '{name}' deleted successfully", fg="green")


@agent.command()
@click.option("--sort-by", "-s",
              type=click.Choice(["name", "runs", "tokens", "created"]),
              default="runs",
              help="Sort criterion")
def stats(sort_by: str):
    """Show agent usage statistics and token tracking.
    
    Examples:
        azcore agent stats                # Default sort by runs
        azcore agent stats -s tokens      # Sort by token usage
        azcore agent stats -s created     # Sort by creation date
    """
    console = get_console()
    registry = AgentRegistry()
    agents = registry.list_agents()
    
    if not agents:
        if console:
            console.print("[yellow]No agents registered yet.[/yellow]")
        else:
            click.echo("No agents registered yet.")
        return
    
    # Sort agents
    if sort_by == "runs":
        agents.sort(key=lambda a: a.get("run_count", 0), reverse=True)
    elif sort_by == "tokens":
        agents.sort(key=lambda a: a.get("total_tokens", 0), reverse=True)
    elif sort_by == "created":
        agents.sort(key=lambda a: a.get("created_at", ""), reverse=True)
    else:  # name
        agents.sort(key=lambda a: a["name"])
    
    # Calculate totals
    total_runs = sum(a.get("run_count", 0) for a in agents)
    total_tokens = sum(a.get("total_tokens", 0) for a in agents)
    
    if console:
        _display_stats_table(console, agents, total_runs, total_tokens)
    else:
        _display_stats_simple(agents, total_runs, total_tokens)


# Helper functions for Rich display

def _interactive_create(console, registry):
    """Interactive agent creation with Rich."""
    console.print(Panel.fit(
        "[bold cyan]Interactive Agent Creation[/bold cyan]\n"
        "Answer the following questions to create your agent.",
        border_style="cyan"
    ))
    
    # Get agent name
    name = Prompt.ask("\n[cyan]Agent name[/cyan]", default="my_agent")
    
    # Check if exists
    if registry.get_agent(name):
        if not Confirm.ask(f"[yellow]Agent '{name}' exists. Overwrite?[/yellow]"):
            console.print("[red]Creation cancelled[/red]")
            return
    
    # Get agent type
    agent_type = Prompt.ask(
        "[cyan]Agent type[/cyan]",
        choices=["enhanced", "simple"],
        default="enhanced"
    )
    
    # Get model
    model = Prompt.ask(
        "[cyan]LLM model[/cyan]",
        default="gpt-4"
    )
    
    # Get system prompt
    prompt = Prompt.ask(
        "[cyan]System prompt[/cyan]",
        default="You are a helpful AI assistant."
    )
    
    # Get features (only for enhanced)
    features = {}
    if agent_type == "enhanced":
        console.print("\n[bold]Enable features:[/bold]")
        features["filesystem"] = Confirm.ask("[cyan]• File operations?[/cyan]", default=True)
        features["memory"] = Confirm.ask("[cyan]• Long-term memory?[/cyan]", default=True)
        features["subagents"] = Confirm.ask("[cyan]• Subagent delegation?[/cyan]", default=True)
        features["shell"] = Confirm.ask("[cyan]• Shell commands?[/cyan]", default=True)
        features["hitl"] = Confirm.ask("[cyan]• Human-in-the-loop approval?[/cyan]", default=False)
    else:
        features = {"filesystem": True, "todolist": True, "patch": True}
    
    # Get workspace
    workspace = Prompt.ask(
        "[cyan]Workspace directory[/cyan]",
        default=str(Path.cwd())
    )
    
    # Create configuration
    config = {
        "type": agent_type,
        "model": model,
        "prompt": prompt,
        "features": features,
        "workspace": workspace
    }
    
    # Save to registry
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task("Creating agent...", total=None)
        registry.add_agent(name, config)
    
    # Display success
    console.print(f"\n[green]✓ Agent '{name}' created successfully![/green]")
    console.print(Panel(
        f"[bold]Name:[/bold] {name}\n"
        f"[bold]Type:[/bold] {agent_type}\n"
        f"[bold]Model:[/bold] {model}\n"
        f"[bold]Features:[/bold] {', '.join(k for k, v in features.items() if v)}\n"
        f"[bold]Workspace:[/bold] {workspace}",
        title="Agent Configuration",
        border_style="green"
    ))


def _basic_interactive_create(registry):
    """Basic interactive creation without Rich."""
    click.echo("\n=== Interactive Agent Creation ===\n")
    
    name = click.prompt("Agent name", default="my_agent")
    
    if registry.get_agent(name):
        if not click.confirm(f"Agent '{name}' exists. Overwrite?"):
            click.echo("Creation cancelled")
            return
    
    agent_type = click.prompt(
        "Agent type",
        type=click.Choice(["enhanced", "simple"]),
        default="enhanced"
    )
    
    model = click.prompt("LLM model", default="gpt-4")
    prompt = click.prompt("System prompt", default="You are a helpful AI assistant.")
    
    features = {}
    if agent_type == "enhanced":
        click.echo("\nEnable features:")
        features["filesystem"] = click.confirm("• File operations?", default=True)
        features["memory"] = click.confirm("• Long-term memory?", default=True)
        features["subagents"] = click.confirm("• Subagent delegation?", default=True)
        features["shell"] = click.confirm("• Shell commands?", default=True)
        features["hitl"] = click.confirm("• Human-in-the-loop?", default=False)
    
    workspace = click.prompt("Workspace directory", default=str(Path.cwd()))
    
    config = {
        "type": agent_type,
        "model": model,
        "prompt": prompt,
        "features": features,
        "workspace": workspace
    }
    
    registry.add_agent(name, config)
    click.secho(f"\n✓ Agent '{name}' created successfully!", fg="green")


def _display_agents_table(console, agents):
    """Display agents in a Rich table."""
    table = Table(title="Registered Agents", show_header=True, header_style="bold cyan")
    table.add_column("Name", style="cyan")
    table.add_column("Type")
    table.add_column("Model")
    table.add_column("Features")
    table.add_column("Runs", justify="right")
    table.add_column("Tokens", justify="right")
    
    for agent in agents:
        features = agent.get("features", {})
        feature_list = ", ".join(k for k, v in features.items() if v)
        
        table.add_row(
            agent["name"],
            agent.get("type", "unknown"),
            agent.get("model", "unknown"),
            feature_list[:30] + "..." if len(feature_list) > 30 else feature_list,
            str(agent.get("run_count", 0)),
            f"{agent.get('total_tokens', 0):,}"
        )
    
    console.print(table)


def _display_agents_simple(agents):
    """Display agents in simple format."""
    click.echo("\n=== Registered Agents ===\n")
    for agent in agents:
        click.echo(f"• {agent['name']}")
        click.echo(f"  Type: {agent.get('type', 'unknown')}")
        click.echo(f"  Model: {agent.get('model', 'unknown')}")
        click.echo(f"  Runs: {agent.get('run_count', 0)}")
        click.echo()


def _display_agent_details(console, name, config):
    """Display agent details with Rich."""
    features = config.get("features", {})
    feature_list = "\n".join(f"• {k}: {'✓' if v else '✗'}" for k, v in features.items())
    
    console.print(Panel(
        f"[bold]Type:[/bold] {config.get('type', 'unknown')}\n"
        f"[bold]Model:[/bold] {config.get('model', 'unknown')}\n"
        f"[bold]Created:[/bold] {config.get('created_at', 'unknown')}\n"
        f"[bold]Last used:[/bold] {config.get('last_used', 'never')}\n"
        f"[bold]Runs:[/bold] {config.get('run_count', 0)}\n"
        f"[bold]Tokens:[/bold] {config.get('total_tokens', 0):,}\n"
        f"[bold]Workspace:[/bold] {config.get('workspace', 'unknown')}\n\n"
        f"[bold]Features:[/bold]\n{feature_list}\n\n"
        f"[bold]System Prompt:[/bold]\n{config.get('prompt', 'N/A')}",
        title=f"Agent: {name}",
        border_style="cyan"
    ))


def _display_agent_details_simple(name, config):
    """Display agent details in simple format."""
    click.echo(f"\n=== Agent: {name} ===\n")
    click.echo(f"Type: {config.get('type', 'unknown')}")
    click.echo(f"Model: {config.get('model', 'unknown')}")
    click.echo(f"Created: {config.get('created_at', 'unknown')}")
    click.echo(f"Last used: {config.get('last_used', 'never')}")
    click.echo(f"Runs: {config.get('run_count', 0)}")
    click.echo(f"Tokens: {config.get('total_tokens', 0):,}")
    click.echo(f"\nSystem Prompt:\n{config.get('prompt', 'N/A')}")


def _display_stats_table(console, agents, total_runs, total_tokens):
    """Display statistics in a Rich table."""
    table = Table(title="Agent Statistics", show_header=True, header_style="bold cyan")
    table.add_column("Agent", style="cyan")
    table.add_column("Type")
    table.add_column("Runs", justify="right")
    table.add_column("Tokens", justify="right")
    table.add_column("Avg Tokens/Run", justify="right")
    table.add_column("Last Used")
    
    for agent in agents:
        runs = agent.get("run_count", 0)
        tokens = agent.get("total_tokens", 0)
        avg_tokens = tokens // runs if runs > 0 else 0
        last_used = agent.get("last_used", "never")
        if last_used != "never":
            # Format datetime
            try:
                dt = datetime.fromisoformat(last_used)
                last_used = dt.strftime("%Y-%m-%d %H:%M")
            except:
                pass
        
        table.add_row(
            agent["name"],
            agent.get("type", "unknown"),
            str(runs),
            f"{tokens:,}",
            f"{avg_tokens:,}",
            last_used
        )
    
    console.print(table)
    console.print(f"\n[bold]Total Runs:[/bold] {total_runs:,}")
    console.print(f"[bold]Total Tokens:[/bold] {total_tokens:,}")


def _display_stats_simple(agents, total_runs, total_tokens):
    """Display statistics in simple format."""
    click.echo("\n=== Agent Statistics ===\n")
    for agent in agents:
        runs = agent.get("run_count", 0)
        tokens = agent.get("total_tokens", 0)
        click.echo(f"• {agent['name']}")
        click.echo(f"  Runs: {runs}")
        click.echo(f"  Tokens: {tokens:,}")
        click.echo()
    
    click.echo(f"Total Runs: {total_runs:,}")
    click.echo(f"Total Tokens: {total_tokens:,}")


# Export
__all__ = ["agent"]
