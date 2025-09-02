/**
 * Pokemon Battle AI - Frontend Game Logic
 * =====================================
 * 
 * Maneja la lógica del juego y comunicación con el backend.
 */

class PokemonBattleGame {
    constructor() {
        this.sessionId = null;
        this.gameActive = false;
        this.currentTurn = 1;
        this.apiBaseUrl = 'http://localhost:5000/api';
        
        this.initializeEventListeners();
        this.checkServerStatus();
    }

    /**
     * Inicializa los event listeners de la interfaz.
     */
    initializeEventListeners() {
        // Botones principales
        document.getElementById('new-game-btn').addEventListener('click', () => this.startNewGame());
        document.getElementById('end-game-btn').addEventListener('click', () => this.endGame());
        document.getElementById('help-btn').addEventListener('click', () => this.showHelp());
        document.getElementById('stats-btn').addEventListener('click', () => this.showStats());

        // Botones de acción
        document.querySelectorAll('.action-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const action = e.currentTarget.dataset.action;
                this.handlePlayerAction(action);
            });
        });

        // Botones de movimientos en modal
        document.querySelectorAll('.move-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const move = e.currentTarget.dataset.move;
                this.selectMove(move);
            });
        });
    }

    /**
     * Verifica el estado del servidor.
     */
    async checkServerStatus() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/health`);
            const data = await response.json();
            
            if (data.status === 'healthy') {
                this.updateStatusBadge('success', 'Conectado');
            } else {
                this.updateStatusBadge('warning', 'Servidor con problemas');
            }
        } catch (error) {
            console.error('Error verificando estado del servidor:', error);
            this.updateStatusBadge('danger', 'Desconectado');
        }
    }

    /**
     * Actualiza el badge de estado de conexión.
     */
    updateStatusBadge(type, text) {
        const badge = document.getElementById('status-badge');
        badge.className = `badge bg-${type} me-3`;
        badge.innerHTML = `<i class="fas fa-circle"></i> ${text}`;
    }

    /**
     * Inicia una nueva partida.
     */
    async startNewGame() {
        try {
            this.showLoading('Iniciando nueva partida...');
            
            const response = await fetch(`${this.apiBaseUrl}/game/start`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            const data = await response.json();

            if (data.success) {
                this.sessionId = data.session_id;
                this.gameActive = true;
                this.currentTurn = 1;
                
                this.updateTurnCounter(1);
                this.clearBattleLog();
                this.addLogEntry('system', '¡Nueva batalla iniciada! Elige tu primera acción.');
                this.enableGameControls();
                
                console.log('Nueva partida iniciada:', data.session_id);
            } else {
                this.showError('Error iniciando partida: ' + data.error);
            }
        } catch (error) {
            console.error('Error iniciando partida:', error);
            this.showError('Error de conexión al iniciar partida');
        } finally {
            this.hideLoading();
        }
    }

    /**
     * Maneja las acciones del jugador.
     */
    async handlePlayerAction(action) {
        if (!this.gameActive) {
            this.showError('No hay partida activa');
            return;
        }

        switch (action) {
            case 'attack':
                this.showMoveSelection();
                break;
            case 'switch':
                this.handleSwitch();
                break;
            case 'item':
                this.handleItem();
                break;
            case 'run':
                this.handleRun();
                break;
        }
    }

    /**
     * Muestra el modal de selección de movimientos.
     */
    showMoveSelection() {
        const modal = new bootstrap.Modal(document.getElementById('moveModal'));
        modal.show();
    }

    /**
     * Selecciona un movimiento específico.
     */
    async selectMove(moveName) {
        // Cerrar modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('moveModal'));
        modal.hide();

        const action = {
            type: 'move',
            move_name: moveName,
            target: 'opponent'
        };

        await this.sendPlayerMove(action);
    }

    /**
     * Maneja el cambio de Pokemon.
     */
    async handleSwitch() {
        const action = {
            type: 'switch',
            pokemon_index: 1 // Simplificado por ahora
        };

        await this.sendPlayerMove(action);
    }

    /**
     * Maneja el uso de objetos.
     */
    async handleItem() {
        const action = {
            type: 'item',
            item_name: 'potion',
            target: 'self'
        };

        await this.sendPlayerMove(action);
    }

    /**
     * Maneja la huida del combate.
     */
    async handleRun() {
        if (confirm('¿Estás seguro de que quieres huir? Perderás la batalla.')) {
            await this.endGame('ai');
        }
    }

    /**
     * Envía el movimiento del jugador al servidor.
     */
    async sendPlayerMove(action) {
        try {
            this.disableGameControls();
            this.showAIThinking();
            
            this.addLogEntry('player', `Jugador usa ${this.formatActionText(action)}`);

            const response = await fetch(`${this.apiBaseUrl}/game/${this.sessionId}/move`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ action })
            });

            const data = await response.json();

            if (data.success) {
                // Mostrar movimiento de IA
                setTimeout(() => {
                    this.addLogEntry('ai', `IA usa ${this.formatActionText(data.ai_action)}`);
                    this.updateTurnCounter(data.turn);
                    this.hideAIThinking();
                    this.enableGameControls();
                }, 1500); // Simular tiempo de pensamiento de IA
                
            } else {
                this.showError('Error procesando movimiento: ' + data.error);
                this.enableGameControls();
                this.hideAIThinking();
            }
        } catch (error) {
            console.error('Error enviando movimiento:', error);
            this.showError('Error de conexión');
            this.enableGameControls();
            this.hideAIThinking();
        }
    }

    /**
     * Formatea el texto de una acción para mostrar en el log.
     */
    formatActionText(action) {
        switch (action.type) {
            case 'move':
                return `${action.move_name}`;
            case 'switch':
                return `cambio de Pokemon`;
            case 'item':
                return `${action.item_name}`;
            default:
                return action.type;
        }
    }

    /**
     * Termina la partida actual.
     */
    async endGame(winner = null) {
        if (!this.gameActive) return;

        try {
            const response = await fetch(`${this.apiBaseUrl}/game/${this.sessionId}/end`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ winner })
            });

            const data = await response.json();

            if (data.success) {
                this.gameActive = false;
                this.sessionId = null;
                
                const winnerText = winner === 'player' ? 'Jugador' : 
                                 winner === 'ai' ? 'IA' : 'Nadie';
                
                this.addLogEntry('system', `¡Batalla terminada! Ganador: ${winnerText}`);
                this.disableGameControls();
                
                console.log('Partida terminada:', data);
            }
        } catch (error) {
            console.error('Error terminando partida:', error);
        }
    }

    /**
     * Muestra estadísticas del sistema.
     */
    async showStats() {
        try {
            const modal = new bootstrap.Modal(document.getElementById('statsModal'));
            modal.show();

            const response = await fetch(`${this.apiBaseUrl}/stats`);
            const data = await response.json();

            const statsContent = document.getElementById('stats-content');
            statsContent.innerHTML = `
                <div class="row g-3">
                    <div class="col-6">
                        <div class="card text-center">
                            <div class="card-body">
                                <h5 class="card-title">${data.active_sessions}</h5>
                                <p class="card-text">Sesiones Activas</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="card text-center">
                            <div class="card-body">
                                <h5 class="card-title">${data.total_sessions}</h5>
                                <p class="card-text">Total de Partidas</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-12">
                        <div class="card">
                            <div class="card-body">
                                <h6>Estado del Modelo IA:</h6>
                                <span class="badge ${data.ai_model_status === 'loaded' ? 'bg-success' : 'bg-warning'}">
                                    ${data.ai_model_status === 'loaded' ? 'Cargado' : 'No Cargado'}
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        } catch (error) {
            console.error('Error obteniendo estadísticas:', error);
            document.getElementById('stats-content').innerHTML = 
                '<div class="alert alert-danger">Error cargando estadísticas</div>';
        }
    }

    /**
     * Muestra el modal de ayuda.
     */
    showHelp() {
        const modal = new bootstrap.Modal(document.getElementById('helpModal'));
        modal.show();
    }

    /**
     * Añade una entrada al log de batalla.
     */
    addLogEntry(type, message) {
        const battleLog = document.getElementById('battle-log');
        const entry = document.createElement('div');
        entry.className = `log-entry ${type}`;
        
        let icon;
        switch (type) {
            case 'player':
                icon = 'fas fa-user';
                break;
            case 'ai':
                icon = 'fas fa-robot';
                break;
            default:
                icon = 'fas fa-info-circle';
        }
        
        entry.innerHTML = `
            <i class="${icon}"></i>
            <span>${message}</span>
        `;
        
        battleLog.appendChild(entry);
        battleLog.scrollTop = battleLog.scrollHeight;
    }

    /**
     * Limpia el log de batalla.
     */
    clearBattleLog() {
        document.getElementById('battle-log').innerHTML = '';
    }

    /**
     * Actualiza el contador de turnos.
     */
    updateTurnCounter(turn) {
        document.getElementById('turn-counter').textContent = turn;
        this.currentTurn = turn;
    }

    /**
     * Habilita los controles del juego.
     */
    enableGameControls() {
        document.querySelectorAll('.action-btn').forEach(btn => {
            btn.disabled = false;
            btn.classList.remove('loading');
        });
        
        document.querySelector('.player-status .badge').textContent = 'Tu Turno';
        document.querySelector('.player-status .badge').className = 'badge bg-light text-dark';
    }

    /**
     * Deshabilita los controles del juego.
     */
    disableGameControls() {
        document.querySelectorAll('.action-btn').forEach(btn => {
            btn.disabled = true;
            btn.classList.add('loading');
        });
    }

    /**
     * Muestra que la IA está pensando.
     */
    showAIThinking() {
        const aiStatus = document.querySelector('.ai-status .badge');
        aiStatus.textContent = 'Pensando...';
        aiStatus.className = 'badge bg-warning text-dark thinking';
        
        const playerStatus = document.querySelector('.player-status .badge');
        playerStatus.textContent = 'Esperando IA';
        playerStatus.className = 'badge bg-secondary';
    }

    /**
     * Oculta el indicador de IA pensando.
     */
    hideAIThinking() {
        const aiStatus = document.querySelector('.ai-status .badge');
        aiStatus.textContent = 'Listo';
        aiStatus.className = 'badge bg-light text-dark';
    }

    /**
     * Muestra un mensaje de carga.
     */
    showLoading(message) {
        // Implementar overlay de carga si es necesario
        console.log('Loading:', message);
    }

    /**
     * Oculta el mensaje de carga.
     */
    hideLoading() {
        // Ocultar overlay de carga
        console.log('Loading finished');
    }

    /**
     * Muestra un mensaje de error.
     */
    showError(message) {
        this.addLogEntry('system', `Error: ${message}`);
        console.error('Game Error:', message);
    }
}

// Inicializar el juego cuando se carga la página
document.addEventListener('DOMContentLoaded', () => {
    window.pokemonGame = new PokemonBattleGame();
    
    // Verificar estado del servidor cada 30 segundos
    setInterval(() => {
        window.pokemonGame.checkServerStatus();
    }, 30000);
});
