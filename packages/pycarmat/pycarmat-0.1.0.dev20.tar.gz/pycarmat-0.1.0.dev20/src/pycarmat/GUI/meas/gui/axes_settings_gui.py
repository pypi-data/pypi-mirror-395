import sys

from PySide6.QtGui import QFont, QPalette
from PySide6.QtWidgets import (QApplication, QVBoxLayout, QLabel, QPushButton, QFormLayout, QDialog, QMessageBox,
                               QComboBox)
from PySide6.QtCore import Qt
from serial.serialutil import SerialException

from pycarmat.ressources.ESP import ESP30xController
from pycarmat.ressources.config.ue31pp_motor import configure_ue31pp_motor
from pycarmat.ressources.config.ue72pp_motor import configure_ue72pp_motor


class AxesSettingsWindow(QDialog):
    def __init__(self, parent, models=None):
        super().__init__()
        if models is None:
            models = []
        self.setWindowTitle("ESP Axes Settings")
        self.setFixedSize(300, 250)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.init_ui(models)
        self.worker = None

        # Variables for dragging the window
        self.dragging = False
        self.drag_position = None
        self.parent = parent

    def show_error_dialog(self, message):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setInformativeText(message)
        msg_box.setWindowTitle("Error")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec()

    def is_dark_theme(self):
        """Detect if the application is using a dark theme"""
        palette = QApplication.palette()
        bg_color = palette.color(QPalette.Window)
        # If background is dark (luminance < 128), it's dark mode
        luminance = (0.299 * bg_color.red() +
                     0.587 * bg_color.green() +
                     0.114 * bg_color.blue())
        return luminance < 128

    def lighten_color(self, hex_color):
        """Lighten a hex color"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
        lighter_rgb = tuple(min(255, int(c + (255 - c) * 0.3)) for c in rgb)
        return f'#{lighter_rgb[0]:02x}{lighter_rgb[1]:02x}{lighter_rgb[2]:02x}'

    def darken_color(self, hex_color):
        """Darken a hex color"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
        darker_rgb = tuple(max(0, int(c * 0.8)) for c in rgb)
        return f'#{darker_rgb[0]:02x}{darker_rgb[1]:02x}{darker_rgb[2]:02x}'

    def init_ui(self, models):

        layout = QVBoxLayout()
        self.setLayout(layout)

        warning = QLabel("Unknown ESP stage model")
        warning.setStyleSheet("font-size: 16pt;")
        layout.addWidget(warning, 0, Qt.AlignCenter)

        # Form layout for settings
        form_layout = QFormLayout()

        self.select_combo1 = QComboBox()
        if models[0] is not None:
            self.select_combo1.addItem(models[0])
        self.select_combo1.addItems(["None", "UE72PP"])
        form_layout.addRow("AXIS 1 > Connected motor", self.select_combo1)

        self.select_combo2 = QComboBox()
        if models[1] is not None:
            self.select_combo2.addItem(models[1])
        self.select_combo2.addItems(["None", "UE31PP"])
        form_layout.addRow("AXIS 2 > Connected motor", self.select_combo2)
        layout.addLayout(form_layout)

        # Start button
        self.start_button = QPushButton("Apply")
        self.start_button.clicked.connect(self.apply)
        self.start_button.setMinimumHeight(50)
        self.start_button.setFont(QFont("Arial", 12))
        layout.addWidget(self.start_button)
        self.start_button.setCursor(Qt.PointingHandCursor)

        self.start_button.setStyleSheet(f"""
                    QPushButton {{
                        border: none;
                        border-radius: 5px;
                        padding: 10px 20px;
                    }}
                """)

    def apply(self):
        motor1 = self.select_combo1.currentText()
        motor2 = self.select_combo2.currentText()
        print(motor1, motor2)

        # motor1 configuration
        if motor1 == "None":
            # deactivate TRL
            self.parent.deactivate_eps(True, False)
        elif motor1 == "UE72PP":
            try:
                with ESP30xController(serial_port='ASRL/dev/ttyUSB0') as esp:
                    configure_ue72pp_motor(esp, axis=1)
            except SerialException:
                # fail, deactivate TRL
                self.parent.deactivate_eps(True, False)

        if motor2 == "None":
            self.parent.deactivate_eps(False, True)
        elif motor2 == "UE31PP":
            try:
                with ESP30xController(serial_port='ASRL/dev/ttyUSB0') as esp:
                    configure_ue31pp_motor(esp, axis=2)
            except SerialException:
                # fail, deactivate angle sweep
                self.parent.deactivate_eps(False, True)

        self.close()


    def mousePressEvent(self, event):
        """Handle mouse press for window dragging"""
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        """Handle mouse move for window dragging"""
        if self.dragging and event.buttons() == Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        """Handle mouse release for window dragging"""
        if event.button() == Qt.LeftButton:
            self.dragging = False
            event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    detected_esp_stage_models = (None, 'EPL209-AM')
    window = AxesSettingsWindow(detected_esp_stage_models)
    window.exec()
    sys.exit(app.exec())