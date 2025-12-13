"""
Prompt loading utilities for the Azcore..

This module provides functionality to load and manage system prompts
from files or templates.
"""

from pathlib import Path
from typing import Dict, Optional
import logging
from azcore.exceptions import ConfigurationError

logger = logging.getLogger(__name__)


class PromptLoader:
    """
    Loader for system prompts from files or templates.
    
    Supports loading prompts from markdown files with optional
    variable substitution.
    
    Example:
        >>> loader = PromptLoader("prompts/")
        >>> prompt = loader.load("coordinator.md")
        >>> # Or with variables
        >>> prompt = loader.load("team.md", team_name="security")
    """
    
    def __init__(self, prompts_dir: str | Path):
        """
        Initialize prompt loader.
        
        Args:
            prompts_dir: Directory containing prompt files
        """
        self.prompts_dir = Path(prompts_dir)
        self._cache: Dict[str, str] = {}
        self._logger = logging.getLogger(self.__class__.__name__)
        
        if not self.prompts_dir.exists():
            self._logger.warning(f"Prompts directory not found: {self.prompts_dir}")
    
    def load(
        self,
        prompt_name: str,
        variables: Optional[Dict[str, str]] = None,
        use_cache: bool = True
    ) -> str:
        """
        Load a prompt from file.
        
        Args:
            prompt_name: Name of the prompt file
            variables: Optional variables for substitution
            use_cache: Whether to use cached prompts
            
        Returns:
            Loaded prompt text
            
        Raises:
            FileNotFoundError: If prompt file doesn't exist
        """
        # Check cache
        if use_cache and prompt_name in self._cache and not variables:
            self._logger.debug(f"Using cached prompt: {prompt_name}")
            return self._cache[prompt_name]
        
        # Load from file
        prompt_path = self.prompts_dir / prompt_name
        
        if not prompt_path.exists():
            raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
        
        with open(prompt_path, 'r', encoding='utf-8') as f:
            prompt_text = f.read()
        
        # Substitute variables if provided
        if variables:
            for key, value in variables.items():
                placeholder = f"{{{key}}}"
                prompt_text = prompt_text.replace(placeholder, str(value))
        
        # Cache if no variables
        if not variables:
            self._cache[prompt_name] = prompt_text
        
        self._logger.debug(f"Loaded prompt: {prompt_name}")
        
        return prompt_text
    
    def load_template(
        self,
        template_name: str,
        **kwargs
    ) -> str:
        """
        Load a prompt template with keyword arguments.
        
        Args:
            template_name: Name of the template file
            **kwargs: Variables for substitution
            
        Returns:
            Rendered prompt text
        """
        return self.load(template_name, variables=kwargs, use_cache=False)
    
    def clear_cache(self) -> None:
        """Clear the prompt cache."""
        self._cache.clear()
        self._logger.debug("Cleared prompt cache")
    
    def list_prompts(self) -> list[str]:
        """
        List all available prompt files.
        
        Returns:
            List of prompt filenames
        """
        if not self.prompts_dir.exists():
            return []
        
        return [
            f.name for f in self.prompts_dir.iterdir()
            if f.is_file() and f.suffix in ['.md', '.txt']
        ]
    
    def __repr__(self) -> str:
        return f"PromptLoader(dir='{self.prompts_dir}', cached={len(self._cache)})"


# Global prompt loader instance
_default_loader: Optional[PromptLoader] = None


def set_default_prompts_dir(prompts_dir: str | Path) -> None:
    """
    Set the default prompts directory.
    
    Args:
        prompts_dir: Directory containing prompt files
    """
    global _default_loader
    _default_loader = PromptLoader(prompts_dir)
    logger.info(f"Set default prompts directory: {prompts_dir}")


def load_prompt(
    prompt_name: str,
    prompts_dir: Optional[str | Path] = None,
    **variables
) -> str:
    """
    Load a prompt using default or specified directory.
    
    Args:
        prompt_name: Name of the prompt file
        prompts_dir: Optional custom prompts directory
        **variables: Variables for substitution
        
    Returns:
        Loaded prompt text
    """
    global _default_loader
    
    if prompts_dir:
        loader = PromptLoader(prompts_dir)
    elif _default_loader:
        loader = _default_loader
    else:
        # Try common locations
        for common_dir in ["prompts", "agent/prompts", "arc/prompts"]:
            if Path(common_dir).exists():
                loader = PromptLoader(common_dir)
                break
        else:
            logger.error("No prompts directory found in default locations")
            raise ConfigurationError(
                "No prompts directory found. Use set_default_prompts_dir() "
                "or provide prompts_dir parameter",
                details={
                    "searched_locations": ["prompts", "agent/prompts", "arc/prompts"],
                    "prompt_name": prompt_name
                }
            )
    
    return loader.load(prompt_name, variables=variables if variables else None)
