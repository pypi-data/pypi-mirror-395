"""Initialize new Az-Core project."""

import os
import click
from pathlib import Path
from typing import Optional

from azcore.cli.templates import (
    get_basic_agent_template,
    get_team_agent_template,
    get_modular_team_agent_template,
    get_rl_agent_template,
    get_workflow_template,
    get_config_template,
    get_gitignore_template,
    get_readme_template,
)

# Import version from main package
try:
    from azcore import __version__ as AZCORE_VERSION
except ImportError:
    AZCORE_VERSION = "0.0.9"


def print_banner():
    """Print Az-Core ASCII banner."""
    banner = """
            █████╗ ███████╗      ██████╗ ██████╗ ██████╗ ███████╗
            ██╔══██╗╚══███╔╝     ██╔════╝██╔═══██╗██╔══██╗██╔════╝
            ███████║  ███╔╝█████╗██║     ██║   ██║██████╔╝█████╗  
            ██╔══██║ ███╔╝ ╚════╝██║     ██║   ██║██╔══██╗██╔══╝  
            ██║  ██║███████╗     ╚██████╗╚██████╔╝██║  ██║███████╗
            ╚═╝  ╚═╝╚══════╝      ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝                                   
"""
    
    # Print banner in cyan
    click.secho(banner, fg="cyan", bold=True)
    
    # Print attribution and version
    click.secho("                                                  powered by Azrienlabs", fg="bright_black")
    click.secho(f"                                                  version {AZCORE_VERSION}", fg="green")
    click.echo()


TEMPLATES = {
    "basic-agent": {
        "name": "Basic Agent",
        "description": "Single agent setup with ReAct reasoning",
        "details": "Perfect for simple tasks, Q&A, or getting started with Az-Core",
        "use_cases": ["Question answering", "Simple automation", "Getting started"]
    },
    "team-agent": {
        "name": "Team Agent",
        "description": "Multi-agent collaboration system",
        "details": "Multiple specialized agents working together on complex tasks",
        "use_cases": ["Complex workflows", "Role-based tasks", "Research & analysis"]
    },
    "modular-team": {
        "name": "Modular Team Agent",
        "description": "Modular team system with separate tool modules",
        "details": "Enterprise-ready team structure with organized tool modules, MCP support, and RL optimization",
        "use_cases": ["Large-scale systems", "Multiple MCP servers", "Enterprise applications"]
    },
    "rl-agent": {
        "name": "RL-Optimized Agent",
        "description": "Agent with reinforcement learning for tool selection",
        "details": "Self-improving agent that learns optimal tool usage patterns",
        "use_cases": ["Tool optimization", "Adaptive systems", "Long-term learning"]
    },
    "workflow": {
        "name": "Custom Workflow",
        "description": "Flexible workflow orchestration system",
        "details": "Build custom agent workflows with sequential, parallel, or graph execution",
        "use_cases": ["Custom pipelines", "Complex orchestration", "Advanced patterns"]
    }
}


