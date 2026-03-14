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

    def is_pressed(self, action: str) -> bool:
        """Retorna True si la tecla de la acción está presionada."""
        key = ACTION_MAP.get(action)
        if key is None:
            return False
        return self._current_keys.get(key, False)

    def was_just_pressed(self, action: str) -> bool:
        """Retorna True solo en el frame en que la tecla se presionó."""
        key = ACTION_MAP.get(action)
        if key is None:
            return False
        current = self._current_keys.get(key, False)
        previous = self._previous_keys.get(key, False)
        return current and not previous

    def was_just_released(self, action: str) -> bool:
        """Retorna True solo en el frame en que la tecla se soltó."""
        key = ACTION_MAP.get(action)
        if key is None:
            return False
        current = self._current_keys.get(key, False)
        previous = self._previous_keys.get(key, False)
        return not current and previous

    def update(self) -> None:
        """Actualiza el estado de las teclas. Llamar una vez por frame antes de procesar eventos."""
        self._previous_keys = self._current_keys.copy()
        keys = pygame.key.get_pressed()
        for action, key in ACTION_MAP.items():
            self._current_keys[key] = keys[key]
