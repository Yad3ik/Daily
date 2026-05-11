import sys
from pathlib import Path

from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QColor, QFont, QFontDatabase, QIcon, QPainter, QPainterPath
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
APP_ICON_PATH = ASSERTS_DIR / "icons" / "daily_logo.png"


class AuthWindow(QWidget):
    def __init__(self):
        super().__init__()
        ensure_asserts()
        self._load_fonts()

        self.setWindowTitle("Daily")
        self.resize(960, 740)
        self.setMinimumSize(960, 740)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowIcon(_app_icon())

        self._build_ui()
        self._apply_styles()    
        self._center_on_screen()

    def _center_on_screen(self):
        screen = QApplication.primaryScreen().availableGeometry()
        frame = self.frameGeometry()
        frame.moveCenter(screen.center())
        self.move(frame.topLeft())

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


def _app_icon() -> QIcon:
    """Абсолютный путь: на Linux относительный путь к PNG иногда даёт пустой QIcon."""
    return QIcon(str(APP_ICON_PATH.resolve()))


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Daily")
    # Иначе setWindowIcon до первого ensure_asserts() — файла ещё нет, иконка не подхватится.
    ensure_asserts()
    icon = _app_icon()
    app.setWindowIcon(icon)
    try:
        app.setDesktopFileName("daily")
    except AttributeError:
        pass
    window = AuthWindow()
    window.setWindowIcon(icon)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
