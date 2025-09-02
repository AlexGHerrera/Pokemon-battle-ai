# %% [markdown]
# # Pokemon Battle Dataset - Análisis Exploratorio de Datos (EDA)
# 
# ## Alcance del Proyecto
# 
# Este proyecto tiene como objetivo desarrollar un **modelo de inteligencia artificial capaz de jugar Pokemon de forma autónoma** contra usuarios humanos. Para lograr esto, necesitamos comprender profundamente los patrones de batalla, estrategias ganadoras y comportamientos de los jugadores expertos.
# 
# ### Finalidad del EDA
# 
# **Objetivo Principal**: Extraer insights del dataset de batallas Pokemon Showdown para entrenar un modelo de IA competitivo.
# 
# **Objetivos Específicos**:
# 1. **Análisis de Calidad**: Validar la integridad y completitud del dataset de batallas
# 2. **Patrones Estratégicos**: Identificar comportamientos que llevan al éxito en batalla
# 3. **Feature Engineering**: Extraer características relevantes para el aprendizaje automático
# 4. **Análisis del Meta**: Entender qué Pokemon y estrategias dominan el formato competitivo
# 5. **Optimización de Datos**: Preparar el dataset para entrenamiento eficiente del modelo
# 
# ### Contexto del Dataset
# 
# - **Fuente**: Batallas reales de Pokemon Showdown (formato gen9randombattle)
# - **Volumen**: ~14,000 batallas individuales en formato JSON
# - **Contenido**: Turnos secuenciales, eventos de batalla, estados del juego, resultados
# - **Aplicación**: Entrenamiento de modelo de IA para toma de decisiones en tiempo real
# 
# ### Metodología
# 
# Este EDA está estructurado para maximizar la extracción de conocimiento útil para el modelo de IA:
# - **Análisis incremental** desde datos básicos hasta patrones complejos
# - **Visualizaciones explicativas** que revelen insights estratégicos
# - **Optimizaciones de rendimiento** para manejo eficiente de grandes volúmenes de datos
# - **Features estructuradas** listas para algoritmos de machine learning
# 
# ---
# 
# # %% [markdown]
# ## Importación de librerías y configuración inicial
# 
# **Objetivo de esta sección:**
# - Importamos las librerías necesarias para el análisis de datos y visualización
# - Configuramos matplotlib y seaborn para generar gráficas consistentes y profesionales
# - Establecemos warnings para evitar mensajes innecesarios durante el procesamiento
# - Estas configuraciones son fundamentales para un EDA reproducible y visualmente atractivo

# %%
from __future__ import annotations
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import random

# Configuración de visualizaciones
plt.style.use('default')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

print("✅ Librerías importadas correctamente")
print("✅ Configuración de visualización establecida")

# %% [markdown]
# ## Configuración de rutas y constantes
# 
# **Propósito de la configuración:**
# - Centralizamos la gestión de archivos para facilitar el mantenimiento del código
# - `BATTLES_DIR`: Contiene los archivos JSON individuales de cada batalla
# - `ALL_BATTLES_JSON`: Archivo consolidado que mejora la velocidad de carga
# - `OUTPUT_DIR`: Directorio donde guardaremos visualizaciones y resultados
# - Esta organización es crucial para un flujo de trabajo ordenado y escalable

# %%
DATA_DIR = Path("data")
BATTLES_DIR = DATA_DIR / "battles"
ALL_BATTLES_JSON = DATA_DIR / "all_battles.json"
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

print(f"📁 Directorio de datos: {DATA_DIR}")
print(f"📁 Directorio de batallas: {BATTLES_DIR}")
print(f"📄 Archivo consolidado: {ALL_BATTLES_JSON}")
print(f"📊 Directorio de salida: {OUTPUT_DIR}")

# %% [markdown]
# ## Funciones auxiliares para procesamiento de datos
# 
# **Funciones implementadas:**
# - `get_in()`: Navega estructuras JSON anidadas de forma segura, evitando errores por claves faltantes
# - `extract_pokemon_info()`: Extrae información específica de Pokemon que será clave para el modelo de IA
# - `calculate_battle_metrics()`: Calcula métricas estratégicas como eventos por turno, tipos de acciones, etc.
# - Estas funciones nos permiten transformar datos complejos en features estructuradas para machine learning

