import ctypes
from typing import Optional, Callable, Tuple
from enum import IntEnum
from .lib import get_lib

lib = get_lib()

class PersistentChannelState(IntEnum):
    DISCONNECTED = 0
    CONNECTING = 1
    CONNECTED = 2

RAPID_Core_PersistentChannelStateFunc = ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.c_char_p, ctypes.c_void_p)
RAPID_Core_PersistentChannelMessageFunc = ctypes.CFUNCTYPE(None, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_void_p)

lib.RAPID_Core_PersistentChannel_SetStateCallback.argtypes = [RAPID_Core_PersistentChannelStateFunc, ctypes.c_void_p]
lib.RAPID_Core_PersistentChannel_SetStateCallback.restype = None

lib.RAPID_Core_PersistentChannel_SetMessageCallback.argtypes = [RAPID_Core_PersistentChannelMessageFunc, ctypes.c_void_p]
lib.RAPID_Core_PersistentChannel_SetMessageCallback.restype = None

lib.RAPID_Core_PersistentChannel_Connect.argtypes = []
lib.RAPID_Core_PersistentChannel_Connect.restype = None

lib.RAPID_Core_PersistentChannel_Disconnect.argtypes = []
lib.RAPID_Core_PersistentChannel_Disconnect.restype = None

lib.RAPID_Core_PersistentChannel_CurrentState.argtypes = []
lib.RAPID_Core_PersistentChannel_CurrentState.restype = ctypes.c_int


class PersistentChannel:
    _instance = None
    _state_callback = None
    _message_callback = None
    _c_state_callback = None
    _c_message_callback = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def connect(self):
        lib.RAPID_Core_PersistentChannel_Connect()

    def disconnect(self):
        lib.RAPID_Core_PersistentChannel_Disconnect()

    @property
    def state(self) -> PersistentChannelState:
        return PersistentChannelState(lib.RAPID_Core_PersistentChannel_CurrentState())

    def set_state_listener(self, callback: Optional[Callable[[PersistentChannelState, str], None]]):
        if callback is None:
            PersistentChannel._state_callback = None
            PersistentChannel._c_state_callback = None
            lib.RAPID_Core_PersistentChannel_SetStateCallback(None, None)
            return

        def wrapper(state, reason, user_data):
            try:
                if callback:
                    reason_str = reason.decode('utf-8') if reason else ""
                    callback(PersistentChannelState(state), reason_str)
            except:
                pass

        PersistentChannel._state_callback = callback
        PersistentChannel._c_state_callback = RAPID_Core_PersistentChannelStateFunc(wrapper)
        lib.RAPID_Core_PersistentChannel_SetStateCallback(PersistentChannel._c_state_callback, None)

    def set_message_listener(self, callback: Optional[Callable[[str, str], None]]):
        if callback is None:
            PersistentChannel._message_callback = None
            PersistentChannel._c_message_callback = None
            lib.RAPID_Core_PersistentChannel_SetMessageCallback(None, None)
            return

        def wrapper(name, detail, user_data):
            try:
                if callback:
                    name_str = name.decode('utf-8') if name else ""
                    detail_str = detail.decode('utf-8') if detail else ""
                    callback(name_str, detail_str)
            except:
                pass

        PersistentChannel._message_callback = callback
        PersistentChannel._c_message_callback = RAPID_Core_PersistentChannelMessageFunc(wrapper)
        lib.RAPID_Core_PersistentChannel_SetMessageCallback(PersistentChannel._c_message_callback, None)
