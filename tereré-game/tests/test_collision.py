"""Tests para el sistema de colisiones."""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pygame
pygame.init()

from systems.collision import CollisionSystem


class TestCollisionSystem(unittest.TestCase):
    """Tests básicos de detección de colisiones."""

    def setUp(self) -> None:
        self.collision = CollisionSystem()

    def test_colliding_rects(self) -> None:
        """Dos rectángulos superpuestos deben colisionar."""
        rect1 = pygame.Rect(0, 0, 50, 50)
        rect2 = pygame.Rect(25, 25, 50, 50)
        self.assertTrue(self.collision.check_collision(rect1, rect2))

    def test_non_colliding_rects(self) -> None:
        """Dos rectángulos separados no deben colisionar."""
        rect1 = pygame.Rect(0, 0, 50, 50)
        rect2 = pygame.Rect(100, 100, 50, 50)
        self.assertFalse(self.collision.check_collision(rect1, rect2))

    def test_touching_rects(self) -> None:
        """Dos rectángulos que se tocan en el borde deben colisionar."""
        rect1 = pygame.Rect(0, 0, 50, 50)
        rect2 = pygame.Rect(49, 0, 50, 50)
        self.assertTrue(self.collision.check_collision(rect1, rect2))

    def test_adjacent_rects_no_collision(self) -> None:
        """Dos rectángulos adyacentes (sin superposición) no colisionan."""
        rect1 = pygame.Rect(0, 0, 50, 50)
        rect2 = pygame.Rect(50, 0, 50, 50)
        self.assertFalse(self.collision.check_collision(rect1, rect2))


if __name__ == "__main__":
    unittest.main()
