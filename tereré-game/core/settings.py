"""Constantes y configuración global del juego Terere Core."""

import os
import pygame

FONT_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "fonts", "pressstart2p.ttf")
FONT_UI_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "fonts", "pressstart2p.ttf")
FONT_UI_BOLD_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "fonts", "pressstart2p.ttf")

# Pantalla
SCREEN_WIDTH: int = 1280
SCREEN_HEIGHT: int = 720
FPS: int = 60
TITLE: str = "Terere Core"

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 50, 50)
GREEN = (50, 200, 50)
BLUE = (50, 100, 220)
YELLOW = (255, 220, 50)
DARK_GREEN = (20, 80, 20)
ORANGE = (240, 160, 40)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (60, 60, 60)
BROWN = (139, 90, 43)
SKY_BLUE = (135, 200, 235)
TERERE_GREEN = (100, 180, 80)

# Física
GRAVITY: float = 0.8
JUMP_FORCE: float = -15.0
PLAYER_SPEED: float = 5.0
GROUND_Y: int = 600

# Estados del juego
STATE_MENU: str = "menu"
STATE_NAME: str = "name"
STATE_STORY: str = "story"
STATE_SELECT: str = "select"
STATE_GAME: str = "game"
STATE_MINIGAME: str = "minigame"
STATE_GAMEOVER: str = "gameover"
STATE_VICTORY: str = "victory"

# Combate
ATTACK_COOLDOWN: int = 40
SPECIAL_COOLDOWN: int = 60
COMBO_WINDOW: int = 30
KNOCKBACK_FORCE: float = 8.0

# Niveles
MAX_LEVELS: int = 4
