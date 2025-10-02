"""
Data Processing Module
=====================

Handles all data-related operations for Pokemon battle analysis.

Components:
- battle_parser: Parse battle JSON files
- feature_extractor: Extract features for ML models (Fase 1)
- state_builder: Build states for RL agents (Fase 2+)
- pokemon_data: Pokemon database (types, BST, etc.)
"""

__all__ = ['BattleParser', 'FeatureExtractor', 'StateBuilder']
