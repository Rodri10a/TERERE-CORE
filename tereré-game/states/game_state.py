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
