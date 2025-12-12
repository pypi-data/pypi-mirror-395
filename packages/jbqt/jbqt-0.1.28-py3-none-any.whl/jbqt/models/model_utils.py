"""Collection of utility functions local to the models package"""

from jbutils import JbuConsole
from jbutils.types import Function
from rich import print

from jbqt.models.model_consts import RegisteredFunctions


def register_fct(name: str, fct: Function, override: bool = False) -> None:
    exists = name in RegisteredFunctions

    if not exists or override:
        RegisteredFunctions[name] = fct
        if exists:
            JbuConsole.warn(
                f"Function '{name}' already defined and was overwritten"
            )
    else:
        JbuConsole.warn(f"Function '{name}' already defined")


def get_fct(name: str, fallback: Function | None = None) -> Function | None:
    return RegisteredFunctions.get(name, fallback)


__all__ = ["register_fct", "get_fct"]
