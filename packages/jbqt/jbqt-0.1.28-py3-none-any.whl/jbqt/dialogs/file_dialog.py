from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QFileDialog


class JbFileDialog(QWidget):
    """A simple widget that opens a file dialog in either 'open' or 'save' mode.

    Emits:
        selectedFile (str): Emitted when a file path is chosen.

    Args:
        title (str): The dialog window title.
        directory (str): The starting directory.
        mode (str): 'open' to open an existing file, 'save' to choose a save location.
    """

    selectedFile = pyqtSignal(str)

    def __init__(
        self, title: str = "File Dialog", directory: str = "", mode: str = "open"
    ) -> None:
        super().__init__()

        self.title = title
        self.directory = directory
        self.mode = mode.lower()

        if self.mode not in {"open", "save"}:
            raise ValueError("mode must be either 'open' or 'save'")

        self.setWindowTitle(title)

        self.button = QPushButton(
            "Open File" if self.mode == "open" else "Save File", self
        )
        self.button.clicked.connect(self.open_file_dialog)

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)

    def open_file_dialog(self) -> None:
        """Open a file dialog based on the selected mode."""
        if self.mode == "open":
            file_name, _ = QFileDialog.getOpenFileName(
                self,
                self.title,
                self.directory,
                "All Files (*);;Text Files (*.txt)",
            )
        else:
            file_name, _ = QFileDialog.getSaveFileName(
                self,
                self.title,
                self.directory,
                "All Files (*);;Text Files (*.txt)",
            )

        if file_name:
            self.selectedFile.emit(file_name)
