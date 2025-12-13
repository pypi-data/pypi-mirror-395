"""Diagnose and validate Az-Core environment setup."""

import click
import sys
import os
from pathlib import Path
from typing import List, Tuple, Optional
import importlib.util


@click.command()
@click.option(
    "--fix",
    "-f",
    is_flag=True,
    help="Attempt to auto-fix issues",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Show detailed diagnostic information",
)
@click.option(
    "--check-gpu",
    is_flag=True,
    help="Check GPU availability for RL training",
)
def doctor(fix: bool, verbose: bool, check_gpu: bool):
    """Diagnose and validate Az-Core environment setup.
    
    This command checks:
    - Python version compatibility
    - Required dependencies
    - Configuration files
    - API key setup
    - Optional components (RL, MCP)
    
    Examples:
        azcore doctor
        azcore doctor --fix
        azcore doctor --verbose --check-gpu
    """
    click.secho("\n🏥 Az-Core Environment Diagnostics\n", fg="cyan", bold=True)
    click.echo("=" * 70 + "\n")
    
    issues: List[Tuple[str, str, str]] = []  # (severity, category, message)
    warnings: List[Tuple[str, str]] = []  # (category, message)
    
    # Run all checks
    _check_python_version(issues, warnings, verbose)
    _check_dependencies(issues, warnings, verbose)
    _check_configuration(issues, warnings, verbose)
    _check_environment_variables(issues, warnings, verbose)
    _check_directories(issues, warnings, verbose)
    _check_optional_dependencies(issues, warnings, verbose, check_gpu)
    
    # Display results
    click.echo("\n" + "=" * 70)
    click.secho("Diagnostic Summary", fg="cyan", bold=True)
    click.echo("=" * 70 + "\n")
    
    # Count by severity
    errors = [i for i in issues if i[0] == "error"]
    
    if not errors and not warnings:
        click.secho("✓ All checks passed! Your environment is ready.", fg="green", bold=True)
        click.echo("\nYour Az-Core installation is properly configured.")
        click.echo("Run 'azcore examples list' to get started with examples.\n")
        return
    
    # Display errors
    if errors:
        click.secho(f"\n❌ Errors ({len(errors)}):", fg="red", bold=True)
        for severity, category, message in errors:
            click.echo(f"   [{category}] {message}")
    
    # Display warnings
    if warnings:
        click.secho(f"\n⚠️  Warnings ({len(warnings)}):", fg="yellow", bold=True)
        for category, message in warnings:
            click.echo(f"   [{category}] {message}")
    
    click.echo()
    
    # Auto-fix if requested
    if fix and (errors or warnings):
        click.echo("\n" + "=" * 70)
        click.secho("Attempting Auto-Fix...", fg="cyan", bold=True)
        click.echo("=" * 70 + "\n")
        
        fixed = _attempt_fixes(issues, warnings, verbose)
        
        if fixed:
            click.secho(f"\n✓ Fixed {fixed} issue(s)", fg="green")
            click.echo("\nRun 'azcore doctor' again to verify fixes.")
        else:
            click.secho("\nNo issues could be auto-fixed.", fg="yellow")
            click.echo("Please manually resolve the issues above.")
    else:
        click.echo("Run 'azcore doctor --fix' to attempt automatic fixes.\n")
    
    # Exit with error code if there are errors
    if errors:
        sys.exit(1)


