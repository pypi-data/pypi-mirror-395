import ctypes
import os
import platform

MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHON_PLATFORM_DIR = os.path.realpath(os.path.join(MODULE_DIR, os.pardir))

_explicit_libraries_dir = None
_core_lib = None
_media_lib = None
_sdl_lib = None
_core_path = None
_media_path = None
_sdl_path = None


def _detect_platform() -> str:
    system = platform.system().lower()
    if system == "darwin":
        return "darwin"
    if system == "windows":
        return "windows"
    if system == "linux":
        return "linux"
    raise RuntimeError(f"Unsupported system: {system}")


def _get_libraries_dir() -> str:
    if _explicit_libraries_dir is None:
        raise RuntimeError("lib_dir not set, call initialize() first")
    return _explicit_libraries_dir


def _load_libraries_if_needed() -> None:
    global _core_lib, _media_lib, _sdl_lib, _core_path, _media_path, _sdl_path
    if _core_lib is not None:
        return

    libraries_dir = _get_libraries_dir()
    key = _detect_platform()

    if key == "darwin":
        core_name = "libRapidCore.dylib"
        sdl_name = "libRapidSDL.dylib"
        media_name = "libRapidMedia.dylib"
    elif key == "windows":
        core_name = "RapidCore.dll"
        sdl_name = "RapidSDL.dll"
        media_name = "RapidMedia.dll"
    else:
        core_name = "libRapidCore.so"
        sdl_name = "libRapidSDL.so"
        media_name = "libRapidMedia.so"

    core_path = os.path.join(libraries_dir, core_name)
    sdl_path = os.path.join(libraries_dir, sdl_name)
    media_path = os.path.join(libraries_dir, media_name)

    if not os.path.exists(core_path):
        raise RuntimeError(f"Core library not found: {core_path}")

    _core = ctypes.CDLL(core_path, mode=ctypes.RTLD_GLOBAL)
    _sdl = None
    _media = None

    if os.path.exists(sdl_path):
        try:
            _sdl = ctypes.CDLL(sdl_path, mode=ctypes.RTLD_GLOBAL)
        except Exception:
            _sdl = None

    if os.path.exists(media_path):
        try:
            _media = ctypes.CDLL(media_path, mode=ctypes.RTLD_GLOBAL)
        except Exception:
            _media = None

    _core_lib = _core
    _sdl_lib = _sdl
    _media_lib = _media
    _core_path = core_path
    _sdl_path = sdl_path
    _media_path = media_path


def get_lib() -> ctypes.CDLL:
    _load_libraries_if_needed()
    if _core_lib is None:
        raise RuntimeError("Core library is not loaded")
    return _core_lib


def get_media_lib() -> ctypes.CDLL:
    _load_libraries_if_needed()
    if _media_lib is None:
        raise RuntimeError("Media library is not loaded")
    return _media_lib


def get_sdl_lib() -> ctypes.CDLL:
    _load_libraries_if_needed()
    if _sdl_lib is None:
        raise RuntimeError("SDL library is not loaded")
    return _sdl_lib


def get_all_loaded_libs() -> dict:
    _load_libraries_if_needed()
    result = {}
    if _core_lib is not None and _core_path is not None:
        result[os.path.basename(_core_path)] = _core_lib
    if _media_lib is not None and _media_path is not None:
        result[os.path.basename(_media_path)] = _media_lib
    if _sdl_lib is not None and _sdl_path is not None:
        result[os.path.basename(_sdl_path)] = _sdl_lib
    return result
