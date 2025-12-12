import os
import sys
from copy import deepcopy
from pathlib import Path
import traceback

import numpy as np
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QLabel, QLineEdit, QPushButton,
                               QFileDialog, QSpinBox, QDoubleSpinBox,
                               QGroupBox, QGridLayout, QTextEdit, QProgressBar,
                               QCheckBox, QTabWidget, QSplitter, QComboBox)
from PySide6.QtCore import Qt, QThread, Signal, QObject

import matplotlib

from pycarmat.inverse_model.analyse.analyze_angle_independence import load_parameters
from pycarmat.inverse_model.score_functions.metrics import lsq_score
from pycarmat.inverse_model.enhanced_model import EnhancedInverseProblem

matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib import rcParams
from matplotlib import pyplot as plt

from qosm.propagation import GBTC

class WorkerSignals(QObject):
    progress = Signal(int)
    finished = Signal(dict)
    error = Signal(str)
    log = Signal(str)


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


class EstimationWorker(QThread):
    def __init__(self, fitter, model, initial_guess_thickness, freq_step_thickness, freq_step_permittivity):
        super().__init__()
        self.fitter = fitter
        self.model = model
        self.initial_guess_thickness = initial_guess_thickness
        self.freq_step_thickness = freq_step_thickness
        self.freq_step_permittivity = freq_step_permittivity
        self.signals = WorkerSignals()
        self.two_passes = True

    def run(self):
        try:
            self.signals.log.emit("Starting two-pass estimation...")
            self.signals.log.emit("Pass 1: Estimating thickness and permittivity...")
            epsr_est, epsr_raw, h_est = self.fitter.sweep_fit(
                self.model, self.initial_guess_thickness, frequency_step=self.freq_step_thickness
            )
            wg = self.fitter.compute_weights(1)
            epsr_mean =  np.sum(epsr_est(self.fitter.frequencies_ghz) * wg, axis=0)

            self.signals.log.emit(f"Estimated thickness: {h_est} mm")
            self.signals.log.emit(f"Mean permittivity: {epsr_mean.real:.5f}{epsr_mean.imag:.5f}j")

            if self.two_passes:
                _init_config = self.fitter.config
                self.fitter.config = deepcopy(self.fitter.config_est)
                self.signals.log.emit("Pass 2: Refining permittivity... ")
                initial_guess_refined = (epsr_mean.real, epsr_mean.imag)
                epsr_est, epsr_raw = self.fitter.sweep_fit(
                    self.model, initial_guess_refined, frequency_step=self.freq_step_permittivity
                )
                epsr_mean =  np.sum(epsr_est(self.fitter.frequencies_ghz) * wg, axis=0)
                # epsr_mean = np.nanmedian(epsr_est(self.fitter.frequencies_ghz))

                # Restore initial thickness values
                self.fitter.config = _init_config
                self.signals.log.emit(f"Mean permittivity: {epsr_mean.real:.5f}{epsr_mean.imag:.5f}j")
            else:
                self.signals.log.emit("Pass 2: Refining permittivity skipped")

            results = {
                'epsr_est': epsr_est,
                'epsr_raw': epsr_raw,
                'thickness_mm': h_est,
                'epsr_mean': epsr_mean
            }

            self.signals.log.emit("Generating sweep data...")
            results['sweep_data'] = self.fitter.sweep(model=self.model)

            self.signals.finished.emit(results)
            self.signals.log.emit("Estimation completed!")

        except Exception as e:
            self.signals.error.emit(f"Error: {str(e)}")
            traceback.print_exc()


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=8, height=6, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.fitter = None
        self.results = None
        self.worker = None

        self.setWindowTitle("Enhanced Material Parameters Estimation")
        self.setup_style()

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)

        left_panel = self.create_control_panel()
        splitter.addWidget(left_panel)

        right_panel = self.create_visualization_panel()
        splitter.addWidget(right_panel)

        splitter.setSizes([450, 1500])

        # Connect signals
        self.single_layer.stateChanged.connect(self.update_ui_for_layer_mode)
        self.account_air_gap.stateChanged.connect(self.update_ui_for_air_gap)
        self.unknown_material_id.textChanged.connect(self.update_paths)
        self.known_material_id.textChanged.connect(self.update_paths)
        self.forced_air_gap.stateChanged.connect(self.update_paths)
        self.account_air_gap.stateChanged.connect(self.update_paths)
        self.single_layer.stateChanged.connect(self.update_paths)
        self.thickness_id.textChanged.connect(self.update_paths)
        self.trl_id.valueChanged.connect(self.update_paths)
        self.unknown_layer.valueChanged.connect(self.update_paths)
        self.generated_data.stateChanged.connect(self.update_paths)
        self.generated_data.stateChanged.connect(self.update_base_folder_visibility)
        self.band_selector.currentIndexChanged.connect(self.update_paths)

        self.update_ui_for_layer_mode()
        self.update_ui_for_air_gap()
        self.update_base_folder_visibility()
        self.update_paths()

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
                QPushButton#load_files_btn {{ background-color: #474b4d; padding: 8px; }}
                QPushButton#load_files_btn:hover {{ background-color: #5a5f61; }}
                QPushButton#load_files_btn:pressed {{ background-color: #3a3e3f; }}
                QPushButton#optimize_btn {{ background-color: #1a7a33; padding: 8px; }}
                QPushButton#optimize_btn:hover {{ background-color: #1f9940; }}
                QPushButton#optimize_btn:pressed {{ background-color: #155d26; }}
                QPushButton#apply_btn {{ background-color: #0078d4; font-weight: bold; }}
                QPushButton#apply_btn:hover {{ background-color: #1084e0; }}
                QPushButton#apply_btn:pressed {{ background-color: #005fa3; }}
                QTextEdit {{ background-color: #1e1e1e; border: 1px solid #3d3d3d; border-radius: 3px; padding: 6px; color: #e0e0e0; font-family: 'Consolas', 'Courier New'; }}
                QProgressBar {{ border: 1px solid #3d3d3d; border-radius: 3px; background-color: #3d3d3d; text-align: center; color: white; height: 18px; }}
                QProgressBar::chunk {{ background-color: {accent_hex}; border-radius: 2px; }}
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
                QPushButton#load_files_btn {{ background-color: #666666; padding: 8px; }}
                QPushButton#load_files_btn:hover {{ background-color: #7a7a7a; }}
                QPushButton#load_files_btn:pressed {{ background-color: #525252; }}
                QPushButton#optimize_btn {{ background-color: #2e8b57; padding: 8px; }}
                QPushButton#optimize_btn:hover {{ background-color: #3cb371; }}
                QPushButton#optimize_btn:pressed {{ background-color: #256d43; }}
                QPushButton#apply_btn {{ background-color: #0078d4; font-weight: bold; }}
                QPushButton#apply_btn:hover {{ background-color: #1084e0; }}
                QPushButton#apply_btn:pressed {{ background-color: #005fa3; }}
                QTextEdit {{ background-color: #ffffff; border: 1px solid #d0d0d0; border-radius: 3px; padding: 6px; color: #2b2b2b; font-family: 'Consolas', 'Courier New'; }}
                QProgressBar {{ border: 1px solid #d0d0d0; border-radius: 3px; background-color: #e8e8e8; text-align: center; color: #2b2b2b; height: 18px; }}
                QProgressBar::chunk {{ background-color: {accent_hex}; border-radius: 2px; }}
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

    def create_control_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(10)

        # Create tabs for parameters
        params_tabs = QTabWidget()
        params_tabs.addTab(self.create_files_and_materials_tab(), "📂 Files & Materials")
        params_tabs.addTab(self.create_estimation_params_tab(), "⚙️ Estimation")
        params_tabs.addTab(self.create_processing_params_tab(), "🔧 Processing")

        layout.addWidget(params_tabs)

        # Action buttons
        button_layout = QVBoxLayout()
        self.load_btn = QPushButton("📁 Load Data")
        self.load_btn.clicked.connect(self.load_data)
        button_layout.addWidget(self.load_btn)

        self.estimate_btn = QPushButton("🚀 Start Estimation")
        self.estimate_btn.clicked.connect(self.start_estimation)
        self.estimate_btn.setEnabled(False)
        button_layout.addWidget(self.estimate_btn)
        layout.addLayout(button_layout)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # Log output
        log_label = QLabel("📋 Log Output:")
        log_label.setStyleSheet("font-weight: bold; color: #4a9eff;")
        layout.addWidget(log_label)

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setMaximumHeight(160)
        layout.addWidget(self.log_output)

        return panel

    def create_files_and_materials_tab(self):
        tab = QWidget()
        main_layout = QVBoxLayout(tab)

        # Material Configuration Section (now first)
        material_group = QGroupBox("Material Configuration")
        material_layout = QGridLayout()

        self.single_layer = QCheckBox("Single Layer Mode")
        material_layout.addWidget(self.single_layer, 0, 0, 1, 2)

        material_layout.addWidget(QLabel("Unknown Material:"), 1, 0)
        self.unknown_material_id = QLineEdit("pa6")
        material_layout.addWidget(self.unknown_material_id, 1, 1)

        self.known_material_label = QLabel("Known Material:")
        material_layout.addWidget(self.known_material_label, 2, 0)
        self.known_material_id = QLineEdit("pvc")
        material_layout.addWidget(self.known_material_id, 2, 1)

        self.unknown_layer_label = QLabel("Unknown Layer:")
        material_layout.addWidget(self.unknown_layer_label, 4, 0)
        self.unknown_layer = QSpinBox()
        self.unknown_layer.setRange(0, 10)
        self.unknown_layer.setValue(2)
        material_layout.addWidget(self.unknown_layer, 4, 1)

        self.account_air_gap = QCheckBox("Account for Air Gap")
        self.account_air_gap.setChecked(True)
        material_layout.addWidget(self.account_air_gap, 5, 0, 1, 2)

        self.air_gap_layer_label = QLabel("Air Gap Layer:")
        material_layout.addWidget(self.air_gap_layer_label, 6, 0)
        self.air_gap_layer = QSpinBox()
        self.air_gap_layer.setRange(0, 10)
        self.air_gap_layer.setValue(1)
        material_layout.addWidget(self.air_gap_layer, 6, 1)

        self.forced_air_gap = QCheckBox("Forced Air Gap")
        self.forced_air_gap.setChecked(False)
        material_layout.addWidget(self.forced_air_gap, 7, 0, 1, 2)

        material_group.setLayout(material_layout)
        main_layout.addWidget(material_group)

        # File Selection Section (now second)
        file_group = QGroupBox("File Selection")
        file_layout = QGridLayout()

        file_layout.addWidget(QLabel("Band:"), 0, 0)
        self.band_selector = QComboBox()
        self.band_selector.addItems(["J-band", "W-band", "D-band"])
        self.band_selector.setCurrentIndex(0)
        file_layout.addWidget(self.band_selector, 0, 1, 1, 2)

        file_layout.addWidget(QLabel("TRL ID:"), 1, 0)
        self.trl_id = QSpinBox()
        self.trl_id.setRange(1, 99)
        self.trl_id.setValue(1)
        file_layout.addWidget(self.trl_id, 1, 1)

        file_layout.addWidget(QLabel("Thickness ID:"), 2, 0)
        self.thickness_id = QLineEdit("5-3")
        file_layout.addWidget(self.thickness_id, 2, 1)

        self.generated_data = QCheckBox("Use Generated Data")
        self.generated_data.setChecked(False)
        file_layout.addWidget(self.generated_data, 3, 0, 1, 2)

        self.base_folder_label = QLabel("Base Folder:")
        file_layout.addWidget(self.base_folder_label, 4, 0)
        self.base_folder = QLineEdit(
            "/media/g18gaudi/Data/Personal/Documents/Projects/PyCarMat/measures/J-Band/20251008/")
        file_layout.addWidget(self.base_folder, 4, 1)

        base_folder_btn = QPushButton("Browse")
        base_folder_btn.clicked.connect(lambda: self.browse_folder(self.base_folder))
        file_layout.addWidget(base_folder_btn, 4, 2)

        self.config_base_folder_label = QLabel("Config Base Folder:")
        file_layout.addWidget(self.config_base_folder_label, 5, 0)
        self.config_base_folder = QLineEdit(
            "/media/g18gaudi/Data/Personal/Documents/Studies/")
        file_layout.addWidget(self.config_base_folder, 5, 1)

        self.config_base_folder_btn = QPushButton("Browse")
        self.config_base_folder_btn.clicked.connect(lambda: self.browse_folder(self.config_base_folder))
        file_layout.addWidget(self.config_base_folder_btn, 5, 2)

        file_layout.addWidget(QLabel("Config (auto):"), 6, 0)
        self.config_path_display = QLabel("")
        self.config_path_display.setStyleSheet("color: #4a9eff; font-style: italic;")
        self.config_path_display.setWordWrap(True)
        file_layout.addWidget(self.config_path_display, 6, 1, 1, 2)

        file_layout.addWidget(QLabel("S2P (auto):"), 7, 0)
        self.s2p_path_display = QLabel("")
        self.s2p_path_display.setStyleSheet("color: #4a9eff; font-style: italic;")
        self.s2p_path_display.setWordWrap(True)
        file_layout.addWidget(self.s2p_path_display, 7, 1, 1, 2)

        file_layout.addWidget(QLabel("Number of angles to use:"), 8, 0)
        self.num_angles_used = QSpinBox()
        self.num_angles_used.setRange(1, 5)
        self.num_angles_used.setValue(4)
        file_layout.addWidget(self.num_angles_used, 8, 1)

        file_group.setLayout(file_layout)
        main_layout.addWidget(file_group)

        main_layout.addStretch()
        return tab

    def create_estimation_params_tab(self):
        tab = QWidget()
        layout = QGridLayout(tab)

        layout.addWidget(QLabel("ε' Initial:"), 0, 0)
        self.eps_real = QDoubleSpinBox()
        self.eps_real.setRange(1.0, 100.0)
        self.eps_real.setValue(3.0)
        self.eps_real.setDecimals(3)
        layout.addWidget(self.eps_real, 0, 1)

        layout.addWidget(QLabel("ε'' Initial:"), 1, 0)
        self.eps_imag = QDoubleSpinBox()
        self.eps_imag.setRange(-1.0, -0.0001)
        self.eps_imag.setValue(-0.0001)
        self.eps_imag.setDecimals(4)
        layout.addWidget(self.eps_imag, 1, 1)

        layout.addWidget(QLabel("Unknown Thickness (mm):"), 2, 0)
        self.unknown_thickness_guess = QDoubleSpinBox()
        self.unknown_thickness_guess.setRange(0.001, 100.0)
        self.unknown_thickness_guess.setValue(3.0)
        self.unknown_thickness_guess.setDecimals(3)
        layout.addWidget(self.unknown_thickness_guess, 2, 1)

        self.air_gap_thickness_label = QLabel("Air Gap Thickness (mm):")
        layout.addWidget(self.air_gap_thickness_label, 3, 0)
        self.air_gap_thickness_guess = QDoubleSpinBox()
        self.air_gap_thickness_guess.setRange(0.001, 100.0)
        self.air_gap_thickness_guess.setValue(0.05)
        self.air_gap_thickness_guess.setDecimals(3)
        layout.addWidget(self.air_gap_thickness_guess, 3, 1)

        layout.addWidget(QLabel("Freq Step Pass 1:"), 4, 0)
        self.freq_step_1 = QSpinBox()
        self.freq_step_1.setRange(1, 100)
        self.freq_step_1.setValue(40)
        layout.addWidget(self.freq_step_1, 4, 1)

        layout.addWidget(QLabel("Freq Step Pass 2:"), 5, 0)
        self.freq_step_2 = QSpinBox()
        self.freq_step_2.setRange(1, 100)
        self.freq_step_2.setValue(10)
        layout.addWidget(self.freq_step_2, 5, 1)

        self.use_two_passes = QCheckBox("Enable two passes (permittivity refinement)")
        self.use_two_passes.setChecked(True)
        layout.addWidget(self.use_two_passes, 6, 0, 1, 2)

        layout.setRowStretch(7, 1)
        return tab

    def create_processing_params_tab(self):
        tab = QWidget()
        layout = QGridLayout(tab)

        layout.addWidget(QLabel("Poly Fit Degree:"), 0, 0)
        self.poly_degree = QSpinBox()
        self.poly_degree.setRange(0, 10)
        self.poly_degree.setValue(0)
        layout.addWidget(self.poly_degree, 0, 1)

        layout.addWidget(QLabel("Filter Window:"), 1, 0)
        self.filter_window = QSpinBox()
        self.filter_window.setRange(3, 201)
        self.filter_window.setValue(71)
        self.filter_window.setSingleStep(2)
        layout.addWidget(self.filter_window, 1, 1)

        layout.addWidget(QLabel("Filter Poly Order:"), 2, 0)
        self.filter_poly = QSpinBox()
        self.filter_poly.setRange(1, 10)
        self.filter_poly.setValue(5)
        layout.addWidget(self.filter_poly, 2, 1)

        layout.setRowStretch(3, 1)
        return tab

    def create_visualization_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)

        self.tab_widget = QTabWidget()

        self.s21_canvas = MplCanvas(self, width=8, height=10)
        self.tab_widget.addTab(self.s21_canvas, "S21 Parameters")

        self.s11_canvas = MplCanvas(self, width=8, height=6)
        self.tab_widget.addTab(self.s11_canvas, "S11 Parameters")

        self.eps_canvas = MplCanvas(self, width=8, height=6)
        self.tab_widget.addTab(self.eps_canvas, "Permittivity")

        layout.addWidget(self.tab_widget)
        return panel

    def browse_folder(self, line_edit):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            line_edit.setText(folder_path + "/")

    def update_ui_for_layer_mode(self):
        is_single_layer = self.single_layer.isChecked()

        self.known_material_label.setVisible(not is_single_layer)
        self.known_material_id.setVisible(not is_single_layer)
        self.unknown_layer_label.setVisible(not is_single_layer)
        self.unknown_layer.setVisible(not is_single_layer)
        self.account_air_gap.setVisible(not is_single_layer)
        self.forced_air_gap.setVisible(not is_single_layer)

        if is_single_layer:
            self.air_gap_thickness_label.setVisible(False)
            self.air_gap_thickness_guess.setVisible(False)
            self.air_gap_layer_label.setVisible(False)
            self.air_gap_layer.setVisible(False)
        else:
            self.update_ui_for_air_gap()

    def update_ui_for_air_gap(self):
        is_single_layer = self.single_layer.isChecked()
        account_air_gap = self.account_air_gap.isChecked()

        show_air_gap = not is_single_layer and account_air_gap

        self.air_gap_layer_label.setVisible(show_air_gap)
        self.air_gap_layer.setVisible(show_air_gap)
        self.forced_air_gap.setVisible(show_air_gap)
        self.air_gap_thickness_label.setVisible(show_air_gap)
        self.air_gap_thickness_guess.setVisible(show_air_gap)

    def update_base_folder_visibility(self):
        is_generated = self.generated_data.isChecked()
        self.base_folder_label.setVisible(not is_generated)
        self.base_folder.setVisible(not is_generated)

    def update_paths(self):
        is_single_layer = self.single_layer.isChecked()
        account_air_gap = self.account_air_gap.isChecked()
        forced_air_gap = self.forced_air_gap.isChecked()
        is_generated = self.generated_data.isChecked()

        unknown_material = self.unknown_material_id.text()
        known_material = self.known_material_id.text()
        unknown_layer_idx = self.unknown_layer.value()
        thickness = self.thickness_id.text()
        trl_id = self.trl_id.value()

        config_base = self.config_base_folder.text()
        band_display = self.band_selector.currentText()  # "J-Band", "W-Band", "D-Band"
        band_name = band_display.replace("-", "")  # "JBand", "WBand", "DBand" for file names

        air_gap_str = '-air-' if account_air_gap else '-'

        if not is_single_layer:
            layer_str = '3layers' if account_air_gap else '2layers'
            if unknown_layer_idx == 0:
                material = f'{unknown_material}{air_gap_str}{known_material}' if forced_air_gap \
                    else f'{unknown_material}-{known_material}'
                bench_config_file = f'{config_base}bench_{band_name}_{layer_str}_{unknown_material}{air_gap_str}{known_material}.toml'
            else:
                material = f'{known_material}{air_gap_str}{unknown_material}' if forced_air_gap \
                    else f'{known_material}-{unknown_material}'
                bench_config_file = f'{config_base}bench_{band_name}_{layer_str}_{known_material}{air_gap_str}{unknown_material}.toml'
        else:
            material = unknown_material
            bench_config_file = f'{config_base}bench_{band_name}.toml'

        if is_generated:
            s2p_folder = f'./s2p/{material}_sim/'
        else:
            base = self.base_folder.text()
            s2p_folder = f'{base}{material}_{thickness}/trl{trl_id:02d}/'

        self.config_path_display.setText(bench_config_file)
        self.s2p_path_display.setText(s2p_folder)

        self.current_config_path = bench_config_file
        self.current_s2p_path = s2p_folder
        self.current_material = material

    def log(self, message):
        self.log_output.append(message)

    def load_data(self):
        try:
            self.log("Loading data...")
            self.update_paths()

            if not self.current_config_path or not self.current_s2p_path:
                self.log("❌ Error: Paths are empty")
                return

            self.log(f"Config: {self.current_config_path}")
            self.log(f"S2P folder: {self.current_s2p_path}")
            self.log(f"Material: {self.current_material}")
            self.fitter = EnhancedInverseProblem(
                config_file=self.current_config_path,
                unknown_layer=self.unknown_layer.value() if not self.single_layer.isChecked() else 0,
                air_gap_layer=self.air_gap_layer.value() if not self.single_layer.isChecked() else None,
                score_fn=lsq_score)

            self.fitter.load_experimental_data(
                self.current_s2p_path,
                n_angles_to_use=self.num_angles_used.value(),
                poly_fit_degree=self.poly_degree.value(),
                filter_window_length=self.filter_window.value(),
                filter_poly_order=self.filter_poly.value()
            )

            self.log(f"✅ Data loaded!")
            self.log(f"   Angles: {self.fitter.theta_y_deg_array}")
            self.log(f"   Frequencies: {len(self.fitter.frequencies_ghz)} points")

            self.estimate_btn.setEnabled(True)
            self.plot_raw_data()

        except Exception as e:
            import traceback
            self.log(f"❌ Error: {str(e)}")
            self.log(traceback.format_exc())

    def start_estimation(self):
        if self.fitter is None:
            self.log("❌ Error: Load data first")
            return

        try:
            is_single_layer = self.single_layer.isChecked()
            account_air_gap = self.account_air_gap.isChecked()

            if is_single_layer or not account_air_gap:
                initial_guess_thickness = (
                    self.unknown_thickness_guess.value(),
                    self.eps_real.value(),
                    self.eps_imag.value()
                )
            else:
                initial_guess_thickness = (
                    self.unknown_thickness_guess.value(),
                    self.air_gap_thickness_guess.value(),
                    self.eps_real.value(),
                    self.eps_imag.value()
                )

            freq_step_thickness = self.freq_step_1.value()
            freq_step_permittivity = self.freq_step_2.value()

            self.log(f"Starting estimation...")
            self.log(f"Pass 1 guess: {initial_guess_thickness}")
            self.log(f"Pass 1 step: {freq_step_thickness}, Pass 2 step: {freq_step_permittivity}")

            self.estimate_btn.setEnabled(False)
            self.load_btn.setEnabled(False)
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 0)

            self.worker = EstimationWorker(
                self.fitter, GBTC, initial_guess_thickness,
                freq_step_thickness, freq_step_permittivity
            )
            self.worker.two_passes = self.use_two_passes.isChecked()

            self.worker.signals.log.connect(self.log)
            self.worker.signals.finished.connect(self.on_estimation_finished)
            self.worker.signals.error.connect(self.on_estimation_error)

            self.worker.start()

        except Exception as e:
            import traceback
            self.log(f"❌ Error: {str(e)}")
            self.log(traceback.format_exc())
            self.reset_controls()

    def on_estimation_finished(self, results):
        self.results = results
        self.plot_results()
        self.reset_controls()

    def on_estimation_error(self, error_msg):
        self.log(error_msg)
        self.reset_controls()

    def reset_controls(self):
        self.estimate_btn.setEnabled(True)
        self.load_btn.setEnabled(True)
        self.progress_bar.setVisible(False)

    def plot_raw_data(self):
        if self.fitter is None:
            return

        self.s21_canvas.fig.clear()
        n_angles = len(self.fitter.theta_y_deg_array)

        axes = self.s21_canvas.fig.subplots(n_angles, 2)
        if n_angles == 1:
            axes = [axes]

        for i, angle in enumerate(self.fitter.theta_y_deg_array):
            axes[i][0].plot(self.fitter.frequencies_ghz,
                            self.fitter.raw_data[i].s_db[:, 1, 0],
                            'o-', alpha=0.2, label='Raw', markersize=2)
            axes[i][0].plot(self.fitter.frequencies_ghz,
                            self.fitter.data_list[i].s_db[:, 1, 0],
                            '-', linewidth=4, label='Processed')
            axes[i][0].set_ylabel(f'θ={angle}°\n|S21| (dB)')
            axes[i][0].legend()
            axes[i][0].grid(True, alpha=0.3)

            axes[i][1].plot(self.fitter.frequencies_ghz,
                            np.angle(self.fitter.raw_data[i].s[:, 1, 0]),
                            'o-', alpha=0.2, label='Raw', markersize=2)
            axes[i][1].plot(self.fitter.frequencies_ghz,
                            np.angle(self.fitter.data_list[i].s[:, 1, 0]),
                            '-', linewidth=4, label='Processed')
            axes[i][1].set_ylabel('∠S21 (rad)')
            axes[i][1].legend()
            axes[i][1].grid(True, alpha=0.3)

        axes[-1][0].set_xlabel('Frequency (GHz)')
        axes[-1][1].set_xlabel('Frequency (GHz)')

        self.s21_canvas.fig.tight_layout()
        self.s21_canvas.draw()

    def plot_results(self):
        if self.results is None or self.fitter is None:
            return

        self.plot_s21_comparison()
        self.plot_s11_comparison()
        self.plot_permittivity()

    def plot_s21_comparison(self):
        self.s21_canvas.fig.clear()
        sweep_data = self.results['sweep_data']
        n_angles = len(self.fitter.theta_y_deg_array)

        axes = self.s21_canvas.fig.subplots(n_angles, 2)
        if n_angles == 1:
            axes = [axes]

        for i, angle in enumerate(self.fitter.theta_y_deg_array):
            angle_str = f'{angle:.2f}'

            # Plot raw data with 30% opacity
            axes[i][0].plot(self.fitter.frequencies_ghz,
                            self.fitter.raw_data[i].s_db[:, 1, 0],
                            'o-', alpha=0.2, label='Raw', markersize=2)
            axes[i][0].plot(self.fitter.frequencies_ghz,
                            self.fitter.data_list[i].s_db[:, 1, 0],
                            '-', label='Measured', linewidth=4)
            axes[i][0].plot(self.fitter.frequencies_ghz,
                            sweep_data[angle_str].s_db[:, 1, 0],
                            label='Estimated', linewidth=4)
            axes[i][0].set_ylabel(f'θ={angle}°\n|S21| (dB)')
            axes[i][0].legend()
            axes[i][0].grid(True, alpha=0.3)

            axes[i][1].plot(self.fitter.frequencies_ghz,
                            np.angle(self.fitter.raw_data[i].s[:, 1, 0]),
                            'o-', alpha=0.2, label='Raw', markersize=2)
            axes[i][1].plot(self.fitter.frequencies_ghz,
                            np.angle(self.fitter.data_list[i].s[:, 1, 0]),
                            '-', label='Measured', linewidth=4)
            axes[i][1].plot(self.fitter.frequencies_ghz,
                            np.angle(sweep_data[angle_str].s[:, 1, 0]),
                            label='Estimated', linewidth=4)
            axes[i][1].set_ylabel('∠S21 (rad)')
            axes[i][1].legend()
            axes[i][1].grid(True, alpha=0.3)

        axes[-1][0].set_xlabel('Frequency (GHz)')
        axes[-1][1].set_xlabel('Frequency (GHz)')

        self.s21_canvas.fig.tight_layout()
        self.s21_canvas.draw()

    def plot_s11_comparison(self):
        self.s11_canvas.fig.clear()
        sweep_data = self.results['sweep_data']

        ax1, ax2 = self.s11_canvas.fig.subplots(2, 1)
        s2p_file_ang0 = self.fitter.angles_pairs[0]
        path1 = os.path.join(self.current_s2p_path, s2p_file_ang0[0])
        path2 = os.path.join(self.current_s2p_path, s2p_file_ang0[1])
        raw_s2p_ang0, s2p_ang0 = load_parameters(path1, path2, 71, 5)

        # Plot raw data with 30% opacity
        ax1.plot(self.fitter.frequencies_ghz,
                 raw_s2p_ang0.s_db[:, 0, 0],
                 'o-', alpha=0.2, label='Raw', markersize=2)
        ax1.plot(self.fitter.frequencies_ghz,
                 s2p_ang0.s_db[:, 0, 0],
                 '-', label='Measured', linewidth=3)
        ax1.plot(self.fitter.frequencies_ghz,
                 sweep_data['0.00'].s_db[:, 0, 0],
                 '-', label='Estimated', linewidth=3)
        ax1.set_ylabel('|S11| (dB)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        ax2.plot(self.fitter.frequencies_ghz,
                 np.unwrap(np.angle(raw_s2p_ang0.s[:, 0, 0])),
                 'o-', alpha=0.2, label='Raw', markersize=2)
        ax2.plot(self.fitter.frequencies_ghz,
                 np.unwrap(np.angle(s2p_ang0.s[:, 0, 0])),
                 '-', label='Measured', linewidth=3)
        ax2.plot(self.fitter.frequencies_ghz,
                 np.unwrap(np.angle(sweep_data['0.00'].s[:, 0, 0])),
                 '-', label='Estimated', linewidth=3)
        ax2.set_xlabel('Frequency (GHz)')
        ax2.set_ylabel('∠S11 (rad)')
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        self.s11_canvas.fig.tight_layout()
        self.s11_canvas.draw()

    def plot_permittivity(self):
        self.eps_canvas.fig.clear()

        ax1, ax2 = self.eps_canvas.fig.subplots(2, 1)

        freqs = self.fitter.frequencies_ghz
        epsr_est = self.results['epsr_est']
        epsr_raw = self.results['epsr_raw']

        # Plot initial permittivity if available
        try:
            if hasattr(self.fitter, 'stack') and self.fitter.stack is not None:
                unknown_layer_idx = self.unknown_layer.value() if not self.single_layer.isChecked() else 0
                initial_epsr = self.fitter.stack.layers[unknown_layer_idx].material.epsr(freqs)

                ax1.plot(freqs, np.real(initial_epsr),
                         ':', linewidth=2, color='gray', label='Initial (config)')
                ax2.plot(freqs, np.imag(initial_epsr),
                         ':', linewidth=2, color='gray', label='Initial (config)')
        except Exception as e:
            print(f"Could not plot initial permittivity: {e}")

        ax1.plot(freqs, np.real(epsr_raw(freqs)),
                 'o', alpha=0.5, label='Raw estimation')
        ax1.plot(freqs, np.real(epsr_est(freqs)),
                 '-', linewidth=2, label='Fitted')
        ax1.set_ylabel("ε' (Real part)")
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        ax2.plot(freqs, np.imag(epsr_raw(freqs)),
                 'o', alpha=0.5, label='Raw estimation')
        ax2.plot(freqs, np.imag(epsr_est(freqs)),
                 '-', linewidth=2, label='Fitted')
        ax2.set_xlabel('Frequency (GHz)')
        ax2.set_ylabel("ε'' (Imaginary part)")
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        self.eps_canvas.fig.tight_layout()
        self.eps_canvas.draw()


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("PyCarMat Enhanced Material Characterization")
    app.setOrganizationName("IMT Atlantique")

    window = MainWindow()
    window.showMaximized()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()