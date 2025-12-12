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

    def __init__(self, font_path: str | None = None, font_size: int = 24):
        """
        :param font_path: Optional path to a TTF font file to load.
        :type font_path: str | None

        :param font_size: Font size in points to use when loading the font.
        :type font_size: int
        """
        self._engine = native.Engine()
        self._font_path = font_path
        self._font_size = font_size

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

        # Load font if provided
        if self._font_path is not None:
            self._engine.load_font(self._font_path, self._font_size)

    def set_clear_color(self, r: int, g: int, b: int):
        """
        Set the background/clear color used by begin_frame.

        :param r: Red component (0-255).
        :type r: int

        :param g: Green component (0-255).
        :type g: int

        :param b: Blue component (0-255).
        :type b: int
        """
        self._engine.set_clear_color(int(r), int(g), int(b))

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

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def draw_rect(
        self,
        x: int,
        y: int,
        w: int,
        h: int,
        color: tuple[int, ...] = (255, 255, 255),
    ):
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

        :param color: Color of the rectangle as (r, g, b) or (r, g, b, a).
        :type color: tuple[int, ...]
        """
        if len(color) == 3:
            r, g, b = color
            self._engine.draw_rect(x, y, w, h, r, g, b)
        elif len(color) == 4:
            r, g, b, a = color
            self._engine.draw_rect_rgba(x, y, w, h, r, g, b, a)
        else:
            raise ValueError(
                f"Color must be (r,g,b) or (r,g,b,a), got {color!r}"
            )

    # pylint: enable=too-many-arguments,too-many-positional-arguments

    def draw_text(
        self,
        x: int,
        y: int,
        text: str,
        color: tuple[int, int, int] = (255, 255, 255),
    ):
        """
        Draw text at the given position using the loaded font.
        If no font is loaded, this is a no-op.

        :param x: X coordinate for the text position.
        :type x: int

        :param y: Y coordinate for the text position.
        :type y: int

        :param text: The text string to draw.
        :type text: str

        :param color: Color of the text as (r, g, b).
        :type color: tuple[int, int, int]
        """
        # We rely on C++ side to no-op if font is missing
        r, g, b = color
        self._engine.draw_text(text, x, y, int(r), int(g), int(b))

    def capture_frame(self, path: str | None = None) -> bool:
        """
        Capture the current frame.

        :param path: Optional file path to save the captured frame (e.g., PNG).
        :type path: str | None

        :return: True if the frame was successfully captured (and saved if path provided),
            False otherwise.
        :rtype: bool
        """
        return self._engine.capture_frame(path)
