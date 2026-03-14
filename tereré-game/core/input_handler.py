"""Sistema centralizado de entrada de teclado."""

import pygame


# Mapeo de acciones a teclas
ACTION_MAP: dict[str, int] = {
    "MOVE_LEFT": pygame.K_LEFT,
    "MOVE_RIGHT": pygame.K_RIGHT,
    "JUMP": pygame.K_SPACE,
    "ATTACK": pygame.K_z,
    "SPECIAL": pygame.K_x,
    "UP": pygame.K_UP,
    "DOWN": pygame.K_DOWN,
    "CONFIRM": pygame.K_RETURN,
    "BACK": pygame.K_ESCAPE,
}


class InputHandler:
    """Centraliza el manejo de input del teclado con detección de pulsación y liberación."""

    def __init__(self) -> None:
        self._current_keys: dict[int, bool] = {}
        self._previous_keys: dict[int, bool] = {}
