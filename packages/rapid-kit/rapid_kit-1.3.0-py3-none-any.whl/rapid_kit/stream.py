import ctypes
import time
from .lib import get_lib
from enum import Enum, IntEnum
from typing import Callable, Optional, Any, Union
from .packet import Packet
from .pipe import Pipe

lib = get_lib()

FILE_NOT_FOUND_CALLBACK = ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.c_void_p)
DOWNLOAD_COMPLETE_CALLBACK = ctypes.CFUNCTYPE(None, ctypes.c_void_p)
STREAM_PACKET_LISTENER = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_void_p)
EXTERNAL_USER_DATA_CALLBACK = ctypes.CFUNCTYPE(None, ctypes.c_uint, ctypes.c_uint, ctypes.c_char_p, ctypes.c_int, ctypes.c_void_p)

lib.RAPID_Core_LiveStream_CreateDefault.argtypes = [ctypes.c_void_p]
lib.RAPID_Core_LiveStream_CreateDefault.restype = ctypes.c_void_p

lib.RAPID_Core_LiveStream_CreateSecondary.argtypes = [ctypes.c_void_p]
lib.RAPID_Core_LiveStream_CreateSecondary.restype = ctypes.c_void_p

lib.RAPID_Core_LiveStream_Start.argtypes = [ctypes.c_void_p]
lib.RAPID_Core_LiveStream_Start.restype = None

lib.RAPID_Core_LiveStream_Stop.argtypes = [ctypes.c_void_p]
lib.RAPID_Core_LiveStream_Stop.restype = None

lib.RAPID_Core_LiveStream_IsStarted.argtypes = [ctypes.c_void_p]
lib.RAPID_Core_LiveStream_IsStarted.restype = ctypes.c_int

lib.RAPID_Core_LiveStream_SwitchQuality.argtypes = [ctypes.c_void_p, ctypes.c_int]
lib.RAPID_Core_LiveStream_SwitchQuality.restype = None

lib.RAPID_Core_LiveStream_SwitchHighQuality.argtypes = [ctypes.c_void_p]
lib.RAPID_Core_LiveStream_SwitchHighQuality.restype = None

lib.RAPID_Core_LiveStream_SwitchLowQuality.argtypes = [ctypes.c_void_p]
lib.RAPID_Core_LiveStream_SwitchLowQuality.restype = None

lib.RAPID_Core_LiveStream_CurrentQuality.argtypes = [ctypes.c_void_p]
lib.RAPID_Core_LiveStream_CurrentQuality.restype = ctypes.c_int

lib.RAPID_Core_LiveStream_RequestKeyFrame.argtypes = [ctypes.c_void_p]
lib.RAPID_Core_LiveStream_RequestKeyFrame.restype = None

lib.RAPID_Core_LiveStream_Release.argtypes = [ctypes.c_void_p]
lib.RAPID_Core_LiveStream_Release.restype = None

lib.RAPID_Core_LiveStream_IndexedProvider.argtypes = [ctypes.c_void_p, ctypes.c_uint]
lib.RAPID_Core_LiveStream_IndexedProvider.restype = ctypes.c_void_p

lib.RAPID_Core_LocalReplayStream_Create.argtypes = [ctypes.c_void_p]
lib.RAPID_Core_LocalReplayStream_Create.restype = ctypes.c_void_p

lib.RAPID_Core_LocalReplayStream_Start.argtypes = [ctypes.c_void_p]
lib.RAPID_Core_LocalReplayStream_Start.restype = None

lib.RAPID_Core_LocalReplayStream_Prepare.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_uint]
lib.RAPID_Core_LocalReplayStream_Prepare.restype = None

lib.RAPID_Core_LocalReplayStream_Stop.argtypes = [ctypes.c_void_p]
lib.RAPID_Core_LocalReplayStream_Stop.restype = None

lib.RAPID_Core_LocalReplayStream_IsStarted.argtypes = [ctypes.c_void_p]
lib.RAPID_Core_LocalReplayStream_IsStarted.restype = ctypes.c_int

