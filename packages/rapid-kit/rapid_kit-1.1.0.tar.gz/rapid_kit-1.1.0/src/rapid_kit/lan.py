import ctypes
import json
from .lib import get_lib

lib = get_lib()

lib.RAPID_Core_LocalNetwork_SetBroadcastAddress.argtypes = [ctypes.c_char_p]
lib.RAPID_Core_LocalNetwork_SetBroadcastAddress.restype = None

lib.RAPID_Core_LanScanner_Create.argtypes = []
lib.RAPID_Core_LanScanner_Create.restype = ctypes.c_void_p

lib.RAPID_Core_LanScanner_Destroy.argtypes = [ctypes.c_void_p]
lib.RAPID_Core_LanScanner_Destroy.restype = None

lib.RAPID_Core_LanScanner_FoundDevices.argtypes = [ctypes.c_void_p]
lib.RAPID_Core_LanScanner_FoundDevices.restype = ctypes.c_char_p

lib.RAPID_Core_LanScanner_Start.argtypes = [ctypes.c_void_p]
lib.RAPID_Core_LanScanner_Start.restype = None

lib.RAPID_Core_LanScanner_Stop.argtypes = [ctypes.c_void_p]
lib.RAPID_Core_LanScanner_Stop.restype = None

def set_broadcast_address(address):
    if address:
        address_bytes = address.encode('utf-8') if isinstance(address, str) else address
        lib.RAPID_Core_LocalNetwork_SetBroadcastAddress(address_bytes)

class LanScanner:
    def __init__(self):
        self._handle = lib.RAPID_Core_LanScanner_Create()
        if not self._handle:
            raise RuntimeError("Failed to create LAN scanner")
    
    def __del__(self):
        self.close()
    
    def start(self):
        if self._handle:
            lib.RAPID_Core_LanScanner_Start(self._handle)
    
    def stop(self):
        if self._handle:
            lib.RAPID_Core_LanScanner_Stop(self._handle)
    
    def get_found_devices(self):
        if not self._handle:
            return []
        
        devices_json = lib.RAPID_Core_LanScanner_FoundDevices(self._handle)
        if not devices_json:
            return []
        
        try:
            devices_str = devices_json.decode('utf-8')
            return json.loads(devices_str)
        except:
            return []
    
    def close(self):
        if self._handle:
            self.stop()
            lib.RAPID_Core_LanScanner_Destroy(self._handle)
            self._handle = None 