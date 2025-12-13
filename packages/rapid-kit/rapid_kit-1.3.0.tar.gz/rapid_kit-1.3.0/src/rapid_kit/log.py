import ctypes
from typing import Optional, Callable
from .lib import get_lib

lib = get_lib()

RAPID_LOG_UNKNOWN = 0
RAPID_LOG_DEFAULT = 1
RAPID_LOG_VERBOSE = 2
RAPID_LOG_DEBUG = 3
RAPID_LOG_INFO = 4
RAPID_LOG_WARN = 5
RAPID_LOG_ERROR = 6
RAPID_LOG_FATAL = 7
RAPID_LOG_SILENT = 8

CONSOLE_LOGGING_CALLBACK = ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_void_p)

_console_logging_callback = None

lib.RAPID_Core_LeveledLoggingPrint.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p]
lib.RAPID_Core_LeveledLoggingPrint.restype = None

lib.RAPID_Core_LeveledLoggingPrintWithPrefix.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p]
lib.RAPID_Core_LeveledLoggingPrintWithPrefix.restype = None

lib.RAPID_Core_UploadLogging.argtypes = []
lib.RAPID_Core_UploadLogging.restype = ctypes.c_char_p

lib.RAPID_Core_ExportLogging.argtypes = []
lib.RAPID_Core_ExportLogging.restype = ctypes.c_char_p

lib.RAPID_Core_Logging_Flush.argtypes = []
lib.RAPID_Core_Logging_Flush.restype = None

lib.RAPID_Core_SetConsoleLoggingFunc.argtypes = [CONSOLE_LOGGING_CALLBACK]
lib.RAPID_Core_SetConsoleLoggingFunc.restype = None

lib.RAPID_Core_CleanExpiredLogs.argtypes = [ctypes.c_char_p]
lib.RAPID_Core_CleanExpiredLogs.restype = None

def leveled_logging_print(level, tag, message):
    tag_bytes = tag.encode('utf-8') if isinstance(tag, str) else tag
    message_bytes = message.encode('utf-8') if isinstance(message, str) else message
    lib.RAPID_Core_LeveledLoggingPrint(level, tag_bytes, message_bytes)

def leveled_logging_info(tag, message):
    leveled_logging_print(RAPID_LOG_INFO, tag, message)

def leveled_logging_error(tag, message):
    leveled_logging_print(RAPID_LOG_ERROR, tag, message)

def leveled_logging_print_with_prefix(prefix, level, tag, message):
    prefix_bytes = prefix.encode('utf-8') if isinstance(prefix, str) else prefix
    tag_bytes = tag.encode('utf-8') if isinstance(tag, str) else tag
    message_bytes = message.encode('utf-8') if isinstance(message, str) else message
    lib.RAPID_Core_LeveledLoggingPrintWithPrefix(prefix_bytes, level, tag_bytes, message_bytes)

def upload_logging():
    result = lib.RAPID_Core_UploadLogging()
    if result:
        return result.decode('utf-8')
    return None

def export_logging():
    result = lib.RAPID_Core_ExportLogging()
    if result:
        return result.decode('utf-8')
    return None

def flush_logging():
    lib.RAPID_Core_Logging_Flush()

def set_console_logging_listener(callback: Optional[Callable[[int, str, str], None]]):
    global _console_logging_callback

    if callback is None:
        _console_logging_callback = None
        lib.RAPID_Core_SetConsoleLoggingFunc(None)
        return

    def wrapper(level, tag, fmt, va_list_ptr):
        try:
            if callback:
                tag_str = tag.decode('utf-8') if tag else ""
                fmt_str = fmt.decode('utf-8') if fmt else ""
                callback(level, tag_str, fmt_str)
        except:
            pass

    _console_logging_callback = CONSOLE_LOGGING_CALLBACK(wrapper)
    lib.RAPID_Core_SetConsoleLoggingFunc(_console_logging_callback)

def clean_expired_logs(cache_directory: str):
    dir_bytes = cache_directory.encode('utf-8')
    lib.RAPID_Core_CleanExpiredLogs(dir_bytes) 