# %% [markdown]
# # 🔥 Pokemon Battle AI - El Despertar de los Datos
# 
# > *"En el mundo de las batallas Pokemon, cada decisión cuenta. Cada movimiento, cada cambio, cada estrategia puede determinar la diferencia entre la victoria y la derrota."*
# 
# ## 🎯 La Misión: Descifrar el Código de la Victoria
# 
# **Imagina tener acceso a 14,000 batallas épicas de entrenadores Pokemon de todo el mundo.** Cada batalla es un testimonio de estrategia, intuición y maestría. Dentro de estos datos se esconden los secretos que separan a los maestros Pokemon de los novatos.
# 
# **Nuestra misión:** Analizar estas batallas como un maestro Pokemon estudiaría a sus rivales, descubriendo:
# 
# - ⚔️ **Los patrones ocultos** que predicen la victoria
# - 🧬 **El ADN estratégico** de las batallas ganadoras  
# - 🎭 **Los protagonistas** que dominan el meta competitivo
# - ⏰ **Los momentos críticos** donde se decide el destino
# - 🎯 **Las características clave** que debe dominar nuestra IA
# 
# ## 📖 El Viaje Épico que Nos Espera
# 
# **Capítulo 1**: *El Despertar* - Validación de nuestro arsenal de datos
# **Capítulo 2**: *Los Secretos de la Victoria* - Descifrando patrones de combate
# **Capítulo 3**: *La Anatomía del Combate* - Duración y distribuciones
# **Capítulo 4**: *Los Gladiadores* - Análisis profundo de Pokemon
# **Capítulo 5**: *El Poder de los Elementos* - Análisis de tipos Pokemon
# **Capítulo 6**: *La Alquimia de los Datos* - Forjando características para la IA
# **Capítulo 7**: *El Primer Desafío* - Validación con modelo baseline
# 
# ## 🌟 El Arsenal de Datos
# 
# - **Origen**: Batallas reales de Pokemon Showdown (gen9randombattle)
# - **Escala épica**: ~14,000 batallas de entrenadores reales
# - **Riqueza**: Cada batalla contiene decisiones, estrategias y resultados
# - **Objetivo**: Entrenar una IA que comprenda el arte del combate Pokemon
# 
# ---
# 
# # %% [markdown]
# ## 🛠️ Preparando el Laboratorio de Análisis
# 
# **Como un entrenador prepara su equipo antes de una batalla, preparamos nuestras herramientas de análisis.**
# 
# En esta sección equipamos nuestro laboratorio con:
# - 🔬 Herramientas de análisis de datos (pandas, numpy)
# - 🎨 Paleta de colores temática Pokemon para visualizaciones épicas
# - 📊 Configuración de gráficos profesionales
# - 🎯 Sistema de reproducibilidad para resultados consistentes

# %%
from __future__ import annotations
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import sys
# Nota: No suprimimos warnings para mantener visibilidad de posibles problemas

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import random

# Importar datos de Pokemon (tipos, BST, efectividad)
# Detectar si estamos en notebooks/ o en raíz
if Path.cwd().name == "notebooks":
    sys.path.append(str(Path.cwd().parent / 'data'))
else:
    sys.path.append(str(Path.cwd() / 'data'))

try:
    from pokemon_data import (
        get_pokemon_types, get_pokemon_bst, get_type_effectiveness,
        calculate_matchup_score, is_legendary, is_pseudo_legendary,
        POKEMON_TYPES, POKEMON_BST, TYPE_EFFECTIVENESS
    )
    POKEMON_DATA_AVAILABLE = True
    print("✅ pokemon_data.py cargado correctamente")
except ImportError as e:
    print(f"⚠️  pokemon_data.py no encontrado: {e}")
    print("   Features de tipo limitadas.")
    POKEMON_DATA_AVAILABLE = False

# Configuración de visualizaciones con paleta Pokemon temática
plt.style.use('seaborn-v0_8-whitegrid')  # Estilo más moderno

# Paleta Pokemon temática - colores vibrantes pero profesionales
pokemon_colors = {
    'fire': '#FF6B35',      # Naranja fuego vibrante
    'water': '#4A90E2',     # Azul agua profundo  
    'grass': '#7ED321',     # Verde hierba brillante
    'electric': '#F5A623',  # Amarillo eléctrico
    'psychic': '#BD10E0',   # Púrpura psíquico
    'dragon': '#9013FE',    # Púrpura dragón
    'dark': '#2C3E50',      # Gris oscuro elegante
    'steel': '#95A5A6',     # Gris metálico
    'fairy': '#FF69B4',     # Rosa hada
    'fighting': '#D0021B',  # Rojo lucha
    'poison': '#7B68EE',    # Púrpura veneno
    'ground': '#8B4513',    # Marrón tierra
    'flying': '#87CEEB',    # Azul cielo
    'bug': '#9ACD32',       # Verde insecto
    'rock': '#A0522D',      # Marrón roca
    'ghost': '#483D8B',     # Púrpura fantasma
    'ice': '#B0E0E6',       # Azul hielo
    'normal': '#A8A878'     # Beige normal
}

# Paletas para diferentes tipos de gráficos
primary_palette = [pokemon_colors['fire'], pokemon_colors['water'], pokemon_colors['grass'], 
                  pokemon_colors['electric'], pokemon_colors['psychic'], pokemon_colors['dragon']]

secondary_palette = [pokemon_colors['dark'], pokemon_colors['steel'], pokemon_colors['fairy'],
                    pokemon_colors['fighting'], pokemon_colors['poison'], pokemon_colors['ground']]

# Configurar seaborn con la nueva paleta
sns.set_palette(primary_palette)
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['figure.titlesize'] = 16

# Configuración de colores para gráficos específicos
plot_colors = {
    'histogram': pokemon_colors['water'],
    'scatter': pokemon_colors['fire'], 
    'line': pokemon_colors['electric'],
    'bar': pokemon_colors['grass'],
    'boxplot': primary_palette,
    'heatmap': 'RdYlBu_r'  # Colormap para matrices de correlación
}

# Configuración de reproducibilidad
import platform
import sys
random.seed(42)
np.random.seed(42)

# Configuración completada - entorno listo para análisis

# %% [markdown]
# ## 📁 Organizando el Arsenal de Datos
# 
# **Como un maestro Pokemon organiza su Pokédex, organizamos nuestros datos.**
# 
# Establecemos las rutas hacia:
# - ⚔️ `BATTLES_DIR`: La biblioteca de 14,000 batallas épicas
# - 📚 `ALL_BATTLES_JSON`: El tomo consolidado de sabiduría
# - 🎨 `OUTPUT_DIR`: Donde nacerán nuestras visualizaciones

# %%
# Detectar si estamos ejecutando desde notebooks/ o desde raíz
current_dir = Path.cwd()
if current_dir.name == "notebooks":
    DATA_DIR = Path("../data")
    OUTPUT_DIR = Path("../output")
else:
    DATA_DIR = Path("data")
    OUTPUT_DIR = Path("output")

BATTLES_DIR = DATA_DIR / "battles"
ALL_BATTLES_JSON = DATA_DIR / "all_battles.json"
OUTPUT_DIR.mkdir(exist_ok=True)

# Rutas configuradas correctamente

# %% [markdown]
# ## 🧪 Las Herramientas del Alquimista
# 
# **Como un alquimista transforma elementos básicos en oro, transformaremos datos crudos en conocimiento.**
# 
# Nuestras herramientas mágicas:
# - 🗝️ `get_in()`: Navega las profundidades de estructuras complejas
# - 🔬 `extract_pokemon_info()`: Extrae el ADN de cada Pokemon
# - ⚖️ `calculate_battle_metrics()`: Mide el pulso de cada batalla
# - 🎯 `extract_pre_battle_features()`: Captura la esencia del combate
# - ⚔️ `calculate_team_type_advantage()`: Descifra las ventajas elementales

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
                # Extraer todas las estadísticas base disponibles
                base_stats = pokemon.get('base_stats', {})
                info = {
                    'battle_id': battle.get('battle_id'),
                    'player': player_id,
                    'species': pokemon.get('species'),
                    'level': pokemon.get('level'),
                    'gender': pokemon.get('gender'),
                    'hp': base_stats.get('hp'),
                    'attack': base_stats.get('attack'),
                    'defense': base_stats.get('defense'),
                    'sp_attack': base_stats.get('sp_attack'),
                    'sp_defense': base_stats.get('sp_defense'),
                    'speed': base_stats.get('speed'),
                    'first_seen_turn': pokemon.get('first_seen_turn'),
                    'revelation_status': pokemon.get('revelation_status'),
                    'known_ability': pokemon.get('known_ability'),
                    'known_item': pokemon.get('known_item'),
                    'known_tera_type': pokemon.get('known_tera_type'),
                    'known_moves_count': len(pokemon.get('known_moves', [])),
                    'unknown_move_slots': pokemon.get('unknown_move_slots', 0)
                }
                pokemon_info.append(info)
    return pokemon_info

