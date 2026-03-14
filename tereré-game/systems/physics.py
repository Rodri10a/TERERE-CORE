"""Sistema de física para personajes."""

from core.settings import GRAVITY, GROUND_Y, SCREEN_WIDTH


class PhysicsSystem:
    """Aplica gravedad, colisión con suelo y salto a los personajes."""

    def __init__(self, gravity: float = GRAVITY, ground_y: int = GROUND_Y) -> None:
        self.gravity = gravity
        self.ground_y = ground_y
