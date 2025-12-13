"""
Configuration validation using Pydantic models.

This module provides Pydantic models for validating framework configuration,
ensuring type safety and value constraints are enforced.
"""

from typing import Optional, Dict, Any, List
from pathlib import Path
from pydantic import BaseModel, Field, field_validator, model_validator
import logging
from azcore.exceptions import ValidationError

logger = logging.getLogger(__name__)


class LLMConfig(BaseModel):
    """
    Configuration for a language model.
    
    Attributes:
        model: Model name/identifier
        temperature: Sampling temperature (0.0 = deterministic, 2.0 = very random)
        max_tokens: Maximum tokens to generate
        timeout: Request timeout in seconds
        api_key: Optional API key (prefer environment variables)
        max_retries: Maximum retry attempts for failed requests
    """
    model: str = Field(
        ...,
        min_length=1,
        description="Model name or identifier"
    )
    temperature: float = Field(
        default=0.5,
        ge=0.0,
        le=2.0,
        description="Sampling temperature"
    )
    max_tokens: int = Field(
        default=4096,
        ge=1,
        le=100000,
        description="Maximum tokens to generate"
    )
    timeout: float = Field(
        default=30.0,
        ge=1.0,
        le=300.0,
        description="Request timeout in seconds"
    )
    api_key: Optional[str] = Field(
        default=None,
        description="API key (prefer environment variables)"
    )
    max_retries: int = Field(
        default=3,
        ge=0,
        le=10,
        description="Maximum retry attempts"
    )
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "model": "gpt-4o-mini",
                    "temperature": 0.7,
                    "max_tokens": 2000,
                    "timeout": 30.0,
                    "max_retries": 3
                }
            ]
        }
    }


class RLConfig(BaseModel):
    """
    Configuration for Reinforcement Learning.
    
    Attributes:
        enabled: Whether RL is enabled
        exploration_rate: Probability of random exploration (epsilon-greedy)
        learning_rate: Q-learning learning rate (alpha)
        discount_factor: Future reward discount factor (gamma)
        q_table_path: Path to persist Q-table
        use_embeddings: Whether to use semantic embeddings for state matching
        embedding_model: Sentence transformer model name
        similarity_threshold: Minimum cosine similarity for state matching
        negative_reward_multiplier: Penalty multiplier for negative rewards
    """
    enabled: bool = Field(
        default=False,
        description="Enable reinforcement learning"
    )
    exploration_rate: float = Field(
        default=0.15,
        ge=0.0,
        le=1.0,
        description="Exploration probability (epsilon)"
    )
    learning_rate: float = Field(
        default=0.1,
        ge=0.0,
        le=1.0,
        description="Learning rate (alpha)"
    )
    discount_factor: float = Field(
        default=0.99,
        ge=0.0,
        le=1.0,
        description="Discount factor (gamma)"
    )
    q_table_path: str = Field(
        default="rl_data/q_table.pkl",
        description="Path to Q-table file"
    )
    use_embeddings: bool = Field(
        default=True,
        description="Use semantic embeddings for state matching"
    )
    embedding_model: str = Field(
        default="all-MiniLM-L6-v2",
        description="Sentence transformer model name"
    )
    similarity_threshold: float = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="Minimum similarity for state matching"
    )
    negative_reward_multiplier: float = Field(
        default=1.5,
        ge=1.0,
        le=5.0,
        description="Penalty multiplier for negative rewards"
    )
    
    @field_validator('q_table_path')
    @classmethod
    def validate_path(cls, v: str) -> str:
        """Ensure Q-table directory exists."""
        path = Path(v)
        if not path.parent.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created Q-table directory: {path.parent}")
        return str(path)
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "enabled": True,
                    "exploration_rate": 0.15,
                    "learning_rate": 0.1,
                    "q_table_path": "rl_data/my_q_table.pkl",
                    "use_embeddings": True
                }
            ]
        }
    }


class GraphConfig(BaseModel):
    """
    Configuration for graph orchestration.
    
    Attributes:
        max_iterations: Maximum workflow iterations to prevent infinite loops
        timeout: Maximum workflow execution time in seconds
        enable_checkpointing: Enable state checkpointing
        checkpoint_dir: Directory for checkpoint files
        enable_cycle_detection: Detect and prevent routing cycles
    """
    max_iterations: int = Field(
        default=20,
        ge=1,
        le=100,
        description="Maximum workflow iterations"
    )
    timeout: float = Field(
        default=120.0,
        ge=1.0,
        le=600.0,
        description="Maximum workflow execution time"
    )
    enable_checkpointing: bool = Field(
        default=True,
        description="Enable state checkpointing"
    )
    checkpoint_dir: str = Field(
        default="checkpoints",
        description="Checkpoint directory"
    )
    enable_cycle_detection: bool = Field(
        default=True,
        description="Detect routing cycles"
    )
    
    @field_validator('checkpoint_dir')
    @classmethod
    def validate_checkpoint_dir(cls, v: str) -> str:
        """Ensure checkpoint directory exists."""
        path = Path(v)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created checkpoint directory: {path}")
        return str(path)


