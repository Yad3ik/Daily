import sys
from pathlib import Path

from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QColor, QFont, QFontDatabase, QPainter, QPainterPath
from PyQt5.QtWidgets import QApplication, QFrame, QHBoxLayout, QVBoxLayout, QWidget

if __package__:
    from .widgets import AuthCard, LeftPanel, TitleBar
    from .widgets.asset_builder import ensure_asserts
else:
    sys.path.append(str(Path(__file__).resolve().parent))
    from widgets import AuthCard, LeftPanel, TitleBar
    from widgets.asset_builder import ensure_asserts


BASE_DIR = Path(__file__).resolve().parent
ASSERTS_DIR = BASE_DIR / "asserts"
QSS_PATH = BASE_DIR / "auth_styles.qss"


class AuthWindow(QWidget):
    def __init__(self):
        super().__init__()
        ensure_asserts()
        self._load_fonts()

        self.setWindowTitle("Daily")
        self.resize(960, 640)
        self.setMinimumSize(900, 600)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self._build_ui()
        self._apply_styles()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(1, 1, 1, 1)
        root.setSpacing(0)

        surface = QFrame()
        surface.setObjectName("windowSurface")
        surface_layout = QVBoxLayout(surface)
        surface_layout.setContentsMargins(0, 0, 0, 0)
        surface_layout.setSpacing(0)

        surface_layout.addWidget(TitleBar(self))

        content = QHBoxLayout()
        content.setContentsMargins(0, 0, 0, 0)
        content.setSpacing(0)

        right = QFrame()
        right.setObjectName("rightPanel")
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(30, 24, 36, 36)
        right_layout.setSpacing(0)
        right_layout.addWidget(AuthCard(ASSERTS_DIR))

        content.addWidget(LeftPanel(ASSERTS_DIR))
        content.addWidget(right, 1)
        surface_layout.addLayout(content, 1)
        root.addWidget(surface)

    def _load_fonts(self):
        for font_file in (ASSERTS_DIR / "fonts").glob("*.ttf"):
            QFontDatabase.addApplicationFont(str(font_file))
        QApplication.instance().setFont(QFont("Noto Sans", 10))

    def _apply_styles(self):
        self.setStyleSheet(QSS_PATH.read_text(encoding="utf-8"))

    def toggle_maximized(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5)
        path = QPainterPath()
        path.addRoundedRect(rect, 16, 16)
        painter.fillPath(path, QColor("#15131a"))
        painter.setPen(QColor("#393443"))
        painter.drawPath(path)
        super().paintEvent(event)


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Daily")
    window = AuthWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
