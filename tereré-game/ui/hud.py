"""HUD (Heads-Up Display) para el modo de pelea."""

import pygame
from core.settings import SCREEN_WIDTH, WHITE, BLACK, RED, GREEN, YELLOW
from ui.text_renderer import TextRenderer


class HUD:
    """Muestra barras de vida, puntaje y nivel durante la pelea."""

    def __init__(self) -> None:
        self.text = TextRenderer()

    def _draw_health_bar(
        self,
        screen: pygame.Surface,
        x: int,
        y: int,
        width: int,
        height: int,
        health: int,
        max_health: int,
        reverse: bool = False
    ) -> None:
        

        bar_y = y + 12

        # Fondo
        
        pygame.draw.rect(screen, (40, 40, 40), (x, bar_y, width, height))

        # Ratio de vida
        ratio = max(0, health / max_health)
        bar_width = int(width * ratio)

        # Color según la vida
        if ratio > 0.5:
            color = GREEN
        elif ratio > 0.25:
            color = YELLOW
        else:
            color = RED

        # Barra
        if reverse:
            bar_x = x + width - bar_width
        else:
            bar_x = x
        
        pygame.draw.rect(screen, color, (bar_x, bar_y, bar_width, height))

        # Borde
        pygame.draw.rect(screen, WHITE, (x, bar_y, width, height), 1)


    # Dividir la barra de vida del Capiateño (_player) y los enemigos (_enemy)

    def _draw_player_health_bar(self, screen: pygame.Surface, player) -> None:

        """Dibuja la barra de vida y nombre del jugador."""

        # Redefinir coordenadas (x, y)
        x = 10
        y = 10
        width = 200
        height = 20
        self.text.render(screen, "CAPIATENO", x, y - 2, 16, WHITE)

        # HP dividido del Capiateño
        hp_text = f"{player.health}/{player.max_health}"
        self.text.render(screen, hp_text, x + 70, y + 14, 16, WHITE)

        self._draw_health_bar(
            screen,
            10,
            10,
            200,
            20,
            player.health,
            player.max_health
        )

    def _draw_enemy_health_bar(self, screen: pygame.Surface, enemy) -> None:
        """Dibuja la barra de vida del enemigo."""

        # Redefinir coordenadas (x, y)
        x = SCREEN_WIDTH - 210
        y = 10
        width = 200
        height = 20

        name = "CHETO"
        size = 16

        font = self.text._get_font(size)
        surface = font.render(name, True, WHITE)
        text_width = surface.get_width()

        self.text.render(screen, "CHETO", x + 150, y - 2, 16, WHITE)

        # HP dividido del Enemigo
        hp_text = f"{enemy.health}/{enemy.max_health}"
        size = 16

        font = self.text._get_font(size)
        surface = font.render(hp_text, True, WHITE)
        text_width = surface.get_width()

        self.text.render(screen, hp_text, x + width - text_width, y + 14, size, WHITE)

        self._draw_health_bar(
            screen,
            SCREEN_WIDTH - 210,
            10,
            200,
            20,
            enemy.health,
            enemy.max_health,
            reverse=True
        )

    def draw(self, screen: pygame.Surface, player, enemy, score: int, level: int) -> None:
        """Dibuja el HUD completo."""

        # Fondo semitransparente del HUD
        hud_bg = pygame.Surface((SCREEN_WIDTH, 55), pygame.SRCALPHA)
        hud_bg.fill((0, 0, 0, 120))
        screen.blit(hud_bg, (0, 0))

        # Barras de vida del jugador y del enemigo separadas
        self._draw_player_health_bar(screen, player)
        self._draw_enemy_health_bar(screen, enemy)

        # Puntaje
        self.text.render_centered(screen, f"SCORE: {score}", 8, 22, YELLOW)

        # Nivel
        self.text.render_centered(screen, f"NIVEL {level}", 32, 18, WHITE)