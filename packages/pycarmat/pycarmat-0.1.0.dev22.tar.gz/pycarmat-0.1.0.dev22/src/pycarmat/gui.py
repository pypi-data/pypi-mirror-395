#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUI Launcher - Main interface to launch different applications
"""

import sys
import subprocess
from pathlib import Path
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QPushButton, QLabel, QMessageBox, QSpacerItem,
                               QSizePolicy, QHBoxLayout, QGridLayout)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QPalette, QColor


class GUILauncher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Application Launcher")
        self.setMinimumSize(700, 400)

        # Remove window decorations
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Detect dark mode from application palette
        self.is_dark_mode = self.is_dark_theme()

        # Configure applications
        self.applications = [
            {
                'name': 'Forward Model',
                'color': '#082b27',
                'icon': '⧁',
                'path': '-m qosm',
                'absolute': True,
            },
            {
                'name': 'Measurements',
                'color': '#3498db',
                'icon': '📊',
                'path': 'GUI/meas/gui_meas.py',
                'absolute': False,
            },
            {
                'name': 'Epsilon Estimation',
                'color': '#e74c3c',
                'icon': '⚙️',
                'path': 'GUI/epsilon/gui_optim.py',
                'absolute': False,
            },
            {
                'name': 'Enhanced Estimation',
                'color': '#527315',
                'icon': '⚙️',
                'path': 'GUI/optim/gui.py',
                'absolute': False,
            }
        ]

        self.setup_ui()
        self.center_window()

        # Variables for dragging the window
        self.dragging = False
        self.drag_position = None

    def is_dark_theme(self):
        """Detect if the application is using a dark theme"""
        palette = QApplication.palette()
        bg_color = palette.color(QPalette.Window)
        # If background is dark (luminance < 128), it's dark mode
        luminance = (0.299 * bg_color.red() +
                     0.587 * bg_color.green() +
                     0.114 * bg_color.blue())
        return luminance < 128

    def setup_ui(self):
        """Setup the user interface"""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        central_widget.setLayout(main_layout)

        # Title section
        title_widget = QWidget()
        title_widget.setFixedHeight(70)
        if self.is_dark_mode:
            title_widget.setStyleSheet("background-color: #252526;")
        else:
            title_widget.setStyleSheet("background-color: #2c3e50;")

        title_layout = QVBoxLayout()
        title_layout.setContentsMargins(20, 0, 0, 0)
        title_widget.setLayout(title_layout)

        # Header with title and close button
        header_layout = QVBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)

        # Close button
        close_btn = QPushButton("✕")
        close_btn.setFont(QFont("Arial", 20))
        close_btn.setFixedSize(30, 30)
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                border-radius: 15px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.2);
            }
        """)
        close_btn.clicked.connect(self.close)

        # Top bar with close button

        top_bar = QWidget()
        top_bar_layout = QHBoxLayout()
        top_bar_layout.setContentsMargins(20, 20, 20, 20)
        top_bar.setLayout(top_bar_layout)

        title_label = QLabel("PyCarMat Applications")
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont("Arial", 20, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: white;")
        top_bar_layout.addWidget(title_label, 0, Qt.AlignCenter)

        close_layout = QHBoxLayout()
        close_layout.addWidget(close_btn)
        top_bar_layout.addLayout(close_layout)

        title_layout.addWidget(top_bar)
        title_layout.addStretch()

        main_layout.addWidget(title_widget)
        main_layout.addSpacing(0)

        # Buttons container
        buttons_widget = QWidget()
        buttons_layout = QGridLayout()
        buttons_layout.setContentsMargins(30, 20, 30, 20)
        buttons_layout.setSpacing(15)
        buttons_widget.setLayout(buttons_layout)

        # Create application buttons in a grid (2 columns)
        row = 0
        col = 0
        for app in self.applications:
            btn = self.create_app_button(app)
            buttons_layout.addWidget(btn, row, col)
            col += 1
            if col >= 2:  # 2 buttons per row
                col = 0
                row += 1

        # Add stretch to push buttons to top
        buttons_layout.setRowStretch(row + 1, 1)
        main_layout.addWidget(buttons_widget, 1)


    def create_app_button(self, app):
        """Create a large rectangular button for launching an application"""
        btn = QPushButton(f"{app['icon']}\n{app['name']}")
        btn.setFont(QFont("Arial", 14, QFont.Bold))
        btn.setFixedSize(280, 150)  # Wider rectangular buttons
        btn.setCursor(Qt.PointingHandCursor)

        color = app['color']
        hover_color = self.lighten_color(color)
        pressed_color = self.darken_color(color)

        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 12px;
                padding: 15px 10px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
            QPushButton:pressed {{
                background-color: {pressed_color};
            }}
        """)

        btn.clicked.connect(lambda: self.launch_app(app))
        return btn

    def launch_app(self, app):
        """Launch an application GUI"""
        try:
            # Get the package directory
            import pycarmat
            if not app['absolute']:
                package_dir = Path(pycarmat.__file__).parent

                # Build the correct path based on app name
                script_path = package_dir / app['path']

                # Check if file exists
                if not script_path.exists():
                    QMessageBox.critical(
                        self,
                        "Error",
                        f"The file '{script_path}' was not found.\n\n"
                        f"Expected location: {script_path}"
                    )
                    return
            else:
                script_path = app['path']

            # Launch the script in a new process
            if str(script_path).startswith('-m'):
                cmd = script_path.split(' ')
                subprocess.Popen([sys.executable, cmd[0], cmd[1]])
            else:
                subprocess.Popen([sys.executable, str(script_path)])

        except Exception as e:
            QMessageBox.critical(
                self,
                "Launch Error",
                f"Unable to launch '{app['name']}':\n\n{str(e)}"
            )

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


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("PyCarMat Launcher")
    app.setOrganizationName("IMT Atlantique")

    # Set application style
    app.setStyle('Fusion')

    launcher = GUILauncher()
    launcher.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()