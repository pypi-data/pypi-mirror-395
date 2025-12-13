"""
Settings dataclasses for type-safe configuration.

This module provides Pydantic-style dataclasses for configuration
with validation and type hints.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class LLMConfig:
    """
    Configuration for a language model.
    
    Attributes:
        model: Model identifier
        temperature: Sampling temperature (0-2)
        max_tokens: Maximum tokens to generate
        api_key: Optional API key
    """
    
    model: str = "gpt-4o-mini"
    temperature: float = 0.5
    max_tokens: Optional[int] = None
    api_key: Optional[str] = None
    
    def validate(self) -> bool:
        """
        Validate configuration.
        
        Returns:
            True if valid, False otherwise
        """
        if not 0 <= self.temperature <= 2:
            return False
        if self.max_tokens and self.max_tokens <= 0:
            return False
        return True


@dataclass
class RLConfig:
    """
    Configuration for Reinforcement Learning.
    
    Attributes:
        enabled: Enable RL-based tool selection
        q_table_path: Path to persist Q-table
        exploration_rate: Exploration probability (0-1)
        learning_rate: Learning rate alpha (0-1)
        discount_factor: Discount factor gamma (0-1)
        use_embeddings: Use semantic state matching
        embedding_model: Sentence transformer model name
        similarity_threshold: Minimum similarity for fuzzy match
        negative_reward_multiplier: Penalty multiplier for negative rewards
    """
    
    enabled: bool = False
    q_table_path: str = "rl_data/q_table.pkl"
    exploration_rate: float = 0.15
    learning_rate: float = 0.1
    discount_factor: float = 0.99
    use_embeddings: bool = True
    embedding_model: str = "all-MiniLM-L6-v2"
    similarity_threshold: float = 0.7
    negative_reward_multiplier: float = 1.5
    
    def validate(self) -> bool:
        """
        Validate configuration.
        
        Returns:
            True if valid, False otherwise
        """
        if not 0 <= self.exploration_rate <= 1:
            return False
        if not 0 <= self.learning_rate <= 1:
            return False
        if not 0 <= self.discount_factor <= 1:
            return False
        if not 0 <= self.similarity_threshold <= 1:
            return False
        return True


@dataclass
class Settings:
    """
    Complete framework settings.
    
    Attributes:
        llm: Main LLM configuration
        fast_llm: Fast LLM for quick operations
        coordinator_llm: LLM for coordinator
        embedding_model: Embedding model identifier
        log_level: Logging level
        rl: Reinforcement learning configuration
    """
    
    llm: LLMConfig = field(default_factory=LLMConfig)
    fast_llm: LLMConfig = field(default_factory=LLMConfig)
    coordinator_llm: LLMConfig = field(default_factory=lambda: LLMConfig(temperature=0))
    embedding_model: str = "text-embedding-3-large"
    log_level: str = "INFO"
    rl: RLConfig = field(default_factory=RLConfig)
    
    @classmethod
    def from_dict(cls, config: dict) -> 'Settings':
        """
        Create settings from dictionary.
        
        Args:
            config: Configuration dictionary
            
        Returns:
            Settings instance
        """
        return cls(
            llm=LLMConfig(**config.get("llm", {})),
            fast_llm=LLMConfig(**config.get("fast_llm", {})),
            coordinator_llm=LLMConfig(**config.get("coordinator_llm", {})),
            embedding_model=config.get("embedding_model", "text-embedding-3-large"),
            log_level=config.get("log_level", "INFO"),
            rl=RLConfig(**config.get("rl", {}))
        )