def _check_python_version(issues: List, warnings: List, verbose: bool):
    """Check Python version compatibility."""
    click.secho("Checking Python version...", fg="blue")
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    if verbose:
        click.echo(f"  Python {version_str}")
        click.echo(f"  Executable: {sys.executable}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 12):
        issues.append((
            "error",
            "Python",
            f"Python 3.12+ required, found {version_str}"
        ))
        click.secho("  ✗ Incompatible Python version", fg="red")
    else:
        click.secho(f"  ✓ Python {version_str}", fg="green")


def _check_dependencies(issues: List, warnings: List, verbose: bool):
    """Check required dependencies."""
    click.secho("\nChecking dependencies...", fg="blue")
    
    required_packages = [
        ("azcore", "azcore"),
        ("langchain", "langchain"),
        ("langchain_openai", "langchain-openai"),
        ("yaml", "pyyaml"),
        ("dotenv", "python-dotenv"),
        ("click", "click"),
    ]
    
    missing = []
    installed = []
    
    for module_name, package_name in required_packages:
        spec = importlib.util.find_spec(module_name)
        if spec is None:
            missing.append(package_name)
            click.secho(f"  ✗ {package_name}", fg="red")
        else:
            installed.append(package_name)
            if verbose:
                click.secho(f"  ✓ {package_name}", fg="green")
    
    if not verbose and installed:
        click.secho(f"  ✓ {len(installed)} core dependencies installed", fg="green")
    
    if missing:
        issues.append((
            "error",
            "Dependencies",
            f"Missing packages: {', '.join(missing)}"
        ))


def _check_configuration(issues: List, warnings: List, verbose: bool):
    """Check for configuration files."""
    click.secho("\nChecking configuration files...", fg="blue")
    
    config_files = ["config.yml", "configs/config.yml"]
    config_found = False
    
    for config_file in config_files:
        config_path = Path(config_file)
        if config_path.exists():
            config_found = True
            click.secho(f"  ✓ Found {config_file}", fg="green")
            
            # Validate config content
            try:
                import yaml
                with open(config_path) as f:
                    config = yaml.safe_load(f)
                
                if not config:
                    warnings.append(("Config", f"{config_file} is empty"))
                    click.secho(f"    ⚠ Config file is empty", fg="yellow")
                elif verbose:
                    click.echo(f"    Keys: {', '.join(config.keys())}")
            except Exception as e:
                issues.append((
                    "error",
                    "Config",
                    f"Invalid YAML in {config_file}: {str(e)}"
                ))
                click.secho(f"    ✗ Invalid YAML syntax", fg="red")
            break
    
    if not config_found:
        warnings.append((
            "Config",
            "No config.yml found. Create one with 'azcore init'"
        ))
        click.secho("  ⚠ No config.yml found", fg="yellow")


def _check_environment_variables(issues: List, warnings: List, verbose: bool):
    """Check for API keys and environment variables."""
    click.secho("\nChecking environment variables...", fg="blue")
    
    # Check for .env file
    env_file = Path(".env")
    if env_file.exists():
        click.secho("  ✓ .env file found", fg="green")
        
        # Load and check for API keys
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except ImportError:
            pass
    else:
        warnings.append((
            "Environment",
            "No .env file found. API keys should be configured."
        ))
        click.secho("  ⚠ No .env file found", fg="yellow")
    
    # Check important environment variables
    api_keys = {
        "OPENAI_API_KEY": "OpenAI API",
        "ANTHROPIC_API_KEY": "Anthropic API (optional)",
    }
    
    keys_found = 0
    for key, name in api_keys.items():
        if os.getenv(key):
            keys_found += 1
            if verbose:
                masked_key = os.getenv(key)[:8] + "..." if os.getenv(key) else ""
                click.secho(f"  ✓ {name}: {masked_key}", fg="green")
        else:
            if "optional" not in name.lower():
                warnings.append((
                    "Environment",
                    f"{name} not set ({key})"
                ))
                click.secho(f"  ⚠ {name} not set", fg="yellow")
    
    if keys_found == 0:
        issues.append((
            "error",
            "Environment",
            "No API keys configured. Set OPENAI_API_KEY in .env"
        ))


def _check_directories(issues: List, warnings: List, verbose: bool):
    """Check for standard directories."""
    click.secho("\nChecking directories...", fg="blue")
    
    standard_dirs = {
        "data": "Data storage",
        "logs": "Log files",
        "models": "Model storage (optional)",
        "configs": "Configuration files (optional)",
    }
    
    dirs_found = 0
    for dir_name, description in standard_dirs.items():
        dir_path = Path(dir_name)
        if dir_path.exists():
            dirs_found += 1
            if verbose:
                click.secho(f"  ✓ {dir_name}/ ({description})", fg="green")
    
    if dirs_found > 0:
        click.secho(f"  ✓ {dirs_found} standard directories found", fg="green")
    else:
        warnings.append((
            "Directories",
            "No standard directories found. Run 'azcore init' to set up."
        ))
        click.secho("  ⚠ Standard directories not found", fg="yellow")


def _check_optional_dependencies(issues: List, warnings: List, verbose: bool, check_gpu: bool):
    """Check optional dependencies."""
    click.secho("\nChecking optional features...", fg="blue")
    
    optional_packages = [
        ("torch", "PyTorch (for RL)", "RL training"),
        ("sentence_transformers", "SentenceTransformers (for RL embeddings)", "RL with embeddings"),
        ("langchain_mcp_adapters", "LangChain MCP (for MCP integration)", "MCP support"),
    ]
    
    for module_name, package_desc, feature in optional_packages:
        spec = importlib.util.find_spec(module_name)
        if spec is None:
            if verbose:
                click.secho(f"  - {package_desc} not installed", fg="bright_black")
        else:
            click.secho(f"  ✓ {feature} available", fg="green")
    
    # Check GPU if requested
    if check_gpu:
        try:
            import torch
            if torch.cuda.is_available():
                click.secho(f"  ✓ GPU available: {torch.cuda.get_device_name(0)}", fg="green")
                if verbose:
                    click.echo(f"    CUDA version: {torch.version.cuda}")
            else:
                warnings.append((
                    "GPU",
                    "No GPU available. RL training will use CPU."
                ))
                click.secho("  ⚠ No GPU available (CPU only)", fg="yellow")
        except ImportError:
            if verbose:
                click.secho("  - PyTorch not installed (can't check GPU)", fg="bright_black")


def _attempt_fixes(issues: List, warnings: List, verbose: bool) -> int:
    """Attempt to automatically fix issues."""
    fixed_count = 0
    
    # Create standard directories
    for category, message in warnings:
        if category == "Directories" and "standard directories" in message:
            click.echo("Creating standard directories...")
            dirs = ["data", "logs", "models", "configs"]
            for dir_name in dirs:
                Path(dir_name).mkdir(exist_ok=True)
                click.secho(f"  ✓ Created {dir_name}/", fg="green")
            fixed_count += 1
    
    # Create .env.example if .env missing
    for category, message in warnings:
        if category == "Environment" and ".env file" in message:
            click.echo("Creating .env.example template...")
            env_template = """# OpenAI API Key
OPENAI_API_KEY=your-api-key-here

# Anthropic API Key (optional)
ANTHROPIC_API_KEY=your-api-key-here

# LangSmith (optional)
LANGCHAIN_API_KEY=your-api-key-here
LANGCHAIN_TRACING_V2=false
LANGCHAIN_PROJECT=azcore-project
"""
            Path(".env.example").write_text(env_template)
            click.secho("  ✓ Created .env.example", fg="green")
            click.echo("  Copy .env.example to .env and add your API keys")
            fixed_count += 1
    
    # Create sample config if missing
    for category, message in warnings:
        if category == "Config" and "No config.yml" in message:
            click.echo("Creating sample config.yml...")
            config_template = """# Az-Core Configuration

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
"""
            Path("config.yml").write_text(config_template)
            click.secho("  ✓ Created config.yml", fg="green")
            fixed_count += 1
    
    return fixed_count
