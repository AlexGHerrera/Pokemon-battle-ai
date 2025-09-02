"""
Sistema de Entrenamiento de IA Pokemon
=====================================

Entrenador principal para modelos de batalla Pokemon.
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging
from pathlib import Path
import json
from datetime import datetime

from ..models.architectures import PokemonBattleNet, RecurrentBattleNet
from ..data.processors import BattleDataProcessor

logger = logging.getLogger(__name__)


class BattleDataset(Dataset):
    """Dataset personalizado para datos de batalla Pokemon."""
    
    def __init__(self, features: np.ndarray, labels: np.ndarray):
        """
        Inicializa el dataset.
        
        Args:
            features: Características de entrada (estados del juego)
            labels: Etiquetas objetivo (acciones tomadas)
        """
        self.features = torch.FloatTensor(features)
        self.labels = torch.LongTensor(labels)
    
    def __len__(self) -> int:
        return len(self.features)
    
    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor]:
        return self.features[idx], self.labels[idx]


class PokemonTrainer:
    """Entrenador principal para modelos de IA Pokemon."""
    
    def __init__(self, 
                 model: nn.Module,
                 device: str = 'cuda' if torch.cuda.is_available() else 'cpu',
                 learning_rate: float = 0.001,
                 batch_size: int = 32):
        """
        Inicializa el entrenador.
        
        Args:
            model: Modelo de red neuronal a entrenar
            device: Dispositivo de cómputo (cuda/cpu)
            learning_rate: Tasa de aprendizaje
            batch_size: Tamaño del lote
        """
        self.model = model.to(device)
        self.device = device
        self.batch_size = batch_size
        
        # Optimizador y función de pérdida
        self.optimizer = optim.Adam(model.parameters(), lr=learning_rate)
        self.criterion = nn.CrossEntropyLoss()
        
        # Métricas de entrenamiento
        self.train_losses = []
        self.val_losses = []
        self.train_accuracies = []
        self.val_accuracies = []
        
    def prepare_data(self, battles: List[Dict]) -> Tuple[DataLoader, DataLoader]:
        """
        Prepara los datos para entrenamiento.
        
        Args:
            battles: Lista de batallas procesadas
            
        Returns:
            DataLoaders de entrenamiento y validación
        """
        # Extraer características y etiquetas
        features, labels = self._extract_training_data(battles)
        
        # División entrenamiento/validación
        split_idx = int(0.8 * len(features))
        
        train_features = features[:split_idx]
        train_labels = labels[:split_idx]
        val_features = features[split_idx:]
        val_labels = labels[split_idx:]
        
        # Crear datasets
        train_dataset = BattleDataset(train_features, train_labels)
        val_dataset = BattleDataset(val_features, val_labels)
        
        # Crear DataLoaders
        train_loader = DataLoader(
            train_dataset, 
            batch_size=self.batch_size, 
            shuffle=True
        )
        val_loader = DataLoader(
            val_dataset, 
            batch_size=self.batch_size, 
            shuffle=False
        )
        
        logger.info(f"Datos preparados: {len(train_dataset)} entrenamiento, {len(val_dataset)} validación")
        
        return train_loader, val_loader
    
    def train_epoch(self, train_loader: DataLoader) -> Tuple[float, float]:
        """
        Entrena una época.
        
        Args:
            train_loader: DataLoader de entrenamiento
            
        Returns:
            Pérdida y precisión promedio de la época
        """
        self.model.train()
        total_loss = 0.0
        correct_predictions = 0
        total_samples = 0
        
        for batch_features, batch_labels in train_loader:
            # Mover datos al dispositivo
            batch_features = batch_features.to(self.device)
            batch_labels = batch_labels.to(self.device)
            
            # Reiniciar gradientes
            self.optimizer.zero_grad()
            
            # Propagación hacia adelante
            outputs = self.model(batch_features)
            loss = self.criterion(outputs, batch_labels)
            
            # Propagación hacia atrás
            loss.backward()
            self.optimizer.step()
            
            # Métricas
            total_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            correct_predictions += (predicted == batch_labels).sum().item()
            total_samples += batch_labels.size(0)
        
        avg_loss = total_loss / len(train_loader)
        accuracy = correct_predictions / total_samples
        
        return avg_loss, accuracy
    
    def validate_epoch(self, val_loader: DataLoader) -> Tuple[float, float]:
        """
        Valida una época.
        
        Args:
            val_loader: DataLoader de validación
            
        Returns:
            Pérdida y precisión promedio de validación
        """
        self.model.eval()
        total_loss = 0.0
        correct_predictions = 0
        total_samples = 0
        
        with torch.no_grad():
            for batch_features, batch_labels in val_loader:
                # Mover datos al dispositivo
                batch_features = batch_features.to(self.device)
                batch_labels = batch_labels.to(self.device)
                
                # Propagación hacia adelante
                outputs = self.model(batch_features)
                loss = self.criterion(outputs, batch_labels)
                
                # Métricas
                total_loss += loss.item()
                _, predicted = torch.max(outputs.data, 1)
                correct_predictions += (predicted == batch_labels).sum().item()
                total_samples += batch_labels.size(0)
        
        avg_loss = total_loss / len(val_loader)
        accuracy = correct_predictions / total_samples
        
        return avg_loss, accuracy
    
    def train(self, 
              train_loader: DataLoader, 
              val_loader: DataLoader,
              num_epochs: int = 100,
              save_path: Optional[str] = None) -> Dict:
        """
        Entrena el modelo completo.
        
        Args:
            train_loader: DataLoader de entrenamiento
            val_loader: DataLoader de validación
            num_epochs: Número de épocas
            save_path: Ruta para guardar el modelo
            
        Returns:
            Historial de entrenamiento
        """
        logger.info(f"Iniciando entrenamiento por {num_epochs} épocas")
        
        best_val_accuracy = 0.0
        
        for epoch in range(num_epochs):
            # Entrenar época
            train_loss, train_acc = self.train_epoch(train_loader)
            val_loss, val_acc = self.validate_epoch(val_loader)
            
            # Guardar métricas
            self.train_losses.append(train_loss)
            self.val_losses.append(val_loss)
            self.train_accuracies.append(train_acc)
            self.val_accuracies.append(val_acc)
            
            # Logging
            if epoch % 10 == 0:
                logger.info(f"Época {epoch}: Train Loss={train_loss:.4f}, Train Acc={train_acc:.4f}, "
                           f"Val Loss={val_loss:.4f}, Val Acc={val_acc:.4f}")
            
            # Guardar mejor modelo
            if val_acc > best_val_accuracy and save_path:
                best_val_accuracy = val_acc
                self.save_model(save_path)
                logger.info(f"Nuevo mejor modelo guardado con precisión: {val_acc:.4f}")
        
        logger.info("Entrenamiento completado")
        
        return {
            'train_losses': self.train_losses,
            'val_losses': self.val_losses,
            'train_accuracies': self.train_accuracies,
            'val_accuracies': self.val_accuracies,
            'best_val_accuracy': best_val_accuracy
        }
    
    def save_model(self, path: str) -> None:
        """Guarda el modelo entrenado."""
        torch.save({
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'train_losses': self.train_losses,
            'val_losses': self.val_losses,
            'timestamp': datetime.now().isoformat()
        }, path)
    
    def load_model(self, path: str) -> None:
        """Carga un modelo previamente entrenado."""
        checkpoint = torch.load(path, map_location=self.device)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        
        if 'train_losses' in checkpoint:
            self.train_losses = checkpoint['train_losses']
            self.val_losses = checkpoint['val_losses']
    
    def _extract_training_data(self, battles: List[Dict]) -> Tuple[np.ndarray, np.ndarray]:
        """
        Extrae características y etiquetas para entrenamiento.
        
        Args:
            battles: Lista de batallas
            
        Returns:
            Características y etiquetas como arrays numpy
        """
        # Placeholder - implementar extracción real de características
        # Esto debería convertir el estado del juego en vectores numéricos
        # y las acciones en etiquetas categóricas
        
        features = []
        labels = []
        
        for battle in battles:
            # Extraer estado del juego como vector de características
            game_state = self._battle_to_features(battle)
            # Extraer acción tomada como etiqueta
            action_label = self._battle_to_action(battle)
            
            if game_state is not None and action_label is not None:
                features.append(game_state)
                labels.append(action_label)
        
        return np.array(features), np.array(labels)
    
    def _battle_to_features(self, battle: Dict) -> Optional[np.ndarray]:
        """Convierte una batalla en vector de características."""
        # Implementación simplificada - expandir según necesidades
        try:
            events = battle.get('events', [])
            features = [
                len(events),  # Número total de eventos
                battle.get('turns', 0),  # Número de turnos
                # Agregar más características según el estado del juego
            ]
            
            # Padding para tamaño fijo
            while len(features) < 512:  # Tamaño de entrada del modelo
                features.append(0.0)
            
            return np.array(features[:512])
        except:
            return None
    
    def _battle_to_action(self, battle: Dict) -> Optional[int]:
        """Extrae la acción tomada de una batalla."""
        # Implementación simplificada - expandir según necesidades
        try:
            # Placeholder: usar ganador como etiqueta simple
            winner = battle.get('winner', 'unknown')
            if winner == 'p1':
                return 1
            elif winner == 'p2':
                return 0
            else:
                return None
        except:
            return None
