# animated_button.py
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, pyqtProperty, Qt
from PyQt5.QtGui import QColor

class AnimatedButton(QPushButton):
    def __init__(self, text='', parent=None, bg_color=QColor(75, 0, 130, 255), hover_color=QColor(138, 43, 226, 255)):
        super(AnimatedButton, self).__init__(text, parent)
        self._bg_color = bg_color  # Исходный цвет фона
        self.hover_color = hover_color  # Цвет при наведении
        self.animation = QPropertyAnimation(self, b"bg_color")
        self.animation.setDuration(300)  # Длительность анимации в миллисекундах
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.setStyleSheet(f"background-color: {self._bg_color.name()}; border: none;")
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedSize(40, 40)

    def get_bg_color(self):
        return self._bg_color

    def set_bg_color(self, color):
        self._bg_color = color
        self.setStyleSheet(f"background-color: {self._bg_color.name()}; border: none; border-radius: 10px;")

    bg_color = pyqtProperty(QColor, fget=get_bg_color, fset=set_bg_color)

    def enterEvent(self, event):
        self.animation.stop()
        self.animation.setStartValue(self._bg_color)
        self.animation.setEndValue(self.hover_color)
        self.animation.start()
        super(AnimatedButton, self).enterEvent(event)

    def leaveEvent(self, event):
        self.animation.stop()
        self.animation.setStartValue(self._bg_color)
        self.animation.setEndValue(QColor(75, 0, 130, 255))  # Возвращаемся к исходному цвету
        self.animation.start()
        super(AnimatedButton, self).leaveEvent(event)
