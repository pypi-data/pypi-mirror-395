"""
CLI error handler for user-friendly error messages.

This module provides error handling for CLI commands with
helpful messages, suggestions, and recovery options.
"""

import click
import sys
from typing import Optional, Callable, Any
from functools import wraps


def handle_cli_error(func: Callable) -> Callable:
    """
    Decorator for CLI commands to handle errors gracefully.
    
    Catches common exceptions and displays user-friendly error messages
    with solutions and suggestions.
    
    Usage:
        @click.command()
        @handle_cli_error
        def my_command():
            ...
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        
        except FileNotFoundError as e:
            _handle_file_not_found(e)
            sys.exit(1)
        
        except ImportError as e:
            _handle_import_error(e)
            sys.exit(1)
        
        except PermissionError as e:
            _handle_permission_error(e)
            sys.exit(1)
        
        except KeyboardInterrupt:
            click.echo("\n")
            click.secho("⚠️  Operation cancelled by user", fg="yellow")
            sys.exit(130)
        
        except Exception as e:
            _handle_generic_error(e)
            sys.exit(1)
    
    return wrapper


def _handle_file_not_found(error: FileNotFoundError):
    """Handle file not found errors."""
    from azcore.exceptions import AzCoreException
    
    if isinstance(error, AzCoreException):
        click.echo(str(error))
    else:
        click.secho("\n❌ File Not Found Error", fg="red", bold=True)
        click.echo("="*70)
        click.echo(f"\n{str(error)}")
        click.echo("\n💡 Solutions:")
        click.echo("  1. Check the file path is correct")
        click.echo("  2. Verify the file exists: ls <path>")
        click.echo("  3. Use absolute paths to avoid confusion")
        click.echo("  4. Run 'azcore init' to create necessary files")
        click.echo("\n" + "="*70 + "\n")


def _handle_import_error(error: ImportError):
    """Handle import/dependency errors."""
    error_msg = str(error).lower()
    
    click.secho("\n❌ Dependency Error", fg="red", bold=True)
    click.echo("="*70)
    click.echo(f"\n{str(error)}")
    
    # Detect specific missing packages
    if "openai" in error_msg:
        click.echo("\n💡 Missing OpenAI dependency")
        click.echo("\nInstall with:")
        click.secho("  pip install langchain-openai", fg="green")
    
    elif "langchain" in error_msg:
        click.echo("\n💡 Missing LangChain dependency")
        click.echo("\nInstall with:")
        click.secho("  pip install langchain", fg="green")
    
    elif "torch" in error_msg or "transformers" in error_msg:
        click.echo("\n💡 Missing RL dependencies")
        click.echo("\nInstall with:")
        click.secho("  pip install azcore[rl]", fg="green")
    
    elif "mcp" in error_msg:
        click.echo("\n💡 Missing MCP dependencies")
        click.echo("\nInstall with:")
        click.secho("  pip install azcore[mcp]", fg="green")
    
    else:
        click.echo("\n💡 Solutions:")
        click.echo("  1. Install missing dependencies:")
        click.secho("     pip install -r requirements.txt", fg="green")
        click.echo("  2. Reinstall azcore:")
        click.secho("     pip install --upgrade azcore", fg="green")
        click.echo("  3. Check your environment:")
        click.secho("     azcore doctor", fg="green")
    
    click.echo("\n" + "="*70 + "\n")


def _handle_permission_error(error: PermissionError):
    """Handle permission errors."""
    click.secho("\n❌ Permission Error", fg="red", bold=True)
    click.echo("="*70)
    click.echo(f"\n{str(error)}")
    click.echo("\n💡 Solutions:")
    click.echo("  1. Check file/directory permissions")
    click.echo("  2. Run with appropriate user permissions")
    click.echo("  3. Ensure directory is writable")
    
    if sys.platform == "win32":
        click.echo("  4. Try running as Administrator")
    else:
        click.echo("  4. Try: sudo <command> (use with caution)")
    
    click.echo("\n" + "="*70 + "\n")


def _handle_generic_error(error: Exception):
    """Handle generic errors."""
    from azcore.exceptions import AzCoreException
    
    # If it's an AzCoreException, use its formatted output
    if isinstance(error, AzCoreException):
        click.echo(str(error))
        return
    
    # Otherwise, create a generic error message
    click.secho("\n❌ Unexpected Error", fg="red", bold=True)
    click.echo("="*70)
    click.echo(f"\n{type(error).__name__}: {str(error)}")
    
    click.echo("\n💡 Troubleshooting:")
    click.echo("  1. Run diagnostics:")
    click.secho("     azcore doctor --verbose", fg="green")
    click.echo("  2. Validate your configuration:")
    click.secho("     azcore validate config", fg="green")
    click.echo("  3. Check for updates:")
    click.secho("     azcore upgrade --check", fg="green")
    click.echo("  4. Review logs in ./logs directory")
    
    click.echo("\n📚 Get Help:")
    click.echo("  • Documentation: https://docs.azrienlabs.com")
    click.echo("  • Examples: azcore examples list")
    click.echo("  • Issues: https://github.com/Azrienlabs/Az-Core/issues")
    
    # Offer to show full traceback
    if click.confirm("\nShow full error details?", default=False):
        import traceback
        click.echo("\n" + "-"*70)
        click.echo("Full Traceback:")
        click.echo("-"*70)
        traceback.print_exception(type(error), error, error.__traceback__)
    
    click.echo("\n" + "="*70 + "\n")


def show_warning(message: str, suggestion: Optional[str] = None):
    """
    Show a warning message to the user.
    
    Args:
        message: Warning message
        suggestion: Optional suggestion for resolution
    """
    click.secho(f"\n⚠️  Warning: {message}", fg="yellow")
    if suggestion:
        click.echo(f"   💡 {suggestion}")
    click.echo()


def show_error(message: str, solution: Optional[str] = None):
    """
    Show an error message to the user.
    
    Args:
        message: Error message
        solution: Optional solution suggestion
    """
    click.secho(f"\n❌ Error: {message}", fg="red")
    if solution:
        click.echo(f"   💡 {solution}")
    click.echo()


def show_success(message: str):
    """
    Show a success message to the user.
    
    Args:
        message: Success message
    """
    click.secho(f"\n✅ {message}", fg="green")
    click.echo()


def confirm_action(
    message: str,
    default: bool = False,
    abort: bool = True
) -> bool:
    """
    Ask user to confirm an action.
    
    Args:
        message: Confirmation question
        default: Default choice if user presses Enter
        abort: Abort execution if user declines
        
    Returns:
        User's choice
    """
    try:
        result = click.confirm(f"\n❓ {message}", default=default)
        if not result and abort:
            click.secho("\nOperation cancelled.", fg="yellow")
            sys.exit(0)
        return result
    except click.Abort:
        click.secho("\n\nOperation cancelled.", fg="yellow")
        sys.exit(0)


def suggest_command(
    invalid_command: str,
    valid_commands: list,
    message: Optional[str] = None
):
    """
    Suggest valid commands when user enters invalid one.
    
    Args:
        invalid_command: The command user tried
        valid_commands: List of valid commands
        message: Optional custom message
    """
    from azcore.utils.error_helpers import suggest_command_fix
    
    if message:
        click.secho(f"\n❌ {message}", fg="red")
    else:
        click.secho(f"\n❌ Unknown command: '{invalid_command}'", fg="red")
    
    suggestion = suggest_command_fix(invalid_command, valid_commands)
    if suggestion:
        click.echo(suggestion)
    
    click.echo(f"\nRun 'azcore --help' to see all available commands.")
    click.echo()


def validate_file_exists(
    file_path: str,
    file_type: str = "file",
    create_if_missing: bool = False
) -> bool:
    """
    Validate that a file exists, with helpful error if not.
    
    Args:
        file_path: Path to file
        file_type: Type of file for error message
        create_if_missing: Offer to create if missing
        
    Returns:
        True if file exists or was created
        
    Raises:
        click.Abort: If file doesn't exist and user declines to create
    """
    from pathlib import Path
    
    path = Path(file_path)
    
    if path.exists():
        return True
    
    show_error(
        f"{file_type.capitalize()} not found: {file_path}",
        "Check the path or create the file"
    )
    
    if create_if_missing:
        if confirm_action(f"Create {file_type}?", default=True, abort=False):
            try:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.touch()
                show_success(f"Created {file_type}: {file_path}")
                return True
            except Exception as e:
                show_error(f"Failed to create {file_type}", str(e))
                raise click.Abort()
    
    raise click.Abort()


def validate_required_env_vars(required_vars: list) -> bool:
    """
    Validate that required environment variables are set.
    
    Args:
        required_vars: List of required environment variable names
        
    Returns:
        True if all required vars are set
    """
    import os
    
    missing = [var for var in required_vars if not os.getenv(var)]
    
    if missing:
        show_error(
            "Missing required environment variables",
            "Set these variables in your .env file"
        )
        
        click.echo("Missing variables:")
        for var in missing:
            click.echo(f"  • {var}")
        
        click.echo("\nExample .env file:")
        click.echo("-" * 40)
        for var in missing:
            if "API_KEY" in var:
                click.echo(f"{var}=your-key-here")
            else:
                click.echo(f"{var}=your-value-here")
        click.echo("-" * 40)
        
        click.echo("\n💡 Run 'azcore doctor' to check your environment")
        click.echo()
        
        return False
    
    return True


def handle_api_error(error: Exception, provider: str = "OpenAI"):
    """
    Handle API-related errors with specific guidance.
    
    Args:
        error: The API error
        provider: API provider name
    """
    error_msg = str(error).lower()
    
    click.secho(f"\n❌ {provider} API Error", fg="red", bold=True)
    click.echo("="*70)
    click.echo(f"\n{str(error)}")
    
    # Provide specific guidance based on error type
    if "api key" in error_msg or "401" in error_msg:
        click.echo("\n💡 API Key Issue:")
        click.echo("  1. Check your API key in .env file")
        click.echo("  2. Verify the key is valid and active")
        click.echo("  3. Ensure you have API credits")
        click.secho("  4. Run: azcore doctor", fg="green")
    
    elif "rate limit" in error_msg or "429" in error_msg:
        click.echo("\n💡 Rate Limit Exceeded:")
        click.echo("  1. Wait before retrying")
        click.echo("  2. Reduce request frequency")
        click.echo("  3. Implement exponential backoff")
        click.echo("  4. Consider upgrading your API plan")
    
    elif "timeout" in error_msg:
        click.echo("\n💡 Request Timeout:")
        click.echo("  1. Increase timeout in config")
        click.echo("  2. Use a faster model")
        click.echo("  3. Simplify your request")
        click.echo("  4. Check network connection")
    
    else:
        click.echo("\n💡 General Solutions:")
        click.echo("  1. Check API status page")
        click.echo("  2. Verify your configuration")
        click.echo("  3. Review API documentation")
        click.echo("  4. Try again in a moment")
    
    click.echo("\n" + "="*70 + "\n")
