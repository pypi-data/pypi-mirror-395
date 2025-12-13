"""Main CLI entry point for Az-Core."""

import sys
import click
from azcore import __version__


@click.group()
@click.version_option(version=__version__, prog_name="azcore")
def cli():
    """Az-Core: Advanced AI Agent Framework with RL Integration.
    
    A powerful framework for building, orchestrating, and optimizing AI agents.
    """
    pass


def main():
    """Main entry point for the CLI."""
    # Import commands lazily to avoid import errors
    from azcore.cli.commands import (
        init, run, train, validate, stats, create,
        examples, doctor, upgrade, agent
    )
    
    # Register command groups
    cli.add_command(init.init)
    cli.add_command(run.run)
    cli.add_command(train.train)
    cli.add_command(validate.validate)
    cli.add_command(stats.stats)
    cli.add_command(create.create)
    cli.add_command(examples.examples)
    cli.add_command(doctor.doctor)
    cli.add_command(upgrade.upgrade)
    cli.add_command(agent.agent)
    
    # Run CLI
    cli()


if __name__ == "__main__":
    main()