@click.command()
@click.option(
    "--template",
    "-t",
    type=click.Choice(list(TEMPLATES.keys())),
    default=None,
    help="Project template to use (skip interactive mode)",
)
@click.option(
    "--name",
    "-n",
    default=None,
    help="Project name (skip interactive mode)",
)
@click.option(
    "--path",
    "-p",
    type=click.Path(),
    default=".",
    help="Directory to create project in",
)
@click.option(
    "--force",
    "-f",
    is_flag=True,
    help="Override existing files",
)
@click.option(
    "--with-rl/--no-rl",
    default=False,
    help="Include RL synthetic-data training scaffolding (scripts, config, deps)",
)
def init(template: Optional[str], name: Optional[str], path: str, force: bool, with_rl: bool):
    """Initialize a new Az-Core project.
    
    Interactive mode (no options):
        azcore init
        
    Direct mode (with options):
        azcore init --template basic-agent --name my-agent
        azcore init -t rl-agent -n rl-optimizer --with-rl
    """
    # Interactive mode if no template or name provided
    interactive_mode = template is None or name is None
    
    if interactive_mode:
        # Print the banner
        print_banner()
        click.secho(">>> Welcome to Az-Core Project Setup! <<<\n", fg="cyan", bold=True)
        
        # Get project name
        if name is None:
            name = click.prompt(
                click.style("Enter project name", fg="yellow"),
                default="my-azcore-project",
                type=str
            )
        
        # Get template with interactive selection
        if template is None:
            template = _interactive_template_selection()
        
        # Ask about RL scaffolding in interactive mode
        click.echo()
        click.secho("RL Training Scaffolding", fg="cyan", bold=True)
        click.echo("Include RL synthetic-data training tools?")
        click.echo("  - Creates: configs/rl_training_config.yml")
        click.echo("  - Creates: scripts/train_synthetic.py")
        click.echo("  - Creates: scripts/generate_synthetic.py")
        click.echo("  - Adds RL dependencies to requirements.txt")
        click.echo()
        with_rl = click.confirm(
            click.style("Include RL training scaffolding?", fg="yellow"),
            default=(template == "rl-agent")
        )
    
    # Show banner in direct mode too
    else:
        print_banner()
    
    # Validate template
    if template not in TEMPLATES:
        click.secho(f"Error: Invalid template '{template}'", fg="red")
        return
    project_path = Path(path) / name
    
    # Check if directory exists
    if project_path.exists() and not force:
        if any(project_path.iterdir()):
            click.secho(
                f"Error: Directory '{project_path}' already exists and is not empty.",
                fg="red"
            )
            click.echo("Use --force to override existing files.")
            return
    
    # Create project directory
    project_path.mkdir(parents=True, exist_ok=True)
    
    click.echo("=" * 70)
    click.secho(f"Creating Az-Core project: {name}", fg="cyan", bold=True)
    click.echo(f"Template: {TEMPLATES[template]['name']}")
    click.echo(f"Location: {project_path.absolute()}")
    click.echo("=" * 70 + "\n")
    
    # Create project structure (optionally include RL training scaffolding)
    _create_project_structure(project_path, template, name, include_rl=with_rl)
    
    click.echo()
    click.secho("[SUCCESS] Project created successfully!", fg="green", bold=True)
    click.echo("\n" + "=" * 70)
    click.secho("Next Steps:", fg="cyan", bold=True)
    click.echo("=" * 70)
    click.echo(f"  1. cd {name}")
    click.echo("  2. pip install -r requirements.txt")
    click.echo("  3. Copy .env.example to .env and add your API keys")
    click.echo("  4. azcore run main.py")
    click.echo("\n" + "=" * 70)
    click.secho(f"Project Type: {TEMPLATES[template]['name']}", fg="blue")
    click.echo(f"   {TEMPLATES[template]['details']}")
    click.echo("=" * 70 + "\n")


def _create_project_structure(project_path: Path, template: str, name: str, include_rl: bool = False):
    """Create the project structure based on template."""
    
    # Create directories
    (project_path / "configs").mkdir(exist_ok=True)
    (project_path / "data").mkdir(exist_ok=True)
    (project_path / "logs").mkdir(exist_ok=True)
    
    if template == "rl-agent" or template == "modular-team" or include_rl:
        (project_path / "rl_data").mkdir(exist_ok=True)
        (project_path / "models").mkdir(exist_ok=True)
        # Create scripts directory for training and data generation
        (project_path / "scripts").mkdir(exist_ok=True)
    
    # Create team_modules directory for modular-team template
    if template == "modular-team":
        (project_path / "team_modules").mkdir(exist_ok=True)
    
    # Create main application file
    main_content = _get_template_content(template, name)
    _write_file(project_path / "main.py", main_content)
    click.echo("  Created main.py")
    
    # Copy team modules for modular-team template
    if template == "modular-team":
        _create_team_modules(project_path)
        click.echo("  Created team_modules/")
    
    # Create config file (base)
    config_content = get_config_template(template)
    _write_file(project_path / "configs" / "config.yml", config_content)
    click.echo("  Created configs/config.yml")

    # If RL scaffolding requested, add training config and scripts
    if template == "rl-agent" or include_rl:
        rl_config = _get_rl_training_config()
        _write_file(project_path / "configs" / "rl_training_config.yml", rl_config)
        click.echo("  Created configs/rl_training_config.yml")

        # Training script
        train_script = _get_train_script()
        _write_file(project_path / "scripts" / "train_synthetic.py", train_script)
        click.echo("  Created scripts/train_synthetic.py")

        # Data generation script
        gen_script = _get_generate_script()
        _write_file(project_path / "scripts" / "generate_synthetic.py", gen_script)
        click.echo("  Created scripts/generate_synthetic.py")
    
    # Create requirements.txt
    requirements = _get_requirements(template, include_rl=include_rl)
    _write_file(project_path / "requirements.txt", requirements)
    click.echo("  Created requirements.txt")
    
    # Create .gitignore
    gitignore = get_gitignore_template()
    _write_file(project_path / ".gitignore", gitignore)
    click.echo("  Created .gitignore")
    
    # Create README.md
    readme = get_readme_template(name, template)
    _write_file(project_path / "README.md", readme)
    click.echo("  Created README.md")
    
    # Create .env.example
    env_example = _get_env_example(template)
    _write_file(project_path / ".env.example", env_example)
    click.echo("  Created .env.example")


