import re

from PyQt6.QtCore import pyqtSignal, Qt, QObject, QEvent
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import QLabel, QLineEdit

NUM_RE = re.compile(r"^[-0-9]\d*$")


class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def mousePressEvent(self, ev):
        self.clicked.emit()
        super().mousePressEvent(ev)


def is_valid_key(event: QKeyEvent) -> bool:
    if event.key() in [
        Qt.Key.Key_0,
        Qt.Key.Key_1,
        Qt.Key.Key_2,
        Qt.Key.Key_3,
        Qt.Key.Key_4,
        Qt.Key.Key_5,
        Qt.Key.Key_6,
        Qt.Key.Key_7,
        Qt.Key.Key_8,
        Qt.Key.Key_9,
        Qt.Key.Key_Backspace,
    ]:
        return True

    if event.keyCombination().keyboardModifiers().name == "ControlModifier":
        return True
    return False


class LongIntSpinBox(QLineEdit):
    valueChanged = pyqtSignal(int)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.installEventFilter(self)
        self._value = 0
        self.textChanged.connect(self.update_value)

    def update_value(self, *_) -> None:
        self.valueChanged.emit(self.value())

    def setValue(self, value: int) -> None:
        if value != self.value():
            self.setText(str(value))

    def value(self) -> int | None:
        text = self.text()
        if NUM_RE.match(text):
            return int(text)

    def eventFilter(
        self, a0: QObject | None, a1: QKeyEvent | QEvent | None
    ) -> bool:
        if isinstance(a1, QKeyEvent):
            if a1.type() == QEvent.Type.KeyPress:
                if not is_valid_key(a1):
                    return True
        return super().eventFilter(a0, a1)
