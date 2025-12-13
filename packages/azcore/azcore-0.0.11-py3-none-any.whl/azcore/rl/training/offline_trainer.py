"""
Offline trainer for RL models using synthetic data.

This module trains RL models in an offline setting with batch updates.
"""

import logging
from typing import List, Dict, Any, Optional
from tqdm import tqdm

logger = logging.getLogger(__name__)


class OfflineTrainer:
    """
    Offline trainer for RL models.
    
    Example:
        >>> from azcore.rl.rl_manager import RLManager
        >>> rl_manager = RLManager(tool_names=["search", "calculator"])
        >>> trainer = OfflineTrainer(rl_manager)
        >>> trainer.train(training_data, epochs=10)
    """
    
    def __init__(
        self,
        rl_manager,
        batch_size: int = 32,
        verbose: bool = True
    ):
        """
        Initialize offline trainer.
        
        Args:
            rl_manager: RLManager instance to train
            batch_size: Batch size for training
            verbose: Whether to show progress bars
        """
        self.rl_manager = rl_manager
        self.batch_size = batch_size
        self.verbose = verbose
        
        # Training metrics
        self.training_history = {
            'epoch_rewards': [],
            'epoch_losses': [],
            'q_value_stats': []
        }
        
        logger.info(f"OfflineTrainer initialized (batch_size={batch_size})")
    
    def train(
        self,
        training_data: List[Dict[str, Any]],
        epochs: int = 10,
        shuffle: bool = True
    ) -> Dict[str, Any]:
        """
        Train RL model on synthetic data.
        
        Args:
            training_data: List of training samples
            epochs: Number of training epochs
            shuffle: Whether to shuffle data each epoch
            
        Returns:
            Training statistics
        """
        logger.info(f"Starting offline training: {len(training_data)} samples, {epochs} epochs")
        
        for epoch in range(epochs):
            epoch_rewards = []
            
            # Shuffle data if requested
            if shuffle:
                import random
                random.shuffle(training_data)
            
            # Process in batches
            progress_bar = tqdm(
                range(0, len(training_data), self.batch_size),
                desc=f"Epoch {epoch+1}/{epochs}",
                disable=not self.verbose
            )
            
            for batch_start in progress_bar:
                batch_end = min(batch_start + self.batch_size, len(training_data))
                batch = training_data[batch_start:batch_end]
                
                # Process batch
                batch_rewards = self._process_batch(batch)
                epoch_rewards.extend(batch_rewards)
                
                # Update progress bar
                if self.verbose:
                    avg_reward = sum(batch_rewards) / len(batch_rewards) if batch_rewards else 0
                    progress_bar.set_postfix({'avg_reward': f'{avg_reward:.3f}'})
            
            # Epoch statistics
            avg_epoch_reward = sum(epoch_rewards) / len(epoch_rewards) if epoch_rewards else 0
            self.training_history['epoch_rewards'].append(avg_epoch_reward)
            
            # Get Q-value statistics
            q_stats = self._get_q_value_stats()
            self.training_history['q_value_stats'].append(q_stats)
            
            logger.info(
                f"Epoch {epoch+1}/{epochs}: "
                f"avg_reward={avg_epoch_reward:.3f}, "
                f"avg_q_value={q_stats['avg_q_value']:.3f}"
            )
            
            # Save checkpoint periodically
            if (epoch + 1) % 5 == 0:
                self.rl_manager.force_persist()
                logger.info(f"Checkpoint saved at epoch {epoch+1}")
        
        # Final save
        self.rl_manager.force_persist()
        
        stats = {
            'epochs': epochs,
            'total_samples': len(training_data),
            'final_avg_reward': self.training_history['epoch_rewards'][-1],
            'training_history': self.training_history
        }
        
        logger.info(f"Training completed: final_avg_reward={stats['final_avg_reward']:.3f}")
        return stats
    
    def _process_batch(self, batch: List[Dict[str, Any]]) -> List[float]:
        """Process a batch of training samples."""
        batch_rewards = []
        
        for sample in batch:
            state_key = sample['state_key']
            selected_tools = sample['selected_tools']
            reward = sample['reward']
            
            # Update Q-values for each selected tool
            for tool in selected_tools:
                self.rl_manager.update(
                    state_key=state_key,
                    action=tool,
                    reward=reward
                )
            
            batch_rewards.append(reward)
        
        return batch_rewards
    
    def _get_q_value_stats(self) -> Dict[str, float]:
        """Get statistics about Q-values."""
        all_q_values = []
        
        for state_actions in self.rl_manager.q_table.values():
            all_q_values.extend(state_actions.values())
        
        if not all_q_values:
            return {
                'avg_q_value': 0.0,
                'min_q_value': 0.0,
                'max_q_value': 0.0,
                'non_zero_count': 0
            }
        
        non_zero = [q for q in all_q_values if q != 0.0]
        
        return {
            'avg_q_value': sum(all_q_values) / len(all_q_values),
            'min_q_value': min(all_q_values),
            'max_q_value': max(all_q_values),
            'non_zero_count': len(non_zero)
        }
    
    def evaluate(
        self,
        validation_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Evaluate model on validation data.
        
        Args:
            validation_data: List of validation samples
            
        Returns:
            Evaluation metrics
        """
        logger.info(f"Evaluating on {len(validation_data)} samples")
        
        # Handle empty validation data
        if not validation_data:
            logger.warning("Empty validation data provided")
            return {
                'avg_reward': 0.0,
                'top1_accuracy': 0.0,
                'top3_accuracy': 0.0,
                'total_samples': 0
            }
        
        total_reward = 0.0
        correct_top1 = 0
        correct_top3 = 0
        
        for sample in validation_data:
            query = sample['query']
            optimal_tools = sample['scenario'].optimal_tools
            
            # Get model predictions
            selected_tools, _ = self.rl_manager.select_tools(
                query=query,
                top_n=3
            )
            
            # Check accuracy
            if selected_tools and optimal_tools:
                if selected_tools[0] in optimal_tools:
                    correct_top1 += 1
                if any(tool in optimal_tools for tool in selected_tools[:3]):
                    correct_top3 += 1
            
            # Accumulate reward
            total_reward += sample['reward']
        
        metrics = {
            'avg_reward': total_reward / len(validation_data),
            'top1_accuracy': correct_top1 / len(validation_data),
            'top3_accuracy': correct_top3 / len(validation_data),
            'total_samples': len(validation_data)
        }
        
        logger.info(
            f"Evaluation results: "
            f"avg_reward={metrics['avg_reward']:.3f}, "
            f"top1_acc={metrics['top1_accuracy']:.2%}, "
            f"top3_acc={metrics['top3_accuracy']:.2%}"
        )
        
        return metrics
    
    def get_training_history(self) -> Dict[str, Any]:
        """Get training history."""
        return self.training_history.copy()
