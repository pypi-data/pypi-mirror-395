from dataclasses import dataclass

from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QWidget, QMainWindow, QApplication, QDialog


@dataclass
class DialogOptions:
    title: str = ""
    x_pos: int | None = None
    y_pos: int | None = None
    height: int | None = None
    width: int | None = None

    def apply(self, q_obj: QWidget | QMainWindow | QDialog):
        if self.title:
            q_obj.setWindowTitle(self.title)

        h, w, x, y = self.height, self.width, self.x_pos, self.y_pos
        if h or w:
            h = h or 400
            w = w or 400
            q_obj.resize(w, h)

        if x is not None or y is not None:
            x = x or 0
            y = y or 0
            q_obj.move(x, y)
