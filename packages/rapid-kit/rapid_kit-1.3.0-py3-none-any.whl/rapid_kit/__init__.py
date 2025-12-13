"""
RAPID Kit Python SDK
"""
from importlib import import_module

__version__ = "1.3.0"

__all__ = [
    # Core functionalities
    "initialize",
    "version_name",
    "build_id",
    "commit_hash",
    "app_id",
    "package_name",
    "authenticate",
    # HTTP related
    "HttpMethod",
    "http_request",
    "http_get",
    "http_post",
    "http_delete",
    "http_patch",
    "enable_http_logging",
    # Media playback
    "MediaPlayer",
    "MediaRenderState",
    "PixelFrame",
    "VideoFrameToRender",
    "AudioFrameToRender",
    "MediaChat",
    "MediaChatAudioSampleRate",
    "MediaCapture",
    "MediaCaptureState",
    # Communication and streams
    "ChatChannel",
    "LiveStream",
    "LocalReplayStream",
    "CloudReplayStream",
    "StreamProvider",
    "RelayStream",
    "enable_stream_debugging",
    "Packet",
    "StreamCodecID",
    "Pipe",
    "PipeState",
    # Stats and monitoring
    "Stats",
    "PersistentChannel",
    "PersistentChannelState",
    # Profile and provisioning
    "BindingProfile",
    "ProfileTransmitter",
    "ProfileTransmitterState",
    # Logging
    "leveled_logging_info",
    "leveled_logging_error",
    "leveled_logging_print_with_prefix",
    "upload_logging",
    "export_logging",
    "flush_logging",
    "set_console_logging_listener",
    "clean_expired_logs",
    "RAPID_LOG_VERBOSE",
    "RAPID_LOG_DEBUG",
    "RAPID_LOG_INFO",
    "RAPID_LOG_WARN",
    "RAPID_LOG_ERROR",
    "RAPID_LOG_FATAL",
    # Debugging and diagnostics
    "create_debugging_code",
    "apply_debugging_code",
    "check_internet_connectivity",
    "InstructStandard",
    "register_signal_handler",
    "get_previous_crash_detail",
    "set_unauthorized_handler",
]


_lazy_attrs = {
    # Core
    "initialize": ("initialize", "initialize"),
    "version_name": ("initialize", "version_name"),
    "build_id": ("initialize", "build_id"),
    "commit_hash": ("initialize", "commit_hash"),
    "app_id": ("initialize", "app_id"),
    "package_name": ("initialize", "package_name"),
    # Auth
    "authenticate": ("auth", "authenticate"),
    # HTTP
    "HttpMethod": ("http", "HttpMethod"),
    "http_request": ("http", "http_request"),
    "http_get": ("http", "http_get"),
    "http_post": ("http", "http_post"),
    "http_delete": ("http", "http_delete"),
    "http_patch": ("http", "http_patch"),
    "enable_http_logging": ("http", "enable_http_logging"),
    # Media playback
    "MediaPlayer": ("player", "MediaPlayer"),
    "MediaRenderState": ("player", "MediaRenderState"),
    "PixelFrame": ("player", "PixelFrame"),
    "VideoFrameToRender": ("player", "VideoFrameToRender"),
    "AudioFrameToRender": ("player", "AudioFrameToRender"),
    "MediaChat": ("media_chat", "MediaChat"),
    "MediaChatAudioSampleRate": ("media_chat", "MediaChatAudioSampleRate"),
    "MediaCapture": ("capture", "MediaCapture"),
    "MediaCaptureState": ("capture", "MediaCaptureState"),
    # Communication and streams
    "ChatChannel": ("chat_channel", "ChatChannel"),
    "LiveStream": ("stream", "LiveStream"),
    "LocalReplayStream": ("stream", "LocalReplayStream"),
    "CloudReplayStream": ("stream", "CloudReplayStream"),
    "StreamProvider": ("stream", "StreamProvider"),
    "RelayStream": ("stream", "RelayStream"),
    "enable_stream_debugging": ("stream", "enable_stream_debugging"),
    "Packet": ("packet", "Packet"),
    "StreamCodecID": ("packet", "StreamCodecID"),
    "Pipe": ("pipe", "Pipe"),
    "PipeState": ("pipe", "PipeState"),
    # Stats and monitoring
    "Stats": ("stats", "Stats"),
    "PersistentChannel": ("persistent_channel", "PersistentChannel"),
    "PersistentChannelState": ("persistent_channel", "PersistentChannelState"),
    # Profile and provisioning
    "BindingProfile": ("profile", "BindingProfile"),
    "ProfileTransmitter": ("profile", "ProfileTransmitter"),
    "ProfileTransmitterState": ("profile", "ProfileTransmitterState"),
    # Logging
    "leveled_logging_info": ("log", "leveled_logging_info"),
    "leveled_logging_error": ("log", "leveled_logging_error"),
    "leveled_logging_print_with_prefix": ("log", "leveled_logging_print_with_prefix"),
    "upload_logging": ("log", "upload_logging"),
    "export_logging": ("log", "export_logging"),
    "flush_logging": ("log", "flush_logging"),
    "set_console_logging_listener": ("log", "set_console_logging_listener"),
    "clean_expired_logs": ("log", "clean_expired_logs"),
    "RAPID_LOG_VERBOSE": ("log", "RAPID_LOG_VERBOSE"),
    "RAPID_LOG_DEBUG": ("log", "RAPID_LOG_DEBUG"),
    "RAPID_LOG_INFO": ("log", "RAPID_LOG_INFO"),
    "RAPID_LOG_WARN": ("log", "RAPID_LOG_WARN"),
    "RAPID_LOG_ERROR": ("log", "RAPID_LOG_ERROR"),
    "RAPID_LOG_FATAL": ("log", "RAPID_LOG_FATAL"),
    # Debugging and diagnostics
    "create_debugging_code": ("debug", "create_debugging_code"),
    "apply_debugging_code": ("debug", "apply_debugging_code"),
    "check_internet_connectivity": ("debug", "check_internet_connectivity"),
    "InstructStandard": ("instruct", "InstructStandard"),
    "register_signal_handler": ("signal", "register_signal_handler"),
    "get_previous_crash_detail": ("signal", "get_previous_crash_detail"),
    "set_unauthorized_handler": ("unauthorized", "set_unauthorized_handler"),
}


def __getattr__(name):
    if name in _lazy_attrs:
        module_name, attr_name = _lazy_attrs[name]
        module = import_module(f".{module_name}", __name__)
        value = getattr(module, attr_name)
        globals()[name] = value
        return value
    raise AttributeError(f"module {__name__} has no attribute {name}")