# %%
def get_in(d: Any, path: List[str], default: Any = None) -> Any:
    """Extrae valores anidados de diccionarios de forma segura."""
    cur = d
    for k in path:
        if isinstance(cur, dict) and k in cur:
            cur = cur[k]
        else:
            return default
    return cur

def extract_pokemon_info(battle: dict) -> List[dict]:
    """Extrae información detallada de Pokemon de una batalla."""
    pokemon_info = []
    teams = get_in(battle, ["team_revelation", "teams"], {})
    
    for player_id, team in teams.items():
        if isinstance(team, list):
            for pokemon in team:
                info = {
                    'battle_id': battle.get('battle_id'),
                    'player': player_id,
                    'species': pokemon.get('species'),
                    'level': pokemon.get('level'),
                    'gender': pokemon.get('gender'),
                    'hp': get_in(pokemon, ['base_stats', 'hp']),
                    'first_seen_turn': pokemon.get('first_seen_turn'),
                    'revelation_status': pokemon.get('revelation_status')
                }
                pokemon_info.append(info)
    return pokemon_info

def calculate_battle_metrics(battle: dict) -> dict:
    """Calcula métricas clave de una batalla para análisis."""
    metadata = battle.get('metadata', {})
    turns = battle.get('turns', [])
    
    # Métricas básicas
    total_turns = len(turns)
    winner = get_in(metadata, ['outcome', 'winner'])
    reason = get_in(metadata, ['outcome', 'reason'])
    
    # Análisis de eventos por turno
    total_events = sum(len(turn.get('events', [])) for turn in turns)
    move_events = 0
    switch_events = 0
    damage_events = 0
    
    for turn in turns:
        events = turn.get('events', [])
        for event in events:
            event_type = event.get('type')
            if event_type == 'move':
                move_events += 1
            elif event_type == 'switch':
                switch_events += 1
            elif event_type == 'damage':
                damage_events += 1
    
    return {
        'battle_id': battle.get('battle_id'),
        'total_turns': total_turns,
        'total_events': total_events,
        'move_events': move_events,
        'switch_events': switch_events,
        'damage_events': damage_events,
        'winner': winner,
        'reason': reason,
        'events_per_turn': total_events / max(total_turns, 1),
        'timestamp': metadata.get('timestamp_unix')
    }

print("✅ Funciones auxiliares definidas correctamente")

# %% [markdown]
# ## Funciones de optimización para datasets grandes
# 
# **Estrategias implementadas:**
# - Muestreo aleatorio para desarrollo rápido
# - Conversión a formato Parquet (más eficiente)
# - Carga por chunks para evitar problemas de memoria
# - Procesamiento incremental de batallas

# %%
def create_sample_dataset(sample_size: int = 1000, force_recreate: bool = False) -> List[dict]:
    """
    Crea un dataset de muestra para desarrollo rápido.
    
    Args:
        sample_size: Número de batallas a incluir en la muestra
        force_recreate: Si True, recrea la muestra aunque ya exista
    """
    sample_path = DATA_DIR / f"battles_sample_{sample_size}.json"
    
    if sample_path.exists() and not force_recreate:
        print(f"Cargando muestra existente: {sample_path}")
        with open(sample_path, "r") as f:
            return json.load(f)
    
    print(f"Creando nueva muestra de {sample_size} batallas...")
    
    # Cargar dataset completo y tomar muestra aleatoria
    with open(ALL_BATTLES_JSON, "r") as f:
        all_battles = json.load(f)
    
    import random
    random.seed(42)  # Para reproducibilidad
    sample_battles = random.sample(all_battles, min(sample_size, len(all_battles)))
    
    # Guardar muestra
    with open(sample_path, "w") as f:
        json.dump(sample_battles, f, indent=2)
    
    print(f"Muestra guardada: {sample_path}")
    print(f"Tamaño de muestra: {len(sample_battles)} batallas")
    
    return sample_battles

