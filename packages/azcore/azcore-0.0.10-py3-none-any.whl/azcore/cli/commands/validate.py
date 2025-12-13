"""Validate Az-Core configuration files."""

import click
import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional


@click.group()
def validate():
    """Validate Az-Core configuration and project files.
    
    Examples:
        azcore validate config config.yml
        azcore validate config config.yml --strict
        azcore validate project
    """
    pass


@validate.command()
@click.argument("config_file", type=click.Path(exists=True), required=False)
@click.option(
    "--strict",
    "-s",
    is_flag=True,
    help="Enable strict validation",
)
@click.option(
    "--fix",
    "-f",
    is_flag=True,
    help="Auto-fix common issues",
)
def config(config_file: Optional[str], strict: bool, fix: bool):
    """Validate configuration files.
    
    Examples:
        azcore validate config config.yml
        azcore validate config --strict
        azcore validate config --fix
    """
    # Default to config.yml if not specified
    if not config_file:
        if Path("config.yml").exists():
            config_file = "config.yml"
        elif Path("configs/config.yml").exists():
            config_file = "configs/config.yml"
        else:
            click.secho("Error: No config file found.", fg="red")
            click.echo("Specify a file: azcore validate config <file>")
            return
    from azcore.config.validation import validate_config_dict
    
    config_path = Path(config_file)
    click.echo(f"Validating configuration: {config_path.name}\n")
    
    try:
        # Load config file
        with open(config_path, "r") as f:
            config_data = yaml.safe_load(f)
        
        if config_data is None:
            click.secho("✗ Error: Configuration file is empty", fg="red")
            return
        
        # Validate configuration
        errors: List[str] = []
        warnings: List[str] = []
        
        # Run validation
        try:
            validate_config_dict(config_data)
            click.secho("✓ Schema validation passed", fg="green")
        except Exception as e:
            errors.append(f"Schema validation failed: {str(e)}")
        
        # Additional checks
        _check_required_fields(config_data, errors, warnings)
        _check_llm_config(config_data, errors, warnings)
        _check_rl_config(config_data, errors, warnings, strict)
        _check_workflow_config(config_data, errors, warnings)
        
        # Print results
        click.echo("\nValidation Results:")
        click.echo("=" * 60)
        
        if errors:
            click.secho(f"\nErrors ({len(errors)}):", fg="red", bold=True)
            for i, error in enumerate(errors, 1):
                click.secho(f"  {i}. {error}", fg="red")
        
        if warnings:
            click.secho(f"\nWarnings ({len(warnings)}):", fg="yellow", bold=True)
            for i, warning in enumerate(warnings, 1):
                click.secho(f"  {i}. {warning}", fg="yellow")
        
        if not errors and not warnings:
            click.secho("\n✓ Configuration is valid!", fg="green", bold=True)
            return
        
        # Auto-fix if requested
        if fix and not errors:
            click.echo("\nAttempting to auto-fix warnings...")
            fixed_config = _auto_fix_config(config_data, warnings)
            
            if fixed_config != config_data:
                backup_path = config_path.with_suffix(".yml.bak")
                config_path.rename(backup_path)
                
                with open(config_path, "w") as f:
                    yaml.dump(fixed_config, f, default_flow_style=False)
                
                click.secho(f"✓ Config fixed and saved", fg="green")
                click.echo(f"  Backup saved to: {backup_path}")
        
        # Exit with error code if there are errors
        if errors:
            raise click.Abort()
    
    except yaml.YAMLError as e:
        click.secho(f"✗ Invalid YAML syntax: {str(e)}", fg="red")
        raise click.Abort()
    except Exception as e:
        click.secho(f"✗ Validation failed: {str(e)}", fg="red")
        raise click.Abort()


def _check_required_fields(config: Dict[str, Any], errors: List[str], warnings: List[str]):
    """Check for required configuration fields."""
    if "llm" not in config and "model" not in config:
        errors.append("Missing required field: 'llm' or 'model'")
    
    if "agents" not in config and "workflow" not in config:
        warnings.append("No agents or workflow configured")


def _check_llm_config(config: Dict[str, Any], errors: List[str], warnings: List[str]):
    """Validate LLM configuration."""
    llm_config = config.get("llm") or config.get("model")
    
    if llm_config:
        if isinstance(llm_config, dict):
            if "provider" not in llm_config and "model_name" not in llm_config:
                warnings.append("LLM config missing 'provider' or 'model_name'")
            
            if "temperature" in llm_config:
                temp = llm_config["temperature"]
                if not (0 <= temp <= 2):
                    errors.append(f"Invalid temperature: {temp} (must be 0-2)")


