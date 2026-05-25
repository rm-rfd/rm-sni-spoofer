"""Temporary shim for the planned src.core.config.profiles module."""

from src.core.config import app_config as _core_app_config

__all__ = [
    "XRAY_LOG_LEVELS",
    "XRAY_PROFILES_KEY",
    "XRAY_ACTIVE_PROFILE_ID_KEY",
    "GUI_EDITABLE_FIELDS",
    "build_xray_profile_record",
    "get_xray_profiles",
    "get_active_xray_profile",
    "get_active_xray_share_url",
    "replace_xray_profiles",
    "normalize_config",
    "normalize_xray_log_level",
    "resolve_connect_port",
]


def __getattr__(name: str):
    return getattr(_core_app_config, name)


def __dir__() -> list[str]:
    return sorted(set(__all__) | set(dir(_core_app_config)))
