"""
Entry point for the mini_arcade_core package.
Provides access to core classes and a convenience function to run a game.
"""

from __future__ import annotations

from .backend import Backend, Event, EventType
from .entity import Entity, SpriteEntity
from .game import Game, GameConfig
from .scene import Scene


def run_game(initial_scene_cls: type[Scene], config: GameConfig | None = None):
    """
    Convenience helper to bootstrap and run a game with a single scene.

    :param initial_scene_cls: The Scene subclass to instantiate as the initial scene.
    :param config: Optional GameConfig to customize game settings.
    """
    game = Game(config or GameConfig())
    scene = initial_scene_cls(game)
    game.run(scene)


__all__ = [
    "Game",
    "GameConfig",
    "Scene",
    "Entity",
    "SpriteEntity",
    "run_game",
    "Backend",
    "Event",
    "EventType",
]