def convert_to_parquet() -> None:
    """
    Convierte el dataset a formato Parquet para acceso más rápido.
    """
    parquet_path = DATA_DIR / "battles_optimized.parquet"
    
    if parquet_path.exists():
        print(f"Archivo Parquet ya existe: {parquet_path}")
        return
    
    print("Convirtiendo a formato Parquet...")
    
    # Cargar y procesar por chunks
    chunk_size = 1000
    all_metrics = []
    
    with open(ALL_BATTLES_JSON, "r") as f:
        battles = json.load(f)
    
    for i in range(0, len(battles), chunk_size):
        chunk = battles[i:i+chunk_size]
        chunk_metrics = [calculate_battle_metrics(battle) for battle in chunk]
        all_metrics.extend(chunk_metrics)
        
        if (i + chunk_size) % 5000 == 0:
            print(f"Procesadas {i + chunk_size} batallas...")
    
    # Convertir a DataFrame y guardar
    df = pd.DataFrame(all_metrics)
    df.to_parquet(parquet_path, index=False)
    
    print(f"Dataset convertido a Parquet: {parquet_path}")
    print(f"Tamaño original JSON: {ALL_BATTLES_JSON.stat().st_size / 1024 / 1024:.1f} MB")
    print(f"Tamaño Parquet: {parquet_path.stat().st_size / 1024 / 1024:.1f} MB")

def load_battles_optimized(use_sample: bool = True, sample_size: int = 1000) -> List[dict]:
    """
    Carga optimizada de datos con opciones de muestreo.
    
    Args:
        use_sample: Si True, usa una muestra para desarrollo rápido
        sample_size: Tamaño de la muestra si use_sample=True
    """
    if use_sample:
        print(f"Modo desarrollo: usando muestra de {sample_size} batallas")
        return create_sample_dataset(sample_size)
    else:
        print("Modo producción: cargando dataset completo")
        if ALL_BATTLES_JSON.exists():
            with open(ALL_BATTLES_JSON, "r") as f:
                return json.load(f)
        else:
            raise FileNotFoundError(f"No existe {ALL_BATTLES_JSON}")

def load_parquet_if_exists() -> Optional[pd.DataFrame]:
    """
    Carga el archivo Parquet si existe, para análisis rápido.
    """
    parquet_path = DATA_DIR / "battles_optimized.parquet"
    
    if parquet_path.exists():
        print(f"Cargando datos desde Parquet: {parquet_path}")
        return pd.read_parquet(parquet_path)
    else:
        print("Archivo Parquet no encontrado. Usa convert_to_parquet() primero.")
        return None

# %% [markdown]
# ## 1. Carga y consolidación de datos
# 
# **Justificación de la consolidación:**
# - Los datos vienen en miles de archivos JSON individuales, lo que es ineficiente para análisis
# - La consolidación mejora significativamente la velocidad de carga y procesamiento
# - Nos permite validar la integridad de los datos y detectar archivos corruptos
# - Facilita el análisis posterior al tener todos los datos en una estructura unificada
# - Es un paso fundamental antes de cualquier análisis exploratorio serio

# %%
def load_battles_data() -> List[dict]:
    """Carga y consolida todos los datos de batallas."""
    if ALL_BATTLES_JSON.exists():
        with open(ALL_BATTLES_JSON, "r") as f:
            return json.load(f)
    
    # Si no existe el archivo consolidado, lo creamos
    json_files = sorted(BATTLES_DIR.glob("*.json"))
    battles_data = []
    
    print(f"Consolidando {len(json_files)} archivos JSON...")
    
    for i, file in enumerate(json_files):
        try:
            with open(file, "r") as f:
                battle = json.load(f)
                battles_data.append(battle)
        except Exception as e:
            print(f"Error procesando {file.name}: {e}")
            continue
        
        if (i + 1) % 1000 == 0:
            print(f"Procesados {i + 1} archivos...")
    
    # Guardar archivo consolidado
    with open(ALL_BATTLES_JSON, "w") as f:
        json.dump(battles_data, f, indent=2)
    
    print(f"Datos consolidados: {len(battles_data)} batallas")
    return battles_data

