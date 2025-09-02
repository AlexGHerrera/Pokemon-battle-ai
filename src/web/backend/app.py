"""
Servidor Backend para Pokemon Battle AI
=======================================

API REST para la interfaz web del juego Pokemon.
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import torch
import numpy as np
from typing import Dict, List, Optional
import logging
import json
from datetime import datetime
import os

from ...models.architectures import PokemonBattleNet
from ...training.trainer import PokemonTrainer
from ...data.processors import BattleDataProcessor

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar Flask
app = Flask(__name__)
CORS(app)  # Permitir requests desde frontend

# Variables globales
ai_model = None
trainer = None
game_sessions = {}  # Almacenar sesiones de juego activas


class GameSession:
    """Representa una sesión de juego entre humano y IA."""
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.created_at = datetime.now()
        self.moves_history = []
        self.game_state = self._initialize_game_state()
        self.is_active = True
    
    def _initialize_game_state(self) -> Dict:
        """Inicializa el estado del juego."""
        return {
            'turn': 1,
            'player_team': [],
            'ai_team': [],
            'field_conditions': {},
            'weather': None,
            'current_player_pokemon': None,
            'current_ai_pokemon': None
        }
    
    def add_move(self, player: str, action: Dict) -> None:
        """Añade un movimiento al historial."""
        self.moves_history.append({
            'turn': self.game_state['turn'],
            'player': player,
            'action': action,
            'timestamp': datetime.now().isoformat()
        })
    
    def get_battle_data(self) -> Dict:
        """Convierte la sesión en formato de datos de batalla."""
        return {
            'session_id': self.session_id,
            'events': self.moves_history,
            'turns': self.game_state['turn'],
            'winner': None,  # Se determinará al final
            'timestamp': self.created_at.isoformat()
        }


def load_ai_model() -> None:
    """Carga el modelo de IA entrenado."""
    global ai_model, trainer
    
    try:
        # Configuración del modelo
        model_config = {
            'input_size': 512,
            'hidden_sizes': [256, 128, 64],
            'num_actions': 10,
            'dropout_rate': 0.2
        }
        
        # Crear modelo
        ai_model = PokemonBattleNet(**model_config)
        trainer = PokemonTrainer(ai_model)
        
        # Intentar cargar modelo entrenado
        model_path = 'src/models/pretrained/pokemon_ai_model.pth'
        if os.path.exists(model_path):
            trainer.load_model(model_path)
            logger.info("Modelo de IA cargado exitosamente")
        else:
            logger.warning("No se encontró modelo entrenado, usando modelo aleatorio")
            
    except Exception as e:
        logger.error(f"Error cargando modelo de IA: {e}")


@app.route('/')
def index():
    """Página principal del juego."""
    return render_template('index.html')


@app.route('/api/health', methods=['GET'])
def health_check():
    """Endpoint de salud del servidor."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'ai_model_loaded': ai_model is not None
    })


