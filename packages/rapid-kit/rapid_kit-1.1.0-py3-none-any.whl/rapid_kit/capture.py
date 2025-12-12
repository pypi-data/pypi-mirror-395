import ctypes
from typing import Optional, Callable
from enum import IntEnum
from .lib import get_media_lib

lib = get_media_lib()

class MediaCaptureState(IntEnum):
    IDLE = 0
    PREPARING = 1
    PREPARED = 2
    STARTED = 3
    STOPPED = 4
    ERROR = 5

RAPID_MediaCapture_StateFunc = ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.c_void_p)
RAPID_MediaCapture_UtsFunc = ctypes.CFUNCTYPE(None, ctypes.c_longlong, ctypes.c_void_p)

lib.RAPID_MediaCapture_Create.argtypes = []
lib.RAPID_MediaCapture_Create.restype = ctypes.c_void_p

lib.RAPID_MediaCapture_Destroy.argtypes = [ctypes.c_void_p]
lib.RAPID_MediaCapture_Destroy.restype = None

lib.RAPID_MediaCapture_Prepare.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
lib.RAPID_MediaCapture_Prepare.restype = None

lib.RAPID_MediaCapture_Start.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
lib.RAPID_MediaCapture_Start.restype = None

lib.RAPID_MediaCapture_Stop.argtypes = [ctypes.c_void_p]
lib.RAPID_MediaCapture_Stop.restype = None

lib.RAPID_MediaCapture_GetUts.argtypes = [ctypes.c_void_p]
lib.RAPID_MediaCapture_GetUts.restype = ctypes.c_longlong

lib.RAPID_MediaCapture_CurrentState.argtypes = [ctypes.c_void_p]
lib.RAPID_MediaCapture_CurrentState.restype = ctypes.c_int

lib.RAPID_MediaCapture_SetStateFunc.argtypes = [ctypes.c_void_p, RAPID_MediaCapture_StateFunc, ctypes.c_void_p]
lib.RAPID_MediaCapture_SetStateFunc.restype = None

lib.RAPID_MediaCapture_SetUtsFunc.argtypes = [ctypes.c_void_p, RAPID_MediaCapture_UtsFunc, ctypes.c_void_p]
lib.RAPID_MediaCapture_SetUtsFunc.restype = None


class MediaCapture:
    def __init__(self):
        self._handle = lib.RAPID_MediaCapture_Create()
        if not self._handle:
            raise RuntimeError("Failed to create media capture")
        self._state_callback = None
        self._uts_callback = None

    def __del__(self):
        if self._handle:
            lib.RAPID_MediaCapture_Destroy(self._handle)
            self._handle = None

    def prepare(self, provider) -> None:
        if not self._handle:
            return
        provider_handle = provider._handle if hasattr(provider, '_handle') else provider
        lib.RAPID_MediaCapture_Prepare(self._handle, provider_handle)

    def start(self, output_file_path: str) -> None:
        if not self._handle:
            return
        output_path_bytes = output_file_path.encode('utf-8')
        lib.RAPID_MediaCapture_Start(self._handle, output_path_bytes)

    def stop(self) -> None:
        if not self._handle:
            return
        lib.RAPID_MediaCapture_Stop(self._handle)

    @property
    def uts(self) -> int:
        if not self._handle:
            return 0
        return lib.RAPID_MediaCapture_GetUts(self._handle)

    @property
    def state(self) -> MediaCaptureState:
        if not self._handle:
            return MediaCaptureState.IDLE
        return MediaCaptureState(lib.RAPID_MediaCapture_CurrentState(self._handle))

    def set_state_listener(self, callback: Optional[Callable[[MediaCaptureState], None]]):
        if callback is None:
            self._state_callback = None
            lib.RAPID_MediaCapture_SetStateFunc(self._handle, None, None)
            return

        def wrapper(state, user_data):
            try:
                if callback:
                    callback(MediaCaptureState(state))
            except:
                pass

        self._state_callback = RAPID_MediaCapture_StateFunc(wrapper)
        lib.RAPID_MediaCapture_SetStateFunc(self._handle, self._state_callback, None)

    def set_uts_listener(self, callback: Optional[Callable[[int], None]]):
        if callback is None:
            self._uts_callback = None
            lib.RAPID_MediaCapture_SetUtsFunc(self._handle, None, None)
            return

        def wrapper(uts_ms, user_data):
            try:
                if callback:
                    callback(uts_ms)
            except:
                pass

        self._uts_callback = RAPID_MediaCapture_UtsFunc(wrapper)
        lib.RAPID_MediaCapture_SetUtsFunc(self._handle, self._uts_callback, None)
