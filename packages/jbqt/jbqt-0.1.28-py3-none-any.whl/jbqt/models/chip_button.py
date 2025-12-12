"""Model for chips widget"""

from PyQt6.QtWidgets import QWidget


class IChipButton(QWidget):
    """ChipButton model"""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
