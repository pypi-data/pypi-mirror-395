from re import Pattern

from PyQt6.QtCore import Qt, pyqtSignal, QObject, QEvent
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
    QComboBox,
)

from jbutils import jbutils

import jbqt.consts as consts

from jbqt.models import IChipsWidget
from jbqt.widgets.chip_button import ChipButton
from jbqt.widgets.multiselect import MultiSelectComboBox


class ChipsWidget(IChipsWidget):
    valuesChanged = pyqtSignal(list)

    def __init__(
        self,
        chips: list[str] | None = None,
        data: dict | list | None = None,
        path: str = "",
        label: str = "",
        weight_re: Pattern | None = None,
        use_weight: bool = False,
        debug: bool = False,
    ):
        super().__init__()
        self.values: list[str] = chips or []
        # Main layout
        main_layout = QVBoxLayout()
        self.debug = debug
        if label:
            main_layout.addWidget(QLabel(label))
        self.installEventFilter(self)

        self.use_weight = use_weight
        if use_weight:
            weight_re = weight_re or consts.TAG_RE

        self.weight_re = weight_re
        self.options = data or {}
        self.data = data or {}
        self.data_path = path
        self.list_widget: QComboBox | MultiSelectComboBox | None = None

        if data is not None:
            if isinstance(data, dict):
                if path:
                    self.options = jbutils.get_nested(self.data, path, [])

                self.list_widget = MultiSelectComboBox(
                    data=self.options, selected=self.values
                )
                self.list_widget.selectedChanged.connect(
                    self.handle_multiselect_change
                )

            elif isinstance(data, list):
                self.list_widget = QComboBox()

                # self.list_widget.addItems(self.options)
                for option in self.options:
                    self.list_widget.addItem(option)
                init_value = self.values[0] if self.values else ""
                self.list_widget.setCurrentText(init_value)
                self.list_widget.currentTextChanged.connect(
                    self.handle_multiselect_change
                )
            self.valuesChanged.connect(self.update_multiselect)
            main_layout.addWidget(self.list_widget)

        # Scroll area for the chips
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Widget inside the scroll area to hold the buttons
        self.chip_widget = QWidget()
        self.chip_layout = QHBoxLayout(self.chip_widget)
        self.chip_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Add existing chips as buttons
        self.set_items(emit=False)

        scroll_area.setWidget(self.chip_widget)

        # Layout for the input and add button
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit(self)
        self.add_button = QPushButton("Add", self)
        self.add_button.clicked.connect(self.parse_chip_input)

        self.clear_button = QPushButton(consts.ICONS.TRASH("darkred"), "", self)
        self.clear_button.clicked.connect(self.remove_all)
        # self.clear_button.setStyleSheet("color: red")

        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.add_button)
        input_layout.addWidget(self.clear_button)

        main_layout.addWidget(scroll_area)
        main_layout.addLayout(input_layout)

        self.setLayout(main_layout)

    def eventFilter(
        self, a0: QObject | None, a1: QKeyEvent | QEvent | None
    ) -> bool:
        focus: QWidget | None = None
        if consts.QtGlobalRefs.app:
            focus = consts.QtGlobalRefs.app.focusWidget()

        if not a1 or not isinstance(a1, QKeyEvent):
            return super().eventFilter(a0, a1)

        if a1.type() == QEvent.Type.KeyPress and focus == self.input_field:
            match a1.key():
                case Qt.Key.Key_Return | Qt.Key.Key_Enter:
                    self.parse_chip_input()
        return super().eventFilter(a0, a1)

    def get_unweight_chip(self, tag: str) -> str:
        if self.weight_re:
            search_re = self.weight_re.search(tag)
            if search_re:
                return search_re.groups()[0]

        return tag

    def get_chip_list(self, tags: list[str] | None = None) -> list[str]:
        tags = tags or []
        return [self.get_unweight_chip(tag) for tag in tags]

    def same_values(self, values: list[str]) -> bool:
        return set(self.get_chip_list(values)) == set(
            self.get_chip_list(self.values)
        )

    def handle_multiselect_change(self, selections: list[str] | str) -> None:
        if isinstance(selections, str):
            selections = [selections]

        selections = jbutils.dedupe_list(selections)
        if self.same_values(selections):
            return

        # self.values = selections
        self.set_items(selections, debug=True)

    def update_multiselect(self, values: list[str]) -> None:
        if not self.list_widget:
            return

        if isinstance(self.list_widget, MultiSelectComboBox):
            self.list_widget.set_selected(values, emit=False)
        else:
            value = values[0] if values else ""
            self.list_widget.setCurrentText(value)

    def clear_widgets(self) -> None:
        while self.chip_layout.count():
            layout = self.chip_layout.takeAt(0)
            if not layout:
                return

            widget = layout.widget()

            if widget is not None:
                widget.deleteLater()

    def set_items(
        self,
        values: list[str] | None = None,
        emit: bool = True,
        debug: bool = False,
    ) -> None:
        self.clear_widgets()
        if self.values is None:
            self.values = []
        # TODO: Temp fix for weighted/custom tags and incoming multiselect values
        if values:
            tags = self.get_chip_list(self.values)
            for value in values:
                if value not in tags:
                    self.values.append(value)

            self.values = jbutils.dedupe_list(self.values)
        self.values = [value for value in self.values if value]
        for item in self.values:
            if not consts.QtGlobalRefs.debug_set:
                debug = True
                consts.QtGlobalRefs.debug_set = True
            else:
                debug = False
            chip_button = ChipButton(
                item,
                self.update_chip,
                self.remove_chip,
                weight_re=self.weight_re,
                use_weight=self.use_weight,
            )

            self.chip_layout.addWidget(chip_button)

        if emit:
            self.emit_changes()

    def update_chip(self, prev_text: str, new_text: str) -> None:
        idx = self.values.index(prev_text)
        if idx >= 0:
            self.values[idx] = new_text

    def emit_changes(self):
        self.valuesChanged.emit(self.values)

    def parse_chip_input(self) -> None:
        text = self.input_field.text().strip()
        if "," in text:
            self.add_chips(jbutils.parse_csv_line(text))
        else:
            self.add_chip()
        self.input_field.setText("")

    def add_chip(self):
        text = self.input_field.text().strip()

        if text and text not in self.values:
            chip_button = ChipButton(text, self.update_chip, self.remove_chip)

            self.chip_layout.addWidget(chip_button)
            self.values.append(text)
            self.emit_changes()

    def remove_chip(self, button: ChipButton):  # type: ignore
        self.chip_layout.removeWidget(button)
        button.deleteLater()  # Schedule button widget for deletion
        self.values.remove(button.text)
        self.emit_changes()

    def add_chips(self, items: list[str]) -> None:
        jbutils.update_list_values(self.values, items)
        self.set_items()

    def remove_chips(self, items: list[str]) -> None:
        jbutils.remove_list_values(self.values, items)
        self.set_items()

    def remove_all(self, *_) -> None:
        self.values.clear()
        self.clear_widgets()
        self.emit_changes()
