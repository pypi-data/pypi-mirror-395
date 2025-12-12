"""
Game core module defining the Game class and configuration.
"""

from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter, sleep
from typing import TYPE_CHECKING

from .backend import Backend

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
    :ivar backend: Optional backend class to use for rendering and input.
    """

    width: int = 800
    height: int = 600
    title: str = "Mini Arcade Game"
    fps: int = 60
    background_color: tuple[int, int, int] = (0, 0, 0)
    backend: Backend | None = None


class Game:
    """Core game object responsible for managing the main loop and active scene."""

    def __init__(self, config: GameConfig):
        """
        :param config: Game configuration options.
        :type config: GameConfig
        """
        self.config = config
        self._current_scene: Scene | None = None
        self._running: bool = False
        self.backend: Backend | None = config.backend

        if config.backend is None:
            raise ValueError(
                "GameConfig.backend must be set to a Backend instance"
            )
        self.backend: Backend = config.backend

    def change_scene(self, scene: Scene):
        """
        Swap the active scene. Concrete implementations should call
        ``on_exit``/``on_enter`` appropriately.

        :param scene: The new scene to activate.
        :type scene: Scene
        """
        if self._current_scene is not None:
            self._current_scene.on_exit()
        self._current_scene = scene
        self._current_scene.on_enter()

    def quit(self):
        """Request that the main loop stops."""
        self._running = False

    def run(self, initial_scene: Scene):
        """
        Run the main loop starting with the given scene.

        This is intentionally left abstract so you can plug pygame, pyglet,
        or another backend.

        :param initial_scene: The scene to start the game with.
        :type initial_scene: Scene
        """
        backend = self.backend
        backend.init(self.config.width, self.config.height, self.config.title)

        br, bg, bb = self.config.background_color
        backend.set_clear_color(br, bg, bb)

        self.change_scene(initial_scene)

        self._running = True
        target_dt = 1.0 / self.config.fps if self.config.fps > 0 else 0.0
        last_time = perf_counter()

        while self._running:
            now = perf_counter()
            dt = now - last_time
            last_time = now

            scene = self._current_scene
            if scene is None:
                break

            for ev in backend.poll_events():
                scene.handle_event(ev)

            scene.update(dt)

            backend.begin_frame()
            scene.draw(backend)
            backend.end_frame()

            if target_dt > 0 and dt < target_dt:
                sleep(target_dt - dt)

        if self._current_scene is not None:
            self._current_scene.on_exit()