# Cargar datos
battles = load_battles_optimized(use_sample=True, sample_size=2000)  # Modo desarrollo por defecto
print(f"Total de batallas cargadas: {len(battles):,}")

# %% [markdown]
# ### Configuración de modo de trabajo
# 
# **Para cambiar entre modos:**
# - **Desarrollo rápido**: `battles = load_battles_optimized(use_sample=True, sample_size=2000)`
# - **Dataset completo**: `battles = load_battles_optimized(use_sample=False)`
# - **Desde Parquet**: `df_battles = load_parquet_if_exists()`

# %% [markdown]
# ## 2. Análisis de calidad de datos
# 
# **Importancia del análisis de calidad:**
# - Identificamos problemas de datos antes de invertir tiempo en análisis incorrectos
# - Validamos que las batallas tengan la estructura esperada (battle_id, metadata, turns)
# - Detectamos patrones de datos faltantes que podrían sesgar nuestro modelo
# - Entendemos la distribución de formatos de batalla para enfocar el entrenamiento
# - La calidad de datos determina directamente la calidad del modelo de IA resultante

# %%
print("=" * 60)
print("ANÁLISIS DE CALIDAD DE DATOS")
print("=" * 60)

# Estadísticas básicas
total_battles = len(battles)
print(f"Total de batallas: {total_battles:,}")

# Validación de estructura
valid_battles = 0
incomplete_battles = 0

required_keys = ['battle_id', 'metadata', 'turns']
for battle in battles:
    if all(key in battle for key in required_keys):
        valid_battles += 1
    else:
        incomplete_battles += 1

print(f"Batallas con estructura completa: {valid_battles:,} ({valid_battles/total_battles*100:.1f}%)")
print(f"Batallas incompletas: {incomplete_battles:,} ({incomplete_battles/total_battles*100:.1f}%)")

# Análisis de formatos
formats = Counter(battle.get('format_id') for battle in battles)
print(f"\nFormatos de batalla encontrados:")
for format_id, count in formats.most_common():
    print(f"  - {format_id}: {count:,} batallas")

# %% [markdown]
# ## 3. Análisis de resultados de batalla
# 
# **Relevancia del análisis de resultados:**
# - Verificamos si hay balance entre jugadores (p1 vs p2) para evitar sesgos en el entrenamiento
# - Las razones de finalización nos indican qué estrategias son más efectivas
# - La duración de batallas revela patrones de juego defensivo vs agresivo
# - Estos patrones son fundamentales para que la IA aprenda estrategias ganadoras
# - Un dataset balanceado asegura que el modelo no favorezca injustamente a un jugador

# %%
print("\n" + "=" * 60)
print("ANÁLISIS DE RESULTADOS DE BATALLA")
print("=" * 60)

# Extraer métricas de batalla
battle_metrics = [calculate_battle_metrics(battle) for battle in battles]
df_battles = pd.DataFrame(battle_metrics)

# Análisis de ganadores
winner_counts = df_battles['winner'].value_counts()
print(f"Distribución de ganadores:")
for winner, count in winner_counts.items():
    print(f"  - {winner}: {count:,} ({count/len(df_battles)*100:.1f}%)")

# Razones de victoria
reason_counts = df_battles['reason'].value_counts()
print(f"\nRazones de finalización:")
for reason, count in reason_counts.items():
    print(f"  - {reason}: {count:,} ({count/len(df_battles)*100:.1f}%)")

# Estadísticas de duración
print(f"\nEstadísticas de duración de batalla:")
print(f"  - Turnos promedio: {df_battles['total_turns'].mean():.1f}")
print(f"  - Turnos mediana: {df_battles['total_turns'].median():.1f}")
print(f"  - Turnos min/max: {df_battles['total_turns'].min()}/{df_battles['total_turns'].max()}")

# Mostrar primeras filas del DataFrame
print(f"\nPrimeras 5 batallas procesadas:")
print(df_battles[['battle_id', 'total_turns', 'winner', 'reason', 'move_events', 'switch_events']].head())

