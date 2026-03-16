"""Estado principal de pelea 2D."""

import os
import pygame
from core.settings import (SCREEN_WIDTH, SCREEN_HEIGHT, STATE_MINIGAME,
                           STATE_GAMEOVER, STATE_VICTORY, STATE_MENU, MAX_LEVELS,
                           GROUND_Y, WHITE, BLACK, SKY_BLUE, BROWN,
                           TERERE_GREEN, DARK_GREEN)
from ui.button import Button
from core.input_handler import InputHandler
from core.state_manager import StateManager
from entities.player import Player
from entities.enemy import Enemy
from systems.collision import CollisionSystem
from systems.score import ScoreSystem
from levels.level_loader import LevelLoader
from ui.hud import HUD
from ui.text_renderer import TextRenderer


class GameState:
    """Estado de pelea donde el jugador combate al cheto en cada nivel."""

    def __init__(self, screen: pygame.Surface, state_manager: StateManager,
                 input_handler: InputHandler) -> None:
        self.screen = screen
        self.state_manager = state_manager
        self.input_handler = input_handler
        self.collision = CollisionSystem()
        self.score_system = ScoreSystem()
        self.score_system.score = state_manager.shared_data.get("score", 0)
        self.level_loader = LevelLoader()
        self.hud = HUD()
        self.text = TextRenderer()

        self.current_level: int = state_manager.shared_data.get("current_level", 1)
        self.player_name: str = state_manager.shared_data.get("player_name", "Capiateno")
        self.character_file: str = state_manager.shared_data.get("character", "personaje_principal.jpg")
        self.level_data: dict = {}
        self.level_name: str = ""
        self.minigame_id: str = ""
        self.platforms: list = []
        self.bg_image: pygame.Surface | None = None

        # Pausa
        self.paused: bool = False
        self.show_instructions: bool = False
        self._setup_pause_buttons()

        # Transición
        self.transition_timer: int = 0
        self.show_level_intro: bool = True
        self.intro_timer: int = 180  # 3 segundos

        self.player: Player = Player(200, GROUND_Y - 250, input_handler, self.character_file)
        self.enemy: Enemy = Enemy(900, GROUND_Y - 100)

        self.load_level(self.current_level)

    def load_level(self, level_number: int) -> None:
        """Carga la configuración del nivel desde JSON."""
        self.level_data = self.level_loader.load_level(level_number)
        self.level_name = self.level_data.get("name", f"Nivel {level_number}")
        self.minigame_id = self.level_data.get("minigame", "terere_rush")
        self.platforms = self.level_data.get("platforms", [])

        enemy_config = self.level_data.get("enemy", {})
        enemy_speed = enemy_config.get("speed", 3)
        enemy_health = enemy_config.get("health", 100)
        enemy_damage = enemy_config.get("damage", 10)
        enemy_start_x = self.level_data.get("enemy_start_x", 600)

        self.enemy = Enemy(enemy_start_x, GROUND_Y - 100, speed=enemy_speed,
                           health=enemy_health, damage=enemy_damage)

        # Restaurar vida del jugador
        player_health = self.state_manager.shared_data.get("player_health", 100)
        self.player = Player(200, GROUND_Y - 250, self.input_handler, self.character_file)
        self.player.health = player_health

        # Cargar imagen de fondo del nivel
        self.bg_image = None
        bg_file = self.level_data.get("bg_image", "")
        if bg_file:
            bg_path = os.path.join(os.path.dirname(__file__), "..",
                                   "assets", "images", "backgrounds", bg_file)
            if os.path.exists(bg_path):
                self.bg_image = pygame.image.load(bg_path).convert()
                self.bg_image = pygame.transform.scale(
                    self.bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.show_level_intro = True
        self.intro_timer = 180

    def handle_events(self, event: pygame.event.Event) -> None:
        """Maneja eventos durante la pelea."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            self._on_enemy_defeated()
            return

        if self.show_level_intro and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.show_level_intro = False
            return

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if self.show_instructions:
                self.show_instructions = False
            elif not self.show_level_intro:
                self.paused = not self.paused

        if self.paused and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if self.pause_buttons["reanudar"].is_clicked(mouse_pos, True):
                self.paused = False
            elif self.pause_buttons["instrucciones"].is_clicked(mouse_pos, True):
                self.show_instructions = True
            elif self.pause_buttons["menu"].is_clicked(mouse_pos, True):
                self.state_manager.change_state(STATE_MENU)
            elif self.pause_buttons["salir"].is_clicked(mouse_pos, True):
                self.state_manager.should_quit = True

    def update(self, dt: float) -> None:
        """Actualiza toda la lógica del nivel de pelea."""
        # Intro del nivel - espera ENTER
        if self.show_level_intro:
            return

        if self.paused:
            return

        # Actualizar entidades
        self.player.update()
        self.enemy.update_ai(self.player.x, self.player.y)
        self.enemy.update()

        # Colisiones con plataformas elevadas
        if self.player.y + self.player.height < GROUND_Y:
            if not self.collision.check_ground_collision(self.player, self.platforms):
                self.player.on_ground = False
        if self.enemy.y + self.enemy.height < GROUND_Y:
            if not self.collision.check_ground_collision(self.enemy, self.platforms):
                self.enemy.on_ground = False

        # Colisiones de ataque del jugador
        if self.player.is_attacking and self.player.attack_active_frames > 0:
            if self.collision.check_attack_hit(self.player, self.enemy):
                dmg = self.player.get_current_damage()
                knockback = 1 if self.player.direction == 1 else -1
                self.enemy.take_damage(dmg, knockback)
                self.score_system.add_points(dmg * 10)
                self.player.attack_active_frames = 0  # Un hit por ataque

        # Colisiones de ataque del enemigo
        if self.enemy.is_attacking and self.enemy.attack_active_frames > 0:
            if self.collision.check_attack_hit(self.enemy, self.player):
                knockback = 1 if self.enemy.direction == 1 else -1
                self.player.take_damage(self.enemy.damage, knockback)
                self.enemy.attack_active_frames = 0

        # Verificar fin de pelea
        if not self.enemy.is_alive():
            self._on_enemy_defeated()
        elif not self.player.is_alive():
            self._on_player_defeated()

    def _on_enemy_defeated(self) -> None:
        """El jugador ganó la pelea del nivel."""
        score_bonus = self.level_data.get("score_bonus", 500)
        self.score_system.add_points(score_bonus)
        self.state_manager.shared_data["score"] = self.score_system.score
        self.state_manager.shared_data["player_health"] = self.player.health

        if self.current_level >= MAX_LEVELS:
            self.state_manager.change_state(STATE_VICTORY)
        else:
            self.state_manager.shared_data["current_level"] = self.current_level
            self.state_manager.shared_data["minigame_id"] = self.minigame_id
            self.state_manager.change_state(STATE_MINIGAME)

    def _on_player_defeated(self) -> None:
        """El jugador perdió."""
        self.state_manager.shared_data["score"] = self.score_system.score
        self.state_manager.change_state(STATE_GAMEOVER)

    def draw(self) -> None:
        """Dibuja el nivel de pelea."""
        if self.bg_image:
            self.screen.blit(self.bg_image, (0, 0))
        else:
            bg_color = self._get_bg_color()
            self.screen.fill(bg_color)

            # Suelo
            ground_rect = pygame.Rect(0, GROUND_Y, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_Y)
            pygame.draw.rect(self.screen, BROWN, ground_rect)
            pygame.draw.line(self.screen, DARK_GREEN, (0, GROUND_Y), (SCREEN_WIDTH, GROUND_Y), 3)

            # Decoración de fondo
            self._draw_background_decor()

        # Plataformas elevadas (solo sin imagen de fondo)
        if not self.bg_image:
            self._draw_platforms()

        if self.show_level_intro:
            self._draw_level_intro()
            return

        # Entidades
        self.player.draw(self.screen)
        self.enemy.draw(self.screen)

        # HUD
        self.hud.draw(self.screen, self.player, self.enemy,
                      self.score_system.score, self.current_level, self.player_name)

        # Nombre del nivel (sutil, debajo del HUD)
        self.text.render_centered(self.screen, self.level_name, 58, 13, (160, 160, 160))

        if self.paused:
            self._draw_pause_menu()

    def _get_bg_color(self) -> tuple:
        """Color de fondo desde el JSON del nivel."""
        bg = self.level_data.get("bg_color", list(SKY_BLUE))
        return tuple(bg)

    def _draw_background_decor(self) -> None:
        """Dibuja decoración de fondo según el nivel."""
        if self.current_level == 1:
            for x in [100, 350, 650]:
                pygame.draw.rect(self.screen, (100, 70, 40), (x, GROUND_Y - 80, 20, 80))
                pygame.draw.circle(self.screen, DARK_GREEN, (x + 10, GROUND_Y - 100), 40)
        elif self.current_level == 2:
            for x in [50, 250, 500, 700]:
                h = 150 + (x % 100)
                pygame.draw.rect(self.screen, (80, 80, 100), (x, GROUND_Y - h, 60, h))
                for wy in range(GROUND_Y - h + 15, GROUND_Y - 10, 25):
                    pygame.draw.rect(self.screen, (200, 200, 100), (x + 10, wy, 15, 15))
                    pygame.draw.rect(self.screen, (200, 200, 100), (x + 35, wy, 15, 15))
        elif self.current_level == 3:
            for x in [120, 400, 680]:
                pygame.draw.rect(self.screen, (90, 75, 55), (x, GROUND_Y - 100, 25, 100))
                pygame.draw.circle(self.screen, (60, 130, 50), (x + 12, GROUND_Y - 120), 35)
        elif self.current_level == 4:
            for x in [50, 200, 400, 600, 750]:
                h = 180 + (x % 120)
                pygame.draw.rect(self.screen, (70, 70, 90), (x, GROUND_Y - h, 70, h))
                for wy in range(GROUND_Y - h + 20, GROUND_Y - 10, 30):
                    pygame.draw.rect(self.screen, (220, 200, 100), (x + 10, wy, 18, 18))
                    pygame.draw.rect(self.screen, (220, 200, 100), (x + 42, wy, 18, 18))

    def _setup_pause_buttons(self) -> None:
        """Crea los botones del menú de pausa."""
        cx = SCREEN_WIDTH // 2 - 110
        self.pause_buttons = {
            "reanudar":      Button(cx, 210, 220, 45, "Reanudar",
                                   bg_color=(40, 100, 40), hover_color=(60, 140, 60)),
            "instrucciones": Button(cx, 270, 220, 45, "Instrucciones",
                                   bg_color=(40, 60, 100), hover_color=(60, 90, 140)),
            "menu":          Button(cx, 330, 220, 45, "Volver al Menu",
                                   bg_color=(80, 60, 30), hover_color=(120, 90, 45)),
            "salir":         Button(cx, 390, 220, 45, "Salir",
                                   bg_color=(100, 30, 30), hover_color=(140, 50, 50)),
        }

    def _draw_pause_menu(self) -> None:
        """Dibuja el overlay del menú de pausa."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))
        self.text.render_centered(self.screen, "PAUSA", 130, 48, WHITE)
        if self.show_instructions:
            self._draw_pause_instructions()
            return
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.pause_buttons.values():
            btn.draw(self.screen, mouse_pos)

    def _draw_pause_instructions(self) -> None:
        """Dibuja los controles del juego."""
        self.text.render_centered(self.screen, "CONTROLES", 185, 26, TERERE_GREEN)
        lines = [
            ("Mover",            "Flechas  /  A  D"),
            ("Saltar",           "Espacio  /  W"),
            ("Ataque normal",    "Enter"),
            ("Ataque especial",  "J"),
            ("Pausar",           "Escape"),
            ("Saltar nivel",     "P"),
        ]
        y = 230
        for action, keys in lines:
            self.text.render(self.screen, action, 200, y, 20, WHITE)
            self.text.render(self.screen, keys, 440, y, 20, TERERE_GREEN)
            y += 35
        self.text.render_centered(self.screen, "Escape para volver", 450, 16, (150, 150, 150))

    def _draw_platforms(self) -> None:
        """Dibuja las plataformas elevadas del nivel con colores temáticos."""
        platform_colors = {
            1: (100, 70, 40),   # Madera (banco de plaza)
            2: (70, 70, 90),    # Metal (techo de auto / parada de bus)
            3: (90, 80, 60),    # Madera rustica (barrio)
            4: (80, 80, 100),   # Concreto (ciudad)
        }
        edge_colors = {
            1: (60, 40, 20),
            2: (50, 50, 70),
            3: (60, 50, 35),
            4: (50, 50, 70),
        }
        color = platform_colors.get(self.current_level, BROWN)
        edge = edge_colors.get(self.current_level, DARK_GREEN)
        for plat in self.platforms:
            if plat["y"] < GROUND_Y:
                pygame.draw.rect(self.screen, color,
                                 (plat["x"], plat["y"], plat["width"], plat["height"]))
                pygame.draw.rect(self.screen, edge,
                                 (plat["x"], plat["y"], plat["width"], plat["height"]), 2)

    def _draw_level_intro(self) -> None:
        """Dibuja la intro del nivel."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        self.text.render_centered(self.screen, f"NIVEL {self.current_level}", 200, 48, WHITE)
        self.text.render_centered(self.screen, self.level_name, 270, 28, TERERE_GREEN)
        self.text.render_centered(self.screen, "Preparate para la pelea!", 340, 20, (200, 200, 200))
        self.text.render_centered(self.screen, "Presiona ENTER para comenzar", 420, 18, (150, 150, 150))