def _get_template_content(template: str, name: str) -> str:
    """Get the main application content for the template."""
    if template == "basic-agent":
        return get_basic_agent_template(name)
    elif template == "team-agent":
        return get_team_agent_template(name)
    elif template == "modular-team":
        return get_modular_team_agent_template(name)
    elif template == "rl-agent":
        return get_rl_agent_template(name)
    elif template == "workflow":
        return get_workflow_template(name)
    else:
        return get_basic_agent_template(name)


def _get_requirements(template: str, include_rl: bool = False) -> str:
    """Get requirements.txt content based on template."""
    base_requirements = """# Az-Core Framework
azcore>=0.0.9

# LangChain
langchain>=0.1.0
langchain-openai>=0.0.5
langchain-anthropic>=0.1.0

# Utilities
python-dotenv>=1.0.0
pyyaml>=6.0
"""
    # Add RL dependencies when requested
    if template == "rl-agent" or template == "modular-team" or include_rl:
        base_requirements += """
# RL-specific dependencies
sentence-transformers>=2.2.0
torch>=2.0.0
numpy>=1.24.0
tqdm>=4.0.0
scikit-learn>=1.0.0
"""
    
    # Add modular-team specific dependencies
    if template == "modular-team":
        base_requirements += """
# Modular team dependencies
requests>=2.28.0
beautifulsoup4>=4.11.0
"""
    
    return base_requirements


def _get_rl_training_config() -> str:
    """Return a YAML config template for RL synthetic-data training."""
    return """# RL training configuration (synthetic data)

# Tools to include in training
tools:
  - search
  - calculator
  - code_executor

synthetic_data:
  num_samples: 1000
  use_llm: false
  min_quality_score: 0.6
  validate: true

rl_manager:
  learning_rate: 0.1
  discount_factor: 0.99
  exploration_rate: 0.15
  use_embeddings: true
  embedding_model: "all-MiniLM-L6-v2"

training:
  epochs: 10
  batch_size: 32
  shuffle: true

output:
  dir: ./rl_data
"""


def _get_train_script() -> str:
    """Return a small training runner script that uses Az-Core synthetic pipeline."""
    return '''"""Train RL agent with synthetic data (scaffold)

Run from project root: python scripts/train_synthetic.py
"""

import yaml
from pathlib import Path
from azcore.rl.synthetic_data.training_pipeline import SyntheticDataPipeline
from azcore.rl.training.offline_trainer import OfflineTrainer
from azcore.rl.rl_manager import RLManager


def main():
    cfg_path = Path("configs/rl_training_config.yml")
    if not cfg_path.exists():
        print("Missing configs/rl_training_config.yml")
        return

    cfg = yaml.safe_load(cfg_path.read_text())

    tools = cfg.get("tools", [])
    synth_cfg = cfg.get("synthetic_data", {})
    train_cfg = cfg.get("training", {})

    pipeline = SyntheticDataPipeline(tool_names=tools, use_llm=synth_cfg.get("use_llm", False))
    data = pipeline.generate(num_samples=synth_cfg.get("num_samples", 1000), validate=synth_cfg.get("validate", True))

    # split
    split = int(len(data) * (1 - cfg.get("training", {}).get("validation_split", 0.2)))
    train_data = data[:split]
    val_data = data[split:]

    q_path = cfg.get("output", {}).get("dir", "./rl_data")
    q_table_file = Path(q_path) / "q_table.pkl"

    rl_manager = RLManager(tool_names=tools, q_table_path=str(q_table_file))
    trainer = OfflineTrainer(rl_manager=rl_manager, batch_size=train_cfg.get("batch_size", 32), verbose=True)

    trainer.train(training_data=train_data, epochs=train_cfg.get("epochs", 10))
    metrics = trainer.evaluate(val_data)

    print("Training finished. Validation metrics:", metrics)


if __name__ == "__main__":
    main()
'''


