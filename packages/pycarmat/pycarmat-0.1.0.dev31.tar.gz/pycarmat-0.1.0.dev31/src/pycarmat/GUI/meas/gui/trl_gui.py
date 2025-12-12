import sys
from time import sleep

from PySide6.QtGui import QFont, QPalette
from PySide6.QtWidgets import (QApplication, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout,
                               QDialog, QMessageBox)
from PySide6.QtCore import Qt, QThread, Signal

from pycarmat.ressources.ESP import ESP30xController, UNIT
from pycarmat.ressources.VNA import RohdeSchwarzVNA, KeysightVNA
from pycarmat.GUI.meas.gui.core import Worker


class TRLWorker(Worker):
    result_signal = Signal(bool)
    progress_signal = Signal(str, int)
    reflect_wait_signal = Signal()
    line_wait_signal = Signal()

    def __init__(self, params: dict):
        super().__init__(None, params)
        self.ok_reflect = False
        self.ok_line = False
        self.cancel = False

    def _run(self):
        self._running = True
        axis_transl = self.params.get('esp_axis', 1)

        # Connexion au VNA

        __vna__ = RohdeSchwarzVNA if self.params['is_rs'] else KeysightVNA
        with __vna__(ip_address=self.params['ip_address'], simulate=False) as vna, \
                ESP30xController(serial_port='ASRL/dev/ttyUSB0') as esp:
            # Configuration du sweep en bande W
            vna.set_sweep(
                freq_start_GHz=self.params['freq_start_GHz'],
                freq_end_GHz=self.params['freq_end_GHz'],
                num_pts=int(self.params['num_points']),
                bandwidth=self.params['bandwidth']
            )
            #esp.homing(axis=axis_transl)
            esp.write('1VA1') # velocity: 1 mm/s
            esp.write('1AC5') # acceleration: 5 mm/s
            esp.write('1AG5') # Decelleration: 5 mm/s

            if vna.enable_trl_calibration(cal_kit=self.params['kit']):

                self.reflect_wait_signal.emit()
                while not self.ok_reflect:
                    if self.cancel:
                        return
                    sleep(0.1)
                esp.move_absolute(axis=axis_transl, value=-self.params['refl'], motion_unit=UNIT.TRANSLATION_MM)
                sleep(self.params['refl']*1.1)
                self.progress_signal.emit('reflect', -2)
                stage1, err1 = vna.perform_reflect_measurement()
                self.progress_signal.emit('reflect', int(stage1))
                if not stage1:
                    self.error_signal.emit(str(err1))
                    return

                self.line_wait_signal.emit()
                while not self.ok_line:
                    if self.cancel:
                        return
                    sleep(0.1)
                vel_line = 0.5 # mm/s
                esp.write(f'1VA{vel_line:.1f}')
                esp.move_absolute(axis=axis_transl, value=-self.params['line'], motion_unit=UNIT.TRANSLATION_MM)
                sleep(abs(self.params['refl'] - self.params['line']) / vel_line * 1.2)

                self.progress_signal.emit('line', -2)
                stage2, err2 = vna.perform_line_measurement()
                self.progress_signal.emit('line', int(stage2))
                if not stage2:
                    self.error_signal.emit(str(err2))
                    return

                vel_thru = 0.1 # mm/s
                esp.write(f'1VA{vel_thru:.1f}')
                esp.move_absolute(axis=axis_transl, value=0, motion_unit=UNIT.TRANSLATION_MM)
                sleep(abs(self.params['line']) / vel_thru * 1.2)
                self.progress_signal.emit('thru', -2)
                stage3, err3 = vna.perform_thru_measurement()
                self.progress_signal.emit('thru', int(stage3))
                if not stage3:
                    self.error_signal.emit(str(err3))
                    return

                final, err = vna.save_trl_calibration()
                self.result_signal.emit(final)
                if not final:
                    self.progress_signal.emit('thru', int(0))
                    self.progress_signal.emit('line', int(0))
                    self.progress_signal.emit('reflect', int(0))
                    self.error_signal.emit(str(err))
                    return


