"""Run Az-Core workflows and agents."""

import os
import sys
import click
import importlib.util
from pathlib import Path
from typing import Optional
from azcore.cli.error_handler import (
    handle_cli_error,
    show_error,
    show_warning,
    validate_required_env_vars
)


@click.command()
@click.argument("file", type=click.Path(exists=True))
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True),
    help="Configuration file path",
)
@click.option(
    "--env",
    "-e",
    type=click.Path(exists=True),
    help="Environment file path",
)
@click.option(
    "--debug",
    "-d",
    is_flag=True,
    help="Enable debug logging",
)
@click.option(
    "--input",
    "-i",
    help="Input query/prompt to run",
)
@handle_cli_error
def run(file: str, config: Optional[str], env: Optional[str], debug: bool, input: Optional[str]):
    """Run an Az-Core workflow or agent.
    
    Examples:
        azcore run workflow.py
        azcore run main.py --config config.yml --input "Hello"
        azcore run agent.py --debug
    """
    file_path = Path(file).absolute()
    
    # Load environment variables if provided
    if env:
        from dotenv import load_dotenv
        load_dotenv(env)
        click.echo(f"Loaded environment from: {env}")
    
    # Set debug logging if requested
    if debug:
        os.environ["AZCORE_LOG_LEVEL"] = "DEBUG"
        click.echo("Debug logging enabled")
    
    # Load config if provided
    if config:
        os.environ["AZCORE_CONFIG_PATH"] = str(Path(config).absolute())
        click.echo(f"Using config: {config}")
    
    # Add input to environment if provided
    if input:
        os.environ["AZCORE_INPUT_QUERY"] = input
    
    click.echo(f"\nRunning: {file_path.name}\n")
    click.secho("=" * 60, fg="cyan")
    
    try:
        # Import and run the file
        spec = importlib.util.spec_from_file_location("__main__", file_path)
        if spec is None or spec.loader is None:
            click.secho(f"Error: Could not load file '{file_path}'", fg="red")
            sys.exit(1)
        
        module = importlib.util.module_from_spec(spec)
        sys.modules["__main__"] = module
        
        # Add file directory to sys.path
        sys.path.insert(0, str(file_path.parent))
        
        spec.loader.exec_module(module)
        
        click.secho("\n" + "=" * 60, fg="cyan")
        click.secho("✓ Execution completed successfully!", fg="green")
        
    except KeyboardInterrupt:
        click.secho("\n\nExecution interrupted by user", fg="yellow")
        sys.exit(130)
    except Exception as e:
        click.secho("\n" + "=" * 60, fg="cyan")
        click.secho(f"✗ Execution failed with error:", fg="red")
        click.secho(f"  {type(e).__name__}: {str(e)}", fg="red")
        if debug:
            import traceback
            click.echo("\nFull traceback:")
            traceback.print_exc()
        sys.exit(1)
