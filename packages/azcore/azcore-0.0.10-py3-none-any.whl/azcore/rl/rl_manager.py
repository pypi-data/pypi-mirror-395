"""
Q-learning based Reinforcement Learning Manager for Azcore..

This module implements a Q-learning algorithm with semantic state matching
for intelligent tool selection and continual optimization.
"""

import logging
import os
import pickle
import random
import numpy as np
import asyncio
import threading
import time
from collections import defaultdict
from typing import List, Dict, Optional, Tuple, Any, DefaultDict, Callable
from pathlib import Path
from enum import Enum
from azcore.utils.caching import get_embedding_cache

logger = logging.getLogger(__name__)


class ExplorationStrategy(Enum):
    """Exploration strategies for RL tool selection."""
    EPSILON_GREEDY = "epsilon_greedy"
    UCB = "ucb"  # Upper Confidence Bound
    THOMPSON_SAMPLING = "thompson_sampling"
    EPSILON_DECAY = "epsilon_decay"


class RLManager:
    """
    Reinforcement Learning Manager using Q-learning for tool selection.
    
    This manager learns which tools work best for different query contexts
    through experience, using Q-learning with optional semantic state matching.
    
    Features:
    - Q-learning algorithm for value-based decision making
    - Semantic similarity matching for state generalization (optional)
    - Persistent Q-table storage
    - Configurable exploration/exploitation trade-off
    - Support for both discrete and continuous reward signals
    
    Example:
        >>> rl = RLManager(
        ...     tool_names=["search", "calculator", "weather"],
        ...     q_table_path="data/q_table.pkl",
        ...     use_embeddings=True
        ... )
        >>> selected_tools, state_key = rl.select_tools(query="What's 2+2?", top_n=2)
        >>> # ... execute tools ...
        >>> rl.update(state_key, "calculator", reward=1.0)
    """
    
    def __init__(
        self,
        tool_names: List[str],
        q_table_path: str = "rl_data/q_table.pkl",
        exploration_rate: float = 0.15,
        learning_rate: float = 0.1,
        discount_factor: float = 0.99,
        use_embeddings: bool = True,
        embedding_model_name: str = "all-MiniLM-L6-v2",
        similarity_threshold: float = 0.7,
        negative_reward_multiplier: float = 1.5,
        exploration_strategy: ExplorationStrategy = ExplorationStrategy.EPSILON_GREEDY,
        ucb_c: float = 2.0,
        epsilon_decay_rate: float = 0.995,
        min_exploration_rate: float = 0.01,
        enable_q_table_pruning: bool = False,
        prune_threshold: int = 100,
        min_visits_to_keep: int = 5,
        enable_q_value_decay: bool = False,
        q_decay_rate: float = 0.999,
        state_cache_size: int = 1000,
        enable_async_persistence: bool = True,
        batch_update_size: int = 10
    ):
        """
        Initialize the RL Manager.
        
        Args:
            tool_names: List of available tool names
            q_table_path: Path to persist Q-table
            exploration_rate: Probability of random exploration (0-1)
            learning_rate: Learning rate alpha for Q-learning (0-1)
            discount_factor: Discount factor gamma for future rewards (0-1)
            use_embeddings: Whether to use semantic embeddings for state matching
            embedding_model_name: Name of sentence transformer model
            similarity_threshold: Minimum cosine similarity for fuzzy matching
            negative_reward_multiplier: Penalty multiplier for negative rewards
            exploration_strategy: Strategy to use for exploration (epsilon-greedy, UCB, etc.)
            ucb_c: Exploration constant for UCB algorithm
            epsilon_decay_rate: Decay rate for epsilon-decay strategy
            min_exploration_rate: Minimum exploration rate after decay
            enable_q_table_pruning: Enable automatic pruning of rarely-used states
            prune_threshold: Number of states before triggering pruning
            min_visits_to_keep: Minimum visits required to keep a state
            enable_q_value_decay: Enable decay of Q-values over time
            q_decay_rate: Decay rate for Q-values
            state_cache_size: Size of in-memory cache for hot states
            enable_async_persistence: Enable asynchronous Q-table persistence
            batch_update_size: Number of updates before persisting
        """
        self.tool_names = list(set(tool_names))
        self.exploration_rate = exploration_rate
        self.initial_exploration_rate = exploration_rate
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.q_table_path = Path(q_table_path)
        self.use_embeddings = use_embeddings
        self.similarity_threshold = similarity_threshold
        self.negative_reward_multiplier = negative_reward_multiplier
        
        # New parameters
        self.exploration_strategy = exploration_strategy
        self.ucb_c = ucb_c
        self.epsilon_decay_rate = epsilon_decay_rate
        self.min_exploration_rate = min_exploration_rate
        self.enable_q_table_pruning = enable_q_table_pruning
        self.prune_threshold = prune_threshold
        self.min_visits_to_keep = min_visits_to_keep
        self.enable_q_value_decay = enable_q_value_decay
        self.q_decay_rate = q_decay_rate
        self.state_cache_size = state_cache_size
        self.enable_async_persistence = enable_async_persistence
        self.batch_update_size = batch_update_size
        
        # Initialize embedding model if enabled
        self.embedding_model = None
        if use_embeddings:
            try:
                from sentence_transformers import SentenceTransformer
                logger.info(f"Loading embedding model: {embedding_model_name}")
                self.embedding_model = SentenceTransformer(embedding_model_name)
                logger.info("Embedding model loaded successfully")
            except ImportError:
                logger.warning(
                    "sentence-transformers not installed. "
                    "Semantic state matching disabled. "
                    "Install with: pip install sentence-transformers"
                )
                self.use_embeddings = False
            except Exception as e:
                logger.error(f"Failed to load embedding model: {e}")
                self.use_embeddings = False
        
        # Initialize Q-table and state embeddings FIRST
        self.q_table: DefaultDict[str, DefaultDict[str, float]] = defaultdict(
            lambda: defaultdict(float)
        )
        self.state_embeddings: Dict[str, np.ndarray] = {}
        
        # Initialize new data structures BEFORE loading
        self.visit_counts: DefaultDict[str, DefaultDict[str, int]] = defaultdict(
            lambda: defaultdict(int)
        )
        self.state_visit_counts: DefaultDict[str, int] = defaultdict(int)
        self.last_access_time: Dict[str, float] = {}
        self.state_cache: Dict[str, Dict[str, float]] = {}
        self.pending_updates: List[Tuple[str, str, float, Optional[str]]] = []
        self.update_lock = threading.Lock()
        self.persist_thread: Optional[threading.Thread] = None
        self.stop_persist_thread = False
        
        # Thompson Sampling parameters
        self.alpha_params: DefaultDict[str, DefaultDict[str, float]] = defaultdict(
            lambda: defaultdict(lambda: 1.0)
        )
        self.beta_params: DefaultDict[str, DefaultDict[str, float]] = defaultdict(
            lambda: defaultdict(lambda: 1.0)
        )
        
        # NOW load persisted data
        self._load_persisted_data()
        
        # Initialize Q-values for all tools
        self._initialize_tool_values()
        
        # Start async persistence if enabled
        if self.enable_async_persistence:
            self._start_async_persistence()
        
        logger.info(
            f"RLManager initialized with {len(self.tool_names)} tools, "
            f"exploration_rate={exploration_rate}, embeddings={use_embeddings}, "
            f"strategy={exploration_strategy.value}"
        )
    
    def _initialize_tool_values(self) -> None:
        """Initialize Q-values for all known tools to 0.0."""
        for state_key in list(self.q_table.keys()):
            for tool_name in self.tool_names:
                self.q_table[state_key].setdefault(tool_name, 0.0)
    
    def _load_persisted_data(self) -> None:
        """Load Q-table and state embeddings from disk if available."""
        if not self.q_table_path.exists():
            logger.info(f"No existing Q-table found at {self.q_table_path}")
            return
        
        try:
            with open(self.q_table_path, "rb") as f:
                data = pickle.load(f)
                
            # Load Q-table
            loaded_q_table = data.get("q_table", {})
            for state, actions in loaded_q_table.items():
                self.q_table[state] = defaultdict(float, actions)
            
            # Load embeddings if available
            if self.use_embeddings:
                self.state_embeddings = data.get("state_embeddings", {})
            
            # Load new data structures if available
            loaded_visit_counts = data.get("visit_counts", {})
            for state, actions in loaded_visit_counts.items():
                self.visit_counts[state] = defaultdict(int, actions)
            
            loaded_state_visits = data.get("state_visit_counts", {})
            self.state_visit_counts = defaultdict(int, loaded_state_visits)
            
            self.last_access_time = data.get("last_access_time", {})
            
            # Load Thompson Sampling parameters if available
            loaded_alpha = data.get("alpha_params", {})
            for state, actions in loaded_alpha.items():
                self.alpha_params[state] = defaultdict(lambda: 1.0, actions)
            
            loaded_beta = data.get("beta_params", {})
            for state, actions in loaded_beta.items():
                self.beta_params[state] = defaultdict(lambda: 1.0, actions)
            
            logger.info(
                f"Loaded Q-table with {len(self.q_table)} states "
                f"and {len(self.state_embeddings)} embeddings"
            )
        except Exception as e:
            logger.error(f"Error loading Q-table from {self.q_table_path}: {e}")
    
    def _save_persisted_data(self) -> None:
        """Save Q-table and state embeddings to disk."""
        # Ensure directory exists
        self.q_table_path.parent.mkdir(parents=True, exist_ok=True)
        
        with self.update_lock:
            # Convert to regular dicts for pickling
            q_table_dict = {
                state: dict(actions) for state, actions in self.q_table.items()
            }
            
            visit_counts_dict = {
                state: dict(actions) for state, actions in self.visit_counts.items()
            }
            
            alpha_params_dict = {
                state: dict(actions) for state, actions in self.alpha_params.items()
            }
            
            beta_params_dict = {
                state: dict(actions) for state, actions in self.beta_params.items()
            }
            
            data = {
                "q_table": q_table_dict,
                "state_embeddings": self.state_embeddings,
                "visit_counts": visit_counts_dict,
                "state_visit_counts": dict(self.state_visit_counts),
                "last_access_time": self.last_access_time,
                "alpha_params": alpha_params_dict,
                "beta_params": beta_params_dict
            }
        
        try:
            with open(self.q_table_path, "wb") as f:
                pickle.dump(data, f)
            logger.debug(f"Saved Q-table to {self.q_table_path}")
        except Exception as e:
            logger.error(f"Error saving Q-table to {self.q_table_path}: {e}")
    
    def _get_embedding(self, text: str) -> Optional[np.ndarray]:
        """
        Generate embedding for a text string with caching.
        
        Uses global embedding cache to avoid recomputing embeddings.
        """
        if not self.embedding_model:
            return None
        
        # Try cache first
        embedding_cache = get_embedding_cache()
        cached_embedding = embedding_cache.get(text)
        
        if cached_embedding is not None:
            logger.debug(f"Embedding cache HIT for: {text[:50]}...")
            return cached_embedding
        
        # Cache miss - compute embedding
        try:
            logger.debug(f"Embedding cache MISS - computing for: {text[:50]}...")
            embedding = self.embedding_model.encode(text, convert_to_numpy=True)
            
            # Store in cache
            embedding_cache.put(text, embedding)
            
            return embedding
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            return None
    
    def _cache_embedding(self, state_key: str) -> None:
        """Cache embedding for a state key."""
        if not self.use_embeddings or state_key in self.state_embeddings:
            return
        
        embedding = self._get_embedding(state_key)
        if embedding is not None:
            self.state_embeddings[state_key] = embedding
            logger.debug(f"Cached embedding for state: {state_key[:50]}...")
    
    def _find_similar_state(self, query: str) -> Optional[str]:
        """
        Find the most similar existing state using semantic similarity.
        
        Args:
            query: Query string to match
            
        Returns:
            Most similar state key if above threshold, None otherwise
        """
        if not self.use_embeddings or not self.state_embeddings:
            return None
        
        query_embedding = self._get_embedding(query)
        if query_embedding is None:
            return None
        
        # Get candidate states (those in Q-table)
        candidate_states = [s for s in self.q_table.keys() if s != query]
        if not candidate_states:
            return None
        
        # Compute similarities
        try:
            from sentence_transformers import util
            import torch
            
            candidate_embeddings = [
                self.state_embeddings[s] for s in candidate_states 
                if s in self.state_embeddings
            ]
            
            if not candidate_embeddings:
                return None
            
            # Convert to numpy arrays first, then to tensors to avoid slow list conversion
            query_tensor = torch.tensor(np.array([query_embedding]))
            candidate_tensor = torch.tensor(np.array(candidate_embeddings))
            
            similarities = util.cos_sim(query_tensor, candidate_tensor)[0]
            similarities = similarities.cpu().numpy() if hasattr(similarities, 'cpu') else np.array(similarities)
            
            max_idx = np.argmax(similarities)
            max_similarity = similarities[max_idx]
            
            if max_similarity >= self.similarity_threshold:
                similar_state = candidate_states[max_idx]
                logger.info(
                    f"Found similar state with similarity {max_similarity:.3f}: "
                    f"{similar_state[:50]}..."
                )
                return similar_state
        except Exception as e:
            logger.error(f"Error computing similarity: {e}")
        
        return None
    
    def _start_async_persistence(self) -> None:
        """Start background thread for async Q-table persistence."""
        def persist_worker():
            while not self.stop_persist_thread:
                time.sleep(5)  # Check every 5 seconds
                if len(self.pending_updates) >= self.batch_update_size:
                    self._save_persisted_data()
                    with self.update_lock:
                        self.pending_updates.clear()
        
        self.persist_thread = threading.Thread(target=persist_worker, daemon=True)
        self.persist_thread.start()
        logger.info("Started async persistence thread")
    
    def _stop_async_persistence(self) -> None:
        """Stop background persistence thread."""
        if self.persist_thread and self.persist_thread.is_alive():
            self.stop_persist_thread = True
            self.persist_thread.join(timeout=2)
            logger.info("Stopped async persistence thread")
    
    def _prune_q_table(self) -> None:
        """Prune rarely-used states from Q-table."""
        if not self.enable_q_table_pruning:
            return
        
        if len(self.q_table) < self.prune_threshold:
            return
        
        states_to_remove = []
        for state_key in self.q_table.keys():
            total_visits = self.state_visit_counts.get(state_key, 0)
            if total_visits < self.min_visits_to_keep:
                states_to_remove.append(state_key)
        
        with self.update_lock:
            for state_key in states_to_remove:
                del self.q_table[state_key]
                if state_key in self.visit_counts:
                    del self.visit_counts[state_key]
                if state_key in self.state_visit_counts:
                    del self.state_visit_counts[state_key]
                if state_key in self.state_embeddings:
                    del self.state_embeddings[state_key]
                if state_key in self.last_access_time:
                    del self.last_access_time[state_key]
        
        if states_to_remove:
            logger.info(f"Pruned {len(states_to_remove)} rarely-used states from Q-table")
    
    def _apply_q_value_decay(self) -> None:
        """Apply decay to Q-values to prioritize recent experiences."""
        if not self.enable_q_value_decay:
            return
        
        current_time = time.time()
        with self.update_lock:
            for state_key in self.q_table.keys():
                last_access = self.last_access_time.get(state_key, current_time)
                time_delta = current_time - last_access
                
                # Apply decay based on time since last access
                if time_delta > 3600:  # More than 1 hour
                    decay_factor = self.q_decay_rate ** (time_delta / 3600)
                    for action in self.q_table[state_key]:
                        self.q_table[state_key][action] *= decay_factor
    
    def _get_cached_q_values(self, state_key: str) -> Optional[Dict[str, float]]:
        """Get Q-values from cache if available."""
        if state_key in self.state_cache:
            return self.state_cache[state_key]
        return None
    
    def _update_cache(self, state_key: str, q_values: Dict[str, float]) -> None:
        """Update state cache with Q-values."""
        if len(self.state_cache) >= self.state_cache_size:
            # Remove oldest entry (simple FIFO)
            oldest_key = next(iter(self.state_cache))
            del self.state_cache[oldest_key]
        
        self.state_cache[state_key] = q_values.copy()
    
    def _select_tools_ucb(self, state_key: str, top_n: int = 3) -> List[str]:
        """
        Select tools using Upper Confidence Bound (UCB) exploration.
        
        Args:
            state_key: State to select tools for
            top_n: Number of tools to select
            
        Returns:
            List of selected tool names
        """
        total_visits = sum(self.visit_counts[state_key].values())
        if total_visits == 0:
            # No visits yet, return random selection
            return random.sample(self.tool_names, k=min(top_n, len(self.tool_names)))
        
        ucb_scores = {}
        for tool in self.tool_names:
            q_value = self.q_table[state_key][tool]
            visits = self.visit_counts[state_key][tool]
            
            if visits == 0:
                ucb_scores[tool] = float('inf')
            else:
                exploration_bonus = self.ucb_c * np.sqrt(np.log(total_visits) / visits)
                ucb_scores[tool] = q_value + exploration_bonus
        
        # Select top tools by UCB score
        sorted_tools = sorted(ucb_scores.items(), key=lambda x: x[1], reverse=True)
        return [tool for tool, _ in sorted_tools[:top_n]]
    
    def _select_tools_thompson(self, state_key: str, top_n: int = 3) -> List[str]:
        """
        Select tools using Thompson Sampling.
        
        Args:
            state_key: State to select tools for
            top_n: Number of tools to select
            
        Returns:
            List of selected tool names
        """
        sampled_values = {}
        for tool in self.tool_names:
            alpha = self.alpha_params[state_key][tool]
            beta = self.beta_params[state_key][tool]
            # Sample from Beta distribution
            sampled_values[tool] = np.random.beta(alpha, beta)
        
        # Select top tools by sampled value
        sorted_tools = sorted(sampled_values.items(), key=lambda x: x[1], reverse=True)
        return [tool for tool, _ in sorted_tools[:top_n]]
    
    def _select_tools_epsilon_decay(self, state_key: str, top_n: int = 3, 
                                   exploration_min: int = 1, 
                                   exploration_max: int = 3) -> List[str]:
        """
        Select tools using epsilon-greedy with automatic decay.
        
        Args:
            state_key: State to select tools for
            top_n: Number of tools to select
            exploration_min: Min tools in exploration
            exploration_max: Max tools in exploration
            
        Returns:
            List of selected tool names
        """
        # Apply epsilon decay
        self.exploration_rate = max(
            self.min_exploration_rate,
            self.exploration_rate * self.epsilon_decay_rate
        )
        
        # Use standard epsilon-greedy with decayed rate
        if random.random() < self.exploration_rate:
            # Explore
            max_k = min(exploration_max, len(self.tool_names))
            min_k = min(exploration_min, max_k)
            k = random.randint(min_k, max_k) if max_k > 0 else 0
            if k > 0:
                return random.sample(self.tool_names, k=k)
        else:
            # Exploit
            sorted_actions = sorted(
                self.q_table[state_key].items(),
                key=lambda x: x[1],
                reverse=True
            )
            return [action for action, _ in sorted_actions[:top_n]]
        
        return []
    
    def select_tools(
        self,
        query: str,
        top_n: int = 3,
        exploration_min: int = 1,
        exploration_max: int = 3
    ) -> Tuple[List[str], str]:
        """
        Select tools for a query using Q-learning policy.
        
        Args:
            query: User query or task description
            top_n: Number of tools to select in exploitation mode
            exploration_min: Minimum tools to select in exploration mode
            exploration_max: Maximum tools to select in exploration mode
            
        Returns:
            Tuple of (selected tool names, effective state key used)
        """
        if not self.tool_names:
            logger.warning("No tools available for selection")
            return [], query
        
        # Cache embedding for this query
        self._cache_embedding(query)
        
        # Determine effective state key (exact match or similar)
        state_key = query
        is_new_state = query not in self.q_table
        
        if is_new_state and self.use_embeddings:
            similar_state = self._find_similar_state(query)
            if similar_state:
                state_key = similar_state
                is_new_state = False
                logger.info(f"Using similar state for Q-lookup")
        
        # Initialize Q-values for this state
        self.q_table.setdefault(state_key, defaultdict(float))
        for tool_name in self.tool_names:
            self.q_table[state_key].setdefault(tool_name, 0.0)
        
        # Update state access time and visit count
        self.state_visit_counts[state_key] += 1
        self.last_access_time[state_key] = time.time()
        
        # Check cache first
        cached_q_values = self._get_cached_q_values(state_key)
        if cached_q_values:
            self.q_table[state_key] = defaultdict(float, cached_q_values)
        
        selected_tools: List[str] = []
        
        # Select tools based on exploration strategy
        if self.exploration_strategy == ExplorationStrategy.UCB:
            logger.info("RL: Using UCB exploration")
            selected_tools = self._select_tools_ucb(state_key, top_n)
            
        elif self.exploration_strategy == ExplorationStrategy.THOMPSON_SAMPLING:
            logger.info("RL: Using Thompson Sampling")
            selected_tools = self._select_tools_thompson(state_key, top_n)
            
        elif self.exploration_strategy == ExplorationStrategy.EPSILON_DECAY:
            logger.info("RL: Using epsilon-decay exploration")
            selected_tools = self._select_tools_epsilon_decay(
                state_key, top_n, exploration_min, exploration_max
            )
            
        else:  # EPSILON_GREEDY (default)
            # Decide: explore or exploit
            effective_exploration_rate = self.exploration_rate
            if is_new_state:
                # Increase exploration for truly new states
                effective_exploration_rate = max(self.exploration_rate, 0.5)
                logger.info("Increased exploration for new state")
            
            if random.random() < effective_exploration_rate:
                # EXPLORE: random selection
                logger.info("RL: Exploring (random tool selection)")
                max_k = min(exploration_max, len(self.tool_names))
                min_k = min(exploration_min, max_k)
                k = random.randint(min_k, max_k) if max_k > 0 else 0
                if k > 0:
                    selected_tools = random.sample(self.tool_names, k=k)
            else:
                # EXPLOIT: select top Q-value tools
                logger.info("RL: Exploiting (selecting top Q-value tools)")
                sorted_actions = sorted(
                    self.q_table[state_key].items(),
                    key=lambda x: x[1],
                    reverse=True
                )
                selected_tools = [action for action, _ in sorted_actions[:top_n]]
        
        # Fallback to random if nothing selected
        if not selected_tools and self.tool_names:
            selected_tools = random.sample(self.tool_names, k=1)
            logger.warning("No tools selected, falling back to random")
        
        # Update cache
        self._update_cache(state_key, dict(self.q_table[state_key]))
        
        # Periodic maintenance
        if len(self.q_table) % 50 == 0:
            self._apply_q_value_decay()
            self._prune_q_table()
        
        logger.info(f"Selected tools: {selected_tools} for state: {state_key[:50]}...")
        
        return selected_tools, state_key
    
    def update(
        self,
        state_key: str,
        action: str,
        reward: float,
        next_state_key: Optional[str] = None
    ) -> None:
        """
        Update Q-values based on reward feedback.
        
        Args:
            state_key: State key where action was taken
            action: Tool name that was executed
            reward: Reward signal (typically -1 to +1)
            next_state_key: Optional next state for multi-step episodes
        """
        if action not in self.tool_names:
            logger.warning(f"Unknown action '{action}' - skipping update")
            return
        
        with self.update_lock:
            # Ensure state exists in Q-table
            if state_key not in self.q_table:
                self.q_table[state_key] = defaultdict(float)
                for tool in self.tool_names:
                    self.q_table[state_key][tool] = 0.0
                # Cache embedding for new state
                self._cache_embedding(state_key)
            
            # Update visit counts
            self.visit_counts[state_key][action] += 1
            
            # Update Thompson Sampling parameters
            if reward > 0:
                self.alpha_params[state_key][action] += reward
            else:
                self.beta_params[state_key][action] += abs(reward)
            
            # Apply negative reward multiplier
            effective_reward = reward
            if reward < 0:
                effective_reward = reward * self.negative_reward_multiplier
            
            # Q-learning update rule
            current_q = self.q_table[state_key][action]
            
            # Estimate max future value if next_state provided
            max_future_q = 0.0
            if next_state_key and next_state_key in self.q_table:
                max_future_q = max(self.q_table[next_state_key].values(), default=0.0)
            
            # Q(s,a) = Q(s,a) + α * [r + γ * max(Q(s',a')) - Q(s,a)]
            new_q = current_q + self.learning_rate * (
                effective_reward + self.discount_factor * max_future_q - current_q
            )
            
            self.q_table[state_key][action] = new_q
            
            # Update cache
            self._update_cache(state_key, dict(self.q_table[state_key]))
            
            # Track pending updates
            self.pending_updates.append((state_key, action, reward, next_state_key))
        
        logger.info(
            f"RL updated: Q({state_key[:30]}..., {action}) = {new_q:.4f} "
            f"(reward: {reward:.2f}, effective: {effective_reward:.2f})"
        )
        
        # Persist changes (async or sync)
        if self.enable_async_persistence:
            if len(self.pending_updates) >= self.batch_update_size:
                self._save_persisted_data()
                with self.update_lock:
                    self.pending_updates.clear()
        else:
            self._save_persisted_data()
    
    def update_batch(
        self,
        state_key: str,
        actions: List[str],
        reward: float
    ) -> None:
        """
        Update Q-values for multiple actions with the same reward.
        
        Useful when multiple tools were used and contributed to the outcome.
        
        Args:
            state_key: State key where actions were taken
            actions: List of tool names that were executed
            reward: Shared reward signal
        """
        for action in actions:
            self.update(state_key, action, reward)
    
    def anneal_exploration(
        self,
        decay_rate: float = 0.995,
        min_rate: float = 0.01
    ) -> None:
        """
        Gradually reduce exploration rate over time.
        
        Args:
            decay_rate: Multiplicative decay factor (< 1.0)
            min_rate: Minimum exploration rate
        """
        old_rate = self.exploration_rate
        self.exploration_rate = max(min_rate, self.exploration_rate * decay_rate)
        
        if old_rate != self.exploration_rate:
            logger.info(f"Exploration rate: {old_rate:.4f} → {self.exploration_rate:.4f}")
    
    def get_q_values(self, state_key: str) -> Dict[str, float]:
        """
        Get Q-values for all actions in a given state.
        
        Args:
            state_key: State to query
            
        Returns:
            Dictionary mapping action names to Q-values
        """
        if state_key in self.q_table:
            return dict(self.q_table[state_key])
        return {tool: 0.0 for tool in self.tool_names}
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get current RL statistics.
        
        Returns:
            Dictionary with statistics about the RL system
        """
        total_states = len(self.q_table)
        total_updates = sum(
            sum(1 for q in actions.values() if q != 0.0)
            for actions in self.q_table.values()
        )
        
        total_visits = sum(self.state_visit_counts.values())
        avg_visits_per_state = total_visits / total_states if total_states > 0 else 0
        
        return {
            "total_states": total_states,
            "total_tools": len(self.tool_names),
            "exploration_rate": self.exploration_rate,
            "initial_exploration_rate": self.initial_exploration_rate,
            "learning_rate": self.learning_rate,
            "use_embeddings": self.use_embeddings,
            "cached_embeddings": len(self.state_embeddings),
            "non_zero_q_values": total_updates,
            "q_table_path": str(self.q_table_path),
            "exploration_strategy": self.exploration_strategy.value,
            "total_state_visits": total_visits,
            "avg_visits_per_state": avg_visits_per_state,
            "cache_size": len(self.state_cache),
            "pending_updates": len(self.pending_updates),
            "async_persistence": self.enable_async_persistence,
            "q_table_pruning": self.enable_q_table_pruning,
            "q_value_decay": self.enable_q_value_decay
        }
    
    def export_readable(self, output_path: Optional[str] = None) -> str:
        """
        Export Q-table in human-readable format.
        
        Args:
            output_path: Optional path to write file
            
        Returns:
            Path to exported file
        """
        if output_path is None:
            output_path = str(self.q_table_path).replace('.pkl', '_readable.txt')
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("Azcore. - Q-Table Export\n")
                f.write("=" * 80 + "\n\n")
                
                f.write(f"Total States: {len(self.q_table)}\n")
                f.write(f"Total Tools: {len(self.tool_names)}\n")
                f.write(f"Exploration Rate: {self.exploration_rate:.4f}\n\n")
                
                sorted_states = sorted(self.q_table.keys())
                for state in sorted_states:
                    f.write("-" * 80 + "\n")
                    f.write(f"State: {state[:100]}...\n" if len(state) > 100 else f"State: {state}\n")
                    f.write("-" * 80 + "\n")
                    
                    actions = self.q_table[state]
                    sorted_actions = sorted(
                        actions.items(),
                        key=lambda x: x[1],
                        reverse=True
                    )
                    
                    for action, q_value in sorted_actions:
                        f.write(f"  {action:30} → {q_value:8.4f}\n")
                    f.write("\n")
            
            logger.info(f"Exported readable Q-table to {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Error exporting Q-table: {e}")
            raise
    
    def reset(self) -> None:
        """Reset Q-table and embeddings (for testing/debugging)."""
        with self.update_lock:
            self.q_table.clear()
            self.state_embeddings.clear()
            self.visit_counts.clear()
            self.state_visit_counts.clear()
            self.last_access_time.clear()
            self.state_cache.clear()
            self.pending_updates.clear()
            self.alpha_params.clear()
            self.beta_params.clear()
            self.exploration_rate = self.initial_exploration_rate
        logger.warning("Q-table and all associated data have been reset")
    
    def cleanup(self) -> None:
        """Clean up resources (call before destroying the manager)."""
        # Stop async persistence thread
        self._stop_async_persistence()
        
        # Save any pending updates
        if self.pending_updates:
            self._save_persisted_data()
            self.pending_updates.clear()
        
        logger.info("RLManager cleanup completed")
    
    def __del__(self):
        """Destructor to ensure cleanup."""
        try:
            self.cleanup()
        except:
            pass
    
    def set_exploration_strategy(self, strategy: ExplorationStrategy) -> None:
        """
        Change the exploration strategy at runtime.
        
        Args:
            strategy: New exploration strategy to use
        """
        old_strategy = self.exploration_strategy
        self.exploration_strategy = strategy
        logger.info(f"Changed exploration strategy: {old_strategy.value} → {strategy.value}")
    
    def get_top_performing_tools(self, top_n: int = 5) -> List[Tuple[str, float]]:
        """
        Get the top performing tools across all states.
        
        Args:
            top_n: Number of top tools to return
            
        Returns:
            List of (tool_name, avg_q_value) tuples
        """
        tool_q_values: DefaultDict[str, List[float]] = defaultdict(list)
        
        for state_actions in self.q_table.values():
            for tool, q_value in state_actions.items():
                tool_q_values[tool].append(q_value)
        
        avg_q_values = {
            tool: np.mean(values) for tool, values in tool_q_values.items()
        }
        
        sorted_tools = sorted(avg_q_values.items(), key=lambda x: x[1], reverse=True)
        return sorted_tools[:top_n]
    
    def get_state_quality(self, state_key: str) -> Dict[str, Any]:
        """
        Get quality metrics for a specific state.
        
        Args:
            state_key: State to analyze
            
        Returns:
            Dictionary with state quality metrics
        """
        if state_key not in self.q_table:
            return {
                "exists": False,
                "message": "State not found in Q-table"
            }
        
        q_values = dict(self.q_table[state_key])
        visits = dict(self.visit_counts[state_key])
        
        return {
            "exists": True,
            "q_values": q_values,
            "visits": visits,
            "total_visits": self.state_visit_counts.get(state_key, 0),
            "best_tool": max(q_values.items(), key=lambda x: x[1])[0] if q_values else None,
            "avg_q_value": np.mean(list(q_values.values())) if q_values else 0.0,
            "last_accessed": self.last_access_time.get(state_key),
            "in_cache": state_key in self.state_cache
        }
    
    def force_persist(self) -> None:
        """Force immediate persistence of Q-table."""
        self._save_persisted_data()
        with self.update_lock:
            self.pending_updates.clear()
        logger.info("Forced Q-table persistence")
    
    def update_batch_optimized(
        self,
        updates: List[Tuple[str, str, float, Optional[str]]]
    ) -> None:
        """
        Batch update Q-values for better performance.
        
        Args:
            updates: List of (state_key, action, reward, next_state_key) tuples
        """
        for state_key, action, reward, next_state_key in updates:
            self.update(state_key, action, reward, next_state_key)
        
        # Force persistence after batch
        if not self.enable_async_persistence:
            self._save_persisted_data()
    
    def __repr__(self) -> str:
        return (
            f"RLManager(tools={len(self.tool_names)}, "
            f"states={len(self.q_table)}, "
            f"exploration={self.exploration_rate:.3f}, "
            f"strategy={self.exploration_strategy.value})"
        )
