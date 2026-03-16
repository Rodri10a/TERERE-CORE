"""Cargador de niveles desde archivos JSON."""

import json
import os


DEFAULT_LEVELS = {
    1: {
        "id": 1,
        "name": "Plaza de Capiata",
        "background": "plaza",
        "bg_color": [135, 200, 235],
        "score_bonus": 300,
        "enemy_start_x": 600,
        "enemy": {"speed": 3, "health": 100, "damage": 10},
        "minigame": "terere_rush",
        "platforms": [
            {"x": 0, "y": 500, "width": 800, "height": 100},
            {"x": 50, "y": 440, "width": 150, "height": 15},
            {"x": 320, "y": 390, "width": 160, "height": 15},
        ],
    },
    2: {
        "id": 2,
        "name": "Campus de la UNA",
        "background": "calle",
        "bg_color": [100, 120, 150],
        "score_bonus": 500,
        "enemy_start_x": 580,
        "enemy": {"speed": 4, "health": 150, "damage": 15},
        "minigame": "esquiva_cheto",
        "platforms": [
            {"x": 0, "y": 500, "width": 800, "height": 100},
            {"x": 80, "y": 420, "width": 130, "height": 12},
            {"x": 570, "y": 400, "width": 150, "height": 12},
        ],
    },
    3: {
        "id": 3,
        "name": "Barrio de Luque",
        "background": "barrio",
        "bg_color": [120, 140, 100],
        "score_bonus": 600,
        "enemy_start_x": 450,
        "enemy": {"speed": 5, "health": 180, "damage": 18},
        "minigame": "yuyos_quiz",
        "platforms": [
            {"x": 0, "y": 500, "width": 800, "height": 100},
            {"x": 80, "y": 450, "width": 180, "height": 15},
            {"x": 180, "y": 390, "width": 130, "height": 15},
            {"x": 500, "y": 360, "width": 200, "height": 15},
        ],
    },
    4: {
        "id": 4,
        "name": "Terreno final : Asuncion",
        "background": "ciudad",
        "bg_color": [60, 30, 50],
        "score_bonus": 1000,
        "enemy_start_x": 450,
        "enemy": {"speed": 6, "health": 250, "damage": 25},
        "minigame": None,
        "platforms": [
            {"x": 0, "y": 500, "width": 800, "height": 100},
            {"x": 60, "y": 440, "width": 160, "height": 15},
            {"x": 250, "y": 380, "width": 140, "height": 15},
            {"x": 480, "y": 350, "width": 200, "height": 15},
        ],
    },
}


class LevelLoader:
    """Carga configuración de niveles desde JSON con fallback a datos por defecto."""

    def __init__(self, levels_dir: str = "") -> None:
        if levels_dir:
            self.levels_dir = levels_dir
        else:
            self.levels_dir = os.path.dirname(os.path.abspath(__file__))

    def load_level(self, level_number: int) -> dict:
        """Carga el nivel desde JSON. Si no existe, usa valores por defecto."""
        filepath = os.path.join(self.levels_dir, f"level{level_number}.json")
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError, Exception):
            return DEFAULT_LEVELS.get(level_number, DEFAULT_LEVELS[1])
