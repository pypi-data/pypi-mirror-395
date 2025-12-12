"""Common type definitions for the jbqt package"""

from typing import Protocol, Optional, runtime_checkable, Sequence
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtCore import QSize


@runtime_checkable
class IconGetter(Protocol):
    """Factory function that assembles a QIcon instance"""

    def __call__(
        self, color: Optional[str | QColor] = ..., size: QSize | int | None = ...
    ) -> QIcon: ...


MultiSelectData = (
    list[str] | Sequence[tuple[str, str] | tuple[str, str, bool]] | dict
)

__all__ = [
    "IconGetter",
    "MultiSelectData",
]
