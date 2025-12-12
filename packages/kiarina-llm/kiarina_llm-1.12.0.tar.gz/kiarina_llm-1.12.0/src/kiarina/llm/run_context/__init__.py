import logging
from importlib import import_module
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ._model import RunContext
    from ._registry import create_run_context
    from .settings import settings_manager

__all__ = [
    "create_run_context",
    "RunContext",
    "settings_manager",
]

logging.getLogger(__name__).addHandler(logging.NullHandler())


def __getattr__(name: str) -> object:
    if name not in __all__:
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

    module_map = {
        "create_run_context": "._registry",
        "RunContext": "._model",
        "settings_manager": ".settings",
    }

    globals()[name] = getattr(import_module(module_map[name], __name__), name)
    return globals()[name]
