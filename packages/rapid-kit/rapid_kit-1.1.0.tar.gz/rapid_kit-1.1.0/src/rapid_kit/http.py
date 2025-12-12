import ctypes
from enum import IntEnum
from typing import Dict, Optional, Union, Any
from .lib import get_lib

lib = get_lib()

class HttpMethod(IntEnum):
    GET = 0
    POST = 1
    DELETE = 2
    PATCH = 3

class HttpResp(ctypes.Structure):
    _fields_ = [
        ("data", ctypes.c_char_p),
        ("success", ctypes.c_int),
        ("message", ctypes.c_char_p),
        ("code", ctypes.c_int)
    ]

lib.RAPID_Core_HttpRequest.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p]
lib.RAPID_Core_HttpRequest.restype = ctypes.POINTER(HttpResp)

lib.RAPID_Core_HttpResp_Free.argtypes = [ctypes.POINTER(HttpResp)]
lib.RAPID_Core_HttpResp_Free.restype = None

lib.RAPID_Core_Http_LoggingEnable.argtypes = [ctypes.c_int]
lib.RAPID_Core_Http_LoggingEnable.restype = None

def http_request(path: str, method: Union[HttpMethod, int], request_content: Optional[str] = None) -> Optional[Dict[str, Any]]:
    path_bytes = path.encode('utf-8') if isinstance(path, str) else path
    
    if request_content is not None:
        content_bytes = request_content.encode('utf-8') if isinstance(request_content, str) else request_content
    else:
        content_bytes = None
    
    if isinstance(method, HttpMethod):
        method_value = method.value
    else:
        method_value = method
    
    resp_ptr = lib.RAPID_Core_HttpRequest(path_bytes, method_value, content_bytes)
    
    if not resp_ptr:
        return None
    
    resp = resp_ptr.contents
    result = {
        'data': resp.data.decode('utf-8') if resp.data else None,
        'success': bool(resp.success),
        'message': resp.message.decode('utf-8') if resp.message else None,
        'code': resp.code
    }
    
    lib.RAPID_Core_HttpResp_Free(resp_ptr)
    return result

def http_get(path: str) -> Optional[Dict[str, Any]]:
    return http_request(path, HttpMethod.GET)

def http_post(path: str, content: str) -> Optional[Dict[str, Any]]:
    return http_request(path, HttpMethod.POST, content)

def http_delete(path: str, content: Optional[str] = None) -> Optional[Dict[str, Any]]:
    return http_request(path, HttpMethod.DELETE, content)

def http_patch(path: str, content: str) -> Optional[Dict[str, Any]]:
    return http_request(path, HttpMethod.PATCH, content)

def enable_http_logging(enable: bool = True) -> None:
    lib.RAPID_Core_Http_LoggingEnable(1 if enable else 0) 