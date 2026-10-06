"""Точка входа: запуск планировщика без окна авторизации."""

import sys

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication

from .planner_window import PlannerWindow


def main() -> None:
    """Создаёт QApplication и показывает PlannerWindow."""
    app = QApplication(sys.argv)
    app.setApplicationName("Daily")
    window = PlannerWindow()
    window.show()
    QTimer.singleShot(0, window.apply_initial_layout)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
