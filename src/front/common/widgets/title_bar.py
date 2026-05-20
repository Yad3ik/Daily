"""Общий title bar для PlannerWindow и диалогов (перетаскивание, кнопки окна)."""

from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QColor, QPainter, QPen
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QWidget


class WindowControlButton(QPushButton):
    """Кнопка minimize / maximize / close."""

    def __init__(self, kind: str) -> None:
        """kind определяет пиктограмму в paintEvent."""
        super().__init__()
        self.kind = kind
        self.setObjectName("titleButton")
        self.setFixedSize(32, 30)
        self.setCursor(Qt.PointingHandCursor)
        self.setAutoRepeat(False)
        self.setFocusPolicy(Qt.NoFocus)

    def mousePressEvent(self, event) -> None:
        """Не отдаём нажатие title bar (drag)."""
        event.accept()
        super().mousePressEvent(event)

    def paintEvent(self, event) -> None:
        """Рисует иконку управления окном."""
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
    """Заголовок по центру, версия и кнопки; drag окна."""

    def __init__(
        self,
        window,
        title_markup: str | None = None,
        *,
        show_version: bool = True,
    ) -> None:
        """show_version=False — для диалогов без «v1.0»; window — родительское окно."""
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

        self._left_spacer = QWidget(self)
        self._left_spacer.setAttribute(Qt.WA_TransparentForMouseEvents)

        version = QLabel("v1.0")
        version.setObjectName("versionLabel")

        minimize = WindowControlButton("minimize")
        maximize = WindowControlButton("maximize")
        close = WindowControlButton("close")
        for button in (minimize, maximize, close):
            button.setCursor(Qt.PointingHandCursor)

        if hasattr(window, "minimize_window"):
            minimize.clicked.connect(window.minimize_window)
        else:
            minimize.clicked.connect(window.showMinimized)
        maximize.clicked.connect(window.toggle_maximized)
        close.clicked.connect(window.close)

        self._show_version = show_version
        self._version = version

        layout.addWidget(self._left_spacer)
        if show_version:
            layout.addStretch(1)
            layout.addWidget(version)
            layout.addSpacing(12)
        layout.addWidget(minimize)
        layout.addWidget(maximize)
        layout.addWidget(close)

    def resizeEvent(self, event) -> None:
        """Балансирует отступ слева и центрирует title."""
        controls_width = 14 + 32 * 3
        if self._show_version:
            controls_width += 12 + self._version.sizeHint().width()
        self._left_spacer.setFixedWidth(controls_width)
        self.title.setGeometry(0, 0, self.width(), self.height())
        super().resizeEvent(event)

    def mousePressEvent(self, event) -> None:
        """Начало перетаскивания окна."""
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.window.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event) -> None:
        """Двигает окно, если не maximized."""
        expanded = getattr(self.window, "_is_expanded", self.window.isMaximized())
        if self.drag_position and event.buttons() & Qt.LeftButton and not expanded:
            self.window.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event) -> None:
        """Конец перетаскивания."""
        self.drag_position = None
        super().mouseReleaseEvent(event)
