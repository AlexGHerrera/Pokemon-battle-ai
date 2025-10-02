# %% [markdown]
# # 🤖 Pokemon Battle AI - La Búsqueda del Modelo Definitivo
# 
# En el mundo de las batallas Pokemon, cada decisión cuenta. Cada movimiento, cada cambio, cada estrategia puede determinar la diferencia entre la victoria y la derrota. Nuestro viaje hasta ahora nos ha llevado desde el análisis exploratorio hasta un baseline sólido con **ROC-AUC de 0.837**.
# 
# Pero sabemos que podemos hacer mejor. Mucho mejor.
# 
# ## 🎯 La Misión: Superar lo Imposible
# 
# Hoy emprendemos la fase más emocionante de nuestro proyecto: **crear el modelo de Machine Learning más avanzado** para predecir batallas Pokemon. No nos conformamos con modelos simples; vamos a desplegar un arsenal completo de algoritmos de última generación.
# 
# ### 🗺️ Nuestro Plan de Batalla
# 
# Como entrenadores Pokemon experimentados, sabemos que la preparación es clave. Nuestro plan de entrenamiento seguirá una estrategia meticulosa:
# 
# **🔧 Fase 1: Preparación del Campo de Batalla**
# - Refinamiento de características basado en insights del EDA
# - Ingeniería de features que capturen la esencia de cada batalla
# - Selección inteligente de variables predictivas
# 
# **⚔️ Fase 2: Despliegue del Arsenal Base**
# - Logistic Regression: La elegancia de la simplicidad
# - Random Forest: El poder de la sabiduría colectiva
# - SVM: La precisión matemática en acción
# 
# **🚀 Fase 3: Armas de Destrucción Masiva**
# - XGBoost: El campeón de Kaggle
# - LightGBM: Velocidad y precisión combinadas
# - Neural Networks: La inteligencia artificial pura
# 
# **⚙️ Fase 4: Perfeccionamiento Táctico**
# - Hyperparameter tuning con búsqueda inteligente
# - Cross-validation para robustez máxima
# - Análisis profundo de curvas de aprendizaje
# 
# **🤝 Fase 5: La Unión Hace la Fuerza**
# - Ensemble de los mejores modelos
# - Voting strategies para decisiones consensuadas
# - Meta-learning para superar límites individuales
# 
# **🏆 Fase 6: El Momento de la Verdad**
# - Evaluación exhaustiva contra el baseline
# - Análisis de errores y casos límite
# - Selección del modelo campeón
# 
# ¿Lograremos superar el **ROC-AUC de 0.837**? ¿Cuánto podremos mejorar? El viaje comienza ahora…

# %% [markdown]
# ## 📦 Armando Nuestro Arsenal: Las Herramientas del Maestro
# 
# Como cualquier entrenador Pokemon sabe, tener las herramientas adecuadas es fundamental para el éxito. En nuestro laboratorio de Machine Learning, cada librería es como un Pokemon especializado, cada una con sus propias habilidades únicas.
# 
# Vamos a importar nuestro equipo completo:
# - **Pandas & NumPy**: Nuestros Pikachu y Charizard, confiables y poderosos para manipulación de datos
# - **Scikit-learn**: El Mew de ML, versátil y con acceso a casi cualquier algoritmo
# - **XGBoost & LightGBM**: Los legendarios Rayquaza y Kyogre del gradient boosting
# - **Matplotlib & Seaborn**: Nuestros artistas Smeargle, creando visualizaciones que cuentan historias
# 
# Cada importación nos acerca más a nuestro objetivo: crear el modelo más poderoso jamás visto en batallas Pokemon.

# %%
# Librerías básicas
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Machine Learning
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import (
    train_test_split, cross_val_score, GridSearchCV, 
    StratifiedKFold, RandomizedSearchCV
)
from sklearn.preprocessing import StandardScaler, RobustScaler, LabelEncoder
from sklearn.metrics import (
    roc_auc_score, accuracy_score, precision_score, recall_score, 
    f1_score, classification_report, confusion_matrix, roc_curve, auc
)
from sklearn.feature_selection import SelectKBest, f_classif, RFE, SelectFromModel

# Modelos avanzados
import xgboost as xgb
import lightgbm as lgb

# Utilidades
import json
import pickle
from pathlib import Path
from datetime import datetime
import logging

# Configuración de visualización
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

# Colores Pokemon
POKEMON_COLORS = {
    'fire': '#FF6B35',
    'water': '#4A90E2', 
    'grass': '#7ED321',
    'electric': '#F5A623',
    'psychic': '#BD10E0',
    'ice': '#50E3C2',
    'dragon': '#9013FE',
    'dark': '#4A4A4A',
    'fighting': '#D0021B',
    'poison': '#B8E986'
}

# Detectar entorno de ejecución
import os
IS_KAGGLE = 'KAGGLE_KERNEL_RUN_TYPE' in os.environ
WORKING_DIR = "/kaggle/working" if IS_KAGGLE else "."

print("✅ Librerías importadas correctamente")
print(f"🌍 Entorno detectado: {'Kaggle' if IS_KAGGLE else 'Local'}")
print(f"📁 Directorio de trabajo: {WORKING_DIR}")

# %% [markdown]
# ## 📊 El Despertar de los Datos: Liberando el Arsenal Completo
# 
# Cada dataset cuenta una historia, y el nuestro es **absolutamente épico**. Hemos pasado del entrenamiento con una muestra a desatar **TODO EL PODER** de nuestro arsenal de datos completo. Ya no son solo 2000 batallas - ahora tenemos acceso a **TODAS las batallas Pokemon disponibles**.
# 
# Imagina por un momento: **Miles y miles de enfrentamientos únicos**, decenas de miles de decisiones críticas, cientos de Pokemon diferentes luchando por la gloria en una escala nunca antes vista. Desde batallas rápidas y decisivas hasta maratones épicos, tenemos la biblioteca completa de la experiencia competitiva Pokemon.
# 
# ### 🎭 Los Protagonistas de Nuestra Historia
# 
# Nuestros datos no son simples números; son las memorias digitales de entrenadores que:
# - Tomaron decisiones bajo presión
# - Ejecutaron estrategias complejas
# - Experimentaron la emoción de la victoria y la amargura de la derrota
# 
# Cada log de batalla es como un pergamino antiguo que debemos descifrar. Cada evento registrado - cada movimiento, cada cambio, cada momento crítico - contiene pistas sobre qué hace que un entrenador triunfe sobre otro.
# 
# **¿Qué secretos revelarán estos datos a escala masiva?** Con este arsenal completo de batallas, nuestros modelos tendrán acceso a patrones que solo emergen con grandes volúmenes de datos. ¿Descubriremos estrategias meta que solo son visibles con miles de batallas? ¿Encontraremos correlaciones sutiles que se perdían en muestras más pequeñas?
# 
# **¡La aventura de entrenar con el dataset completo comienza ahora!** 🚀

# %%
# Cargar datos con estructura correcta (solución al problema de ganadores)
try:
    # Usar dataset público de Kaggle: pokemon-showdown-battles-gen9-randbats (~14,000 batallas)
    import glob
    
    # Usar dataset público de Kaggle con estructura correcta (archivos en raíz)
    possible_patterns = [
        "/kaggle/input/pokemon-showdown-battles-gen9-randbats/*.json",        # Dataset público (raíz) - CORRECTO
        "../data/battles/*.json",                                             # Archivos locales para desarrollo
        "/kaggle/input/*/parsed/*.json",                                      # Por si hay subcarpeta parsed/
        "/kaggle/input/*/*.json",                                             # Fallback general
    ]
    
    battle_files = []
    for pattern in possible_patterns:
        battle_files = glob.glob(pattern)
        if battle_files:
            print(f"✅ Encontrados archivos con patrón: {pattern}")
            break
    
    battles_data = []
    print(f"🔍 Encontrados {len(battle_files)} archivos de batalla")
    
    for i, file_path in enumerate(battle_files):
        try:
            with open(file_path, 'r') as f:
                battle = json.load(f)
                battles_data.append(battle)
            
            # Mostrar progreso cada 1000 archivos
            if (i + 1) % 1000 == 0:
                print(f"📊 Procesados {i + 1}/{len(battle_files)} archivos...")
                
        except Exception as e:
            print(f"⚠️ Error procesando {file_path}: {e}")
            continue
    
    print(f"✅ Datos cargados desde archivos individuales: {len(battles_data)} batallas")
    
except Exception as e:
    print(f"⚠️ Error cargando desde Kaggle: {e}")
    # Fallback local para desarrollo
    import glob
    battle_files = glob.glob("../data/battles/*.json")
    
    battles_data = []
    print(f"🔍 Encontrados {len(battle_files)} archivos locales")
    
    for i, file_path in enumerate(battle_files):
        try:
            with open(file_path, 'r') as f:
                battle = json.load(f)
                battles_data.append(battle)
                
            # Mostrar progreso cada 1000 archivos
            if (i + 1) % 1000 == 0:
                print(f"📊 Procesados {i + 1}/{len(battle_files)} archivos...")
                
        except Exception as e:
            print(f"⚠️ Error procesando {file_path}: {e}")
            continue
    
    print(f"✅ Dataset local cargado: {len(battles_data)} batallas")
    print(f"🚀 ¡Usando archivos individuales con diversidad de ganadores garantizada!")

