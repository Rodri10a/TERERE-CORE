"""Gestor de estados del juego."""

from __future__ import annotations
from typing import Any, Optional, TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from core.input_handler import InputHandler


class StateManager:
    """Maneja las transiciones entre estados del juego (menú, pelea, minijuego, etc.)."""

    def __init__(self, screen: pygame.Surface, input_handler: InputHandler) -> None:
        self.screen = screen
        self.input_handler = input_handler
        self.current_state: Optional[Any] = None
        self.shared_data: dict[str, Any] = {
            "score": 0,
            "current_level": 1,
            "player_health": 100,
        }
        self.should_quit: bool = False
        self._states: dict[str, Any] = {}

    def _get_state(self, state_name: str) -> Any:
        """Obtiene o crea la instancia del estado solicitado."""
        if state_name == "menu":
            from states.menu_state import MenuState
            return MenuState(self.screen, self, self.input_handler)
        elif state_name == "game":
            from states.game_state import GameState
            return GameState(self.screen, self, self.input_handler)
        elif state_name == "minigame":
            from states.minigame_state import MinigameState
            return MinigameState(self.screen, self, self.input_handler)
        elif state_name == "gameover":
            from states.gameover_state import GameOverState
            return GameOverState(self.screen, self, self.input_handler)
        elif state_name == "victory":
            from states.victory_state import VictoryState
            return VictoryState(self.screen, self, self.input_handler)
        return None

    def change_state(self, state_name: str, **kwargs: Any) -> None:
        """Cambia al estado especificado, pasando datos adicionales."""
        self.shared_data.update(kwargs)
        self.current_state = self._get_state(state_name)

    def handle_events(self, event: pygame.event.Event) -> None:
        """Pasa eventos al estado actual."""
        if self.current_state:
            self.current_state.handle_events(event)
