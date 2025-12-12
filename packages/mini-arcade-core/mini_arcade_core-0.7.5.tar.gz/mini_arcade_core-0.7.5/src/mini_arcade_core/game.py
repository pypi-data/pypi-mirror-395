"""
Game core module defining the Game class and configuration.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from time import perf_counter, sleep
from typing import TYPE_CHECKING

from PIL import Image  # type: ignore[import]

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

    @staticmethod
    def _convert_bmp_to_image(bmp_path: str, out_path: str) -> bool:
        """
        Convert a BMP file to another image format using Pillow.

        :param bmp_path: Path to the input BMP file.
        :type bmp_path: str

        :param out_path: Path to the output image file.
        :type out_path: str

        :return: True if conversion was successful, False otherwise.
        :rtype: bool
        """
        try:
            img = Image.open(bmp_path)
            img.save(out_path)  # Pillow chooses format from extension
            return True
        # Justification: Pillow can raise various exceptions on failure
        # pylint: disable=broad-exception-caught
        except Exception:
            return False
        # pylint: enable=broad-exception-caught

    def screenshot(
        self, label: str | None = None, directory: str = "screenshots"
    ) -> str | None:
        """
        Ask backend to save a screenshot. Returns the file path or None.

        :param label: Optional label to include in the filename.
        :type label: str | None

        :param directory: Directory to save screenshots in.
        :type directory: str

        :return: The file path of the saved screenshot, or None on failure.
        :rtype: str | None
        """
        os.makedirs(directory, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        label = label or "shot"
        filename = f"{stamp}_{label}"
        bmp_path = os.path.join(directory, f"{filename}.bmp")

        if self.backend.capture_frame(bmp_path):
            out_path = Path(directory) / f"{filename}.png"
            self._convert_bmp_to_image(bmp_path, str(out_path))
            return str(out_path)
        return None