# %% [markdown]
# ### 🔧 La Alquimia de los Datos: Transformando Batallas en Sabiduría
# 
# Ahora viene la parte más artística de nuestro proceso: la **ingeniería de características**. Como un alquimista medieval transformando metales comunes en oro, vamos a convertir logs de batalla crudos en features predictivas poderosas.
# 
# ### 🧬 Decodificando el ADN de una Batalla
# 
# Cada batalla Pokemon tiene su propio "ADN" - una secuencia única de eventos que la define. Nuestro trabajo es extraer la esencia de este ADN y convertirla en números que nuestros algoritmos puedan entender.
# 
# **¿Qué hace que una batalla sea única?**
# - **Intensidad**: ¿Fue una batalla rápida y brutal o un duelo prolongado de resistencia?
# - **Complejidad**: ¿Cuántos cambios estratégicos hubo? ¿Qué tan dinámica fue?
# - **Agresividad**: ¿Los entrenadores fueron directos o cautelosos?
# - **Adaptabilidad**: ¿Qué tan bien respondieron a las situaciones cambiantes?
# 
# ### 🎯 Las Métricas que Importan
# 
# Basándonos en nuestro análisis exploratorio previo, sabemos que ciertas métricas son cruciales:
# - **Eventos de movimiento**: El corazón de cada batalla
# - **Ratios de daño**: La eficiencia ofensiva
# - **Patrones de cambio**: La flexibilidad táctica
# - **Duración e intensidad**: El ritmo de la batalla
# 
# Cada feature que extraemos es como capturar la esencia de miles de decisiones estratégicas. ¿Lograremos capturar los patrones que separan a los maestros de los novatos?

# %%
def extract_battle_features(battles_data):
    """
    Extrae características numéricas de las batallas para ML.
    Basado en los hallazgos del EDA previo y estructura real de datos.
    """
    features_list = []
    
    def get_in(data, keys, default=None):
        """Función auxiliar para acceso seguro a datos anidados."""
        for key in keys:
            if isinstance(data, dict) and key in data:
                data = data[key]
            else:
                return default
        return data
    
    def calculate_battle_metrics(battle: dict) -> dict:
        """Calcula métricas clave de una batalla (copiado del EDA)."""
        metadata = battle.get('metadata', {})
        turns = battle.get('turns', [])
        
        # Métricas básicas
        total_turns = len(turns)
        winner = get_in(metadata, ['outcome', 'winner'])
        reason = get_in(metadata, ['outcome', 'reason'])
        
        # Análisis detallado de eventos
        total_events = 0
        move_events = 0
        switch_events = 0
        damage_events = 0
        effect_events = 0
        heal_events = 0
        status_events = 0
        
        # Métricas de momentum y timing
        early_game_events = 0  # Primeros 3 turnos
        mid_game_events = 0    # Turnos 4-8
        late_game_events = 0   # Turnos 9+
        
        # Patrones de decisión
        consecutive_moves = 0
        consecutive_switches = 0
        last_action_type = None
        current_streak = 0
        
        for turn_idx, turn in enumerate(turns):
            turn_events = turn.get('events', [])
            turn_event_count = len(turn_events)
            total_events += turn_event_count
            
            # Clasificar eventos por fase del juego
            if turn_idx < 3:
                early_game_events += turn_event_count
            elif turn_idx < 8:
                mid_game_events += turn_event_count
            else:
                late_game_events += turn_event_count
            
            # Analizar tipos de eventos
            for event in turn_events:
                event_type = event.get('type', '').lower()
                
                if event_type == 'move':
                    move_events += 1
                elif event_type == 'switch':
                    switch_events += 1
                elif 'damage' in event_type:
                    damage_events += 1
                elif 'heal' in event_type:
                    heal_events += 1
                elif 'faint' in event_type:
                    status_events += 1
                else:
                    effect_events += 1
                
                # Rastrear patrones consecutivos
                if event_type in ['move', 'switch']:
                    if event_type == last_action_type:
                        current_streak += 1
                    else:
                        if last_action_type == 'move':
                            consecutive_moves = max(consecutive_moves, current_streak)
                        elif last_action_type == 'switch':
                            consecutive_switches = max(consecutive_switches, current_streak)
                        current_streak = 1
                        last_action_type = event_type
        
        # Finalizar rastreo de patrones
        if last_action_type == 'move':
            consecutive_moves = max(consecutive_moves, current_streak)
        elif last_action_type == 'switch':
            consecutive_switches = max(consecutive_switches, current_streak)
        
        return {
            'total_turns': total_turns,
            'winner': winner,
            'reason': reason,
            'total_events': total_events,
            'move_events': move_events,
            'switch_events': switch_events,
            'damage_events': damage_events,
            'heal_events': heal_events,
            'status_events': status_events,
            'effect_events': effect_events,
            'events_per_turn': total_events / max(total_turns, 1),
            'early_game_intensity': early_game_events / max(min(total_turns, 3), 1),
            'mid_game_intensity': mid_game_events / max(min(total_turns - 3, 5), 1) if total_turns > 3 else 0,
            'late_game_intensity': late_game_events / max(total_turns - 8, 1) if total_turns > 8 else 0,
            'move_switch_ratio': move_events / max(switch_events, 1),
            'consecutive_moves': consecutive_moves,
            'consecutive_switches': consecutive_switches,
            'action_diversity': len(set([e.get('type') for turn in turns for e in turn.get('events', [])]))
        }
    
    def extract_team_composition_features(battle: dict) -> dict:
        """Extrae features de composición de equipos (copiado del EDA)."""
        teams = get_in(battle, ["team_revelation", "teams"], {})
        features = {}
        
        for player_id in ['p1', 'p2']:
            team = teams.get(player_id, [])
            if isinstance(team, list) and team:
                # Métricas básicas del equipo
                levels = [p.get('level', 0) for p in team if p.get('level')]
                hps = [get_in(p, ['base_stats', 'hp']) for p in team if get_in(p, ['base_stats', 'hp'])]
                
                # Estadísticas de nivel
                avg_level = np.mean(levels) if levels else 0
                level_std = np.std(levels) if len(levels) > 1 else 0
                
                # Estadísticas de HP
                avg_hp = np.mean(hps) if hps else 0
                hp_std = np.std(hps) if len(hps) > 1 else 0
                total_hp = sum(hps) if hps else 0
                
                # Diversidad y revelación
                species_count = len(set(p.get('species') for p in team if p.get('species')))
                fully_revealed = sum(1 for p in team if p.get('revelation_status') == 'fully_revealed')
                partially_revealed = sum(1 for p in team if p.get('revelation_status') == 'partially_revealed')
                
                # Información conocida
                known_abilities = sum(1 for p in team if p.get('known_ability'))
                known_items = sum(1 for p in team if p.get('known_item'))
                total_known_moves = sum(len(p.get('known_moves', [])) for p in team)
                
                features.update({
                    f'{player_id}_team_size': len(team),
                    f'{player_id}_avg_level': avg_level,
                    f'{player_id}_level_std': level_std,
                    f'{player_id}_min_level': min(levels) if levels else 0,
                    f'{player_id}_max_level': max(levels) if levels else 0,
                    f'{player_id}_avg_hp': avg_hp,
                    f'{player_id}_hp_std': hp_std,
                    f'{player_id}_total_hp': total_hp,
                    f'{player_id}_species_diversity': species_count,
                    f'{player_id}_fully_revealed': fully_revealed,
                    f'{player_id}_partially_revealed': partially_revealed,
                    f'{player_id}_known_abilities': known_abilities,
                    f'{player_id}_known_items': known_items,
                    f'{player_id}_total_known_moves': total_known_moves,
                    f'{player_id}_info_advantage': fully_revealed + partially_revealed * 0.5
                })
            else:
                # Valores por defecto si no hay datos del equipo
                for metric in ['team_size', 'avg_level', 'level_std', 'min_level', 'max_level', 
                              'avg_hp', 'hp_std', 'total_hp', 'species_diversity', 
                              'fully_revealed', 'partially_revealed', 'known_abilities', 
                              'known_items', 'total_known_moves', 'info_advantage']:
                    features[f'{player_id}_{metric}'] = 0
        
        return features
    
    # Procesar cada batalla
    for i, battle in enumerate(battles_data):
        try:
            # Métricas básicas mejoradas
            metrics = calculate_battle_metrics(battle)
            
            # Features de composición de equipos
            team_features = extract_team_composition_features(battle)
            
            # Combinar todas las features
            features = {
                'battle_id': battle.get('battle_id'),
                'format': battle.get('format_id', ''),
                'turns': metrics['total_turns'],
                'winner': metrics['winner'],
                'reason': metrics['reason'],
                'total_events': metrics['total_events'],
                'move_events': metrics['move_events'],
                'switch_events': metrics['switch_events'],
                'damage_events': metrics['damage_events'],
                'heal_events': metrics['heal_events'],
                'status_events': metrics['status_events'],
                'effect_events': metrics['effect_events'],
                'events_per_turn': metrics['events_per_turn'],
                'early_game_intensity': metrics['early_game_intensity'],
                'mid_game_intensity': metrics['mid_game_intensity'],
                'late_game_intensity': metrics['late_game_intensity'],
                'move_switch_ratio': metrics['move_switch_ratio'],
                'consecutive_moves': metrics['consecutive_moves'],
                'consecutive_switches': metrics['consecutive_switches'],
                'action_diversity': metrics['action_diversity']
            }
            
            # Información de jugadores
            players = battle.get('players', {})
            for player_id in ['p1', 'p2']:
                player_info = players.get(player_id, {})
                features[f'{player_id}_rating'] = player_info.get('ladder_rating_pre', 0)
            
            # Agregar features de composición de equipos
            features.update(team_features)
            
            # Features de ventaja competitiva
            if features['p1_rating'] and features['p2_rating']:
                features['rating_difference'] = abs(features['p1_rating'] - features['p2_rating'])
                features['rating_advantage_p1'] = features['p1_rating'] - features['p2_rating']
            else:
                features['rating_difference'] = 0
                features['rating_advantage_p1'] = 0
            
            # Features de balance de equipos
            features['team_size_difference'] = abs(features['p1_team_size'] - features['p2_team_size'])
            features['level_advantage_p1'] = features['p1_avg_level'] - features['p2_avg_level']
            features['hp_advantage_p1'] = features['p1_total_hp'] - features['p2_total_hp']
            features['info_advantage_p1'] = features['p1_info_advantage'] - features['p2_info_advantage']
            
            # Ratios importantes (corregidos)
            if features['total_events'] > 0:
                features['switch_ratio'] = features['switch_events'] / features['total_events']
                features['move_ratio'] = features['move_events'] / features['total_events']
                features['damage_ratio'] = features['damage_events'] / features['total_events']
            else:
                features['switch_ratio'] = 0
                features['move_ratio'] = 0
                features['damage_ratio'] = 0
            
            # Métricas de intensidad
            features['battle_intensity'] = (features['damage_events'] + features['status_events']) / max(features['turns'], 1)
            
            features_list.append(features)
            
        except Exception as e:
            print(f"Error procesando batalla {battle.get('battle_id', 'unknown')}: {e}")
            continue
    
    return pd.DataFrame(features_list)

