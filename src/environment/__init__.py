"""
Environment Module
==================

Pokemon battle environment compatible with OpenAI Gym.

Components:
- battle_env: Main Gym environment
- battle_state: State representation
- action_space: Action space definition
- showdown_client: Pokemon Showdown API client (future)
"""

__all__ = ['PokemonBattleEnv', 'BattleState', 'ActionSpace']
