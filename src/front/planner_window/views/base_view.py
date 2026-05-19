from PyQt5.QtWidgets import QWidget


class BaseView(QWidget):
    """Base class for planner content views."""

    def refresh(self) -> None:
        """Reload data from session / backend."""