# Extraer características
print("🔧 Extrayendo características de las batallas...")
df_features = extract_battle_features(battles_data)

# Codificar variables categóricas
label_encoders = {}
categorical_cols = ['format', 'winner']

for col in categorical_cols:
    if col in df_features.columns:
        le = LabelEncoder()
        df_features[f'{col}_encoded'] = le.fit_transform(df_features[col].astype(str))
        label_encoders[col] = le

print(f"✅ Características extraídas: {df_features.shape}")
print(f"📊 Columnas: {list(df_features.columns)}")

# %% [markdown]
# ### 📈 El Primer Vistazo: ¿Qué Nos Susurran los Datos?
# 
# Antes de lanzarnos a entrenar modelos complejos, necesitamos escuchar lo que nuestros datos tienen que decirnos. Como un entrenador Pokemon experimentado que observa el campo antes de la batalla, vamos a hacer un reconocimiento rápido pero crucial.
# 
# ### 🎲 El Equilibrio del Universo Pokemon
# 
# Una pregunta fundamental: **¿Nuestros datos están balanceados?** En el mundo real de las batallas Pokemon, ¿hay un sesgo hacia algún tipo de ganador? ¿O vivimos en un universo perfectamente equilibrado donde la habilidad es el único factor determinante?
# 
# ### 🔍 Los Primeros Indicios del Éxito
# 
# También vamos a echar un vistazo a las correlaciones iniciales. ¿Qué características muestran las primeras señales de ser predictivas? Es como observar las primeras cartas en una partida de poker - no nos dice todo, pero nos da pistas valiosas sobre qué esperar.
# 
# **¿Qué patrones emergerán?** ¿Confirmarán nuestras hipótesis del EDA o nos sorprenderán con revelaciones inesperadas? Los números están a punto de hablar…

