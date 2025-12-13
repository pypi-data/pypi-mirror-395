import ctypes
from enum import IntEnum
from .lib import get_media_lib

lib = get_media_lib()

class MediaChatAudioSampleRate(IntEnum):
    AUDIO_SAMPLE_RATE_8K = 0
    AUDIO_SAMPLE_RATE_16K = 1

lib.RAPID_MediaChat_Create.argtypes = []
lib.RAPID_MediaChat_Create.restype = ctypes.c_void_p

lib.RAPID_MediaChat_SetAudioSampleRate.argtypes = [ctypes.c_void_p, ctypes.c_int]
lib.RAPID_MediaChat_SetAudioSampleRate.restype = None

lib.RAPID_MediaChat_EnableAEC.argtypes = [ctypes.c_void_p, ctypes.c_int]
lib.RAPID_MediaChat_EnableAEC.restype = None

lib.RAPID_MediaChat_IsStarted.argtypes = [ctypes.c_void_p]
lib.RAPID_MediaChat_IsStarted.restype = ctypes.c_int

lib.RAPID_MediaChat_Start.argtypes = [ctypes.c_void_p]
lib.RAPID_MediaChat_Start.restype = None

lib.RAPID_MediaChat_Stop.argtypes = [ctypes.c_void_p]
lib.RAPID_MediaChat_Stop.restype = None

lib.RAPID_MediaChat_Release.argtypes = [ctypes.c_void_p]
lib.RAPID_MediaChat_Release.restype = None

lib.RAPID_MediaChat_SetAin.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
lib.RAPID_MediaChat_SetAin.restype = None

lib.RAPID_MediaChat_SetChatChannel.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
lib.RAPID_MediaChat_SetChatChannel.restype = None

class MediaChat:
    def __init__(self):
        self._handle = lib.RAPID_MediaChat_Create()
        if not self._handle:
            raise RuntimeError("Failed to create media chat")
    
    def __del__(self):
        self.release()
    
    def set_audio_sample_rate(self, sample_rate):
        if not self._handle:
            return

        if isinstance(sample_rate, MediaChatAudioSampleRate):
            sample_rate_value = sample_rate.value
        else:
            sample_rate_value = sample_rate

        lib.RAPID_MediaChat_SetAudioSampleRate(self._handle, sample_rate_value)

    def enable_aec(self, enable: bool):
        if not self._handle:
            return
        lib.RAPID_MediaChat_EnableAEC(self._handle, 1 if enable else 0)

    def is_started(self):
        if not self._handle:
            return False
        
        return lib.RAPID_MediaChat_IsStarted(self._handle) != 0
    
    def start(self):
        if not self._handle:
            return
        
        lib.RAPID_MediaChat_Start(self._handle)
    
    def stop(self):
        if not self._handle:
            return
        
        lib.RAPID_MediaChat_Stop(self._handle)
    
    def set_ain(self, ain):
        if not self._handle:
            return
        
        lib.RAPID_MediaChat_SetAin(self._handle, ain)
    
    def set_chat_channel(self, channel):
        if not self._handle:
            return
        
        if hasattr(channel, '_handle'):
            channel_handle = channel._handle
        else:
            channel_handle = channel
            
        lib.RAPID_MediaChat_SetChatChannel(self._handle, channel_handle)
    
    def release(self):
        if self._handle:
            lib.RAPID_MediaChat_Release(self._handle)
            self._handle = None 