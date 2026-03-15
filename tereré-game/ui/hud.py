"""HUD (Heads-Up Display) para el modo de pelea."""

import pygame
from core.settings import SCREEN_WIDTH, WHITE, BLACK, RED, GREEN, YELLOW
from ui.text_renderer import TextRenderer


class HUD:
    """Muestra barras de vida, puntaje y nivel durante la pelea."""

    def __init__(self) -> None:
        self.text = TextRenderer()

    def _draw_health_bar(self, screen: pygame.Surface, x: int, y: int,
                         width: int, height: int, health: int,
                         max_health: int, label: str) -> None:
        """Dibuja una barra de vida con gradiente verde a rojo."""
        # Label
        self.text.render(screen, label, x, y - 2, 16, WHITE)

        bar_y = y + 12
        # Fondo
        pygame.draw.rect(screen, (40, 40, 40), (x, bar_y, width, height))

        # Barra de vida
        ratio = max(0, health / max_health)
        bar_width = int(width * ratio)
        if ratio > 0.5:
            color = GREEN
        elif ratio > 0.25:
            color = YELLOW
        else:
            color = RED
        pygame.draw.rect(screen, color, (x, bar_y, bar_width, height))

        # Borde
        pygame.draw.rect(screen, WHITE, (x, bar_y, width, height), 1)

        # Texto de vida
        hp_text = f"{health}/{max_health}"
        self.text.render(screen, hp_text, x + width // 2 - 20, bar_y + 2, 16, WHITE)

    def draw(self, screen: pygame.Surface, player, enemy,
             score: int, level: int, player_name: str = "CAPIATENO") -> None:
        """Dibuja el HUD completo."""
        # Fondo semitransparente del HUD
        hud_bg = pygame.Surface((SCREEN_WIDTH, 55), pygame.SRCALPHA)
        hud_bg.fill((0, 0, 0, 120))
        screen.blit(hud_bg, (0, 0))

        # Barra de vida del jugador
        self._draw_health_bar(screen, 10, 10, 200, 20,
                              player.health, player.max_health, player_name.upper())

        # Barra de vida del enemigo
        self._draw_health_bar(screen, SCREEN_WIDTH - 210, 10, 200, 20,
                              enemy.health, enemy.max_health, "CHETO")

        # Puntaje
        self.text.render_centered(screen, f"SCORE: {score}", 8, 22, YELLOW)

        # Nivel
        self.text.render_centered(screen, f"NIVEL {level}", 32, 18, WHITE)
