import ctypes
from typing import Optional, Callable
from .lib import get_lib

lib = get_lib()

UNAUTHORIZED_CALLBACK = ctypes.CFUNCTYPE(None, ctypes.c_void_p)

_unauthorized_callback = None

lib.RAPID_Core_Unauthorized_SetFunc.argtypes = [UNAUTHORIZED_CALLBACK, ctypes.c_void_p]
lib.RAPID_Core_Unauthorized_SetFunc.restype = None

def set_unauthorized_handler(callback: Optional[Callable[[], None]]):
    global _unauthorized_callback

    if callback is None:
        _unauthorized_callback = None
        lib.RAPID_Core_Unauthorized_SetFunc(None, None)
        return

    def wrapper(user_context):
        try:
            if callback:
                callback()
        except:
            pass

    _unauthorized_callback = UNAUTHORIZED_CALLBACK(wrapper)
    lib.RAPID_Core_Unauthorized_SetFunc(_unauthorized_callback, None)