def _get_generate_script() -> str:
    """Return a small data generation script scaffold."""
    return '''"""Generate synthetic training data scaffold

Run from project root: python scripts/generate_synthetic.py
"""

import yaml
from pathlib import Path
from azcore.rl.synthetic_data.training_pipeline import SyntheticDataPipeline


def main():
    cfg_path = Path("configs/rl_training_config.yml")
    if not cfg_path.exists():
        print("Missing configs/rl_training_config.yml")
        return

    cfg = yaml.safe_load(cfg_path.read_text())
    tools = cfg.get("tools", [])
    synth_cfg = cfg.get("synthetic_data", {})

    pipeline = SyntheticDataPipeline(tool_names=tools, use_llm=synth_cfg.get("use_llm", False))
    data = pipeline.generate(num_samples=synth_cfg.get("num_samples", 1000), validate=synth_cfg.get("validate", True))

    out = Path("data/synthetic_data.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    import json
    with open(out, "w", encoding="utf-8") as f:
        json.dump([{
            "query": s["query"],
            "selected_tools": s["selected_tools"],
            "reward": s["reward"]
        } for s in data], f, indent=2)

    print(f"Written {len(data)} samples to {out}")


if __name__ == "__main__":
    main()
'''


def _get_env_example(template: str = "basic-agent") -> str:
    """Get .env.example content."""
    base_env = """# OpenAI API Key
OPENAI_API_KEY=your-api-key-here

# Anthropic API Key (optional)
ANTHROPIC_API_KEY=your-api-key-here

# LangSmith (optional)
LANGCHAIN_API_KEY=your-api-key-here
LANGCHAIN_TRACING_V2=false
LANGCHAIN_PROJECT=azcore-project
"""
    
    if template == "modular-team":
        base_env += """
# External API Keys (add as needed)
# SERPER_API_KEY=your-serper-key
# SENDGRID_API_KEY=your-sendgrid-key
# SLACK_BOT_TOKEN=your-slack-token
"""
    
    return base_env


def _write_file(path: Path, content: str):
    """Write content to file."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def _create_team_modules(project_path: Path):
    """Copy team module templates to project."""
    import shutil
    from pathlib import Path as PathLib
    
    # Get the template modules directory
    template_modules_dir = PathLib(__file__).parent.parent / "templates" / "team_modules"
    
    # Target directory
    target_dir = project_path / "team_modules"
    
    # Copy all module files
    if template_modules_dir.exists():
        for file in template_modules_dir.iterdir():
            if file.is_file() and file.suffix == ".py":
                shutil.copy2(file, target_dir / file.name)
    
    # Copy prompts directory
    prompts_source = template_modules_dir / "prompts"
    prompts_target = target_dir / "prompts"
    if prompts_source.exists():
        shutil.copytree(prompts_source, prompts_target, dirs_exist_ok=True)


def _interactive_template_selection() -> str:
    """Interactive template selection with descriptions."""
    click.echo("\n" + "=" * 70)
    click.secho("Available Project Templates", fg="cyan", bold=True)
    click.echo("=" * 70 + "\n")
    
    # Display all templates with details
    template_keys = list(TEMPLATES.keys())
    for idx, key in enumerate(template_keys, 1):
        template_info = TEMPLATES[key]
        
        # Template header
        click.secho(f"{idx}. {template_info['name']}", fg="green", bold=True)
        click.echo(f"   {template_info['description']}")
        
        # Details
        click.secho(f"   > Details: ", fg="blue", nl=False)
        click.echo(template_info['details'])
        
        # Use cases
        click.secho(f"   > Use Cases: ", fg="blue", nl=False)
        click.echo(", ".join(template_info['use_cases']))
        click.echo()
    
    # Get user selection
    click.echo("-" * 70)
    while True:
        choice = click.prompt(
            click.style("\nSelect a template", fg="yellow"),
            type=click.IntRange(1, len(template_keys)),
            default=1
        )
        
        selected_key = template_keys[choice - 1]
        selected_template = TEMPLATES[selected_key]
        
        # Confirm selection
        click.echo()
        click.secho(f"[*] Selected: {selected_template['name']}", fg="green")
        click.echo(f"    {selected_template['description']}")
        
        if click.confirm("\nProceed with this template?", default=True):
            return selected_key
        
        click.echo("\nLet's choose again...\n")
