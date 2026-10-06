"""Главное окно планировщика: календарь и задачи."""

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QFontDatabase, QIcon
from PyQt5.QtWidgets import QApplication, QFrame, QHBoxLayout, QStackedWidget, QVBoxLayout, QWidget

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
    """Безрамочное окно с сайдбаром и переключением календарь/задачи."""

    def __init__(self) -> None:
        """Собирает UI, стили и открывает календарь."""
        super().__init__()
        self.setObjectName("plannerWindow")
        self._load_fonts()

        self.setWindowTitle("Daily")
        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.Window | Qt.WindowMinimizeButtonHint
        )
        self._is_expanded = False
        self._auto_fit_on_show = True
        self._toggle_busy = False
        self.setAutoFillBackground(True)
        self.setWindowIcon(QIcon(str(APP_ICON_PATH.resolve())))

        self._screen_fitted = False
        self._calendar_state = CalendarState()
        self._build_ui()
        self._apply_styles()
        self._show_view("calendar")

    def _fit_to_screen(self) -> None:
        """Занимает всю доступную область экрана (без панели задач ОС)."""
        screen = QApplication.primaryScreen().availableGeometry()
        self.setMinimumSize(
            min(960, screen.width()),
            min(600, screen.height()),
        )
        self.setGeometry(screen)
        self._is_expanded = True

    def _load_fonts(self) -> None:
        """Подключает Noto Sans из assets auth."""
        fonts_dir = _AUTH_ASSERTS / "fonts"
        if fonts_dir.exists():
            for font_file in fonts_dir.glob("*.ttf"):
                QFontDatabase.addApplicationFont(str(font_file))
        QApplication.instance().setFont(QFont("Noto Sans", 10))

    def _apply_styles(self) -> None:
        """Склеивает QSS auth и planner."""
        auth_qss = (_BASE_DIR.parent / "auth_window" / "auth_styles.qss").read_text(encoding="utf-8")
        planner_qss = QSS_PATH.read_text(encoding="utf-8")
        self.setStyleSheet(auth_qss + "\n" + planner_qss)

    def _build_ui(self) -> None:
        """Title bar, сайдбар и стек CalendarView / TasksView."""
        root = QVBoxLayout(self)
        root.setContentsMargins(1, 1, 1, 1)
        root.setSpacing(0)

        surface = QFrame()
        surface.setObjectName("windowSurface")
        surface.setAttribute(Qt.WA_StyledBackground, True)
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
        """HTML-заголовок title bar для вида."""
        label = "Календарь" if view_key == "calendar" else "Задачи"
        return f'<b><span style="color:#F03F83;">Daily</span></b> · {label}'

    def _on_view_changed(self, view_key: str) -> None:
        """Обработчик сигнала сайдбара."""
        self._show_view(view_key)

    def _show_view(self, view_key: str) -> None:
        """Переключает стек и вызывает refresh активного вида."""
        self._sidebar.set_active_view(view_key)
        self._title_bar.title.setText(self._title_for_view(view_key))
        if view_key == "tasks":
            self._stack.setCurrentWidget(self._tasks_view)
            self._tasks_view.refresh()
        else:
            self._stack.setCurrentWidget(self._calendar_view)
            self._calendar_view.refresh()

    def apply_initial_layout(self) -> None:
        """Один раз при открытии: растянуть на весь экран."""
        if self._screen_fitted or not self._auto_fit_on_show:
            return
        self._screen_fitted = True
        self._fit_to_screen()

    def toggle_maximized(self) -> None:
        """На весь экран или ~85% (квадрат в title bar)."""
        if self._toggle_busy:
            return
        self._toggle_busy = True
        QTimer.singleShot(250, lambda: setattr(self, "_toggle_busy", False))

        screen = QApplication.primaryScreen().availableGeometry()
        if self._is_expanded:
            w = max(self.minimumWidth(), int(screen.width() * 0.85))
            h = max(self.minimumHeight(), int(screen.height() * 0.85))
            self.setGeometry(
                screen.x() + (screen.width() - w) // 2,
                screen.y() + (screen.height() - h) // 2,
                w,
                h,
            )
            self._is_expanded = False
            self._auto_fit_on_show = False
        else:
            self._auto_fit_on_show = True
            self._fit_to_screen()

    def minimize_window(self) -> None:
        """Сворачивает в панель задач (для frameless-окна)."""
        self.setWindowState(self.windowState() | Qt.WindowMinimized)

__all__ = ["PlannerWindow", "QSS_PATH"]
