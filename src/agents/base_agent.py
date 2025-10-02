"""
Base Agent Class
================

Abstract base class for all RL agents.
"""

from abc import ABC, abstractmethod
import numpy as np
from typing import Any, Dict


class BaseAgent(ABC):
    """Abstract base class for RL agents."""
    
    def __init__(self, state_size: int, action_size: int, config: Dict[str, Any]):
        """
        Initialize base agent.
        
        Args:
            state_size: Dimension of state space
            action_size: Number of possible actions
            config: Configuration dictionary
        """
        self.state_size = state_size
        self.action_size = action_size
        self.config = config
    
    @abstractmethod
    def select_action(self, state: np.ndarray, training: bool = True) -> int:
        """
        Select an action given a state.
        
        Args:
            state: Current state
            training: Whether in training mode (affects exploration)
            
        Returns:
            Selected action index
        """
        pass
    
    @abstractmethod
    def train_step(self, batch) -> Dict[str, float]:
        """
        Perform one training step.
        
        Args:
            batch: Batch of experiences
            
        Returns:
            Dictionary of training metrics
        """
        pass
    
    @abstractmethod
    def save(self, path: str):
        """
        Save agent to disk.
        
        Args:
            path: Path to save agent
        """
        pass
    
    @abstractmethod
    def load(self, path: str):
        """
        Load agent from disk.
        
        Args:
            path: Path to load agent from
        """
        pass
