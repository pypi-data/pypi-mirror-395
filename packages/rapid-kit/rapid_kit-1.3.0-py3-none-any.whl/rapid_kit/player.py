import ctypes
from enum import IntEnum
from typing import Optional, Callable, Union, Any, TYPE_CHECKING
from .lib import get_media_lib
from .stream import StreamProvider

lib = get_media_lib()

class VideoFrameToRender:
    def __init__(self, data: bytes, width: int, height: int, pixel_format: str):
        self.data = data
        self.width = width
        self.height = height
        self.pixel_format = pixel_format

class AudioFrameToRender:
    def __init__(self, data: bytes, sample_rate: int, channels: int, sample_format: str, samples: int):
        self.data = data
        self.sample_rate = sample_rate
        self.channels = channels
        self.sample_format = sample_format
        self.samples = samples

class MediaRenderState(IntEnum):
    UNKNOWN = -1
    STARTED = 0
    BUFFERING = 1
    COMPLETED = 2
    PAUSED = 3

UTS_CALLBACK = ctypes.CFUNCTYPE(None, ctypes.c_longlong, ctypes.c_void_p)
PTS_CALLBACK = ctypes.CFUNCTYPE(None, ctypes.c_longlong, ctypes.c_void_p)
STATE_CALLBACK = ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.c_void_p)
PIXEL_SIZE_CALLBACK = ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.c_int, ctypes.c_void_p)

lib.RAPID_MediaPlayer_Create.argtypes = []
lib.RAPID_MediaPlayer_Create.restype = ctypes.c_void_p

lib.RAPID_MediaPlayer_Prepare.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
lib.RAPID_MediaPlayer_Prepare.restype = None

lib.RAPID_MediaPlayer_Mute.argtypes = [ctypes.c_void_p, ctypes.c_int]
lib.RAPID_MediaPlayer_Mute.restype = None

lib.RAPID_MediaPlayer_IsMute.argtypes = [ctypes.c_void_p]
lib.RAPID_MediaPlayer_IsMute.restype = ctypes.c_int

lib.RAPID_MediaPlayer_Start.argtypes = [ctypes.c_void_p]
lib.RAPID_MediaPlayer_Start.restype = None

lib.RAPID_MediaPlayer_Pause.argtypes = [ctypes.c_void_p]
lib.RAPID_MediaPlayer_Pause.restype = None

lib.RAPID_MediaPlayer_Resume.argtypes = [ctypes.c_void_p]
lib.RAPID_MediaPlayer_Resume.restype = None

lib.RAPID_MediaPlayer_Stop.argtypes = [ctypes.c_void_p]
lib.RAPID_MediaPlayer_Stop.restype = None

lib.RAPID_MediaPlayer_State.argtypes = [ctypes.c_void_p]
lib.RAPID_MediaPlayer_State.restype = ctypes.c_int

lib.RAPID_MediaPlayer_Flush.argtypes = [ctypes.c_void_p]
lib.RAPID_MediaPlayer_Flush.restype = None

lib.RAPID_MediaPlayer_Destroy.argtypes = [ctypes.c_void_p]
lib.RAPID_MediaPlayer_Destroy.restype = None

lib.RAPID_MediaPlayer_BindPlayer.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
lib.RAPID_MediaPlayer_BindPlayer.restype = None

lib.RAPID_MediaPlayer_SetVout.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
lib.RAPID_MediaPlayer_SetVout.restype = None

lib.RAPID_MediaPlayer_SetAout.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
lib.RAPID_MediaPlayer_SetAout.restype = None

lib.RAPID_MediaPlayer_Capture.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
lib.RAPID_MediaPlayer_Capture.restype = ctypes.c_int

lib.RAPID_MediaPlayer_StartRecord.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
lib.RAPID_MediaPlayer_StartRecord.restype = ctypes.c_int

lib.RAPID_MediaPlayer_StopRecord.argtypes = [ctypes.c_void_p]
lib.RAPID_MediaPlayer_StopRecord.restype = ctypes.c_int

lib.RAPID_MediaPlayer_EnableBuffering.argtypes = [ctypes.c_void_p, ctypes.c_int]
lib.RAPID_MediaPlayer_EnableBuffering.restype = None