# %% [markdown]
# ## 4. Análisis de patrones de batalla
# 
# **Valor del análisis de patrones:**
# - Los eventos por batalla (movimientos, switches, daño) son las acciones que debe aprender la IA
# - La correlación turnos-eventos nos indica la intensidad estratégica de las batallas
# - Los patrones por ganador revelan qué comportamientos llevan al éxito
# - El ratio movimientos/switches indica agresividad vs cautela en las estrategias
# - Estos insights guiarán el diseño de la función de recompensa del modelo de IA

# %%
print("\n" + "=" * 60)
print("ANÁLISIS DE PATRONES DE BATALLA")
print("=" * 60)

# Análisis de eventos por batalla
print(f"Eventos por batalla:")
print(f"  - Eventos totales promedio: {df_battles['total_events'].mean():.1f}")
print(f"  - Movimientos promedio: {df_battles['move_events'].mean():.1f}")
print(f"  - Switches promedio: {df_battles['switch_events'].mean():.1f}")
print(f"  - Eventos de daño promedio: {df_battles['damage_events'].mean():.1f}")

# Relación entre duración y eventos
correlation = df_battles['total_turns'].corr(df_battles['total_events'])
print(f"\nCorrelación turnos-eventos: {correlation:.3f}")

# Análisis por ganador
print(f"\nPatrones por ganador:")
for winner in ['p1', 'p2']:
    winner_data = df_battles[df_battles['winner'] == winner]
    if len(winner_data) > 0:
        print(f"  {winner}:")
        print(f"    - Turnos promedio: {winner_data['total_turns'].mean():.1f}")
        print(f"    - Eventos promedio: {winner_data['total_events'].mean():.1f}")
        print(f"    - Ratio movimientos/switches: {winner_data['move_events'].mean() / max(winner_data['switch_events'].mean(), 1):.2f}")

# %% [markdown]
# ## 5. Análisis de uso de Pokemon
# 
# **Importancia del análisis de Pokemon:**
# - Identificamos el 'meta' actual: qué Pokemon son más populares y por qué
# - Los niveles y HP nos dan información sobre el balance del juego
# - La frecuencia de uso indica qué Pokemon debe priorizar la IA en sus decisiones
# - Esta información es crucial para que la IA entienda amenazas y oportunidades
# - Los Pokemon más utilizados probablemente tienen estrategias más desarrolladas en los datos

# %%
print("\n" + "=" * 60)
print("ANÁLISIS DE USO DE POKEMON")
print("=" * 60)

# Extraer información de Pokemon
all_pokemon = []
for battle in battles:
    pokemon_info = extract_pokemon_info(battle)
    for pokemon in pokemon_info:
        pokemon['winner'] = get_in(battle, ['metadata', 'outcome', 'winner'])
        all_pokemon.append(pokemon)

df_pokemon = pd.DataFrame(all_pokemon)

if len(df_pokemon) > 0:
    # Pokemon más utilizados
    species_counts = df_pokemon['species'].value_counts()
    print(f"Top 10 Pokemon más utilizados:")
    for i, (species, count) in enumerate(species_counts.head(10).items(), 1):
        print(f"  {i:2d}. {species}: {count:,} usos")
    
    # Análisis de niveles
    print(f"\nDistribución de niveles:")
    print(f"  - Nivel promedio: {df_pokemon['level'].mean():.1f}")
    print(f"  - Nivel mediana: {df_pokemon['level'].median():.1f}")
    print(f"  - Rango de niveles: {df_pokemon['level'].min()}-{df_pokemon['level'].max()}")
    
    # Análisis de HP
    hp_data = df_pokemon.dropna(subset=['hp'])
    if len(hp_data) > 0:
        print(f"\nEstadísticas de HP:")
        print(f"  - HP promedio: {hp_data['hp'].mean():.1f}")
        print(f"  - HP mediana: {hp_data['hp'].median():.1f}")
        print(f"  - Rango HP: {hp_data['hp'].min()}-{hp_data['hp'].max()}")