# %%
# Verificar distribución del target
if 'winner_encoded' in df_features.columns:
    # Debug: Verificar valores únicos del winner original
    print("Valores únicos de 'winner':", df_features['winner'].unique())
    print("Conteo de valores de 'winner':")
    print(df_features['winner'].value_counts())
    
    # Verificar si hay al menos 2 clases diferentes
    unique_winners = df_features['winner'].nunique()
    if unique_winners < 2:
        print(f"⚠️  ADVERTENCIA: Solo hay {unique_winners} clase(s) única(s) en 'winner'")
        print("Esto causará errores en el entrenamiento de ML")
        print("Verificando datos de batalla...")
        
        # Mostrar algunas batallas de ejemplo para debug
        print("\nEjemplos de datos de batalla:")
        for i, battle in enumerate(battles_data[:5]):
            print(f"Batalla {i+1}: winner = {battle.get('winner', 'N/A')}")
    
    winner_dist = df_features['winner_encoded'].value_counts()
    print("Distribución del ganador:")
    print(winner_dist)
    
    # Visualizar distribución
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    winner_dist.plot(kind='bar', color=[POKEMON_COLORS['fire'], POKEMON_COLORS['water']], alpha=0.8)
    plt.title('Distribución de Ganadores', fontsize=14, fontweight='bold')
    plt.xlabel('Ganador Codificado')
    plt.ylabel('Frecuencia')
    plt.xticks(rotation=0)
    
    plt.subplot(1, 2, 2)
    # Correlaciones importantes
    numeric_cols = df_features.select_dtypes(include=[np.number]).columns.tolist()
    # Remover el target de las correlaciones para evitar correlación perfecta consigo mismo
    feature_cols = [col for col in numeric_cols if col not in ['winner_encoded']]
    
    if len(feature_cols) > 0 and 'winner_encoded' in df_features.columns:
        # Calcular correlaciones solo con las características, no con el target
        corr_matrix = df_features[feature_cols + ['winner_encoded']].corr()
        corr_with_target = corr_matrix['winner_encoded'].abs().drop('winner_encoded').sort_values(ascending=False)
        top_corr = corr_with_target.head(8)
        
        top_corr.plot(kind='barh', color=POKEMON_COLORS['electric'], alpha=0.8)
        plt.title('Top Correlaciones con Ganador', fontsize=14, fontweight='bold')
        plt.xlabel('Correlación Absoluta')
        
        # Debug: Mostrar las correlaciones más altas
        print(f"\n🔍 TOP CORRELACIONES CON GANADOR:")
        print("-" * 50)
        for feature, corr in top_corr.head(5).items():
            print(f"   {feature:20} | Correlación: {corr:.4f}")
    else:
        plt.text(0.5, 0.5, 'No hay datos suficientes\npara correlaciones', 
                ha='center', va='center', transform=plt.gca().transAxes)
    
    plt.tight_layout()
    
    # Guardar gráfico para documentación técnica
    if IS_KAGGLE:
        plots_dir = Path(f"{WORKING_DIR}/plots")
    else:
        plots_dir = Path("../plots")
    
    plots_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(plots_dir / "00_data_distribution_analysis.png", 
                dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    print(f"💾 Gráfico guardado: {plots_dir / '00_data_distribution_analysis.png'}")
    
    plt.show()

# %% [markdown]
# ## 🤖 El Laboratorio del Dr. Frankenstein: Creando Nuestros Monstruos de ML
# 
# Ha llegado el momento más emocionante: **crear nuestros modelos de Machine Learning**. Como el Dr. Frankenstein en su laboratorio, vamos a dar vida a siete criaturas diferentes, cada una con sus propias fortalezas, debilidades y personalidades únicas.
# 
# ### 🧪 La Clase PokemonMLTrainer: Nuestro Laboratorio Personal
# 
# Hemos diseñado una clase especial que actuará como nuestro laboratorio de experimentación. Esta no es una clase ordinaria; es un **centro de comando avanzado** que:
# 
# - **Gestiona múltiples experimentos simultáneamente**
# - **Evalúa el rendimiento con métricas sofisticadas**
# - **Genera visualizaciones que cuentan historias**
# - **Optimiza automáticamente los hiperparámetros**
# - **Crea ensembles inteligentes**
# - **Analiza errores como un detective**
# 
# ### 🎭 Conoce a Nuestros Siete Gladiadores
# 
# Cada modelo que vamos a entrenar tiene su propia "personalidad" y enfoque para resolver el problema:
# 
# **🎯 Logistic Regression**: El estratega clásico, elegante y directo
# **🌳 Random Forest**: El consejo de ancianos, sabiduría colectiva
# **⚡ Gradient Boosting**: El perfeccionista, aprende de cada error
# **🚀 XGBoost**: El campeón de competencias, optimizado para ganar
# **💨 LightGBM**: El velocista inteligente, rápido pero preciso
# **🧠 Neural Network**: El cerebro artificial, patrones complejos
# **⚔️ SVM**: El matemático puro, fronteras de decisión perfectas
# 
# **¿Cuál de estos gladiadores se alzará como campeón?** ¿O será que la verdadera magia ocurre cuando trabajen juntos? El torneo está a punto de comenzar…

# %%
# Importar librerías adicionales para análisis avanzado
from sklearn.model_selection import learning_curve, validation_curve
from sklearn.calibration import calibration_curve, CalibratedClassifierCV
from sklearn.inspection import permutation_importance
import shap
from scipy import stats

class PokemonMLTrainer:
    """Entrenador avanzado de Machine Learning para batallas Pokemon."""
    
    def __init__(self, random_state=42, save_plots=True, plots_dir=None):
        self.random_state = random_state
        self.models = {}
        self.results = {}
        self.best_model = None
        self.best_score = 0.0
        self.scaler = StandardScaler()
        self.learning_curves = {}
        self.roc_curves = {}
        self.save_plots = save_plots
        
        # Detectar entorno y configurar rutas apropiadas
        if IS_KAGGLE:
            # Entorno Kaggle
            self.plots_dir = Path(f"{WORKING_DIR}/plots")
        elif plots_dir is not None:
            # Ruta personalizada
            self.plots_dir = Path(plots_dir)
        else:
            # Desarrollo local
            self.plots_dir = Path("../plots")
        
        # Crear directorio de plots si no existe
        if self.save_plots:
            self.plots_dir.mkdir(parents=True, exist_ok=True)
            print(f"📁 Directorio de gráficos creado: {self.plots_dir}")
    
    def save_plot(self, filename, dpi=300, bbox_inches='tight'):
        """Guarda el plot actual con alta calidad para documentación técnica."""
        if self.save_plots:
            filepath = self.plots_dir / f"{filename}.png"
            plt.savefig(filepath, dpi=dpi, bbox_inches=bbox_inches, 
                       facecolor='white', edgecolor='none')
            print(f"💾 Gráfico guardado: {filepath}")
        return filepath if self.save_plots else None
    
    def generate_plots_index(self):
        """Genera un índice de todos los gráficos exportados para documentación técnica."""
        if not self.save_plots:
            return
            
        plots_info = [
            ("00_data_distribution_analysis.png", "Distribución de Datos y Correlaciones", "Análisis inicial de la distribución de ganadores y correlaciones con el target"),
            ("01_roc_curves_comparison.png", "Curvas ROC - Comparación de Modelos", "Comparación del rendimiento de todos los modelos usando curvas ROC"),
            ("02_precision_recall_curves.png", "Curvas Precision-Recall", "Análisis de precisión y recall para cada modelo"),
            ("03_calibration_curves.png", "Curvas de Calibración", "Evaluación de la confiabilidad de las probabilidades predichas"),
            ("04_feature_importance_analysis.png", "Análisis de Importancia de Características", "Consenso entre modelos sobre las características más importantes"),
            ("05_prediction_errors_analysis.png", "Análisis de Errores de Predicción", "Investigación detallada de los patrones de error del mejor modelo")
        ]
        
        index_path = self.plots_dir / "README_PLOTS.md"
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write("# 📊 Índice de Gráficos - Pokemon Battle AI\n\n")
            f.write("Este directorio contiene todos los gráficos generados durante el entrenamiento del modelo de ML para batallas Pokemon.\n\n")
            f.write("## 📈 Gráficos Disponibles\n\n")
            
            for filename, title, description in plots_info:
                f.write(f"### {title}\n")
                f.write(f"**Archivo:** `{filename}`\n\n")
                f.write(f"**Descripción:** {description}\n\n")
                f.write(f"![{title}]({filename})\n\n")
                f.write("---\n\n")
            
            f.write("## 🎯 Uso en Documentación Técnica\n\n")
            f.write("Todos los gráficos están guardados en alta resolución (300 DPI) con fondo blanco, ")
            f.write("optimizados para su inclusión en documentos técnicos, presentaciones y reportes.\n\n")
            f.write("**Formato:** PNG con transparencia\n")
            f.write("**Resolución:** 300 DPI\n")
            f.write("**Colores:** Paleta Pokemon temática\n")
        
        print(f"📋 Índice de gráficos creado: {index_path}")
        
    def setup_models(self):
        """Configura todos los modelos a entrenar."""
        models = {
            'logistic_regression': LogisticRegression(
                random_state=self.random_state,
                max_iter=1000,
                class_weight='balanced'
            ),
            
            'random_forest': RandomForestClassifier(
                n_estimators=200,
                max_depth=15,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=self.random_state,
                class_weight='balanced',
                n_jobs=-1
            ),
            
            'gradient_boosting': GradientBoostingClassifier(
                n_estimators=200,
                learning_rate=0.1,
                max_depth=6,
                random_state=self.random_state
            ),
            
            'xgboost': xgb.XGBClassifier(
                n_estimators=200,
                learning_rate=0.1,
                max_depth=6,
                random_state=self.random_state,
                eval_metric='logloss',
                use_label_encoder=False
            ),
            
            'lightgbm': lgb.LGBMClassifier(
                n_estimators=200,
                learning_rate=0.1,
                max_depth=6,
                random_state=self.random_state,
                verbose=-1
            ),
            
            'neural_network': MLPClassifier(
                hidden_layer_sizes=(256, 128, 64),
                activation='relu',
                solver='adam',
                learning_rate_init=0.001,
                max_iter=500,
                random_state=self.random_state,
                early_stopping=True,
                validation_fraction=0.1
            ),
            
            'svm': SVC(
                kernel='rbf',
                probability=True,
                random_state=self.random_state,
                class_weight='balanced'
            )
        }
        
        return models
    
    def prepare_data(self, df, target_col='winner_encoded', test_size=0.2):
        """Prepara los datos para entrenamiento."""
        # Seleccionar características numéricas
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if target_col in numeric_cols:
            numeric_cols.remove(target_col)
        
        # Remover columnas no útiles
        exclude_cols = ['battle_id']
        numeric_cols = [col for col in numeric_cols if col not in exclude_cols]
        
        X = df[numeric_cols].copy()
        y = df[target_col].copy()
        
        # Manejar valores faltantes
        X = X.fillna(X.median())
        
        # División de datos
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=self.random_state, stratify=y
        )
        
        return X_train, X_test, y_train, y_test, numeric_cols
    
    def calculate_advanced_metrics(self, y_true, y_pred, y_pred_proba, model_name):
        """Calcula métricas avanzadas específicas por tipo de modelo."""
        
        # Métricas básicas
        basic_metrics = {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred, average='weighted'),
            'recall': recall_score(y_true, y_pred, average='weighted'),
            'f1': f1_score(y_true, y_pred, average='weighted'),
            'roc_auc': roc_auc_score(y_true, y_pred_proba)
        }
        
        # Métricas avanzadas
        advanced_metrics = {}
        
        # Brier Score (calibración de probabilidades)
        from sklearn.metrics import brier_score_loss
        advanced_metrics['brier_score'] = brier_score_loss(y_true, y_pred_proba)
        
        # Log Loss
        from sklearn.metrics import log_loss
        try:
            advanced_metrics['log_loss'] = log_loss(y_true, y_pred_proba)
        except:
            advanced_metrics['log_loss'] = np.nan
        
        # Matthews Correlation Coefficient
        from sklearn.metrics import matthews_corrcoef
        advanced_metrics['mcc'] = matthews_corrcoef(y_true, y_pred)
        
        # Balanced Accuracy
        from sklearn.metrics import balanced_accuracy_score
        advanced_metrics['balanced_accuracy'] = balanced_accuracy_score(y_true, y_pred)
        
        # Métricas específicas por clase
        precision_per_class = precision_score(y_true, y_pred, average=None)
        recall_per_class = recall_score(y_true, y_pred, average=None)
        
        advanced_metrics['precision_class_0'] = precision_per_class[0] if len(precision_per_class) > 0 else 0
        advanced_metrics['precision_class_1'] = precision_per_class[1] if len(precision_per_class) > 1 else 0
        advanced_metrics['recall_class_0'] = recall_per_class[0] if len(recall_per_class) > 0 else 0
        advanced_metrics['recall_class_1'] = recall_per_class[1] if len(recall_per_class) > 1 else 0
        
        # Combinar métricas
        all_metrics = {**basic_metrics, **advanced_metrics}
        
        return all_metrics
    
    def plot_learning_curves(self, model, X, y, model_name, cv=5):
        """Genera curvas de aprendizaje para un modelo."""
        
        train_sizes, train_scores, val_scores = learning_curve(
            model, X, y, cv=cv, n_jobs=-1, 
            train_sizes=np.linspace(0.1, 1.0, 10),
            scoring='roc_auc', random_state=self.random_state
        )
        
        # Calcular medias y desviaciones estándar
        train_mean = np.mean(train_scores, axis=1)
        train_std = np.std(train_scores, axis=1)
        val_mean = np.mean(val_scores, axis=1)
        val_std = np.std(val_scores, axis=1)
        
        # Guardar para análisis posterior
        self.learning_curves[model_name] = {
            'train_sizes': train_sizes,
            'train_mean': train_mean,
            'train_std': train_std,
            'val_mean': val_mean,
            'val_std': val_std
        }
        
        return train_sizes, train_mean, train_std, val_mean, val_std
    
    def plot_roc_curves(self, models_results, X_test, y_test):
        """Genera curvas ROC para todos los modelos."""
        
        plt.figure(figsize=(12, 8))
        
        colors = [POKEMON_COLORS['fire'], POKEMON_COLORS['water'], 
                 POKEMON_COLORS['grass'], POKEMON_COLORS['electric'],
                 POKEMON_COLORS['psychic'], POKEMON_COLORS['ice'],
                 POKEMON_COLORS['dragon']]
        
        for i, (model_name, result) in enumerate(models_results.items()):
            if i >= len(colors):
                break
                
            y_pred_proba = result['probabilities']
            fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
            roc_auc = auc(fpr, tpr)
            
            # Guardar curva ROC
            self.roc_curves[model_name] = {'fpr': fpr, 'tpr': tpr, 'auc': roc_auc}
            
            plt.plot(fpr, tpr, color=colors[i], lw=2, alpha=0.8,
                    label=f'{model_name} (AUC = {roc_auc:.3f})')
        
        # Línea diagonal (clasificador aleatorio)
        plt.plot([0, 1], [0, 1], color='gray', lw=1, linestyle='--', alpha=0.8)
        
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('Tasa de Falsos Positivos', fontsize=12)
        plt.ylabel('Tasa de Verdaderos Positivos', fontsize=12)
        plt.title('Curvas ROC - Comparación de Modelos', fontsize=16, fontweight='bold')
        plt.legend(loc="lower right")
        plt.grid(alpha=0.3)
        
        # Añadir línea de baseline
        baseline_auc = 0.837
        plt.axhline(y=baseline_auc, color='red', linestyle=':', alpha=0.7, 
                   label=f'Baseline AUC = {baseline_auc}')
        
        plt.tight_layout()
        
        # Guardar gráfico
        self.save_plot("01_roc_curves_comparison")
        
        plt.show()
    
    def plot_precision_recall_curves(self, models_results, X_test, y_test):
        """Genera curvas Precision-Recall para todos los modelos."""
        
        from sklearn.metrics import precision_recall_curve, average_precision_score
        
        plt.figure(figsize=(12, 8))
        
        colors = [POKEMON_COLORS['fire'], POKEMON_COLORS['water'], 
                 POKEMON_COLORS['grass'], POKEMON_COLORS['electric'],
                 POKEMON_COLORS['psychic'], POKEMON_COLORS['ice'],
                 POKEMON_COLORS['dragon']]
        
        for i, (model_name, result) in enumerate(models_results.items()):
            if i >= len(colors):
                break
                
            y_pred_proba = result['probabilities']
            precision, recall, _ = precision_recall_curve(y_test, y_pred_proba)
            avg_precision = average_precision_score(y_test, y_pred_proba)
            
            plt.plot(recall, precision, color=colors[i], lw=2, alpha=0.8,
                    label=f'{model_name} (AP = {avg_precision:.3f})')
        
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('Recall', fontsize=12)
        plt.ylabel('Precision', fontsize=12)
        plt.title('Curvas Precision-Recall - Comparación de Modelos', fontsize=16, fontweight='bold')
        plt.legend(loc="lower left")
        plt.grid(alpha=0.3)
        
        plt.tight_layout()
        
        # Guardar gráfico
        self.save_plot("02_precision_recall_curves")
        
        plt.show()
    
    def plot_calibration_curves(self, models_results, X_test, y_test):
        """Genera curvas de calibración para evaluar la confiabilidad de las probabilidades."""
        
        plt.figure(figsize=(12, 8))
        
        colors = [POKEMON_COLORS['fire'], POKEMON_COLORS['water'], 
                 POKEMON_COLORS['grass'], POKEMON_COLORS['electric'],
                 POKEMON_COLORS['psychic'], POKEMON_COLORS['ice'],
                 POKEMON_COLORS['dragon']]
        
        for i, (model_name, result) in enumerate(models_results.items()):
            if i >= len(colors):
                break
                
            y_pred_proba = result['probabilities']
            fraction_of_positives, mean_predicted_value = calibration_curve(
                y_test, y_pred_proba, n_bins=10
            )
            
            plt.plot(mean_predicted_value, fraction_of_positives, "s-",
                    color=colors[i], alpha=0.8, label=f'{model_name}')
        
        # Línea de calibración perfecta
        plt.plot([0, 1], [0, 1], "k:", label="Calibración perfecta")
        
        plt.xlabel('Probabilidad Predicha Promedio', fontsize=12)
        plt.ylabel('Fracción de Positivos', fontsize=12)
        plt.title('Curvas de Calibración - Confiabilidad de Probabilidades', fontsize=16, fontweight='bold')
        plt.legend()
        plt.grid(alpha=0.3)
        
        plt.tight_layout()
        
        # Guardar gráfico
        self.save_plot("03_calibration_curves")
        
        plt.show()
    
    def plot_feature_importance_analysis(self, models_results, feature_names):
        """Analiza y visualiza la importancia de características con consenso entre modelos."""
        
        # Recopilar importancias de todos los modelos
        feature_importances = {}
        
        for model_name, result in models_results.items():
            model = result['model']
            
            # Obtener importancias según el tipo de modelo
            if hasattr(model, 'feature_importances_'):
                # Tree-based models
                importances = model.feature_importances_
            elif hasattr(model, 'coef_'):
                # Linear models
                importances = np.abs(model.coef_[0])
            else:
                # Para otros modelos, usar permutation importance
                continue
            
            feature_importances[model_name] = importances
        
        if not feature_importances:
            print("⚠️ No se pudieron extraer importancias de características")
            return None
        
        # Crear DataFrame de importancias
        importance_df = pd.DataFrame(feature_importances, index=feature_names)
        
        # Calcular estadísticas de consenso
        importance_df['mean'] = importance_df.mean(axis=1)
        importance_df['std'] = importance_df.std(axis=1)
        importance_df['stability'] = 1 - (importance_df['std'] / (importance_df['mean'] + 1e-8))
        
        # Ordenar por importancia promedio
        importance_df = importance_df.sort_values('mean', ascending=False)
        
        # Visualización
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # 1. Top 10 características por importancia promedio
        top_features = importance_df.head(10)
        axes[0, 0].barh(range(len(top_features)), top_features['mean'], 
                       color=POKEMON_COLORS['fire'], alpha=0.8)
        axes[0, 0].set_yticks(range(len(top_features)))
        axes[0, 0].set_yticklabels(top_features.index)
        axes[0, 0].set_title('Top 10 Características - Importancia Promedio', fontweight='bold')
        axes[0, 0].set_xlabel('Importancia Promedio')
        
        # 2. Estabilidad vs Importancia
        axes[0, 1].scatter(importance_df['mean'], importance_df['stability'], 
                          c=POKEMON_COLORS['water'], alpha=0.7, s=60)
        axes[0, 1].set_xlabel('Importancia Promedio')
        axes[0, 1].set_ylabel('Estabilidad (1 - CV)')
        axes[0, 1].set_title('Estabilidad vs Importancia', fontweight='bold')
        
        # Anotar características más estables e importantes
        stable_important = importance_df[(importance_df['stability'] > 0.7) & 
                                       (importance_df['mean'] > importance_df['mean'].median())]
        for idx, row in stable_important.head(5).iterrows():
            axes[0, 1].annotate(idx, (row['mean'], row['stability']), 
                              xytext=(5, 5), textcoords='offset points', fontsize=8)
        
        # 3. Heatmap de importancias por modelo
        models_to_plot = list(feature_importances.keys())[:5]  # Top 5 modelos
        features_to_plot = top_features.index[:8]  # Top 8 características
        
        heatmap_data = importance_df.loc[features_to_plot, models_to_plot]
        im = axes[1, 0].imshow(heatmap_data.values, cmap='YlOrRd', aspect='auto')
        axes[1, 0].set_xticks(range(len(models_to_plot)))
        axes[1, 0].set_xticklabels(models_to_plot, rotation=45)
        axes[1, 0].set_yticks(range(len(features_to_plot)))
        axes[1, 0].set_yticklabels(features_to_plot)
        axes[1, 0].set_title('Heatmap de Importancias por Modelo', fontweight='bold')
        
        # Añadir colorbar
        plt.colorbar(im, ax=axes[1, 0])
        
        # 4. Distribución de importancias
        axes[1, 1].hist(importance_df['mean'], bins=20, color=POKEMON_COLORS['grass'], 
                       alpha=0.7, edgecolor='black')
        axes[1, 1].axvline(importance_df['mean'].mean(), color='red', linestyle='--', 
                          label=f'Media: {importance_df["mean"].mean():.4f}')
        axes[1, 1].set_xlabel('Importancia Promedio')
        axes[1, 1].set_ylabel('Frecuencia')
        axes[1, 1].set_title('Distribución de Importancias', fontweight='bold')
        axes[1, 1].legend()
        
        plt.tight_layout()
        
        # Guardar gráfico
        self.save_plot("04_feature_importance_analysis")
        
        plt.show()
        
        # Reporte de características más importantes
        print("\n🏆 TOP 10 CARACTERÍSTICAS MÁS IMPORTANTES:")
        print("-" * 60)
        for i, (feature, row) in enumerate(top_features.iterrows(), 1):
            stability_emoji = "🔒" if row['stability'] > 0.8 else "📊" if row['stability'] > 0.6 else "📈"
            print(f"{i:2d}. {stability_emoji} {feature:25} | Importancia: {row['mean']:.4f} | Estabilidad: {row['stability']:.3f}")
        
        print(f"\n🎯 CARACTERÍSTICAS MÁS ESTABLES (Estabilidad > 0.7): {len(importance_df[importance_df['stability'] > 0.7])}")
        print(f"⚡ CARACTERÍSTICAS ALTAMENTE PREDICTIVAS (Importancia > media): {len(importance_df[importance_df['mean'] > importance_df['mean'].mean()])}")
        
        return importance_df
    
    def hyperparameter_optimization(self, X_train, y_train, top_models=3):
        """Optimiza hiperparámetros para los mejores modelos."""
        
        print(f"\n⚙️ Optimizando hiperparámetros para los top {top_models} modelos...")
        
        # Obtener los mejores modelos por ROC-AUC
        model_scores = [(name, result['metrics']['roc_auc']) for name, result in self.results.items()]
        model_scores.sort(key=lambda x: x[1], reverse=True)
        top_model_names = [name for name, _ in model_scores[:top_models]]
        
        optimized_models = {}
        
        # Definir espacios de búsqueda para cada modelo
        param_grids = {
            'random_forest': {
                'n_estimators': [100, 200, 300],
                'max_depth': [10, 15, 20, None],
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2, 4],
                'max_features': ['sqrt', 'log2', None]
            },
            'xgboost': {
                'n_estimators': [100, 200, 300],
                'learning_rate': [0.01, 0.1, 0.2],
                'max_depth': [3, 6, 9],
                'subsample': [0.8, 0.9, 1.0],
                'colsample_bytree': [0.8, 0.9, 1.0]
            },
            'lightgbm': {
                'n_estimators': [100, 200, 300],
                'learning_rate': [0.01, 0.1, 0.2],
                'max_depth': [3, 6, 9],
                'num_leaves': [31, 50, 100],
                'subsample': [0.8, 0.9, 1.0]
            },
            'gradient_boosting': {
                'n_estimators': [100, 200, 300],
                'learning_rate': [0.01, 0.1, 0.2],
                'max_depth': [3, 6, 9],
                'subsample': [0.8, 0.9, 1.0]
            },
            'logistic_regression': {
                'C': [0.1, 1.0, 10.0, 100.0],
                'penalty': ['l1', 'l2'],
                'solver': ['liblinear', 'saga']
            }
        }
        
        for model_name in top_model_names:
            if model_name not in param_grids:
                print(f"⚠️ No hay parámetros definidos para {model_name}")
                continue
                
            print(f"\n🔧 Optimizando {model_name}...")
            
            try:
                # Obtener modelo base
                base_model = self.setup_models()[model_name]
                
                # Preparar datos
                if model_name in ['neural_network', 'svm', 'logistic_regression']:
                    X_train_final = self.scaler.fit_transform(X_train)
                else:
                    X_train_final = X_train
                
                # Búsqueda aleatoria
                random_search = RandomizedSearchCV(
                    base_model,
                    param_grids[model_name],
                    n_iter=20,  # Reducido para velocidad
                    cv=3,       # Reducido para velocidad
                    scoring='roc_auc',
                    random_state=self.random_state,
                    n_jobs=-1,
                    verbose=0
                )
                
                random_search.fit(X_train_final, y_train)
                
                optimized_models[f"{model_name}_optimized"] = {
                    'model': random_search.best_estimator_,
                    'best_params': random_search.best_params_,
                    'best_score': random_search.best_score_,
                    'cv_results': random_search.cv_results_
                }
                
                print(f"✅ {model_name} optimizado - CV Score: {random_search.best_score_:.4f}")
                print(f"   Mejores parámetros: {random_search.best_params_}")
                
            except Exception as e:
                print(f"❌ Error optimizando {model_name}: {str(e)}")
                continue
        
        return optimized_models
    
    def create_ensemble(self, models_results, X_train, y_train):
        """Crea un modelo ensemble con los mejores modelos."""
        
        print("\n🤝 Creando modelo ensemble...")
        
        try:
            # Seleccionar los mejores modelos (top 5)
            model_scores = [(name, result['metrics']['roc_auc']) for name, result in models_results.items()]
            model_scores.sort(key=lambda x: x[1], reverse=True)
            top_models = model_scores[:5]
            
            print(f"   Modelos seleccionados para ensemble:")
            for name, score in top_models:
                print(f"   - {name}: {score:.4f}")
            
            # Crear lista de estimadores para el ensemble
            estimators = []
            for name, _ in top_models:
                model = models_results[name]['model']
                estimators.append((name, model))
            
            # Crear VotingClassifier con soft voting
            ensemble = VotingClassifier(
                estimators=estimators,
                voting='soft'
            )
            
            # Entrenar ensemble
            ensemble.fit(X_train, y_train)
            
            print("✅ Modelo ensemble creado exitosamente")
            return ensemble
            
        except Exception as e:
            print(f"❌ Error creando ensemble: {str(e)}")
            return None
    
    def analyze_prediction_errors(self, models_results, X_test, y_test, feature_names):
        """Analiza los errores de predicción para entender patrones de fallo."""
        
        print("\n🔍 Analizando errores de predicción...")
        
        # Obtener el mejor modelo
        best_model_name = max(models_results.keys(), 
                             key=lambda x: models_results[x]['metrics']['roc_auc'])
        best_result = models_results[best_model_name]
        
        y_pred = best_result['predictions']
        y_pred_proba = best_result['probabilities']
        
        # Crear DataFrame de análisis
        error_df = pd.DataFrame({
            'true_label': y_test,
            'predicted_label': y_pred,
            'predicted_proba': y_pred_proba,
            'correct': y_test == y_pred
        })
        
        # Añadir características
        for i, feature in enumerate(feature_names):
            error_df[feature] = X_test.iloc[:, i].values
        
        # Calcular métricas de error
        error_df['prediction_confidence'] = np.abs(error_df['predicted_proba'] - 0.5)
        error_df['error_type'] = 'Correct'
        error_df.loc[(error_df['true_label'] == 1) & (error_df['predicted_label'] == 0), 'error_type'] = 'False Negative'
        error_df.loc[(error_df['true_label'] == 0) & (error_df['predicted_label'] == 1), 'error_type'] = 'False Positive'
        
        # Visualizaciones
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # 1. Distribución de confianza por tipo de error
        error_types = error_df['error_type'].unique()
        colors = [POKEMON_COLORS['grass'], POKEMON_COLORS['fire'], POKEMON_COLORS['water']]
        
        for i, error_type in enumerate(error_types):
            if i < len(colors):
                subset = error_df[error_df['error_type'] == error_type]
                axes[0, 0].hist(subset['prediction_confidence'], alpha=0.7, 
                              label=error_type, color=colors[i], bins=20)
        
        axes[0, 0].set_xlabel('Confianza de Predicción')
        axes[0, 0].set_ylabel('Frecuencia')
        axes[0, 0].set_title('Distribución de Confianza por Tipo de Error', fontweight='bold')
        axes[0, 0].legend()
        
        # 2. Probabilidades predichas vs reales
        axes[0, 1].scatter(error_df[error_df['correct']]['predicted_proba'], 
                          error_df[error_df['correct']]['true_label'], 
                          alpha=0.6, color=POKEMON_COLORS['grass'], label='Correctas', s=30)
        axes[0, 1].scatter(error_df[~error_df['correct']]['predicted_proba'], 
                          error_df[~error_df['correct']]['true_label'], 
                          alpha=0.8, color=POKEMON_COLORS['fire'], label='Incorrectas', s=30)
        axes[0, 1].set_xlabel('Probabilidad Predicha')
        axes[0, 1].set_ylabel('Etiqueta Real')
        axes[0, 1].set_title('Probabilidades Predichas vs Etiquetas Reales', fontweight='bold')
        axes[0, 1].legend()
        
        # 3. Matriz de confusión
        from sklearn.metrics import confusion_matrix
        cm = confusion_matrix(y_test, y_pred)
        im = axes[1, 0].imshow(cm, interpolation='nearest', cmap='Blues')
        axes[1, 0].set_title('Matriz de Confusión', fontweight='bold')
        
        # Añadir texto a la matriz
        thresh = cm.max() / 2.
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                axes[1, 0].text(j, i, format(cm[i, j], 'd'),
                               ha="center", va="center",
                               color="white" if cm[i, j] > thresh else "black")
        
        axes[1, 0].set_ylabel('Etiqueta Real')
        axes[1, 0].set_xlabel('Etiqueta Predicha')
        
        # 4. Características más diferentes en errores
        incorrect_cases = error_df[~error_df['correct']]
        correct_cases = error_df[error_df['correct']]
        
        feature_diffs = []
        for feature in feature_names[:10]:  # Top 10 características
            if feature in error_df.columns:
                diff = abs(incorrect_cases[feature].mean() - correct_cases[feature].mean())
                feature_diffs.append((feature, diff))
        
        feature_diffs.sort(key=lambda x: x[1], reverse=True)
        features, diffs = zip(*feature_diffs[:8])
        
        axes[1, 1].barh(range(len(features)), diffs, color=POKEMON_COLORS['psychic'], alpha=0.8)
        axes[1, 1].set_yticks(range(len(features)))
        axes[1, 1].set_yticklabels(features)
        axes[1, 1].set_xlabel('Diferencia Promedio')
        axes[1, 1].set_title('Características Más Diferentes en Errores', fontweight='bold')
        
        plt.tight_layout()
        
        # Guardar gráfico
        self.save_plot("05_prediction_errors_analysis")
        
        plt.show()
        
        # Estadísticas de error
        print(f"\n📊 ESTADÍSTICAS DE ERROR ({best_model_name}):")
        print("-" * 50)
        print(f"Total de predicciones: {len(error_df)}")
        print(f"Predicciones correctas: {error_df['correct'].sum()} ({error_df['correct'].mean()*100:.1f}%)")
        print(f"Falsos positivos: {len(error_df[error_df['error_type'] == 'False Positive'])}")
        print(f"Falsos negativos: {len(error_df[error_df['error_type'] == 'False Negative'])}")
        
        # Casos de baja confianza
        low_confidence = error_df[error_df['prediction_confidence'] < 0.1]
        print(f"\nCasos de baja confianza (< 0.1): {len(low_confidence)} ({len(low_confidence)/len(error_df)*100:.1f}%)")
        print(f"Precisión en casos de baja confianza: {low_confidence['correct'].mean()*100:.1f}%")
        
        return error_df
    
    def train_models(self, X_train, X_test, y_train, y_test, feature_names):
        """Entrena todos los modelos con análisis avanzado."""
        print("🚀 Iniciando entrenamiento de modelos con análisis avanzado...")
        
        # Escalado para modelos que lo necesitan
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        models = self.setup_models()
        results = {}
        
        for model_name, model in models.items():
            print(f"\n🔄 Entrenando {model_name}...")
            
            try:
                # Seleccionar datos apropiados
                if model_name in ['neural_network', 'svm', 'logistic_regression']:
                    X_train_final = X_train_scaled
                    X_test_final = X_test_scaled
                else:
                    X_train_final = X_train
                    X_test_final = X_test
                
                # Entrenar modelo
                model.fit(X_train_final, y_train)
                
                # Predicciones
                y_pred = model.predict(X_test_final)
                y_pred_proba = model.predict_proba(X_test_final)[:, 1]
                
                # Métricas avanzadas
                metrics = self.calculate_advanced_metrics(y_test, y_pred, y_pred_proba, model_name)
                
                # Cross-validation
                cv_scores = cross_val_score(
                    model, X_train_final, y_train, 
                    cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=self.random_state),
                    scoring='roc_auc'
                )
                
                metrics['cv_mean'] = cv_scores.mean()
                metrics['cv_std'] = cv_scores.std()
                
                # Curvas de aprendizaje (solo para modelos rápidos)
                if model_name in ['logistic_regression', 'random_forest', 'gradient_boosting']:
                    print(f"   📈 Generando curvas de aprendizaje para {model_name}...")
                    self.plot_learning_curves(model, X_train_final, y_train, model_name)
                
                results[model_name] = {
                    'model': model,
                    'metrics': metrics,
                    'predictions': y_pred,
                    'probabilities': y_pred_proba
                }
                
                print(f"✅ {model_name} - ROC-AUC: {metrics['roc_auc']:.4f} | MCC: {metrics['mcc']:.4f} | Brier: {metrics['brier_score']:.4f}")
                
                # Actualizar mejor modelo
                if metrics['roc_auc'] > self.best_score:
                    self.best_score = metrics['roc_auc']
                    self.best_model = model_name
                
            except Exception as e:
                print(f"❌ Error entrenando {model_name}: {str(e)}")
                continue
        
        self.models = {name: result['model'] for name, result in results.items()}
        self.results = results
        
        # Generar visualizaciones comparativas
        print("\n📊 Generando visualizaciones comparativas...")
        self.plot_roc_curves(results, X_test, y_test)
        self.plot_precision_recall_curves(results, X_test, y_test)
        self.plot_calibration_curves(results, X_test, y_test)
        
        return results

