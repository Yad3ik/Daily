from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel


class EventRow(QFrame):
    def __init__(self, time: str, title: str, tag: str, color_name: str) -> None:
        super().__init__()
        self.setObjectName(f"eventRow_{color_name}")
        self.setFixedHeight(32)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 0, 12, 0)
        layout.setSpacing(8)

        time_label = QLabel(time)
        time_label.setObjectName("eventTime")
        time_label.setFixedWidth(46)

        title_label = QLabel(title)
        title_label.setObjectName("eventTitle")

        tag_label = QLabel(tag)
        tag_label.setObjectName(f"tag_{color_name}")
        tag_label.setAlignment(Qt.AlignCenter)
        tag_label.setFixedSize(56, 21)

        layout.addWidget(time_label)
        layout.addWidget(title_label)
        layout.addStretch(1)
        layout.addWidget(tag_label)