def _check_rl_config(config: Dict[str, Any], errors: List[str], warnings: List[str], strict: bool):
    """Validate RL configuration."""
    rl_config = config.get("rl_config")
    
    if rl_config:
        # Check learning rate
        if "learning_rate" in rl_config:
            lr = rl_config["learning_rate"]
            if not (0 < lr <= 1):
                errors.append(f"Invalid learning_rate: {lr} (must be 0-1)")
        
        # Check discount factor
        if "discount_factor" in rl_config:
            gamma = rl_config["discount_factor"]
            if not (0 <= gamma <= 1):
                errors.append(f"Invalid discount_factor: {gamma} (must be 0-1)")
        
        # Check exploration strategy
        if "exploration_strategy" in rl_config:
            strategy = rl_config["exploration_strategy"]
            valid_strategies = ["epsilon_greedy", "ucb", "thompson_sampling"]
            if strategy not in valid_strategies:
                errors.append(f"Invalid exploration_strategy: {strategy}")
        
        if strict and "q_table_path" not in rl_config:
            warnings.append("RL config missing 'q_table_path' for persistence")


def _check_workflow_config(config: Dict[str, Any], errors: List[str], warnings: List[str]):
    """Validate workflow configuration."""
    workflow = config.get("workflow")
    
    if workflow:
        if isinstance(workflow, dict):
            workflow_type = workflow.get("type")
            if workflow_type:
                valid_types = ["sequential", "concurrent", "graph", "hierarchical", "swarm"]
                if workflow_type not in valid_types:
                    errors.append(f"Invalid workflow type: {workflow_type}")


def _auto_fix_config(config: Dict[str, Any], warnings: List[str]) -> Dict[str, Any]:
    """Attempt to auto-fix common configuration issues."""
    fixed_config = config.copy()
    
    # Add default RL config if missing
    if "rl_config" in config and "q_table_path" not in config["rl_config"]:
        fixed_config["rl_config"]["q_table_path"] = "./data/q_table.pkl"
    
    # Add default temperature if missing
    if "llm" in fixed_config and isinstance(fixed_config["llm"], dict):
        if "temperature" not in fixed_config["llm"]:
            fixed_config["llm"]["temperature"] = 0.7
    
    return fixed_config


@validate.command()
@click.option(
    "--path",
    "-p",
    type=click.Path(exists=True),
    default=".",
    help="Project directory to validate",
)
def project(path: str):
    """Validate Az-Core project structure.
    
    Examples:
        azcore validate project
        azcore validate project --path ./my-project
    """
    project_path = Path(path)
    
    click.secho(f"\n🔍 Validating project: {project_path.absolute()}\n", fg="cyan", bold=True)
    click.echo("=" * 70 + "\n")
    
    issues = []
    warnings = []
    
    # Check for required files
    _check_project_files(project_path, issues, warnings)
    
    # Check for standard structure
    _check_project_structure(project_path, issues, warnings)
    
    # Display results
    click.echo("\n" + "=" * 70)
    click.secho("Validation Results", fg="cyan", bold=True)
    click.echo("=" * 70 + "\n")
    
    if not issues and not warnings:
        click.secho("✓ Project structure is valid!", fg="green", bold=True)
        click.echo("\nYour project follows Az-Core best practices.")
        return
    
    if issues:
        click.secho(f"Errors ({len(issues)}):", fg="red", bold=True)
        for issue in issues:
            click.echo(f"  ✗ {issue}")
    
    if warnings:
        click.secho(f"\nWarnings ({len(warnings)}):", fg="yellow", bold=True)
        for warning in warnings:
            click.echo(f"  ⚠ {warning}")
    
    click.echo()


def _check_project_files(project_path: Path, issues: List[str], warnings: List[str]):
    """Check for required project files."""
    # Check for main files
    main_files = ["main.py", "app.py", "agent.py"]
    has_main = any((project_path / f).exists() for f in main_files)
    
    if not has_main:
        warnings.append("No main entry point found (main.py, app.py, or agent.py)")
    
    # Check for requirements.txt
    if not (project_path / "requirements.txt").exists():
        warnings.append("requirements.txt not found")
    
    # Check for .gitignore
    if not (project_path / ".gitignore").exists():
        warnings.append(".gitignore not found")
    
    # Check for README
    if not (project_path / "README.md").exists():
        warnings.append("README.md not found")


def _check_project_structure(project_path: Path, issues: List[str], warnings: List[str]):
    """Check for standard directory structure."""
    recommended_dirs = {
        "data": "Data storage directory",
        "logs": "Logging directory",
        "configs": "Configuration directory",
    }
    
    for dir_name, description in recommended_dirs.items():
        if not (project_path / dir_name).exists():
            warnings.append(f"Recommended directory missing: {dir_name}/ ({description})")
