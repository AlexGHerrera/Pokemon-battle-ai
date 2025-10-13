#!/usr/bin/env python3
"""
Pokemon Coverage Analysis Script
=================================

Analiza el dataset completo de batallas para identificar:
1. Todos los Pokemon únicos que aparecen
2. Pokemon que faltan en pokemon_data.py
3. Frecuencia de uso de cada Pokemon
4. Sugerencias de tipos y BST basados en datos oficiales

Uso:
    python scripts/analyze_pokemon_coverage.py
"""

import json
import sys
from pathlib import Path
from collections import Counter
from typing import Dict, List, Set, Tuple
import pandas as pd

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data.pokemon_data import POKEMON_TYPES, POKEMON_BST


def load_battles(data_path: Path) -> List[Dict]:
    """Carga el dataset de batallas."""
    json_path = data_path / "all_battles.json"
    
    if not json_path.exists():
        print(f"❌ No se encontró {json_path}")
        print("   Intentando con battles_sample_2000.json...")
        json_path = data_path / "battles_sample_2000.json"
        
        if not json_path.exists():
            raise FileNotFoundError("No se encontró ningún archivo de batallas")
    
    print(f"📂 Cargando batallas desde: {json_path.name}")
    with open(json_path, 'r') as f:
        battles = json.load(f)
    
    print(f"✅ Cargadas {len(battles):,} batallas")
    return battles


def extract_pokemon_from_battle(battle: Dict) -> List[str]:
    """Extrae todos los Pokemon de una batalla."""
    pokemon_list = []
    
    # Extraer de team_revelation 
    if 'team_revelation' in battle and 'teams' in battle['team_revelation']:
        teams = battle['team_revelation']['teams']
        for player in ['p1', 'p2']:
            if player in teams:
                for pokemon in teams[player]:
                    if 'species' in pokemon:
                        species = pokemon['species']
                        pokemon_list.append(species)
    
    return pokemon_list


def analyze_pokemon_coverage(battles: List[Dict]) -> Tuple[Counter, Set, Set]:
    """
    Analiza la cobertura de Pokemon en el dataset.
    
    Returns:
        - Counter con frecuencia de cada Pokemon
        - Set de Pokemon en el dataset
        - Set de Pokemon faltantes en pokemon_data.py
    """
    print("\n🔍 Analizando Pokemon en el dataset...")
    
    all_pokemon = []
    for battle in battles:
        all_pokemon.extend(extract_pokemon_from_battle(battle))
    
    # Contar frecuencias
    pokemon_counter = Counter(all_pokemon)
    dataset_pokemon = set(pokemon_counter.keys())
    
    # Pokemon en pokemon_data.py
    registered_pokemon = set(POKEMON_TYPES.keys())
    
    # Pokemon faltantes
    missing_pokemon = dataset_pokemon - registered_pokemon
    
    print(f"✅ Pokemon únicos en dataset: {len(dataset_pokemon)}")
    print(f"✅ Pokemon en pokemon_data.py: {len(registered_pokemon)}")
    print(f"⚠️  Pokemon faltantes: {len(missing_pokemon)}")
    
    return pokemon_counter, dataset_pokemon, missing_pokemon


def get_pokemon_official_data(species: str) -> Dict:
    """
    Obtiene datos oficiales de un Pokemon desde una API o base de datos.
    Por ahora, retorna estructura vacía para completar manualmente.
    """
    # TODO: Integrar con PokeAPI o base de datos oficial
    return {
        'species': species,
        'types': ['Unknown'],  # Completar manualmente
        'bst': 0,  # Completar manualmente
        'tier': 'Unknown'
    }


