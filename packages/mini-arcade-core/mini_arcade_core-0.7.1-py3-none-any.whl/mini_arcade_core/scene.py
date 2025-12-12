"""
Base class for game scenes (states/screens).
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from .game import Game


class Scene(ABC):
    """Base class for game scenes (states/screens)."""

    def __init__(self, game: Game):
        """
        :param game: Reference to the main Game object.
        :type game: Game
        """
        self.game = game

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
