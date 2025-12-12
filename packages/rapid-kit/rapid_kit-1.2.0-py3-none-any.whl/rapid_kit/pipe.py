import ctypes
from enum import IntEnum
from typing import Callable, Optional
from .lib import get_lib

lib = get_lib()

class PipeState(IntEnum):
    UNDEFINED = 0
    ATTEMPTING = 1
    ESTABLISHED = 2
    ABOLISHED = 3
    FAILED = 4
    SHUTDOWN_BY_REMOTE = 5
    BROKEN = 6
    TOKEN_NOT_AVAILABLE = 7

PIPE_STATE_CALLBACK = ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.c_void_p)
INSTRUCT_RESPONSE_CALLBACK = ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_void_p)
EXTERNAL_USER_DATA_CALLBACK = ctypes.CFUNCTYPE(None, ctypes.c_uint, ctypes.c_uint, ctypes.c_char_p, ctypes.c_int, ctypes.c_void_p)

lib.RAPID_Core_PipeProxy_Create.argtypes = [ctypes.c_char_p]
lib.RAPID_Core_PipeProxy_Create.restype = ctypes.c_void_p

lib.RAPID_Core_PipeProxy_Destroy.argtypes = [ctypes.c_void_p]
lib.RAPID_Core_PipeProxy_Destroy.restype = None

lib.RAPID_Core_PipeProxy_Establish.argtypes = [ctypes.c_void_p]
lib.RAPID_Core_PipeProxy_Establish.restype = None

lib.RAPID_Core_PipeProxy_Abolish.argtypes = [ctypes.c_void_p]
lib.RAPID_Core_PipeProxy_Abolish.restype = None

lib.RAPID_Core_PipeProxy_Status.argtypes = [ctypes.c_void_p]
lib.RAPID_Core_PipeProxy_Status.restype = ctypes.c_int

lib.RAPID_Core_PipeProxy_EnableLanMode.argtypes = [ctypes.c_void_p, ctypes.c_int]
lib.RAPID_Core_PipeProxy_EnableLanMode.restype = None

lib.RAPID_Core_PipeProxy_SetStatusFunc.argtypes = [ctypes.c_void_p, PIPE_STATE_CALLBACK, ctypes.c_void_p]
lib.RAPID_Core_PipeProxy_SetStatusFunc.restype = None

lib.RAPID_Core_PipeProxy_InstructRequest.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_char_p, ctypes.c_uint, INSTRUCT_RESPONSE_CALLBACK, ctypes.c_uint, ctypes.c_void_p]
lib.RAPID_Core_PipeProxy_InstructRequest.restype = None

lib.RAPID_Core_PipeToken_Prepare.argtypes = [ctypes.c_char_p]
lib.RAPID_Core_PipeToken_Prepare.restype = None

lib.RAPID_Core_Instruct_SetUserExternalDataFunc.argtypes = [ctypes.c_void_p, EXTERNAL_USER_DATA_CALLBACK, ctypes.c_void_p]
lib.RAPID_Core_Instruct_SetUserExternalDataFunc.restype = None

lib.RAPID_Core_PipeProxy_SetTransportMode.argtypes = [ctypes.c_void_p, ctypes.c_int]
lib.RAPID_Core_PipeProxy_SetTransportMode.restype = None

class Pipe:
    def __init__(self, device_id: str):
        device_id_bytes = device_id.encode('utf-8')
        self._handle = lib.RAPID_Core_PipeProxy_Create(device_id_bytes)
        if not self._handle:
            raise RuntimeError("Failed to create pipe proxy")
        self._state_callback = None
        self._instruct_callback = None
        self._external_data_callback = None
    
    def __del__(self):        
        if hasattr(self, '_handle') and self._handle:
            lib.RAPID_Core_PipeProxy_Destroy(self._handle)
            self._handle = None
            self._state_callback = None
            self._instruct_callback = None
    
    def establish(self) -> None:       
        if not self._handle:
            return
        lib.RAPID_Core_PipeProxy_Establish(self._handle)
    
    def abolish(self) -> None:      
        if not self._handle:
            return
        lib.RAPID_Core_PipeProxy_Abolish(self._handle)
    
    def state(self) -> PipeState:      
        if not self._handle:
            return PipeState.UNDEFINED
        return PipeState(lib.RAPID_Core_PipeProxy_Status(self._handle))
    
    def listen(self, callback: Callable[[PipeState], None]):       
        if not self._handle:
            return
        
        def wrapper(status, user_data):
            try:
                if callback:
                    callback(PipeState(status))
            except:
                pass
        
        self._state_callback = PIPE_STATE_CALLBACK(wrapper)
        lib.RAPID_Core_PipeProxy_SetStatusFunc(self._handle, self._state_callback, None)
    
    def instruct_request(self, id: int, buffer: bytes = b'', timeout_s: int = 5, 
                         callback: Callable[[int, Optional[bytes]], None] = None):       
        if not self._handle:
            return
        
        def wrapper(state, response_buffer, buffer_size, user_data):
            try:
                if callback:
                    # response_buffer可能为空
                    response = None
                    if response_buffer:
                        response = response_buffer[:buffer_size]
                    callback(state, response)
            except:
                pass
        
        self._instruct_callback = INSTRUCT_RESPONSE_CALLBACK(wrapper)
        lib.RAPID_Core_PipeProxy_InstructRequest(
            self._handle, id, buffer, len(buffer),
            self._instruct_callback, timeout_s, None
        )

    def set_external_data_handler(self, callback: Optional[Callable[[int, int, bytes], None]]):
        if not self._handle:
            return

        if callback is None:
            self._external_data_callback = None
            lib.RAPID_Core_Instruct_SetUserExternalDataFunc(self._handle, None, None)
            return

        def wrapper(data1, data2, buffer, buffer_size, user_data):
            try:
                if callback and buffer:
                    data = buffer[:buffer_size] if buffer_size > 0 else b''
                    callback(data1, data2, data)
            except:
                pass

        self._external_data_callback = EXTERNAL_USER_DATA_CALLBACK(wrapper)
        lib.RAPID_Core_Instruct_SetUserExternalDataFunc(self._handle, self._external_data_callback, None)

    def set_transport_mode(self, mode: int):
        if not self._handle:
            return
        lib.RAPID_Core_PipeProxy_SetTransportMode(self._handle, mode)