def generate_report(pokemon_counter: Counter, missing_pokemon: Set) -> None:
    """Genera reporte detallado de cobertura."""
    
    print("\n" + "="*80)
    print("📊 REPORTE DE COBERTURA DE POKEMON")
    print("="*80)
    
    # Top 20 Pokemon más usados
    print("\n🏆 TOP 20 POKEMON MÁS USADOS EN EL DATASET:")
    print("-" * 80)
    for i, (species, count) in enumerate(pokemon_counter.most_common(20), 1):
        in_db = "✅" if species in POKEMON_TYPES else "❌"
        types = POKEMON_TYPES.get(species, ['Unknown'])
        bst = POKEMON_BST.get(species, 0)
        print(f"{i:2d}. {in_db} {species:25s} - {count:5,} usos | Tipos: {types} | BST: {bst}")
    
    # Pokemon faltantes ordenados por frecuencia
    if missing_pokemon:
        print("\n⚠️  POKEMON FALTANTES EN pokemon_data.py:")
        print("-" * 80)
        print(f"Total: {len(missing_pokemon)} Pokemon")
        print()
        
        missing_sorted = [(species, pokemon_counter[species]) 
                         for species in missing_pokemon]
        missing_sorted.sort(key=lambda x: x[1], reverse=True)
        
        print("Ordenados por frecuencia de uso:")
        for i, (species, count) in enumerate(missing_sorted, 1):
            print(f"{i:3d}. {species:30s} - {count:5,} usos")
        
        # Generar código Python para agregar
        print("\n" + "="*80)
        print("📝 CÓDIGO PYTHON PARA AGREGAR A pokemon_data.py:")
        print("="*80)
        print("\n# Pokemon faltantes identificados por analyze_pokemon_coverage.py")
        print("# TODO: Completar tipos y BST correctos\n")
        
        for species, count in missing_sorted[:10]:  # Top 10 más importantes
            print(f"    '{species}': ['Unknown'],  # {count:,} usos - COMPLETAR TIPOS")
    else:
        print("\n✅ ¡EXCELENTE! Todos los Pokemon del dataset están en pokemon_data.py")
    
    # Estadísticas generales
    print("\n" + "="*80)
    print("📈 ESTADÍSTICAS GENERALES:")
    print("="*80)
    total_pokemon = len(pokemon_counter)
    registered = len(set(pokemon_counter.keys()) & set(POKEMON_TYPES.keys()))
    coverage_pct = (registered / total_pokemon * 100) if total_pokemon > 0 else 0
    
    print(f"Pokemon únicos en dataset:     {total_pokemon:4d}")
    print(f"Pokemon registrados:           {registered:4d}")
    print(f"Pokemon faltantes:             {len(missing_pokemon):4d}")
    print(f"Cobertura:                     {coverage_pct:5.1f}%")
    
    total_appearances = sum(pokemon_counter.values())
    missing_appearances = sum(pokemon_counter[p] for p in missing_pokemon)
    missing_pct = (missing_appearances / total_appearances * 100) if total_appearances > 0 else 0
    
    print(f"\nApariciones totales:           {total_appearances:,}")
    print(f"Apariciones de faltantes:      {missing_appearances:,}")
    print(f"% de apariciones faltantes:    {missing_pct:5.2f}%")


def export_to_csv(pokemon_counter: Counter, missing_pokemon: Set, output_dir: Path) -> None:
    """Exporta resultados a CSV para análisis posterior."""
    
    # Crear DataFrame con todos los Pokemon
    data = []
    for species, count in pokemon_counter.items():
        data.append({
            'species': species,
            'appearances': count,
            'in_pokemon_data': species in POKEMON_TYPES,
            'types': str(POKEMON_TYPES.get(species, ['Unknown'])),
            'bst': POKEMON_BST.get(species, 0),
            'status': 'Registered' if species in POKEMON_TYPES else 'Missing'
        })
    
    if not data:
        print("⚠️  No hay datos para exportar")
        return
    
    df = pd.DataFrame(data)
    df = df.sort_values('appearances', ascending=False)
    
    # Exportar
    output_file = output_dir / 'pokemon_coverage_analysis.csv'
    df.to_csv(output_file, index=False)
    print(f"\n💾 Análisis exportado a: {output_file}")
    
    # Exportar solo faltantes
    if missing_pokemon:
        df_missing = df[df['status'] == 'Missing']
        missing_file = output_dir / 'pokemon_missing.csv'
        df_missing.to_csv(missing_file, index=False)
        print(f"💾 Pokemon faltantes exportados a: {missing_file}")


def main():
    """Función principal."""
    print("🔥 Pokemon Coverage Analysis Tool")
    print("="*80)
    
    # Paths
    project_root = Path(__file__).parent.parent
    data_dir = project_root / "data"
    output_dir = project_root / "output"
    
    try:
        # Cargar batallas
        battles = load_battles(data_dir)
        
        # Analizar cobertura
        pokemon_counter, dataset_pokemon, missing_pokemon = analyze_pokemon_coverage(battles)
        
        # Generar reporte
        generate_report(pokemon_counter, missing_pokemon)
        
        # Exportar a CSV
        export_to_csv(pokemon_counter, missing_pokemon, output_dir)
        
        print("\n" + "="*80)
        print("✅ Análisis completado exitosamente")
        print("="*80)
        
        # Retornar código de salida
        return 0 if len(missing_pokemon) == 0 else 1
        
    except Exception as e:
        print(f"\n❌ Error durante el análisis: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