lib.RAPID_Core_LocalReplayStream_Seek.argtypes = [ctypes.c_void_p, ctypes.c_longlong]
lib.RAPID_Core_LocalReplayStream_Seek.restype = None

lib.RAPID_Core_LocalReplayStream_SetSpeed.argtypes = [ctypes.c_void_p, ctypes.c_int]
lib.RAPID_Core_LocalReplayStream_SetSpeed.restype = None

lib.RAPID_Core_LocalReplayStream_Pause.argtypes = [ctypes.c_void_p]
lib.RAPID_Core_LocalReplayStream_Pause.restype = None

lib.RAPID_Core_LocalReplayStream_IsPaused.argtypes = [ctypes.c_void_p]
lib.RAPID_Core_LocalReplayStream_IsPaused.restype = ctypes.c_int

lib.RAPID_Core_LocalReplayStream_Resume.argtypes = [ctypes.c_void_p]
lib.RAPID_Core_LocalReplayStream_Resume.restype = None

lib.RAPID_Core_LocalReplayStream_Release.argtypes = [ctypes.c_void_p]
lib.RAPID_Core_LocalReplayStream_Release.restype = None

lib.RAPID_Core_LocalReplayStream_IndexedProvider.argtypes = [ctypes.c_void_p, ctypes.c_uint]
lib.RAPID_Core_LocalReplayStream_IndexedProvider.restype = ctypes.c_void_p

lib.RAPID_Core_CloudReplayStream_Create.argtypes = [ctypes.c_char_p]
lib.RAPID_Core_CloudReplayStream_Create.restype = ctypes.c_void_p

lib.RAPID_Core_CloudReplayStream_Prepare.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_uint, ctypes.c_char_p]
lib.RAPID_Core_CloudReplayStream_Prepare.restype = None

lib.RAPID_Core_CloudReplayStream_Start.argtypes = [ctypes.c_void_p]
lib.RAPID_Core_CloudReplayStream_Start.restype = None

lib.RAPID_Core_CloudReplayStream_Seek.argtypes = [ctypes.c_void_p, ctypes.c_uint]
lib.RAPID_Core_CloudReplayStream_Seek.restype = None

lib.RAPID_Core_CloudReplayStream_SetSpeed.argtypes = [ctypes.c_void_p, ctypes.c_int]
lib.RAPID_Core_CloudReplayStream_SetSpeed.restype = None

lib.RAPID_Core_CloudReplayStream_Pause.argtypes = [ctypes.c_void_p]
lib.RAPID_Core_CloudReplayStream_Pause.restype = None

lib.RAPID_Core_CloudReplayStream_Resume.argtypes = [ctypes.c_void_p]
lib.RAPID_Core_CloudReplayStream_Resume.restype = None

lib.RAPID_Core_CloudReplayStream_Stop.argtypes = [ctypes.c_void_p]
lib.RAPID_Core_CloudReplayStream_Stop.restype = None

lib.RAPID_Core_CloudReplayStream_IsPaused.argtypes = [ctypes.c_void_p]
lib.RAPID_Core_CloudReplayStream_IsPaused.restype = ctypes.c_int

lib.RAPID_Core_CloudReplayStream_IsStarted.argtypes = [ctypes.c_void_p]
lib.RAPID_Core_CloudReplayStream_IsStarted.restype = ctypes.c_int

lib.RAPID_Core_CloudReplayStream_Release.argtypes = [ctypes.c_void_p]
lib.RAPID_Core_CloudReplayStream_Release.restype = None

lib.RAPID_Core_CloudReplayStream_SetFileNotFoundFunc.argtypes = [ctypes.c_void_p, FILE_NOT_FOUND_CALLBACK, ctypes.c_void_p]
lib.RAPID_Core_CloudReplayStream_SetFileNotFoundFunc.restype = None

