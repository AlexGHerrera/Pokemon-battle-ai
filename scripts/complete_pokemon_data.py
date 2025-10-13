#!/usr/bin/env python3
"""
Pokemon Data Completer - Automatic Pokemon Data Fetcher
========================================================

Completa automáticamente los Pokemon faltantes en pokemon_data.py
usando PokeAPI para obtener datos oficiales.

Características:
- Obtiene tipos y stats de PokeAPI
- Maneja formas alternativas y regionales
- Genera código Python listo para copiar
- Backup automático de pokemon_data.py
- Validación de datos

Uso:
    python scripts/complete_pokemon_data.py --top 50
    python scripts/complete_pokemon_data.py --all
    python scripts/complete_pokemon_data.py --species "Oricorio,Tauros,Deoxys"
"""

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import requests
from collections import defaultdict

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data.pokemon_data import POKEMON_TYPES, POKEMON_BST


class PokeAPIClient:
    """Cliente para interactuar con PokeAPI."""
    
    BASE_URL = "https://pokeapi.co/api/v2"
    
    # Mapeo de nombres especiales que difieren en PokeAPI
    NAME_MAPPING = {
        'Deoxys': 'deoxys-normal',
        'Oricorio': 'oricorio-baile',
        'Tauros': 'tauros',
        'Wormadam': 'wormadam-plant',
        'Giratina': 'giratina-altered',
        'Shaymin': 'shaymin-land',
        'Basculin': 'basculin-red-striped',
        'Darmanitan': 'darmanitan-standard',
        'Tornadus': 'tornadus-incarnate',
        'Thundurus': 'thundurus-incarnate',
        'Landorus': 'landorus-incarnate',
        'Keldeo': 'keldeo-ordinary',
        'Meloetta': 'meloetta-aria',
        'Meowstic': 'meowstic-male',
        'Aegislash': 'aegislash-shield',
        'Pumpkaboo': 'pumpkaboo-average',
        'Gourgeist': 'gourgeist-average',
        'Zygarde': 'zygarde-50',
        'Hoopa': 'hoopa-confined',
        'Oricorio-Pom-Pom': 'oricorio-pom-pom',
        'Oricorio-Pau': 'oricorio-pau',
        'Oricorio-Sensu': 'oricorio-sensu',
        'Lycanroc': 'lycanroc-midday',
        'Wishiwashi': 'wishiwashi-solo',
        'Minior': 'minior-red-meteor',
        'Mimikyu': 'mimikyu-disguised',
        'Toxtricity': 'toxtricity-amped',
        'Eiscue': 'eiscue-ice',
        'Indeedee': 'indeedee-male',
        'Morpeko': 'morpeko-full-belly',
        'Urshifu': 'urshifu-single-strike',
        'Basculegion': 'basculegion-male',
        'Enamorus': 'enamorus-incarnate',
        'Oinkologne': 'oinkologne-male',
        'Maushold': 'maushold-family-of-four',
        'Squawkabilly': 'squawkabilly-green-plumage',
        'Palafin': 'palafin-zero',
        'Tatsugiri': 'tatsugiri-curly',
        'Dudunsparce': 'dudunsparce-two-segment',
        'Gimmighoul': 'gimmighoul-chest',
    }
    
    def __init__(self, cache_dir: Optional[Path] = None):
        self.cache_dir = cache_dir or Path(__file__).parent.parent / "data" / ".pokeapi_cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.session = requests.Session()
    
    def _get_cache_path(self, endpoint: str, identifier: str) -> Path:
        """Obtiene la ruta del cache para un recurso."""
        safe_id = identifier.replace("/", "_").replace(" ", "_").lower()
        return self.cache_dir / f"{endpoint}_{safe_id}.json"
    
    def _get_cached(self, endpoint: str, identifier: str) -> Optional[Dict]:
        """Obtiene datos del cache si existen."""
        cache_path = self._get_cache_path(endpoint, identifier)
        if cache_path.exists():
            with open(cache_path, 'r') as f:
                return json.load(f)
        return None
    
    def _save_cache(self, endpoint: str, identifier: str, data: Dict):
        """Guarda datos en el cache."""
        cache_path = self._get_cache_path(endpoint, identifier)
        with open(cache_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_pokemon(self, name_or_id: str) -> Optional[Dict]:
        """
        Obtiene información de un Pokemon de PokeAPI.
        
        Args:
            name_or_id: Nombre o ID del Pokemon
            
        Returns:
            Diccionario con datos del Pokemon o None si no existe
        """
        # Aplicar mapeo de nombres especiales
        if name_or_id in self.NAME_MAPPING:
            normalized = self.NAME_MAPPING[name_or_id]
        else:
            # Normalizar nombre para PokeAPI
            normalized = name_or_id.lower().replace(" ", "-").replace("'", "")
        
        # Intentar obtener del cache
        cached = self._get_cached("pokemon", normalized)
        if cached:
            return cached
        
        # Obtener de API
        url = f"{self.BASE_URL}/pokemon/{normalized}"
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                self._save_cache("pokemon", normalized, data)
                return data
            elif response.status_code == 404:
                print(f"  ⚠️  Pokemon no encontrado en PokeAPI: {name_or_id}")
                return None
            else:
                print(f"  ❌ Error {response.status_code} para {name_or_id}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"  ❌ Error de conexión para {name_or_id}: {e}")
            return None
    
    def get_pokemon_species(self, name_or_id: str) -> Optional[Dict]:
        """Obtiene información de especie (para nombres, etc)."""
        normalized = name_or_id.lower().replace(" ", "-").replace("'", "")
        
        cached = self._get_cached("species", normalized)
        if cached:
            return cached
        
        url = f"{self.BASE_URL}/pokemon-species/{normalized}"
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                self._save_cache("species", normalized, data)
                return data
        except:
            pass
        return None


class PokemonDataCompleter:
    """Completa datos de Pokemon faltantes."""
    
    def __init__(self, api_client: PokeAPIClient):
        self.api = api_client
        self.completed = []
        self.failed = []
        self.skipped = []
    
    def extract_pokemon_data(self, species_name: str) -> Optional[Dict]:
        """
        Extrae tipos y BST de un Pokemon desde PokeAPI.
        
        Returns:
            Dict con 'types' y 'bst' o None si falla
        """
        print(f"  🔍 Buscando: {species_name}")
        
        # Obtener datos del Pokemon
        pokemon_data = self.api.get_pokemon(species_name)
        if not pokemon_data:
            return None
        
        # Extraer tipos
        types = []
        for type_data in pokemon_data.get('types', []):
            type_name = type_data['type']['name'].capitalize()
            types.append(type_name)
        
        # Extraer stats y calcular BST
        stats = pokemon_data.get('stats', [])
        bst = sum(stat['base_stat'] for stat in stats)
        
        # Información adicional
        height = pokemon_data.get('height', 0) / 10  # decímetros a metros
        weight = pokemon_data.get('weight', 0) / 10  # hectogramos a kg
        
        result = {
            'species': species_name,
            'types': types,
            'bst': bst,
            'height': height,
            'weight': weight,
            'abilities': [a['ability']['name'] for a in pokemon_data.get('abilities', [])]
        }
        
        print(f"  ✅ {species_name}: {types} | BST: {bst}")
        return result
    
    def complete_missing_pokemon(self, missing_list: List[Tuple[str, int]], 
                                 limit: Optional[int] = None) -> List[Dict]:
        """
        Completa datos de Pokemon faltantes.
        
        Args:
            missing_list: Lista de tuplas (species, appearances)
            limit: Límite de Pokemon a procesar (None = todos)
            
        Returns:
            Lista de Pokemon completados con sus datos
        """
        completed_data = []
        total = len(missing_list) if limit is None else min(limit, len(missing_list))
        
        print(f"\n🚀 Completando datos de {total} Pokemon...")
        print("="*80)
        
        for i, (species, appearances) in enumerate(missing_list[:limit], 1):
            print(f"\n[{i}/{total}] {species} ({appearances:,} apariciones)")
            
            # Verificar si ya existe
            if species in POKEMON_TYPES:
                print(f"  ⏭️  Ya existe en pokemon_data.py")
                self.skipped.append(species)
                continue
            
            # Obtener datos
            data = self.extract_pokemon_data(species)
            
            if data:
                data['appearances'] = appearances
                completed_data.append(data)
                self.completed.append(species)
            else:
                self.failed.append(species)
            
            # Rate limiting (PokeAPI: 100 req/min)
            if i < total:
                time.sleep(0.6)  # ~100 requests per minute
        
        return completed_data
    
    def generate_python_code(self, completed_data: List[Dict]) -> Tuple[str, str]:
        """
        Genera código Python para agregar a pokemon_data.py.
        
        Returns:
            Tupla (código_types, código_bst)
        """
        if not completed_data:
            return "", ""
        
        # Ordenar por apariciones (más usados primero)
        completed_data.sort(key=lambda x: x['appearances'], reverse=True)
        
        # Generar código para POKEMON_TYPES
        types_code = []
        types_code.append("# === Pokemon completados automáticamente ===")
        types_code.append(f"# Generado: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        types_code.append(f"# Total: {len(completed_data)} Pokemon")
        types_code.append("")
        
        for data in completed_data:
            types_str = str(data['types'])
            comment = f"# {data['appearances']:,} apariciones"
            types_code.append(f"    '{data['species']}': {types_str},  {comment}")
        
        # Generar código para POKEMON_BST
        bst_code = []
        bst_code.append("# === BST de Pokemon completados ===")
        bst_code.append(f"# Generado: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        bst_code.append("")
        
        for data in completed_data:
            bst_code.append(f"    '{data['species']}': {data['bst']},")
        
        return "\n".join(types_code), "\n".join(bst_code)
    
    def save_to_file(self, completed_data: List[Dict], output_path: Path):
        """Guarda datos completados en un archivo JSON."""
        output_data = {
            'generated_at': time.strftime('%Y-%m-%d %H:%M:%S'),
            'total_completed': len(completed_data),
            'pokemon': completed_data
        }
        
        with open(output_path, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        print(f"\n💾 Datos guardados en: {output_path}")


def load_missing_pokemon(csv_path: Path) -> List[Tuple[str, int]]:
    """Carga lista de Pokemon faltantes desde CSV."""
    import csv
    
    missing = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            species = row['species']
            appearances = int(row['appearances'])
            missing.append((species, appearances))
    
    return missing


def backup_pokemon_data(source_path: Path, backup_dir: Path):
    """Crea backup de pokemon_data.py."""
    backup_dir.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime('%Y%m%d_%H%M%S')
    backup_path = backup_dir / f"pokemon_data_backup_{timestamp}.py"
    
    import shutil
    shutil.copy2(source_path, backup_path)
    print(f"✅ Backup creado: {backup_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Completa automáticamente Pokemon faltantes en pokemon_data.py"
    )
    parser.add_argument(
        '--top', 
        type=int, 
        help='Completar solo los N Pokemon más usados'
    )
    parser.add_argument(
        '--all', 
        action='store_true',
        help='Completar todos los Pokemon faltantes'
    )
    parser.add_argument(
        '--species',
        type=str,
        help='Completar Pokemon específicos (separados por coma)'
    )
    parser.add_argument(
        '--no-backup',
        action='store_true',
        help='No crear backup de pokemon_data.py'
    )
    parser.add_argument(
        '--output',
        type=str,
        help='Archivo de salida para código generado (default: output/pokemon_completed.txt)'
    )
    
    args = parser.parse_args()
    
    # Paths
    project_root = Path(__file__).parent.parent
    csv_path = project_root / "output" / "pokemon_missing.csv"
    pokemon_data_path = project_root / "src" / "data" / "pokemon_data.py"
    output_dir = project_root / "output"
    backup_dir = project_root / "backups"
    
    print("🔥 Pokemon Data Completer")
    print("="*80)
    
    # Verificar que existe el CSV de Pokemon faltantes
    if not csv_path.exists():
        print(f"❌ No se encontró {csv_path}")
        print("   Ejecuta primero: python scripts/analyze_pokemon_coverage.py")
        return 1
    
    # Crear backup
    if not args.no_backup:
        print("\n📦 Creando backup de pokemon_data.py...")
        backup_pokemon_data(pokemon_data_path, backup_dir)
    
    # Cargar Pokemon faltantes
    print(f"\n📂 Cargando Pokemon faltantes desde: {csv_path.name}")
    missing_pokemon = load_missing_pokemon(csv_path)
    print(f"✅ {len(missing_pokemon)} Pokemon faltantes identificados")
    
    # Determinar cuántos completar
    if args.species:
        # Pokemon específicos
        species_list = [s.strip() for s in args.species.split(',')]
        missing_pokemon = [(s, 0) for s in species_list]
        limit = len(species_list)
        print(f"\n🎯 Modo: Pokemon específicos ({limit} especies)")
    elif args.all:
        limit = None
        print(f"\n🎯 Modo: Completar TODOS ({len(missing_pokemon)} Pokemon)")
    elif args.top:
        limit = args.top
        print(f"\n🎯 Modo: Top {limit} Pokemon más usados")
    else:
        # Default: Top 50
        limit = 50
        print(f"\n🎯 Modo: Top {limit} Pokemon más usados (default)")
    
    # Inicializar cliente API
    print("\n🌐 Inicializando cliente PokeAPI...")
    api_client = PokeAPIClient()
    completer = PokemonDataCompleter(api_client)
    
    # Completar Pokemon
    completed_data = completer.complete_missing_pokemon(missing_pokemon, limit)
    
    # Generar código Python
    print("\n" + "="*80)
    print("📝 GENERANDO CÓDIGO PYTHON")
    print("="*80)
    
    types_code, bst_code = completer.generate_python_code(completed_data)
    
    # Guardar en archivo
    output_path = Path(args.output) if args.output else output_dir / "pokemon_completed.txt"
    with open(output_path, 'w') as f:
        f.write("# ============================================\n")
        f.write("# CÓDIGO PARA AGREGAR A pokemon_data.py\n")
        f.write("# ============================================\n\n")
        f.write("# 1. Agregar a POKEMON_TYPES (después de línea 378):\n\n")
        f.write(types_code)
        f.write("\n\n")
        f.write("# 2. Agregar a POKEMON_BST (después de línea 610):\n\n")
        f.write(bst_code)
        f.write("\n")
    
    print(f"\n💾 Código generado guardado en: {output_path}")
    
    # Guardar datos completos en JSON
    json_path = output_dir / "pokemon_completed.json"
    completer.save_to_file(completed_data, json_path)
    
    # Resumen final
    print("\n" + "="*80)
    print("📊 RESUMEN FINAL")
    print("="*80)
    print(f"✅ Pokemon completados:  {len(completer.completed)}")
    print(f"⏭️  Pokemon omitidos:     {len(completer.skipped)}")
    print(f"❌ Pokemon fallidos:     {len(completer.failed)}")
    
    if completer.failed:
        print(f"\n⚠️  Pokemon que fallaron:")
        for species in completer.failed:
            print(f"   - {species}")
    
    print("\n" + "="*80)
    print("🎯 PRÓXIMOS PASOS")
    print("="*80)
    print(f"1. Revisar código generado: {output_path}")
    print(f"2. Copiar código a: {pokemon_data_path}")
    print(f"3. Verificar que no hay duplicados")
    print(f"4. Ejecutar: python scripts/analyze_pokemon_coverage.py")
    print(f"5. Verificar nueva cobertura")
    
    if not args.no_backup:
        print(f"\n💡 Si algo sale mal, restaurar desde: {backup_dir}/")
    
    return 0 if not completer.failed else 1


if __name__ == "__main__":
    sys.exit(main())
