"""Collection of models for PyQt6"""

from collections.abc import Callable
from dataclasses import dataclass

from PyQt6.QtCore import QSize, QObject
from PyQt6.QtGui import QIcon, QColor, QAction

from jbconsts import COLORS
from jbutils.models import Base

from jbqt.consts import ICONS, QtIconSizes
from jbqt.models import model_utils


@dataclass
class ToolbarButton(Base):
    name: str = ""
    icon: QIcon | str = ""
    color: QColor | str = COLORS.BLUE_GRAY
    checkable: bool = False
    checked: bool = False
    status_tip: str = ""
    size: QSize | str = QtIconSizes.ICON_MD
    function: Callable[..., None] | str | None = None
    text: str = ""

    def __post_init__(self) -> None:
        if isinstance(self.function, str):
            fct = model_utils.get_fct(self.function)
            print("fct:", fct)
            self.function = fct if fct else None

    def to_action(self, parent: QObject | None = None) -> QAction:
        color: QColor | str = self.color
        if isinstance(color, str):
            color = COLORS.get(color, color)

        size = self.size
        if isinstance(size, str):
            size = QtIconSizes.get(size)

        icon = self.icon
        if isinstance(icon, str):
            icon_getter = ICONS.get(icon)
            if callable(icon_getter):
                icon = icon_getter(color, size)

            icon = QIcon() if isinstance(icon, str) else icon

        action = QAction(icon=icon, text=self.text, parent=parent)
        if self.checkable:
            action.setCheckable(True)
            action.setChecked(self.checkable)
        if self.status_tip:
            action.setStatusTip(self.status_tip)
        if self.function:
            action.triggered.connect(self.function)

        return action