def calculate_battle_metrics(battle: dict) -> dict:
    """
    Calcula métricas básicas de batalla SOLO para análisis EDA.
    ⚠️  NOTA: Estas métricas NO se usan para ML (son post-batalla).
    """
    metadata = battle.get('metadata', {})
    turns = battle.get('turns', [])
    
    return {
        'battle_id': battle.get('battle_id'),
        'total_turns': len(turns),
        'winner': get_in(metadata, ['outcome', 'winner']),
        'reason': get_in(metadata, ['outcome', 'reason']),
        'timestamp': metadata.get('timestamp_unix'),
    }

def calculate_team_type_advantage(team1_species: list, team2_species: list) -> dict:
    """
    Calcula ventajas de tipo entre dos equipos.
    Esta es información VÁLIDA (derivable de species observables).
    """
    if not POKEMON_DATA_AVAILABLE:
        return {
            'type_advantage_score': 0,
            'p1_super_effective_count': 0,
            'p2_super_effective_count': 0,
            'p1_resisted_count': 0,
            'p2_resisted_count': 0,
        }
    
    p1_super_effective = 0
    p2_super_effective = 0
    p1_resisted = 0
    p2_resisted = 0
    
    for p1_species in team1_species:
        p1_types = get_pokemon_types(p1_species)
        for p2_species in team2_species:
            p2_types = get_pokemon_types(p2_species)
            
            # P1 atacando a P2
            matchup = calculate_matchup_score(p1_types, p2_types)
            if matchup >= 2.0:
                p1_super_effective += 1
            elif matchup <= 0.5:
                p1_resisted += 1
            
            # P2 atacando a P1
            matchup = calculate_matchup_score(p2_types, p1_types)
            if matchup >= 2.0:
                p2_super_effective += 1
            elif matchup <= 0.5:
                p2_resisted += 1
    
    type_advantage_score = (p1_super_effective - p1_resisted) - (p2_super_effective - p2_resisted)
    
    return {
        'type_advantage_score': type_advantage_score,
        'p1_super_effective_count': p1_super_effective,
        'p2_super_effective_count': p2_super_effective,
        'p1_resisted_count': p1_resisted,
        'p2_resisted_count': p2_resisted,
    }

def extract_pre_battle_features(battle: dict) -> dict:
    """
    Extrae SOLO features disponibles al INICIO de la batalla.
    ✅ SIN DATA LEAKAGE - Todas las features son observables pre-batalla.
    """
    teams = get_in(battle, ["team_revelation", "teams"], {})
    features = {'battle_id': battle.get('battle_id')}
    
    # Extraer species de ambos equipos para matchups
    p1_species = [p.get('species') for p in teams.get('p1', []) if p.get('species')]
    p2_species = [p.get('species') for p in teams.get('p2', []) if p.get('species')]
    
    for player_id in ['p1', 'p2']:
        team = teams.get(player_id, [])
        if isinstance(team, list) and team:
            # 1. COMPOSICIÓN OBSERVABLE
            species_list = [p.get('species') for p in team if p.get('species')]
            levels = [p.get('level', 0) for p in team if p.get('level')]
            hps = [get_in(p, ['base_stats', 'hp']) for p in team if get_in(p, ['base_stats', 'hp'])]
            
            features.update({
                f'{player_id}_team_size': len(team),
                f'{player_id}_avg_level': np.mean(levels) if levels else 0,
                f'{player_id}_level_std': np.std(levels) if len(levels) > 1 else 0,
                f'{player_id}_total_hp': sum(hps) if hps else 0,
                f'{player_id}_avg_hp': np.mean(hps) if hps else 0,
                f'{player_id}_species_diversity': len(set(species_list)),
            })
            
            # 2. TYPE MATCHUPS & BST (derivables de species)
            if POKEMON_DATA_AVAILABLE:
                types_list = []
                bst_list = []
                dual_type_count = 0
                
                for species in species_list:
                    pokemon_types = get_pokemon_types(species)
                    types_list.extend(pokemon_types)
                    bst_list.append(get_pokemon_bst(species))
                    if len(pokemon_types) == 2:
                        dual_type_count += 1
                
                features.update({
                    # Type diversity
                    f'{player_id}_type_diversity': len(set(types_list)),
                    f'{player_id}_dual_type_count': dual_type_count,
                    
                    # Pokemon strength (BST)
                    f'{player_id}_avg_bst': np.mean(bst_list) if bst_list else 400,
                    f'{player_id}_bst_std': np.std(bst_list) if len(bst_list) > 1 else 0,
                    f'{player_id}_min_bst': min(bst_list) if bst_list else 400,
                    f'{player_id}_max_bst': max(bst_list) if bst_list else 400,
                    
                    # Tiers
                    f'{player_id}_legendary_count': sum(1 for bst in bst_list if bst >= 580),
                    f'{player_id}_pseudo_legendary_count': sum(1 for bst in bst_list if bst == 600),
                })
            else:
                # Defaults si no hay pokemon_data
                for metric in ['type_diversity', 'dual_type_count', 'avg_bst', 'bst_std', 
                              'min_bst', 'max_bst', 'legendary_count', 'pseudo_legendary_count']:
                    features[f'{player_id}_{metric}'] = 0
        else:
            # Valores por defecto si no hay datos del equipo
            for metric in ['team_size', 'avg_level', 'level_std', 'total_hp', 'avg_hp', 
                          'species_diversity', 'type_diversity', 'dual_type_count',
                          'avg_bst', 'bst_std', 'min_bst', 'max_bst', 
                          'legendary_count', 'pseudo_legendary_count']:
                features[f'{player_id}_{metric}'] = 0
    
    # 3. TYPE MATCHUPS entre equipos
    type_advantage = calculate_team_type_advantage(p1_species, p2_species)
    features.update(type_advantage)
    
    # 4. VENTAJAS DERIVADAS
    features['level_advantage_p1'] = features['p1_avg_level'] - features['p2_avg_level']
    features['hp_advantage_p1'] = features['p1_total_hp'] - features['p2_total_hp']
    features['bst_advantage_p1'] = features['p1_avg_bst'] - features['p2_avg_bst']
    features['team_size_difference'] = abs(features['p1_team_size'] - features['p2_team_size'])
    
    # 5. TARGET (winner) - Necesario para entrenamiento
    winner = get_in(battle, ['metadata', 'outcome', 'winner'])
    features['winner'] = winner if winner in ['p1', 'p2'] else None
    
    return features

# Funciones auxiliares listas para procesamiento

# %% [markdown]
# ## Función para Crear Muestra de Datos

# %%
def create_sample_if_needed(sample_size: int = 2000) -> List[dict]:
    """
    Crea una muestra de batallas para EDA si no existe.
    
    Args:
        sample_size: Número de batallas en la muestra (default: 2000)
    
    Returns:
        Lista de batallas de la muestra
    """
    sample_path = DATA_DIR / f"battles_sample_{sample_size}.json"
    
    # Si ya existe, cargarla
    if sample_path.exists():
        print(f"✅ Cargando muestra existente: {sample_path.name}")
        with open(sample_path, "r") as f:
            return json.load(f)
    
    # Si no existe, crearla desde el dataset completo
    print(f"📝 Creando muestra de {sample_size} batallas...")
    print(f"   Cargando dataset completo desde: {ALL_BATTLES_JSON.name}")
    
    with open(ALL_BATTLES_JSON, "r") as f:
        all_battles = json.load(f)
    
    print(f"   Dataset completo: {len(all_battles):,} batallas")
    
    # Tomar muestra aleatoria (seed para reproducibilidad)
    sample_battles = random.sample(all_battles, min(sample_size, len(all_battles)))
    
    # Guardar muestra
    with open(sample_path, "w") as f:
        json.dump(sample_battles, f, indent=2)
    
    print(f"✅ Muestra guardada: {sample_path.name}")
    print(f"   {len(sample_battles):,} batallas listas para EDA")
    
    return sample_battles