# %% [markdown]
# ## 🚀 ¡Que Comience el Espectáculo! El Gran Torneo de Algoritmos
# 
# **Ladies and gentlemen, trainers and Pokemon masters!** Ha llegado el momento que todos estábamos esperando. Después de semanas de preparación, análisis y diseño, nuestros siete gladiadores están listos para enfrentarse en la arena más desafiante: **predecir el resultado de batallas Pokemon reales**.
# 
# ### 🎪 El Escenario Está Preparado
# 
# Nuestros datos están pulidos y listos. Nuestras características han sido cuidadosamente seleccionadas y engineered. Nuestros modelos están configurados con parámetros iniciales inteligentes. Todo está en su lugar para el espectáculo del siglo.
# 
# ### ⚡ La Tensión en el Aire
# 
# Podemos sentir la electricidad en el ambiente. Cada algoritmo "sabe" que está compitiendo no solo contra los datos, sino contra otros seis competidores igualmente determinados. El baseline de **ROC-AUC 0.837** se alza como el dragón final que todos deben derrotar.
# 
# **¿Quién será el primero en caer?** ¿Qué modelo sorprenderá con un rendimiento inesperado? ¿Veremos una batalla reñida o habrá un claro dominador desde el principio?
# 
# La preparación ha terminado. Los dados están echados. **¡Que comience la batalla!**

