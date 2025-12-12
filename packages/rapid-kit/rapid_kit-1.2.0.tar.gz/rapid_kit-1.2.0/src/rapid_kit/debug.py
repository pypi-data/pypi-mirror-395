import ctypes
from .lib import get_lib
from .auth import RAPID_Core_AuthResp

lib = get_lib()

lib.RAPID_Core_DebuggingCode_Create.argtypes = []
lib.RAPID_Core_DebuggingCode_Create.restype = ctypes.c_char_p

lib.RAPID_Core_DebuggingCode_Free.argtypes = [ctypes.c_char_p]
lib.RAPID_Core_DebuggingCode_Free.restype = None

lib.RAPID_Core_DebuggingCode_Apply.argtypes = [ctypes.c_char_p]
lib.RAPID_Core_DebuggingCode_Apply.restype = ctypes.POINTER(RAPID_Core_AuthResp)

lib.RAPID_Core_AuthResp_Free.argtypes = [ctypes.POINTER(RAPID_Core_AuthResp)]
lib.RAPID_Core_AuthResp_Free.restype = None

lib.RAPID_Core_CheckInternetConnectivity.argtypes = []
lib.RAPID_Core_CheckInternetConnectivity.restype = ctypes.c_int

def create_debugging_code():
    code = lib.RAPID_Core_DebuggingCode_Create()
    if not code:
        return None
    
    result = code.decode('utf-8')
    return result

def apply_debugging_code(code):
    if not code:
        return None
    
    code_bytes = code.encode('utf-8')
    resp_ptr = lib.RAPID_Core_DebuggingCode_Apply(code_bytes)
    
    if not resp_ptr:
        return None
    
    try:
        resp = resp_ptr.contents

        result = {
            "user_id": resp.user_id,
            "issue_at": resp.issue_at,
            "expires_in": resp.expires_in,
            "success": resp.success != 0,
            "message": resp.message.decode('utf-8') if resp.message else None,
            "code": resp.code
        }
        return result
    finally:
        lib.RAPID_Core_AuthResp_Free(resp_ptr)

def check_internet_connectivity() -> bool:
    return lib.RAPID_Core_CheckInternetConnectivity() != 0 