"""
Arquitecturas de Modelos de IA
=============================

Definiciones de redes neuronales para el AI de batallas Pokemon.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Dict, List, Tuple, Optional
import numpy as np


class PokemonBattleNet(nn.Module):
    """Red neuronal principal para decisiones de batalla Pokemon."""
    
    def __init__(self, 
                 input_size: int = 512,
                 hidden_sizes: List[int] = [256, 128, 64],
                 num_actions: int = 10,
                 dropout_rate: float = 0.2):
        """
        Inicializa la red neuronal.
        
        Args:
            input_size: Tamaño de entrada (features del estado del juego)
            hidden_sizes: Lista de tamaños de capas ocultas
            num_actions: Número de acciones posibles (movimientos + switches)
            dropout_rate: Tasa de dropout para regularización
        """
        super(PokemonBattleNet, self).__init__()
        
        self.input_size = input_size
        self.num_actions = num_actions
        
        # Capas de la red
        layers = []
        prev_size = input_size
        
        for hidden_size in hidden_sizes:
            layers.extend([
                nn.Linear(prev_size, hidden_size),
                nn.ReLU(),
                nn.Dropout(dropout_rate)
            ])
            prev_size = hidden_size
        
        # Capa de salida
        layers.append(nn.Linear(prev_size, num_actions))
        
        self.network = nn.Sequential(*layers)
        
        # Inicialización de pesos
        self._initialize_weights()
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Propagación hacia adelante.
        
        Args:
            x: Tensor de entrada con el estado del juego
            
        Returns:
            Probabilidades de acción
        """
        logits = self.network(x)
        return F.softmax(logits, dim=-1)
    
    def _initialize_weights(self):
        """Inicializa los pesos de la red."""
        for module in self.modules():
            if isinstance(module, nn.Linear):
                nn.init.xavier_uniform_(module.weight)
                nn.init.zeros_(module.bias)


class RecurrentBattleNet(nn.Module):
    """Red neuronal recurrente para capturar secuencias de batalla."""
    
    def __init__(self,
                 input_size: int = 512,
                 hidden_size: int = 128,
                 num_layers: int = 2,
                 num_actions: int = 10,
                 dropout_rate: float = 0.2):
        """
        Inicializa la red recurrente.
        
        Args:
            input_size: Tamaño de entrada por turno
            hidden_size: Tamaño del estado oculto LSTM
            num_layers: Número de capas LSTM
            num_actions: Número de acciones posibles
            dropout_rate: Tasa de dropout
        """
        super(RecurrentBattleNet, self).__init__()
        
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        
        # Capas LSTM
        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            dropout=dropout_rate if num_layers > 1 else 0,
            batch_first=True
        )
        
        # Capas de salida
        self.fc = nn.Sequential(
            nn.Linear(hidden_size, hidden_size // 2),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            nn.Linear(hidden_size // 2, num_actions)
        )
    
    def forward(self, x: torch.Tensor, hidden: Optional[Tuple] = None) -> Tuple[torch.Tensor, Tuple]:
        """
        Propagación hacia adelante con memoria de secuencia.
        
        Args:
            x: Secuencia de estados del juego [batch, seq_len, features]
            hidden: Estado oculto previo (opcional)
            
        Returns:
            Probabilidades de acción y nuevo estado oculto
        """
        # LSTM forward pass
        lstm_out, hidden = self.lstm(x, hidden)
        
        # Usar solo la última salida de la secuencia
        last_output = lstm_out[:, -1, :]
        
        # Capas fully connected
        logits = self.fc(last_output)
        probabilities = F.softmax(logits, dim=-1)
        
        return probabilities, hidden
    
    def init_hidden(self, batch_size: int, device: torch.device) -> Tuple:
        """Inicializa el estado oculto."""
        h0 = torch.zeros(self.num_layers, batch_size, self.hidden_size, device=device)
        c0 = torch.zeros(self.num_layers, batch_size, self.hidden_size, device=device)
        return (h0, c0)


class AttentionBattleNet(nn.Module):
    """Red con mecanismo de atención para enfocarse en aspectos críticos."""
    
    def __init__(self,
                 input_size: int = 512,
                 attention_dim: int = 64,
                 hidden_size: int = 256,
                 num_actions: int = 10):
        """
        Inicializa la red con atención.
        
        Args:
            input_size: Tamaño de entrada
            attention_dim: Dimensión del mecanismo de atención
            hidden_size: Tamaño de capas ocultas
            num_actions: Número de acciones posibles
        """
        super(AttentionBattleNet, self).__init__()
        
        # Capas de atención
        self.attention = nn.MultiheadAttention(
            embed_dim=input_size,
            num_heads=8,
            dropout=0.1,
            batch_first=True
        )
        
        # Red principal
        self.network = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_size, hidden_size // 2),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_size // 2, num_actions)
        )
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Propagación con mecanismo de atención.
        
        Args:
            x: Estado del juego
            
        Returns:
            Probabilidades de acción
        """
        # Aplicar atención (self-attention)
        attended, _ = self.attention(x, x, x)
        
        # Combinar con entrada original
        combined = x + attended
        
        # Red principal
        logits = self.network(combined)
        return F.softmax(logits, dim=-1)


class EnsembleBattleNet(nn.Module):
    """Ensemble de múltiples modelos para mayor robustez."""
    
    def __init__(self, models: List[nn.Module], weights: Optional[List[float]] = None):
        """
        Inicializa el ensemble.
        
        Args:
            models: Lista de modelos a combinar
            weights: Pesos para cada modelo (opcional)
        """
        super(EnsembleBattleNet, self).__init__()
        
        self.models = nn.ModuleList(models)
        
        if weights is None:
            weights = [1.0 / len(models)] * len(models)
        
        self.register_buffer('weights', torch.tensor(weights))
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Propagación del ensemble.
        
        Args:
            x: Estado del juego
            
        Returns:
            Probabilidades promedio ponderado
        """
        outputs = []
        
        for model in self.models:
            output = model(x)
            outputs.append(output)
        
        # Promedio ponderado
        weighted_sum = torch.zeros_like(outputs[0])
        for output, weight in zip(outputs, self.weights):
            weighted_sum += weight * output
        
        return weighted_sum
