from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout


class EventRow(QFrame):
    def __init__(self, time: str, title: str, tag: str, color_name: str):
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


class ScheduleCard(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("scheduleCard")
        self.setFixedHeight(116)
        self.setFixedWidth(292)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 6, 14, 8)
        layout.setSpacing(6)

        header_box = QFrame()
        header_box.setFixedHeight(12)
        header_row = QHBoxLayout(header_box)
        header_row.setContentsMargins(0, 0, 0, 0)
        header_row.setSpacing(0)
        header = QLabel("С Е Г О Д Н Я · Ч Т")
        header.setObjectName("scheduleHeader")
        header.setFixedHeight(12)
        dot = QLabel("•")
        dot.setObjectName("pinkDot")
        dot.setFixedHeight(12)
        dot.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        header_row.addWidget(header)
        header_row.addStretch(1)
        header_row.addWidget(dot)

        layout.addWidget(header_box)
        layout.addWidget(EventRow("10:00", "Поход в кино", "Личное", "pink"))
        layout.addWidget(EventRow("19:30", "Бот матана", "Учеба", "purple"))


class FadedImage(QLabel):
    def __init__(self, image_path: Path, width: int, height: int):
        super().__init__()
        self.setObjectName("illustration")
        self.setAlignment(Qt.AlignCenter)
        self.setFixedHeight(height)
        self.setPixmap(self._make_pixmap(image_path, width, height - 4))

    def _make_pixmap(self, image_path: Path, width: int, height: int):
        return QPixmap(str(image_path)).scaled(
            width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )


class LeftPanel(QFrame):
    def __init__(self, asserts_dir: Path):
        super().__init__()
        self.asserts_dir = asserts_dir
        self.setObjectName("leftPanel")
        self.setFixedWidth(480)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(34, 34, 26, 20)
        layout.setSpacing(0)

        logo_row = QHBoxLayout()
        logo_row.setSpacing(13)

        logo = QLabel()
        logo.setFixedSize(38, 38)
        logo.setPixmap(
            QPixmap(str(asserts_dir / "icons" / "daily_logo.png")).scaled(
                38, 38, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )

        brand = QLabel('Daily<span style="color:#F03F83;">.</span>')
        brand.setObjectName("brandName")

        logo_row.addWidget(logo)
        logo_row.addWidget(brand)
        logo_row.addStretch(1)

        caption = QLabel("—  ПЛАНЕР СОБЫТИЙ")
        caption.setObjectName("caption")

        slogan = QLabel(
            'Организуй <span style="color:#F03F83;"><i>день</i></span>.<br>'
            'Освободи <span style="color:#F03F83;"><i>мысли</i></span>.'
        )
        slogan.setObjectName("slogan")

        description = QLabel("Задачи, дедлайны и личные планы —\nв одном пространстве.")
        description.setObjectName("description")

        illustration = FadedImage(
            asserts_dir / "images" / "desk_scene.png",
            width=380,
            height=210,
        )

        layout.addLayout(logo_row)
        layout.addSpacing(28)
        layout.addWidget(caption)
        layout.addSpacing(13)
        layout.addWidget(slogan)
        layout.addSpacing(18)
        layout.addWidget(description)
        layout.addSpacing(-8)
        layout.addWidget(illustration)
        layout.addSpacing(30)

        schedule_row = QHBoxLayout()
        schedule_row.setContentsMargins(0, 0, 0, 0)
        schedule_row.addStretch(1)
        schedule_row.addWidget(ScheduleCard())
        schedule_row.addStretch(1)
        layout.addLayout(schedule_row)
        layout.addStretch(1)
