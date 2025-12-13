"""Display Az-Core statistics and metrics."""

import click
import json
from pathlib import Path
from typing import Optional, Dict, Any
import pickle


@click.command()
@click.option(
    "--show-rl-metrics",
    is_flag=True,
    help="Show RL training metrics",
)
@click.option(
    "--show-cache-stats",
    is_flag=True,
    help="Show cache statistics",
)
@click.option(
    "--show-agent-stats",
    is_flag=True,
    help="Show agent execution statistics",
)
@click.option(
    "--data-dir",
    "-d",
    type=click.Path(exists=True),
    default="./data",
    help="Data directory path",
)
@click.option(
    "--format",
    "-f",
    type=click.Choice(["table", "json", "simple"]),
    default="table",
    help="Output format",
)
@click.option(
    "--export",
    "-e",
    type=click.Path(),
    help="Export stats to file",
)
@click.option(
    "--tips",
    "-t",
    is_flag=True,
    help="Show productivity tips based on usage patterns",
)
def stats(
    show_rl_metrics: bool,
    show_cache_stats: bool,
    show_agent_stats: bool,
    data_dir: str,
    format: str,
    export: Optional[str],
    tips: bool,
):
    """Display Az-Core statistics and metrics.
    
    Examples:
        azcore stats --show-rl-metrics
        azcore stats --show-cache-stats --format json
        azcore stats --show-rl-metrics --export stats.json
        azcore stats --tips
    """
    data_path = Path(data_dir)
    
    if not any([show_rl_metrics, show_cache_stats, show_agent_stats]):
        # Show all stats by default
        show_rl_metrics = True
        show_cache_stats = True
        show_agent_stats = True
    
    all_stats = {}
    
    click.echo(f"Az-Core Statistics")
    click.echo(f"Data Directory: {data_path.absolute()}")
    click.echo("=" * 70 + "\n")
    
    # RL Metrics
    if show_rl_metrics:
        rl_stats = _get_rl_metrics(data_path)
        all_stats["rl_metrics"] = rl_stats
        _display_rl_metrics(rl_stats, format)
    
    # Cache Statistics
    if show_cache_stats:
        cache_stats = _get_cache_stats(data_path)
        all_stats["cache_stats"] = cache_stats
        _display_cache_stats(cache_stats, format)
    
    # Agent Statistics
    if show_agent_stats:
        agent_stats = _get_agent_stats(data_path)
        all_stats["agent_stats"] = agent_stats
        _display_agent_stats(agent_stats, format)
    
    # Export if requested
    if export:
        export_path = Path(export)
        with open(export_path, "w") as f:
            json.dump(all_stats, f, indent=2, default=str)
        click.secho(f"\n✓ Stats exported to: {export_path}", fg="green")
    
    # Show productivity tips
    if tips:
        _show_productivity_tips(all_stats)


def _get_rl_metrics(data_path: Path) -> Dict[str, Any]:
    """Load RL metrics from Q-table and training logs."""
    stats = {
        "q_table_exists": False,
        "num_states": 0,
        "num_actions": 0,
        "total_updates": 0,
        "avg_q_value": 0.0,
    }
    
    # Check for Q-table
    q_table_path = data_path / "q_table.pkl"
    if q_table_path.exists():
        try:
            with open(q_table_path, "rb") as f:
                q_table = pickle.load(f)
            
            stats["q_table_exists"] = True
            stats["num_states"] = len(q_table)
            
            if q_table:
                # Get number of actions from first state
                first_state = next(iter(q_table.values()))
                stats["num_actions"] = len(first_state)
                
                # Calculate average Q-value
                all_q_values = [q for state in q_table.values() for q in state.values()]
                if all_q_values:
                    stats["avg_q_value"] = sum(all_q_values) / len(all_q_values)
        except Exception as e:
            stats["error"] = str(e)
    
    # Check for training logs
    log_path = data_path / "training_logs.json"
    if log_path.exists():
        try:
            with open(log_path, "r") as f:
                logs = json.load(f)
            stats["training_episodes"] = len(logs.get("episodes", []))
            stats["total_reward"] = logs.get("total_reward", 0)
        except Exception:
            pass
    
    return stats