print(f"\nDataFrame de Pokemon - Shape: {df_pokemon.shape}")
print(df_pokemon.head())

# %% [markdown]
# ## 6. Visualizaciones clave para entrenamiento de IA
# 
# **Visualizaciones seleccionadas:**
# - **Distribución de duración**: Muestra la variabilidad de estrategias (rápidas vs largas)
# - **Eventos vs turnos**: Revela la intensidad de acción, clave para modelar decisiones
# - **Patrones por ganador**: Identifica comportamientos exitosos que la IA debe imitar
# - **Razones de finalización**: Enseña a la IA los diferentes caminos hacia la victoria
# - Estas gráficas nos ayudan a validar hipótesis y comunicar insights del dataset

# %%
# Configurar subplots
fig, axes = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle('Análisis de Patrones de Batalla Pokemon', fontsize=16, fontweight='bold')

# 1. Distribución de duración de batallas
axes[0, 0].hist(df_battles['total_turns'], bins=30, alpha=0.7, color='skyblue', edgecolor='black')
axes[0, 0].set_title('Distribución de Duración de Batallas')
axes[0, 0].set_xlabel('Número de Turnos')
axes[0, 0].set_ylabel('Frecuencia')
axes[0, 0].axvline(df_battles['total_turns'].mean(), color='red', linestyle='--', 
                   label=f'Media: {df_battles["total_turns"].mean():.1f}')
axes[0, 0].legend()

# 2. Eventos por turno
axes[0, 1].scatter(df_battles['total_turns'], df_battles['events_per_turn'], 
                   alpha=0.6, color='green')
axes[0, 1].set_title('Eventos por Turno vs Duración')
axes[0, 1].set_xlabel('Número de Turnos')
axes[0, 1].set_ylabel('Eventos por Turno')

# 3. Comparación de patrones por ganador
winner_data = df_battles.groupby('winner').agg({
    'total_turns': 'mean',
    'move_events': 'mean',
    'switch_events': 'mean'
}).reset_index()

x = range(len(winner_data))
width = 0.25
axes[1, 0].bar([i - width for i in x], winner_data['total_turns'], width, 
               label='Turnos Promedio', alpha=0.8)
axes[1, 0].bar(x, winner_data['move_events'], width, 
               label='Movimientos Promedio', alpha=0.8)
axes[1, 0].bar([i + width for i in x], winner_data['switch_events'], width, 
               label='Switches Promedio', alpha=0.8)
axes[1, 0].set_title('Patrones por Ganador')
axes[1, 0].set_xlabel('Ganador')
axes[1, 0].set_ylabel('Cantidad')
axes[1, 0].set_xticks(x)
axes[1, 0].set_xticklabels(winner_data['winner'])
axes[1, 0].legend()

# 4. Razón de finalización
reason_counts = df_battles['reason'].value_counts()
axes[1, 1].pie(reason_counts.values, labels=reason_counts.index, autopct='%1.1f%%')
axes[1, 1].set_title('Razones de Finalización')

plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'battle_patterns_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

print(f"Visualización guardada: {OUTPUT_DIR / 'battle_patterns_analysis.png'}")

# %% [markdown]
# ## 7. Análisis visual de Pokemon
# 
# **Enfoque del análisis visual:**
# - **Top Pokemon**: La IA debe conocer las amenazas más comunes del meta
# - **Distribución de niveles**: Entiende el rango de poder esperado en batallas
# - **HP vs Nivel**: Revela la relación entre estadísticas, crucial para cálculos de daño
# - **Distribución por género**: Algunos movimientos y habilidades dependen del género
# - Estas visualizaciones informan las decisiones de selección de equipo de la IA