# %%
# Inicializar entrenador
trainer = PokemonMLTrainer(random_state=42)
print("✅ Entrenador ML avanzado inicializado")
print("🚀 ¡Listo para comenzar el entrenamiento!")

# %%
# Preparar datos
print("📊 Preparando datos para entrenamiento...")
X_train, X_test, y_train, y_test, feature_names = trainer.prepare_data(df_features)

print(f"✅ Datos preparados:")
print(f"   - Entrenamiento: {X_train.shape}")
print(f"   - Prueba: {X_test.shape}")
print(f"   - Características: {len(feature_names)}")

# %% [markdown]
# ### 🤖 Round 1: Los Gladiadores Entran en Acción
# 
# **¡DING DING DING!** Suena la campana y nuestros siete gladiadores saltan al ring. Este es el momento de la verdad - después de toda la preparación, finalmente veremos de qué están hechos nuestros modelos.
# 
# ### 🎭 El Drama se Desarrolla
# 
# Cada modelo aborda el problema desde su perspectiva única:
# - **Logistic Regression** entra con confianza clásica, buscando relaciones lineales claras
# - **Random Forest** despliega su ejército de árboles, cada uno votando por su predicción favorita
# - **Gradient Boosting** comienza lentamente, aprendiendo meticulosamente de cada error
# - **XGBoost** llega con toda la experiencia de miles de competencias de Kaggle
# - **LightGBM** se mueve con agilidad felina, optimizando cada cálculo
# - **Neural Network** activa sus neuronas, buscando patrones que otros no pueden ver
# - **SVM** traza fronteras de decisión con precisión matemática
# 
# ### 📊 Las Métricas Que Importan
# 
# No nos conformamos con una sola métrica. Como jueces experimentados, evaluamos cada modelo desde múltiples ángulos:
# - **ROC-AUC**: ¿Qué tan bien separa ganadores de perdedores?
# - **MCC**: ¿Qué tan balanceado es su rendimiento?
# - **Brier Score**: ¿Qué tan calibradas están sus probabilidades?
# - **Cross-validation**: ¿Es consistente o solo tuvo suerte?
# 
# **¿Quién tomará la delantera inicial?** Los primeros resultados están a punto de revelarse…

