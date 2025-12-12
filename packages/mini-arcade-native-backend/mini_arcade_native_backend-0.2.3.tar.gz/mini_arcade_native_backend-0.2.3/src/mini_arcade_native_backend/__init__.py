"""
mini-arcade native backend package.
"""

from __future__ import annotations

import os
import sys

# --- 1) Make sure Windows can find SDL2.dll when using vcpkg ------------------

if sys.platform == "win32":
    vcpkg_root = os.environ.get("VCPKG_ROOT")
    if vcpkg_root:
        # Typical vcpkg layout: <VCPKG_ROOT>/installed/x64-windows/bin/SDL2.dll
        sdl_bin = os.path.join(vcpkg_root, "installed", "x64-windows", "bin")
        if os.path.isdir(sdl_bin):
            # Python 3.8+ – add DLL search path before importing the extension
            os.add_dll_directory(sdl_bin)

# --- 2) Now import native extension and core types ----------------------------

# Justification: Need to import core after setting DLL path on Windows
# pylint: disable=wrong-import-position
from mini_arcade_core import Backend, Event, EventType

# Justification: Importing the native extension module
# pylint: disable=import-self,no-name-in-module
from . import _native as native

# --- 2) Now import core + define NativeBackend as before ---


__all__ = ["NativeBackend", "native"]


_NATIVE_TO_CORE = {
    native.EventType.Unknown: EventType.UNKNOWN,
    native.EventType.Quit: EventType.QUIT,
    native.EventType.KeyDown: EventType.KEYDOWN,
    native.EventType.KeyUp: EventType.KEYUP,
}


class NativeBackend(Backend):
    """Adapter that makes the C++ Engine usable as a mini-arcade backend."""

    def __init__(self):
        self._engine = native.Engine()

    def init(self, width: int, height: int, title: str):
        """
        Initialize the backend with a window of given width, height, and title.

        :param width: Width of the window in pixels.
        :type width: int

        :param height: Height of the window in pixels.
        :type height: int

        :param title: Title of the window.
        :type title: str
        """
        self._engine.init(width, height, title)

    def poll_events(self) -> list[Event]:
        """
        Poll for events from the backend and return them as a list of Event objects.

        :return: List of Event objects representing the polled events.
        :rtype: list[Event]
        """
        events: list[Event] = []
        for ev in self._engine.poll_events():
            core_type = _NATIVE_TO_CORE.get(ev.type, EventType.UNKNOWN)
            key = ev.key if getattr(ev, "key", 0) != 0 else None
            events.append(Event(type=core_type, key=key))
        return events

    def begin_frame(self):
        """Begin a new frame for rendering."""
        self._engine.begin_frame()

    def end_frame(self):
        """End the current frame for rendering."""
        self._engine.end_frame()

    def draw_rect(self, x: int, y: int, w: int, h: int):
        """
        Draw a rectangle at the specified position with given width and height.

        :param x: X coordinate of the rectangle's top-left corner.
        :type x: int

        :param y: Y coordinate of the rectangle's top-left corner.
        :type y: int

        :param w: Width of the rectangle.
        :type w: int

        :param h: Height of the rectangle.
        :type h: int
        """
        self._engine.draw_rect(x, y, w, h)
