import ctypes
from typing import Callable, Optional, Any, Protocol, cast
from .lib import get_lib

lib = get_lib()

INSTRUCT_CALLBACK_TYPE = ctypes.CFUNCTYPE(None, ctypes.c_char_p, ctypes.c_int, ctypes.c_void_p)

lib.RAPID_Core_InstructStandard_Create.argtypes = [ctypes.c_void_p, INSTRUCT_CALLBACK_TYPE, ctypes.c_void_p]
lib.RAPID_Core_InstructStandard_Create.restype = ctypes.c_void_p

lib.RAPID_Core_InstructStandard_Request.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]
lib.RAPID_Core_InstructStandard_Request.restype = None

lib.RAPID_Core_InstructStandard_Release.argtypes = [ctypes.c_void_p]
lib.RAPID_Core_InstructStandard_Release.restype = None

class PipeProtocol(Protocol):
    _handle: ctypes.c_void_p

class InstructStandard:
    def __init__(self, pipe: PipeProtocol, callback: Optional[Callable[[str], None]] = None) -> None:
        self._callback_func: Optional[INSTRUCT_CALLBACK_TYPE] = None
        self._handle: Optional[ctypes.c_void_p] = None
        
        if callback:
            def wrapper(json_str: ctypes.c_char_p, json_length: ctypes.c_int, user_data: ctypes.c_void_p) -> None:
                if json_str:
                    try:
                        json_data = json_str[:json_length].decode('utf-8')
                        callback(json_data)
                    except Exception:
                        pass
            
            self._callback_func = INSTRUCT_CALLBACK_TYPE(wrapper)
        
        if hasattr(pipe, '_handle') and pipe._handle:
            self._handle = lib.RAPID_Core_InstructStandard_Create(
                pipe._handle,
                self._callback_func,
                None
            )
        else:
            raise ValueError("Invalid pipe provided or pipe handle is None")
        
        if not self._handle:
            raise RuntimeError("Failed to create instruct channel")
    
    def __del__(self) -> None:
        self.release()
    
    def release(self) -> None:
        if hasattr(self, '_handle') and self._handle:
            lib.RAPID_Core_InstructStandard_Release(self._handle)
            self._handle = None
    
    def request(self, name: str, params: Optional[str] = None) -> None:
        if not self._handle:
            raise RuntimeError("Instruct channel not initialized or already released")
        
        if not name:
            raise ValueError("Command name cannot be empty")
        
        name_bytes = name.encode('utf-8')
        params_bytes = b'' if params is None else params.encode('utf-8')
        
        lib.RAPID_Core_InstructStandard_Request(self._handle, name_bytes, params_bytes)