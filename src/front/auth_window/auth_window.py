"""Окно авторизации: вход, регистрация, переход в планировщик."""

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QColor, QFont, QFontDatabase, QIcon, QPainter, QPainterPath
from PyQt5.QtWidgets import QApplication, QFrame, QHBoxLayout, QVBoxLayout, QWidget

if __package__:
    from ..planner_window import PlannerWindow
    from .widgets import AuthCard, LeftPanel, TitleBar
else:
    _auth_dir = Path(__file__).resolve().parent
    _front_dir = _auth_dir.parent
    sys.path.insert(0, str(_front_dir))
    sys.path.insert(0, str(_auth_dir))
    from planner_window import PlannerWindow
    from widgets import AuthCard, LeftPanel, TitleBar


BASE_DIR = Path(__file__).resolve().parent
ASSERTS_DIR = BASE_DIR / "asserts"
QSS_PATH = BASE_DIR / "auth_styles.qss"
APP_ICON_PATH = ASSERTS_DIR / "icons" / "daily_logo.png"


class AuthWindow(QWidget):
    """Безрамочное окно с левой промо-панелью и формой входа."""

    def __init__(self):
        """Собирает UI, шрифты, стили; центрирует на экране."""
        super().__init__()
        self._planner_window: QWidget | None = None
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
        """Центрирует окно на экране."""
        screen = QApplication.primaryScreen().availableGeometry()
        frame = self.frameGeometry()
        frame.moveCenter(screen.center())
        self.move(frame.topLeft())

    def _build_ui(self):
        """TitleBar, LeftPanel и AuthCard."""
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
        self._auth_card = AuthCard(ASSERTS_DIR, self._on_auth_success)
        right_layout.addWidget(self._auth_card, 1)

        content.addWidget(LeftPanel(ASSERTS_DIR))
        content.addWidget(right, 1)
        surface_layout.addLayout(content, 1)
        root.addWidget(surface)

    def _load_fonts(self):
        """Регистрирует TTF из asserts/fonts."""
        for font_file in (ASSERTS_DIR / "fonts").glob("*.ttf"):
            QFontDatabase.addApplicationFont(str(font_file))
        QApplication.instance().setFont(QFont("Noto Sans", 10))

    def _apply_styles(self):
        """Подключает auth_styles.qss."""
        self.setStyleSheet(QSS_PATH.read_text(encoding="utf-8"))

    def toggle_maximized(self):
        """Развернуть / восстановить окно."""
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def paintEvent(self, event):
        """Скруглённый фон окна."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5)
        path = QPainterPath()
        path.addRoundedRect(rect, 16, 16)
        painter.fillPath(path, QColor("#15131a"))
        painter.setPen(QColor("#393443"))
        painter.drawPath(path)
        super().paintEvent(event)

    def _on_auth_success(self) -> None:
        """Открывает PlannerWindow и скрывает auth."""
        if self._planner_window is None:
            self._planner_window = PlannerWindow()
        self._planner_window.show()
        self.hide()


def _app_icon() -> QIcon:
    """Абсолютный путь: на Linux относительный путь к PNG иногда даёт пустой QIcon."""
    return QIcon(str(APP_ICON_PATH.resolve()))


def main():
    """Точка входа: auth → exec."""
    app = QApplication(sys.argv)
    app.setApplicationName("Daily")
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
