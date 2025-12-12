from PyQt6.QtCore import Qt, QTimer, QRect
from PyQt6.QtWidgets import QLabel


class Toast(QLabel):
    def __init__(self, message, duration=2000):
        super().__init__(message)

        # Set the basic appearance
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.ToolTip
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.setStyleSheet(
            "background-color: black; color: white; padding: 10px; border-radius: 5px;"
        )
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Set the duration for the toast
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.hide)
        self.timer.setInterval(duration)

    def show_toast(self, parent):
        self.setParent(parent)
        self.adjustSize()

        # Center the toast in the parent widget
        parent_rect: QRect = parent.rect()
        move_point = parent_rect.center() - self.rect().center()
        move_point.setY(20)
        self.move(move_point)
        # self.move((parent_rect.center() / 2) - self.rect().center())
        self.show()
        self.timer.start()
