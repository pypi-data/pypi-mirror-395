"""
Entity base classes for mini_arcade_core.
"""

from __future__ import annotations

from typing import Any


class Entity:
    """Entity base class for game objects."""

    def update(self, dt: float):
        """
        Advance the entity state by ``dt`` seconds.

        :param dt: Time delta in seconds.
        :type dt: float
        """

    def draw(self, surface: Any):
        """
        Render the entity to the given surface.

        :param surface: The surface to draw on.
        :type surface: Any
        """


class SpriteEntity(Entity):
    """Entity with position and size."""

    def __init__(self, x: float, y: float, width: int, height: int):
        """
        :param x: X position.
        :type x: float

        :param y: Y position.
        :type y: float

        :param width: Width of the entity.
        :type width: int

        :param height: Height of the entity.
        :type height: int
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        # TODO: velocity, color, etc.
