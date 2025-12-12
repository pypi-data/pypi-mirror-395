import logging

from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QTabWidget
import sys
from pathlib import Path

from pycarmat.GUI.meas.gui.sidebar import Sidebar
from pycarmat.GUI.meas.gui.tab1 import Tab1

from matplotlib import rcParams
from matplotlib import pyplot as plt


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Characterisation Bench")
        self.resize(1200, 900)

        main_layout = QHBoxLayout(self)
        self.tab1 = Tab1()

        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self.tab1, "S-Parameters")

        self.sidebar = Sidebar((self.tab_widget, self.tab1, ), min_width=300)

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.tab_widget, 1)
        self.setLayout(main_layout)

def create_arrow_icons():
    """Crée les icônes de flèches SVG"""
    temp_dir = Path.home() / '.temp_icons'
    temp_dir.mkdir(exist_ok=True)

    # Flèche haut sombre
    up_dark = temp_dir / 'arrow_up_dark.svg'
    up_dark.write_text('''<svg width="10" height="6" viewBox="0 0 10 6" xmlns="http://www.w3.org/2000/svg">
        <path d="M5 0L10 6H0L5 0Z" fill="#e0e0e0"/>
    </svg>''')

    # Flèche bas sombre
    down_dark = temp_dir / 'arrow_down_dark.svg'
    down_dark.write_text('''<svg width="10" height="6" viewBox="0 0 10 6" xmlns="http://www.w3.org/2000/svg">
        <path d="M0 0H10L5 6L0 0Z" fill="#e0e0e0"/>
    </svg>''')

    # Flèche haut clair
    up_light = temp_dir / 'arrow_up_light.svg'
    up_light.write_text('''<svg width="10" height="6" viewBox="0 0 10 6" xmlns="http://www.w3.org/2000/svg">
        <path d="M5 0L10 6H0L5 0Z" fill="#2b2b2b"/>
    </svg>''')

    # Flèche bas clair
    down_light = temp_dir / 'arrow_down_light.svg'
    down_light.write_text('''<svg width="10" height="6" viewBox="0 0 10 6" xmlns="http://www.w3.org/2000/svg">
        <path d="M0 0H10L5 6L0 0Z" fill="#2b2b2b"/>
    </svg>''')

    return temp_dir


def apply_dark_mode_to_plots():
    """Configure Matplotlib pour le mode sombre"""
    plt.style.use('dark_background')

    # Configuration complète des couleurs
    rcParams['figure.facecolor'] = '#2b2b2b'
    rcParams['axes.facecolor'] = '#1e1e1e'
    rcParams['axes.edgecolor'] = '#555555'
    rcParams['axes.labelcolor'] = '#e0e0e0'
    rcParams['text.color'] = '#e0e0e0'
    rcParams['xtick.color'] = '#e0e0e0'
    rcParams['ytick.color'] = '#e0e0e0'
    rcParams['grid.color'] = '#3d3d3d'
    rcParams['legend.facecolor'] = '#2b2b2b'
    rcParams['legend.edgecolor'] = '#555555'
    rcParams['legend.framealpha'] = 0.9

    # Couleurs des lignes (palette claire pour contraster)
    rcParams['axes.prop_cycle'] = plt.cycler('color',
                                             ['#4a9eff', '#ff6b6b', '#51cf66', '#ffd93d', '#a78bfa', '#ff8787',
                                              '#69db7c', '#ffa94d'])


def apply_light_mode_to_plots():
    """Configure Matplotlib pour le mode clair"""
    plt.style.use('default')

    # Configuration complète des couleurs
    rcParams['figure.facecolor'] = '#ffffff'
    rcParams['axes.facecolor'] = '#ffffff'
    rcParams['axes.edgecolor'] = '#2b2b2b'
    rcParams['axes.labelcolor'] = '#2b2b2b'
    rcParams['text.color'] = '#2b2b2b'
    rcParams['xtick.color'] = '#2b2b2b'
    rcParams['ytick.color'] = '#2b2b2b'
    rcParams['grid.color'] = '#d0d0d0'
    rcParams['legend.facecolor'] = '#ffffff'
    rcParams['legend.edgecolor'] = '#c0c0c0'
    rcParams['legend.framealpha'] = 0.9

    # Couleurs des lignes
    rcParams['axes.prop_cycle'] = plt.cycler('color',
                                             ['#1976d2', '#d32f2f', '#388e3c', '#f57c00', '#7b1fa2', '#c2185b',
                                              '#0097a7', '#689f38'])


