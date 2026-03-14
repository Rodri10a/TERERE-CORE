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
