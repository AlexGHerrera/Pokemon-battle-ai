"""
Random Agent
============

Simple random agent for baseline evaluation.
"""

import numpy as np
from typing import Dict, Any
from .base_agent import BaseAgent


class RandomAgent(BaseAgent):
    """Agent that selects actions randomly."""
    
    def __init__(self, state_size: int, action_size: int, config: Dict[str, Any] = None):
        """
        Initialize random agent.
        
        Args:
            state_size: Dimension of state space
            action_size: Number of possible actions
            config: Configuration dictionary (unused)
        """
        super().__init__(state_size, action_size, config or {})
    
    def select_action(self, state: np.ndarray, training: bool = True) -> int:
        """
        Select a random action.
        
        Args:
            state: Current state (unused)
            training: Whether in training mode (unused)
            
        Returns:
            Random action index
        """
        return np.random.randint(0, self.action_size)
    
    def train_step(self, batch) -> Dict[str, float]:
        """
        Random agent doesn't train.
        
        Args:
            batch: Batch of experiences (unused)
            
        Returns:
            Empty metrics dictionary
        """
        return {}
    
    def save(self, path: str):
        """Random agent has no parameters to save."""
        pass
    
    def load(self, path: str):
        """Random agent has no parameters to load."""
        pass
