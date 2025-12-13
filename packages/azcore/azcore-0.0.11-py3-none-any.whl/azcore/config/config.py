"""
Configuration classes for the Azcore..

This module provides configuration management with YAML and environment
variable support, validation, and type safety.
"""

from typing import Optional, Dict, Any
from pathlib import Path
import yaml
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.embeddings import Embeddings
from azcore.exceptions import ConfigurationError
import logging

logger = logging.getLogger(__name__)


class Config:
    """
    Main configuration class for the Azcore..
    
    Supports loading from YAML files and environment variables with
    validation and type conversion.
    
    Example:
        >>> config = Config.from_yaml("config.yml")
        >>> llm = config.get_llm()
        >>> embeddings = config.get_embeddings()
    """
    
    def __init__(self, config_dict: Dict[str, Any]):
        """
        Initialize configuration from dictionary.
        
        Args:
            config_dict: Configuration dictionary
        """
        self._config = config_dict
        self._logger = logging.getLogger(self.__class__.__name__)
        
        self._logger.info("Configuration initialized")
    
    @classmethod
    def from_yaml(cls, config_path: str | Path) -> 'Config':
        """
        Load configuration from YAML file.
        
        Args:
            config_path: Path to YAML configuration file
            
        Returns:
            Config instance
            
        Raises:
            ConfigurationError: If config file doesn't exist or is invalid
        """
        config_path = Path(config_path)
        
        if not config_path.exists():
            # Check for common config file locations
            common_locations = [
                Path("config.yml"),
                Path("configs/config.yml"),
                Path(".azcore/config.yml")
            ]
            
            found_alternatives = [loc for loc in common_locations if loc.exists()]
            
            solution_parts = [
                "The configuration file was not found.",
                f"Looked for: {config_path}",
                "",
                "Solutions:",
                "1. Create a config file: azcore init",
                "2. Specify the correct path to your config file"
            ]
            
            if found_alternatives:
                solution_parts.append(f"3. Use one of the existing configs found: {', '.join(str(f) for f in found_alternatives)}")
            
            example_config = """# Example config.yml
llm:
  model: gpt-4o-mini
  temperature: 0.7

fast_llm:
  model: gpt-4o-mini
  temperature: 0.5

embedding_model: text-embedding-3-large"""
            
            from azcore.exceptions import ConfigurationError
            raise ConfigurationError(
                message=f"Configuration file not found: {config_path}",
                details={"path": str(config_path.absolute())},
                solution="\n".join(solution_parts),
                doc_url="https://docs.azrienlabs.com/configuration",
                examples=[example_config]
            )
        
        try:
            with open(config_path, 'r') as file:
                config_dict = yaml.safe_load(file)
        except yaml.YAMLError as e:
            solution = """The YAML file has syntax errors.

Common YAML mistakes:
• Check indentation (use spaces, not tabs)
• Ensure colons have spaces after them (key: value)
• Quote strings with special characters
• Check for unclosed quotes or brackets

Fix:
1. Run 'azcore validate config' for detailed validation
2. Use a YAML validator online to check syntax
3. Compare with example configs: azcore examples show basic-agent"""
            
            from azcore.exceptions import ConfigurationError
            raise ConfigurationError(
                message=f"Invalid YAML syntax in {config_path}",
                details={
                    "path": str(config_path),
                    "error": str(e),
                    "line": getattr(e, 'problem_mark', None)
                },
                solution=solution,
                doc_url="https://docs.azrienlabs.com/configuration/yaml-syntax"
            ) from e
        
        if config_dict is None:
            solution = """The configuration file is empty.

Solutions:
1. Add configuration to the file
2. Use 'azcore init' to generate a template
3. Copy example configuration from documentation"""
            
            example_config = """# Minimal config.yml
llm:
  model: gpt-4o-mini
  temperature: 0.7"""
            
            from azcore.exceptions import ConfigurationError
            raise ConfigurationError(
                message=f"Configuration file is empty: {config_path}",
                details={"path": str(config_path)},
                solution=solution,
                examples=[example_config]
            )
        
        logger.info(f"Loaded configuration from {config_path}")
        
        return cls(config_dict)
    
    @classmethod
    def from_env(cls, env_file: str | Path = ".env") -> 'Config':
        """
        Load configuration from environment variables.
        
        Args:
            env_file: Path to .env file (default: .env)
            
        Returns:
            Config instance
        """
        load_dotenv(env_file)
        
        config_dict = {
            "llm": {
                "model": os.getenv("LLM_MODEL", "gpt-4o-mini"),
                "temperature": float(os.getenv("LLM_TEMPERATURE", "0.5")),
                "api_key": os.getenv("OPENAI_API_KEY"),
            },
            "fast_llm": {
                "model": os.getenv("FAST_LLM_MODEL", "gpt-4o-mini"),
                "temperature": float(os.getenv("FAST_LLM_TEMPERATURE", "0.5")),
            },
            "coordinator_llm": {
                "model": os.getenv("COORDINATOR_LLM_MODEL", "gpt-4o-mini"),
                "temperature": float(os.getenv("COORDINATOR_LLM_TEMPERATURE", "0")),
            },
            "embedding_model": os.getenv("EMBEDDING_MODEL", "text-embedding-3-large"),
        }
        
        logger.info("Loaded configuration from environment variables")
        
        return cls(config_dict)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key.
        
        Args:
            key: Configuration key (supports dot notation: "llm.model")
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value.
        
        Args:
            key: Configuration key (supports dot notation)
            value: Value to set
        """
        keys = key.split('.')
        config = self._config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        self._logger.debug(f"Set config: {key} = {value}")
    
    def get_llm(
        self,
        llm_key: str = "llm",
        provider: str = "openai"
    ) -> BaseChatModel:
        """
        Get a language model from configuration.
        
        Args:
            llm_key: Configuration key for LLM settings (default: "llm")
            provider: LLM provider (default: "openai")
            
        Returns:
            Configured language model
            
        Raises:
            ConfigurationError: If provider is not supported or config is invalid
        """
        llm_config = self.get(llm_key, {})
        
        if not llm_config:
            example_config = f"""# Add to your config.yml
{llm_key}:
  model: gpt-4o-mini
  temperature: 0.7"""
            
            from azcore.exceptions import create_config_error
            raise create_config_error(
                key=llm_key,
                value="<empty>",
                reason="LLM configuration is missing",
                example_config=example_config
            )
        
        if provider == "openai":
            # Validate temperature if present
            temperature = llm_config.get("temperature", 0.5)
            if not isinstance(temperature, (int, float)) or not (0 <= temperature <= 2):
                example = f"""# Valid temperature configuration
{llm_key}:
  model: gpt-4o-mini
  temperature: 0.7  # Must be between 0 and 2"""
                
                from azcore.exceptions import create_config_error
                raise create_config_error(
                    key=f"{llm_key}.temperature",
                    value=temperature,
                    reason="Temperature must be a number between 0 and 2",
                    valid_values=["0.0 to 2.0"],
                    example_config=example
                )
            
            try:
                return ChatOpenAI(
                    model=llm_config.get("model", "gpt-4o-mini"),
                    temperature=temperature,
                )
            except Exception as e:
                from azcore.exceptions import create_llm_error
                raise create_llm_error(
                    error_message=f"Failed to initialize OpenAI LLM: {str(e)}",
                    model=llm_config.get("model"),
                    provider="openai",
                    original_error=e
                )
        else:
            self._logger.error(f"Unsupported LLM provider requested: {provider}")
            
            from azcore.exceptions import create_config_error, suggest_similar
            
            supported = ["openai"]
            suggestion = suggest_similar(provider, supported)
            
            solution_parts = [
                f"Supported providers: {', '.join(supported)}",
            ]
            
            if suggestion:
                solution_parts.append(suggestion)
            
            solution_parts.append(f"\nUpdate your configuration to use a supported provider.")
            
            raise ConfigurationError(
                message=f"Unsupported LLM provider: {provider}",
                details={
                    "provider": provider,
                    "supported_providers": supported,
                    "llm_key": llm_key
                },
                solution="\n".join(solution_parts),
                doc_url="https://docs.azrienlabs.com/configuration/providers"
            )
    
    def get_embeddings(
        self,
        provider: str = "openai"
    ) -> Embeddings:
        """
        Get embeddings model from configuration.
        
        Args:
            provider: Embeddings provider (default: "openai")
            
        Returns:
            Configured embeddings model
            
        Raises:
            ConfigurationError: If provider is not supported
        """
        if provider == "openai":
            model = self.get("embedding_model", "text-embedding-3-large")
            try:
                return OpenAIEmbeddings(model=model)
            except Exception as e:
                from azcore.exceptions import create_llm_error
                raise create_llm_error(
                    error_message=f"Failed to initialize embeddings: {str(e)}",
                    model=model,
                    provider="openai",
                    original_error=e
                )
        else:
            self._logger.error(f"Unsupported embeddings provider requested: {provider}")
            
            from azcore.exceptions import suggest_similar
            supported = ["openai"]
            suggestion = suggest_similar(provider, supported)
            
            solution = f"Supported providers: {', '.join(supported)}\n"
            if suggestion:
                solution += f"{suggestion}\n"
            solution += "Update your configuration to use a supported provider."
            
            raise ConfigurationError(
                f"Unsupported embeddings provider: {provider}",
                details={
                    "provider": provider,
                    "supported_providers": supported
                },
                solution=solution,
                doc_url="https://docs.azrienlabs.com/configuration/embeddings"
            )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Get configuration as dictionary.
        
        Returns:
            Configuration dictionary
        """
        return self._config.copy()
    
    def save(self, output_path: str | Path) -> None:
        """
        Save configuration to YAML file.
        
        Args:
            output_path: Path to save configuration
        """
        output_path = Path(output_path)
        
        with open(output_path, 'w') as file:
            yaml.dump(self._config, file, default_flow_style=False)
        
        self._logger.info(f"Saved configuration to {output_path}")
    
    def __repr__(self) -> str:
        return f"Config(keys={list(self._config.keys())})"


def load_config(
    config_path: Optional[str | Path] = None,
    env_file: Optional[str | Path] = None
) -> Config:
    """
    Load configuration from file or environment.
    
    Priority:
    1. YAML file if config_path provided
    2. Environment variables if env_file provided
    3. Default .env in current directory
    
    Args:
        config_path: Optional path to YAML config file
        env_file: Optional path to .env file
        
    Returns:
        Config instance
    """
    if config_path:
        return Config.from_yaml(config_path)
    elif env_file:
        return Config.from_env(env_file)
    else:
        # Try default locations
        if Path("config.yml").exists():
            return Config.from_yaml("config.yml")
        elif Path(".env").exists():
            return Config.from_env(".env")
        else:
            logger.warning("No configuration file found, using defaults")
            return Config({})
