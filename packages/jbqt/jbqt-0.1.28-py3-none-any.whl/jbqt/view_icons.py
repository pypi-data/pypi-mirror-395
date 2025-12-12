import argparse
import os
import sys

from PyQt6.QtCore import QSize, Qt, QTimer
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QStyle,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from fuzzywuzzy import process  # Needs fuzzywuzzy + python-Levenshtein

parser = argparse.ArgumentParser(description="Simple tool to display icons")
parser.add_argument(
    "--from-theme",
    "-f",
    action="store_true",
    help="Search and display all icons from the Ubuntu themes as opposed to the StandardIcon library in Qt6",
)
parser.add_argument(
    "--theme-icons",
    "-t",
    action="store_true",
    help="Pull icons from the QIcon.ThemeIcon list",
)
parser.add_argument(
    "--add-quotes",
    "-q",
    action="store_true",
    help="Wrap copied icon name with quotes",
)
args = parser.parse_args()

THEMES_DIR = "/usr/share/icons"


# TODO: fix type checking
class Toast(QLabel):
    def __init__(self, text: str, parent: QWidget = None, duration_ms: int = 1500):  # type: ignore
        super().__init__(parent)

        self.setText(text)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet(
            """
            background-color: rgba(50, 50, 50, 180);
            color: white;
            border-radius: 8px;
            padding: 8px 16px;
            font-size: 14px;
        """
        )
        self.setWindowFlags(Qt.WindowType.ToolTip)
        self.adjustSize()

        # Center it over parent if available
        if parent:
            parent_rect = parent.rect()
            toast_rect = self.rect()
            self.move(
                parent_rect.center().x() - toast_rect.width() // 2,
                parent_rect.top() + 50,  # appear slightly under the top
            )

        QTimer.singleShot(duration_ms, self.close)


def get_theme_icons(theme_dir: str) -> list[str]:
    icon_names = set()
    for root, _, files in os.walk(theme_dir):
        for file in files:
            if file.endswith((".svg", ".png")):
                rel_path = os.path.relpath(os.path.join(root, file), theme_dir)
                parts = rel_path.split(os.sep)
                if len(parts) >= 2:
                    icon_name = os.path.splitext(parts[-1])[0]
                    icon_names.add(icon_name)
    return sorted(icon_names)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(1000, 400, 1600, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.layout = QVBoxLayout()  # type: ignore
        central_widget.setLayout(self.layout)  # type: ignore

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search icons...")
        self.search_bar.textChanged.connect(self.update_display)

        self.table = QTableWidget()
        self.table.setColumnCount(4)  # 4 columns of icons
        self.table.horizontalHeader().setVisible(False)  # type: ignore
        self.table.verticalHeader().setVisible(False)  # type: ignore
        self.table.setIconSize(QSize(64, 64))
        self.table.setShowGrid(False)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.table.cellClicked.connect(self.copy_icon_name_to_clipboard)
        self.table.setStyleSheet(
            """
        QTableWidget::item:hover {
            background-color: #444444;
        }
        """
        )

        self.layout.addWidget(self.search_bar)  # type: ignore
        self.layout.addWidget(self.table)  # type: ignore

        cur_theme = QIcon.themeName()
        self.icon_src = "standard"
        if args.from_theme:
            self.icon_src = "from_theme"
        elif args.theme_icons:
            self.icon_src = "theme_icons"

        match self.icon_src:
            case "from_theme":
                self.icons = get_theme_icons(os.path.join(THEMES_DIR, cur_theme))
            case "theme_icons":
                self.icons = [
                    i for i in dir(QIcon.ThemeIcon) if not i.startswith("_")
                ]
            case _:
                self.icons = sorted(
                    [
                        attr
                        for attr in dir(QStyle.StandardPixmap)
                        if attr.startswith("SP_")
                    ]
                )

        self.update_display()

    def copy_icon_name_to_clipboard(self, row: int, column: int) -> None:
        item = self.table.item(row, column)
        if item and item.text():
            text = f'"{item.text()}"' if args.add_quotes else item.text()
            QApplication.clipboard().setText(text)  # type: ignore
            print(f"Copied '{item.text()}' to clipboard")
            Toast(f"Copied '{item.text()}'", parent=self).show()

    def update_display(self):
        text = self.search_bar.text().strip()

        if text:
            # Use fuzzy matching
            matches = process.extract(
                text,
                self.icons,
                limit=200,  # Don't explode the table even if 2400+ icons exist
            )
            filtered_icons = [match[0] for match in matches if match[1] >= 50]
        else:
            filtered_icons = self.icons

        self.table.setRowCount((len(filtered_icons) + 3) // 4)

        for i in range(self.table.rowCount()):
            for j in range(4):
                idx = i * 4 + j
                if idx >= len(filtered_icons):
                    self.table.setItem(i, j, QTableWidgetItem())
                    continue

                name = filtered_icons[idx]

                match self.icon_src:
                    case "from_theme":
                        icon = QIcon.fromTheme(name)
                    case "theme_icons":
                        icon = QIcon.fromTheme(getattr(QIcon.ThemeIcon, name))
                    case _:

                        pixmapi = getattr(QStyle.StandardPixmap, name)
                        icon = self.style().standardIcon(pixmapi)  # type: ignore

                item = QTableWidgetItem(name)
                item.setIcon(icon)
                self.table.setItem(i, j, item)

        self.table.resizeRowsToContents()
        self.table.resizeColumnsToContents()


app = QApplication(sys.argv)
w = Window()
w.show()

app.exec()
