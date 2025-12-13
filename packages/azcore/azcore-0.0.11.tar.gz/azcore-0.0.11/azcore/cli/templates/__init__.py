"""Templates for project initialization."""

from azcore.cli.templates.agent_templates import (
    get_basic_agent_template,
    get_team_agent_template,
    get_rl_agent_template,
    get_modular_team_agent_template,
)
from azcore.cli.templates.workflow_templates import get_workflow_template
from azcore.cli.templates.config_templates import get_config_template
from azcore.cli.templates.misc_templates import (
    get_gitignore_template,
    get_readme_template,
)

__all__ = [
    "get_basic_agent_template",
    "get_team_agent_template",
    "get_rl_agent_template",
    "get_modular_team_agent_template",
    "get_workflow_template",
    "get_config_template",
    "get_gitignore_template",
    "get_readme_template",
]
