"""Miscellaneous templates."""


def get_gitignore_template() -> str:
    """Get .gitignore template."""
    return """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Environment variables
.env
.env.local

# Logs
logs/
*.log

# Data
data/
rl_data/
models/
*.pkl
*.pt
*.pth

# Cache
.cache/
*.cache

# OS
.DS_Store
Thumbs.db

# Testing
.pytest_cache/
.coverage
htmlcov/

# Jupyter
.ipynb_checkpoints/
"""


def get_readme_template(project_name: str, template_type: str) -> str:
    """Get README template."""
    template_desc = {
        "basic-agent": "single agent setup",
        "team-agent": "multi-agent team collaboration",
        "modular-team": "modular team system with organized tool modules",
        "rl-agent": "RL-optimized agent with training capabilities",
        "workflow": "custom workflow orchestration",
    }
    
    desc = template_desc.get(template_type, "Az-Core project")
    
    return f"""# {project_name}

An Az-Core project with {desc}.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env and add your API keys
```

## Usage

Run the main application:
```bash
azcore run main.py
```

Or run with a custom input:
```bash
azcore run main.py --input "Your query here"
```

With a config file:
```bash
azcore run main.py --config configs/config.yml
```

## Configuration

Edit `configs/config.yml` to customize:
- LLM settings (model, temperature, etc.)
- Agent behavior
- Workflow parameters
- RL training settings (if applicable)

{"## Customizing Teams" if template_type == "modular-team" else ""}

{"Each team is defined in a separate module in `team_modules/`:" if template_type == "modular-team" else ""}

{"### Adding a New Team" if template_type == "modular-team" else ""}
{"1. Create a new file in `team_modules/` (e.g., `my_team_tools.py`)" if template_type == "modular-team" else ""}
{"2. Define your tools using `@tool` decorator" if template_type == "modular-team" else ""}
{"3. Export tools list and team config" if template_type == "modular-team" else ""}
{"4. Update `graph_builder.py` to include your team" if template_type == "modular-team" else ""}
{"5. Add team name to supervisor members list" if template_type == "modular-team" else ""}

{"### Team Module Structure" if template_type == "modular-team" else ""}
{"```python" if template_type == "modular-team" else ""}
{"from langchain_core.tools import tool" if template_type == "modular-team" else ""}

{"@tool" if template_type == "modular-team" else ""}
{"def my_tool(param: str) -> str:" if template_type == "modular-team" else ""}
{'    """Tool description."""' if template_type == "modular-team" else ""}
{"    return f'Result: {param}'" if template_type == "modular-team" else ""}

{"my_team_tools = [my_tool]" if template_type == "modular-team" else ""}

{"my_team_config = {" if template_type == "modular-team" else ""}
{'    "name": "my_team",' if template_type == "modular-team" else ""}
{'    "prompt": "Team prompt...",' if template_type == "modular-team" else ""}
{'    "description": "Team description"' if template_type == "modular-team" else ""}
{"}" if template_type == "modular-team" else ""}
{"```" if template_type == "modular-team" else ""}

## Project Structure

```
{project_name}/
├── main.py              # Main application entry point
{"├── team_modules/       # Modular team tool definitions" if template_type == "modular-team" else ""}
{"│   ├── __init__.py" if template_type == "modular-team" else ""}
{"│   ├── camera_tools.py      # Security camera tools" if template_type == "modular-team" else ""}
{"│   ├── document_tools.py    # Document management tools" if template_type == "modular-team" else ""}
{"│   ├── hr_tools.py          # HR & attendance tools" if template_type == "modular-team" else ""}
{"│   ├── mcp_teams.py         # MCP team builders" if template_type == "modular-team" else ""}
{"│   └── graph_builder.py     # Main graph orchestrator" if template_type == "modular-team" else ""}
{"├── database.py         # Database configuration" if template_type == "modular-team" else ""}
{"├── uploads/            # File upload directory" if template_type == "modular-team" else ""}
├── configs/             # Configuration files
│   └── config.yml
├── data/               # Data directory
├── logs/               # Log files
{"├── rl_data/           # RL training data" if template_type in ["rl-agent", "modular-team"] else ""}
{"├── models/            # Trained models" if template_type in ["rl-agent", "modular-team"] else ""}
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
└── README.md          # This file
```

## Commands

### Run
```bash
azcore run main.py
```

### Validate Configuration
```bash
azcore validate configs/config.yml
```

{"### Train RL Agent" if template_type == "rl-agent" else ""}
{"```bash" if template_type == "rl-agent" else ""}
{"azcore train rl-agent --config configs/config.yml --episodes 1000" if template_type == "rl-agent" else ""}
{"```" if template_type == "rl-agent" else ""}

{"### View Statistics" if template_type == "rl-agent" else ""}
{"```bash" if template_type == "rl-agent" else ""}
{"azcore stats --show-rl-metrics" if template_type == "rl-agent" else ""}
{"```" if template_type == "rl-agent" else ""}

## Documentation

- [Az-Core Documentation](https://github.com/Azrienlabs/Az-Core)
- [Examples](https://github.com/Azrienlabs/Az-Core/tree/main/examples)

## License

[Your License Here]
"""
