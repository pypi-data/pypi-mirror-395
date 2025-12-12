import importlib
import os
import sys
import types
from dataclasses import dataclass

import pytest


def setup_fake_core_and_native(monkeypatch):
    """
    Inject fake mini_arcade_core and mini_arcade_native_backend._native modules
    into sys.modules so we can import the package without the real C++ extension.
    """
    # --- Fake mini_arcade_core -------------------------------------------------
    fake_core = types.ModuleType("mini_arcade_core")

    class FakeBackend:
        """Minimal base class just to satisfy inheritance."""
        pass

    class FakeCoreEventType:
        UNKNOWN = "core_unknown"
        QUIT = "core_quit"
        KEYDOWN = "core_keydown"
        KEYUP = "core_keyup"

    @dataclass
    class FakeEvent:
        type: object
        key: object = None

    fake_core.Backend = FakeBackend
    fake_core.Event = FakeEvent
    fake_core.EventType = FakeCoreEventType

    sys.modules["mini_arcade_core"] = fake_core

    # --- Fake native extension: mini_arcade_native_backend._native -------------
    fake_native = types.ModuleType("mini_arcade_native_backend._native")

    class FakeNativeEventType:
        Unknown = "native_unknown"
        Quit = "native_quit"
        KeyDown = "native_keydown"
        KeyUp = "native_keyup"

    class FakeEngine:
        def __init__(self):
            self.init_args = None
            self.frames = []
            self.rects = []
            self._events_to_return = []

        def init(self, width, height, title):
            self.init_args = (width, height, title)

        def poll_events(self):
            return list(self._events_to_return)

        def begin_frame(self):
            self.frames.append("begin")

        def end_frame(self):
            self.frames.append("end")

        def draw_rect(self, x, y, w, h):
            self.rects.append((x, y, w, h))

    fake_native.EventType = FakeNativeEventType
    fake_native.Engine = FakeEngine

    # Register the fake native module under the expected name
    sys.modules["mini_arcade_native_backend._native"] = fake_native

    return fake_core, fake_native


def import_backend_package(monkeypatch, *, platform="linux", vcpkg_root=None, sdl_dir_exists=False):
    """
    Helper to import mini_arcade_native_backend with controlled platform/env.
    Returns (package_module, fake_core_module, fake_native_module, added_paths).
    """
    fake_core, fake_native = setup_fake_core_and_native(monkeypatch)

    # Control sys.platform
    monkeypatch.setattr(sys, "platform", platform)

    # Control VCPKG_ROOT
    if vcpkg_root is None:
        monkeypatch.delenv("VCPKG_ROOT", raising=False)
    else:
        monkeypatch.setenv("VCPKG_ROOT", vcpkg_root)

    # Track calls to os.add_dll_directory (may not exist on non-Windows)
    added_paths = []

    def fake_add_dll_directory(path):
        added_paths.append(path)

    monkeypatch.setattr(os, "add_dll_directory", fake_add_dll_directory, raising=False)

    # Control os.path.isdir for the SDL bin path check
    real_isdir = os.path.isdir

    def fake_isdir(path):
        if sdl_dir_exists:
            return True
        return real_isdir(path)

    monkeypatch.setattr(os.path, "isdir", fake_isdir)

    # Force a fresh import of the package so the top-level code re-runs
    sys.modules.pop("mini_arcade_native_backend", None)
    pkg = importlib.import_module("mini_arcade_native_backend")

    return pkg, fake_core, fake_native, added_paths


# --------------------------------------------------------------------------- #
#  DLL path / Windows bootstrap tests
# --------------------------------------------------------------------------- #


def test_non_windows_does_not_add_dll_directory(monkeypatch):
    pkg, fake_core, fake_native, added_paths = import_backend_package(
        monkeypatch,
        platform="linux",
        vcpkg_root=None,
        sdl_dir_exists=False,
    )

    assert added_paths == []


def test_windows_without_vcpkg_root_does_not_add_dll_directory(monkeypatch):
    pkg, fake_core, fake_native, added_paths = import_backend_package(
        monkeypatch,
        platform="win32",
        vcpkg_root=None,
        sdl_dir_exists=True,
    )

    assert added_paths == []


def test_windows_with_vcpkg_root_and_existing_sdl_dir_adds_dll_directory(monkeypatch):
    vcpkg_root = r"C:\vcpkg"

    pkg, fake_core, fake_native, added_paths = import_backend_package(
        monkeypatch,
        platform="win32",
        vcpkg_root=vcpkg_root,
        sdl_dir_exists=True,
    )

    expected_sdl_bin = os.path.join(vcpkg_root, "installed", "x64-windows", "bin")
    assert expected_sdl_bin in added_paths


# --------------------------------------------------------------------------- #
#  NativeBackend behaviour tests
# --------------------------------------------------------------------------- #


@pytest.fixture
def backend_module(monkeypatch):
    """
    Import the package on a non-Windows platform and return:
    (pkg, fake_core, fake_native)
    """
    pkg, fake_core, fake_native, _ = import_backend_package(
        monkeypatch,
        platform="linux",
        vcpkg_root=None,
        sdl_dir_exists=False,
    )
    return pkg, fake_core, fake_native


def test_exports_nativebackend_and_native(backend_module):
    pkg, fake_core, fake_native = backend_module
    assert "NativeBackend" in pkg.__all__
    assert "native" in pkg.__all__


def test_nativebackend_init_calls_engine_init(backend_module):
    pkg, fake_core, fake_native = backend_module

    backend = pkg.NativeBackend()
    backend.init(800, 600, "Test Window")

    engine = backend._engine
    assert engine.init_args == (800, 600, "Test Window")


def test_nativebackend_begin_end_frame_delegate_to_engine(backend_module):
    pkg, fake_core, fake_native = backend_module

    backend = pkg.NativeBackend()
    backend.begin_frame()
    backend.end_frame()

    assert backend._engine.frames == ["begin", "end"]


def test_nativebackend_draw_rect_delegates_to_engine(backend_module):
    pkg, fake_core, fake_native = backend_module

    backend = pkg.NativeBackend()
    backend.draw_rect(10, 20, 30, 40)

    assert backend._engine.rects == [(10, 20, 30, 40)]


def test_poll_events_maps_native_events_to_core_events_and_keys(backend_module):
    pkg, fake_core, fake_native = backend_module

    backend = pkg.NativeBackend()

    # Create fake native events
    @dataclass
    class FakeNativeEvent:
        type: object
        key: int = 0

    engine = backend._engine
    engine._events_to_return = [
        FakeNativeEvent(fake_native.EventType.Quit, 0),             # -> QUIT, key=None
        FakeNativeEvent(fake_native.EventType.KeyDown, 32),         # -> KEYDOWN, key=32
        FakeNativeEvent("something_unknown", 10),                   # -> UNKNOWN, key=10
    ]

    events = backend.poll_events()

    assert len(events) == 3

    # 1) Quit event, key==0 -> key should become None
    assert events[0].type == fake_core.EventType.QUIT
    assert events[0].key is None

    # 2) KeyDown, key!=0 passes through
    assert events[1].type == fake_core.EventType.KEYDOWN
    assert events[1].key == 32

    # 3) Unknown type -> UNKNOWN
    assert events[2].type == fake_core.EventType.UNKNOWN
    assert events[2].key == 10
