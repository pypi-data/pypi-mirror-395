import ctypes
from typing import Callable
from .lib import get_sdl_lib

lib = get_sdl_lib()

class AudioSpec(ctypes.Structure):
    _fields_ = [
        ("sample_rate", ctypes.c_int),
        ("format", ctypes.c_uint16),
        ("channels", ctypes.c_uint8),
        ("samples", ctypes.c_int),
        ("callback", ctypes.c_void_p),
        ("user_data", ctypes.c_void_p),
    ]

VOUT_FRAME_CALLBACK = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_void_p)
AOUT_FRAME_CALLBACK = ctypes.CFUNCTYPE(
    None,
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.c_int,
    ctypes.POINTER(AudioSpec),
    ctypes.c_void_p
)

lib.RAPID_SDL_Vout_SimpleCallback_Create.argtypes = [VOUT_FRAME_CALLBACK, ctypes.c_void_p]
lib.RAPID_SDL_Vout_SimpleCallback_Create.restype = ctypes.c_void_p

lib.RAPID_SDL_Aout_SimpleCallback_Create.argtypes = [AOUT_FRAME_CALLBACK, ctypes.c_void_p]
lib.RAPID_SDL_Aout_SimpleCallback_Create.restype = ctypes.c_void_p

def _create_vout_with_frame_bridge(handler: Callable):
    from .player import VideoFrameToRender

    class VoutOverlay(ctypes.Structure):
        _fields_ = [
            ("w", ctypes.c_int),
            ("h", ctypes.c_int),
            ("format", ctypes.c_int),
            ("pixels_size", ctypes.c_int),
            ("pixels", ctypes.POINTER(ctypes.c_uint8)),
        ]

    def bridge_callback(overlay_ptr, user_data):
        try:
            overlay = ctypes.cast(overlay_ptr, ctypes.POINTER(VoutOverlay)).contents
            yuv_data = ctypes.string_at(overlay.pixels, overlay.pixels_size)

            pixel_format_map = {
                0: "yuv420p",
            }
            pixel_format = pixel_format_map.get(overlay.format, f"unknown({overlay.format})")

            frame = VideoFrameToRender(
                data=yuv_data,
                width=overlay.w,
                height=overlay.h,
                pixel_format=pixel_format
            )

            handler(frame)
        except Exception as e:
            print(f"Error in video frame handler: {e}")

    c_callback = VOUT_FRAME_CALLBACK(bridge_callback)
    vout_ptr = lib.RAPID_SDL_Vout_SimpleCallback_Create(c_callback, None)
    return vout_ptr, c_callback

def _create_aout_with_frame_bridge(handler: Callable):
    from .player import AudioFrameToRender

    def bridge_callback(buffer_ptr, length, spec_ptr, user_data):
        try:
            pcm_data = ctypes.string_at(buffer_ptr, length)
            spec = spec_ptr.contents

            frame = AudioFrameToRender(
                data=pcm_data,
                sample_rate=spec.sample_rate,
                channels=spec.channels,
                sample_format="s16",
                samples=spec.samples
            )

            handler(frame)
        except Exception as e:
            print(f"Error in audio frame handler: {e}")

    c_callback = AOUT_FRAME_CALLBACK(bridge_callback)
    aout_ptr = lib.RAPID_SDL_Aout_SimpleCallback_Create(c_callback, None)
    return aout_ptr, c_callback
