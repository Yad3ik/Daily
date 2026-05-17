from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QColor, QPainter, QPen
from PyQt5.QtWidgets import QFrame


class CheckSquareIcon(QFrame):
    def __init__(self, size: int = 30, active: bool = False) -> None:
        super().__init__()
        self._active = active
        self.setFixedSize(size, size)

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        color = QColor("#F03F83") if self._active else QColor("#c8b6e2")
        pen = QPen(color, 2.0 if self.width() < 24 else 2.4)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        m = 2.0 if self.width() < 24 else 3.0
        side = self.width() - 2 * m
        painter.drawRoundedRect(QRectF(m, m, side, side), 4, 4)
        if self.width() >= 24:
            painter.drawLine(9, 16, 13, 20)
            painter.drawLine(13, 20, 22, 11)
        else:
            painter.drawLine(5, 9, 7, 11)
            painter.drawLine(7, 11, 13, 5)


class CalendarNavIcon(QFrame):
    def __init__(self, size: int = 18, active: bool = False) -> None:
        super().__init__()
        self._active = active
        self.setFixedSize(size, size)

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        color = QColor("#F03F83") if self._active else QColor("#9c95a1")
        pen = QPen(color, 1.6)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(2, 4, 14, 12, 2, 2)
        painter.drawLine(2, 8, 16, 8)
        for x in (6, 10, 14):
            painter.drawLine(x, 11, x, 14)