@app.route('/api/game/start', methods=['POST'])
def start_game():
    """Inicia una nueva sesión de juego."""
    try:
        # Generar ID de sesión único
        session_id = f"game_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(game_sessions)}"
        
        # Crear nueva sesión
        session = GameSession(session_id)
        game_sessions[session_id] = session
        
        logger.info(f"Nueva sesión de juego iniciada: {session_id}")
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'game_state': session.game_state,
            'message': 'Juego iniciado exitosamente'
        })
        
    except Exception as e:
        logger.error(f"Error iniciando juego: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/game/<session_id>/move', methods=['POST'])
def make_move(session_id: str):
    """Procesa un movimiento del jugador y genera respuesta de IA."""
    try:
        # Verificar sesión
        if session_id not in game_sessions:
            return jsonify({
                'success': False,
                'error': 'Sesión de juego no encontrada'
            }), 404
        
        session = game_sessions[session_id]
        data = request.get_json()
        
        # Procesar movimiento del jugador
        player_action = data.get('action')
        session.add_move('human', player_action)
        
        # Generar movimiento de IA
        ai_action = generate_ai_move(session)
        session.add_move('ai', ai_action)
        
        # Actualizar estado del juego
        session.game_state['turn'] += 1
        
        logger.info(f"Movimiento procesado en sesión {session_id}")
        
        return jsonify({
            'success': True,
            'player_action': player_action,
            'ai_action': ai_action,
            'game_state': session.game_state,
            'turn': session.game_state['turn']
        })
        
    except Exception as e:
        logger.error(f"Error procesando movimiento: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/game/<session_id>/end', methods=['POST'])
def end_game(session_id: str):
    """Termina una sesión de juego y guarda datos para aprendizaje."""
    try:
        if session_id not in game_sessions:
            return jsonify({
                'success': False,
                'error': 'Sesión de juego no encontrada'
            }), 404
        
        session = game_sessions[session_id]
        data = request.get_json()
        
        # Determinar ganador
        winner = data.get('winner')
        session.is_active = False
        
        # Guardar datos de batalla para aprendizaje continuo
        battle_data = session.get_battle_data()
        battle_data['winner'] = winner
        
        save_battle_for_learning(battle_data)
        
        # Limpiar sesión
        del game_sessions[session_id]
        
        logger.info(f"Juego terminado: {session_id}, Ganador: {winner}")
        
        return jsonify({
            'success': True,
            'winner': winner,
            'total_turns': session.game_state['turn'],
            'message': 'Juego terminado y datos guardados'
        })
        
    except Exception as e:
        logger.error(f"Error terminando juego: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Obtiene estadísticas del sistema."""
    try:
        active_sessions = len([s for s in game_sessions.values() if s.is_active])
        
        return jsonify({
            'active_sessions': active_sessions,
            'total_sessions': len(game_sessions),
            'ai_model_status': 'loaded' if ai_model else 'not_loaded',
            'server_uptime': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error obteniendo estadísticas: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


def generate_ai_move(session: GameSession) -> Dict:
    """
    Genera un movimiento de IA basado en el estado actual del juego.
    
    Args:
        session: Sesión de juego actual
        
    Returns:
        Acción de IA
    """
    try:
        if ai_model is None:
            # Movimiento aleatorio si no hay modelo
            return {
                'type': 'move',
                'move_name': 'tackle',
                'target': 'opponent',
                'confidence': 0.1
            }
        
        # Convertir estado del juego a vector de características
        game_features = game_state_to_features(session.game_state)
        
        # Obtener predicción del modelo
        with torch.no_grad():
            features_tensor = torch.FloatTensor(game_features).unsqueeze(0)
            action_probabilities = ai_model(features_tensor)
            predicted_action = torch.argmax(action_probabilities, dim=1).item()
        
        # Convertir predicción a acción del juego
        ai_action = action_index_to_game_action(predicted_action)
        ai_action['confidence'] = float(torch.max(action_probabilities).item())
        
        return ai_action
        
    except Exception as e:
        logger.error(f"Error generando movimiento de IA: {e}")
        # Fallback a movimiento aleatorio
        return {
            'type': 'move',
            'move_name': 'tackle',
            'target': 'opponent',
            'confidence': 0.0
        }


def game_state_to_features(game_state: Dict) -> np.ndarray:
    """Convierte el estado del juego en vector de características."""
    # Implementación simplificada
    features = [
        game_state.get('turn', 0),
        len(game_state.get('player_team', [])),
        len(game_state.get('ai_team', [])),
        # Agregar más características según necesidades
    ]
    
    # Padding a tamaño fijo
    while len(features) < 512:
        features.append(0.0)
    
    return np.array(features[:512])


def action_index_to_game_action(action_index: int) -> Dict:
    """Convierte índice de acción a acción del juego."""
    # Mapeo simplificado
    actions = [
        {'type': 'move', 'move_name': 'tackle', 'target': 'opponent'},
        {'type': 'move', 'move_name': 'thunderbolt', 'target': 'opponent'},
        {'type': 'switch', 'pokemon_index': 1},
        # Agregar más acciones según necesidades
    ]
    
    if 0 <= action_index < len(actions):
        return actions[action_index]
    else:
        return actions[0]  # Acción por defecto


def save_battle_for_learning(battle_data: Dict) -> None:
    """Guarda datos de batalla para aprendizaje continuo."""
    try:
        # Crear directorio si no existe
        learning_dir = Path('data/continuous_learning')
        learning_dir.mkdir(parents=True, exist_ok=True)
        
        # Guardar batalla individual
        filename = f"battle_{battle_data['session_id']}.json"
        filepath = learning_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(battle_data, f, indent=2)
        
        logger.info(f"Datos de batalla guardados para aprendizaje: {filename}")
        
    except Exception as e:
        logger.error(f"Error guardando datos para aprendizaje: {e}")


if __name__ == '__main__':
    # Cargar modelo de IA al iniciar
    load_ai_model()
    
    # Iniciar servidor
    app.run(host='0.0.0.0', port=5000, debug=True)
