"""Точка входа: запуск планировщика без окна авторизации."""

import sys

from PyQt5.QtWidgets import QApplication

from .planner_window import PlannerWindow


def main() -> None:
    """Создаёт QApplication и показывает PlannerWindow."""
    app = QApplication(sys.argv)
    app.setApplicationName("Daily")
    window = PlannerWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
