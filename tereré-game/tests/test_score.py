"""Tests para el sistema de puntaje."""

import unittest
import sys
import os
import json
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from systems.score import ScoreSystem


class TestScoreSystem(unittest.TestCase):
    """Tests básicos del sistema de puntaje."""

    def setUp(self) -> None:
        self.score = ScoreSystem()

    def test_add_points(self) -> None:
        """Al agregar puntos el score aumenta correctamente."""
        self.score.add_points(100)
        self.assertEqual(self.score.get_score(), 100)
        self.score.add_points(50)
        self.assertEqual(self.score.get_score(), 150)

    def test_reset(self) -> None:
        """Reset vuelve el score a 0."""
        self.score.add_points(500)
        self.score.reset()
        self.assertEqual(self.score.get_score(), 0)

    def test_save_and_load_highscore(self) -> None:
        """Se guarda y carga correctamente un highscore."""
        # Usar archivo temporal
        temp_file = os.path.join(tempfile.gettempdir(), "test_highscores.json")
        original_file = ScoreSystem.HIGHSCORE_FILE
        ScoreSystem.HIGHSCORE_FILE = temp_file

        try:
            score_sys = ScoreSystem()
            score_sys.save_highscore("TestPlayer", 1000)
            loaded = score_sys.load_highscores()
            self.assertTrue(len(loaded) > 0)
            self.assertEqual(loaded[0]["name"], "TestPlayer")
            self.assertEqual(loaded[0]["score"], 1000)
        finally:
            ScoreSystem.HIGHSCORE_FILE = original_file
            if os.path.exists(temp_file):
                os.remove(temp_file)

    def test_initial_score_is_zero(self) -> None:
        """El puntaje inicial debe ser 0."""
        self.assertEqual(self.score.get_score(), 0)


if __name__ == "__main__":
    unittest.main()
