"""
Data Processing Pipeline
=======================

Core data processing functions for Pokemon battle data.
"""

import json
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class BattleDataProcessor:
    """Main class for processing Pokemon battle data."""
    
    def __init__(self, data_path: str):
        self.data_path = Path(data_path)
        self.battles_cache = {}
    
    def load_battles_optimized(self, use_sample: bool = True, sample_size: int = 2000) -> List[Dict]:
        """Load battles with performance optimizations."""
        if use_sample:
            return self.create_sample_dataset(sample_size)
        
        # Try loading from parquet first
        parquet_path = self.data_path / "battles_processed.parquet"
        if parquet_path.exists():
            df = pd.read_parquet(parquet_path)
            return df.to_dict('records')
        
        # Fallback to JSON
        json_path = self.data_path / "all_battles.json"
        if json_path.exists():
            with open(json_path, 'r') as f:
                battles = json.load(f)
            logger.info(f"Loaded {len(battles)} battles from JSON")
            return battles
        
        raise FileNotFoundError("No battle data found")
    
    def create_sample_dataset(self, sample_size: int = 2000) -> List[Dict]:
        """Create a sample dataset for development."""
        sample_path = self.data_path / f"battles_sample_{sample_size}.json"
        
        if sample_path.exists():
            with open(sample_path, 'r') as f:
                return json.load(f)
        
        # Create sample from full dataset
        battles = self.load_battles_optimized(use_sample=False)
        sample = np.random.choice(battles, min(sample_size, len(battles)), replace=False).tolist()
        
        # Save sample
        with open(sample_path, 'w') as f:
            json.dump(sample, f)
        
        logger.info(f"Created sample dataset with {len(sample)} battles")
        return sample
    
    def extract_features(self, battles: List[Dict]) -> pd.DataFrame:
        """Extract features for ML training."""
        features = []
        
        for battle in battles:
            try:
                feature_dict = self._extract_battle_features(battle)
                features.append(feature_dict)
            except Exception as e:
                logger.warning(f"Failed to extract features from battle: {e}")
                continue
        
        return pd.DataFrame(features)
    
    def _extract_battle_features(self, battle: Dict) -> Dict:
        """Extract features from a single battle."""
        events = battle.get('events', [])
        
        # Basic metrics
        total_events = len(events)
        total_turns = battle.get('turns', 0)
        
        # Event type counts
        move_events = sum(1 for e in events if e.get('type') == 'move')
        switch_events = sum(1 for e in events if e.get('type') == 'switch')
        damage_events = sum(1 for e in events if 'damage' in str(e))
        
        # Player information
        p1_rating = battle.get('p1', {}).get('rating', 1000)
        p2_rating = battle.get('p2', {}).get('rating', 1000)
        winner = battle.get('winner', 'unknown')
        
        return {
            'total_events': total_events,
            'total_turns': total_turns,
            'move_events': move_events,
            'switch_events': switch_events,
            'damage_events': damage_events,
            'events_per_turn': total_events / max(total_turns, 1),
            'p1_rating': p1_rating,
            'p2_rating': p2_rating,
            'rating_diff': abs(p1_rating - p2_rating),
            'winner': winner,
            'p1_won': 1 if winner == 'p1' else 0
        }
    
    def convert_to_parquet(self) -> None:
        """Convert JSON data to Parquet for faster loading."""
        battles = self.load_battles_optimized(use_sample=False)
        df = pd.DataFrame(battles)
        
        parquet_path = self.data_path / "battles_processed.parquet"
        df.to_parquet(parquet_path, compression='snappy')
        
        logger.info(f"Converted {len(battles)} battles to Parquet format")
