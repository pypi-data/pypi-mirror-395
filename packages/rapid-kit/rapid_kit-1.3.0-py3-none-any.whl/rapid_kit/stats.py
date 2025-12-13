import ctypes
import json
from typing import Optional, List, Dict, Callable
from enum import IntEnum
from .lib import get_lib

lib = get_lib()

class StatsLevel(IntEnum):
    INFO = 0
    WARN = 1
    ERROR = 2

RAPID_Stats_LatestEventFunc = ctypes.CFUNCTYPE(None, ctypes.c_char_p, ctypes.c_void_p)

lib.RAPID_Stats_GetAllEvents.argtypes = [ctypes.c_char_p]
lib.RAPID_Stats_GetAllEvents.restype = ctypes.c_void_p

lib.RAPID_Stats_GetLatestEvent.argtypes = [ctypes.c_char_p]
lib.RAPID_Stats_GetLatestEvent.restype = ctypes.c_void_p

lib.RAPID_Stats_GetAllEventsAfterTs.argtypes = [ctypes.c_char_p, ctypes.c_longlong]
lib.RAPID_Stats_GetAllEventsAfterTs.restype = ctypes.c_void_p

lib.RAPID_Stats_GetRenderPerf.argtypes = [ctypes.c_char_p]
lib.RAPID_Stats_GetRenderPerf.restype = ctypes.c_void_p

lib.RAPID_Stats_SetLatestEventFunc.argtypes = [RAPID_Stats_LatestEventFunc, ctypes.c_void_p]
lib.RAPID_Stats_SetLatestEventFunc.restype = None

lib.RAPID_Stats_ClearEvents.argtypes = [ctypes.c_char_p]
lib.RAPID_Stats_ClearEvents.restype = None

lib.RAPID_Stats_FreeString.argtypes = [ctypes.c_void_p]
lib.RAPID_Stats_FreeString.restype = None


class Stats:
    _instance = None
    _event_callback = None
    _c_callback = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @staticmethod
    def _parse_and_free(ptr) -> Optional[List[Dict]]:
        if not ptr:
            return None
        try:
            c_str = ctypes.cast(ptr, ctypes.c_char_p)
            if not c_str.value:
                return None
            result = json.loads(c_str.value.decode('utf-8'))
            return result if isinstance(result, list) else [result]
        except (json.JSONDecodeError, UnicodeDecodeError):
            return None
        finally:
            lib.RAPID_Stats_FreeString(ptr)

    def get_all_events(self, device_id: str) -> Optional[List[Dict]]:
        device_id_bytes = device_id.encode('utf-8')
        json_str = lib.RAPID_Stats_GetAllEvents(device_id_bytes)
        return self._parse_and_free(json_str)

    def get_latest_event(self, device_id: str) -> Optional[Dict]:
        device_id_bytes = device_id.encode('utf-8')
        json_str = lib.RAPID_Stats_GetLatestEvent(device_id_bytes)
        result = self._parse_and_free(json_str)
        return result[0] if result else None

    def get_events_after(self, device_id: str, timestamp: int) -> Optional[List[Dict]]:
        device_id_bytes = device_id.encode('utf-8')
        json_str = lib.RAPID_Stats_GetAllEventsAfterTs(device_id_bytes, timestamp)
        return self._parse_and_free(json_str)

    def get_render_perf(self, device_id: str) -> Optional[Dict]:
        device_id_bytes = device_id.encode('utf-8')
        json_str = lib.RAPID_Stats_GetRenderPerf(device_id_bytes)
        result = self._parse_and_free(json_str)
        return result[0] if result else None

    def set_event_listener(self, callback: Optional[Callable[[Dict], None]]):
        if callback is None:
            Stats._event_callback = None
            Stats._c_callback = None
            lib.RAPID_Stats_SetLatestEventFunc(None, None)
            return

        def wrapper(event_json, user_data):
            try:
                if callback and event_json:
                    event = json.loads(event_json.decode('utf-8'))
                    callback(event)
            except:
                pass

        Stats._event_callback = callback
        Stats._c_callback = RAPID_Stats_LatestEventFunc(wrapper)
        lib.RAPID_Stats_SetLatestEventFunc(Stats._c_callback, None)

    def clear(self, device_id: str):
        device_id_bytes = device_id.encode('utf-8')
        lib.RAPID_Stats_ClearEvents(device_id_bytes)
