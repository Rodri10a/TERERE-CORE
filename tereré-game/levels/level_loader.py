"""Cargador de niveles desde archivos JSON."""

import json
import os


DEFAULT_LEVELS = {
    1: {
        "id": 1,
        "name": "Plaza de Capiata",
        "background": "plaza",
        "enemy": {"speed": 3, "health": 100, "damage": 10},
        "minigame": "terere_rush",
        "platforms": [{"x": 0, "y": 550, "width": 800, "height": 50}],
    },
    2: {
        "id": 2,
        "name": "Calle de Asuncion",
        "background": "calle",
        "enemy": {"speed": 4, "health": 150, "damage": 15},
        "minigame": "esquiva_cheto",
        "platforms": [{"x": 0, "y": 550, "width": 800, "height": 50}],
    },
    3: {
        "id": 3,
        "name": "Boss Final - Mansion del Cheto",
        "background": "mansion",
        "enemy": {"speed": 5, "health": 200, "damage": 20},
        "minigame": "yuyos_quiz",
        "platforms": [{"x": 0, "y": 550, "width": 800, "height": 50}],
    },
}


class LevelLoader:
    """Carga configuración de niveles desde JSON con fallback a datos por defecto."""

    def __init__(self, levels_dir: str = "levels") -> None:
        self.levels_dir = levels_dir

    def load_level(self, level_number: int) -> dict:
        """Carga el nivel desde JSON. Si no existe, usa valores por defecto."""
        filepath = os.path.join(self.levels_dir, f"level{level_number}.json")
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError, Exception):
            return DEFAULT_LEVELS.get(level_number, DEFAULT_LEVELS[1])
