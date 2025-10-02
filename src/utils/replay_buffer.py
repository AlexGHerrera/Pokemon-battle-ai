"""
Replay Buffer for Experience Replay
====================================

Stores and samples experiences for RL training.
"""

import numpy as np
from collections import deque
from typing import Tuple, List
import random


class ReplayBuffer:
    """Experience replay buffer for DQN and similar algorithms."""
    
    def __init__(self, capacity: int = 100000):
        """
        Initialize replay buffer.
        
        Args:
            capacity: Maximum number of experiences to store
        """
        self.buffer = deque(maxlen=capacity)
        self.capacity = capacity
    
    def push(self, state, action, reward, next_state, done):
        """
        Add an experience to the buffer.
        
        Args:
            state: Current state
            action: Action taken
            reward: Reward received
            next_state: Next state
            done: Whether episode ended
        """
        self.buffer.append((state, action, reward, next_state, done))
    
    def sample(self, batch_size: int) -> Tuple:
        """
        Sample a batch of experiences.
        
        Args:
            batch_size: Number of experiences to sample
            
        Returns:
            Tuple of (states, actions, rewards, next_states, dones)
        """
        batch = random.sample(self.buffer, batch_size)
        
        states = np.array([exp[0] for exp in batch])
        actions = np.array([exp[1] for exp in batch])
        rewards = np.array([exp[2] for exp in batch])
        next_states = np.array([exp[3] for exp in batch])
        dones = np.array([exp[4] for exp in batch])
        
        return states, actions, rewards, next_states, dones
    
    def __len__(self) -> int:
        """Return current size of buffer."""
        return len(self.buffer)
    
    def clear(self):
        """Clear all experiences from buffer."""
        self.buffer.clear()
