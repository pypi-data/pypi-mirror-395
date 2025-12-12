from re import Pattern

from PyQt6.QtCore import QObject, pyqtSignal, Qt, QEvent
from PyQt6.QtGui import QCursor, QMouseEvent, QWheelEvent
from PyQt6.QtWidgets import QComboBox, QListWidget, QListWidgetItem, QLineEdit

from jbutils import jbutils
import jbqt.consts as consts
from jbqt.common import qt_utils
from jbqt.types import MultiSelectData


class MultiSelectComboBox(QComboBox):
    selectedChanged = pyqtSignal(list)

    def __init__(
        self,
        data: MultiSelectData | None = None,
        selected: list[str] | None = None,
        multi_enabled: bool = True,
        use_weight: bool = False,
        weight_re: Pattern | None = None,
    ):
        super().__init__()

        self.use_weight = use_weight
        if use_weight:
            weight_re = weight_re or consts.TAG_RE

        self.weight_re = weight_re

        self._multi_select_enabled: bool = multi_enabled
        # Make the combo box read-only and use a custom view
        self.setEditable(True)

        self.line_edit().setReadOnly(True)
        # Override the mouse press event of the QLineEdit
        self.line_edit().installEventFilter(self)

        self.view: QListWidget = QListWidget()  # type: ignore
        self._selected = selected or []

        # Set the custom view
        self.setModel(self.view.model())
        self.setView(self.view)

        # Add items and categories
        if isinstance(data, dict):
            for name, items in data.items():
                self.add_group(name, items)
        elif isinstance(data, list):
            self.add_items(data)

        # Connect the item clicked signal
        self.view.itemClicked.connect(self.toggle_check_state)
        self.update_display_text()

    def line_edit(self) -> QLineEdit:
        return self.lineEdit() or QLineEdit(parent=self)

    def eventFilter(
        self, a0: QObject | None, a1: QMouseEvent | QEvent | None
    ) -> bool:

        if (
            a0 == self.lineEdit()
            and isinstance(a1, QMouseEvent)
            and a1.type() == QMouseEvent.Type.MouseButtonRelease
        ):
            self.showPopup()

            return True
        return super().eventFilter(a0, a1)

    def wheelEvent(self, e: QWheelEvent | None):
        # Check if the mouse cursor is within the bounds of the line edit
        pos = self.mapFromGlobal(QCursor.pos())
        if self.line_edit().rect().contains(pos):
            # Consume the wheel event to prevent scrolling
            return

        # If not over the line edit, let the base class handle it (scrolling)
        super().wheelEvent(e)

    def toggle_check_state(self, item: QListWidgetItem):
        # Toggle check state if the item is selectable
        if item.flags() & Qt.ItemFlag.ItemIsUserCheckable:
            current_state = item.checkState()

            new_state = (
                Qt.CheckState.Unchecked
                if current_state == Qt.CheckState.Checked
                else Qt.CheckState.Checked
            )
            item.setCheckState(new_state)
            if not self._multi_select_enabled:
                self.toggle_others(item)

            self.update_display_text()
            self._selected_changed()

    def toggle_others(self, selected: QListWidgetItem) -> None:

        for i in range(self.view.count()):
            item = self.view.item(i)
            if item and item != selected:
                item.setCheckState(Qt.CheckState.Unchecked)
        self.update_display_text()

    def setMultiSelectEnabled(self, value: bool) -> None:
        self._multi_select_enabled = value

    def multiSelectEnabled(self) -> bool:
        return self._multi_select_enabled

    def add_items(self, items: MultiSelectData, indent: int = 0) -> None:

        indent_str = "    " * indent
        if isinstance(items, dict):
            for name, children in items.items():
                self.add_group(name, children, indent + 1)
        else:
            for item_value in items:
                disabled: bool = False
                if isinstance(item_value, tuple):
                    item = QListWidgetItem(f"{indent_str}{item_value[0]}")
                    item.setData(consts.LIST_ITEM_ROLE, item_value[1])
                    if len(item_value) > 2:
                        disabled = bool(item_value[2])
                else:
                    item = QListWidgetItem(f"{indent_str}{item_value}")

                qt_utils.set_item_disabled(item, disabled)

                value = item.data(consts.LIST_ITEM_ROLE) or item.text()
                if value.strip() in self._selected:
                    item.setCheckState(Qt.CheckState.Checked)
                else:
                    item.setCheckState(Qt.CheckState.Unchecked)
                self.view.addItem(item)

    def add_group(self, group_name: str, items: MultiSelectData, indent: int = 0):
        indent_str = "    " * indent
        # Add group header
        header_item = QListWidgetItem(indent_str + group_name)
        if isinstance(items, dict) and items.get("__disabled__", False) is True:
            header_item.setFlags(Qt.ItemFlag.NoItemFlags)
        else:
            header_item.setFlags(Qt.ItemFlag.ItemIsEnabled)
        header_item.setData(Qt.ItemDataRole.UserRole, False)  # Non-selectable
        self.view.addItem(header_item)

        # Add items with checkboxes
        self.add_items(items, indent + 1)

    def update_display_text(self):
        selected_items = []
        for i in range(self.view.count()):
            item = self.view.item(i)
            if item and item.checkState() == Qt.CheckState.Checked:
                selected_items.append(item.text().strip())

        text = ", ".join(selected_items)
        self.line_edit().setText(text)

    def showPopup(self):
        # Override showPopup to update text when the dropdown is shown
        self.update_display_text()
        super().showPopup()

    def hidePopup(self):
        # Override hidePopup to update text when closing dropdown
        self.update_display_text()
        super().hidePopup()

    def same_selected(self, values: list[str]) -> bool:
        return set(values) == set(self._selected)

    def get_selected(self) -> list[str]:
        return [
            qt_utils.get_item_value(item)
            for item in self.view.findItems("", Qt.MatchFlag.MatchContains)
            if item.checkState() == Qt.CheckState.Checked
        ]

    def _selected_changed(self):
        self.selectedChanged.emit(self.get_selected())

    def get_unweight_chip(self, tag: str) -> str:
        if self.weight_re:
            search_re = self.weight_re.search(tag)
            if search_re:
                return search_re.groups()[0]
        return tag

    def get_chip_list(self, tags: list[str]) -> list[str]:
        return [self.get_unweight_chip(tag) for tag in tags]

    def set_selected(self, values: list[str], emit: bool = True):
        """if self.same_selected(values):
        return"""

        values = self.get_chip_list(values)
        # Set the selected items and emit the signal
        self._selected = jbutils.dedupe_list(values)
        # Update the checked state of items based on the new selection
        for i in range(self.view.count()):
            item = self.view.item(i)
            if not item:
                continue

            item.setCheckState(
                Qt.CheckState.Checked
                if qt_utils.get_item_value(item) in values
                else Qt.CheckState.Unchecked
            )
        self.update_display_text()
        if emit:
            self._selected_changed()