lib.RAPID_MediaPlayer_EnableAout.argtypes = [ctypes.c_void_p, ctypes.c_int]
lib.RAPID_MediaPlayer_EnableAout.restype = None

lib.RAPID_MediaPlayer_GetPixelWidth.argtypes = [ctypes.c_void_p]
lib.RAPID_MediaPlayer_GetPixelWidth.restype = ctypes.c_int

lib.RAPID_MediaPlayer_GetPixelHeight.argtypes = [ctypes.c_void_p]
lib.RAPID_MediaPlayer_GetPixelHeight.restype = ctypes.c_int

lib.RAPID_MediaPlayer_GetUts.argtypes = [ctypes.c_void_p]
lib.RAPID_MediaPlayer_GetUts.restype = ctypes.c_longlong

lib.RAPID_MediaPlayer_GetPts.argtypes = [ctypes.c_void_p]
lib.RAPID_MediaPlayer_GetPts.restype = ctypes.c_longlong

lib.RAPID_MediaPlayer_SetPtsFunc.argtypes = [ctypes.c_void_p, PTS_CALLBACK, ctypes.c_void_p]
lib.RAPID_MediaPlayer_SetPtsFunc.restype = None

lib.RAPID_MediaPlayer_SetUtsFunc.argtypes = [ctypes.c_void_p, UTS_CALLBACK, ctypes.c_void_p]
lib.RAPID_MediaPlayer_SetUtsFunc.restype = None

lib.RAPID_MediaPlayer_SetRenderStateFunc.argtypes = [ctypes.c_void_p, STATE_CALLBACK, ctypes.c_void_p]
lib.RAPID_MediaPlayer_SetRenderStateFunc.restype = None

lib.RAPID_MediaPlayer_SetOverloadWaterMark.argtypes = [ctypes.c_void_p, ctypes.c_int]
lib.RAPID_MediaPlayer_SetOverloadWaterMark.restype = None

lib.RAPID_MediaPlayer_SetWaterMark.argtypes = [ctypes.c_void_p, ctypes.c_int]
lib.RAPID_MediaPlayer_SetWaterMark.restype = None

lib.RAPID_MediaPlayer_GetMuxerQueueSize.argtypes = [ctypes.c_void_p]
lib.RAPID_MediaPlayer_GetMuxerQueueSize.restype = ctypes.c_longlong

lib.RAPID_Media_PixelFrame_Create.argtypes = []
lib.RAPID_Media_PixelFrame_Create.restype = ctypes.c_void_p

lib.RAPID_Media_PixelFrame_Free.argtypes = [ctypes.c_void_p]
lib.RAPID_Media_PixelFrame_Free.restype = None

lib.RAPID_MediaPlayer_GetPixelFrame.argtypes = [ctypes.c_void_p]
lib.RAPID_MediaPlayer_GetPixelFrame.restype = ctypes.c_void_p

lib.RAPID_MediaPlayer_SetPixelSizeFunc.argtypes = [ctypes.c_void_p, PIXEL_SIZE_CALLBACK, ctypes.c_void_p]
lib.RAPID_MediaPlayer_SetPixelSizeFunc.restype = None

lib.RAPID_MediaPlayer_GetMetricsJson.argtypes = [ctypes.c_void_p]
lib.RAPID_MediaPlayer_GetMetricsJson.restype = ctypes.c_void_p

lib.RAPID_MediaPlayer_FreeMetricsJson.argtypes = [ctypes.c_void_p]
lib.RAPID_MediaPlayer_FreeMetricsJson.restype = None

class PixelFrame:
    def __init__(self):
        self._handle = lib.RAPID_Media_PixelFrame_Create()
        if not self._handle:
            raise RuntimeError("Failed to create pixel frame")

    def __del__(self):
        if self._handle:
            lib.RAPID_Media_PixelFrame_Free(self._handle)
            self._handle = None