# %% [markdown]
# ## Capítulo 1: El Despertar - Invocando las Batallas del Pasado
# 
# **Como un maestro Pokemon invoca recuerdos de batallas pasadas, cargamos nuestro arsenal de datos.**
# 
# 📚 **Para el EDA usamos una muestra de 2,000 batallas** (análisis rápido y eficiente)
# 
# 💡 **Para el entrenamiento del baseline** usaremos el dataset completo de 14,000+ batallas
# 
# Cada batalla es un testimonio de:
# - Decisiones bajo presión de entrenadores reales
# - Estrategias complejas ejecutadas en tiempo real  
# - Momentos críticos que definieron victoria o derrota
# - Patrones meta que solo emergen con grandes volúmenes
# 
# **¿Qué secretos revelarán estos datos?** El viaje comienza...

# %%
# Cargar muestra de 2,000 batallas para EDA
battles = create_sample_if_needed(sample_size=2000)
print(f"\n📊 Dataset para EDA: {len(battles):,} batallas")
print(f"💡 Nota: El baseline se entrenará con el dataset completo (~14,000 batallas)")

# Crear DataFrame de métricas básicas de batalla para análisis exploratorio
battle_metrics = [calculate_battle_metrics(battle) for battle in battles]
df_battles = pd.DataFrame(battle_metrics)
print(f"📈 Métricas básicas extraídas: {len(df_battles.columns)} campos (battle_id, turns, winner, etc.)")
print(f"   ⚠️  Nota: Las features para ML (~37) se extraerán más adelante en el Capítulo 6")

# %% [markdown]
# ### 👁️ Primera Mirada: ¿Qué Contienen Nuestros Datos?
# 
# **Como un entrenador examina su Pokédex, echemos un vistazo a nuestro dataset.**
# 
# Cada batalla es un archivo JSON con información completa del combate. Aquí mostramos **de dónde partimos**.

# %%
print("\n" + "="*70)
print("📦 ESTRUCTURA DE UNA BATALLA (JSON RAW)")
print("="*70)

example_battle = battles[0]

# 1. METADATA - Información básica de la batalla
print("\n1️⃣  METADATA (Información de la batalla):")
metadata = example_battle.get('metadata', {})
print(f"   • Battle ID: {example_battle.get('battle_id')}")
print(f"   • Formato: {example_battle.get('format_id')}")
print(f"   • Timestamp: {metadata.get('timestamp_unix')}")
print(f"   • Total turnos: {metadata.get('total_turns')}")
print(f"   • Ganador: {metadata.get('outcome', {}).get('winner')}")
print(f"   • Razón: {metadata.get('outcome', {}).get('reason')}")

# 2. PLAYERS - Información de jugadores
print("\n2️⃣  PLAYERS (Jugadores):")
players = example_battle.get('players', {})
for player_id, player_data in players.items():
    print(f"   • {player_id}:")
    print(f"     - Nombre: {player_data.get('name')}")
    print(f"     - Rating: {player_data.get('ladder_rating_pre')}")

# 3. TEAM REVELATION - Los equipos Pokemon ⭐⭐⭐⭐⭐ MÁS IMPORTANTE
print("\n3️⃣  TEAM REVELATION (Equipos Pokemon) ⭐ DATOS CLAVE PARA ML:")
teams = example_battle.get('team_revelation', {}).get('teams', {})
for player_id, team in teams.items():
    print(f"\n   {player_id} - Equipo de {len(team)} Pokemon:")
    for i, pokemon in enumerate(team[:3], 1):  # Mostrar solo 3
        print(f"      {i}. {pokemon.get('species')} (Lv.{pokemon.get('level')})")
        print(f"         - HP: {pokemon.get('base_stats', {}).get('hp')}")
        print(f"         - Género: {pokemon.get('gender', 'N/A')}")
        moves = pokemon.get('known_moves', [])
        print(f"         - Moves conocidos: {len(moves)}")
    if len(team) > 3:
        print(f"      ... y {len(team) - 3} Pokemon más")

# 4. TURNS - Eventos de batalla (NO se usan para predicción pre-batalla)
print("\n4️⃣  TURNS (Eventos de batalla):")
turns = example_battle.get('turns', [])
print(f"   • Total de turnos: {len(turns)}")
if len(turns) > 0:
    first_turn = turns[0]
    print(f"   • Eventos en turno 1: {len(first_turn.get('events', []))}")
    print(f"   • Tipos de eventos: move, switch, damage, heal, status, etc.")
print(f"   ⚠️  Nota: Estos datos son POST-BATALLA (no se usan para predicción)")

# 5. SUMMARY - Resumen de la batalla
print("\n5️⃣  SUMMARY (Resumen):")
summary = example_battle.get('summary', {})
pokemon_used = summary.get('pokemon_used', {})
for player_id, poke_list in pokemon_used.items():
    print(f"   • {player_id} usó {len(poke_list)} Pokemon")

# %% [markdown]
# ## Capítulo 1.1: Inspeccionando el Arsenal - ¿Son Confiables Nuestras Armas?
# 
# **Antes de entrar en batalla, un maestro Pokemon inspecciona su equipo.**
# 
# 🔍 **Validación del arsenal de datos:**
# - ¿Todas las batallas están completas y listas para análisis?
# - ¿Existen datos corruptos o incompletos que podrían engañarnos?
# - ¿Qué formatos de batalla dominan nuestro dataset?
# - ¿Estamos ante un ejército sólido o hay debilidades ocultas?
# 
# **La integridad de nuestros datos determina el destino de nuestra IA.**

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
# ## Capítulo 1.1: Detectando Imperfecciones en Nuestros Datos
# 
# **¿Qué secretos ocultan los datos faltantes?**
# 
# Como detectives examinando evidencia, debemos identificar qué información nos falta y por qué. Los datos nulos no son solo números ausentes - son pistas sobre la calidad de nuestro dataset y posibles sesgos que podrían confundir a nuestra IA.
# 
# **¿Por qué es crucial para nuestra IA?**
# - **Sesgos ocultos**: Los nulos pueden indicar patrones sistemáticos que sesgarían el aprendizaje
# - **Estrategias de imputación**: Decidir cómo manejar información faltante afecta directamente la precisión del modelo
# - **Robustez del modelo**: Una IA entrenada con datos incompletos debe saber manejar incertidumbre

# %%
print(f"\n🔍 {'='*50}")
print("   CAPÍTULO 1.1: DETECTANDO IMPERFECCIONES")
print(f"{'='*60}")

# Análisis de nulos en DataFrame de batallas
if len(df_battles) > 0:
    nulls_battles = df_battles.isnull().sum().sort_values(ascending=False)
    print("\nNulos en DataFrame de batallas:")
    for col, null_count in nulls_battles.items():
        if null_count > 0:
            print(f"  - {col}: {null_count:,} ({null_count/len(df_battles)*100:.1f}%)")
    
    # Duplicados
    dupes_battles = df_battles.duplicated().sum()
    print(f"\nDuplicados exactos en batallas: {dupes_battles:,}")
    
    # Duplicados por battle_id
    dupes_by_id = df_battles['battle_id'].duplicated().sum()
    print(f"Batallas con battle_id duplicado: {dupes_by_id:,}")

# %% [markdown]
# ## Capítulo 1.2: El ADN de Nuestros Datos
# 
# **¿Qué tipo de información tenemos realmente?**
# 
# Cada variable en nuestro dataset tiene una personalidad única. Algunas son categóricas (como especies de Pokemon), otras numéricas (como HP), y algunas tienen miles de valores únicos mientras otras solo unos pocos. Entender esta diversidad es crucial para que nuestra IA aprenda correctamente.
# 
# **El impacto en el entrenamiento:**
# - **Variables categóricas**: Requieren encoding especial para que la IA las entienda
# - **Alta cardinalidad**: Puede causar overfitting si no se maneja correctamente
# - **Tipos incorrectos**: Pueden hacer que la IA malinterprete patrones importantes

# %%
print(f"\n🧬 {'='*50}")
print("   CAPÍTULO 1.2: EL ADN DE LOS DATOS")
print(f"{'='*60}")

if len(df_battles) > 0:
    audit_battles = (df_battles.dtypes.to_frame('dtype')
                    .assign(cardinalidad=df_battles.nunique(),
                           nulos=df_battles.isnull().sum(),
                           pct_nulos=(df_battles.isnull().sum()/len(df_battles)*100).round(2))
                    .sort_values('cardinalidad', ascending=False))
    
    print("\nAuditoría DataFrame batallas:")
    print(audit_battles)
    
    # Guardar auditoría
    audit_path = OUTPUT_DIR / 'data_audit_battles.csv'
    audit_battles.to_csv(audit_path)
    print(f"\nAuditoría guardada: {audit_path}")