lib.RAPID_Core_CloudReplayStream_SetDownloadCompleteFunc.argtypes = [ctypes.c_void_p, DOWNLOAD_COMPLETE_CALLBACK, ctypes.c_void_p]
lib.RAPID_Core_CloudReplayStream_SetDownloadCompleteFunc.restype = None

lib.RAPID_Core_CloudReplayStream_IndexedProvider.argtypes = [ctypes.c_void_p, ctypes.c_uint]
lib.RAPID_Core_CloudReplayStream_IndexedProvider.restype = ctypes.c_void_p

lib.RAPID_Core_RelayStream_Create.argtypes = [ctypes.c_char_p]
lib.RAPID_Core_RelayStream_Create.restype = ctypes.c_void_p

lib.RAPID_Core_RelayStream_Enqueue.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
lib.RAPID_Core_RelayStream_Enqueue.restype = None

lib.RAPID_Core_RelayStream_Release.argtypes = [ctypes.c_void_p]
lib.RAPID_Core_RelayStream_Release.restype = None

lib.RAPID_Core_RelayStream_IndexedProvider.argtypes = [ctypes.c_void_p, ctypes.c_uint]
lib.RAPID_Core_RelayStream_IndexedProvider.restype = ctypes.c_void_p

lib.RAPID_Core_LiveStream_SetUserExternalDataFunc.argtypes = [ctypes.c_void_p, EXTERNAL_USER_DATA_CALLBACK, ctypes.c_void_p]
lib.RAPID_Core_LiveStream_SetUserExternalDataFunc.restype = None

lib.RAPID_Core_LiveStream_CreateSecondaryWithAudio.argtypes = [ctypes.c_void_p]
lib.RAPID_Core_LiveStream_CreateSecondaryWithAudio.restype = ctypes.c_void_p

lib.RAPID_Core_LocalReplayStream_CompatibleOnResumeInstruct.argtypes = [ctypes.c_void_p]
lib.RAPID_Core_LocalReplayStream_CompatibleOnResumeInstruct.restype = None

lib.RAPID_Core_CloudReplayStream_SetRetrieveErrorFunc.argtypes = [ctypes.c_void_p, ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.c_void_p), ctypes.c_void_p]
lib.RAPID_Core_CloudReplayStream_SetRetrieveErrorFunc.restype = None

lib.RAPID_Core_CloudReplayStream_EnableDownloadControl.argtypes = [ctypes.c_void_p, ctypes.c_int]
lib.RAPID_Core_CloudReplayStream_EnableDownloadControl.restype = None

lib.RAPID_Core_Stream_EnableDebugging.argtypes = [ctypes.c_int]
lib.RAPID_Core_Stream_EnableDebugging.restype = None

lib.RAPID_Core_StreamProvider_SetPacketFunc.argtypes = [ctypes.c_void_p, STREAM_PACKET_LISTENER, ctypes.c_void_p]
lib.RAPID_Core_StreamProvider_SetPacketFunc.restype = None

lib.RAPID_Core_StreamProvider_RemovePacketFunc.argtypes = [ctypes.c_void_p]
lib.RAPID_Core_StreamProvider_RemovePacketFunc.restype = None

class StreamQuality(IntEnum):
    HIGH = 1
    LOW = 5    

class StreamProvider:
    def __init__(self, handle: ctypes.c_void_p):
        self._handle = handle
        self._packet_listener = None
    
    def get_native_handle(self) -> ctypes.c_void_p:
        return self._handle
    
    def set_packet_listener(self, callback: Callable[[Packet], None]) -> None:
        if not self._handle:
            return
        
        def wrapper(packet, user_data):
            try:
                if callback and packet:
                    from .packet import Packet
                    packet_obj = Packet._from_handle(packet)
                    callback(packet_obj)
            except:
                pass
        
        self._packet_listener = STREAM_PACKET_LISTENER(wrapper)
        lib.RAPID_Core_StreamProvider_SetPacketFunc(self._handle, self._packet_listener, None)
    
    def remove_packet_listener(self) -> None:
        if not self._handle:
            return
        
        lib.RAPID_Core_StreamProvider_RemovePacketFunc(self._handle)
        self._packet_listener = None