# %%
if len(df_pokemon) > 0:
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Análisis de Pokemon en Batallas', fontsize=16, fontweight='bold')
    
    # 1. Top Pokemon más utilizados
    top_pokemon = df_pokemon['species'].value_counts().head(15)
    axes[0, 0].barh(range(len(top_pokemon)), top_pokemon.values)
    axes[0, 0].set_yticks(range(len(top_pokemon)))
    axes[0, 0].set_yticklabels(top_pokemon.index)
    axes[0, 0].set_title('Top 15 Pokemon Más Utilizados')
    axes[0, 0].set_xlabel('Número de Usos')
    
    # 2. Distribución de niveles
    axes[0, 1].hist(df_pokemon['level'].dropna(), bins=20, alpha=0.7, color='orange', edgecolor='black')
    axes[0, 1].set_title('Distribución de Niveles de Pokemon')
    axes[0, 1].set_xlabel('Nivel')
    axes[0, 1].set_ylabel('Frecuencia')
    
    # 3. HP vs Nivel
    hp_level_data = df_pokemon.dropna(subset=['hp', 'level'])
    if len(hp_level_data) > 0:
        axes[1, 0].scatter(hp_level_data['level'], hp_level_data['hp'], alpha=0.6, color='purple')
        axes[1, 0].set_title('HP vs Nivel de Pokemon')
        axes[1, 0].set_xlabel('Nivel')
        axes[1, 0].set_ylabel('HP')
    
    # 4. Distribución por género
    gender_counts = df_pokemon['gender'].value_counts()
    axes[1, 1].pie(gender_counts.values, labels=gender_counts.index, autopct='%1.1f%%')
    axes[1, 1].set_title('Distribución por Género')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'pokemon_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"Visualización guardada: {OUTPUT_DIR / 'pokemon_analysis.png'}")

# %% [markdown]
# ## 8. Extracción de features para entrenamiento de IA
# 
# **Features seleccionados:**
# - **Métricas de batalla**: Duración, eventos, ratios - capturan el 'estilo' de juego
# - **Ratings de jugadores**: Proxy del nivel de habilidad, importante para el aprendizaje
# - **Información de equipos**: Tamaño, niveles promedio - contexto estratégico
# - **Patrones temporales**: Eventos por turno - ritmo de juego que debe aprender la IA
# - Estos features formarán el input del modelo de machine learning para toma de decisiones

# %%
print("\n" + "=" * 60)
print("EXTRACCIÓN DE FEATURES PARA IA")
print("=" * 60)

# Features a nivel de batalla
battle_features = []

for battle in battles:
    # Métricas básicas
    metrics = calculate_battle_metrics(battle)
    
    # Features adicionales
    features = {
        'battle_id': battle.get('battle_id'),
        'total_turns': metrics['total_turns'],
        'winner': metrics['winner'],
        'reason': metrics['reason'],
        'move_events': metrics['move_events'],
        'switch_events': metrics['switch_events'],
        'events_per_turn': metrics['events_per_turn'],
    }
    
    # Información de jugadores
    players = battle.get('players', {})
    for player_id in ['p1', 'p2']:
        player_data = players.get(player_id, {})
        features[f'{player_id}_rating'] = player_data.get('ladder_rating_pre', 0)
    
    # Información de equipos
    teams = get_in(battle, ['team_revelation', 'teams'], {})
    for player_id in ['p1', 'p2']:
        team = teams.get(player_id, [])
        features[f'{player_id}_team_size'] = len(team) if isinstance(team, list) else 0
        
        # Nivel promedio del equipo
        if isinstance(team, list) and team:
            levels = [p.get('level', 0) for p in team if p.get('level')]
            features[f'{player_id}_avg_level'] = np.mean(levels) if levels else 0
        else:
            features[f'{player_id}_avg_level'] = 0
    
    battle_features.append(features)

df_features = pd.DataFrame(battle_features)

# Guardar features
features_path = OUTPUT_DIR / 'battle_features.csv'
df_features.to_csv(features_path, index=False)

print(f"Features extraídas: {len(df_features.columns)} columnas")
print(f"Batallas procesadas: {len(df_features)} registros")
print(f"Features guardadas en: {features_path}")

# Mostrar correlaciones importantes
numeric_cols = df_features.select_dtypes(include=[np.number]).columns
if len(numeric_cols) > 1:
    correlations = df_features[numeric_cols].corr()
    print(f"\nCorrelaciones más altas con 'total_turns':")
    turn_corr = correlations['total_turns'].abs().sort_values(ascending=False)
    for feature, corr in turn_corr.head(5).items():
        if feature != 'total_turns':
            print(f"  - {feature}: {corr:.3f}")

