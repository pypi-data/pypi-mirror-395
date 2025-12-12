from PyQt6.QtGui import QFontMetrics
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QTextEdit,
    QPushButton,
)


class TextPreviewDialog(QDialog):
    def __init__(self, text: str, title: str = "", parent=None):
        super().__init__(parent)

        self.setWindowTitle("Text Preview")
        if title:
            self.setWindowTitle(f"Text Preview [{title}]")

        layout = QVBoxLayout(self)

        # QTextEdit to display the text
        self.text_edit = QTextEdit(self)
        self.text_edit.setPlainText(text)
        self.text_edit.setReadOnly(True)
        layout.addWidget(self.text_edit)

        # Close button
        close_button = QPushButton("Close", self)
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)

        # Adjust the dialog size based on the text
        self.adjust_size_based_on_text(text)

    def adjust_size_based_on_text(self, text):
        # Calculate text size
        font_metrics = QFontMetrics(self.text_edit.font())
        text_size = font_metrics.size(0, text)

        # Adjust size with some padding
        h_padding = 20
        v_padding = 100
        self.resize(text_size.width() + h_padding, text_size.height() + v_padding)
