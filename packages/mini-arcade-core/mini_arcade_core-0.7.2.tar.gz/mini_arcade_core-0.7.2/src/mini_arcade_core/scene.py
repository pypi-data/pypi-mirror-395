"""
Base class for game scenes (states/screens).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable, List

from mini_arcade_core.backend import Backend

from .game import Game

OverlayFunc = Callable[[Backend], None]


class Scene(ABC):
    """Base class for game scenes (states/screens)."""

    def __init__(self, game: Game):
        """
        :param game: Reference to the main Game object.
        :type game: Game
        """
        self.game = game
        # overlays drawn on top of the scene
        self._overlays: List[OverlayFunc] = []

    def add_overlay(self, overlay: OverlayFunc) -> None:
        """Register an overlay (drawn every frame, after entities)."""
        self._overlays.append(overlay)

    def remove_overlay(self, overlay: OverlayFunc) -> None:
        if overlay in self._overlays:
            self._overlays.remove(overlay)

    def clear_overlays(self) -> None:
        self._overlays.clear()

    def draw_overlays(self, surface: Backend) -> None:
        """Call all overlays. Scenes should call this at the end of draw()."""
        for overlay in self._overlays:
            overlay(surface)

    @abstractmethod
    def on_enter(self):
        """Called when the scene becomes active."""

    @abstractmethod
    def on_exit(self):
        """Called when the scene is replaced."""

    @abstractmethod
    def handle_event(self, event: object):
        """Handle input / events (e.g. pygame.Event)."""

    @abstractmethod
    def update(self, dt: float):
        """Update game logic. ``dt`` is the delta time in seconds."""

    @abstractmethod
    def draw(self, surface: object):
        """Render to the main surface."""

    def draw(self, surface: object):
        """Render to the main surface."""

    def draw(self, surface: object):
        """Render to the main surface."""