class LiveStream:
    def __init__(self, pipe: Pipe, is_secondary: bool = False):
        if not pipe or not hasattr(pipe, '_handle'):
            raise ValueError("Invalid pipe provided")

        if is_secondary:
            self._handle = lib.RAPID_Core_LiveStream_CreateSecondary(pipe._handle)
        else:
            self._handle = lib.RAPID_Core_LiveStream_CreateDefault(pipe._handle)

        if not self._handle:
            raise RuntimeError("Failed to create live stream")
        self._external_data_callback = None

    @classmethod
    def create_secondary_with_audio(cls, pipe: Pipe):
        if not pipe or not hasattr(pipe, '_handle'):
            raise ValueError("Invalid pipe provided")
        instance = cls.__new__(cls)
        instance._handle = lib.RAPID_Core_LiveStream_CreateSecondaryWithAudio(pipe._handle)
        if not instance._handle:
            raise RuntimeError("Failed to create secondary stream with audio")
        instance._external_data_callback = None
        return instance
    
    def __del__(self) -> None:
        self._release()
    
    def start(self) -> None:
        if not self._handle:
            return
        lib.RAPID_Core_LiveStream_Start(self._handle)
    
    def stop(self) -> None:
        if not self._handle:
            return
        lib.RAPID_Core_LiveStream_Stop(self._handle)
    
    def is_started(self) -> bool:
        if not self._handle:
            return False
        return lib.RAPID_Core_LiveStream_IsStarted(self._handle) != 0
    
    def switch_quality(self, quality: int) -> None:
        if not self._handle:
            return
        lib.RAPID_Core_LiveStream_SwitchQuality(self._handle, quality)
    
    def switch_high_quality(self) -> None:
        if not self._handle:
            return
        lib.RAPID_Core_LiveStream_SwitchHighQuality(self._handle)
    
    def switch_low_quality(self) -> None:
        if not self._handle:
            return
        lib.RAPID_Core_LiveStream_SwitchLowQuality(self._handle)
    
    def current_quality(self) -> int:
        if not self._handle:
            return 0
        return lib.RAPID_Core_LiveStream_CurrentQuality(self._handle)
    
    def request_key_frame(self) -> None:
        if not self._handle:
            return
        lib.RAPID_Core_LiveStream_RequestKeyFrame(self._handle)
    
    def provider(self, index: int = 0) -> Optional[StreamProvider]:
        if not self._handle:
            return None
        provider_handle = lib.RAPID_Core_LiveStream_IndexedProvider(self._handle, index)
        if not provider_handle:
            return None
        return StreamProvider(provider_handle)
    
    def set_external_data_handler(self, callback: Optional[Callable[[int, int, bytes], None]]):
        if not self._handle:
            return

        if callback is None:
            self._external_data_callback = None
            lib.RAPID_Core_LiveStream_SetUserExternalDataFunc(self._handle, None, None)
            return

        def wrapper(data1, data2, buffer, buffer_size, user_data):
            try:
                if callback and buffer:
                    data = buffer[:buffer_size] if buffer_size > 0 else b''
                    callback(data1, data2, data)
            except:
                pass

        self._external_data_callback = EXTERNAL_USER_DATA_CALLBACK(wrapper)
        lib.RAPID_Core_LiveStream_SetUserExternalDataFunc(self._handle, self._external_data_callback, None)

    def _release(self) -> None:
        if self._handle:
            lib.RAPID_Core_LiveStream_Release(self._handle)
            self._handle = None
            self._external_data_callback = None

