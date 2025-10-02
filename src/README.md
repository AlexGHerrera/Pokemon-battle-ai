# Source Code Structure

## Módulos

### `agents/` - Agentes de Reinforcement Learning
- `base_agent.py` - Clase base abstracta para todos los agentes
- `dqn_agent.py` - Deep Q-Network agent (Fase 3)
- `ppo_agent.py` - Proximal Policy Optimization agent (Fase 4)
- `random_agent.py` - ✅ Agente random para baseline

### `data/` - Procesamiento de Datos
- `feature_extractor.py` - ✅ Extracción de features para ML (Fase 1)
- `battle_parser.py` - Parser de batallas JSON (Fase 2)
- `state_builder.py` - Construcción de estados para RL (Fase 2)
- `pokemon_data.py` - Base de datos Pokemon (tipos, BST)

### `environment/` - Entorno de Batalla
- `battle_env.py` - Gym environment principal (Fase 3)
- `battle_state.py` - Representación de estado (Fase 3)
- `action_space.py` - Definición de acciones (Fase 3)
- `showdown_client.py` - Cliente Pokemon Showdown (Fase 4)

### `models/` - Redes Neuronales
- `networks.py` - ✅ Arquitecturas de redes neuronales
- `baseline_models.py` - Modelos ML clásicos (Fase 1)

### `training/` - Sistemas de Entrenamiento
- `rl_trainer.py` - Entrenador para agentes RL (Fase 3)
- `self_play.py` - Sistema de self-play (Fase 3)
- `evaluator.py` - Evaluación de agentes (Fase 3)
- `ml_trainer.py` - Entrenador ML clásico (Fase 1)

### `utils/` - Utilidades
- `replay_buffer.py` - ✅ Buffer de experiencias para RL
- `logger.py` - Logging personalizado
- `metrics.py` - Métricas de evaluación
- `visualization.py` - Visualización de entrenamiento

## Estado Actual

✅ = Implementado
🔄 = En progreso
⏸️ = Pendiente

**Fase 1 (Completada):**
- ✅ `data/feature_extractor.py`
- ✅ `models/networks.py`
- ✅ `utils/replay_buffer.py`
- ✅ `agents/base_agent.py`
- ✅ `agents/random_agent.py`

**Fase 2 (Próxima):**
- ⏸️ `data/battle_parser.py`
- ⏸️ `data/state_builder.py`

**Fase 3+ (Futuro):**
- ⏸️ `agents/dqn_agent.py`
- ⏸️ `environment/battle_env.py`
- ⏸️ `training/rl_trainer.py`
- ⏸️ `training/self_play.py`