# %%
# Entrenar modelos
results = trainer.train_models(X_train, X_test, y_train, y_test, feature_names)

print(f"\n🏆 Mejor modelo base: {trainer.best_model} (ROC-AUC: {trainer.best_score:.4f})")

# %% [markdown]
# ### 🔍 Los Secretos Revelados: ¿Qué Hace Ganar una Batalla?
# 
# Ahora que nuestros modelos han mostrado sus cartas, es momento de la **gran revelación**. Como detectives investigando un misterio, vamos a descubrir qué características son realmente importantes para predecir el éxito en las batallas Pokemon.
# 
# ### 🕵️ La Investigación Comienza
# 
# No todos los modelos "ven" las mismas cosas. Algunos se enfocan en patrones sutiles, otros en señales obvias. Pero cuando múltiples modelos coinciden en que una característica es importante, sabemos que hemos encontrado algo especial.
# 
# ### 🎯 El Consenso de los Maestros
# 
# Vamos a realizar un análisis de consenso - como reunir a los mejores entrenadores Pokemon del mundo y preguntarles: **"¿En qué se fijan cuando predicen quién ganará una batalla?"**
# 
# **¿Será la intensidad de la batalla?** ¿La cantidad de movimientos ejecutados? ¿Los patrones de cambio? ¿O descubriremos algo completamente inesperado?
# 
# ### 🏆 Las Características Más Estables
# 
# También buscaremos las características más "estables" - aquellas en las que todos los modelos confían consistentemente. Estas son como las reglas fundamentales del universo Pokemon, principios que trascienden algoritmos específicos.
# 
# **¿Qué secretos del éxito en batallas Pokemon están a punto de ser revelados?**

# %%
# Análisis de importancia de características
print("\n🔍 Analizando importancia de características...")
importance_analysis = trainer.plot_feature_importance_analysis(results, feature_names)

# %% [markdown]
# ### ⚙️ Round 2: Los Gladiadores Evolucionan
# 
# **¡Plot twist!** Como en cualquier buena historia de Pokemon, nuestros competidores están a punto de **evolucionar**. Los tres mejores modelos del primer round han ganado el derecho a una transformación especial: optimización de hiperparámetros.
# 
# ### 🧬 La Evolución No Es Solo Suerte
# 
# En el mundo Pokemon, la evolución requiere las condiciones exactas. De manera similar, nuestros modelos necesitan los hiperparámetros perfectos para alcanzar su máximo potencial. No es magia - es **ciencia pura y búsqueda inteligente**.
# 
# ### 🎯 La Búsqueda del Santo Grial
# 
# Cada modelo tiene su propio "código genético" de hiperparámetros:
# - **Random Forest**: ¿Cuántos árboles? ¿Qué profundidad? ¿Cuántas muestras por hoja?
# - **XGBoost**: ¿Qué learning rate? ¿Cuánta regularización? ¿Qué subsample?
# - **LightGBM**: ¿Cuántas hojas? ¿Qué profundidad máxima? ¿Cuántos estimadores?
# 
# ### 🔬 RandomizedSearchCV: Nuestro Laboratorio de Evolución
# 
# No vamos a probar cada combinación posible (eso tomaría años). En su lugar, usamos **búsqueda aleatoria inteligente** - como un entrenador Pokemon experimentado que sabe exactamente qué condiciones probar para cada evolución.
# 
# **¿Veremos mejoras dramáticas?** ¿Algún modelo dará un salto cuántico en rendimiento? ¿O descubriremos que ya estaban cerca de su potencial máximo?
# 
# **¡La evolución comienza ahora!**

# %%
# Optimización de hiperparámetros
optimized_models = trainer.hyperparameter_optimization(X_train, y_train, top_models=3)

# Evaluar modelos optimizados
print("\n📊 Evaluando modelos optimizados...")
optimized_results = {}

for opt_name, opt_data in optimized_models.items():
    model = opt_data['model']
    
    # Seleccionar datos apropiados
    base_name = opt_name.replace('_optimized', '')
    if base_name in ['neural_network', 'svm', 'logistic_regression']:
        X_test_final = trainer.scaler.transform(X_test)
    else:
        X_test_final = X_test
    
    # Predicciones
    y_pred = model.predict(X_test_final)
    y_pred_proba = model.predict_proba(X_test_final)[:, 1]
    
    # Métricas
    metrics = trainer.calculate_advanced_metrics(y_test, y_pred, y_pred_proba, opt_name)
    
    optimized_results[opt_name] = {
        'model': model,
        'metrics': metrics,
        'predictions': y_pred,
        'probabilities': y_pred_proba
    }
    
    print(f"✅ {opt_name} - ROC-AUC: {metrics['roc_auc']:.4f} | MCC: {metrics['mcc']:.4f}")
    
    # Actualizar mejor modelo si es necesario
    if metrics['roc_auc'] > trainer.best_score:
        trainer.best_score = metrics['roc_auc']
        trainer.best_model = opt_name

# %% [markdown]
# ### 🤝 La Alianza Definitiva: Cuando los Rivales se Unen
# 
# En las mejores historias épicas, llega un momento cuando los antiguos rivales deben unir fuerzas para enfrentar un desafío mayor. **Este es ese momento.**
# 
# ### 🌟 El Poder de la Unión
# 
# Hemos visto lo que cada modelo puede lograr individualmente. Algunos brillan en ciertos aspectos, otros dominan diferentes patrones. Pero ¿qué pasaría si combináramos sus fortalezas únicas en una **súper-alianza**?
# 
# ### 🎭 Los Avengers del Machine Learning
# 
# Como los Avengers, cada modelo aporta algo único al equipo:
# - **Random Forest**: La sabiduría colectiva y estabilidad
# - **XGBoost**: La precisión competitiva y optimización
# - **LightGBM**: La velocidad y eficiencia
# - **Neural Network**: La capacidad de ver patrones complejos
# - **Gradient Boosting**: El aprendizaje meticuloso de errores
# 
# ### 🗳️ Democracia en Acción: Soft Voting
# 
# Nuestro ensemble no es una dictadura donde un modelo domina. Es una **democracia perfecta** donde cada modelo vota con sus probabilidades, y la decisión final emerge del consenso colectivo.
# 
# ### 🎯 La Pregunta del Millón
# 
# **¿Será el ensemble superior a cualquier modelo individual?** En teoría, debería ser así - la diversidad de enfoques debería crear un predictor más robusto y preciso.
# 
# Pero la teoría y la realidad a veces divergen. **¿Nuestros gladiadores trabajarán mejor juntos o en solitario?**
# 
# **¡La alianza definitiva está a punto de formarse!**

# %%
# Crear ensemble
ensemble_model = trainer.create_ensemble(results, X_train, y_train)

if ensemble_model is not None:
    # Evaluar ensemble
    print("\n📊 Evaluando modelo ensemble...")
    
    # Predicciones del ensemble
    y_pred_ensemble = ensemble_model.predict(X_test)
    y_pred_proba_ensemble = ensemble_model.predict_proba(X_test)[:, 1]
    
    # Métricas del ensemble
    ensemble_metrics = trainer.calculate_advanced_metrics(
        y_test, y_pred_ensemble, y_pred_proba_ensemble, 'ensemble'
    )
    
    print(f"🤝 Ensemble - ROC-AUC: {ensemble_metrics['roc_auc']:.4f} | MCC: {ensemble_metrics['mcc']:.4f}")
    
    # Actualizar mejor modelo si el ensemble es superior
    if ensemble_metrics['roc_auc'] > trainer.best_score:
        trainer.best_score = ensemble_metrics['roc_auc']
        trainer.best_model = 'ensemble'
        
        # Añadir ensemble a resultados
        optimized_results['ensemble'] = {
            'model': ensemble_model,
            'metrics': ensemble_metrics,
            'predictions': y_pred_ensemble,
            'probabilities': y_pred_proba_ensemble
        }