class LocalReplayStream:
    def __init__(self, pipe: Pipe):
        if not pipe or not hasattr(pipe, '_handle'):
            raise ValueError("Invalid pipe provided")
        
        self._handle = lib.RAPID_Core_LocalReplayStream_Create(pipe._handle)
        if not self._handle:
            raise RuntimeError("Failed to create local replay stream")
    
    def __del__(self) -> None:
        self._release()
    
    def prepare(self, start_timestamp_s: int, end_timestamp_s: int) -> None:
        if not self._handle:
            return
        lib.RAPID_Core_LocalReplayStream_Prepare(self._handle, start_timestamp_s, end_timestamp_s)
    
    def start(self) -> None:
        if not self._handle:
            return
        lib.RAPID_Core_LocalReplayStream_Start(self._handle)
    
    def stop(self) -> None:
        if not self._handle:
            return
        lib.RAPID_Core_LocalReplayStream_Stop(self._handle)
    
    def is_started(self) -> bool:
        if not self._handle:
            return False
        return lib.RAPID_Core_LocalReplayStream_IsStarted(self._handle) != 0
    
    def seek(self, timestamp: int) -> None:
        if not self._handle:
            return
        lib.RAPID_Core_LocalReplayStream_Seek(self._handle, timestamp)
    
    def set_speed(self, speed: int) -> None:
        if not self._handle:
            return
        lib.RAPID_Core_LocalReplayStream_SetSpeed(self._handle, speed)
    
    def pause(self) -> None:
        if not self._handle:
            return
        lib.RAPID_Core_LocalReplayStream_Pause(self._handle)
    
    def is_paused(self) -> bool:
        if not self._handle:
            return False
        return lib.RAPID_Core_LocalReplayStream_IsPaused(self._handle) != 0
    
    def resume(self) -> None:
        if not self._handle:
            return
        lib.RAPID_Core_LocalReplayStream_Resume(self._handle)
    
    def compatible_on_resume_instruct(self) -> None:
        if not self._handle:
            return
        lib.RAPID_Core_LocalReplayStream_CompatibleOnResumeInstruct(self._handle)

    def provider(self, index: int = 0) -> Optional[StreamProvider]:
        if not self._handle:
            return None
        provider_handle = lib.RAPID_Core_LocalReplayStream_IndexedProvider(self._handle, index)
        if not provider_handle:
            return None
        return StreamProvider(provider_handle)

    def _release(self) -> None:
        if not self._handle:
            lib.RAPID_Core_LocalReplayStream_Release(self._handle)
            self._handle = None