class TRLWindow(QDialog):
    def __init__(self, band_settings: dict, ip_address: str, is_rs:bool = True):
        super().__init__()
        self.setWindowTitle("TRL Settings")
        self.setFixedSize(300, 350)

        # Default settings
        self.band_settings = {
            'num_points' : band_settings['num_points'],
            'bandwidth' : band_settings['meas_bandwidth']
        }
        band_id = band_settings['band_id']
        if band_id == 0:
            self.trl_settings = {'line': 0.25, 'refl': 2, 'kit': 'CarmatJ'}
            self.band_settings['start'] = 220.
            self.band_settings['stop'] = 330.
        elif band_id == 1:
            self.trl_settings = {'line': 1, 'refl': 2, 'kit': 'CarmatW'}
            self.band_settings['start'] = 75.
            self.band_settings['stop'] = 110.
        elif band_id == 2:
            self.trl_settings = {'line': 0.5, 'refl': 2, 'kit': 'CarmatD'}
            self.band_settings['start'] = 110.
            self.band_settings['stop'] = 170.
        elif band_id == 3:
            self.trl_settings = {'line': 0.15, 'refl': 2, 'kit': 'CarmatTHz'}
            self.band_settings['start'] = 500.
            self.band_settings['stop'] = 750.

        # LED states
        self.led_states = {'thru': False, 'reflect': False, 'line': False}

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.init_ui()
        self.load_settings()
        self.worker = None
        self.is_rs = is_rs
        self.ip_address = ip_address

        # Variables for dragging the window
        self.dragging = False
        self.drag_position = None

    def _start_worker(self, worker):
        self.worker = worker
        self.thread = QThread()
        self.thread.started.connect(self.worker.start)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.error_signal.connect(self.show_error_dialog)
        self.worker.progress_signal.connect(self.set_led)
        self.worker.reflect_wait_signal.connect(self.request_reflect)
        self.worker.line_wait_signal.connect(self.request_line)

        self.thread.start()

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

    def init_ui(self):

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Form layout for settings
        form_layout = QFormLayout()

        # Line input
        self.line_edit = QLineEdit()
        form_layout.addRow("Line thickness [mm]:", self.line_edit)

        # Refl input
        self.refl_edit = QLineEdit()
        form_layout.addRow("Refl thickness [mm]:", self.refl_edit)

        # Kit input
        self.kit_edit = QLineEdit()
        form_layout.addRow("Kit:", self.kit_edit)

        layout.addLayout(form_layout)

        # LEDs layout
        leds_layout = QHBoxLayout()

        # THRU LED
        thru_container = QVBoxLayout()
        thru_container.setAlignment(Qt.AlignCenter)
        self.thru_led = QLabel()
        self.thru_led.setStyleSheet(self.get_led_style("orange"))
        self.thru_led.setFixedSize(40, 40)
        thru_label = QLabel("THRU")
        thru_label.setAlignment(Qt.AlignCenter)
        thru_container.addWidget(self.thru_led)
        thru_container.addWidget(thru_label)
        leds_layout.addLayout(thru_container)

        # REFLECT LED
        reflect_container = QVBoxLayout()
        reflect_container.setAlignment(Qt.AlignCenter)
        self.reflect_led = QLabel()
        self.reflect_led.setStyleSheet(self.get_led_style("orange"))
        self.reflect_led.setFixedSize(40, 40)
        reflect_label = QLabel("REFL")
        reflect_label.setAlignment(Qt.AlignCenter)
        reflect_container.addWidget(self.reflect_led)
        reflect_container.addWidget(reflect_label)
        leds_layout.addLayout(reflect_container)

        # LINE LED
        line_container = QVBoxLayout()
        line_container.setAlignment(Qt.AlignCenter)
        self.line_led = QLabel()
        self.line_led.setStyleSheet(self.get_led_style("orange"))
        self.line_led.setFixedSize(40, 40)
        line_label = QLabel("LINE")
        line_label.setAlignment(Qt.AlignCenter)
        line_container.addWidget(self.line_led)
        line_container.addWidget(line_label)
        leds_layout.addLayout(line_container)

        layout.addLayout(leds_layout)


        if self.is_dark_theme():
            btn_color = "#3c3c3c"
            btn_hover = "#4c4c4c"
        else:
            btn_color = "#95a5a6"
            btn_hover = "#7f8c8d"

        # Start button
        self.start_button = QPushButton("Start TRL")
        self.start_button.clicked.connect(self.start_trl)
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

        # Quit button
        self.btnb = QPushButton("❌ Close")
        self.btnb.setFont(QFont("Arial", 12))
        self.btnb.setMinimumHeight(50)
        self.btnb.setCursor(Qt.PointingHandCursor)

        self.btnb.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {btn_color};
                        color: white;
                        border: none;
                        border-radius: 5px;
                        padding: 10px 20px;
                    }}
                    QPushButton:hover {{
                        background-color: {btn_hover};
                    }}
                    QPushButton:pressed {{
                        background-color: {self.darken_color(btn_color)};
                    }}
                """)
        self.btnb.clicked.connect(self.close)

        layout.addWidget(self.btnb, 0, Qt.AlignCenter)

    def get_led_style(self, color):
        """Get LED style based on color"""
        colors = {
            'red': '#ff4444',
            'green': '#44ff44',
            'orange': 'orange',
            'white': '#f0f5a9'
        }
        return f"""
            QLabel {{
                background-color: {colors[color]};
                border: 2px solid #333;
                border-radius: 20px;
                text-align: center;
            }}
        """

    def set_led(self, led_name, state: int):
        """Toggle LED state"""
        if state == -2:
            color = 'white'
        else:
            color = 'green' if state == 1 else 'red' if state == 0 else 'orange'
        if state == 0:
            self.start_button.setDisabled(False)
            self.btnb.setDisabled(False)
        if led_name == 'thru':
            self.thru_led.setStyleSheet(self.get_led_style(color))
            if state == 1:
                self.start_button.setDisabled(False)
                self.btnb.setDisabled(False)
        elif led_name == 'reflect':
            self.reflect_led.setStyleSheet(self.get_led_style(color))
        elif led_name == 'line':
            self.line_led.setStyleSheet(self.get_led_style(color))

    def load_settings(self):
        """Load default settings into fields"""
        self.line_edit.setText(str(self.trl_settings['line']))
        self.refl_edit.setText(str(self.trl_settings['refl']))
        self.kit_edit.setText(self.trl_settings['kit'])

    def get_settings(self):
        """Get current settings from fields"""
        return {
            'line': float(self.line_edit.text()),
            'refl': float(self.refl_edit.text()),
            'kit': self.kit_edit.text(),
            'freq_start_GHz': self.band_settings['start'],
            'freq_end_GHz': self.band_settings['stop'],
            'num_points': self.band_settings['num_points'],
            'bandwidth': self.band_settings['bandwidth'],
            'is_rs': self.is_rs,
            'ip_address': self.ip_address
        }

    def start_trl(self):
        """Start TRL calibration"""
        self.set_led('thru', -1)
        self.set_led('reflect', -1)
        self.set_led('line', -1)
        self.start_button.setDisabled(True)
        self.btnb.setDisabled(True)
        trl_settings = self.get_settings()
        worker = TRLWorker(trl_settings)
        self._start_worker(worker)

    def request_reflect(self):
        from PySide6.QtWidgets import QMessageBox
        reply = QMessageBox.question(self, "REFLECT Calibration",
                                     "Place the REFLECTOR and press OK to continue.",
                                     QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)

        if reply == QMessageBox.StandardButton.Ok:
            self.worker.ok_reflect = True
        else:
            self.worker.cancel = True
            self.set_led('reflect', 0)

    def request_line(self):
        from PySide6.QtWidgets import QMessageBox
        reply = QMessageBox.question(self, "LINE Calibration",
                                     "Remove the REFLECTOR and press OK to continue.",
                                     QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)

        if reply == QMessageBox.StandardButton.Ok:
            self.worker.ok_line = True
        else:
            self.worker.cancel = True
            self.set_led('line', 0)


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

    def center_window(self):
        """Center the window on screen"""
        screen = QApplication.primaryScreen().geometry()
        window_geometry = self.frameGeometry()
        center_point = screen.center()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())

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
    band_settings = {
        'num_points': 5001,
        'meas_bandwidth': '1kHz',
        'band_id': 3
    }
    window = TRLWindow(band_settings=band_settings, ip_address='192.168.0.5', is_rs=False)
    window.exec()
    sys.exit(app.exec())