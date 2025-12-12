from datetime import date
from typing import Any

from jbutils import JbuConsole
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtWidgets import (
    QListWidgetItem,
    QCalendarWidget,
    QApplication,
    QWidget,
    QLineEdit,
    QTextEdit,
    QSpinBox,
    QCheckBox,
    QDoubleSpinBox,
)

import jbqt.consts as consts
from jbqt.models import IChipsWidget


def get_item_value(item: QListWidgetItem) -> str:
    """Retrieves the value from a list widget item

    Args:
        item (QListWidgetItem): Item object to retrieve data from

    Returns:
        str: Value contained in the item
    """

    value = item.data(consts.LIST_ITEM_ROLE) or item.text()
    return value.strip()


def register_app(app: QApplication, icon_dir: str = "") -> None:
    """Registers the PyQt app with the JbQt global config reference

    Args:
        app (QApplication): The PyQt application
        icon_dir (str, optional): Directory containing custom icons. Defaults to "".
    """

    consts.QtGlobalRefs.app = app
    consts.set_icon_dir(icon_dir)


def get_widget_value(widget: QWidget, key: str = "") -> Any:
    """Convenience function to retrieve the value from a variety of
        common widgets

    Args:
        widget (QWidget): Widget to get the value from
        key (str, optional): A key to retrieve a specific value for
            certain widget types. Defaults to "".

    Returns:
        Any: Value contained in the widget, if any.
    """

    if isinstance(widget, QLineEdit):
        return widget.text()
    if isinstance(widget, QTextEdit):
        return widget.toPlainText().strip()
    if isinstance(widget, (QSpinBox, QDoubleSpinBox)):
        return widget.value()
    if isinstance(widget, IChipsWidget):
        return widget.values
    if isinstance(widget, QCheckBox):
        return widget.checkState == Qt.CheckState.Checked
    if isinstance(widget, QCalendarWidget):
        return widget.selectedDate().toString()

    JbuConsole.warn(f"No handler defined for {key} of type `{type(widget)}`")


def set_widget_value(widget: QWidget, value: Any) -> None:
    """Set the value of a one of variety of common widgets

    Currently Supported Widgets:
    - QLineEdit
    - QTextEdit
    - QSpinBox
    - QDoubleSpinBox
    - ChipsWidget
    - QCheckBox
    - QCalendarWidget

    Args:
        widget (QWidget): Widget to assign value to
        value (Any): Value to assign it
    """

    if isinstance(widget, (QLineEdit, QTextEdit)):
        widget.setText(str(value))
    elif isinstance(widget, QSpinBox):
        try:
            widget.setValue(int(value))
        except Exception as e:
            print(e)
            print(type(e))

    elif isinstance(widget, QDoubleSpinBox):
        try:
            widget.setValue(float(value))
        except Exception as e:
            print(e)
            print(type(e))

    elif isinstance(widget, IChipsWidget) and isinstance(value, list):
        widget.add_chips(value)
    elif isinstance(widget, QCheckBox):
        state = Qt.CheckState.Unchecked
        if isinstance(value, Qt.CheckState):
            state = value
        elif value is True:
            state = Qt.CheckState.Checked
        elif value is False:
            state = Qt.CheckState.Unchecked

        widget.setCheckState(state)

    elif isinstance(widget, QCalendarWidget):
        if isinstance(value, (date, QDate)):
            widget.setSelectedDate(value)


def set_item_disabled(item: QListWidgetItem, disabled: bool = True) -> None:
    if disabled:
        item.setFlags(Qt.ItemFlag.NoItemFlags)
        item.setCheckState(Qt.CheckState.Unchecked)
    else:
        item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
