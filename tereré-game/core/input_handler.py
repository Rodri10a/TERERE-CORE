"""Sistema centralizado de entrada de teclado."""

import pygame


# Mapeo de acciones a teclas (soporta múltiples teclas por acción)
ACTION_MAP: dict[str, list[int]] = {
    "MOVE_LEFT": [pygame.K_LEFT, pygame.K_a],
    "MOVE_RIGHT": [pygame.K_RIGHT, pygame.K_d],
    "JUMP": [pygame.K_SPACE, pygame.K_w],
    "ATTACK": [pygame.K_z],
    "SPECIAL": [pygame.K_x],
    "UP": [pygame.K_UP, pygame.K_w],
    "DOWN": [pygame.K_DOWN, pygame.K_s],
    "CONFIRM": [pygame.K_RETURN],
    "BACK": [pygame.K_ESCAPE],
}


class InputHandler:
    """Centraliza el manejo de input del teclado con detección de pulsación y liberación."""

    def __init__(self) -> None:
        self._current_keys: dict[int, bool] = {}
        self._previous_keys: dict[int, bool] = {}

    def is_pressed(self, action: str) -> bool:
        """Retorna True si alguna tecla de la acción está presionada."""
        keys = ACTION_MAP.get(action)
        if keys is None:
            return False
        return any(self._current_keys.get(k, False) for k in keys)

    def was_just_pressed(self, action: str) -> bool:
        """Retorna True solo en el frame en que alguna tecla de la acción se presionó."""
        keys = ACTION_MAP.get(action)
        if keys is None:
            return False
        for k in keys:
            current = self._current_keys.get(k, False)
            previous = self._previous_keys.get(k, False)
            if current and not previous:
                return True
        return False

    def was_just_released(self, action: str) -> bool:
        """Retorna True solo en el frame en que alguna tecla de la acción se soltó."""
        keys = ACTION_MAP.get(action)
        if keys is None:
            return False
        for k in keys:
            current = self._current_keys.get(k, False)
            previous = self._previous_keys.get(k, False)
            if not current and previous:
                return True
        return False

    def update(self) -> None:
        """Actualiza el estado de las teclas. Llamar una vez por frame antes de procesar eventos."""
        self._previous_keys = self._current_keys.copy()
        keys = pygame.key.get_pressed()
        for action, key_list in ACTION_MAP.items():
            for k in key_list:
                self._current_keys[k] = keys[k]
