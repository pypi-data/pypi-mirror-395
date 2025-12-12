import ctypes
from typing import Optional
from .lib import get_lib

lib = get_lib()

lib.RAPID_Core_RegisterSignalHandler.argtypes = []
lib.RAPID_Core_RegisterSignalHandler.restype = None

previous_crash_detail = ctypes.c_char_p.in_dll(lib, "previous_crash_detail")
previous_crash_detail_length = ctypes.c_int.in_dll(lib, "previous_crash_detail_length")

def register_signal_handler():
    lib.RAPID_Core_RegisterSignalHandler()

def get_previous_crash_detail() -> Optional[str]:
    if previous_crash_detail.value and previous_crash_detail_length.value > 0:
        return previous_crash_detail.value[:previous_crash_detail_length.value].decode('utf-8')
    return None