def _get_cache_stats(data_path: Path) -> Dict[str, Any]:
    """Load cache statistics."""
    stats = {
        "cache_exists": False,
        "num_entries": 0,
        "cache_size_mb": 0.0,
        "hit_rate": 0.0,
    }
    
    cache_path = data_path / "cache"
    if cache_path.exists():
        stats["cache_exists"] = True
        
        # Count cache files
        cache_files = list(cache_path.glob("*.cache"))
        stats["num_entries"] = len(cache_files)
        
        # Calculate total size
        total_size = sum(f.stat().st_size for f in cache_files)
        stats["cache_size_mb"] = total_size / (1024 * 1024)
        
        # Load cache stats if available
        stats_path = cache_path / "stats.json"
        if stats_path.exists():
            try:
                with open(stats_path, "r") as f:
                    cache_stats = json.load(f)
                stats["hits"] = cache_stats.get("hits", 0)
                stats["misses"] = cache_stats.get("misses", 0)
                total = stats["hits"] + stats["misses"]
                if total > 0:
                    stats["hit_rate"] = stats["hits"] / total * 100
            except Exception:
                pass
    
    return stats


def _get_agent_stats(data_path: Path) -> Dict[str, Any]:
    """Load agent execution statistics."""
    stats = {
        "logs_exist": False,
        "total_executions": 0,
        "avg_execution_time": 0.0,
        "success_rate": 0.0,
    }
    
    logs_path = data_path / "agent_logs.json"
    if logs_path.exists():
        try:
            with open(logs_path, "r") as f:
                logs = json.load(f)
            
            stats["logs_exist"] = True
            executions = logs.get("executions", [])
            stats["total_executions"] = len(executions)
            
            if executions:
                times = [e.get("execution_time", 0) for e in executions]
                stats["avg_execution_time"] = sum(times) / len(times)
                
                successes = sum(1 for e in executions if e.get("success", False))
                stats["success_rate"] = successes / len(executions) * 100
        except Exception:
            pass
    
    return stats


def _display_rl_metrics(stats: Dict[str, Any], format: str):
    """Display RL metrics."""
    click.secho("RL Metrics", fg="cyan", bold=True)
    click.echo("-" * 70)
    
    if format == "json":
        click.echo(json.dumps(stats, indent=2))
    else:
        if stats["q_table_exists"]:
            click.echo(f"  Q-Table Status:      {'✓ Found' if stats['q_table_exists'] else '✗ Not Found'}")
            click.echo(f"  Number of States:    {stats['num_states']:,}")
            click.echo(f"  Number of Actions:   {stats['num_actions']:,}")
            click.echo(f"  Average Q-Value:     {stats['avg_q_value']:.4f}")
            if "training_episodes" in stats:
                click.echo(f"  Training Episodes:   {stats['training_episodes']:,}")
                click.echo(f"  Total Reward:        {stats.get('total_reward', 0):.2f}")
        else:
            click.secho("  No Q-table found", fg="yellow")
    
    click.echo()


def _display_cache_stats(stats: Dict[str, Any], format: str):
    """Display cache statistics."""
    click.secho("Cache Statistics", fg="cyan", bold=True)
    click.echo("-" * 70)
    
    if format == "json":
        click.echo(json.dumps(stats, indent=2))
    else:
        if stats["cache_exists"]:
            click.echo(f"  Cache Status:        {'✓ Active' if stats['cache_exists'] else '✗ Inactive'}")
            click.echo(f"  Cache Entries:       {stats['num_entries']:,}")
            click.echo(f"  Cache Size:          {stats['cache_size_mb']:.2f} MB")
            if "hits" in stats:
                click.echo(f"  Cache Hits:          {stats['hits']:,}")
                click.echo(f"  Cache Misses:        {stats['misses']:,}")
                click.echo(f"  Hit Rate:            {stats['hit_rate']:.1f}%")
        else:
            click.secho("  No cache found", fg="yellow")
    
    click.echo()


def _display_agent_stats(stats: Dict[str, Any], format: str):
    """Display agent statistics."""
    click.secho("Agent Statistics", fg="cyan", bold=True)
    click.echo("-" * 70)
    
    if format == "json":
        click.echo(json.dumps(stats, indent=2))
    else:
        if stats["logs_exist"]:
            click.echo(f"  Total Executions:    {stats['total_executions']:,}")
            click.echo(f"  Avg Execution Time:  {stats['avg_execution_time']:.2f}s")
            click.echo(f"  Success Rate:        {stats['success_rate']:.1f}%")
        else:
            click.secho("  No agent logs found", fg="yellow")
    
    click.echo()


