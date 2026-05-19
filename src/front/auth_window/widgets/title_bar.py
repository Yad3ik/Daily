"""Title bar окна авторизации (своя копия виджетов)."""

from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QColor, QPainter, QPen
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton


class WindowControlButton(QPushButton):
    """Кнопка свернуть / развернуть / закрыть."""

    def __init__(self, kind: str):
        """kind: minimize | maximize | close."""
        super().__init__()
        self.kind = kind
        self.setObjectName("titleButton")
        self.setFixedSize(32, 30)
        self.setCursor(Qt.PointingHandCursor)

    def paintEvent(self, event):
        """Рисует пиктограмму по kind."""
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(QColor("#eeeaf0"), 1.6)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        painter.setPen(pen)

        cx = self.width() / 2
        cy = self.height() / 2
        size = 12
        half = size / 2

        if self.kind == "minimize":
            painter.drawLine(int(cx - half), int(cy), int(cx + half), int(cy))
        elif self.kind == "maximize":
            painter.drawRect(QRectF(cx - half, cy - half, size, size))
        elif self.kind == "close":
            painter.drawLine(int(cx - half), int(cy - half), int(cx + half), int(cy + half))
            painter.drawLine(int(cx + half), int(cy - half), int(cx - half), int(cy + half))


class TitleBar(QFrame):
    """Перетаскивание окна и кнопки управления."""

    def __init__(self, window, title_markup: str | None = None):
        """window — родитель с toggle_maximized и close."""
        super().__init__()
        self.window = window
        self.drag_position = None
        self.setObjectName("titleBar")
        self.setFixedHeight(48)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 14, 0)
        layout.setSpacing(0)

        default_title = '<b><span style="color:#F03F83;">Daily</span></b> · Планер событий'
        self.title = QLabel(title_markup or default_title, self)
        self.title.setObjectName("windowTitle")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setAttribute(Qt.WA_TransparentForMouseEvents)

        version = QLabel("v1.0")
        version.setObjectName("versionLabel")

        minimize = WindowControlButton("minimize")
        maximize = WindowControlButton("maximize")
        close = WindowControlButton("close")
        for button in (minimize, maximize, close):
            button.setCursor(Qt.PointingHandCursor)

        minimize.clicked.connect(window.showMinimized)
        maximize.clicked.connect(window.toggle_maximized)
        close.clicked.connect(window.close)

        layout.addStretch(1)
        layout.addWidget(version)
        layout.addSpacing(12)
        layout.addWidget(minimize)
        layout.addWidget(maximize)
        layout.addWidget(close)

    def resizeEvent(self, event):
        """Центрирует заголовок на всю ширину."""
        self.title.setGeometry(0, 0, self.width(), self.height())
        super().resizeEvent(event)

    def mousePressEvent(self, event):
        """Запоминает точку для drag."""
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.window.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        """Перемещает окно за title bar."""
        if (
            self.drag_position
            and event.buttons() & Qt.LeftButton
            and not self.window.isMaximized()
        ):
            self.window.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        """Сбрасывает drag."""
        self.drag_position = None
        super().mouseReleaseEvent(event)
