import ctypes
from typing import Optional, Callable
from enum import IntEnum
from .lib import get_lib

lib = get_lib()

class ProfileTransmitterState(IntEnum):
    IDLE = 0
    TRANSMITTING = 1
    SUCCESS = 2
    FAILED = 3

class BindingProfileByteArray(ctypes.Structure):
    _fields_ = [
        ("data", ctypes.POINTER(ctypes.c_ubyte)),
        ("size", ctypes.c_int)
    ]

RAPID_Core_ProfileTransmitter_StateFunc = ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.c_void_p)

lib.RAPID_Core_BindingProfile_Create.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
lib.RAPID_Core_BindingProfile_Create.restype = ctypes.c_char_p

lib.RAPID_Core_BindingProfileWithHeader.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
lib.RAPID_Core_BindingProfileWithHeader.restype = ctypes.POINTER(BindingProfileByteArray)

lib.RAPID_Core_BindingProfile_Release.argtypes = [ctypes.c_char_p]
lib.RAPID_Core_BindingProfile_Release.restype = None

lib.RAPID_Core_BindingProfile_ByteArray_Release.argtypes = [ctypes.POINTER(BindingProfileByteArray)]
lib.RAPID_Core_BindingProfile_ByteArray_Release.restype = None

lib.RAPID_Core_ProfileTransmitter_Create.argtypes = []
lib.RAPID_Core_ProfileTransmitter_Create.restype = ctypes.c_void_p

lib.RAPID_Core_ProfileTransmitter_Prepare.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
lib.RAPID_Core_ProfileTransmitter_Prepare.restype = None

lib.RAPID_Core_ProfileTransmitter_SetStateFunc.argtypes = [ctypes.c_void_p, RAPID_Core_ProfileTransmitter_StateFunc, ctypes.c_void_p]
lib.RAPID_Core_ProfileTransmitter_SetStateFunc.restype = None

lib.RAPID_Core_ProfileTransmitter_GetCurrentState.argtypes = [ctypes.c_void_p]
lib.RAPID_Core_ProfileTransmitter_GetCurrentState.restype = ctypes.c_int

lib.RAPID_Core_ProfileTransmitter_Start.argtypes = [ctypes.c_void_p]
lib.RAPID_Core_ProfileTransmitter_Start.restype = None

lib.RAPID_Core_ProfileTransmitter_Stop.argtypes = [ctypes.c_void_p]
lib.RAPID_Core_ProfileTransmitter_Stop.restype = None

lib.RAPID_Core_ProfileTransmitter_Free.argtypes = [ctypes.c_void_p]
lib.RAPID_Core_ProfileTransmitter_Free.restype = None


class BindingProfile:
    @staticmethod
    def create(wifi: str, password: str, bind_token: str) -> bytes:
        wifi_bytes = wifi.encode('utf-8')
        pwd_bytes = password.encode('utf-8')
        token_bytes = bind_token.encode('utf-8')

        profile_str = lib.RAPID_Core_BindingProfile_Create(wifi_bytes, pwd_bytes, token_bytes)
        if not profile_str:
            raise RuntimeError("Failed to create binding profile")

        result = profile_str.decode('utf-8').encode('utf-8')
        lib.RAPID_Core_BindingProfile_Release(profile_str)
        return result

    @staticmethod
    def create_with_header(wifi: str, password: str, bind_token: str) -> bytes:
        wifi_bytes = wifi.encode('utf-8')
        pwd_bytes = password.encode('utf-8')
        token_bytes = bind_token.encode('utf-8')

        byte_array_ptr = lib.RAPID_Core_BindingProfileWithHeader(wifi_bytes, pwd_bytes, token_bytes)
        if not byte_array_ptr:
            raise RuntimeError("Failed to create binding profile with header")

        byte_array = byte_array_ptr.contents
        result = bytes(byte_array.data[:byte_array.size])
        lib.RAPID_Core_BindingProfile_ByteArray_Release(byte_array_ptr)
        return result


class ProfileTransmitter:
    def __init__(self):
        self._handle = lib.RAPID_Core_ProfileTransmitter_Create()
        if not self._handle:
            raise RuntimeError("Failed to create profile transmitter")
        self._state_callback = None

    def __del__(self):
        if self._handle:
            lib.RAPID_Core_ProfileTransmitter_Free(self._handle)
            self._handle = None

    def prepare(self, ssid: str, password: str, bind_token: str):
        if not self._handle:
            return
        ssid_bytes = ssid.encode('utf-8')
        pwd_bytes = password.encode('utf-8')
        token_bytes = bind_token.encode('utf-8')
        lib.RAPID_Core_ProfileTransmitter_Prepare(self._handle, ssid_bytes, pwd_bytes, token_bytes)

    def start(self):
        if not self._handle:
            return
        lib.RAPID_Core_ProfileTransmitter_Start(self._handle)

    def stop(self):
        if not self._handle:
            return
        lib.RAPID_Core_ProfileTransmitter_Stop(self._handle)

    @property
    def state(self) -> ProfileTransmitterState:
        if not self._handle:
            return ProfileTransmitterState.IDLE
        return ProfileTransmitterState(lib.RAPID_Core_ProfileTransmitter_GetCurrentState(self._handle))

    def set_state_listener(self, callback: Optional[Callable[[ProfileTransmitterState], None]]):
        if not self._handle:
            return

        if callback is None:
            self._state_callback = None
            lib.RAPID_Core_ProfileTransmitter_SetStateFunc(self._handle, None, None)
            return

        def wrapper(state, user_data):
            try:
                if callback:
                    callback(ProfileTransmitterState(state))
            except:
                pass

        self._state_callback = RAPID_Core_ProfileTransmitter_StateFunc(wrapper)
        lib.RAPID_Core_ProfileTransmitter_SetStateFunc(self._handle, self._state_callback, None)
