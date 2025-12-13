"""Configuration file templates."""


def get_config_template(template_type: str) -> str:
    """Get configuration template based on project type."""
    
    if template_type == "basic-agent":
        return _get_basic_config()
    elif template_type == "team-agent":
        return _get_team_config()
    elif template_type == "rl-agent":
        return _get_rl_config()
    elif template_type == "workflow":
        return _get_workflow_config()
    else:
        return _get_basic_config()


def _get_basic_config() -> str:
    """Basic agent configuration."""
    return """# Az-Core Configuration

# LLM Configuration
llm:
  provider: openai
  model_name: gpt-4
  temperature: 0.7
  max_tokens: 2000

# Agent Configuration
agent:
  type: react
  max_iterations: 10
  early_stopping: true

# Logging
logging:
  level: INFO
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: ./logs/app.log
"""


def _get_team_config() -> str:
    """Team agent configuration."""
    return """# Az-Core Team Configuration

# LLM Configuration
llm:
  provider: openai
  model_name: gpt-4
  temperature: 0.7
  max_tokens: 2000

# Team Configuration
team:
  members:
    - name: researcher
      role: Research Specialist
      goal: Gather and analyze information
    - name: analyst
      role: Data Analyst
      goal: Analyze and provide insights
    - name: writer
      role: Content Writer
      goal: Create clear documentation

# Workflow
workflow:
  type: sequential
  max_rounds: 3

# Logging
logging:
  level: INFO
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: ./logs/app.log
"""


def _get_rl_config() -> str:
    """RL agent configuration."""
    return """# Az-Core RL Configuration

# LLM Configuration
llm:
  provider: openai
  model_name: gpt-4
  temperature: 0.7
  max_tokens: 2000

# RL Configuration
rl_config:
  learning_rate: 0.1
  discount_factor: 0.9
  exploration_strategy: epsilon_greedy
  epsilon: 0.2
  epsilon_decay: 0.995
  min_epsilon: 0.01
  q_table_path: ./rl_data/q_table.pkl
  save_frequency: 100

# Training Configuration
training:
  num_episodes: 1000
  max_steps_per_episode: 50
  reward_type: heuristic
  validation_split: 0.2

# Tools
tools:
  - name: calculator
    description: Perform mathematical calculations
  - name: search
    description: Search for information

# Logging
logging:
  level: INFO
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: ./logs/app.log
"""


def _get_workflow_config() -> str:
    """Workflow configuration."""
    return """# Az-Core Workflow Configuration

# LLM Configuration
llm:
  provider: openai
  model_name: gpt-4
  temperature: 0.7
  max_tokens: 2000

# Workflow Configuration
workflow:
  type: graph
  nodes:
    - name: planner
      type: planner
    - name: executor
      type: generator
    - name: validator
      type: validator
  
  edges:
    - [planner, executor]
    - [executor, validator]
    - [validator, __end__]
  
  entry_point: planner

# State Configuration
state:
  checkpointing: true
  checkpoint_dir: ./data/checkpoints

# Logging
logging:
  level: INFO
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: ./logs/app.log
"""
