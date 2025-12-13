"""Utility functions for team modules."""

from pathlib import Path
from typing import Optional


def load_prompt(team_name: str) -> str:
    """Load team prompt from markdown file.
    
    Args:
        team_name: Name of the team (e.g., 'research_team', 'data_team')
        
    Returns:
        str: The prompt content from the markdown file
    """
    prompt_file = Path(__file__).parent / "prompts" / f"{team_name}.md"
    
    if prompt_file.exists():
        return prompt_file.read_text(encoding='utf-8')
    else:
        # Fallback to a basic prompt if file not found
        return f"You are a {team_name.replace('_', ' ')} specialist. Use the appropriate tools to complete tasks."


def get_prompt_path(team_name: str) -> Path:
    """Get the path to a team's prompt file.
    
    Args:
        team_name: Name of the team
        
    Returns:
        Path: Path to the prompt markdown file
    """
    return Path(__file__).parent / "prompts" / f"{team_name}.md"
