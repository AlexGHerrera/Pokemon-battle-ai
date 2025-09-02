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
import argparse
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

def event_type_counts(evts: Any) -> Dict[str, int]:
    """Cuenta tipos de eventos en una lista de eventos."""
    if not isinstance(evts, list):
        return {}
    c = Counter(e.get("type") for e in evts if isinstance(e, dict))
    return dict(c)

def extract_pokemon_info(battle: dict) -> List[dict]:
    """Extrae informacion detallada de Pokemon de una batalla."""
    pokemon_info = []
    teams = get_in(battle, ["team_revelation", "teams"], {})
    
    for player_id, team in teams.items():
        if isinstance(team, list):
            for pokemon in team:
                info = {
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
    
    for turn in turns:
        events = turn.get('events', [])
        for event in events:
            if event.get('type') == 'move':
                move_events += 1
            elif event.get('type') == 'switch':
                switch_events += 1
    
    return {
        'total_turns': total_turns,
        'total_events': total_events,
        'move_events': move_events,
        'switch_events': switch_events,
        'winner': winner,
        'reason': reason,
        'events_per_turn': total_events / max(total_turns, 1)
    }


# =============================================================================
# 1. CONSOLIDACION Y CARGA DE DATOS
# =============================================================================

def consolidate_jsons(battles_dir: Path = BATTLES_DIR, output_path: Path = ALL_BATTLES_JSON) -> None:
    assert battles_dir.exists() and battles_dir.is_dir(), f"No existe el directorio: {battles_dir.resolve()}"
    json_files = sorted(battles_dir.glob("*.json"))
    print(f"Archivos encontrados: {len(json_files)}")
    for p in json_files[:3]:
        print(f"- {p.name}")

    battles_data: List[dict] = []
    errores = 0
    for file in json_files:
        try:
            with open(file, "r") as f:
                battle = json.load(f)
                battles_data.append(battle)
        except Exception as e:
            errores += 1
            print(f"[WARN] Error al procesar {file.name}: {e}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(battles_data, f, indent=2)

    print(f"Archivo consolidado guardado en: {output_path.resolve()}")
    print(f"Batallas válidas: {len(battles_data)} | Errores: {errores}")


# =============================================================================
# 2. ANALISIS EXPLORATORIO DE DATOS (EDA)
# =============================================================================

def load_all_battles(path: Path = ALL_BATTLES_JSON) -> List[dict]:
    assert path.exists(), f"No existe {path.resolve()}. Ejecuta 'consolidate' primero."
    with open(path, "r") as f:
        return json.load(f)


def preview_first_battle(battles: Optional[List[dict]] = None) -> None:
    if battles is None:
        battles = load_all_battles()
    assert len(battles) > 0, "No hay batallas en el archivo consolidado."

    first = battles[0]
    print("Claves nivel 1:", list(first.keys()))

    for key in ["metadata", "players", "summary"]:
        v = first.get(key)
        print(f"\n== {key} ==")
        if isinstance(v, dict):
            keys = list(v.keys())[:30]
            print("keys:", keys)
            # Mostrar algunos valores escalares
            for k in keys[:5]:
                val = v.get(k)
                if isinstance(val, (dict, list)):
                    t = type(val)
                    print(f" - {k}: ", t, "(nested)")
                else:
                    print(f" - {k}: ", type(val), val)
        else:
            print(type(v), v)

    turns = first.get("turns", [])
    print(f"\nturns: tipo={type(turns)}, len={len(turns)}")
    if turns and isinstance(turns[0], dict):
        print("keys turno[0]:", list(turns[0].keys())[:30])
        # Aplanado de primer combate (nivel 1)
        battle_preview = pd.json_normalize([first], sep=".")
        print("\nAplanado por-combate (primeras columnas):")
        print(battle_preview.columns.tolist()[:20])

        # Aplanado por turno del primer combate
        turns_df = pd.json_normalize(turns, sep=".")
        turns_df["events_count"] = turns_df["events"].apply(lambda x: len(x) if isinstance(x, list) else 0)
        turns_df["event_types"] = turns_df["events"].apply(event_type_counts)
        turns_df["n_moves"] = turns_df["event_types"].apply(lambda d: d.get("move", 0) if isinstance(d, dict) else 0)
        turns_df["n_switch"] = turns_df["event_types"].apply(lambda d: d.get("switch", 0) if isinstance(d, dict) else 0)
        turns_df["n_stat_change"] = turns_df["event_types"].apply(lambda d: d.get("stat_change", 0) if isinstance(d, dict) else 0)

        # Columnas aplanadas para estado tras turno
        for col, default in [
            ("state_after.field.weather", pd.NA),
            ("state_after.field.global_conditions", []),
            ("state_after.sides.p1.side_conditions", []),
            ("state_after.sides.p2.side_conditions", []),
        ]:
            if col not in turns_df.columns:
                turns_df[col] = default

        cols_turn = [
            "turn_number",
            "events_count",
            "n_moves",
            "n_switch",
            "n_stat_change",
            "state_after.field.weather",
            "state_after.field.global_conditions",
            "state_after.sides.p1.side_conditions",
            "state_after.sides.p2.side_conditions",
        ]
        cols_turn = [c for c in cols_turn if c in turns_df.columns]
        print("\nPreview por-turno (primeros 10):")
        print(turns_df[cols_turn].sort_values("turn_number").head(10))


# -----------------------------
# Flatten All
# -----------------------------

def flatten_battles_and_turns(battles: Optional[List[dict]] = None,
                               out_battles: Path = DATA_DIR / "battles_flat.parquet",
                               out_turns: Path = DATA_DIR / "turns_flat.parquet") -> None:
    if battles is None:
        battles = load_all_battles()

    # Por-combate
    battles_flat = pd.json_normalize(battles, sep=".")
    cols_battle = [
        "battle_id",
        "format_id",
        "schema_version",
        "metadata.total_turns",
        "metadata.timestamp_unix",
        "metadata.outcome.winner",
        "metadata.outcome.reason",
        "summary.pokemon_used.p1",
        "summary.pokemon_used.p2",
        "summary.fainted_order.p1",
        "summary.fainted_order.p2",
    ]
    cols_battle = [c for c in cols_battle if c in battles_flat.columns]
    battles_final = battles_flat.reindex(columns=cols_battle)

    # Por-turno
    turns_full = pd.json_normalize(
        battles,
        record_path=["turns"],
        meta=[
            "battle_id",
            "format_id",
            ["metadata", "timestamp_unix"],
            ["metadata", "total_turns"],
        ],
        sep=".",
    )
    turns_full["events_count"] = turns_full["events"].apply(lambda x: len(x) if isinstance(x, list) else 0)
    turns_full["event_types"] = turns_full["events"].apply(event_type_counts)
    turns_full["n_moves"] = turns_full["event_types"].apply(lambda d: d.get("move", 0) if isinstance(d, dict) else 0)
    turns_full["n_switch"] = turns_full["event_types"].apply(lambda d: d.get("switch", 0) if isinstance(d, dict) else 0)
    turns_full["n_stat_change"] = turns_full["event_types"].apply(lambda d: d.get("stat_change", 0) if isinstance(d, dict) else 0)

    for col, default in [
        ("state_after.field.weather", pd.NA),
        ("state_after.field.global_conditions", []),
        ("state_after.sides.p1.side_conditions", []),
        ("state_after.sides.p2.side_conditions", []),
    ]:
        if col not in turns_full.columns:
            turns_full[col] = default

    cols_turn = [
        "battle_id",
        "format_id",
        "metadata.timestamp_unix",
        "metadata.total_turns",
        "turn_number",
        "events_count",
        "n_moves",
        "n_switch",
        "n_stat_change",
        "state_after.field.weather",
        "state_after.field.global_conditions",
        "state_after.sides.p1.side_conditions",
        "state_after.sides.p2.side_conditions",
    ]
    cols_turn = [c for c in cols_turn if c in turns_full.columns]
    turns_final = turns_full.reindex(columns=cols_turn).sort_values(["battle_id", "turn_number"])

    # Guardar
    out_battles.parent.mkdir(parents=True, exist_ok=True)
    battles_final.to_parquet(out_battles, index=False)
    turns_final.to_parquet(out_turns, index=False)

    print(f"Guardado por-combate: {out_battles.resolve()}  shape={battles_final.shape}")
    print(f"Guardado por-turno:   {out_turns.resolve()}    shape={turns_final.shape}")


# -----------------------------
# CLI
# -----------------------------

def main():
    parser = argparse.ArgumentParser(description="EDA de combates Pokémon Showdown")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("consolidate", help="Unifica los JSON en data/all_battles.json")
    sub.add_parser("preview-first", help="Muestra previews del primer combate")
    sub.add_parser("flatten-all", help="Genera parquet por-combate y por-turno")

    args = parser.parse_args()

    if args.cmd == "consolidate":
        consolidate_jsons()
    elif args.cmd == "preview-first":
        preview_first_battle()
    elif args.cmd == "flatten-all":
        flatten_battles_and_turns()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