class LoggingConfig(BaseModel):
    """
    Configuration for logging.
    
    Attributes:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format: Log message format
        log_file: Optional log file path
        enable_structured_logging: Use structured JSON logging
    """
    level: str = Field(
        default="INFO",
        description="Logging level"
    )
    format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log message format"
    )
    log_file: Optional[str] = Field(
        default=None,
        description="Optional log file path"
    )
    enable_structured_logging: bool = Field(
        default=False,
        description="Use structured JSON logging"
    )
    
    @field_validator('level')
    @classmethod
    def validate_level(cls, v: str) -> str:
        """Validate logging level."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        v_upper = v.upper()
        if v_upper not in valid_levels:
            logger.error(f"Invalid logging level provided: {v}")
            raise ValidationError(
                f"Invalid logging level: {v}. Must be one of {valid_levels}",
                details={
                    "provided_level": v,
                    "valid_levels": valid_levels
                }
            )
        return v_upper


class FrameworkConfig(BaseModel):
    """
    Complete framework configuration.
    
    This is the root configuration model that contains all subsystem configs.
    
    Attributes:
        llm: Primary language model configuration
        fast_llm: Fast language model for simple tasks
        coordinator_llm: Language model for coordinator node
        embedding_model: Embedding model name
        rl: Reinforcement learning configuration
        graph: Graph orchestration configuration
        logging: Logging configuration
    """
    llm: LLMConfig = Field(
        ...,
        description="Primary language model configuration"
    )
    fast_llm: Optional[LLMConfig] = Field(
        default=None,
        description="Fast LLM for simple tasks"
    )
    coordinator_llm: Optional[LLMConfig] = Field(
        default=None,
        description="Coordinator LLM configuration"
    )
    embedding_model: str = Field(
        default="text-embedding-3-large",
        description="Embedding model name"
    )
    rl: RLConfig = Field(
        default_factory=RLConfig,
        description="Reinforcement learning configuration"
    )
    graph: GraphConfig = Field(
        default_factory=GraphConfig,
        description="Graph orchestration configuration"
    )
    logging: LoggingConfig = Field(
        default_factory=LoggingConfig,
        description="Logging configuration"
    )
    
    @model_validator(mode='after')
    def set_defaults(self) -> 'FrameworkConfig':
        """Set default values for optional configs."""
        # Use primary LLM for fast_llm if not specified
        if self.fast_llm is None:
            self.fast_llm = self.llm.model_copy()
        
        # Use primary LLM for coordinator if not specified
        if self.coordinator_llm is None:
            self.coordinator_llm = self.llm.model_copy()
            self.coordinator_llm.temperature = 0.0  # Coordinator should be deterministic
        
        return self
    
    def validate_rl_requirements(self) -> None:
        """Validate that RL requirements are met if enabled."""
        if self.rl.enabled and self.rl.use_embeddings:
            try:
                import sentence_transformers
                logger.info("RL embeddings requirement satisfied")
            except ImportError:
                logger.warning(
                    "RL is enabled with embeddings but sentence-transformers is not installed. "
                    "Install with: pip install sentence-transformers"
                )
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "llm": {
                        "model": "gpt-4o-mini",
                        "temperature": 0.7,
                        "timeout": 30.0
                    },
                    "embedding_model": "text-embedding-3-large",
                    "rl": {
                        "enabled": True,
                        "exploration_rate": 0.15
                    },
                    "graph": {
                        "max_iterations": 20,
                        "timeout": 120.0
                    }
                }
            ]
        }
    }


def validate_config_dict(config_dict: Dict[str, Any]) -> FrameworkConfig:
    """
    Validate a configuration dictionary.
    
    Args:
        config_dict: Dictionary to validate
        
    Returns:
        Validated FrameworkConfig instance
        
    Raises:
        ValidationError: If validation fails
        
    Example:
        >>> config_dict = {
        ...     "llm": {"model": "gpt-4o-mini", "temperature": 0.7},
        ...     "rl": {"enabled": True}
        ... }
        >>> config = validate_config_dict(config_dict)
    """
    from azcore.exceptions import ValidationError
    
    try:
        config = FrameworkConfig(**config_dict)
        config.validate_rl_requirements()
        logger.info("Configuration validated successfully")
        return config
    except Exception as e:
        raise ValidationError(
            f"Configuration validation failed: {str(e)}",
            details={"config": config_dict}
        )


def load_and_validate_config(config_path: str) -> FrameworkConfig:
    """
    Load and validate configuration from YAML file.
    
    Args:
        config_path: Path to YAML configuration file
        
    Returns:
        Validated FrameworkConfig instance
        
    Raises:
        ConfigurationError: If loading or validation fails
        
    Example:
        >>> config = load_and_validate_config("config.yml")
    """
    from azcore.exceptions import ConfigurationError
    import yaml
    
    try:
        with open(config_path, 'r') as f:
            config_dict = yaml.safe_load(f)
        
        return validate_config_dict(config_dict)
        
    except FileNotFoundError:
        raise ConfigurationError(
            f"Configuration file not found: {config_path}"
        )
    except yaml.YAMLError as e:
        raise ConfigurationError(
            f"Invalid YAML in configuration file: {str(e)}",
            details={"path": config_path}
        )
    except Exception as e:
        raise ConfigurationError(
            f"Failed to load configuration: {str(e)}",
            details={"path": config_path}
        )
