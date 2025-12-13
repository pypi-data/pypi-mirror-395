import ctypes
from .lib import get_lib

lib = get_lib()

class RAPID_Core_AuthResp(ctypes.Structure):
    _fields_ = [
        ("user_id", ctypes.c_int),
        ("issue_at", ctypes.c_int),
        ("expires_in", ctypes.c_int),
        ("success", ctypes.c_int),
        ("message", ctypes.c_char_p),
        ("code", ctypes.c_int)
    ]

lib.RAPID_Core_Authenticate.argtypes = [ctypes.c_char_p]
lib.RAPID_Core_Authenticate.restype = ctypes.POINTER(RAPID_Core_AuthResp)

lib.RAPID_Core_AuthResp_Free.argtypes = [ctypes.POINTER(RAPID_Core_AuthResp)]
lib.RAPID_Core_AuthResp_Free.restype = None

def authenticate(access_token):
    if not access_token:
        return None
    
    token_bytes = access_token.encode('utf-8') if isinstance(access_token, str) else access_token
    resp_ptr = lib.RAPID_Core_Authenticate(token_bytes)
    
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