from typing import Any, Callable

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QLabel,
    QLineEdit,
    QSpinBox,
    QVBoxLayout,
)


INPUT_SIGNAL_TYPES: tuple[Any, ...] = (str, int, float)


class InputDialog(QDialog):
    signal_types: tuple[Any] = INPUT_SIGNAL_TYPES
    """ reference value for external use """

    value = pyqtSignal(*([ptype] for ptype in INPUT_SIGNAL_TYPES))

    def __init__(
        self,
        parent=None,
        title: str = "Input",
        msg_str: str = "Enter Input:",
        input_type: type = str,
        **opts,
    ):
        super().__init__(parent)

        self.setWindowTitle(title)

        QBtn = (
            QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.Open
        )

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()
        message = QLabel(msg_str)
        layout.addWidget(message)

        self.input_widget = None
        if input_type is str:
            self.input_widget = QLineEdit()
        elif input_type is int:
            self.input_widget = QSpinBox()
        elif input_type is float:
            self.input_widget = QDoubleSpinBox()

        self._init_widget(**opts)

        layout.addWidget(self.input_widget)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

    def _init_widget(self, **opts) -> None:
        for key, value in opts.items():
            setter_key = f"set{key[0].upper() + key[1:]}"
            if hasattr(self.input_widget, setter_key):
                setter = getattr(self.input_widget, setter_key)
                if setter:
                    setter(value)

    def connect(self, callback: Callable) -> None:
        for parm_type in self.signal_types:
            self.value[parm_type].connect(callback)

    def accept(self):
        # Emit the custom signal with data when the dialog is accepted

        if isinstance(self.input_widget, QLineEdit):
            self.value[str].emit(self.input_widget.text())
        elif isinstance(self.input_widget, QSpinBox):
            self.value[int].emit(self.input_widget.value())
        elif isinstance(self.input_widget, QDoubleSpinBox):
            self.value[float].emit(self.input_widget.value())

        super().accept()