def setup_style(self):
    icon_dir = create_arrow_icons()
    # Récupérer la couleur d'accentuation du système
    accent_color = self.palette().highlight().color()
    accent_hex = accent_color.name()
    accent_hover = accent_color.lighter(110).name()
    accent_pressed = accent_color.darker(110).name()

    if self.palette().window().color().lightness() < 128:
        apply_dark_mode_to_plots()
        up_arrow = str(icon_dir / 'arrow_up_dark.svg').replace('\\', '/')
        down_arrow = str(icon_dir / 'arrow_down_dark.svg').replace('\\', '/')
        self.setStyleSheet(f"""
            QMainWindow {{ background-color: #2b2b2b; }}
            QWidget {{ background-color: #2b2b2b; color: #e0e0e0; font-family: 'Segoe UI', Arial; font-size: 9pt; }}
            QGroupBox {{ border: 2px solid #3d3d3d; border-radius: 6px; margin-top: 10px; padding-top: 12px; font-weight: bold; color: {accent_hex}; }}
            QGroupBox::title {{ subcontrol-origin: margin; left: 12px; padding: 0 4px; }}
            QLineEdit {{ background-color: #3d3d3d; border: 1px solid #555; border-radius: 3px; padding: 4px; color: #e0e0e0; }}
            QLineEdit:focus {{ border: 2px solid {accent_hex}; }}
            QSpinBox, QDoubleSpinBox {{ background-color: #3d3d3d; border: 1px solid #555; border-radius: 3px; padding: 4px; padding-right: 18px; color: #e0e0e0; }}
            QSpinBox:focus, QDoubleSpinBox:focus {{ border: 2px solid {accent_hex}; }}
            QSpinBox::up-button, QDoubleSpinBox::up-button {{ background-color: #555555; border: none; border-top-right-radius: 3px; width: 16px; }}
            QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover {{ background-color: #666666; }}
            QSpinBox::up-button:pressed, QDoubleSpinBox::up-button:pressed {{ background-color: {accent_hex}; }}
            QSpinBox::down-button, QDoubleSpinBox::down-button {{ background-color: #555555; border: none; border-bottom-right-radius: 3px; width: 16px; }}
            QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {{ background-color: #666666; }}
            QSpinBox::down-button:pressed, QDoubleSpinBox::down-button:pressed {{ background-color: {accent_hex}; }}
            QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {{ image: url({up_arrow}); width: 9px; height: 5px; }}
            QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {{ image: url({down_arrow}); width: 9px; height: 5px; }}
            QComboBox {{ background-color: #3d3d3d; border: 1px solid #555; border-radius: 3px; padding: 4px 8px; color: #e0e0e0; }}
            QComboBox:focus {{ border: 2px solid {accent_hex}; }}
            QComboBox:hover {{ border: 1px solid #666; background-color: #454545; }}
            QComboBox::drop-down {{ border: none; width: 20px; }}
            QComboBox::down-arrow {{ image: url({down_arrow}); width: 9px; height: 5px; }}
            QComboBox QAbstractItemView {{ background-color: #3d3d3d; border: 1px solid #555; border-radius: 3px; selection-background-color: {accent_hex}; selection-color: white; color: #e0e0e0; padding: 4px; }}
            QComboBox QAbstractItemView::item {{ padding: 6px; border-radius: 2px; }}
            QComboBox QAbstractItemView::item:hover {{ background-color: #454545; }}
            QPushButton {{ background-color: {accent_hex}; color: white; border: none; border-radius: 4px; padding: 6px 16px; font-weight: 600; font-size: 9pt; }}
            QPushButton:hover {{ background-color: {accent_hover}; }}
            QPushButton:pressed {{ background-color: {accent_pressed}; }}
            QPushButton:disabled {{ background-color: #555; color: #888; }}
            QPushButton#sweep_btn {{ background-color: #8b4513; padding: 6px 12px; font-size: 10pt; }}
            QPushButton#sweep_btn:hover {{ background-color: #a0522d; }}
            QPushButton#sweep_btn:pressed {{ background-color: #6b3410; }}
            QPushButton#build_btn {{ background-color: #0f7c35; padding: 6px 12px; font-size: 10pt; }}
            QPushButton#build_btn:hover {{ background-color: #12a043; }}
            QPushButton#build_btn:pressed {{ background-color: #0c5c26; }}
            QPushButton#cancel_btn {{ background-color: #d32f2f; }}
            QPushButton#cancel_btn:hover {{ background-color: #e53935; }}
            QPushButton#cancel_btn:pressed {{ background-color: #b71c1c; }}
            QPushButton#export_btn {{ padding: 6px 12px; font-size: 10pt; }}
            QTextEdit {{ background-color: #1e1e1e; border: 1px solid #3d3d3d; border-radius: 3px; padding: 6px; color: #e0e0e0; font-family: 'Consolas', 'Courier New'; }}
            QProgressBar {{ border: 1px solid #3d3d3d; border-radius: 3px; background-color: #3d3d3d; text-align: center; color: white; height: 18px; }}
            QProgressBar::chunk {{ background-color: {accent_hex}; border-radius: 2px; }}
            QCheckBox {{ spacing: 6px; }}
            QCheckBox::indicator {{ width: 16px; height: 16px; border-radius: 3px; border: 2px solid #555; background-color: #3d3d3d; }}
            QCheckBox::indicator:checked {{ background-color: {accent_hex}; border-color: {accent_pressed}; }}
            QListWidget {{ background-color: #1e1e1e; border: 1px solid #3d3d3d; border-radius: 3px; padding: 4px; color: #e0e0e0; }}
            QListWidget::item {{ padding: 6px; border-radius: 2px; }}
            QListWidget::item:selected {{ background-color: {accent_hex}; color: white; }}
            QListWidget::item:hover {{ background-color: #3d3d3d; }}
            QTabWidget::pane {{ border: 1px solid #3d3d3d; border-radius: 3px; background-color: #2b2b2b; }}
            QTabBar::tab {{ background-color: #3d3d3d; color: #e0e0e0; padding: 8px 16px; border-top-left-radius: 3px; border-top-right-radius: 3px; margin-right: 2px; }}
            QTabBar::tab:selected {{ background-color: {accent_hex}; color: white; }}
            QScrollBar:vertical {{ background-color: #2b2b2b; width: 12px; border-radius: 6px; margin: 0px; }}
            QScrollBar::handle:vertical {{ background-color: #555555; min-height: 25px; border-radius: 6px; margin: 2px; }}
            QScrollBar::handle:vertical:hover {{ background-color: #666666; }}
            QScrollBar::handle:vertical:pressed {{ background-color: {accent_hex}; }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0px; }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{ background: none; }}
            QScrollBar:horizontal {{ background-color: #2b2b2b; height: 12px; border-radius: 6px; margin: 0px; }}
            QScrollBar::handle:horizontal {{ background-color: #555555; min-width: 25px; border-radius: 6px; margin: 2px; }}
            QScrollBar::handle:horizontal:hover {{ background-color: #666666; }}
            QScrollBar::handle:horizontal:pressed {{ background-color: {accent_hex}; }}
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ width: 0px; }}
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{ background: none; }}
        """)
    else:
        apply_light_mode_to_plots()
        up_arrow = str(icon_dir / 'arrow_up_light.svg').replace('\\', '/')
        down_arrow = str(icon_dir / 'arrow_down_light.svg').replace('\\', '/')
        self.setStyleSheet(f"""
            QMainWindow {{ background-color: #f5f5f5; }}
            QWidget {{ background-color: #f5f5f5; color: #2b2b2b; font-family: 'Segoe UI', Arial; font-size: 9pt; }}
            QGroupBox {{ border: 2px solid #d0d0d0; border-radius: 6px; margin-top: 10px; padding-top: 12px; font-weight: bold; color: {accent_hex}; }}
            QGroupBox::title {{ subcontrol-origin: margin; left: 12px; padding: 0 4px; }}
            QLineEdit {{ background-color: #ffffff; border: 1px solid #c0c0c0; border-radius: 3px; padding: 4px; color: #2b2b2b; }}
            QLineEdit:focus {{ border: 2px solid {accent_hex}; }}
            QSpinBox, QDoubleSpinBox {{ background-color: #ffffff; border: 1px solid #c0c0c0; border-radius: 3px; padding: 4px; padding-right: 18px; color: #2b2b2b; }}
            QSpinBox:focus, QDoubleSpinBox:focus {{ border: 2px solid {accent_hex}; }}
            QSpinBox::up-button, QDoubleSpinBox::up-button {{ background-color: #e0e0e0; border: none; border-top-right-radius: 3px; width: 16px; }}
            QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover {{ background-color: #d0d0d0; }}
            QSpinBox::up-button:pressed, QDoubleSpinBox::up-button:pressed {{ background-color: {accent_hex}; }}
            QSpinBox::down-button, QDoubleSpinBox::down-button {{ background-color: #e0e0e0; border: none; border-bottom-right-radius: 3px; width: 16px; }}
            QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {{ background-color: #d0d0d0; }}
            QSpinBox::down-button:pressed, QDoubleSpinBox::down-button:pressed {{ background-color: {accent_hex}; }}
            QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {{ image: url({up_arrow}); width: 9px; height: 5px; }}
            QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {{ image: url({down_arrow}); width: 9px; height: 5px; }}
            QComboBox {{ background-color: #ffffff; border: 1px solid #c0c0c0; border-radius: 3px; padding: 4px 8px; color: #2b2b2b; }}
            QComboBox:focus {{ border: 2px solid {accent_hex}; }}
            QComboBox:hover {{ border: 1px solid #a0a0a0; background-color: #f8f8f8; }}
            QComboBox::drop-down {{ border: none; width: 20px; }}
            QComboBox::down-arrow {{ image: url({down_arrow}); width: 9px; height: 5px; }}
            QComboBox QAbstractItemView {{ background-color: #ffffff; border: 1px solid #c0c0c0; border-radius: 3px; selection-background-color: {accent_hex}; selection-color: white; color: #2b2b2b; padding: 4px; }}
            QComboBox QAbstractItemView::item {{ padding: 6px; border-radius: 2px; }}
            QComboBox QAbstractItemView::item:hover {{ background-color: #f0f0f0; }}
            QPushButton {{ background-color: {accent_hex}; color: white; border: none; border-radius: 4px; padding: 6px 16px; font-weight: 600; font-size: 9pt; }}
            QPushButton:hover {{ background-color: {accent_hover}; }}
            QPushButton:pressed {{ background-color: {accent_pressed}; }}
            QPushButton:disabled {{ background-color: #e0e0e0; color: #9e9e9e; }}
            QPushButton#sweep_btn {{ background-color: #d67d3e; padding: 6px 12px; font-size: 10pt; }}
            QPushButton#sweep_btn:hover {{ background-color: #e08f52; }}
            QPushButton#sweep_btn:pressed {{ background-color: #c56b2a; }}
            QPushButton#build_btn {{ background-color: #2e8b57; padding: 6px 12px; font-size: 10pt; }}
            QPushButton#build_btn:hover {{ background-color: #3cb371; }}
            QPushButton#build_btn:pressed {{ background-color: #256d43; }}
            QPushButton#cancel_btn {{ background-color: #e53935; }}
            QPushButton#cancel_btn:hover {{ background-color: #ef5350; }}
            QPushButton#cancel_btn:pressed {{ background-color: #c62828; }}
            QPushButton#export_btn {{ padding: 6px 12px; font-size: 10pt; }}
            QTextEdit {{ background-color: #ffffff; border: 1px solid #d0d0d0; border-radius: 3px; padding: 6px; color: #2b2b2b; font-family: 'Consolas', 'Courier New'; }}
            QProgressBar {{ border: 1px solid #d0d0d0; border-radius: 3px; background-color: #e8e8e8; text-align: center; color: #2b2b2b; height: 18px; }}
            QProgressBar::chunk {{ background-color: {accent_hex}; border-radius: 2px; }}
            QCheckBox {{ spacing: 6px; }}
            QCheckBox::indicator {{ width: 16px; height: 16px; border-radius: 3px; border: 2px solid #c0c0c0; background-color: #ffffff; }}
            QCheckBox::indicator:checked {{ background-color: {accent_hex}; border-color: {accent_pressed}; }}
            QListWidget {{ background-color: #ffffff; border: 1px solid #d0d0d0; border-radius: 3px; padding: 4px; color: #2b2b2b; }}
            QListWidget::item {{ padding: 6px; border-radius: 2px; }}
            QListWidget::item:selected {{ background-color: {accent_hex}; color: white; }}
            QListWidget::item:hover {{ background-color: #f0f0f0; }}
            QTabWidget::pane {{ border: 1px solid #d0d0d0; border-radius: 3px; background-color: #f5f5f5; }}
            QTabBar::tab {{ background-color: #e0e0e0; color: #2b2b2b; padding: 8px 16px; border-top-left-radius: 3px; border-top-right-radius: 3px; margin-right: 2px; }}
            QTabBar::tab:selected {{ background-color: {accent_hex}; color: white; }}
            QScrollBar:vertical {{ background-color: #f5f5f5; width: 12px; border-radius: 6px; margin: 0px; }}
            QScrollBar::handle:vertical {{ background-color: #c0c0c0; min-height: 25px; border-radius: 6px; margin: 2px; }}
            QScrollBar::handle:vertical:hover {{ background-color: #a0a0a0; }}
            QScrollBar::handle:vertical:pressed {{ background-color: {accent_hex}; }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0px; }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{ background: none; }}
            QScrollBar:horizontal {{ background-color: #f5f5f5; height: 12px; border-radius: 6px; margin: 0px; }}
            QScrollBar::handle:horizontal {{ background-color: #c0c0c0; min-width: 25px; border-radius: 6px; margin: 2px; }}
            QScrollBar::handle:horizontal:hover {{ background-color: #a0a0a0; }}
            QScrollBar::handle:horizontal:pressed {{ background-color: {accent_hex}; }}
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ width: 0px; }}
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{ background: none; }}
        """)

def main():

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)

    app = QApplication(sys.argv)
    app.setApplicationName("PyCarMat Measurement Acquisition")
    app.setOrganizationName("IMT Atlantique")
    setup_style(app)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()