class CloudReplayStream:
    def __init__(self, device_id: Union[str, bytes]):
        device_id_bytes = device_id.encode('utf-8') if isinstance(device_id, str) else device_id
        self._handle = lib.RAPID_Core_CloudReplayStream_Create(device_id_bytes)
        if not self._handle:
            raise RuntimeError("Failed to create cloud replay stream")
        self._file_not_found_callback = None
        self._download_complete_callback = None
        self._retrieve_error_callback = None
    
    def __del__(self) -> None:
        self._release()
    
    def prepare(self, start_timestamp_s: int, end_timestamp_s: int, storage_id: Union[str, bytes]) -> None:
        if not self._handle:
            return
        
        storage_id_bytes = storage_id.encode('utf-8') if isinstance(storage_id, str) else storage_id
        lib.RAPID_Core_CloudReplayStream_Prepare(self._handle, start_timestamp_s, end_timestamp_s, storage_id_bytes)
    
    def start(self) -> None:
        if not self._handle:
            return
        lib.RAPID_Core_CloudReplayStream_Start(self._handle)
    
    def seek(self, timestamp_s: int) -> None:
        if not self._handle:
            return
        lib.RAPID_Core_CloudReplayStream_Seek(self._handle, timestamp_s)
    
    def set_speed(self, speed: int) -> None:
        if not self._handle:
            return
        lib.RAPID_Core_CloudReplayStream_SetSpeed(self._handle, speed)
    
    def pause(self) -> None:
        if not self._handle:
            return
        lib.RAPID_Core_CloudReplayStream_Pause(self._handle)
    
    def resume(self) -> None:
        if not self._handle:
            return
        lib.RAPID_Core_CloudReplayStream_Resume(self._handle)
    
    def stop(self) -> None:
        if not self._handle:
            return
        lib.RAPID_Core_CloudReplayStream_Stop(self._handle)
    
    def is_paused(self) -> bool:
        if not self._handle:
            return False
        return lib.RAPID_Core_CloudReplayStream_IsPaused(self._handle) != 0
    
    def is_started(self) -> bool:
        if not self._handle:
            return False
        return lib.RAPID_Core_CloudReplayStream_IsStarted(self._handle) != 0
    
    def set_file_not_found_callback(self, callback: Callable[[int], None]) -> None:
        if not self._handle:
            return
        
        def wrapper(timestamp_s, user_data):
            try:
                if callback:
                    callback(timestamp_s)
            except:
                pass
        
        self._file_not_found_callback = FILE_NOT_FOUND_CALLBACK(wrapper)
        lib.RAPID_Core_CloudReplayStream_SetFileNotFoundFunc(self._handle, self._file_not_found_callback, None)
    
    def set_download_complete_callback(self, callback: Callable[[], None]) -> None:
        if not self._handle:
            return
        
        def wrapper(user_data):
            try:
                if callback:
                    callback()
            except:
                pass
        
        self._download_complete_callback = DOWNLOAD_COMPLETE_CALLBACK(wrapper)
        lib.RAPID_Core_CloudReplayStream_SetDownloadCompleteFunc(self._handle, self._download_complete_callback, None)
    
    def set_retrieve_error_handler(self, callback: Optional[Callable[[int], None]]):
        if not self._handle:
            return

        if callback is None:
            self._retrieve_error_callback = None
            lib.RAPID_Core_CloudReplayStream_SetRetrieveErrorFunc(self._handle, None, None)
            return

        def wrapper(error_code, user_data):
            try:
                if callback:
                    callback(error_code)
            except:
                pass

        self._retrieve_error_callback = ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.c_void_p)(wrapper)
        lib.RAPID_Core_CloudReplayStream_SetRetrieveErrorFunc(self._handle, self._retrieve_error_callback, None)

    def enable_download_control(self, enable: bool):
        if not self._handle:
            return
        lib.RAPID_Core_CloudReplayStream_EnableDownloadControl(self._handle, 1 if enable else 0)

    def provider(self, index: int = 0) -> Optional[StreamProvider]:
        if not self._handle:
            return None
        provider_handle = lib.RAPID_Core_CloudReplayStream_IndexedProvider(self._handle, index)
        if not provider_handle:
            return None
        return StreamProvider(provider_handle)

    def _release(self) -> None:
        if self._handle:
            lib.RAPID_Core_CloudReplayStream_Release(self._handle)
            self._handle = None
            self._file_not_found_callback = None
            self._download_complete_callback = None
            self._retrieve_error_callback = None


class RelayStream:
    def __init__(self, device_id: Union[str, bytes]):
        device_id_bytes = device_id.encode('utf-8') if isinstance(device_id, str) else device_id
        self._handle = lib.RAPID_Core_RelayStream_Create(device_id_bytes)
        if not self._handle:
            raise RuntimeError("Failed to create relay stream")

    def __del__(self) -> None:
        self._release()

    def enqueue(self, packet: Packet) -> None:
        if not self._handle:
            return
        if not packet or not hasattr(packet, '_packet'):
            raise ValueError("Invalid packet provided")
        lib.RAPID_Core_RelayStream_Enqueue(self._handle, packet._packet)

    def provider(self, index: int = 0) -> Optional[StreamProvider]:
        if not self._handle:
            return None
        provider_handle = lib.RAPID_Core_RelayStream_IndexedProvider(self._handle, index)
        if not provider_handle:
            return None
        return StreamProvider(provider_handle)

    def _release(self) -> None:
        if self._handle:
            lib.RAPID_Core_RelayStream_Release(self._handle)
            self._handle = None


def enable_stream_debugging(enable: bool):
    lib.RAPID_Core_Stream_EnableDebugging(1 if enable else 0) 