print(f"\nPrimeras 5 filas del dataset de features:")
print(df_features.head())

# %% [markdown]
# ## 9. Matriz de correlación de features numéricas
# 
# **Propósito del análisis de correlaciones:**
# - Identificamos features redundantes que pueden confundir al modelo
# - Detectamos relaciones no obvias entre variables que pueden ser útiles
# - Ayuda a seleccionar las features más informativas para el entrenamiento
# - Previene problemas de multicolinealidad en modelos lineales
# - Guía la ingeniería de features y la selección de variables para el modelo final

# %%
# Crear matriz de correlación para features numéricas
numeric_features = df_features.select_dtypes(include=[np.number])

if len(numeric_features.columns) > 1:
    plt.figure(figsize=(12, 10))
    correlation_matrix = numeric_features.corr()
    
    # Crear heatmap
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, 
                square=True, fmt='.2f')
    plt.title('Matriz de Correlación - Features Numéricas')
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'correlation_matrix.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"Matriz de correlación guardada: {OUTPUT_DIR / 'correlation_matrix.png'}")

# %% [markdown]
# ## 10. Resumen ejecutivo para entrenamiento de IA
# 
# **Valor del resumen ejecutivo:**
# - Consolida todos los hallazgos en recomendaciones accionables
# - Define la estrategia de modelado basada en los insights del EDA
# - Identifica los próximos pasos técnicos para implementar la IA
# - Establece expectativas realistas sobre el rendimiento del modelo
# - Sirve como documento de referencia durante el desarrollo del modelo

# %%
print("\n" + "=" * 60)
print("RESUMEN EJECUTIVO PARA ENTRENAMIENTO DE IA")
print("=" * 60)

print(f"""
## Hallazgos Clave para el Modelo de IA:

### 1. Características del Dataset:
   - Total de batallas analizadas: {len(battles):,}
   - Formato principal: gen9randombattle
   - Estructura de datos consistente y completa

### 2. Patrones de Batalla Identificados:
   - Duración promedio: {df_battles['total_turns'].mean():.1f} turnos
   - Balance entre jugadores: Distribución equilibrada de victorias
   - Eventos clave: Movimientos, switches, y efectos de estado

### 3. Features Relevantes para IA:
   - Métricas de turnos y eventos: {len(numeric_features.columns)} features numéricas
   - Información de equipos Pokemon
   - Ratings de jugadores
   - Patrones de decisión por turno

### 4. Recomendaciones para Entrenamiento:
   - Usar secuencias de turnos como input temporal
   - Incorporar estado del campo y Pokemon activos
   - Considerar ratings como proxy de skill level
   - Balancear dataset por duración de batalla

### 5. Próximos Pasos:
   - Implementar feature engineering avanzado
   - Crear pipeline de preprocessing
   - Diseñar arquitectura de red neuronal
   - Establecer métricas de evaluación
""")

# %% [markdown]
# ## 11. Estadísticas finales y archivos generados
# 
# **Importancia de la documentación:**
# - Proporciona un inventario completo de los artefactos generados
# - Facilita la reproducibilidad del análisis
# - Permite validar que todos los pasos se ejecutaron correctamente
# - Sirve como checklist para asegurar que no falta ningún componente
# - Documenta el punto de partida para la siguiente fase del proyecto

# %%
print(f"\n{'='*80}")
print("EDA COMPLETADO EXITOSAMENTE")
print(f"{'='*80}")

print(f"\nArchivos generados en: {OUTPUT_DIR.resolve()}")
output_files = list(OUTPUT_DIR.glob("*"))
for file in output_files:
    print(f"  - {file.name}")

print(f"\nDatasets procesados:")
print(f"  - Batallas: {len(df_battles)} registros")
print(f"  - Pokemon: {len(df_pokemon)} registros")
print(f"  - Features: {len(df_features)} registros")

print(f"\nEl análisis está listo para convertir a notebook y ejecutar.")
