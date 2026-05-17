"""Main planner window (tasks)."""

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QColor, QFont, QFontDatabase, QIcon, QPainter, QPainterPath
from PyQt5.QtWidgets import QApplication, QFrame, QHBoxLayout, QVBoxLayout, QWidget

from src.front.auth_window.widgets.asset_builder import ensure_asserts
from src.front.common.widgets import TitleBar

from .shell.sidebar import Sidebar
from .views.tasks_view import TasksView

_BASE_DIR = Path(__file__).resolve().parent
_AUTH_ASSERTS = _BASE_DIR.parent / "auth_window" / "asserts"
QSS_PATH = _BASE_DIR / "planner_styles.qss"
APP_ICON_PATH = _AUTH_ASSERTS / "icons" / "daily_logo.png"


class PlannerWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        ensure_asserts()
        self._load_fonts()

        self.setWindowTitle("Daily")
        self.resize(1920, 1080)
        self.setMinimumSize(1440, 900)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowIcon(QIcon(str(APP_ICON_PATH.resolve())))

        self._build_ui()
        self._apply_styles()
        self._center_on_screen()
        self._tasks_view.refresh()

    def _center_on_screen(self) -> None:
        screen = QApplication.primaryScreen().availableGeometry()
        frame = self.frameGeometry()
        frame.moveCenter(screen.center())
        self.move(frame.topLeft())

    def _load_fonts(self) -> None:
        fonts_dir = _AUTH_ASSERTS / "fonts"
        if fonts_dir.exists():
            for font_file in fonts_dir.glob("*.ttf"):
                QFontDatabase.addApplicationFont(str(font_file))
        QApplication.instance().setFont(QFont("Noto Sans", 10))

    def _apply_styles(self) -> None:
        auth_qss = (_BASE_DIR.parent / "auth_window" / "auth_styles.qss").read_text(encoding="utf-8")
        planner_qss = QSS_PATH.read_text(encoding="utf-8")
        self.setStyleSheet(auth_qss + "\n" + planner_qss)

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(1, 1, 1, 1)
        root.setSpacing(0)

        surface = QFrame()
        surface.setObjectName("windowSurface")
        surface_layout = QVBoxLayout(surface)
        surface_layout.setContentsMargins(0, 0, 0, 0)
        surface_layout.setSpacing(0)

        title = '<b><span style="color:#F03F83;">Daily</span></b> · Задачи'
        surface_layout.addWidget(TitleBar(self, title))

        body = QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)

        self._sidebar = Sidebar()
        self._tasks_view = TasksView()

        content = QFrame()
        content.setObjectName("plannerContent")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(24, 20, 36, 24)
        content_layout.setSpacing(0)
        content_layout.addWidget(self._tasks_view, 1)

        body.addWidget(self._sidebar)
        body.addWidget(content, 1)
        surface_layout.addLayout(body, 1)
        root.addWidget(surface)

    def toggle_maximized(self) -> None:
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5)
        path = QPainterPath()
        path.addRoundedRect(rect, 16, 16)
        painter.fillPath(path, QColor("#15131a"))
        painter.setPen(QColor("#393443"))
        painter.drawPath(path)
        super().paintEvent(event)


__all__ = ["PlannerWindow", "QSS_PATH"]
