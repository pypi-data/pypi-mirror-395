"""
Backend interface for rendering and input.
This is the only part of the code that talks to SDL/pygame directly.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Iterable, Protocol


class EventType(Enum):
    """High-level event types understood by the core."""

    UNKNOWN = auto()
    QUIT = auto()
    KEYDOWN = auto()
    KEYUP = auto()


@dataclass(frozen=True)
class Event:
    """
    Core event type.

    For now we only care about:
    - type: what happened
    - key: integer key code (e.g. ESC = 27), or None if not applicable

    :ivar type (EventType): The type of event.
    :ivar key (int | None): The key code associated with the event, if any.
    """

    type: EventType
    key: int | None = None


class Backend(Protocol):
    """
    Interface that any rendering/input backend must implement.

    mini-arcade-core only talks to this protocol, never to SDL/pygame directly.
    """

    def init(self, width: int, height: int, title: str) -> None:
        """
        Initialize the backend and open a window.

        Should be called once before the main loop.
        """

    def poll_events(self) -> Iterable[Event]:
        """
        Return all pending events since last call.

        Concrete backends will translate their native events into core Event objects.
        """

    def begin_frame(self) -> None:
        """
        Prepare for drawing a new frame (e.g. clear screen).
        """

    def end_frame(self) -> None:
        """
        Present the frame to the user (swap buffers).
        """

    def draw_rect(self, x: int, y: int, w: int, h: int) -> None:
        """
        Draw a filled rectangle in some default color.

        We'll keep this minimal for now; later we can extend with colors/sprites.
        """
