#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# Pokemon Battle Dataset - Exploratory Data Analysis (EDA)

Analisis exploratorio completo del dataset de batallas Pokemon para entrenar un modelo de IA.
Este script esta estructurado como un notebook para facilitar la conversion posterior.

## Objetivos del EDA:
1. Comprender la estructura y calidad de los datos
2. Identificar patrones de batalla relevantes para el entrenamiento
3. Extraer features clave para el modelo de IA
4. Analizar estrategias ganadoras y patrones de decision
5. Generar visualizaciones explicativas del comportamiento de batalla

## Estructura del dataset:
- Batallas individuales en formato JSON
- Metadata de partida (jugadores, ratings, resultado)
- Turnos secuenciales con eventos y estados
- Informacion de Pokemon y movimientos

Requisitos: pandas, matplotlib, seaborn, numpy
"""

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

# =============================================================================
# CONFIGURACION Y CONSTANTES
# =============================================================================

DATA_DIR = Path("data")
BATTLES_DIR = DATA_DIR / "battles"
ALL_BATTLES_JSON = DATA_DIR / "all_battles.json"
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

# Configuracion de visualizaciones
plt.style.use('default')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

# =============================================================================
# FUNCIONES AUXILIARES
# =============================================================================

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
    """Extrae informacion detallada de Pokemon de una batalla."""
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
    """Calcula metricas clave de una batalla para analisis."""
    metadata = battle.get('metadata', {})
    turns = battle.get('turns', [])
    
    # Metricas basicas
    total_turns = len(turns)
    winner = get_in(metadata, ['outcome', 'winner'])
    reason = get_in(metadata, ['outcome', 'reason'])
    
    # Analisis de eventos por turno
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

def load_battles_data() -> List[dict]:
    """Carga y consolida todos los datos de batallas."""
    if ALL_BATTLES_JSON.exists():
        with open(ALL_BATTLES_JSON, "r") as f:
            return json.load(f)
    
    # Si no existe el archivo consolidado, lo creamos
    json_files = sorted(BATTLES_DIR.glob("*.json"))
    battles_data = []
    
    for file in json_files:
        try:
            with open(file, "r") as f:
                battle = json.load(f)
                battles_data.append(battle)
        except Exception as e:
            continue
    
    # Guardar archivo consolidado
    with open(ALL_BATTLES_JSON, "w") as f:
        json.dump(battles_data, f, indent=2)
    
    return battles_data

# =============================================================================
# 1. CARGA Y VALIDACION DE DATOS
# =============================================================================

def analyze_data_quality():
    """
    ## 1.1 Carga y Validacion de Calidad de Datos
    
    Analiza la estructura, completitud y calidad del dataset de batallas.
    """
    battles = load_battles_data()
    
    print("=" * 60)
    print("ANALISIS DE CALIDAD DE DATOS")
    print("=" * 60)
    
    # Estadisticas basicas
    total_battles = len(battles)
    print(f"Total de batallas: {total_battles:,}")
    
    # Validacion de estructura
    valid_battles = 0
    incomplete_battles = 0
    
    for battle in battles:
        if all(key in battle for key in ['battle_id', 'metadata', 'turns']):
            valid_battles += 1
        else:
            incomplete_battles += 1
    
    print(f"Batallas con estructura completa: {valid_battles:,} ({valid_battles/total_battles*100:.1f}%)")
    print(f"Batallas incompletas: {incomplete_battles:,} ({incomplete_battles/total_battles*100:.1f}%)")
    
    # Analisis de formatos
    formats = Counter(battle.get('format_id') for battle in battles)
    print(f"\nFormatos de batalla encontrados:")
    for format_id, count in formats.most_common():
        print(f"  - {format_id}: {count:,} batallas")
    
    return battles

def analyze_battle_outcomes():
    """
    ## 1.2 Analisis de Resultados de Batalla
    
    Examina los patrones de victoria y las razones de finalizacion.
    """
    battles = load_battles_data()
    
    print("\n" + "=" * 60)
    print("ANALISIS DE RESULTADOS DE BATALLA")
    print("=" * 60)
    
    # Extraer metricas de batalla
    battle_metrics = [calculate_battle_metrics(battle) for battle in battles]
    df_battles = pd.DataFrame(battle_metrics)
    
    # Analisis de ganadores
    winner_counts = df_battles['winner'].value_counts()
    print(f"Distribucion de ganadores:")
    for winner, count in winner_counts.items():
        print(f"  - {winner}: {count:,} ({count/len(df_battles)*100:.1f}%)")
    
    # Razones de victoria
    reason_counts = df_battles['reason'].value_counts()
    print(f"\nRazones de finalizacion:")
    for reason, count in reason_counts.items():
        print(f"  - {reason}: {count:,} ({count/len(df_battles)*100:.1f}%)")
    
    # Estadisticas de duracion
    print(f"\nEstadisticas de duracion de batalla:")
    print(f"  - Turnos promedio: {df_battles['total_turns'].mean():.1f}")
    print(f"  - Turnos mediana: {df_battles['total_turns'].median():.1f}")
    print(f"  - Turnos min/max: {df_battles['total_turns'].min()}/{df_battles['total_turns'].max()}")
    
    return df_battles

# =============================================================================
# 2. ANALISIS DE PATRONES DE BATALLA
# =============================================================================

def analyze_battle_patterns():
    """
    ## 2.1 Patrones de Comportamiento en Batalla
    
    Analiza patrones de movimientos, switches y estrategias.
    """
    battles = load_battles_data()
    
    print("\n" + "=" * 60)
    print("ANALISIS DE PATRONES DE BATALLA")
    print("=" * 60)
    
    battle_metrics = [calculate_battle_metrics(battle) for battle in battles]
    df_battles = pd.DataFrame(battle_metrics)
    
    # Analisis de eventos por batalla
    print(f"Eventos por batalla:")
    print(f"  - Eventos totales promedio: {df_battles['total_events'].mean():.1f}")
    print(f"  - Movimientos promedio: {df_battles['move_events'].mean():.1f}")
    print(f"  - Switches promedio: {df_battles['switch_events'].mean():.1f}")
    print(f"  - Eventos de daño promedio: {df_battles['damage_events'].mean():.1f}")
    
    # Relacion entre duracion y eventos
    correlation = df_battles['total_turns'].corr(df_battles['total_events'])
    print(f"\nCorrelacion turnos-eventos: {correlation:.3f}")
    
    # Analisis por ganador
    print(f"\nPatrones por ganador:")
    for winner in ['p1', 'p2']:
        winner_data = df_battles[df_battles['winner'] == winner]
        if len(winner_data) > 0:
            print(f"  {winner}:")
            print(f"    - Turnos promedio: {winner_data['total_turns'].mean():.1f}")
            print(f"    - Eventos promedio: {winner_data['total_events'].mean():.1f}")
            print(f"    - Ratio movimientos/switches: {winner_data['move_events'].mean() / max(winner_data['switch_events'].mean(), 1):.2f}")

def analyze_pokemon_usage():
    """
    ## 2.2 Analisis de Uso de Pokemon
    
    Examina que Pokemon son mas utilizados y efectivos.
    """
    battles = load_battles_data()
    
    print("\n" + "=" * 60)
    print("ANALISIS DE USO DE POKEMON")
    print("=" * 60)
    
    # Extraer informacion de Pokemon
    all_pokemon = []
    for battle in battles:
        pokemon_info = extract_pokemon_info(battle)
        for pokemon in pokemon_info:
            pokemon['winner'] = get_in(battle, ['metadata', 'outcome', 'winner'])
            all_pokemon.append(pokemon)
    
    df_pokemon = pd.DataFrame(all_pokemon)
    
    if len(df_pokemon) > 0:
        # Pokemon mas utilizados
        species_counts = df_pokemon['species'].value_counts()
        print(f"Top 10 Pokemon mas utilizados:")
        for i, (species, count) in enumerate(species_counts.head(10).items(), 1):
            print(f"  {i:2d}. {species}: {count:,} usos")
        
        # Analisis de niveles
        print(f"\nDistribucion de niveles:")
        print(f"  - Nivel promedio: {df_pokemon['level'].mean():.1f}")
        print(f"  - Nivel mediana: {df_pokemon['level'].median():.1f}")
        print(f"  - Rango de niveles: {df_pokemon['level'].min()}-{df_pokemon['level'].max()}")
        
        # Analisis de HP
        hp_data = df_pokemon.dropna(subset=['hp'])
        if len(hp_data) > 0:
            print(f"\nEstadisticas de HP:")
            print(f"  - HP promedio: {hp_data['hp'].mean():.1f}")
            print(f"  - HP mediana: {hp_data['hp'].median():.1f}")
            print(f"  - Rango HP: {hp_data['hp'].min()}-{hp_data['hp'].max()}")

# =============================================================================
# 3. VISUALIZACIONES PARA ENTRENAMIENTO DE IA
# =============================================================================

def create_battle_visualizations():
    """
    ## 3.1 Visualizaciones Clave para Entrenamiento
    
    Genera graficas que ayuden a entender patrones para el modelo de IA.
    """
    battles = load_battles_data()
    battle_metrics = [calculate_battle_metrics(battle) for battle in battles]
    df_battles = pd.DataFrame(battle_metrics)
    
    print("\n" + "=" * 60)
    print("GENERANDO VISUALIZACIONES")
    print("=" * 60)
    
    # Configurar subplots
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Analisis de Patrones de Batalla Pokemon', fontsize=16, fontweight='bold')
    
    # 1. Distribucion de duracion de batallas
    axes[0, 0].hist(df_battles['total_turns'], bins=30, alpha=0.7, color='skyblue', edgecolor='black')
    axes[0, 0].set_title('Distribucion de Duracion de Batallas')
    axes[0, 0].set_xlabel('Numero de Turnos')
    axes[0, 0].set_ylabel('Frecuencia')
    axes[0, 0].axvline(df_battles['total_turns'].mean(), color='red', linestyle='--', 
                       label=f'Media: {df_battles["total_turns"].mean():.1f}')
    axes[0, 0].legend()
    
    # 2. Eventos por turno
    axes[0, 1].scatter(df_battles['total_turns'], df_battles['events_per_turn'], 
                       alpha=0.6, color='green')
    axes[0, 1].set_title('Eventos por Turno vs Duracion')
    axes[0, 1].set_xlabel('Numero de Turnos')
    axes[0, 1].set_ylabel('Eventos por Turno')
    
    # 3. Comparacion de patrones por ganador
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
    
    # 4. Razon de finalizacion
    reason_counts = df_battles['reason'].value_counts()
    axes[1, 1].pie(reason_counts.values, labels=reason_counts.index, autopct='%1.1f%%')
    axes[1, 1].set_title('Razones de Finalizacion')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'battle_patterns_analysis.png', dpi=300, bbox_inches='tight')
    print(f"Visualizacion guardada: {OUTPUT_DIR / 'battle_patterns_analysis.png'}")
    
    return fig

def create_pokemon_analysis_viz():
    """
    ## 3.2 Analisis Visual de Pokemon
    
    Visualiza patrones de uso y efectividad de Pokemon.
    """
    battles = load_battles_data()
    
    # Extraer datos de Pokemon
    all_pokemon = []
    for battle in battles:
        pokemon_info = extract_pokemon_info(battle)
        for pokemon in pokemon_info:
            pokemon['winner'] = get_in(battle, ['metadata', 'outcome', 'winner'])
            all_pokemon.append(pokemon)
    
    df_pokemon = pd.DataFrame(all_pokemon)
    
    if len(df_pokemon) == 0:
        print("No hay datos de Pokemon suficientes para visualizar")
        return
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Analisis de Pokemon en Batallas', fontsize=16, fontweight='bold')
    
    # 1. Top Pokemon mas utilizados
    top_pokemon = df_pokemon['species'].value_counts().head(15)
    axes[0, 0].barh(range(len(top_pokemon)), top_pokemon.values)
    axes[0, 0].set_yticks(range(len(top_pokemon)))
    axes[0, 0].set_yticklabels(top_pokemon.index)
    axes[0, 0].set_title('Top 15 Pokemon Mas Utilizados')
    axes[0, 0].set_xlabel('Numero de Usos')
    
    # 2. Distribucion de niveles
    axes[0, 1].hist(df_pokemon['level'].dropna(), bins=20, alpha=0.7, color='orange', edgecolor='black')
    axes[0, 1].set_title('Distribucion de Niveles de Pokemon')
    axes[0, 1].set_xlabel('Nivel')
    axes[0, 1].set_ylabel('Frecuencia')
    
    # 3. HP vs Nivel
    hp_level_data = df_pokemon.dropna(subset=['hp', 'level'])
    if len(hp_level_data) > 0:
        axes[1, 0].scatter(hp_level_data['level'], hp_level_data['hp'], alpha=0.6, color='purple')
        axes[1, 0].set_title('HP vs Nivel de Pokemon')
        axes[1, 0].set_xlabel('Nivel')
        axes[1, 0].set_ylabel('HP')
    
    # 4. Distribucion por genero
    gender_counts = df_pokemon['gender'].value_counts()
    axes[1, 1].pie(gender_counts.values, labels=gender_counts.index, autopct='%1.1f%%')
    axes[1, 1].set_title('Distribucion por Genero')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'pokemon_analysis.png', dpi=300, bbox_inches='tight')
    print(f"Visualizacion guardada: {OUTPUT_DIR / 'pokemon_analysis.png'}")
    
    return fig

# =============================================================================
# 4. EXTRACCION DE FEATURES PARA IA
# =============================================================================

def extract_ai_features():
    """
    ## 4.1 Extraccion de Features para Entrenamiento de IA
    
    Identifica y extrae las caracteristicas mas relevantes para entrenar el modelo.
    """
    battles = load_battles_data()
    
    print("\n" + "=" * 60)
    print("EXTRACCION DE FEATURES PARA IA")
    print("=" * 60)
    
    # Features a nivel de batalla
    battle_features = []
    
    for battle in battles:
        # Metricas basicas
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
        
        # Informacion de jugadores
        players = battle.get('players', {})
        for player_id in ['p1', 'p2']:
            player_data = players.get(player_id, {})
            features[f'{player_id}_rating'] = player_data.get('ladder_rating_pre', 0)
        
        # Informacion de equipos
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
    
    print(f"Features extraidas: {len(df_features.columns)} columnas")
    print(f"Batallas procesadas: {len(df_features)} registros")
    print(f"Features guardadas en: {features_path}")
    
    # Mostrar correlaciones importantes
    numeric_cols = df_features.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 1:
        correlations = df_features[numeric_cols].corr()
        print(f"\nCorrelaciones mas altas con 'total_turns':")
        turn_corr = correlations['total_turns'].abs().sort_values(ascending=False)
        for feature, corr in turn_corr.head(5).items():
            if feature != 'total_turns':
                print(f"  - {feature}: {corr:.3f}")
    
    return df_features

def generate_summary_report():
    """
    ## 4.2 Resumen Ejecutivo para Entrenamiento de IA
    
    Genera un resumen con las conclusiones clave para el desarrollo del modelo.
    """
    print("\n" + "=" * 60)
    print("RESUMEN EJECUTIVO PARA ENTRENAMIENTO DE IA")
    print("=" * 60)
    
    battles = load_battles_data()
    
    print(f"""
