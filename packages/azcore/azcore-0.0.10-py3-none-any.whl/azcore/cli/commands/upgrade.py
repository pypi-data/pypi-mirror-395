"""Upgrade Az-Core framework."""

import click
import subprocess
import sys
import json
from typing import Optional
import importlib.metadata


@click.command()
@click.option(
    "--check",
    "-c",
    is_flag=True,
    help="Check for updates without installing",
)
@click.option(
    "--version",
    "-v",
    type=str,
    help="Upgrade to specific version",
)
@click.option(
    "--pre",
    is_flag=True,
    help="Include pre-release versions",
)
@click.option(
    "--force",
    "-f",
    is_flag=True,
    help="Force reinstall even if up to date",
)
@click.option(
    "--extras",
    "-e",
    multiple=True,
    type=click.Choice(["dev", "mcp", "rl", "all"]),
    help="Include optional dependencies",
)
def upgrade(
    check: bool,
    version: Optional[str],
    pre: bool,
    force: bool,
    extras: tuple,
):
    """Upgrade Az-Core framework to the latest version.
    
    Examples:
        azcore upgrade --check
        azcore upgrade
        azcore upgrade --version 0.1.0
        azcore upgrade --extras rl
        azcore upgrade --pre
    """
    click.secho("\n🚀 Az-Core Upgrade Utility\n", fg="cyan", bold=True)
    click.echo("=" * 70 + "\n")
    
    # Get current version
    try:
        current_version = importlib.metadata.version("azcore")
        click.echo(f"Current version: {current_version}")
    except importlib.metadata.PackageNotFoundError:
        click.secho("Error: Az-Core not found in the environment", fg="red")
        sys.exit(1)
    
    # Check for latest version
    if check or not version:
        click.echo("\nChecking for updates...")
        latest_version = _get_latest_version(pre)
        
        if latest_version:
            click.echo(f"Latest version:  {latest_version}")
            
            if latest_version == current_version and not force:
                click.secho("\n✓ You are already on the latest version!", fg="green")
                return
            elif _is_newer_version(latest_version, current_version):
                click.secho(f"\n📦 New version available: {latest_version}", fg="yellow", bold=True)
                
                # Show changelog if available
                _show_changelog(current_version, latest_version)
                
                if check:
                    click.echo("\nTo upgrade, run: azcore upgrade")
                    return
            else:
                click.echo(f"\nYour version ({current_version}) is newer than PyPI.")
                if check:
                    return
        else:
            click.secho("\n⚠ Could not check for updates", fg="yellow")
            if check:
                return
    
    # Confirm upgrade
    if not force and not click.confirm(f"\nProceed with upgrade?", default=True):
        click.echo("Upgrade cancelled.")
        return
    
    # Build pip command
    click.echo("\n" + "=" * 70)
    click.secho("Installing update...", fg="cyan", bold=True)
    click.echo("=" * 70 + "\n")
    
    pip_args = [sys.executable, "-m", "pip", "install", "--upgrade"]
    
    # Add version specifier
    if version:
        package = f"azcore=={version}"
    elif force:
        package = "azcore"
    else:
        package = "azcore"
    
    # Add pre-release flag
    if pre:
        pip_args.append("--pre")
    
    # Add extras
    if extras:
        if "all" in extras:
            extra_str = "[dev,mcp,rl]"
        else:
            extra_str = f"[{','.join(extras)}]"
        package += extra_str
    
    pip_args.append(package)
    
    # Show command
    click.secho(f"Running: {' '.join(pip_args)}\n", fg="bright_black")
    
    try:
        # Run pip upgrade
        result = subprocess.run(
            pip_args,
            capture_output=False,
            text=True,
            check=True
        )
        
        # Get new version
        try:
            new_version = importlib.metadata.version("azcore")
            
            click.echo("\n" + "=" * 70)
            click.secho("✓ Upgrade successful!", fg="green", bold=True)
            click.echo("=" * 70 + "\n")
            
            click.echo(f"Previous version: {current_version}")
            click.echo(f"Current version:  {new_version}")
            
            if new_version != current_version:
                click.echo("\n📋 What's New:")
                _show_changelog(current_version, new_version)
            
            click.echo("\n💡 Next Steps:")
            click.echo("  • Run 'azcore doctor' to verify your setup")
            click.echo("  • Check 'azcore --version' to confirm version")
            click.echo("  • Review migration guide if there are breaking changes")
            click.echo()
        
        except importlib.metadata.PackageNotFoundError:
            click.secho("\n⚠ Warning: Could not verify new version", fg="yellow")
    
    except subprocess.CalledProcessError as e:
        click.secho("\n✗ Upgrade failed!", fg="red", bold=True)
        click.echo(f"\nError: {str(e)}")
        click.echo("\nTry:")
        click.echo("  • Run with --verbose for more details")
        click.echo("  • Check your internet connection")
        click.echo("  • Verify pip is up to date: pip install --upgrade pip")
        sys.exit(1)
    
    except KeyboardInterrupt:
        click.secho("\n\n⚠ Upgrade cancelled by user", fg="yellow")
        sys.exit(1)


def _get_latest_version(include_pre: bool = False) -> Optional[str]:
    """Get the latest version from PyPI."""
    try:
        import urllib.request
        import json
        
        url = "https://pypi.org/pypi/azcore/json"
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode())
        
        if include_pre:
            # Get the latest release (including pre-releases)
            versions = list(data.get("releases", {}).keys())
            if versions:
                # Sort versions (simple string sort, may not be perfect for all cases)
                versions.sort(reverse=True)
                return versions[0]
        else:
            # Get the latest stable release
            return data.get("info", {}).get("version")
    
    except Exception as e:
        # Silently fail and return None
        return None


def _is_newer_version(version1: str, version2: str) -> bool:
    """Check if version1 is newer than version2."""
    try:
        from packaging import version
        return version.parse(version1) > version.parse(version2)
    except ImportError:
        # Fallback to simple string comparison
        return version1 > version2


def _show_changelog(from_version: str, to_version: str):
    """Show changelog between versions."""
    # In a real implementation, this would fetch from GitHub releases
    # For now, show a placeholder
    click.echo("\n" + "-" * 70)
    click.secho("Changelog", fg="yellow", bold=True)
    click.echo("-" * 70)
    click.echo(f"Changes from {from_version} to {to_version}:")
    click.echo()
    click.echo("  For detailed changelog, visit:")
    click.echo("  https://github.com/Azrienlabs/Az-Core/releases")
    click.echo("-" * 70)


@click.command()
def check_updates():
    """Check for Az-Core updates (alias for upgrade --check)."""
    ctx = click.get_current_context()
    ctx.invoke(upgrade, check=True)
