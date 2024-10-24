import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QLineEdit, QLabel, QSpacerItem, QSizePolicy
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt, QPoint, QSize, QCoreApplication
from PyQt5.QtGui import QIcon, QColor, QPainter, QBrush, QPen, QPixmap, QFontDatabase, QFont

# Импортируем AnimatedButton
from config.animation import AnimatedButton  # Убедитесь, что файл animated_button.py находится в той же директории или в PYTHONPATH

# Константы для путей к ресурсам
FONT_PATH = "config/ProtestGuerrilla-Regular.ttf"
ICON_PATHS = {
    "window_icon": os.path.join("icons", "SARA(TheRizaev© copyright 2024)-.png"),
    "snd": os.path.join("icons", "snd.png"),
    "mic": os.path.join("icons", "mic.png")
}
STYLESHEET_PATH = "config/styles.qss"  # Путь к файлу стилей

class CustomTitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("CustomTitleBar")
        self.setAutoFillBackground(True)
        self.setFixedHeight(80)  # Увеличенная высота заголовка

        # Загрузка шрифта
        if os.path.exists(FONT_PATH):
            font_id = QFontDatabase.addApplicationFont(FONT_PATH)
            if font_id != -1:
                family = QFontDatabase.applicationFontFamilies(font_id)[0]
            else:
                family = self.font().family()
                print(f"Failed to load font from {FONT_PATH}. Using default font.")
        else:
            family = self.font().family()
            print(f"Font file {FONT_PATH} not found. Using default font.")

        layout = QHBoxLayout()
        layout.setContentsMargins(10, 0, 10, 0)
        self.setLayout(layout)

        # Добавляем небольшой спейсер перед заголовком для смещения вправо
        left_spacer = QSpacerItem(120, 120, QSizePolicy.Fixed, QSizePolicy.Minimum)
        layout.addSpacerItem(left_spacer)
    
        # Центрированный заголовок
        self.title = QLabel("S.A.R.A.", self)
        self.title.setObjectName("titleLabel")
        self.title.setFont(QFont(family, 50))  # Увеличенный размер шрифта
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title, alignment=Qt.AlignCenter)

        # Кнопки управления окном
        self.create_buttons(layout)

        self.start = QPoint(0, 0)

    def create_buttons(self, layout):
        # Кнопка сворачивания
        minimize_button = AnimatedButton('–', self, bg_color=QColor(75, 0, 130, 255), hover_color=QColor(138, 43, 226, 255))
        minimize_button.setObjectName("minimizeButton")
        minimize_button.clicked.connect(self.minimize_window)
        layout.addWidget(minimize_button)

        # Кнопка закрытия
        close_button = AnimatedButton('✕', self, bg_color=QColor(75, 0, 130, 255), hover_color=QColor(200, 0, 0, 255))  # Пример с другими цветами
        close_button.setObjectName("closeButton")
        close_button.clicked.connect(self.close_window)
        layout.addWidget(close_button)

    def close_window(self):
        self.window().close()

    def minimize_window(self):
        self.window().showMinimized()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start = event.globalPos() - self.window().frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.window().move(event.globalPos() - self.start)
            event.accept()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('S.A.R.A.')
        self.setGeometry(300, 150, 1320, 780)

        # Устанавливаем иконку окна
        if os.path.exists(ICON_PATHS["window_icon"]):
            self.setWindowIcon(QIcon(ICON_PATHS["window_icon"]))
        else:
            print(f"Window icon {ICON_PATHS['window_icon']} not found.")

        # Убираем рамки окна и включаем прозрачный фон
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Центральный виджет
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Кастомный title bar
        self.title_bar = CustomTitleBar(self)
        main_layout.addWidget(self.title_bar)

        # Веб-вью
        self.webview = QWebEngineView()
        remote_url = "https://therizaev.github.io/Sara-orb/"
        self.webview.setUrl(QUrl(remote_url))
        self.webview.setMinimumSize(800, 600)
        main_layout.addWidget(self.webview)

        # Нижняя панель
        main_layout.addLayout(self.create_bottom_layout())

    def create_bottom_layout(self):
        bottom_layout = QHBoxLayout()

        # Спейсер слева
        fixed_spacer = QSpacerItem(330, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        bottom_layout.addSpacerItem(fixed_spacer)

        # Текстовое поле с градиентом
        text_input = QLineEdit()
        text_input.setFixedWidth(600)
        text_input.setPlaceholderText("Что вы хотите узнать?")
        text_input.setObjectName("textInput")
        bottom_layout.addWidget(text_input)

        bottom_layout.addSpacing(5)

        # Кнопки snd и mic
        bottom_layout.addWidget(self.create_icon_button("snd"))
        bottom_layout.addSpacing(20)
        bottom_layout.addWidget(self.create_icon_button("mic"))

        # Спейсер справа
        bottom_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        bottom_layout.setContentsMargins(0, 0, 0, 20)
        return bottom_layout

    def create_icon_button(self, key):
        if key == "snd":
            # Кнопка отправки с розовыми оттенками
            button = AnimatedButton(parent=self, bg_color=QColor(66, 0, 133, 255), hover_color=QColor(255, 182, 193, 255))
        elif key == "mic":
            # Кнопка микрофона с розовыми оттенками
            button = AnimatedButton(parent=self, bg_color=QColor(66, 0, 133, 255), hover_color=QColor(255, 192, 203, 255))

        button.setFixedSize(50, 50)
        icon_path = ICON_PATHS.get(key)
        if icon_path and os.path.exists(icon_path):
            pixmap = QPixmap(icon_path).scaled(QSize(30, 30), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            button.setIcon(QIcon(pixmap))
        else:
            print(f"Icon for '{key}' not found at {icon_path}.")

        button.setIconSize(QSize(30, 30))
        button.setCursor(Qt.PointingHandCursor)
        button.setObjectName(f"{key}Button")
        return button

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect()

        # Отрисовка основного фона с закруглёнными углами
        painter.setBrush(QBrush(QColor(0, 0, 0)))  # Черный фон
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, 20, 20)

        # Параметры рамки
        border_color = QColor(128, 128, 128)  # Серый цвет
        border_width = 2  # Толщина рамки

        # Настройка пера для рамки
        pen = QPen(border_color)
        pen.setWidth(border_width)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)

        # Корректировка прямоугольника для рамки, чтобы она не выходила за пределы окна
        adjusted_rect = rect.adjusted(
            border_width // 2,   # Используем целочисленное деление
            border_width // 2,
            -border_width // 2,
            -border_width // 2
        )

        # Отрисовка рамки с закруглёнными углами
        painter.drawRoundedRect(adjusted_rect, 20, 20)

    def load_stylesheet(app, stylesheet_path):
        if os.path.exists(stylesheet_path):
            with open(stylesheet_path, "r", encoding="utf-8") as f:
                app.setStyleSheet(f.read())
        else:
            print(f"Stylesheet file '{stylesheet_path}' not found.")

def load_stylesheet(app, stylesheet_path):
    if os.path.exists(stylesheet_path):
        with open(stylesheet_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    else:
        print(f"Stylesheet file '{stylesheet_path}' not found.")

def main():
    # Устанавливаем атрибуты перед созданием QApplication
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

    app = QApplication(sys.argv)

    # Загрузка стилей из файла .qss
    load_stylesheet(app, STYLESHEET_PATH)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