class MediaPlayer:
    def __init__(self):
        self._handle = lib.RAPID_MediaPlayer_Create()
        if not self._handle:
            raise RuntimeError("Failed to create media player")
        self._pts_callback = None
        self._uts_callback = None
        self._state_callback = None
        self._pixel_size_callback = None
        self._vout = None
        self._aout = None
        self._vout_callback = None
        self._aout_callback = None
        self._video_frame_handler: Optional[Callable[[VideoFrameToRender], None]] = None
        self._audio_frame_handler: Optional[Callable[[AudioFrameToRender], None]] = None
    
    def __del__(self) -> None:
        self._destroy()
    
    def prepare(self, provider: StreamProvider) -> None:
        if not self._handle:
            return
        
        provider_handle = provider._handle if hasattr(provider, '_handle') else provider
        lib.RAPID_MediaPlayer_Prepare(self._handle, provider_handle)
    
    def mute(self, mute: bool) -> None:
        if not self._handle:
            return
        
        lib.RAPID_MediaPlayer_Mute(self._handle, 1 if mute else 0)
    
    def is_mute(self) -> bool:
        if not self._handle:
            return False
        
        return lib.RAPID_MediaPlayer_IsMute(self._handle) != 0
    
    def start(self) -> None:
        if not self._handle:
            return
        
        lib.RAPID_MediaPlayer_Start(self._handle)
    
    def pause(self) -> None:
        if not self._handle:
            return
        
        lib.RAPID_MediaPlayer_Pause(self._handle)
    
    def resume(self) -> None:
        if not self._handle:
            return
        
        lib.RAPID_MediaPlayer_Resume(self._handle)
    
    def stop(self) -> None:
        if not self._handle:
            return

        lib.RAPID_MediaPlayer_Stop(self._handle)

    def state(self) -> MediaRenderState:
        if not self._handle:
            return MediaRenderState.UNKNOWN
        
        return MediaRenderState(lib.RAPID_MediaPlayer_State(self._handle))
    
    def flush(self) -> None:
        if not self._handle:
            return
        
        lib.RAPID_MediaPlayer_Flush(self._handle)
    
    def bind_player(self, main_player: 'MediaPlayer') -> None:
        if not self._handle:
            return
        
        main_handle = main_player._handle if hasattr(main_player, '_handle') else main_player
        lib.RAPID_MediaPlayer_BindPlayer(self._handle, main_handle)
    
    def set_vout(self, vout: ctypes.c_void_p) -> None:
        if not self._handle:
            return

        self._vout = vout
        vout_handle = vout._handle if hasattr(vout, '_handle') else vout
        lib.RAPID_MediaPlayer_SetVout(self._handle, vout_handle)

    def set_aout(self, aout: ctypes.c_void_p) -> None:
        if not self._handle:
            return

        self._aout = aout
        aout_handle = aout._handle if hasattr(aout, '_handle') else aout
        lib.RAPID_MediaPlayer_SetAout(self._handle, aout_handle)
    
    def capture(self, path: str) -> bool:
        if not self._handle:
            return False
        
        path_bytes = path.encode('utf-8')
        return lib.RAPID_MediaPlayer_Capture(self._handle, path_bytes) == 1
    
    def start_record(self, path: str) -> bool:
        if not self._handle:
            return False
        
        path_bytes = path.encode('utf-8')
        return lib.RAPID_MediaPlayer_StartRecord(self._handle, path_bytes) == 1
    
    def stop_record(self) -> bool:
        if not self._handle:
            return False
        
        return lib.RAPID_MediaPlayer_StopRecord(self._handle) == 1
    
    def enable_buffering(self, enable: bool = True) -> None:
        if not self._handle:
            return
        
        lib.RAPID_MediaPlayer_EnableBuffering(self._handle, 1 if enable else 0)
    
    def enable_aout(self, enable: bool = True) -> None:
        if not self._handle:
            return
        
        lib.RAPID_MediaPlayer_EnableAout(self._handle, 1 if enable else 0)
    
    def pixel_width(self) -> int:
        if not self._handle:
            return 0
        
        return lib.RAPID_MediaPlayer_GetPixelWidth(self._handle)
    
    def pixel_height(self) -> int:
        if not self._handle:
            return 0
        
        return lib.RAPID_MediaPlayer_GetPixelHeight(self._handle)
    
    def get_uts(self) -> int:
        if not self._handle:
            return 0
        
        return lib.RAPID_MediaPlayer_GetUts(self._handle)
    
    def get_pts(self) -> int:
        if not self._handle:
            return 0
        
        return lib.RAPID_MediaPlayer_GetPts(self._handle)
    
    def set_pts_callback(self, callback: Callable[[int], None]) -> None:
        if not self._handle:
            return
        
        def wrapper(pts, user_data):
            try:
                if callback:
                    callback(pts)
            except:
                pass
        
        self._pts_callback = PTS_CALLBACK(wrapper)
        lib.RAPID_MediaPlayer_SetPtsFunc(self._handle, self._pts_callback, None)
    
    def set_uts_callback(self, callback: Callable[[int], None]) -> None:
        if not self._handle:
            return
        
        def wrapper(uts, user_data):
            try:
                if callback:
                    callback(uts)
            except:
                pass
        
        self._uts_callback = UTS_CALLBACK(wrapper)
        lib.RAPID_MediaPlayer_SetUtsFunc(self._handle, self._uts_callback, None)
    
    def listen(self, callback: Callable[[MediaRenderState], None]) -> None:
        if not self._handle:
            return

        def wrapper(state, user_data):
            try:
                if callback:
                    callback(MediaRenderState(state))
            except:
                pass

        self._state_callback = STATE_CALLBACK(wrapper)
        lib.RAPID_MediaPlayer_SetRenderStateFunc(self._handle, self._state_callback, None)

    def set_overload_watermark(self, value: int) -> None:
        if not self._handle:
            return
        lib.RAPID_MediaPlayer_SetOverloadWaterMark(self._handle, value)

    def set_watermark(self, value: int) -> None:
        if not self._handle:
            return
        lib.RAPID_MediaPlayer_SetWaterMark(self._handle, value)

    @property
    def muxer_queue_size(self) -> int:
        if not self._handle:
            return 0
        return lib.RAPID_MediaPlayer_GetMuxerQueueSize(self._handle)

    def get_pixel_frame(self) -> Optional[PixelFrame]:
        if not self._handle:
            return None
        frame_handle = lib.RAPID_MediaPlayer_GetPixelFrame(self._handle)
        if not frame_handle:
            return None
        frame = PixelFrame.__new__(PixelFrame)
        frame._handle = frame_handle
        return frame

    def set_pixel_size_listener(self, callback: Optional[Callable[[int, int], None]]) -> None:
        if not self._handle:
            return

        if callback is None:
            self._pixel_size_callback = None
            lib.RAPID_MediaPlayer_SetPixelSizeFunc(self._handle, None, None)
            return

        def wrapper(width, height, user_data):
            try:
                if callback:
                    callback(width, height)
            except:
                pass

        self._pixel_size_callback = PIXEL_SIZE_CALLBACK(wrapper)
        lib.RAPID_MediaPlayer_SetPixelSizeFunc(self._handle, self._pixel_size_callback, None)

    def get_metrics_json(self) -> Optional[str]:
        if not self._handle:
            return None

        ptr = lib.RAPID_MediaPlayer_GetMetricsJson(self._handle)
        if not ptr:
            return None

        try:
            c_str = ctypes.cast(ptr, ctypes.c_char_p)
            if not c_str.value:
                return None
            return c_str.value.decode("utf-8")
        finally:
            lib.RAPID_MediaPlayer_FreeMetricsJson(ptr)

    def listen_video_frame_to_render(self, handler: Optional[Callable[[VideoFrameToRender], None]]) -> None:
        self._video_frame_handler = handler

        if handler is not None and self._vout is None:
            from . import sdl

            def wrapper(frame):
                if self._video_frame_handler is not None:
                    self._video_frame_handler(frame)

            vout, callback = sdl._create_vout_with_frame_bridge(wrapper)
            self._vout_callback = callback
            self.set_vout(vout)

    def listen_audio_frame_to_render(self, handler: Optional[Callable[[AudioFrameToRender], None]]) -> None:
        self._audio_frame_handler = handler

        if handler is not None and self._aout is None:
            from . import sdl

            def wrapper(frame):
                if self._audio_frame_handler is not None:
                    self._audio_frame_handler(frame)

            aout, callback = sdl._create_aout_with_frame_bridge(wrapper)
            self._aout_callback = callback
            self.set_aout(aout)

    def _destroy(self) -> None:
        if self._handle:
            lib.RAPID_MediaPlayer_Destroy(self._handle)
            self._handle = None
            self._pts_callback = None
            self._uts_callback = None
            self._state_callback = None
            self._pixel_size_callback = None
            self._vout = None
            self._aout = None
            self._vout_callback = None
            self._aout_callback = None 