import ctypes
from .lib import get_lib

lib = get_lib()

class ChatAudioSampleRate:
    RATE_8K = 0
    RATE_16K = 1

lib.RAPID_Core_ChatChannel_Create.argtypes = [ctypes.c_void_p]
lib.RAPID_Core_ChatChannel_Create.restype = ctypes.c_void_p

lib.RAPID_Core_ChatChannel_SetAudioSampleRate.argtypes = [ctypes.c_void_p, ctypes.c_int]
lib.RAPID_Core_ChatChannel_SetAudioSampleRate.restype = None

lib.RAPID_Core_ChatChannel_Free.argtypes = [ctypes.c_void_p]
lib.RAPID_Core_ChatChannel_Free.restype = None

class ChatChannel:
    def __init__(self, pipe_proxy):
        self._handle = None
        if pipe_proxy and hasattr(pipe_proxy, '_handle'):
            self._handle = lib.RAPID_Core_ChatChannel_Create(pipe_proxy._handle)
        else:
            raise ValueError("Invalid pipe_proxy provided")
    
    def __del__(self):
        self.close()
    
    def set_audio_sample_rate(self, sample_rate):
        if not self._handle:
            return False
        
        lib.RAPID_Core_ChatChannel_SetAudioSampleRate(self._handle, sample_rate)
        return True
    
    def close(self):
        if self._handle:
            lib.RAPID_Core_ChatChannel_Free(self._handle)
            self._handle = None