"""Estado principal de pelea 2D."""

import pygame
from core.settings import (SCREEN_WIDTH, SCREEN_HEIGHT, STATE_MINIGAME,
                           STATE_GAMEOVER, STATE_VICTORY, MAX_LEVELS,
                           GROUND_Y, WHITE, BLACK, SKY_BLUE, BROWN,
                           TERERE_GREEN, DARK_GREEN)
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
        self.level_data: dict = {}
        self.level_name: str = ""
        self.minigame_id: str = ""

        # Transición
        self.transition_timer: int = 0
        self.show_level_intro: bool = True
        self.intro_timer: int = 180  # 3 segundos

        self.player: Player = Player(100, GROUND_Y - 70, input_handler)
        self.enemy: Enemy = Enemy(600, GROUND_Y - 70)

        self.load_level(self.current_level)

    def load_level(self, level_number: int) -> None:
        """Carga la configuración del nivel desde JSON."""
        self.level_data = self.level_loader.load_level(level_number)
        self.level_name = self.level_data.get("name", f"Nivel {level_number}")
        self.minigame_id = self.level_data.get("minigame", "terere_rush")

        enemy_config = self.level_data.get("enemy", {})
        enemy_speed = enemy_config.get("speed", 3)
        enemy_health = enemy_config.get("health", 100)
        enemy_damage = enemy_config.get("damage", 10)

        self.enemy = Enemy(600, GROUND_Y - 70, speed=enemy_speed,
                           health=enemy_health, damage=enemy_damage)

        # Restaurar vida del jugador
        player_health = self.state_manager.shared_data.get("player_health", 100)
        self.player = Player(100, GROUND_Y - 70, self.input_handler)
        self.player.health = player_health

        self.show_level_intro = True
        self.intro_timer = 180
