"""Main planner window (calendar and tasks)."""

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QColor, QFont, QFontDatabase, QIcon, QPainter, QPainterPath
from PyQt5.QtWidgets import QApplication, QFrame, QHBoxLayout, QStackedWidget, QVBoxLayout, QWidget

from src.front.auth_window.widgets.asset_builder import ensure_asserts
from src.front.common.widgets import TitleBar

from .calendar_state import CalendarState
from .shell.sidebar import Sidebar
from .views.calendar_view import CalendarView
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

        self._calendar_state = CalendarState()
        self._build_ui()
        self._apply_styles()
        self._center_on_screen()
        self._show_view("calendar")

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

        self._title_bar = TitleBar(self, self._title_for_view("calendar"))
        surface_layout.addWidget(self._title_bar)

        body = QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)

        self._sidebar = Sidebar(self._on_view_changed, self._calendar_state)

        self._stack = QStackedWidget()
        self._calendar_view = CalendarView(
            self._calendar_state,
            on_tags_updated=self._sidebar.refresh_tags,
        )
        self._tasks_view = TasksView(self._calendar_state)
        self._stack.addWidget(self._calendar_view)
        self._stack.addWidget(self._tasks_view)

        content = QFrame()
        content.setObjectName("plannerContent")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(24, 20, 32, 24)
        content_layout.setSpacing(0)
        content_layout.addWidget(self._stack, 1)

        body.addWidget(self._sidebar)
        body.addWidget(content, 1)
        surface_layout.addLayout(body, 1)
        root.addWidget(surface)

    def _title_for_view(self, view_key: str) -> str:
        label = "Календарь" if view_key == "calendar" else "Задачи"
        return f'<b><span style="color:#F03F83;">Daily</span></b> · {label}'

    def _on_view_changed(self, view_key: str) -> None:
        self._show_view(view_key)

    def _show_view(self, view_key: str) -> None:
        self._sidebar.set_active_view(view_key)
        self._title_bar.title.setText(self._title_for_view(view_key))
        if view_key == "tasks":
            self._stack.setCurrentWidget(self._tasks_view)
            self._tasks_view.refresh()
        else:
            self._stack.setCurrentWidget(self._calendar_view)
            self._calendar_view.refresh()

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
