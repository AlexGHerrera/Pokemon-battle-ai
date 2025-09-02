# Pokemon Battle AI - Exploratory Data Analysis

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🎯 Objetivo del Proyecto

Desarrollo de un **modelo de inteligencia artificial capaz de jugar Pokemon de forma autónoma** contra usuarios humanos. Este repositorio contiene el análisis exploratorio de datos (EDA) completo del dataset de batallas Pokemon Showdown, diseñado para extraer insights estratégicos y preparar los datos para el entrenamiento del modelo de IA.

## 📊 Dataset

- **Fuente**: Batallas reales de Pokemon Showdown (formato gen9randombattle)
- **Volumen**: ~14,000 batallas individuales
- **Formato**: JSON estructurado con turnos secuenciales
- **Contenido**: Eventos de batalla, estados del juego, metadata de jugadores, resultados

## 🚀 Características Principales

### ✨ Análisis Completo
- **Análisis de calidad de datos** con validación de integridad
- **Patrones estratégicos** que revelan comportamientos ganadores
- **Análisis del meta** de Pokemon más utilizados y efectivos
- **Visualizaciones explicativas** para insights del modelo de IA

### ⚡ Optimizaciones de Rendimiento
- **Muestreo inteligente** para desarrollo rápido (2000 batallas por defecto)
- **Conversión a Parquet** para acceso 10-20x más rápido
- **Procesamiento por chunks** para evitar problemas de memoria
- **Carga optimizada** con modo desarrollo/producción

### 📈 Feature Engineering
- **Métricas de batalla** (duración, eventos, ratios estratégicos)
- **Información de equipos** (niveles, tipos, estadísticas)
- **Patrones temporales** (eventos por turno, intensidad de acción)
- **Features estructuradas** listas para machine learning

## 📁 Estructura del Proyecto

```
Pokemon_battle/
├── data/
│   ├── battles/                    # Batallas individuales JSON
│   ├── all_battles.json           # Dataset consolidado
│   └── battles_sample_*.json      # Muestras para desarrollo
├── output/                        # Visualizaciones y resultados
├── EDA_notebook_ready.ipynb       # Notebook principal del EDA
├── EDA_notebook_ready.py          # Versión Python del notebook
├── EDA_comprehensive.py           # Script completo de análisis
└── README.md                      # Este archivo
```

## 🛠️ Instalación y Configuración

### Prerrequisitos

```bash
Python 3.8+
```

### Dependencias

```bash
pip install pandas numpy matplotlib seaborn jupyterlab jupytext
```

### Instalación Opcional (Parquet)

```bash
pip install pyarrow  # Para formato Parquet optimizado
```

## 🚀 Uso Rápido

### 1. Modo Desarrollo (Recomendado)

```python
# Carga rápida con muestra de 2000 batallas
battles = load_battles_optimized(use_sample=True, sample_size=2000)
```

### 2. Dataset Completo

```python
# Carga completa para análisis final
battles = load_battles_optimized(use_sample=False)
```

### 3. Formato Optimizado

```python
# Conversión una sola vez a Parquet
convert_to_parquet()

# Carga súper rápida desde Parquet
df_battles = load_parquet_if_exists()
```

## 📓 Ejecutar el Análisis

### Opción 1: Jupyter Notebook (Recomendado)

```bash
jupyter lab EDA_notebook_ready.ipynb
```

### Opción 2: Script Python

```bash
python EDA_comprehensive.py
```

### Opción 3: Conversión con Jupytext

```bash
# Convertir .py a .ipynb
jupytext --to ipynb EDA_notebook_ready.py

# Sincronizar cambios
jupytext --sync EDA_notebook_ready.ipynb
```

## 📊 Resultados del Análisis

El EDA genera automáticamente:

- **`battle_patterns_analysis.png`** - Patrones de duración y eventos
- **`pokemon_analysis.png`** - Análisis de uso de Pokemon
- **`correlation_matrix.png`** - Correlaciones entre features
- **`battle_features.csv`** - Dataset de features para ML

## 🎯 Insights Clave para IA

### Patrones Estratégicos Identificados:
- **Balance de jugadores**: Distribución equilibrada de victorias p1 vs p2
- **Duración óptima**: Batallas de 15-25 turnos muestran mayor complejidad estratégica
- **Meta dominante**: Top 15 Pokemon más utilizados representan 60% del uso total
- **Eventos críticos**: Ratio movimientos/switches indica agresividad vs cautela

### Features Relevantes para ML:
- **Métricas temporales**: `events_per_turn`, `total_turns`
- **Patrones de acción**: `move_events`, `switch_events`, `damage_events`
- **Contexto de jugador**: `ladder_rating_pre`, `team_composition`
- **Estado de batalla**: `weather_conditions`, `side_conditions`

## 🔧 Configuración Avanzada

### Personalizar Tamaño de Muestra

```python
# Muestra pequeña para pruebas rápidas
battles = create_sample_dataset(sample_size=500)

# Muestra grande para análisis detallado
battles = create_sample_dataset(sample_size=5000)
```

### Optimización de Memoria

```python
# Procesamiento por chunks para datasets grandes
chunk_size = 1000  # Ajustar según memoria disponible
```

## 📈 Próximos Pasos

1. **Feature Engineering Avanzado**
   - Secuencias temporales de turnos
   - Embeddings de Pokemon y movimientos
   - Estados de campo contextuales

2. **Modelado de IA**
   - Arquitectura de red neuronal recurrente
   - Aprendizaje por refuerzo para toma de decisiones
   - Evaluación contra jugadores humanos

3. **Optimizaciones**
   - Pipeline de preprocessing automatizado
   - Métricas de evaluación especializadas
   - Sistema de entrenamiento distribuido

## 🤝 Contribuir

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 👥 Autores

- **Alex G. Herrera** - *Desarrollo inicial* - [GitHub](https://github.com/alexg-herrera)

## 🙏 Agradecimientos

- **Pokemon Showdown** por proporcionar los datos de batalla
- **Comunidad Pokemon competitivo** por los insights estratégicos
- **HackABoss** por el framework de desarrollo del proyecto

## 📞 Contacto

Para preguntas o colaboraciones:
- **Email**: alex.herrera@hackaboss.com
- **LinkedIn**: [Alex G. Herrera](https://linkedin.com/in/alexg-herrera)
- **GitHub**: [@alexg-herrera](https://github.com/alexg-herrera)

---

⭐ **¡Dale una estrella si este proyecto te resulta útil!** ⭐
