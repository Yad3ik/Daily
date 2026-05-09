from pathlib import Path

from PyQt5.QtCore import QPointF, QRectF, Qt
from PyQt5.QtGui import (
    QColor,
    QConicalGradient,
    QFont,
    QGuiApplication,
    QImage,
    QLinearGradient,
    QPainter,
    QPainterPath,
    QPen,
    QRadialGradient,
)


ROOT = Path(__file__).resolve().parents[1]
ASSERTS = ROOT / "asserts"
ICONS = ASSERTS / "icons"
IMAGES = ASSERTS / "images"


def _canvas(width, height):
    image = QImage(width, height, QImage.Format_ARGB32_Premultiplied)
    image.fill(Qt.transparent)
    painter = QPainter(image)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setRenderHint(QPainter.SmoothPixmapTransform)
    return image, painter


def _save(image, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(str(path))


def _draw_logo():
    image, painter = _canvas(128, 128)
    gradient = QLinearGradient(0, 0, 128, 128)
    gradient.setColorAt(0.0, QColor("#FF5A9B"))
    gradient.setColorAt(1.0, QColor("#F03F83"))
    painter.setPen(Qt.NoPen)
    painter.setBrush(gradient)
    painter.drawRoundedRect(QRectF(6, 6, 116, 116), 28, 28)

    painter.setBrush(QColor("#111018"))
    painter.setPen(QPen(QColor("#fff8fb"), 6))
    painter.drawRoundedRect(QRectF(43, 42, 42, 42), 11, 11)

    gloss = QLinearGradient(10, 6, 118, 72)
    gloss.setColorAt(0, QColor(255, 255, 255, 60))
    gloss.setColorAt(0.55, QColor(255, 255, 255, 0))
    painter.setPen(Qt.NoPen)
    painter.setBrush(gloss)
    painter.drawRoundedRect(QRectF(9, 7, 110, 48), 26, 26)
    painter.end()
    _save(image, ICONS / "daily_logo.png")


def _draw_line_icon(filename, kind):
    image, painter = _canvas(64, 64)
    painter.setBrush(Qt.NoBrush)
    painter.setPen(QPen(QColor("#cbc5cf"), 3.3, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
    if kind == "user":
        painter.drawEllipse(QRectF(23, 11, 18, 18))
        path = QPainterPath(QPointF(16, 52))
        path.cubicTo(18, 39, 27, 35, 32, 35)
        path.cubicTo(37, 35, 46, 39, 48, 52)
        painter.drawPath(path)
    elif kind == "lock":
        painter.drawRoundedRect(QRectF(17, 30, 30, 23), 5, 5)
        path = QPainterPath(QPointF(23, 30))
        path.lineTo(23, 24)
        path.cubicTo(23, 12, 41, 12, 41, 24)
        path.lineTo(41, 30)
        painter.drawPath(path)
    elif kind == "eye":
        path = QPainterPath(QPointF(8, 32))
        path.cubicTo(18, 17, 46, 17, 56, 32)
        path.cubicTo(46, 47, 18, 47, 8, 32)
        painter.drawPath(path)
        painter.drawEllipse(QRectF(26, 26, 12, 12))
    painter.end()
    _save(image, ICONS / filename)


def _draw_left_illustration():
    image, painter = _canvas(700, 420)

    table = QLinearGradient(0, 330, 700, 420)
    table.setColorAt(0, QColor(32, 29, 38, 220))
    table.setColorAt(1, QColor(10, 9, 14, 20))
    painter.setPen(Qt.NoPen)
    painter.setBrush(table)
    painter.drawPolygon(
        QPointF(0, 355), QPointF(700, 238), QPointF(700, 420), QPointF(0, 420)
    )

    glow = QRadialGradient(QPointF(498, 190), 270)
    glow.setColorAt(0, QColor(255, 96, 158, 44))
    glow.setColorAt(0.38, QColor(99, 55, 94, 23))
    glow.setColorAt(1, QColor(0, 0, 0, 0))
    painter.setBrush(glow)
    painter.drawEllipse(QRectF(238, -2, 520, 400))

    # Vase and leaves.
    vase_gradient = QLinearGradient(92, 232, 166, 390)
    vase_gradient.setColorAt(0, QColor("#ba547c"))
    vase_gradient.setColorAt(0.55, QColor("#64304a"))
    vase_gradient.setColorAt(1, QColor("#1e1720"))
    vase = QPainterPath(QPointF(89, 379))
    vase.cubicTo(62, 342, 88, 288, 104, 279)
    vase.lineTo(145, 279)
    vase.cubicTo(168, 306, 183, 345, 151, 379)
    vase.cubicTo(135, 393, 105, 393, 89, 379)
    painter.setBrush(vase_gradient)
    painter.setPen(QPen(QColor("#F03F83"), 1.1))
    painter.drawPath(vase)
    painter.drawEllipse(QRectF(101, 270, 43, 16))

    painter.setPen(QPen(QColor("#974565"), 2.7, Qt.SolidLine, Qt.RoundCap))
    branches = [
        ((123, 279), (91, 213), (54, 176)),
        ((123, 279), (125, 205), (145, 154)),
        ((123, 279), (168, 220), (219, 178)),
        ((123, 279), (91, 232), (72, 191)),
    ]
    for start, mid, end in branches:
        path = QPainterPath(QPointF(*start))
        path.cubicTo(QPointF(*mid), QPointF(*mid), QPointF(*end))
        painter.drawPath(path)
    painter.setPen(Qt.NoPen)
    painter.setBrush(QColor("#a74f74"))
    for x, y, angle in [
        (59, 184, -37), (78, 209, 30), (93, 191, -23), (112, 170, 26),
        (131, 190, -31), (148, 156, 24), (168, 205, -27), (196, 183, 31),
        (211, 171, -35), (149, 232, 30), (104, 229, -28), (76, 172, -34),
    ]:
        painter.save()
        painter.translate(x, y)
        painter.rotate(angle)
        painter.drawEllipse(QRectF(-6, -15, 12, 30))
        painter.restore()

    # Books.
    painter.setPen(QPen(QColor("#2b202c"), 2))
    painter.setBrush(QColor("#332534"))
    painter.drawRoundedRect(QRectF(335, 286, 315, 63), 5, 5)
    painter.setPen(QPen(QColor("#7c3956"), 1.5))
    painter.drawLine(360, 303, 630, 303)
    painter.drawLine(374, 333, 630, 333)

    painter.setPen(QPen(QColor("#251a25"), 2))
    painter.setBrush(QColor("#563149"))
    painter.drawRoundedRect(QRectF(302, 236, 325, 61), 5, 5)
    pages = QLinearGradient(306, 244, 623, 244)
    pages.setColorAt(0, QColor("#ff70a7"))
    pages.setColorAt(1, QColor("#f4a7c5"))
    painter.setPen(Qt.NoPen)
    painter.setBrush(pages)
    painter.drawRoundedRect(QRectF(309, 243, 307, 19), 2, 2)
    painter.setPen(QPen(QColor("#ffc5d9"), 1))
    for y in range(248, 261, 4):
        painter.drawLine(318, y, 606, y)

    # Cup.
    cup_gradient = QLinearGradient(431, 111, 535, 235)
    cup_gradient.setColorAt(0, QColor("#864865"))
    cup_gradient.setColorAt(0.45, QColor("#241923"))
    cup_gradient.setColorAt(1, QColor("#08070b"))
    painter.setBrush(cup_gradient)
    painter.setPen(QPen(QColor("#75405b"), 1.4))
    painter.drawRoundedRect(QRectF(432, 111, 105, 122), 16, 16)
    painter.setBrush(Qt.NoBrush)
    painter.setPen(QPen(QColor("#08070b"), 11))
    painter.drawArc(QRectF(521, 142, 63, 66), -90 * 16, 190 * 16)
    painter.setPen(QPen(QColor("#2a1c28"), 4))
    painter.drawArc(QRectF(523, 146, 52, 56), -90 * 16, 190 * 16)
    coffee = QConicalGradient(QPointF(484, 112), 14)
    coffee.setColorAt(0, QColor("#ff754a"))
    coffee.setColorAt(0.22, QColor("#1d0e12"))
    coffee.setColorAt(0.72, QColor("#09070a"))
    coffee.setColorAt(1, QColor("#ff754a"))
    painter.setBrush(coffee)
    painter.setPen(QPen(QColor("#93516e"), 2))
    painter.drawEllipse(QRectF(431, 101, 106, 28))

    # Pen.
    painter.setPen(QPen(QColor("#ee6299"), 5, Qt.SolidLine, Qt.RoundCap))
    painter.drawLine(235, 363, 382, 391)
    painter.setPen(QPen(QColor("#241b25"), 3, Qt.SolidLine, Qt.RoundCap))
    painter.drawLine(249, 364, 366, 386)
    painter.setPen(QPen(QColor("#f7adc9"), 3, Qt.SolidLine, Qt.RoundCap))
    painter.drawLine(226, 362, 240, 364)

    painter.setFont(QFont("Noto Serif", 18, QFont.Bold))
    painter.setPen(QColor("#F03F83"))
    for x, y, text in [(555, 54, "+"), (608, 116, "✦"), (505, 28, "✦"), (578, 336, "·")]:
        painter.drawText(QPointF(x, y), text)

    painter.end()
    _save(image, IMAGES / "desk_scene.png")


def ensure_asserts():
    expected = [
        ICONS / "daily_logo.png",
        ICONS / "user.png",
        ICONS / "lock.png",
        ICONS / "eye.png",
        IMAGES / "desk_scene.png",
    ]
    if all(path.exists() for path in expected):
        return
    app = QGuiApplication.instance()
    owns_app = app is None
    if owns_app:
        app = QGuiApplication([])
    _draw_logo()
    _draw_line_icon("user.png", "user")
    _draw_line_icon("lock.png", "lock")
    _draw_line_icon("eye.png", "eye")
    _draw_left_illustration()
