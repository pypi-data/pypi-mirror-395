from dataclasses import dataclass
from typing import Any, Callable

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QHBoxLayout,
    QLabel,
    QLayout,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from PyQt6 import QtWidgets

from jbqt.models import DialogOptions


def get_widget(name: str) -> QWidget | None:
    widget: QWidget | None = None
    if hasattr(QtWidgets, name):
        widget = getattr(QtWidgets, name)
    """ elif hasattr(widgets, name):
        widget = getattr(widgets, name) """

    if widget:
        if not callable(widget):
            return

        widget = widget()
        if isinstance(widget, QWidget):
            return widget
    return None


def get_widget_val(widget: QWidget) -> str | int | float | None:
    # Emit the custom signal with data when the dialog is accepted
    value = None
    if isinstance(widget, QLineEdit):
        value = widget.text()
    elif isinstance(widget, QSpinBox):
        value = widget.value()
    elif isinstance(widget, QDoubleSpinBox):
        value = widget.value()

    return value


class InputFormDialog(QDialog):
    """reference value for external use"""

    value = pyqtSignal(dict)

    def __init__(
        self,
        parent=None,
        form_data: list[dict] | None = None,
        opts: DialogOptions | None = None,
    ):
        super().__init__(parent)

        opts = opts or DialogOptions(title="Input")
        opts.apply(self)

        self.form_data: list[dict] = [obj.copy() for obj in form_data or []]
        self.input_widgets: dict[str, QWidget] = {}

        self.main_layout = QVBoxLayout()
        self.construct_widgets()

        button_box = QHBoxLayout()
        submit_btn = QPushButton("Submit", parent=self)
        submit_btn.clicked.connect(self.submit)

        cancel_btn = QPushButton("Cancel", parent=self)
        cancel_btn.clicked.connect(self.close)

        button_box.addWidget(submit_btn)
        button_box.addWidget(cancel_btn)
        self.main_layout.addLayout(button_box)

        self.setLayout(self.main_layout)

    def construct_widgets(self) -> None:
        for widget_def in self.form_data:
            if not "type" in widget_def:
                continue

            layout = QHBoxLayout()

            w_type = widget_def.pop("type")
            label = widget_def.pop("label", "")
            key = widget_def.pop("key", "")
            if not key:
                continue

            widget = get_widget(w_type)
            if not widget:
                continue
            if label and isinstance(label, str):
                layout.addWidget(QLabel(label))

            if widget_def:
                self._init_widget(widget, **widget_def)
            layout.addWidget(widget)
            self.main_layout.addLayout(layout)
            self.input_widgets[key] = widget

    def get_form_data(self) -> dict:
        form_values: dict[str, Any] = {}

        for key, widget in self.input_widgets.items():
            value = get_widget_val(widget)
            if value:
                form_values[key] = value

        return form_values

    def submit(self) -> None:
        form_data = self.get_form_data()
        self.value.emit(form_data)
        self.close()

    def close(self) -> bool:
        self.deleteLater()

        return super().close()

    def _init_widget(self, widget: QWidget, **opts) -> None:
        for key, value in opts.items():
            setter_key = f"set{key[0].upper() + key[1:]}"
            if hasattr(widget, setter_key):
                setter = getattr(widget, setter_key)
                if setter:
                    setter(value)