def _show_productivity_tips(stats: Dict[str, Any]):
    """Show productivity tips based on usage statistics."""
    click.echo("\n" + "=" * 70)
    click.secho("💡 Productivity Tips", fg="yellow", bold=True)
    click.echo("=" * 70 + "\n")
    
    tips_shown = 0
    
    # Cache-related tips
    cache_stats = stats.get("cache_stats", {})
    if cache_stats.get("cache_exists"):
        hit_rate = cache_stats.get("hit_rate", 0)
        if hit_rate < 30:
            click.echo("📌 Tip: Your cache hit rate is low (<30%).")
            click.echo("   Consider using CachedLLM for frequently repeated queries.")
            click.echo("   Example: from azcore.utils import CachedLLM\n")
            tips_shown += 1
        elif hit_rate > 70:
            click.secho("✓ Great cache utilization! You're saving on API costs.", fg="green")
            tips_shown += 1
    else:
        click.echo("📌 Tip: Enable caching to reduce API costs and latency.")
        click.echo("   Use CachedLLM to cache LLM responses automatically.")
        click.echo("   Can save 50-80% on repeated queries!\n")
        tips_shown += 1
    
    # RL-related tips
    rl_stats = stats.get("rl_metrics", {})
    if rl_stats.get("q_table_exists"):
        num_states = rl_stats.get("num_states", 0)
        if num_states < 100:
            click.echo("📌 Tip: Your Q-table has few states. Consider:")
            click.echo("   • Generate more synthetic training data")
            click.echo("   • Run more training episodes")
            click.echo("   • Use: azcore train rl-agent --episodes 500\n")
            tips_shown += 1
        elif num_states > 1000:
            click.echo("📌 Tip: Large Q-table detected. Consider:")
            click.echo("   • Using embeddings for state representation")
            click.echo("   • Enable with: use_embeddings=True in RLManager\n")
            tips_shown += 1
    else:
        click.echo("📌 Tip: Try RL-powered agents for adaptive tool selection!")
        click.echo("   • Create with: azcore init --template rl-agent")
        click.echo("   • Or run: azcore examples show rl-agent\n")
        tips_shown += 1
    
    # Agent performance tips
    agent_stats = stats.get("agent_stats", {})
    if agent_stats.get("logs_exist"):
        success_rate = agent_stats.get("success_rate", 0)
        avg_time = agent_stats.get("avg_execution_time", 0)
        
        if success_rate < 70:
            click.echo("📌 Tip: Low success rate detected. Try:")
            click.echo("   • Add better error handling and retries")
            click.echo("   • Use validation nodes in your workflow")
            click.echo("   • Check agent prompts for clarity\n")
            tips_shown += 1
        
        if avg_time > 10:
            click.echo("📌 Tip: Long execution times detected. Consider:")
            click.echo("   • Using faster models for simple tasks (gpt-4o-mini)")
            click.echo("   • Enable streaming for better UX")
            click.echo("   • Break complex tasks into smaller agents\n")
            tips_shown += 1
    
    # General tips
    if tips_shown < 3:
        general_tips = [
            ("🎯", "Use 'azcore examples list' to discover pre-built patterns"),
            ("🔍", "Run 'azcore doctor' to check your environment setup"),
            ("📚", "Check out 'azcore create agent' for quick scaffolding"),
            ("🚀", "Use hierarchical teams for complex multi-step tasks"),
            ("💾", "Enable conversation persistence with checkpointers"),
            ("⚡", "Try concurrent workflows for independent tasks"),
        ]
        
        import random
        remaining = 3 - tips_shown
        for emoji, tip in random.sample(general_tips, min(remaining, len(general_tips))):
            click.echo(f"{emoji} Tip: {tip}\n")
            tips_shown += 1
    
    if tips_shown == 0:
        click.echo("No specific tips at this time. Keep up the good work! 🎉\n")
    
    click.echo("-" * 70)
    click.echo("Run 'azcore stats --tips' anytime for personalized suggestions.\n")
