from re import Pattern
from typing import Callable

from PyQt6.QtCore import Qt, QEvent, QObject
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QFrame,
    QWidget,
)

import jbqt.consts as consts
from jbconsts import STYLES, COLORS
from jbqt.models import IChipButton
from jbqt.widgets.simple import ClickableLabel
from jbqt.dialogs import InputDialog
from jbqt.widgets.widget_utils import (
    preserve_scroll,
)


class ChipButton(IChipButton):
    def __init__(
        self,
        tag: str,
        on_update: Callable,
        on_remove: Callable,
        use_weight: bool = False,
        weight_re: Pattern | None = None,
    ):
        super().__init__()

        self._tag: str = tag
        self.weight: float = 1.0
        self.use_weight: bool = use_weight

        if use_weight:
            weight_re = weight_re or consts.TAG_RE

        if weight_re:
            tag_match = weight_re.search(tag)

            if tag_match:
                re_tag, weight = tag_match.groups()
                self._tag = re_tag
                self.weight = float(weight)

        self.on_update = on_update
        self.on_remove = on_remove
        self.installEventFilter(self)

        # Layout for the tag button
        # self.frame = QFrame(self, Qt.WindowType.ToolTip)
        self.frame = QFrame()
        frame_layout = QHBoxLayout(self.frame)
        frame_layout.setSpacing(5)
        frame_layout.setContentsMargins(10, 0, 10, 0)

        self.tag_label = ClickableLabel(tag)
        self.tag_label.setFixedHeight(24)
        self.tag_label.clicked.connect(self.toggle_edit_mode)

        self.weight_button: QPushButton | None = None

        if use_weight:
            self.weight_button = QPushButton(consts.ICONS.CODE(), "")
            self.weight_button.clicked.connect(self.apply_weight)
            self.weight_button.setFixedWidth(24)

        self.remove_button = QPushButton(consts.ICONS.TRASH(), "")
        self.remove_button.clicked.connect(lambda: self.on_remove(self))
        self.remove_button.setFixedWidth(24)
        self.remove_button.setStyleSheet(STYLES.BG_DARK_RED)

        self.edit_line = QLineEdit(self)
        self.edit_line.hide()

        self.confirm_btn = QPushButton(consts.ICONS.CIRCLE_CHECK(COLORS.WHITE), "")
        self.confirm_btn.clicked.connect(self.edit_tag)
        self.confirm_btn.setFixedWidth(24)
        self.confirm_btn.setStyleSheet(STYLES.BG_DARK_GREEN)
        self.confirm_btn.hide()

        self.cancel_btn = QPushButton(consts.ICONS.CIRCLE_TIMES(), "")
        self.cancel_btn.clicked.connect(self.cancel)
        self.cancel_btn.setFixedWidth(24)
        self.cancel_btn.setStyleSheet(STYLES.BG_DARK_RED)
        self.cancel_btn.hide()

        self.widgets = [
            self.tag_label,
            self.edit_line,
            self.confirm_btn,
            self.cancel_btn,
            self.weight_button,
            self.remove_button,
        ]
        self.input_widgets = [self.edit_line, self.confirm_btn, self.cancel_btn]
        for widget in self.widgets:
            if widget:
                frame_layout.addWidget(widget)

        # Main layout
        self.main_layout = QHBoxLayout(self)
        self.main_layout.addWidget(self.frame)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        # Apply styling to the frame
        self.frame.setStyleSheet(
            f"""
            QFrame {{
                border: 1px solid #AAA;
                border-radius: 10px;
                background-color: #343439;
                max-height: 36px;
            }}
            QLabel {{
                border: none;
            }}
            QPushButton {{
                {STYLES.BG_GRAY}   
            }}
        """
        )
        self.setLayout(self.main_layout)

    @property
    def text(self) -> str:
        if self.weight == 1:
            return self._tag
        return f"({self._tag}){self.weight:g}"

    @text.setter
    def text(self, value: str) -> None:
        self._tag = value

    def eventFilter(
        self, a0: QObject | None, a1: QKeyEvent | QEvent | None
    ) -> bool:
        focus: QWidget | None = None

        if consts.QtGlobalRefs.app:
            focus = consts.QtGlobalRefs.app.focusWidget()

        if not a1 or not isinstance(a1, QKeyEvent):
            return super().eventFilter(a0, a1)

        if a1.type() == QEvent.Type.KeyPress and focus == self.edit_line:
            match a1.key():
                case Qt.Key.Key_Return | Qt.Key.Key_Enter:
                    self.edit_tag()
                case Qt.Key.Key_Escape:
                    self.cancel()
        return super().eventFilter(a0, a1)

    def toggle_hidden(self, hide: bool = True) -> None:
        for widget in self.widgets:
            if widget:
                is_input = widget in self.input_widgets

                if hide == is_input:
                    widget.hide()
                else:
                    widget.show()

    def cancel(self) -> None:
        self.toggle_hidden()

    def toggle_edit_mode(self):
        self.edit_line.setText(self._tag)
        self.edit_line.setMinimumWidth(self.tag_label.width() + 10)
        self.toggle_hidden(False)

    def emit_update(
        self, text: str | None = None, weight: float | None = None
    ) -> None:
        text = text or self._tag
        if weight is None:
            weight = self.weight
        if weight == "":
            self.on_remove(self)
            return
        prev_text = self.text
        self._tag = text
        self.weight = weight
        self.tag_label.setText(self.text)
        self.on_update(prev_text, self.text)

    def update_weight(self, weight: float) -> None:
        self.emit_update(weight=weight)

    @preserve_scroll
    def edit_tag(self, *_):
        text = self.edit_line.text()
        self.toggle_hidden()

        self.emit_update(text=text)

    def apply_weight(self):
        weight_dialog = InputDialog(
            parent=self,
            title="Tag Weight",
            msg_str=f"Enter weight for `{self.text}`:",
            input_type=float,
            minimum=0,
            maximum=2,
            singleStep=0.1,
            value=self.weight,
        )
        weight_dialog.connect(self.update_weight)
        weight_dialog.exec()