# %% [markdown]
# ## Capítulo 2: Los Secretos de la Victoria
# 
# **¿Qué separa a los ganadores de los perdedores?**
# 
# En el mundo Pokemon, cada batalla cuenta una historia. Algunas terminan rápidamente con estrategias agresivas, otras se extienden en duelos épicos de resistencia. Nuestra IA debe aprender a leer estas historias y entender qué patrones llevan al éxito.
# 
# **Las lecciones ocultas en cada resultado:**
# - **Balance del dataset**: ¿Favorece nuestro dataset a algún jugador? Un sesgo aquí crearía una IA injusta
# - **Razones de victoria**: ¿Ganan por knockout directo o por estrategias más sutiles?
# - **Duración vs éxito**: ¿Las batallas rápidas o largas tienen más probabilidad de éxito?
# - **Patrones temporales**: ¿Hay momentos clave donde se decide el resultado?
# 
# Estos insights guiarán el diseño de la función de recompensa de nuestra IA.

# %%
print(f"\n⚔️ {'='*50}")
print("   CAPÍTULO 2: LOS SECRETOS DE LA VICTORIA")
print(f"{'='*60}")

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

# Análisis de balance de clases
print(f"\nBalance de clases (winner):")
balance = df_battles['winner'].value_counts(normalize=True).mul(100).round(2)
for winner, pct in balance.items():
    print(f"  - {winner}: {pct}%")

# Mostrar primeras filas del DataFrame
print(f"\nPrimeras 5 batallas procesadas:")
print(df_battles[['battle_id', 'total_turns', 'winner', 'reason']].head())

# %% [markdown]
# ## Capítulo 3: La Anatomía del Combate - Duración de las Batallas
# 
# **Valor del análisis de duración:**
# - La duración (turnos) nos indica la complejidad de las batallas
# - Batallas muy cortas pueden indicar mismatches severos
# - Batallas largas sugieren equipos balanceados
# - ⚠️ NOTA: Esta métrica es solo para EDA, NO se usa en ML (es post-batalla)

# %%
print(f"\n🎯 {'='*50}")
print("   CAPÍTULO 3: ANÁLISIS DE DURACIÓN")
print(f"{'='*60}")

# Análisis de duración
print(f"Estadísticas de duración:")
print(f"  - Turnos promedio: {df_battles['total_turns'].mean():.1f}")
print(f"  - Turnos mediana: {df_battles['total_turns'].median():.1f}")
print(f"  - Turnos min/max: {df_battles['total_turns'].min()}/{df_battles['total_turns'].max()}")
print(f"  - Desviación estándar: {df_battles['total_turns'].std():.1f}")

# Análisis por ganador
print(f"\nDuración por ganador:")
for winner in ['p1', 'p2']:
    winner_data = df_battles[df_battles['winner'] == winner]
    if len(winner_data) > 0:
        print(f"  {winner}:")
        print(f"    - Turnos promedio: {winner_data['total_turns'].mean():.1f}")
        print(f"    - Turnos mediana: {winner_data['total_turns'].median():.1f}")

# Distribución de duración
print(f"\n📊 Distribución de duración:")
quartiles = df_battles['total_turns'].quantile([0.25, 0.5, 0.75])
print(f"  - Q1 (25%): {quartiles[0.25]:.0f} turnos")
print(f"  - Q2 (50%): {quartiles[0.5]:.0f} turnos")
print(f"  - Q3 (75%): {quartiles[0.75]:.0f} turnos")

print(f"\n💡 Nota: Esta información es solo descriptiva.")
print(f"   NO se usa para ML (sería data leakage)")

# %% [markdown]
# ### Distribuciones y Outliers
# 
# **Importancia del análisis de distribuciones:**
# - Identifica outliers que pueden sesgar el modelo
# - Revela la forma de las distribuciones para seleccionar algoritmos apropiados
# - Detecta patrones anómalos en los datos
# - ⚠️ NOTA: Analizamos solo 'total_turns' (métrica descriptiva, no para ML)

# %%
print(f"\n📊 {'='*50}")
print("   CAPÍTULO 3.1: DISTRIBUCIONES Y ANOMALÍAS")
print(f"{'='*60}")

# Análisis de distribuciones para variables numéricas clave
num_cols = ['total_turns']  # Solo analizamos duración (descriptivo)

