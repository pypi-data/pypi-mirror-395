"""Train RL agents."""

import click
import yaml
from pathlib import Path
from typing import Optional


@click.command()
@click.argument("agent_type", type=click.Choice(["rl-agent", "tool-selector"]))
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True),
    required=True,
    help="Training configuration file",
)
@click.option(
    "--episodes",
    "-e",
    type=int,
    default=100,
    help="Number of training episodes",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    default="./models",
    help="Output directory for trained models",
)
@click.option(
    "--resume",
    "-r",
    type=click.Path(exists=True),
    help="Resume training from checkpoint",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Verbose output",
)
def train(
    agent_type: str,
    config: str,
    episodes: int,
    output: str,
    resume: Optional[str],
    verbose: bool,
):
    """Train RL agents with synthetic data.
    
    Examples:
        azcore train rl-agent --config rl_config.yml
        azcore train tool-selector -c config.yml -e 500 -o ./my_models
        azcore train rl-agent -c config.yml --resume ./models/checkpoint.pkl
    """
    from azcore.rl.rl_manager import RLManager
    from azcore.rl.synthetic_data.training_pipeline import TrainingPipeline
    
    click.echo(f"Training {agent_type}...")
    click.echo(f"Config: {config}")
    click.echo(f"Episodes: {episodes}")
    click.echo(f"Output: {output}\n")
    
    # Load config
    config_path = Path(config)
    with open(config_path, "r") as f:
        training_config = yaml.safe_load(f)
    
    output_path = Path(output)
    output_path.mkdir(parents=True, exist_ok=True)
    
    if resume:
        click.echo(f"Resuming from checkpoint: {resume}")
    
    try:
        # Initialize training pipeline
        pipeline = TrainingPipeline(
            config=training_config,
            output_dir=str(output_path),
            verbose=verbose,
        )
        
        click.secho("Starting training...", fg="cyan")
        
        # Run training
        results = pipeline.train(
            num_episodes=episodes,
            checkpoint_path=resume,
        )
        
        click.secho("\n✓ Training completed successfully!", fg="green")
        click.echo(f"\nTraining Results:")
        click.echo(f"  Final Reward: {results.get('final_reward', 'N/A'):.4f}")
        click.echo(f"  Average Reward: {results.get('avg_reward', 'N/A'):.4f}")
        click.echo(f"  Total Episodes: {results.get('total_episodes', episodes)}")
        click.echo(f"  Model saved to: {output_path}")
        
        # Save training summary
        summary_path = output_path / "training_summary.txt"
        with open(summary_path, "w") as f:
            f.write(f"Training Summary\n")
            f.write(f"================\n")
            f.write(f"Agent Type: {agent_type}\n")
            f.write(f"Episodes: {episodes}\n")
            f.write(f"Final Reward: {results.get('final_reward', 'N/A')}\n")
            f.write(f"Average Reward: {results.get('avg_reward', 'N/A')}\n")
        
        click.echo(f"\nSummary saved to: {summary_path}")
        
    except KeyboardInterrupt:
        click.secho("\nTraining interrupted by user", fg="yellow")
        click.echo("Progress has been saved.")
    except Exception as e:
        click.secho(f"\n✗ Training failed: {str(e)}", fg="red")
        if verbose:
            import traceback
            traceback.print_exc()
        raise click.Abort()
