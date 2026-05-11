"""Заглушка главного окна планировщика (полный UI — позже)."""

from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget


class PlannerWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Daily — планировщик")
        self.resize(900, 620)
        layout = QVBoxLayout(self)
        layout.addWidget(
            QLabel("Здесь будет основной интерфейс планировщика.")
        )
