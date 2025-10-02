# 🔥 Pokemon Battle AI - El Camino hacia el Maestro Definitivo

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-1.12%2B-red.svg)](https://pytorch.org/)
[![Reinforcement Learning](https://img.shields.io/badge/RL-DQN%20%7C%20PPO-red.svg)](https://pytorch.org/)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3%2B-orange.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Phase%201%20Complete-green.svg)](notebooks/)
[![Vision](https://img.shields.io/badge/Vision-RL%20Agent-purple.svg)](README.md)

![Pokemon Battle Analysis](assets/images/battle_patterns_analysis.png)

> **"En el mundo de las batallas Pokemon, cada decisión cuenta. Cada movimiento, cada cambio, cada estrategia puede determinar la diferencia entre la victoria y la derrota. Nuestro objetivo: crear una IA que no solo prediga batallas, sino que las JUEGUE, aprenda de cada decisión y se convierta en el mejor entrenador Pokemon."**

## 🎯 La Misión Épica: Crear el Maestro Pokemon Definitivo

**Un agente de Reinforcement Learning que juega batallas Pokemon, aprende de cada decisión y evoluciona continuamente.** Este no es un simple predictor: es un **entrenador artificial** que toma decisiones en tiempo real, explora estrategias, comete errores, aprende de ellos y mejora hasta alcanzar el nivel de los mejores jugadores humanos.

### 🌟 La Visión Final

Imagina una IA que:

- ✨ **Juega batallas completas** tomando decisiones turno a turno
- 🧠 **Aprende de cada acción** mediante Reinforcement Learning
- 🔄 **Se entrena mediante self-play** contra versiones de sí misma
- 📈 **Mejora continuamente** con cada batalla jugada
- 🎯 **Explica sus decisiones** con razonamiento estratégico
- 🏆 **Compite contra humanos** y aprende de maestros Pokemon

### 🏆 El Viaje Épico: Estado Actual

**Fase 1: Toma de Contacto - Conociendo el Campo de Batalla** ✅ **COMPLETADO**

- ✅ Análisis exploratorio de 14,000+ batallas reales (`EDA_notebook_ready.ipynb`)
- ✅ Visualizaciones temáticas que revelan patrones del meta-game
- ✅ Comprensión profunda de tipos, Pokemon y mecánicas
- ✅ Baseline predictor: ROC-AUC **0.819** - *"¿Puede un modelo predecir victorias?"*
- 📊 **Aprendizaje clave**: Sí, los patrones existen y son capturables

**Fase 2: Análisis de Decisiones - El Cerebro del Entrenador** 🔄 **EN PROGRESO**

- 🎯 Nuevo notebook: `EDA_Decision_Analysis.ipynb`
- 🔍 Análisis turno a turno de decisiones exitosas
- 🧠 Identificación de patrones en secuencias de movimientos
- 📈 Diseño del espacio de estados y acciones para RL
- 🎮 Extracción de "jugadas ganadoras" de maestros Pokemon

**Fase 3: El Primer Agente - Aprendiendo a Jugar** ⏸️ **PENDIENTE**

- 🤖 Implementación de agente DQN (Deep Q-Network)
- 🎲 Entrenamiento mediante self-play
- 📊 Sistema de recompensas y evaluación
- 🔄 Integración con Pokemon Showdown API
- 🎯 Objetivo: Ganar > 50% contra jugadores random

**Fase 4: Evolución y Maestría - El Camino al Top** ⏸️ **PENDIENTE**

- 🚀 Algoritmos avanzados: PPO, A3C, AlphaZero-style
- 🧬 Optimización de hiperparámetros y arquitecturas
- 🏆 Competición contra jugadores humanos
- 📈 Aprendizaje continuo desde batallas en vivo
- 🎯 Objetivo final: Alcanzar nivel competitivo (1500+ ELO)

### 📊 **Estado Actual del Proyecto**

**🎯 Fase 1 Completada - Toma de Contacto:**

- ✅ **EDA Exploratorio**: 14,000+ batallas analizadas
- ✅ **Baseline Predictor**: ROC-AUC 0.819 (prueba de concepto exitosa)
- ✅ **Feature Engineering**: 37 características pre-batalla extraídas
- ✅ **Type Matchups**: Sistema 18x18 tipos implementado
- ✅ **Pokemon Database**: 200+ especies mapeadas con BST
- 📝 **Conclusión**: Los patrones de victoria son predecibles, base sólida para RL

**🔬 Próximos Pasos - Fase 2:**

- 🎯 Crear `EDA_Decision_Analysis.ipynb`
- 🔍 Analizar decisiones turno a turno
- 🧠 Diseñar espacio de estados para agente RL
- 📊 Identificar patrones en secuencias de acciones
- 🎮 Preparar datos para entrenamiento de agente

### 📊 Visualizaciones Generadas

**Análisis Exploratorio:**

- `battle_patterns_analysis.png` - Patrones de duración y eventos
- `pokemon_analysis.png` - Top Pokemon, niveles, HP
- `type_analysis.png` - Distribución y winrates por tipo
- `distributions_analysis.png` - Distribuciones y outliers
- `correlation_matrix_filtered.png` - Correlaciones entre features

**Modelo Baseline:**

- `baseline_model_performance.png` - ROC Curve (AUC=0.819) + Top 15 Features

## 📊 El Arsenal de Datos: La Memoria de 14,000 Batallas

**La Biblioteca Completa de Experiencia Pokemon:**

- **Fuente**: Batallas reales de Pokemon Showdown (formato gen9randombattle)
- **Escala**: ~14,000 batallas individuales con logs completos
- **Formato**: JSON estructurado con secuencias de decisiones turno a turno
- **Riqueza**: Movimientos, cambios, daño, estados, metadata de jugadores
- **Valor para RL**: Cada batalla es una secuencia de (estado, acción, recompensa)
- **Uso actual**: Fase 1 (predicción) → Fase 2+ (entrenamiento de agente)

### 🎮 Base de Datos Pokemon (`pokemon_data.py`)

**El corazón del sistema de type matchups:**

- **200+ Pokemon** con especies mapeadas (Gen 1-9)
- **Matriz 18x18** de efectividad de tipos completa
- **Base Stat Totals (BST)** para todos los Pokemon
- **Tiers competitivos**: Uber, OU, UU, RU
- **Funciones helper**: `get_pokemon_types()`, `get_pokemon_bst()`, `calculate_matchup_score()`

**Especies incluidas:**

- ✅ Todos los starters (Gen 1-9)
- ✅ Todos los legendarios principales
- ✅ Todos los pseudo-legendarios
- ✅ Pokemon competitivos populares
- ✅ Gen 9 completo (Paldea)

### 🎭 Los Protagonistas de Nuestra Historia

Cada batalla es un testimonio de:
- **Decisiones bajo presión** de entrenadores reales
- **Estrategias complejas** ejecutadas en tiempo real
- **Momentos críticos** que definen victoria o derrota
- **Patrones meta** que solo emergen con grandes volúmenes de datos

## 🚀 Arquitectura del Sistema: Del Análisis al Agente

### 🔬 Fase 1: Fundamentos (Completado)

**Sistema de Predicción (Baseline):**

- ✅ Pipeline de datos: JSON → Features → Modelo
- ✅ 7 algoritmos ML probados (Logistic, RF, XGBoost, LightGBM, NN, SVM, GB)
- ✅ Métricas avanzadas: ROC-AUC, MCC, Brier Score
- ✅ Visualizaciones temáticas Pokemon
- ✅ Base de datos Pokemon con tipos y BST
- 📝 **Resultado**: Predicción funcional, patrones identificados

### 🤖 Fase 2-4: Agente RL (Roadmap)

**Componentes a Desarrollar:**

1. **🧠 Agente de Reinforcement Learning**
   - Arquitecturas: DQN, PPO, A3C
   - Redes neuronales con PyTorch
   - Sistema de memoria y replay buffer
   - Exploración vs explotación (epsilon-greedy)

2. **🎮 Entorno de Batalla**
   - Integración con Pokemon Showdown API
   - Simulador local para self-play
   - Representación de estados de batalla
   - Sistema de acciones (movimientos + cambios)

3. **📊 Sistema de Recompensas**
   - Recompensa final: +1 victoria / -1 derrota
   - Recompensas intermedias: daño, KOs, ventaja
   - Penalizaciones: movimientos inútiles, errores
   - Shaping para acelerar aprendizaje

4. **🔄 Pipeline de Entrenamiento**
   - Self-play: agente vs agente
   - Evaluación contra baselines
   - Guardado de checkpoints
   - Monitorización de progreso

5. **📊 Análisis y Evaluación**
   - Winrate vs diferentes oponentes
   - Análisis de estrategias aprendidas
   - Visualización de decisiones
   - Comparación con jugadores humanos

## 🏗️ Estructura del Proyecto

```text
Pokemon_battle/ 🏰 El Camino hacia el Maestro Pokemon
├── src/ ⚔️ Código Principal
│   ├── data/ 🧬 Procesamiento de Datos
│   │   ├── processors.py          # Extracción de features (Fase 1)
│   │   ├── battle_parser.py       # Parser de batallas para RL (Fase 2+)
│   │   ├── loaders/               # Carga de datos
│   │   └── validators/            # Validación de datos
│   ├── models/ 🤖 Modelos de IA
│   │   ├── architectures.py       # Redes neuronales (predictor + agente)
│   │   ├── rl_agent.py            # Agente RL (DQN/PPO) - Fase 3+
│   │   └── pretrained/            # Modelos guardados
│   ├── training/ 🏟️ Entrenamiento
│   │   ├── ml_trainer.py          # Entrenador ML clásico (Fase 1)
│   │   ├── rl_trainer.py          # Entrenador RL (Fase 3+)
│   │   └── self_play.py           # Sistema de self-play (Fase 3+)
│   ├── environment/ 🎮 Entorno de Batalla
│   │   ├── battle_env.py          # Gym environment (Fase 3+)
│   │   ├── showdown_api.py        # Integración Pokemon Showdown (Fase 3+)
│   │   └── simulator.py           # Simulador local (Fase 3+)
│   └── utils/ 🛠️ Utilidades
├── config/ ⚙️ Configuración
│   └── config.py                  # Configuración global
├── data/ 💾 Datos
│   ├── battles/                   # 14,000+ batallas JSON
│   ├── all_battles.json          # Dataset completo
│   ├── battles_sample_2000.json  # Muestra para desarrollo
│   └── rl_experiences/            # Experiencias del agente (Fase 3+)
├── notebooks/ 📚 Notebooks de Análisis
│   ├── EDA_notebook_ready.ipynb       # ✅ Fase 1: Toma de contacto
│   ├── EDA_Decision_Analysis.ipynb    # 🔄 Fase 2: Análisis de decisiones
│   ├── ML_Training_Advanced.ipynb     # ✅ Fase 1: Baseline predictor
│   └── RL_Agent_Training.ipynb        # ⏸️ Fase 3+: Entrenamiento agente
├── assets/ 🎨 Visualizaciones
│   └── images/                    # Gráficos y análisis
├── tests/ 🧪 Tests
├── docs/ 📜 Documentación
└── logs/ 📝 Logs del sistema
```

## 🛠️ Instalación y Configuración

### Prerrequisitos

- Python 3.8+
- Git
- 4GB RAM mínimo (8GB recomendado)
- GPU opcional (para entrenamiento acelerado)

### Instalación Completa

```bash
# Clonar repositorio
git clone https://github.com/AlexGHerrera/Pokemon-battle-ai.git
cd Pokemon-battle-ai

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Crear directorios necesarios
python config/config.py
```

### Variables de Entorno (Opcional)

```bash
# .env
USE_GPU=true          # Usar GPU para entrenamiento
DEBUG=false           # Modo debug del servidor
DATA_SAMPLE_SIZE=2000 # Tamaño de muestra para desarrollo
```

## 🚀 Guía de Uso

### 📊 Fase 1: Toma de Contacto (Completado)

**1. Análisis Exploratorio de Datos:**

```bash
# Ejecutar EDA completo
jupyter lab notebooks/EDA_notebook_ready.ipynb
```

**Qué descubrirás:**

- Patrones de victoria en 14,000+ batallas
- Pokemon y tipos más efectivos
- Correlaciones entre features
- Baseline predictor: ROC-AUC 0.819

**2. Entrenar Baseline Predictor (Opcional):**

```bash
# Entrenar 7 algoritmos ML
jupyter lab notebooks/ML_Training_Advanced.ipynb
```

**Resultado:**

- Comparación de 7 algoritmos
- Visualizaciones de rendimiento
- Modelo guardado para referencia

### 🔬 Fase 2: Análisis de Decisiones (Próximo Paso)

**Crear notebook de análisis de decisiones:**

```bash
# Analizar decisiones turno a turno
jupyter lab notebooks/EDA_Decision_Analysis.ipynb
```

**Objetivos:**

- Extraer secuencias (estado, acción, resultado)
- Identificar movimientos exitosos por situación
- Diseñar espacio de estados para RL
- Analizar estrategias de jugadores top

### 🤖 Fase 3+: Entrenamiento de Agente RL (Futuro)

**Entrenar agente que juega batallas:**

```python
# Ejemplo conceptual (a implementar)
from src.models.rl_agent import DQNAgent
from src.environment.battle_env import PokemonBattleEnv
from src.training.rl_trainer import RLTrainer

# Crear entorno
env = PokemonBattleEnv()

# Crear agente
agent = DQNAgent(
    state_size=env.observation_space.shape[0],
    action_size=env.action_space.n
)

# Entrenar mediante self-play
trainer = RLTrainer(agent, env)
trainer.train(episodes=10000)
```

## 🔧 Configuración (Roadmap)

### Configuración de Agente RL (Fase 3+)

```python
# config/config.py - A implementar
RL_CONFIG = {
    # Arquitectura del agente
    "agent_type": "DQN",  # DQN, PPO, A3C
    "state_size": 256,    # Dimensión del estado
    "action_size": 9,     # 4 movimientos + 5 cambios
    "hidden_layers": [512, 256, 128],
    
    # Hiperparámetros de entrenamiento
    "learning_rate": 0.0001,
    "gamma": 0.99,        # Factor de descuento
    "epsilon_start": 1.0, # Exploración inicial
    "epsilon_end": 0.01,
    "epsilon_decay": 0.995,
    
    # Replay buffer
    "buffer_size": 100000,
    "batch_size": 64,
    
    # Self-play
    "episodes": 10000,
    "max_steps_per_episode": 100,
    "update_target_every": 1000,
}
```

### Sistema de Recompensas (Fase 3+)

```python
REWARD_CONFIG = {
    "win": 1.0,
    "loss": -1.0,
    "ko_opponent": 0.3,
    "lose_pokemon": -0.3,
    "damage_dealt": 0.001,  # Por punto de daño
    "damage_taken": -0.001,
    "invalid_move": -0.5,
    "type_advantage": 0.1,
}
```

## 📊 Componentes del Sistema

### Fase 1 (Implementado)

- ✅ **BattleDataProcessor**: Extrae features de batallas
- ✅ **PokemonMLTrainer**: Entrena 7 algoritmos ML
- ✅ **Type Matchup System**: Cálculo de efectividad
- ✅ **Visualization Suite**: Gráficos temáticos

### Fase 2+ (A Implementar)

- ⏸️ **BattleParser**: Extrae secuencias de decisiones
- ⏸️ **PokemonBattleEnv**: Gym environment para RL
- ⏸️ **DQNAgent / PPOAgent**: Agentes de RL
- ⏸️ **RLTrainer**: Sistema de entrenamiento RL
- ⏸️ **SelfPlaySystem**: Self-play para mejora continua
- ⏸️ **ShowdownAPI**: Integración con Pokemon Showdown

### Archivos Generados

**Fase 1:**

- `output/battle_features.csv` - Features extraídas
- `output/*.png` - Visualizaciones EDA
- `src/models/pretrained/baseline_*.pkl` - Modelos baseline

**Fase 3+ (Futuro):**

- `data/rl_experiences/` - Experiencias del agente
- `src/models/pretrained/agent_*.pth` - Checkpoints del agente
- `logs/training_*.log` - Logs de entrenamiento RL

## 🎯 Insights Clave para IA

![Pokemon Usage Analysis](assets/images/pokemon_analysis.png)

### Patrones Estratégicos Identificados

- **Balance de jugadores**: Distribución equilibrada de victorias p1 vs p2
- **Duración óptima**: Batallas de 15-25 turnos muestran mayor complejidad estratégica
- **Meta dominante**: Top Pokemon más utilizados (Arceus, Rotom, Oricorio)
- **Eventos críticos**: Ratio movimientos/switches indica agresividad vs cautela
- **Tipos dominantes**: Dragon (143 usos), Flying (134 usos), Poison (81 usos)
- **Mejores winrates**: Rock (51.1%), Dark (51.1%), Ghost (48.8%)

![Type Analysis](assets/images/type_analysis.png)

### Features Válidas para ML (Sin Data Leakage)

**✅ Información PRE-BATALLA (Deployable en producción):**

**1. Type Matchups** ⭐⭐⭐⭐⭐ (Factor #1 en Pokemon)

- `type_advantage_score`: Ventaja elemental general
- `super_effective_count`: Cuántos Pokemon tienen ventaja de tipo
- `resisted_count`: Cuántos ataques serán resistidos
- `type_diversity`: Variedad de tipos en el equipo
- `dual_type_count`: Pokemon con doble tipo

**2. Pokemon Strength (BST)** ⭐⭐⭐⭐

- `avg_bst`: Base Stat Total promedio del equipo
- `bst_advantage`: Ventaja de poder bruto
- `legendary_count`: Número de Pokemon legendarios
- `pseudo_legendary_count`: Número de pseudo-legendarios
- `min/max_bst`: Pokemon más débil/fuerte

**3. Composición Observable** ⭐⭐⭐⭐

- `team_size`: Tamaño del equipo
- `avg_level`: Nivel promedio de Pokemon
- `total_hp`: HP total disponible
- `species_diversity`: Diversidad de especies

**4. Ventajas Derivadas** ⭐⭐⭐

- `level_advantage`: Diferencia de niveles entre equipos
- `hp_advantage`: Diferencia de HP total
- `bst_advantage`: Diferencia de poder bruto

**❌ NO USAMOS (Sería data leakage):**

- ~~`total_turns`~~ - Solo se conoce al final
- ~~`move_events`, `switch_events`~~ - Ocurren durante la batalla
- ~~`ladder_rating`~~ - No disponible en producción

## 📊 Fase 1: Revelaciones del Análisis Exploratorio

### 🎭 La Historia que Cuentan los Números

![Distributions Analysis](assets/images/distributions_analysis.png)

**Patrones épicos descubiertos en nuestro viaje:**
- **Duración de batallas**: Media de 24.5 turnos (el ritmo perfecto del drama)
- **Eventos por turno**: Correlación alta (0.981) con duración total
- **Outliers**: ~3-4% de batallas verdaderamente excepcionales
- **Análisis integrado**: Cada gráfico revela patrones estratégicos Pokemon

### 🏆 Los Campeones Revelados

**Pokemon más utilizados (Los protagonistas):**
- **Arceus**: El dios Pokemon, omnipresente en batallas
- **Rotom**: El espíritu versátil que se adapta a todo
- **Oricorio**: El bailarín que sorprende con su presencia

**Tipos dominantes (Las fuerzas elementales):**
- **Dragon** (143 usos): Los legendarios reinan supremos
- **Flying** (134 usos): La libertad del cielo
- **Poison** (81 usos): La toxicidad estratégica

### Correlaciones de Features Válidas

![Correlation Matrix](assets/images/correlation_matrix_filtered.png)

**Insights clave del análisis de correlaciones:**

- Type matchups y BST son altamente predictivos
- Features de composición observable muestran patrones claros
- No hay multicolinealidad problemática entre features válidas
- El modelo puede aprender relaciones complejas sin data leakage

### Configuración Avanzada

```python
# Muestra pequeña para pruebas rápidas
battles = create_sample_dataset(sample_size=500)

# Muestra grande para análisis detallado
battles = create_sample_dataset(sample_size=5000)
```

## 📈 Roadmap: El Camino hacia el Maestro Pokemon

### ✅ Fase 1: Toma de Contacto (Completado)

**Objetivo:** Entender el dominio y validar que los patrones existen

- ✅ EDA de 14,000+ batallas
- ✅ Sistema de type matchups
- ✅ Base de datos Pokemon (200+ especies)
- ✅ Baseline predictor (ROC-AUC 0.819)
- ✅ Visualizaciones temáticas
- 📝 **Conclusión:** Los patrones de victoria son predecibles

### 🔄 Fase 2: Análisis de Decisiones (En Progreso)

**Objetivo:** Entender qué decisiones llevan a la victoria

- 🎯 Crear `EDA_Decision_Analysis.ipynb`
- 🔍 Extraer secuencias (estado, acción, resultado) de batallas
- 🧠 Analizar movimientos exitosos por situación
- 📊 Identificar patrones en secuencias de acciones
- 🎮 Diseñar espacio de estados y acciones para RL
- 📈 Estudiar estrategias de jugadores top vs random

### ⏸️ Fase 3: Primer Agente RL (Pendiente)

**Objetivo:** Crear un agente que aprenda a jugar desde cero

1. **Implementar Entorno de Batalla**
   - Gym environment compatible con OpenAI Gym
   - Representación de estados de batalla
   - Sistema de acciones válidas
   - Cálculo de recompensas

2. **Implementar Agente DQN**
   - Red neuronal para Q-values
   - Replay buffer para experiencias
   - Target network para estabilidad
   - Epsilon-greedy para exploración

3. **Sistema de Self-Play**
   - Entrenamiento agente vs agente
   - Guardado de checkpoints
   - Monitorización de progreso
   - Evaluación contra baselines

4. **Integración con Pokemon Showdown**
   - API para jugar batallas reales
   - Parser de estados de batalla
   - Sistema de acciones

**🎯 Objetivo:** Winrate > 50% contra jugadores random

### ⏸️ Fase 4: Evolución y Maestría (Futuro)

**Objetivo:** Alcanzar nivel competitivo humano

1. **Algoritmos Avanzados**
   - PPO (Proximal Policy Optimization)
   - A3C (Asynchronous Actor-Critic)
   - AlphaZero-style (MCTS + Neural Networks)

2. **Mejoras de Arquitectura**
   - Attention mechanisms para focus en Pokemon clave
   - LSTM para memoria de secuencias
   - Embeddings de Pokemon y movimientos

3. **Curriculum Learning**
   - Empezar contra oponentes débiles
   - Incrementar dificultad progresivamente
   - Aprender de jugadores humanos top

4. **Explicabilidad**
   - Visualización de decisiones
   - Análisis de estrategias aprendidas
   - Generación de narrativas de batalla

**🎯 Objetivo:** ELO 1500+ en Pokemon Showdown

### 🌟 Visión Final: El Maestro Pokemon AI

Una IA que:

- ✨ **Juega batallas** a nivel competitivo humano
- 🧠 **Aprende continuamente** de cada batalla
- 🔄 **Se adapta** a cambios en el meta-game
- 📊 **Explica sus decisiones** de forma comprensible
- 🏆 **Compite** contra los mejores jugadores
- 💡 **Descubre estrategias** que humanos no han considerado

## 🤝 Contribuir

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 👥 Autores

- **Alejandro Guerra Herrera** - *Desarrollo inicial* - [GitHub](https://github.com/AlexGHerrera)

## 🙏 Agradecimientos Épicos

- **Pokemon Showdown** por ser la fuente de nuestras 14,000+ batallas épicas
- **Comunidad Pokemon competitivo** por crear las estrategias que analizamos
- **HackABoss** por proporcionar el escenario para esta aventura épica
- **Satoshi Tajiri** por crear el universo Pokemon que inspiró este proyecto
- **Todos los entrenadores** cuyas batallas alimentan nuestros algoritmos

### 🎭 **Filosofía del Proyecto**

> *"En cada dataset hay una historia esperando ser contada. En cada algoritmo hay un gladiador esperando su momento de gloria. En cada predicción hay una decisión que puede cambiar el curso de una batalla."*
>
> **— El Manifiesto del Pokemon Battle AI**

## 📞 Contacto

Para preguntas o colaboraciones:
- **Email**: <alex_gh@live.com>
- **LinkedIn**: [Alejandro Guerra Herrera](https://www.linkedin.com/in/alejandro-guerra-herrera-a86053115/)
- **GitHub**: [@AlexGHerrera](https://github.com/AlexGHerrera)

---

---

## 🌟 **¡Únete a la Leyenda!**

⭐ **¡Dale una estrella si este proyecto épico te ha inspirado!** ⭐

**¿Te atreves a crear un agente que aprenda a jugar Pokemon?**  
**¿Lograrás que supere a jugadores humanos?**  
**¿Descubrirás estrategias que ni los maestros Pokemon conocen?**

### 🔥 **La aventura apenas comienza...**

*Fase 1 completada: Sabemos que los patrones existen.*  
*Fase 2 en progreso: Entendiendo las decisiones ganadoras.*  
*Fase 3+: Crear el agente que juegue y aprenda.*

**¡El camino hacia el Maestro Pokemon AI está trazado!** 🚀