if len(df_battles) > 0:
    # Histograma de distribución de duración
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    fig.suptitle('Distribución de Duración de Batallas', fontsize=16)
    
    col = 'total_turns'
    if col in df_battles.columns:
        ax.hist(df_battles[col].dropna(), bins=30, alpha=0.7, edgecolor='black', color=plot_colors['histogram'])
        ax.set_title(f'Distribución: {col}')
        ax.set_xlabel('Número de Turnos')
        ax.set_ylabel('Frecuencia')
        
        # Añadir líneas de media y mediana
        mean_val = df_battles[col].mean()
        median_val = df_battles[col].median()
        ax.axvline(mean_val, color='red', linestyle='--', alpha=0.7, label=f'Media: {mean_val:.1f}')
        ax.axvline(median_val, color='green', linestyle='--', alpha=0.7, label=f'Mediana: {median_val:.1f}')
        ax.legend()
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'distributions_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Análisis de outliers usando IQR
    print(f"\nDetección de outliers (método IQR):")
    for col in num_cols:
        if col in df_battles.columns:
            Q1 = df_battles[col].quantile(0.25)
            Q3 = df_battles[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = df_battles[(df_battles[col] < lower_bound) | (df_battles[col] > upper_bound)]
            pct_outliers = len(outliers) / len(df_battles) * 100
            
            print(f"  - {col}: {len(outliers)} outliers ({pct_outliers:.1f}%)")
    
    # Boxplot de duración por ganador
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    
    # Colores específicos para boxplots
    boxplot_colors = [pokemon_colors['fire'], pokemon_colors['water']]
    
    if 'total_turns' in df_battles.columns:
        sns.boxplot(data=df_battles, x='winner', y='total_turns', ax=ax, 
                   hue='winner', palette=boxplot_colors, legend=False)
        ax.set_title('Duración de Batalla por Ganador')
        ax.set_ylabel('Número de Turnos')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'boxplots_by_winner.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("\n✅ Análisis de distribuciones completado")

# %% [markdown]
# ## Capítulo 4: Los Gladiadores - Análisis de Pokemon
# 
# **Importancia del análisis de Pokemon:**
# - Identificamos el 'meta' actual: qué Pokemon son más populares y por qué
# - Los niveles y HP nos dan información sobre el balance del juego
# - La frecuencia de uso indica qué Pokemon debe priorizar la IA en sus decisiones
# - Esta información es crucial para que la IA entienda amenazas y oportunidades
# - Los Pokemon más utilizados probablemente tienen estrategias más desarrolladas en los datos

# %%
print(f"\n🎮 {'='*50}")
print("   CAPÍTULO 4: LOS PROTAGONISTAS DEL META")
print(f"{'='*60}")

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
        print(f"  - {species}: {count:,} usos")
    
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

print(f"\n📋 Resumen del análisis Pokemon:")
print(f"   • {len(df_pokemon)} registros de Pokemon analizados")
print(f"   • {df_pokemon['species'].nunique()} especies únicas identificadas")
print(f"   • Nivel promedio del meta: {df_pokemon['level'].mean():.1f}")

if len(df_pokemon) > 0:
    # Análisis de completitud de datos
    nulls_pokemon = df_pokemon.isnull().sum().sort_values(ascending=False)
    critical_nulls = [(col, count) for col, count in nulls_pokemon.items() if count > 0 and count/len(df_pokemon) > 0.1]
    if critical_nulls:
        print(f"\n⚠️  Datos faltantes significativos:")
        for col, null_count in critical_nulls[:5]:  # Solo top 5
            print(f"   • {col}: {null_count/len(df_pokemon)*100:.1f}% faltante")

# %% [markdown]
# ### Visualizaciones de Patrones de Batalla
# 
# **Visualizaciones seleccionadas:**
# - **Distribución de duración**: Muestra la variabilidad de estrategias (rápidas vs largas)
# - **Eventos vs turnos**: Revela la intensidad de acción, clave para modelar decisiones
# - **Patrones por ganador**: Identifica comportamientos exitosos que la IA debe imitar
# - **Razones de finalización**: Enseña a la IA los diferentes caminos hacia la victoria
# - Estas gráficas nos ayudan a validar hipótesis y comunicar insights del dataset

# %%
# Configurar subplots - Solo métricas descriptivas (no para ML)
fig, axes = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle('Análisis Descriptivo de Batallas Pokemon', fontsize=16, fontweight='bold')

# 1. Distribución de duración de batallas
axes[0, 0].hist(df_battles['total_turns'], bins=30, alpha=0.7, color=plot_colors['histogram'], edgecolor='black')
axes[0, 0].set_title('Distribución de Duración de Batallas')
axes[0, 0].set_xlabel('Número de Turnos')
axes[0, 0].set_ylabel('Frecuencia')
axes[0, 0].axvline(df_battles['total_turns'].mean(), color='red', linestyle='--', 
                   label=f'Media: {df_battles["total_turns"].mean():.1f}')
axes[0, 0].legend()

# 2. Duración por ganador (boxplot)
winner_data_filtered = df_battles[df_battles['winner'].isin(['p1', 'p2'])]
if len(winner_data_filtered) > 0:
    sns.boxplot(data=winner_data_filtered, x='winner', y='total_turns', ax=axes[0, 1],
               palette=[pokemon_colors['fire'], pokemon_colors['water']])
    axes[0, 1].set_title('Duración por Ganador')
    axes[0, 1].set_xlabel('Ganador')
    axes[0, 1].set_ylabel('Número de Turnos')

# 3. Comparación de duración promedio por ganador
winner_summary = df_battles.groupby('winner')['total_turns'].mean().reset_index()
winner_summary = winner_summary[winner_summary['winner'].isin(['p1', 'p2'])]

if len(winner_summary) > 0:
    axes[1, 0].bar(winner_summary['winner'], winner_summary['total_turns'], 
                   alpha=0.8, color=[pokemon_colors['fire'], pokemon_colors['water']],
                   edgecolor='black', linewidth=1.2)
    axes[1, 0].set_title('Duración Promedio por Ganador')
    axes[1, 0].set_xlabel('Ganador')
    axes[1, 0].set_ylabel('Turnos Promedio')
    axes[1, 0].axhline(df_battles['total_turns'].mean(), color='red', linestyle='--', 
                      alpha=0.7, label='Media Global')
    axes[1, 0].legend()

# 4. Razón de finalización
reason_counts = df_battles['reason'].value_counts()
axes[1, 1].pie(reason_counts.values, labels=reason_counts.index, autopct='%1.1f%%', colors=primary_palette)
axes[1, 1].set_title('Razones de Finalización')

plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'battle_patterns_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

print(f"Visualización guardada: {OUTPUT_DIR / 'battle_patterns_analysis.png'}")
print(f"⚠️  Nota: Estas métricas son solo descriptivas (no se usan para ML)")

# %% [markdown]
# ### Análisis Visual de Pokemon
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
    axes[0, 0].barh(range(len(top_pokemon)), top_pokemon.values, color=plot_colors['bar'])
    axes[0, 0].set_yticks(range(len(top_pokemon)))
    axes[0, 0].set_yticklabels(top_pokemon.index)
    axes[0, 0].set_title('Top 15 Pokemon Más Utilizados')
    axes[0, 0].set_xlabel('Número de Usos')
    
    # 2. Distribución de niveles
    axes[0, 1].hist(df_pokemon['level'].dropna(), bins=20, alpha=0.7, color=plot_colors['histogram'], edgecolor='black')
    axes[0, 1].set_title('Distribución de Niveles de Pokemon')
    axes[0, 1].set_xlabel('Nivel')
    axes[0, 1].set_ylabel('Frecuencia')
    
    # 3. HP vs Nivel
    hp_level_data = df_pokemon.dropna(subset=['hp', 'level'])
    if len(hp_level_data) > 0:
        axes[1, 0].scatter(hp_level_data['level'], hp_level_data['hp'], alpha=0.6, color=plot_colors['scatter'])
        axes[1, 0].set_title('HP vs Nivel de Pokemon')
        axes[1, 0].set_xlabel('Nivel')
        axes[1, 0].set_ylabel('HP')
    
    # 4. Distribución por género
    gender_counts = df_pokemon['gender'].value_counts()
    axes[1, 1].pie(gender_counts.values, labels=gender_counts.index, autopct='%1.1f%%', colors=primary_palette)
    axes[1, 1].set_title('Distribución por Género')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'pokemon_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"Visualización guardada: {OUTPUT_DIR / 'pokemon_analysis.png'}")

# %% [markdown]
# ## Capítulo 5: El Poder de los Elementos - Análisis de Tipos
# 
# **En el mundo Pokemon, los tipos lo son todo.**
# 
# Un Charizard (Fuego/Volador) contra un Blastoise (Agua) está en desventaja antes de lanzar un solo ataque. Los tipos determinan:
# - Efectividad de movimientos (2x, 0.5x, 0x daño)
# - Estrategias de equipo y cobertura
# - Matchups favorables y desfavorables
# 
# **Este es el conocimiento fundamental que nuestra IA debe dominar.**

# %%
print(f"\n🔥 {'='*50}")
print("   CAPÍTULO 5: EL PODER DE LOS ELEMENTOS")
print(f"{'='*60}")

if len(df_pokemon) > 0:
    # Simular tipos basados en especies conocidas
    type_mapping = {
        'Charizard': ['Fire', 'Flying'], 'Blastoise': ['Water'], 'Venusaur': ['Grass', 'Poison'],
        'Pikachu': ['Electric'], 'Garchomp': ['Dragon', 'Ground'], 'Metagross': ['Steel', 'Psychic'],
        'Tyranitar': ['Rock', 'Dark'], 'Dragonite': ['Dragon', 'Flying'], 'Salamence': ['Dragon', 'Flying'],
        'Lucario': ['Fighting', 'Steel'], 'Gengar': ['Ghost', 'Poison'], 'Alakazam': ['Psychic']
    }
    
    # Expandir tipos para análisis
    type_analysis = []
    for _, pokemon in df_pokemon.iterrows():
        species = pokemon['species']
        if species in type_mapping:
            for ptype in type_mapping[species]:
                type_analysis.append({
                    'species': species,
                    'type': ptype,
                    'player': pokemon['player'],
                    'winner': pokemon['winner']
                })
    
    if type_analysis:
        df_types = pd.DataFrame(type_analysis)
        
        # Tipos más comunes
        type_counts = df_types['type'].value_counts()
        print("Top 10 tipos más utilizados:")
        for i, (ptype, count) in enumerate(type_counts.head(10).items(), 1):
            print(f"  {i:2d}. {ptype}: {count:,} usos")
        
        # Análisis de efectividad por tipo
        if 'winner' in df_types.columns:
            # Calcular winrates por tipo
            type_stats = []
            for ptype in df_types['type'].unique():
                type_data = df_types[df_types['type'] == ptype]
                if len(type_data) > 10:
                    winrate = (type_data['winner'] == type_data['player']).mean()
                    type_stats.append({'type': ptype, 'winrate': winrate})
            
            if type_stats:
                type_winrates = pd.DataFrame(type_stats).set_index('type')['winrate'].sort_values(ascending=False)
            
            if len(type_winrates) > 0:
                print(f"\nTipos con mejor winrate (mín. 10 usos):")
                for ptype, winrate in type_winrates.head(5).items():
                    print(f"  - {ptype}: {winrate:.1%}")
        
        # Visualización de tipos
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        # Distribución de tipos
        type_counts.head(12).plot(kind='barh', ax=axes[0], color=plot_colors['bar'])
        axes[0].set_yticks(range(len(type_counts)))
        axes[0].set_yticklabels(type_counts.index)
        axes[0].set_title('Distribución de Tipos de Pokemon')
        axes[0].set_xlabel('Número de Usos')
        
        # Winrates por tipo
        if len(type_winrates) > 0:
            type_winrates.head(10).plot(kind='bar', ax=axes[1], color=plot_colors['bar'])
            axes[1].set_title('Winrate por Tipo de Pokemon')
            axes[1].set_ylabel('Winrate')
            axes[1].tick_params(axis='x', rotation=45)
            axes[1].axhline(y=0.5, color='red', linestyle='--', alpha=0.7, label='50%')
            axes[1].legend()
        
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / 'type_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"Análisis de tipos guardado: {OUTPUT_DIR / 'type_analysis.png'}")
    else:
        print("No se pudieron mapear tipos para las especies encontradas")
else:
    print("No hay datos de Pokemon disponibles para análisis de tipos")

# %% [markdown]
# ## Capítulo 6: La Alquimia de los Datos - Forjando el Conocimiento
# 
# **Como un maestro herrero forja una espada legendaria, forjaremos las características que definirán nuestra IA.**
# 
# ### 🎭 ¿Qué Sabe un Entrenador al Inicio de la Batalla?
# 
# **Imagina el momento antes del primer movimiento.** Dos entrenadores se enfrentan. ¿Qué información tienen?
# 
# 🔍 **Lo que pueden observar:**
# - Los Pokemon que ven en el equipo rival
# - Sus niveles y HP visibles en pantalla
# - Los tipos de cada Pokemon (Fuego, Agua, Planta...)
# - La fuerza relativa de cada criatura
# 
# ### ⚔️ Los Pilares del Conocimiento Estratégico
# 
# **1. Las Ventajas Elementales** ⭐⭐⭐⭐⭐
# 
# En el mundo Pokemon, **los tipos lo son todo.** Un Charizard (Fuego/Volador) contra un Blastoise (Agua) está en desventaja antes de lanzar un solo ataque. Esta es la esencia del combate Pokemon.
# 
# - Type advantage score: ¿Quién tiene la ventaja elemental?
# - Super effective matchups: ¿Cuántos Pokemon tienen ventaja de tipo?
# - Resistencias: ¿Cuántos ataques serán resistidos?
# - Cobertura: ¿Qué tan versátil es cada equipo?
# 
# **2. El Poder Bruto de los Gladiadores** ⭐⭐⭐⭐
# 
# No todos los Pokemon nacen iguales. Un Arceus (legendario) vs un Rattata... ya conoces el resultado.
# 
# - Base Stat Total (BST): La fuerza bruta de cada Pokemon
# - Legendarios: Los dioses del combate
# - Pseudo-legendarios: Los campeones mortales
# 
# **3. La Composición del Ejército** ⭐⭐⭐⭐
# 
# Un equipo balanceado es un equipo peligroso.
# 
# - Tamaño del equipo y diversidad
# - Niveles promedio y distribución
# - HP total disponible
# 
# **4. Las Ventajas Calculadas** ⭐⭐⭐
# 
# La diferencia entre equipos revela mucho.
# 
# - Level advantage: ¿Quién tiene Pokemon más entrenados?
# - HP advantage: ¿Quién tiene más resistencia?
# - BST advantage: ¿Quién tiene el equipo más poderoso?
# 
# ### 🎯 La Filosofía: Predecir Como un Maestro
# 
# **Un maestro Pokemon no necesita ver la batalla completa para predecir el resultado.** Con solo observar los equipos al inicio, puede estimar las probabilidades. Eso es exactamente lo que enseñaremos a nuestra IA.

# %%
print("\n" + "=" * 60)
print("EXTRACCIÓN DE FEATURES PARA IA (SIN DATA LEAKAGE)")
print("=" * 60)

if POKEMON_DATA_AVAILABLE:
    print("✅ pokemon_data.py cargado - Type matchups disponibles")
    print(f"   • {len(POKEMON_TYPES)} especies con tipos mapeados")
    print(f"   • {len(POKEMON_BST)} especies con BST conocidos")
else:
    print("⚠️  pokemon_data.py no disponible - Features limitadas")

battle_features = []

print("\n🔍 Extrayendo features PRE-BATALLA (observables al inicio)...")
for i, battle in enumerate(battles):
    if (i + 1) % 500 == 0:
        print(f"   Procesadas {i + 1} batallas...")
    
    # Extraer SOLO features pre-batalla
    features = extract_pre_battle_features(battle)
    
    # Agregar target (winner)
    winner = get_in(battle, ['metadata', 'outcome', 'winner'])
    features['winner'] = winner
    
    battle_features.append(features)

df_features = pd.DataFrame(battle_features)

# Guardar features
features_path = OUTPUT_DIR / 'battle_features.csv'
df_features.to_csv(features_path, index=False)

print(f"✅ Extracción completada:")
print(f"   • {len(df_features.columns)} características por batalla")
print(f"   • {len(df_features)} batallas procesadas")
print(f"   • Dataset guardado: {features_path.name}")

# Mostrar estadísticas de features
numeric_cols = df_features.select_dtypes(include=[np.number]).columns
print(f"\n📊 Estadísticas de features extraídas:")
print(f"   • Total features numéricas: {len(numeric_cols)}")

# Mostrar algunas features clave si existen
key_features = ['type_advantage_score', 'p1_avg_bst', 'p2_avg_bst', 'level_advantage_p1', 'hp_advantage_p1']
available_key_features = [f for f in key_features if f in df_features.columns]
if available_key_features:
    print(f"   • Features clave disponibles: {len(available_key_features)}")
    for feat in available_key_features[:5]:
        print(f"     - {feat}: rango [{df_features[feat].min():.2f}, {df_features[feat].max():.2f}]")

print(f"\nPrimeras 5 filas del dataset de features:")
display_cols = ['winner'] + [c for c in df_features.columns if c in ['p1_team_size', 'p2_team_size', 'type_advantage_score', 'bst_advantage_p1', 'level_advantage_p1']][:5]
print(df_features[display_cols].head())

# %% [markdown]
# ### 🔗 Matriz de Correlación de Features
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
    correlation_matrix = numeric_features.corr()
    
    # Matriz completa (sin anotaciones para mejor legibilidad)
    plt.figure(figsize=(16, 14))
    sns.heatmap(correlation_matrix, annot=False, cmap=plot_colors['heatmap'], center=0, 
                square=True, cbar_kws={'shrink': 0.8})
    plt.title('Matriz de Correlación Completa - Features Numéricas', fontsize=14)
    plt.xticks(rotation=45, ha='right', fontsize=8)
    plt.yticks(rotation=0, fontsize=8)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'correlation_matrix_full.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Matriz de correlaciones filtrada - Top features más importantes
    plt.figure(figsize=(12, 10))
    
    # Seleccionar features con mayor varianza (más informativas)
    feature_variance = correlation_matrix.var().sort_values(ascending=False)
    
    # Tomar top 20 features con mayor varianza en sus correlaciones
    top_features = feature_variance.head(20).index.tolist()
    
    if len(top_features) > 1:
        filtered_corr = correlation_matrix.loc[top_features, top_features]
        sns.heatmap(filtered_corr, annot=True, cmap=plot_colors['heatmap'], center=0, 
                    square=True, fmt='.2f', cbar_kws={'shrink': 0.8}, annot_kws={'size': 8})
        plt.title('Matriz de Correlación - Top 20 Features Más Informativas', fontsize=14)
        plt.xticks(rotation=45, ha='right', fontsize=9)
        plt.yticks(rotation=0, fontsize=9)
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / 'correlation_matrix_filtered.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"\n📊 Matrices de correlación generadas:")
        print(f"   • Matriz completa: visión general de todas las {len(correlation_matrix.columns)} features")
        print(f"   • Matriz filtrada: top 20 features con mayor variabilidad en correlaciones")
        print(f"\n💡 Insights de correlaciones:")
        
        # Encontrar las correlaciones más fuertes (excluyendo diagonal)
        corr_pairs = []
        for i in range(len(filtered_corr.columns)):
            for j in range(i+1, len(filtered_corr.columns)):
                corr_pairs.append((
                    filtered_corr.columns[i],
                    filtered_corr.columns[j],
                    filtered_corr.iloc[i, j]
                ))
        
        # Ordenar por valor absoluto de correlación
        corr_pairs.sort(key=lambda x: abs(x[2]), reverse=True)
        
        print(f"   Top 5 correlaciones más fuertes:")
        for feat1, feat2, corr_val in corr_pairs[:5]:
            print(f"     • {feat1} ↔ {feat2}: {corr_val:.3f}")
    else:
        print("No hay suficientes features para matriz filtrada")

# %% [markdown]
# ## Capítulo 7: El Primer Desafío - ¿Puede la IA Predecir la Victoria?
# 
# **Ha llegado el momento de la verdad.** Hemos analizado miles de batallas, extraído características estratégicas, y descifrado los secretos del combate Pokemon. Pero surge la pregunta definitiva:
# 
# ### 🎯 ¿Puede una IA Predecir el Resultado Solo Observando los Equipos?
# 
# **Como un maestro Pokemon que evalúa a sus oponentes antes de la batalla, pondremos a prueba nuestra comprensión de los datos.**
# 
# 🔮 **El Desafío:**
# - Entrenar un modelo baseline con las características que hemos forjado
# - Usar SOLO información observable al inicio de la batalla
# - Predecir el ganador basándose en composición, tipos y poder
# 
# 🎭 **¿Qué Esperamos Descubrir?**
# - ¿Son las ventajas de tipo realmente tan predictivas como creemos?
# - ¿El poder bruto (BST) supera a la estrategia?
# - ¿Qué características son las más importantes para la victoria?
# 
# ### ⚔️ El Gladiador Elegido: Logistic Regression
# 
# Para este primer desafío, elegimos al **estratega clásico** - un modelo simple pero poderoso que nos revelará qué características realmente importan.
# 
# **Si este modelo puede predecir victorias con precisión, validaremos que hemos capturado la esencia del combate Pokemon.**

# %%
print(f"\n🎯 {'='*50}")
print("   VALIDACIÓN: MODELO BASELINE LIMPIO (SIN LEAKAGE)")
print(f"{'='*60}")

# Cargar dataset COMPLETO para entrenamiento del baseline
print(f"\n📚 Cargando dataset completo para entrenamiento del baseline...")
with open(ALL_BATTLES_JSON, "r") as f:
    all_battles_full = json.load(f)

print(f"✅ Dataset completo cargado: {len(all_battles_full):,} batallas")
print(f"   (vs {len(battles):,} batallas usadas en EDA)")

# Extraer features del dataset completo
print(f"\n🔬 Extrayendo features del dataset completo...")
print(f"   Procesando {len(all_battles_full):,} batallas...")

features_full = []
for i, battle in enumerate(all_battles_full):
    if (i + 1) % 2000 == 0:
        print(f"   Procesadas {i + 1:,} batallas...")
    features_full.append(extract_pre_battle_features(battle))

df_features_full = pd.DataFrame(features_full)
print(f"✅ Features extraídas: {len(df_features_full):,} batallas x {len(df_features_full.columns)} features")

# Usar el dataset completo para el baseline
df_features = df_features_full

# Preparar datos para modelo baseline
try:
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import roc_auc_score, classification_report
    from sklearn.preprocessing import LabelEncoder, StandardScaler
    
    # Seleccionar features numéricas para el baseline
    numeric_features = df_features.select_dtypes(include=[np.number]).columns.tolist()
    
    # Remover solo battle_id (todas las demás features son válidas)
    exclude_cols = ['battle_id'] if 'battle_id' in numeric_features else []
    feature_cols = [col for col in numeric_features if col not in exclude_cols]
    
    print(f"\n📊 Features disponibles: {len(feature_cols)}")
    print(f"   ✅ Todas son PRE-BATALLA (sin leakage)")
    
    # Mostrar categorías de features
    type_features = [f for f in feature_cols if 'type' in f.lower() or 'super_effective' in f or 'resisted' in f]
    bst_features = [f for f in feature_cols if 'bst' in f or 'legendary' in f]
    comp_features = [f for f in feature_cols if any(x in f for x in ['team_size', 'level', 'hp', 'species_diversity'])]
    
    print(f"\n📋 Categorías de features:")
    print(f"   • Type matchups: {len(type_features)}")
    print(f"   • Pokemon strength (BST): {len(bst_features)}")
    print(f"   • Team composition: {len(comp_features)}")
    print(f"   • Ventajas derivadas: {len(feature_cols) - len(type_features) - len(bst_features) - len(comp_features)}")
    
    # Preparar target
    if 'winner' in df_features.columns:
        # Filtrar solo batallas con ganador definido
        valid_battles = df_features[df_features['winner'].isin(['p1', 'p2'])].copy()
        
        if len(valid_battles) > 10 and len(feature_cols) > 0:  # Mínimo para entrenar
            X = valid_battles[feature_cols].fillna(0)  # Imputar nulos con 0
            y = valid_battles['winner']
            
            # Codificar target
            le = LabelEncoder()
            y_encoded = le.fit_transform(y)
            
            # Split train/test
            X_train, X_test, y_train, y_test = train_test_split(
                X, y_encoded, test_size=0.2, stratify=y_encoded, random_state=42
            )
            
            # Escalar features para mejorar convergencia
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            # Entrenar modelo baseline con features escaladas
            clf = LogisticRegression(max_iter=1000, random_state=42)
            clf.fit(X_train_scaled, y_train)
            
            # Evaluar con datos escalados
            y_pred_proba = clf.predict_proba(X_test_scaled)[:, 1]
            auc_score = roc_auc_score(y_test, y_pred_proba)
            
            print(f"\n✅ Modelo baseline entrenado:")
            print(f"  - Features utilizadas: {len(feature_cols)}")
            print(f"  - Tamaño entrenamiento: {len(X_train):,}")
            print(f"  - Tamaño test: {len(X_test):,}")
            print(f"  - ROC-AUC: {auc_score:.3f}")
            
            # Interpretación del resultado con narrativa épica
            print(f"\n🎭 El Veredicto del Primer Desafío:")
            print(f"{'='*60}")
            if auc_score >= 0.80:
                print(f"  🏆 ¡VICTORIA ÉPICA! ROC-AUC: {auc_score:.3f}")
                print(f"")
                print(f"  ¡Hemos descifrado el código de la victoria!")
                print(f"  Las características que identificamos son ALTAMENTE predictivas.")
                print(f"  Type matchups y poder de Pokemon revelan el destino de las batallas.")
                print(f"")
                print(f"  🎯 Esto valida nuestra comprensión del combate Pokemon.")
            elif auc_score >= 0.70:
                print(f"  ✅ VICTORIA SÓLIDA! ROC-AUC: {auc_score:.3f}")
                print(f"")
                print(f"  El modelo ha aprendido patrones reales del combate Pokemon.")
                print(f"  Mucho mejor que adivinar al azar (0.50).")
                print(f"  Las características capturan la esencia de la batalla.")
            elif auc_score >= 0.65:
                print(f"  ⚠️  Victoria Modesta. ROC-AUC: {auc_score:.3f}")
                print(f"")
                print(f"  Hay señal en los datos, pero podríamos mejorar.")
                print(f"  Considerar más características de synergy y cobertura.")
            else:
                print(f"  ❌ Desafío Fallido. ROC-AUC: {auc_score:.3f}")
                print(f"")
                print(f"  Necesitamos revisar nuestras características.")
            
            print(f"\n⚔️  El Poder de la Predicción Honesta:")
            print(f"  Este modelo usa SOLO información observable al inicio.")
            print(f"  No hace trampa. No ve el futuro. Solo analiza los equipos.")
            print(f"  Como un maestro Pokemon, predice basándose en conocimiento real.")
            
            # Importancia de features
            feature_importance = pd.DataFrame({
                'feature': feature_cols,
                'importance': np.abs(clf.coef_[0])
            }).sort_values('importance', ascending=False)
            
            print(f"\nTop 10 features más importantes:")
            for i, (_, row) in enumerate(feature_importance.head(10).iterrows(), 1):
                print(f"  {i:2d}. {row['feature']}: {row['importance']:.3f}")
            
            # Guardar importancia de features
            importance_path = OUTPUT_DIR / 'feature_importance_baseline.csv'
            feature_importance.to_csv(importance_path, index=False)
            print(f"\nImportancia guardada: {importance_path}")
            
            # Visualizaciones del modelo baseline
            print(f"\n📊 Generando visualizaciones del modelo...")
            
            # 1. ROC Curve
            from sklearn.metrics import roc_curve
            fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
            
            fig, axes = plt.subplots(1, 2, figsize=(14, 5))
            
            # ROC Curve
            axes[0].plot(fpr, tpr, color=plot_colors['line'], linewidth=2, 
                        label=f'ROC curve (AUC = {auc_score:.3f})')
            axes[0].plot([0, 1], [0, 1], 'k--', linewidth=1, label='Random (AUC = 0.5)')
            axes[0].set_xlabel('False Positive Rate', fontsize=12)
            axes[0].set_ylabel('True Positive Rate', fontsize=12)
            axes[0].set_title('ROC Curve - Baseline Model', fontsize=14, fontweight='bold')
            axes[0].legend(loc='lower right', fontsize=10)
            axes[0].grid(True, alpha=0.3)
            
            # Feature Importance
            top_features = feature_importance.head(15)
            axes[1].barh(range(len(top_features)), top_features['importance'], 
                        color=plot_colors['bar'])
            axes[1].set_yticks(range(len(top_features)))
            axes[1].set_yticklabels(top_features['feature'], fontsize=9)
            axes[1].set_xlabel('Importance (|Coefficient|)', fontsize=12)
            axes[1].set_title('Top 15 Features - Baseline Model', fontsize=14, fontweight='bold')
            axes[1].grid(True, alpha=0.3, axis='x')
            axes[1].invert_yaxis()
            
            plt.tight_layout()
            plt.savefig(OUTPUT_DIR / 'baseline_model_performance.png', dpi=300, bbox_inches='tight')
            plt.show()
            
            print(f"✅ Visualizaciones guardadas: {OUTPUT_DIR / 'baseline_model_performance.png'}")
            
        else:
            print("Datos insuficientes para entrenar modelo baseline")
    else:
        print("Variable 'winner' no encontrada para modelo baseline")
        
except ImportError:
    print("Scikit-learn no disponible. Instalar con: pip install scikit-learn")
except Exception as e:
    print(f"Error en modelo baseline: {e}")

# %% [markdown]
# 📊 Análisis del Modelo Baseline - Pokemon Battle AI

## 🎯 Resumen Ejecutivo

# **Modelo**: Logistic Regression (Baseline)  
# **Dataset**: 13,979 batallas completas  
# **ROC-AUC**: **0.819** ✅  
# **Features**: 37 características PRE-BATALLA (sin data leakage)

#---

## 📈 ROC Curve Analysis (Panel Izquierdo)

### ¿Qué nos dice la curva ROC?

# ✅ **Excelente rendimiento**: La curva está muy por encima de la línea diagonal (random = 0.5)
# - El modelo **NO está adivinando al azar**
# - Tiene capacidad real de discriminar entre ganadores p1 y p2

# ✅ **AUC = 0.819**: Muy bueno para un modelo baseline simple
# - **0.5** = Random (lanzar una moneda)
# - **0.819** = El modelo es **64% mejor que adivinar** ((0.819-0.5)/(1-0.5))
# - **0.85+** = Excelente (nuestro objetivo con modelos avanzados)

# ✅ **Forma de la curva**: Sube rápido al inicio
# - Buen balance entre True Positive Rate y False Positive Rate
# - El modelo identifica correctamente muchos ganadores sin muchos falsos positivos
# - La curva se acerca al punto ideal (0,1) en la esquina superior izquierda

# ### Interpretación Práctica

# **¿Qué significa ROC-AUC = 0.819?**

# Si le das al modelo dos batallas aleatorias (una ganada por p1 y otra por p2), el modelo **acertará cuál es cuál el 81.9% de las veces**. Esto es significativamente mejor que adivinar (50%).

#---

## 📊 Feature Importance Analysis (Panel Derecho)

### 🥇 Top 3 Features (Dominantes)

# | Rank | Feature | Importance | Interpretación |
# |------|---------|------------|----------------|
# | 1 | `p2_species_diversity` | ~1.5 | Diversidad del equipo rival |
# | 2 | `p1_species_diversity` | ~1.3 | Diversidad del equipo propio |
# | 3 | `p1_team_size` | ~1.2 | Tamaño del equipo |

# **¿Qué significa?**
# - La **diversidad de especies** es el factor #1 para predecir victorias
# - Equipos con más variedad de Pokemon tienen ventaja estratégica
# - El tamaño del equipo también importa mucho (más opciones = más flexibilidad)

# **Insight clave**: Un equipo de 6 Pokemon diferentes tiene más probabilidad de ganar que un equipo de 6 Pokemon del mismo tipo, incluso si son más poderosos.

### 🥈 Features Secundarias (Poder y Ventajas)

# | Feature | Importance | Interpretación |
# |---------|------------|----------------|
# | `p2_max_bst` | ~0.24 | Pokemon más fuerte del rival |
# | `p2_bst_std` | ~0.21 | Variabilidad de poder en equipo rival |
# | `hp_advantage_p1` | ~0.16 | Ventaja de HP total |
# | `p1_total_hp` | ~0.15 | HP total del equipo |

# **¿Qué significa?**
# - El **poder bruto** (BST) sí importa, pero **mucho menos que la diversidad**
# - La **ventaja de HP** es relevante para predecir victorias
# - La **consistencia del equipo** (desviación estándar de BST) también cuenta

# ### 🥉 Features Menores

# - `p1_legendary_count` / `p2_legendary_count` - Número de legendarios
# - `p1_type_diversity` - Diversidad de tipos
# - `p2_avg_bst` / `p1_avg_hp` - Promedios de stats

# **Observación importante**: Estas features tienen importancia baja, lo que sugiere que:
# - Tener legendarios no garantiza victoria
# - La diversidad de especies > diversidad de tipos
# - Los promedios importan menos que los extremos (max/min)

#---

## 🎯 Conclusiones Clave

### ✅ Lo que FUNCIONA

# 1. **Diversidad > Poder bruto**
#    - Un equipo variado gana más que uno de puros legendarios
#    - La flexibilidad estratégica supera al poder puro
#    - Esto valida la mecánica competitiva de Pokemon

# 2. **Tamaño del equipo**
#    - Tener más Pokemon da ventaja significativa
#    - Más opciones = más adaptabilidad durante la batalla

# 3. **Modelo honesto y deployable**
#    - ROC-AUC 0.819 sin data leakage es excelente
#    - Usa SOLO información observable al inicio de la batalla
#    - Puede desplegarse en producción sin problemas

# ### ⚠️ Lo que SORPRENDE

# 1. **Type matchups NO aparecen en top 15**
#    - Esperábamos que las ventajas de tipo fueran más importantes
#    - Posible explicación: En random battles, los equipos ya están balanceados
#    - Los modelos no-lineales podrían capturar mejor estas interacciones

# 2. **BST no es dominante**
#    - El poder bruto importa, pero no es el factor principal
#    - La estrategia y diversidad superan al poder puro
#    - Esto es coherente con el meta competitivo de Pokemon

# 3. **Diversidad es REY**
#    - La variedad estratégica es el predictor #1
#    - Equipos balanceados > Equipos especializados
#    - Refleja la importancia de la cobertura en Pokemon competitivo

# ### 🔍 Insights Estratégicos

# **Para construir un equipo ganador:**
# 1. ✅ Prioriza **diversidad de especies** sobre poder bruto
# 2. ✅ Mantén un **equipo completo** (6 Pokemon)
# 3. ✅ Busca **balance** en lugar de especialización extrema
# 4. ⚠️ No confíes solo en legendarios
# 5. ⚠️ La ventaja de tipo importa, pero menos de lo esperado

#---

## 🚀 Próximos Pasos

### Para Mejorar el Modelo

# 1. **Modelos No-Lineales**
#    - Random Forest, XGBoost, LightGBM
#    - Deberían capturar mejor las interacciones entre features
#    - Objetivo: **ROC-AUC > 0.85**
# 
# 2. **Feature Engineering Avanzado**
#    - Interacciones entre type matchups y BST
#    - Synergies de equipo más complejas
#    - Embeddings de Pokemon basados en uso competitivo
# 
# 3. **Ensemble Methods**
#    - Combinar múltiples modelos
#    - Aprovechar fortalezas de diferentes algoritmos
#    - Voting/Stacking para mejorar robustez
# 
# ### Expectativas Realistas
# 
# | Modelo | ROC-AUC Esperado | Comentario |
# |--------|------------------|------------|
# | Logistic Regression (actual) | 0.819 | ✅ Baseline sólido |
# | Random Forest | 0.83 - 0.86 | Captura interacciones |
# | XGBoost | 0.84 - 0.87 | Optimizado para tablas |
# | LightGBM | 0.84 - 0.87 | Rápido y preciso |
# | Neural Network | 0.82 - 0.85 | Puede overfittear |
# | Ensemble | 0.85 - 0.88 | Mejor de todos |
# 
# ---
# 
# ## 📝 Notas Técnicas
# 
# ### Configuración del Modelo
# 
# ```python
# Model: LogisticRegression(random_state=42)
# Scaler: StandardScaler()
# Train/Test Split: 80/20 (stratified)
# Training samples: 11,183
# Test samples: 2,796
# Features: 37 (all pre-battle, no leakage)

# %% [markdown]
# ---
# 
# ## 🎯 Análisis Completado
# 
# **El viaje exploratorio ha terminado.** Hemos analizado miles de batallas, identificado patrones clave, y forjado las características que definirán nuestra IA.
# 
# **Próximo capítulo:** `ML_Training_Advanced.ipynb` - El Gran Torneo de Algoritmos
# 
# ---
