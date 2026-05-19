"""Кольцевой индикатор прогресса задач."""

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPainter, QPen
from PyQt5.QtWidgets import QFrame, QLabel


class ProgressRing(QFrame):
    """Круг: доля выполненных задач и подпись «done / total»."""

    def __init__(self) -> None:
        """Фиксированный размер 72×72 и центральная подпись."""
        super().__init__()
        self.setObjectName("progressRing")
        self.setFixedSize(72, 72)
        self._done = 0
        self._total = 0

        self._label = QLabel("0 / 0", self)
        self._label.setObjectName("progressText")
        self._label.setAlignment(Qt.AlignCenter)
        self._label.setAttribute(Qt.WA_TransparentForMouseEvents)

    def set_values(self, done: int, total: int) -> None:
        """Задаёт числа и перерисовывает дугу."""
        self._done = done
        self._total = max(total, 1)
        self._label.setText(f"{done} / {total}")
        self.update()
        self._label.setGeometry(0, 0, self.width(), self.height())

    def resizeEvent(self, event) -> None:
        """Центрирует текст в кольце."""
        super().resizeEvent(event)
        self._label.setGeometry(0, 0, self.width(), self.height())

    def paintEvent(self, event) -> None:
        """Рисует трек и розовую дугу прогресса."""
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect().adjusted(6, 6, -6, -6)

        track = QPen(QColor("#2a2530"), 6)
        track.setCapStyle(Qt.RoundCap)
        painter.setPen(track)
        painter.drawArc(rect, 0, 360 * 16)

        ratio = self._done / self._total if self._total else 0
        span = int(-360 * 16 * ratio)
        accent = QPen(QColor("#F03F83"), 6)
        accent.setCapStyle(Qt.RoundCap)
        painter.setPen(accent)
        painter.drawArc(rect, 90 * 16, span)
