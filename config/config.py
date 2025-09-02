"""
Configuración del Sistema Pokemon Battle AI
==========================================

Configuraciones centralizadas para todo el sistema.
"""

import os
from pathlib import Path
from typing import Dict, Any

# Rutas del proyecto
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
MODELS_DIR = PROJECT_ROOT / "src" / "models" / "pretrained"
LOGS_DIR = PROJECT_ROOT / "logs"
ASSETS_DIR = PROJECT_ROOT / "assets"

# Configuración de datos
DATA_CONFIG = {
    "battles_json_path": DATA_DIR / "all_battles.json",
    "battles_parquet_path": DATA_DIR / "battles_processed.parquet",
    "sample_size_dev": 2000,
    "sample_size_prod": 10000,
    "train_test_split": 0.8,
    "continuous_learning_dir": DATA_DIR / "continuous_learning"
}

# Configuración del modelo
MODEL_CONFIG = {
    "input_size": 512,
    "hidden_sizes": [256, 128, 64],
    "num_actions": 10,
    "dropout_rate": 0.2,
    "learning_rate": 0.001,
    "batch_size": 32,
    "num_epochs": 100,
    "device": "cuda" if os.getenv("USE_GPU", "false").lower() == "true" else "cpu"
}

# Configuración del servidor web
WEB_CONFIG = {
    "host": "0.0.0.0",
    "port": 5000,
    "debug": os.getenv("DEBUG", "false").lower() == "true",
    "cors_origins": ["http://localhost:3000", "http://127.0.0.1:3000"],
    "max_sessions": 100,
    "session_timeout": 3600  # 1 hora en segundos
}

# Configuración de logging
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        }
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler"
        },
        "file": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.FileHandler",
            "filename": LOGS_DIR / "pokemon_ai.log",
            "mode": "a"
        }
    },
    "loggers": {
        "": {
            "handlers": ["default", "file"],
            "level": "INFO",
            "propagate": False
        }
    }
}

# Configuración de Pokemon (simplificada)
POKEMON_CONFIG = {
    "max_team_size": 6,
    "max_hp": 100,
    "moves_per_pokemon": 4,
    "available_moves": [
        {"name": "thunderbolt", "type": "electric", "power": 90, "accuracy": 100},
        {"name": "quick-attack", "type": "normal", "power": 40, "accuracy": 100},
        {"name": "iron-tail", "type": "steel", "power": 100, "accuracy": 75},
        {"name": "agility", "type": "psychic", "power": 0, "accuracy": 100},
        {"name": "tackle", "type": "normal", "power": 35, "accuracy": 100},
        {"name": "water-gun", "type": "water", "power": 40, "accuracy": 100},
        {"name": "ember", "type": "fire", "power": 40, "accuracy": 100},
        {"name": "vine-whip", "type": "grass", "power": 45, "accuracy": 100}
    ]
}

# Configuración de aprendizaje continuo
CONTINUOUS_LEARNING_CONFIG = {
    "enabled": True,
    "retrain_threshold": 50,  # Número de nuevas batallas antes de reentrenar
    "backup_models": True,
    "learning_rate_decay": 0.95,
    "min_learning_rate": 0.0001
}


def get_config(section: str = None) -> Dict[str, Any]:
    """
    Obtiene la configuración completa o de una sección específica.
    
    Args:
        section: Nombre de la sección (opcional)
        
    Returns:
        Diccionario con la configuración
    """
    all_config = {
        "data": DATA_CONFIG,
        "model": MODEL_CONFIG,
        "web": WEB_CONFIG,
        "logging": LOGGING_CONFIG,
        "pokemon": POKEMON_CONFIG,
        "continuous_learning": CONTINUOUS_LEARNING_CONFIG,
        "paths": {
            "project_root": PROJECT_ROOT,
            "data_dir": DATA_DIR,
            "models_dir": MODELS_DIR,
            "logs_dir": LOGS_DIR,
            "assets_dir": ASSETS_DIR
        }
    }
    
    if section:
        return all_config.get(section, {})
    
    return all_config


def create_directories():
    """Crea los directorios necesarios si no existen."""
    directories = [
        DATA_DIR,
        MODELS_DIR,
        LOGS_DIR,
        ASSETS_DIR,
        DATA_CONFIG["continuous_learning_dir"]
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    # Crear directorios al ejecutar el script
    create_directories()
    print("Directorios creados exitosamente")
    
    # Mostrar configuración
    import json
    config = get_config()
    print(json.dumps(config, indent=2, default=str))
