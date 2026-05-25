from src.core.config import app_config as _core_app_config

__all__ = [name for name in dir(_core_app_config) if not name.startswith("_")]


def __getattr__(name: str):
    return getattr(_core_app_config, name)


def __dir__() -> list[str]:
    return sorted(set(__all__) | set(dir(_core_app_config)))
