import ctypes
from typing import Optional, Callable
from .lib import get_sdl_lib

lib = get_sdl_lib()

VOUT_FRAME_CALLBACK = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_void_p)

lib.RAPID_SDL_Vout_Silence_Create.argtypes = []
lib.RAPID_SDL_Vout_Silence_Create.restype = ctypes.c_void_p

lib.RAPID_SDL_Aout_Silence_Create.argtypes = []
lib.RAPID_SDL_Aout_Silence_Create.restype = ctypes.c_void_p

lib.RAPID_SDL_AoutDarwin_CreateForAudioQueue.argtypes = []
lib.RAPID_SDL_AoutDarwin_CreateForAudioQueue.restype = ctypes.c_void_p

lib.RAPID_SDL_Vout_SimpleCallback_Create.argtypes = [VOUT_FRAME_CALLBACK, ctypes.c_void_p]
lib.RAPID_SDL_Vout_SimpleCallback_Create.restype = ctypes.c_void_p

lib.RAPID_SDL_Aout_Silence_Create_WithInterval.argtypes = [ctypes.c_int]
lib.RAPID_SDL_Aout_Silence_Create_WithInterval.restype = ctypes.c_void_p

_vout_callback_storage = {}

def create_silence_vout():
    return lib.RAPID_SDL_Vout_Silence_Create()

def create_silence_aout():
    return lib.RAPID_SDL_Aout_Silence_Create()

def create_audioqueue_aout():
    return lib.RAPID_SDL_AoutDarwin_CreateForAudioQueue()

def create_vout_with_callback(callback: Callable[[ctypes.c_void_p], None]):
    if callback is None:
        return None

    def wrapper(overlay_ptr, user_data):
        try:
            if callback:
                callback(overlay_ptr)
        except:
            pass

    c_callback = VOUT_FRAME_CALLBACK(wrapper)
    vout_ptr = lib.RAPID_SDL_Vout_SimpleCallback_Create(c_callback, None)
    if vout_ptr:
        _vout_callback_storage[vout_ptr] = c_callback
    return vout_ptr

def create_silence_aout_with_interval(interval_ms: int):
    return lib.RAPID_SDL_Aout_Silence_Create_WithInterval(interval_ms)