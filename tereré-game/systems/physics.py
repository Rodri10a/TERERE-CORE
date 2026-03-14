"""Sistema de física para personajes."""

from core.settings import GRAVITY, GROUND_Y, SCREEN_WIDTH


class PhysicsSystem:
    """Aplica gravedad, colisión con suelo y salto a los personajes."""

    def __init__(self, gravity: float = GRAVITY, ground_y: int = GROUND_Y) -> None:
        self.gravity = gravity
        self.ground_y = ground_y

    def apply_gravity(self, character) -> None:
        """Aplica gravedad al personaje."""
        if not character.on_ground:
            character.vel_y += self.gravity

    def check_ground(self, character) -> None:
        """Verifica y resuelve colisión con el suelo."""
        if character.y + character.height >= self.ground_y:
            character.y = self.ground_y - character.height
            character.vel_y = 0
            character.on_ground = True

    def apply_movement(self, character) -> None:
        """Aplica velocidades y fricción."""
        character.x += character.vel_x
        character.y += character.vel_y
        character.vel_x *= 0.85

        # Limitar a pantalla
        if character.x < 0:
            character.x = 0
        if character.x + character.width > SCREEN_WIDTH:
            character.x = SCREEN_WIDTH - character.width

    def update(self, character) -> None:
        """Aplica toda la física a un personaje en un frame."""
        self.apply_gravity(character)
        self.apply_movement(character)
        self.check_ground(character)
