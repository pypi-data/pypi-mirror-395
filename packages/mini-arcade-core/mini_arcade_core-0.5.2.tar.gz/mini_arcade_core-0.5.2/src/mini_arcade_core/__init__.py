"""
Entry point for the mini_arcade_core package.
Provides access to core classes and a convenience function to run a game.
"""

from __future__ import annotations

import logging
from importlib.metadata import PackageNotFoundError, version

from .backend import Backend, Event, EventType
from .entity import Entity, SpriteEntity
from .game import Game, GameConfig
from .scene import Scene

logger = logging.getLogger(__name__)


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

PACKAGE_NAME = "mini-arcade-core"  # or whatever is in your pyproject.toml


def get_version() -> str:
    """
    Return the installed package version.

    This is a thin helper around importlib.metadata.version so games can do:

        from mini_arcade_core import get_version
        print(get_version())

    :return: The version string of the installed package.
    :rtype: str

    :raises PackageNotFoundError: If the package is not installed.
    """
    try:
        return version(PACKAGE_NAME)
    except PackageNotFoundError:  # if running from source / editable
        logger.warning(
            f"Package '{PACKAGE_NAME}' not found. Returning default version '0.0.0'."
        )
        return "0.0.0"


try:
    __version__ = get_version()
# Justification: We want to ensure that any exception during version retrieval
# results in a default version being set, rather than crashing the import.
# pylint: disable=broad-exception-caught
except Exception:
    __version__ = "0.0.0"
# pylint: enable=broad-exception-caught
