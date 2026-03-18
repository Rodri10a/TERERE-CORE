"""HUD (Heads-Up Display) para el modo de pelea."""

import pygame
from core.settings import SCREEN_WIDTH, WHITE, RED, GREEN, YELLOW
from ui.text_renderer import TextRenderer


class HUD:
    """Muestra barras de vida, puntaje y nivel durante la pelea."""

    def __init__(self) -> None:
        self.text = TextRenderer()

    def _draw_health_bar(self, screen: pygame.Surface, x: int, y: int,
                         width: int, height: int, health: int,
                         max_health: int, label: str,
                         align_right: bool = False) -> None:
        """Dibuja una barra de vida con nombre y porcentaje."""
        # Nombre del personaje
        font = self.text._get_font(14)
        name_surf = font.render(label, True, WHITE)
        if align_right:
            name_x = x + width - name_surf.get_width()
        else:
            name_x = x
        screen.blit(name_surf, (name_x, y))

        bar_y = y + 22
        # Fondo de la barra
        pygame.draw.rect(screen, (30, 30, 30), (x, bar_y, width, height))

        # Barra de vida con color segun porcentaje
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
        pygame.draw.rect(screen, WHITE, (x, bar_y, width, height), 2)

        # Texto de vida centrado en la barra
        hp_text = f"{health}/{max_health}"
        hp_font = self.text._get_font(11)
        hp_surf = hp_font.render(hp_text, True, WHITE)
        hp_x = x + (width - hp_surf.get_width()) // 2
        hp_y = bar_y + (height - hp_surf.get_height()) // 2
        screen.blit(hp_surf, (hp_x, hp_y))

    def draw(self, screen: pygame.Surface, player, enemy,
             score: int, level: int, player_name: str = "CAPIATEÑO") -> None:
        """Dibuja el HUD completo."""
        # Fondo semitransparente del HUD
        hud_bg = pygame.Surface((SCREEN_WIDTH, 60), pygame.SRCALPHA)
        hud_bg.fill((0, 0, 0, 140))
        screen.blit(hud_bg, (0, 0))

        # Barra de vida del jugador (izquierda)
        self._draw_health_bar(screen, 20, 8, 250, 24,
                              player.health, player.max_health,
                              player_name.upper())

        # Barra de vida del enemigo (derecha)
        self._draw_health_bar(screen, SCREEN_WIDTH - 270, 8, 250, 24,
                              enemy.health, enemy.max_health,
                              "GUARDIA", align_right=True)

        # Puntaje y nivel (centro)
        self.text.render_centered(screen, f"SCORE: {score}", 10, 20, YELLOW)
        self.text.render_centered(screen, f"NIVEL {level}", 34, 14, WHITE)
