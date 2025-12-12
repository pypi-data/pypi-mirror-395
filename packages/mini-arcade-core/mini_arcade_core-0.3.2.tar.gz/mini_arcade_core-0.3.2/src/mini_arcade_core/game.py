"""
Game core module defining the Game class and configuration.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # avoid runtime circular import
    from .scene import Scene


@dataclass
class GameConfig:
    """
    Configuration options for the Game.

    :ivar width: Width of the game window in pixels.
    :ivar height: Height of the game window in pixels.
    :ivar title: Title of the game window.
    :ivar fps: Target frames per second.
    :ivar background_color: RGB background color.
    """

    width: int = 800
    height: int = 600
    title: str = "Mini Arcade Game"
    fps: int = 60
    background_color: tuple[int, int, int] = (0, 0, 0)


class Game:
    """Core game object responsible for managing the main loop and active scene."""

    def __init__(self, config: GameConfig):
        """
        :param config: Game configuration options.
        """
        self.config = config
        self._current_scene: Scene | None = None
        self._running: bool = False

    def change_scene(self, scene: Scene):
        """
        Swap the active scene. Concrete implementations should call
        ``on_exit``/``on_enter`` appropriately.

        :param scene: The new scene to activate.
        """
        raise NotImplementedError(
            "Game.change_scene must be implemented by a concrete backend."
        )

    def run(self, initial_scene: Scene):
        """
        Run the main loop starting with the given scene.

        This is intentionally left abstract so you can plug pygame, pyglet,
        or another backend.

        :param initial_scene: The scene to start the game with.
        """
        raise NotImplementedError(
            "Game.run must be implemented by a concrete backend."
        )
