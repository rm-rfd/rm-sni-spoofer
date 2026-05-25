"""GUI package surface during the src migration."""

from importlib import import_module

__all__ = ["ControlPanel", "launch_gui"]


def __getattr__(name: str):
	if name in __all__:
		return getattr(import_module("src.gui.window"), name)
	raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__() -> list[str]:
	return sorted(__all__)

