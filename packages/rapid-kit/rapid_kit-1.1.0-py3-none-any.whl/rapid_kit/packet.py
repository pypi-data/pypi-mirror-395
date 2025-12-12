import ctypes
from enum import IntEnum
from .lib import get_lib

lib = get_lib()

class StreamCodecID(IntEnum):
    CODEC_UNKNOWN = 0x00
    CODEC_AVC = 0x4E
    CODEC_HEVC = 0x50
    CODEC_MJPEG = 0x4F
    CODEC_G711A = 0x8A
    CODEC_END = 0x100
    CODEC_SPEED = 0x102
    CODEC_SPECIAL = 0x200

class StreamPacket(ctypes.Structure):
    _fields_ = [
        ("buffer", ctypes.c_char_p),
        ("codec_id", ctypes.c_int32),
        ("sub_type", ctypes.c_int32),
        ("frame_type", ctypes.c_int32),
        ("buffer_size", ctypes.c_int32),
        ("seq_no", ctypes.c_int32),
        ("ts", ctypes.c_int64),
        ("utc_ts", ctypes.c_int64),
        ("final_packet", ctypes.c_int8),
        ("speed_packet", ctypes.c_int8),
        ("speed", ctypes.c_int8)
    ]

lib.RAPID_Core_StreamPacket_Create_From_Buffer.argtypes = [ctypes.c_char_p, ctypes.c_int32]
lib.RAPID_Core_StreamPacket_Create_From_Buffer.restype = ctypes.POINTER(StreamPacket)

lib.RAPID_Core_StreamPacket_Create.argtypes = []
lib.RAPID_Core_StreamPacket_Create.restype = ctypes.POINTER(StreamPacket)

lib.RAPID_Core_StreamPacket_Copy.argtypes = [ctypes.POINTER(StreamPacket)]
lib.RAPID_Core_StreamPacket_Copy.restype = ctypes.POINTER(StreamPacket)

lib.RAPID_Core_StreamPacket_Free.argtypes = [ctypes.POINTER(StreamPacket)]
lib.RAPID_Core_StreamPacket_Free.restype = None

lib.RAPID_Core_StreamPacket_Fill.argtypes = [ctypes.POINTER(StreamPacket), ctypes.c_char_p, ctypes.c_int32]
lib.RAPID_Core_StreamPacket_Fill.restype = None

class Packet:
    def __init__(self):
        self._handle = lib.RAPID_Core_StreamPacket_Create()
        if not self._handle:
            raise RuntimeError("Failed to create packet")
    
    def __del__(self):
        self.free()
    
    @classmethod
    def create_from_buffer(cls, buffer):
        instance = cls.__new__(cls)
        buffer_bytes = buffer if isinstance(buffer, bytes) else bytes(buffer)
        instance._handle = lib.RAPID_Core_StreamPacket_Create_From_Buffer(buffer_bytes, len(buffer_bytes))
        if not instance._handle:
            raise RuntimeError("Failed to create packet from buffer")
        return instance
    
    @classmethod
    def create_copy(cls, packet):
        if not isinstance(packet, Packet) or not packet._handle:
            raise ValueError("Invalid packet to copy")
        
        instance = cls.__new__(cls)
        instance._handle = lib.RAPID_Core_StreamPacket_Copy(packet._handle)
        if not instance._handle:
            raise RuntimeError("Failed to copy packet")
        return instance
    
    @classmethod
    def _from_handle(cls, handle):
        instance = cls.__new__(cls)
        instance._handle = ctypes.cast(handle, ctypes.POINTER(StreamPacket))
        return instance
    
    def fill(self, buffer):
        if not self._handle:
            return
        
        buffer_bytes = buffer if isinstance(buffer, bytes) else bytes(buffer)
        lib.RAPID_Core_StreamPacket_Fill(self._handle, buffer_bytes, len(buffer_bytes))
    
    def free(self):
        if self._handle:
            lib.RAPID_Core_StreamPacket_Free(self._handle)
            self._handle = None
    
    def get_native_handle(self):
        return self._handle
    
    def is_video_packet(self):
        return self.codec_id == StreamCodecID.CODEC_AVC or self.codec_id == StreamCodecID.CODEC_HEVC
    
    def is_audio_packet(self):
        return self.codec_id == StreamCodecID.CODEC_G711A
    
    @property
    def buffer(self):
        if not self._handle or not self._handle.contents.buffer or self._handle.contents.buffer_size <= 0:
            return None
        
        buffer = (ctypes.c_char * self._handle.contents.buffer_size).from_address(ctypes.addressof(self._handle.contents.buffer.contents))
        return bytes(buffer)
    
    @property
    def codec_id(self):
        if not self._handle:
            return StreamCodecID.CODEC_UNKNOWN
        return self._handle.contents.codec_id
    
    @codec_id.setter
    def codec_id(self, value):
        if not self._handle:
            return
        self._handle.contents.codec_id = value
    
    @property
    def sub_type(self):
        if not self._handle:
            return 0
        return self._handle.contents.sub_type
    
    @sub_type.setter
    def sub_type(self, value):
        if not self._handle:
            return
        self._handle.contents.sub_type = value
    
    @property
    def frame_type(self):
        if not self._handle:
            return 0
        return self._handle.contents.frame_type
    
    @frame_type.setter
    def frame_type(self, value):
        if not self._handle:
            return
        self._handle.contents.frame_type = value
    
    @property
    def buffer_size(self):
        if not self._handle:
            return 0
        return self._handle.contents.buffer_size
    
    @property
    def seq_no(self):
        if not self._handle:
            return 0
        return self._handle.contents.seq_no
    
    @seq_no.setter
    def seq_no(self, value):
        if not self._handle:
            return
        self._handle.contents.seq_no = value
    
    @property
    def timestamp(self):
        if not self._handle:
            return 0
        return self._handle.contents.ts
    
    @timestamp.setter
    def timestamp(self, value):
        if not self._handle:
            return
        self._handle.contents.ts = value
    
    @property
    def utc_timestamp(self):
        if not self._handle:
            return 0
        return self._handle.contents.utc_ts
    
    @utc_timestamp.setter
    def utc_timestamp(self, value):
        if not self._handle:
            return
        self._handle.contents.utc_ts = value
    
    @property
    def final_packet(self):
        if not self._handle:
            return False
        return bool(self._handle.contents.final_packet)
    
    @final_packet.setter
    def final_packet(self, value):
        if not self._handle:
            return
        self._handle.contents.final_packet = 1 if value else 0
    
    @property
    def speed_packet(self):
        if not self._handle:
            return False
        return bool(self._handle.contents.speed_packet)
    
    @speed_packet.setter
    def speed_packet(self, value):
        if not self._handle:
            return
        self._handle.contents.speed_packet = 1 if value else 0
    
    @property
    def speed(self):
        if not self._handle:
            return 0
        return self._handle.contents.speed
    
    @speed.setter
    def speed(self, value):
        if not self._handle:
            return
        self._handle.contents.speed = value 