# %% [markdown]
# ### 🔍 CSI: Pokemon Battle Edition - Investigando los Misterios del Fracaso
# 
# Incluso los mejores entrenadores Pokemon pierden batallas. Incluso los mejores modelos de ML cometen errores. Pero la diferencia entre un buen entrenador y un **maestro** está en cómo aprende de esas derrotas.
# 
# ### 🕵️ Convirtiéndonos en Detectives de Datos
# 
# Cada predicción incorrecta es como una escena del crimen que debemos investigar. **¿Por qué falló nuestro modelo?** ¿Fue mala suerte, información insuficiente, o hay patrones sistemáticos en nuestros errores?
# 
# ### 🎭 Los Cuatro Tipos de Drama
# 
# En el teatro del Machine Learning, hay cuatro tipos de drama:
# - **True Positives**: Las victorias bien predichas (¡éxito!)
# - **True Negatives**: Las derrotas bien predichas (¡también éxito!)
# - **False Positives**: Predijimos victoria pero hubo derrota (¡optimismo excesivo!)
# - **False Negatives**: Predijimos derrota pero hubo victoria (¡pesimismo injustificado!)
# 
# ### 🌊 La Zona de Incertidumbre
# 
# Hay batallas que son genuinamente difíciles de predecir - aquellas donde nuestro modelo dice "no estoy seguro" (probabilidades cerca de 0.5). **¿Qué hace que estas batallas sean tan impredecibles?** ¿Son genuinamente aleatorias o hay patrones sutiles que aún no capturamos?
# 
# ### 🔬 Anatomía de un Error
# 
# Vamos a diseccionar nuestros errores como científicos forenses:
# - **¿En qué características difieren los casos mal clasificados?**
# - **¿Hay patrones en las probabilidades de predicción?**
# - **¿Algunos tipos de batalla son más difíciles que otros?**
# 
# **¿Qué secretos revelarán nuestros errores?** A veces, los fracasos enseñan más que los éxitos…

# %%
# Análisis de errores
all_results = {**results, **optimized_results}
error_analysis = trainer.analyze_prediction_errors(all_results, X_test, y_test, feature_names)

# %% [markdown]
# ## 📊 El Momento de la Verdad: ¿Hemos Hecho Historia?
# 
# **Señoras y señores, el momento que todos hemos estado esperando ha llegado.** Después de horas de entrenamiento, optimización y análisis, es hora de responder la pregunta fundamental:
# 
# ### 🎯 ¿Hemos Superado lo Imposible?
# 
# Nuestro baseline de **ROC-AUC 0.837** ha sido nuestro dragón final desde el principio. Un número que parecía formidable, casi inalcanzable. Pero hemos reunido el mejor arsenal de Machine Learning disponible y lo hemos lanzado contra este desafío.
# 
# ### 🏆 El Podio de Campeones
# 
# Como en cualquier competencia épica, vamos a coronar a nuestros campeones:
# - **🥇 Medalla de Oro**: El modelo supremo que reinará sobre todos
# - **🥈 Medalla de Plata**: El digno segundo lugar
# - **🥉 Medalla de Bronce**: El tercer puesto honorable
# 
# ### 📈 La Historia en Números
# 
# Pero esto no es solo sobre ganar o perder. Es sobre **cuánto hemos mejorado**. ¿Fue una mejora marginal del 1%? ¿O logramos un salto cuántico del 10% o más?
# 
# ### 🎭 El Drama del Resultado
# 
# **¿Cuál será el veredicto final?** ¿Celebraremos una victoria aplastante sobre el baseline? ¿O descubriremos que el baseline era más formidable de lo que pensábamos?
# 
# **¿Habrá sorpresas?** ¿Algún modelo underdog que nadie esperaba se alzará como campeón? ¿O el favorito cumplirá las expectativas?
# 
# **El suspenso está matando... ¡Veamos los resultados!**

# %%
# Reporte final
print("\n" + "="*80)
print("🏆 REPORTE FINAL - POKEMON BATTLE AI ML TRAINING")
print("="*80)

baseline_auc = 0.837
print(f"\n📊 BASELINE ROC-AUC: {baseline_auc:.4f}")
print(f"🎯 MEJOR MODELO: {trainer.best_model}")
print(f"🏆 MEJOR ROC-AUC: {trainer.best_score:.4f}")

improvement = ((trainer.best_score - baseline_auc) / baseline_auc) * 100
if trainer.best_score > baseline_auc:
    print(f"✅ MEJORA: +{improvement:.2f}% sobre baseline")
else:
    print(f"❌ RENDIMIENTO: {improvement:.2f}% respecto al baseline")

print(f"\n📈 RESUMEN DE TODOS LOS MODELOS:")
print("-" * 60)

# Combinar todos los resultados
all_model_scores = []

# Modelos base
for name, result in results.items():
    all_model_scores.append((name, result['metrics']['roc_auc'], result['metrics']['mcc']))

# Modelos optimizados
for name, result in optimized_results.items():
    all_model_scores.append((name, result['metrics']['roc_auc'], result['metrics']['mcc']))

# Ordenar por ROC-AUC
all_model_scores.sort(key=lambda x: x[1], reverse=True)

for i, (name, auc, mcc) in enumerate(all_model_scores, 1):
    status = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "  "
    vs_baseline = "✅" if auc > baseline_auc else "❌"
    print(f"{status} {name:25} | ROC-AUC: {auc:.4f} | MCC: {mcc:.4f} | {vs_baseline}")

print("\n" + "="*80)

# %% [markdown]
# ### 💾 Preservando la Historia: El Legado de Nuestros Campeones
# 
# Como arqueólogos del futuro, debemos preservar cuidadosamente nuestros descubrimientos. El modelo campeón que hemos creado no es solo código - es **historia en el making**, el resultado de un viaje épico de descubrimiento y optimización.
# 
# ### 🏛️ El Museo de Nuestros Logros
# 
# Vamos a crear un "museo digital" completo de nuestro proyecto:
# - **El Modelo Campeón**: Serializado y listo para la posteridad
# - **Los Resultados Completos**: Cada métrica, cada comparación, cada insight
# - **El Scaler**: Si nuestro campeón lo necesita, también lo preservamos
# - **Los Metadatos**: La fecha, las condiciones, el contexto completo
# 
# ### 📜 El Pergamino de los Resultados
# 
# Nuestro archivo JSON será como un pergamino antiguo que cuenta la historia completa:
# - ¿Quién fue el campeón?
# - ¿Cuál fue su puntuación final?
# - ¿Cuánto mejoró sobre el baseline?
# - ¿Cuáles fueron las características más importantes?
# - ¿Cuándo ocurrió este momento histórico?
# 
# ### 🚀 Listo para la Producción
# 
# Este no es el final de nuestro viaje - es el **comienzo de una nueva era**. Nuestro modelo campeón está listo para:
# - Predecir batallas Pokemon en tiempo real
# - Ayudar a entrenadores a tomar mejores decisiones
# - Revelar patrones ocultos en el mundo competitivo Pokemon
# 
# **¡La historia ha sido escrita, el legado está asegurado!**

# %%
# Crear directorio de salida - detectar entorno
if IS_KAGGLE:
    output_dir = Path(f"{WORKING_DIR}/models/trained")
else:
    output_dir = Path("../models/trained")

output_dir.mkdir(parents=True, exist_ok=True)

# Guardar mejor modelo
if trainer.best_model in all_results:
    best_model_obj = all_results[trainer.best_model]['model']
    
    # Guardar modelo
    model_path = output_dir / f"best_model_{trainer.best_model}.pkl"
    with open(model_path, 'wb') as f:
        pickle.dump(best_model_obj, f)
    
    # Guardar scaler si es necesario
    if trainer.best_model in ['neural_network', 'svm', 'logistic_regression']:
        scaler_path = output_dir / f"scaler_{trainer.best_model}.pkl"
        with open(scaler_path, 'wb') as f:
            pickle.dump(trainer.scaler, f)
    
    print(f"✅ Mejor modelo guardado: {model_path}")

# Guardar resultados completos
results_data = {
    'best_model': trainer.best_model,
    'best_score': trainer.best_score,
    'baseline_auc': baseline_auc,
    'improvement': improvement,
    'feature_names': feature_names,
    'model_scores': all_model_scores,
    'training_date': datetime.now().isoformat()
}

results_path = output_dir / "training_results.json"
with open(results_path, 'w') as f:
    json.dump(results_data, f, indent=2)

print(f"✅ Resultados guardados: {results_path}")

# Generar índice de gráficos para documentación técnica
trainer.generate_plots_index()

print("\n🎉 ¡Entrenamiento completado exitosamente!")
print("🚀 El modelo está listo para hacer predicciones en batallas Pokemon!")
print("📊 Todos los gráficos han sido exportados para documentación técnica")

# Mostrar resumen de archivos generados
print(f"\n📁 ARCHIVOS GENERADOS EN {output_dir.parent}:")
print("-" * 50)

# Listar archivos de modelos
if output_dir.exists():
    model_files = list(output_dir.glob("*"))
    if model_files:
        print("🤖 MODELOS:")
        for file in model_files:
            print(f"   📄 {file.name}")
    else:
        print("⚠️  No se encontraron archivos de modelos")

# Listar archivos de gráficos
if IS_KAGGLE:
    plots_dir = Path(f"{WORKING_DIR}/plots")
else:
    plots_dir = Path("../plots")

if plots_dir.exists():
    plot_files = list(plots_dir.glob("*.png"))
    if plot_files:
        print("\n📊 GRÁFICOS:")
        for file in plot_files:
            print(f"   🖼️  {file.name}")
    
    # Mostrar README de plots si existe
    readme_plots = plots_dir / "README_PLOTS.md"
    if readme_plots.exists():
        print(f"   📋 README_PLOTS.md")
else:
    print("⚠️  No se encontraron archivos de gráficos")

print(f"\n🌍 Entorno: {'Kaggle' if IS_KAGGLE else 'Local'}")
print(f"📂 Directorio base: {WORKING_DIR}")