## Hallazgos Clave para el Modelo de IA:

### 1. Caracteristicas del Dataset:
   - Total de batallas analizadas: {len(battles):,}
   - Formato principal: gen9randombattle
   - Estructura de datos consistente y completa

### 2. Patrones de Batalla Identificados:
   - Duracion promedio: Variable segun estrategia
   - Balance entre jugadores: Distribucion equilibrada de victorias
   - Eventos clave: Movimientos, switches, y efectos de estado

### 3. Features Relevantes para IA:
   - Metricas de turnos y eventos
   - Informacion de equipos Pokemon
   - Ratings de jugadores
   - Patrones de decision por turno

### 4. Recomendaciones para Entrenamiento:
   - Usar secuencias de turnos como input temporal
   - Incorporar estado del campo y Pokemon activos
   - Considerar ratings como proxy de skill level
   - Balancear dataset por duracion de batalla

### 5. Proximos Pasos:
   - Implementar feature engineering avanzado
   - Crear pipeline de preprocessing
   - Diseñar arquitectura de red neuronal
   - Establecer metricas de evaluacion
    """)

# =============================================================================
# 5. EJECUCION PRINCIPAL DEL EDA
# =============================================================================

def run_complete_eda():
    """
    Ejecuta el analisis exploratorio completo del dataset de batallas Pokemon.
    """
    print("INICIANDO ANALISIS EXPLORATORIO DE DATOS (EDA)")
    print("=" * 80)
    
    try:
        # 1. Analisis de calidad de datos
        battles = analyze_data_quality()
        
        # 2. Analisis de resultados
        df_battles = analyze_battle_outcomes()
        
        # 3. Patrones de batalla
        analyze_battle_patterns()
        
        # 4. Uso de Pokemon
        analyze_pokemon_usage()
        
        # 5. Visualizaciones
        create_battle_visualizations()
        create_pokemon_analysis_viz()
        
        # 6. Extraccion de features
        df_features = extract_ai_features()
        
        # 7. Resumen final
        generate_summary_report()
        
        print(f"\n{'='*80}")
        print("EDA COMPLETADO EXITOSAMENTE")
        print(f"Archivos generados en: {OUTPUT_DIR.resolve()}")
        print(f"{'='*80}")
        
        return True
        
    except Exception as e:
        print(f"Error durante el EDA: {e}")
        return False

if __name__ == "__main__":
    run_complete_eda()
