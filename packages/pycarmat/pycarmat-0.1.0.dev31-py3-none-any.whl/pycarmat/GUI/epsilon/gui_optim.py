import sys
import traceback
import warnings
from copy import deepcopy
from pathlib import Path
from time import sleep

from scipy.constants import c
from scipy.interpolate import interp1d

from matplotlib import rcParams

from pycarmat.GUI.epsilon import PermittivityEditDialog, OptimizationWorker
from pycarmat.inverse_model.tools import load_s2p_file, compute_s11_with_phase_correction

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)

from numpy import full_like, nan, log10, abs, array, real, imag, angle, exp, pi, genfromtxt
from qosm import load_config_from_toml, filter_s2p, PW, GBTC

# PySide6 imports
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                               QTabWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox, QProgressBar,
                               QFileDialog, QMessageBox, QGroupBox, QDialog, QDoubleSpinBox)
from PySide6.QtCore import QTimer
from PySide6.QtGui import QDoubleValidator, QIntValidator

# Matplotlib imports for PySide6
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib

matplotlib.use('Qt5Agg')


def s11_factor(s11, s22, thickness, freq_ghz):
    """
    Calculate S11 reflection parameter with phase correction.

    Applies phase correction based on sample thickness to account for
    the physical distance traveled by the electromagnetic wave.

    Args:
        s11 (complex): S11 reflection parameter (port 1)
        s22 (complex): S22 reflection parameter (port 2)
        thickness (float): Total sample thickness in meters
        freq_ghz (float): Frequency in GHz

    Returns:
        complex: Phase-corrected S11 parameter

    Formula:
        k0 = 2π × frequency / c (wave number in free space)
        f = exp(-j × k0 × thickness) (phase shift factor)
        S11_corrected = |S11 × S22| × exp(j × angle(S11 × S22 × f))
    """
    k0 = 2 * pi * freq_ghz * 1e9 / c
    f = exp(-1j * k0 * thickness)
    return abs(s11 * s22) * exp(1j * angle(s11 * s22 * f))


class OptimizationGUI(QMainWindow):
    """
        Main GUI window for multi-start permittivity estimation using S-parameter optimization.

        This class provides a comprehensive interface for:
        - Loading S2P measurement files and configuration files
        - Setting up optimization parameters
        - Running multi-start optimization algorithms
        - Visualizing results with multiple plots
        - Editing and exporting permittivity data

        Attributes:
            s2p_file_path (str): Path to the loaded S2P file
            config_file_path (str): Path to the loaded TOML configuration file
            optimization_result (dict): Dictionary containing optimization results
            frequencies (ndarray): Array of frequency values from measurements
            s21_s12_measured (ndarray): Measured S21/S12 transmission parameters
            s11_measured (ndarray): Measured S11 reflection parameters
            config (dict): Configuration dictionary loaded from TOML file
            realtime_thickness_data (list): Real-time thickness values during optimization
            realtime_error_data (list): Real-time error values during optimization
            is_dark_mode (bool): Flag indicating if dark mode is active
    """

    def __init__(self):
        """
        Initialize the OptimizationGUI window.

        Sets up the main window, initializes all variables, detects system theme,
        configures matplotlib styling, and builds the user interface.
        """
        super().__init__()
        self.setWindowTitle("Multi-start Permittivity Estimation")

        # Initialize variables
        self.s2p_file_path = ""
        self.config_file_path = ""
        self.optimization_result = None
        self.frequencies = None
        self.s21_s12_measured = None
        self.s11_measured = None
        self.s22_measured = None
        self.config = None

        # Real-time plot data
        self.realtime_thickness_data = []
        self.realtime_error_data = []

        # Setup UI
        self.setup_ui()

    def setup_ui(self):
        """
        Set up the complete user interface.

        Creates the main layout structure with:
        - Central widget and main vertical layout
        - Tab widget for different views
        - Optimization and results tabs
        """

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout(central_widget)

        # Create tab widget
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        # Setup tabs - On enlève le tab Files
        self.setup_optimization_tab()
        self.setup_results_tab()

    def setup_optimization_tab(self):
        """
        Set up the optimization parameters tab with file loading section at the top.

        Creates a comprehensive interface including:
        - File selection group (S2P and configuration files)
        - Optimization parameters group (thickness, permittivity ranges)
        - Optimization controls (start/stop buttons, method selection)
        - Progress bar and status display
        """
        opt_tab = QWidget()
        self.tab_widget.addTab(opt_tab, "Optimization Parameters")

        # Main vertical layout for the tab
        tab_main_layout = QGridLayout(opt_tab)

        # Left side: Parameters
        params_widget = QWidget()
        params_widget.setMaximumWidth(400)
        params_layout = QVBoxLayout(params_widget)

        # === SECTION FICHIERS EN HAUT ===
        file_group = QGroupBox("File Selection")
        file_layout = QGridLayout(file_group)

        # S2P file
        file_layout.addWidget(QLabel("S2P File:"), 0, 0)
        self.s2p_file_edit = QLineEdit()
        file_layout.addWidget(self.s2p_file_edit, 0, 1)
        self.s2p_browse_btn = QPushButton("Browse")
        self.s2p_browse_btn.clicked.connect(self.browse_s2p_file)
        file_layout.addWidget(self.s2p_browse_btn, 0, 2)

        # Config file
        file_layout.addWidget(QLabel("Config TOML File:"), 1, 0)
        self.config_file_edit = QLineEdit()
        file_layout.addWidget(self.config_file_edit, 1, 1)
        self.config_browse_btn = QPushButton("Browse")
        self.config_browse_btn.clicked.connect(self.browse_config_file)
        file_layout.addWidget(self.config_browse_btn, 1, 2)

        # Load button
        self.load_files_btn = QPushButton("Load Files")
        self.load_files_btn.setObjectName("load_files_btn")
        self.load_files_btn.clicked.connect(self.load_files)
        file_layout.addWidget(self.load_files_btn, 2, 1)

        # Edit Layers button
        self.edit_permittivity_btn = QPushButton("Edit Layers")
        self.edit_permittivity_btn.clicked.connect(self.edit_layers)
        self.edit_permittivity_btn.setEnabled(False)
        file_layout.addWidget(self.edit_permittivity_btn, 2, 0)

        params_layout.addWidget(file_group)

        # File information
        info_group = QGroupBox("File Information")
        info_layout = QVBoxLayout(info_group)
        self.file_info_text = QTextEdit()
        info_layout.addWidget(self.file_info_text)
        params_layout.addWidget(info_group)

        # === ESTIMATION PARAMETERS ===
        params_group = QGroupBox("Optimization Parameters")
        params_group_layout = QVBoxLayout(params_group)

        # Create tab widget for optimization parameters
        opt_params_tabs = QTabWidget()
        params_group_layout.addWidget(opt_params_tabs)

        # ===== TAB: PERMITTIVITY =====
        epsilon_tab = QWidget()
        epsilon_tab_layout = QVBoxLayout(epsilon_tab)

        epsilon_group = QGroupBox("Multi-start permittivity estimation")
        epsilon_group.setStyleSheet('border: 0')
        epsilon_layout = QGridLayout(epsilon_group)

        epsilon_layout.addWidget(QLabel("Layer to optimize:"), 0, 0)
        self.layer_epsilon_combo = QComboBox()
        epsilon_layout.addWidget(self.layer_epsilon_combo, 0, 1)
        self.layer_epsilon_combo.currentTextChanged.connect(self.display_permittivity_options)

        self.epsilon_label = QLabel("Real Epsilon:")
        self.num_epsilon_starts_edit = QDoubleSpinBox(prefix='Num. starts  ', decimals=0, minimum=1, value=1)
        self.epsilon_min_edit = QDoubleSpinBox(prefix='From  ', minimum=1, maximum=20, decimals=5, value=2.5)
        self.epsilon_max_edit = QDoubleSpinBox(prefix='To  ', minimum=1, maximum=20, decimals=5, value=2.5)
        epsilon_layout.addWidget(self.epsilon_label, 1, 0)
        epsilon_layout.addWidget(self.num_epsilon_starts_edit, 1, 1)
        epsilon_layout.addWidget(self.epsilon_min_edit, 2, 1)
        epsilon_layout.addWidget(self.epsilon_max_edit, 3, 1)
        self.num_epsilon_starts_edit.valueChanged.connect(self.display_permittivity_options)

        self.epsilon_im_label = QLabel("Imag Epsilon:")
        epsilon_layout.addWidget(self.epsilon_im_label, 4, 0)
        self.epsilon_im_edit = QDoubleSpinBox(minimum=-10, maximum=-0.00001, decimals=5, value=-0.0001)
        epsilon_layout.addWidget(self.epsilon_im_edit, 4, 1)

        epsilon_tab_layout.addWidget(epsilon_group)
        epsilon_tab_layout.addStretch()
        opt_params_tabs.addTab(epsilon_tab, "Permittivity")
        self.display_permittivity_options()

        # ===== TAB: THICKNESS =====
        thickness_tab = QWidget()
        thickness_tab_layout = QVBoxLayout(thickness_tab)

        thickness_group = QGroupBox("Thickness validation")
        thickness_group.setStyleSheet('border: 0')
        thickness_layout = QGridLayout(thickness_group)

        thickness_layout.addWidget(QLabel("Layer to optimize:"), 0, 0)
        self.layer_thickness_combo = QComboBox()
        self.layer_thickness_combo.currentIndexChanged.connect(self.update_thickness_from_selected_layer)
        thickness_layout.addWidget(self.layer_thickness_combo, 0, 1)

        thickness_layout.addWidget(QLabel("Thickness Guess(es):"), 1, 0)
        self.thickness_min_edit = QDoubleSpinBox(prefix='From  ', value=0.00001, minimum=0, maximum=50, decimals=5,
                                                 suffix=' mm')
        self.thickness_max_edit = QDoubleSpinBox(prefix='To  ', value=0.00001, minimum=0, maximum=50, decimals=5,
                                                 suffix=' mm')
        self.num_thickness_points_edit = QDoubleSpinBox(prefix='Num. pts  ', decimals=0, value=11, minimum=1,
                                                        maximum=201)
        self.num_thickness_points_edit.valueChanged.connect(self.display_thickness_options)

        thickness_layout.addWidget(self.num_thickness_points_edit, 1, 1)
        thickness_layout.addWidget(self.thickness_min_edit, 2, 1)
        thickness_layout.addWidget(self.thickness_max_edit, 3, 1)

        thickness_tab_layout.addWidget(thickness_group)
        thickness_tab_layout.addStretch()
        opt_params_tabs.addTab(thickness_tab, "Thickness")

        # ===== TAB: FREQUENCY =====
        freq_tab = QWidget()
        freq_tab_layout = QVBoxLayout(freq_tab)


        freq_step_group = QGroupBox("Frequency range used for estimation")
        freq_step_group.setStyleSheet('border: 0')
        freq_step_layout = QGridLayout(freq_step_group)

        self.freq_step_edit = QDoubleSpinBox(prefix='1 step = ', suffix=' sample(s)', minimum=1, maximum=100, value=50,
                                            decimals=0)
        freq_step_layout.addWidget(self.freq_step_edit, 0, 0)

        freq_tab_layout.addWidget(freq_step_group)

        freq_group = QGroupBox("Frequency range used for validation")
        freq_group.setStyleSheet('border: 0')
        freq_layout = QGridLayout(freq_group)

        self.freq_min_edit = QDoubleSpinBox(prefix='From  ', suffix=' GHz', minimum=0, maximum=1000, value=230.0)
        freq_layout.addWidget(self.freq_min_edit, 0, 0)

        self.freq_max_edit = QDoubleSpinBox(prefix='To  ', suffix=' GHz', minimum=0, maximum=1000, value=300.0)
        freq_layout.addWidget(self.freq_max_edit, 0, 1)

        freq_tab_layout.addWidget(freq_group)

        freq_tab_layout.addStretch()
        opt_params_tabs.addTab(freq_tab, "Frequency")

        # ===== TAB: OTHER PARAMETERS =====
        other_tab = QWidget()
        other_tab_layout = QVBoxLayout(other_tab)

        other_group = QGroupBox("Other parameters")
        other_group.setStyleSheet('border: 0')
        other_layout = QGridLayout(other_group)

        other_layout.addWidget(QLabel("Model:"), 0, 0)
        self.model_combo = QComboBox()
        self.model_combo.addItems(["PW", "GBTC"])
        self.model_combo.currentTextChanged.connect(self.on_model_changed)
        other_layout.addWidget(self.model_combo, 0, 1)

        other_layout.addWidget(QLabel("Window size:"), 1, 0)
        self.fws_edit = QDoubleSpinBox(value=41, decimals=0, minimum=0, maximum=151)
        other_layout.addWidget(self.fws_edit, 1, 1)

        other_layout.addWidget(QLabel("Filter poly-order:"), 2, 0)
        self.fpo_edit = QDoubleSpinBox(value=3, decimals=0, minimum=1, maximum=10)
        other_layout.addWidget(self.fpo_edit, 2, 1)

        # Reflections parameter - only for GBTC
        self.reflections_label = QLabel("Reflections:")
        other_layout.addWidget(self.reflections_label, 3, 0)
        self.num_reflections_edit = QLineEdit("6")
        self.num_reflections_edit.setValidator(QIntValidator())
        other_layout.addWidget(self.num_reflections_edit, 3, 1)

        other_layout.addWidget(QLabel("Metric:"), 4, 0)
        self.metric_combo = QComboBox()
        self.metric_combo.addItems(["r2", "L2", "tanh", "lsq", "correlation"])
        other_layout.addWidget(self.metric_combo, 4, 1)

        other_layout.addWidget(QLabel("Error Mode:"), 5, 0)
        self.error_mode_combo = QComboBox()
        self.error_mode_combo.addItems(["S11", "S21", "S11 & S21"])
        other_layout.addWidget(self.error_mode_combo, 5, 1)

        # Initially hide reflections for PW model
        self.on_model_changed("PW")

        other_tab_layout.addWidget(other_group)
        other_tab_layout.addStretch()
        opt_params_tabs.addTab(other_tab, "Other")

        params_layout.addWidget(params_group)

        # Control buttons
        control_group = QGroupBox("Control")
        control_layout = QVBoxLayout(control_group)

        self.optimize_btn = QPushButton("Start Optimization")
        self.optimize_btn.setObjectName("optimize_btn")
        self.optimize_btn.clicked.connect(self.start_optimization)
        control_layout.addWidget(self.optimize_btn)

        self.stop_btn = QPushButton("Stop Optimization")
        self.stop_btn.setObjectName("stop_btn")
        self.stop_btn.clicked.connect(self.stop_optimization)
        self.stop_btn.setVisible(False)
        control_layout.addWidget(self.stop_btn)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("%p% - Optimizing thickness...")
        self.progress_bar.setVisible(False)
        control_layout.addWidget(self.progress_bar)

        params_layout.addWidget(control_group)
        params_layout.addStretch()

        tab_main_layout.addWidget(params_widget, 0, 0, 2, 1)

        # Right side: Real-time plot
        plot_widget = QWidget()
        plot_layout = QVBoxLayout(plot_widget)

        plot_group = QGroupBox("Real-time Optimization Progress")
        plot_group_layout = QVBoxLayout(plot_group)

        # Create matplotlib figure
        self.realtime_fig = Figure()
        self.realtime_canvas = FigureCanvas(self.realtime_fig)
        self.realtime_ax = self.realtime_fig.add_subplot(111)

        self.realtime_ax.set_xlabel('Thickness [mm]')
        self.realtime_ax.set_ylabel('Total Error')
        self.realtime_ax.set_title('Optimization Error vs Thickness')

        plot_group_layout.addWidget(self.realtime_canvas)
        plot_layout.addWidget(plot_group)

        tab_main_layout.addWidget(plot_widget, 0, 1)

        # Bottom: Log
        log_group = QGroupBox("Optimization Log")
        log_layout = QVBoxLayout(log_group)
        self.log_text = QTextEdit()
        log_layout.addWidget(self.log_text)
        log_group.setFixedHeight(150)

        # Add log to tab layout
        tab_main_layout.addWidget(log_group, 1, 1)

    def setup_results_tab(self):
        """
        Set up the results tab for displaying optimization outputs.

        Creates interface elements including:
        - Results text display area showing optimized parameters
        - Matplotlib figure canvas for result plots (6 subplots)
        - Export buttons for saving plots and permittivity data
        """
        results_tab = QWidget()
        self.tab_widget.addTab(results_tab, "Results")

        layout = QVBoxLayout(results_tab)

        # Results info
        results_group = QGroupBox("Optimization Results")
        results_layout = QVBoxLayout(results_group)
        self.results_text = QTextEdit()
        self.results_text.setMaximumHeight(150)
        results_layout.addWidget(self.results_text)
        layout.addWidget(results_group)

        # Plots
        plots_group = QGroupBox("Results Plots")
        plots_layout = QVBoxLayout(plots_group)

        self.results_fig = Figure(figsize=(15, 8))

        self.results_canvas = FigureCanvas(self.results_fig)
        plots_layout.addWidget(self.results_canvas)
        layout.addWidget(plots_group)

        # Export buttons
        export_layout = QHBoxLayout()
        export_layout.addStretch()

        self.save_plots_btn = QPushButton("Save Plots")
        self.save_plots_btn.clicked.connect(self.save_plots)
        export_layout.addWidget(self.save_plots_btn)

        self.export_permittivity_btn = QPushButton("Export Permittivity")
        self.export_permittivity_btn.clicked.connect(self.export_permittivity)
        export_layout.addWidget(self.export_permittivity_btn)

        layout.addLayout(export_layout)

    def edit_layers(self):
        """
        Open the permittivity edit dialog for manual layer editing.

        Displays a dialog allowing users to:
        - View current layer configurations
        - Edit permittivity values for each layer
        - Modify layer properties

        Updates the layer selection dropdown if changes are accepted.
        Shows a warning if configuration file hasn't been loaded yet.
        """
        if not hasattr(self, 'config') or not self.config:
            QMessageBox.warning(self, "Warning", "Please load configuration file first")
            return

        dialog = PermittivityEditDialog(self.config, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Configuration has been updated
            self.update_layer_selection()

    def on_model_changed(self, model_name):
        """
        Handle model selection change (PW vs GBTC).

        Args:
            model_name (str): Selected model name ("PW" or "GBTC")

        Behavior:
            - Shows/hides the reflections parameter based on model
            - GBTC model requires number of reflections parameter
            - PW model does not use reflections
        """
        if model_name == "GBTC":
            # Show reflections parameter for GBTC
            self.reflections_label.setVisible(True)
            self.num_reflections_edit.setVisible(True)
        else:  # PW
            # Hide reflections parameter for PW
            self.reflections_label.setVisible(False)
            self.num_reflections_edit.setVisible(False)

    def browse_s2p_file(self):
        """
        Open file dialog to select an S2P file.

        S2P files contain two-port S-parameters in Touchstone format.
        Updates the S2P file path and displays it in the UI.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select S2P File", "", "S2P Files (*.s2p);;All Files (*)"
        )
        if file_path:
            self.s2p_file_path = file_path
            self.s2p_file_edit.setText(file_path)

    def browse_config_file(self):
        """
        Open file dialog to select a TOML configuration file.

        Configuration files contain material properties, layer definitions,
        and optimization parameters. Updates the config file path and displays it in the UI.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select TOML Configuration File", "", "TOML Files (*.toml);;All Files (*)"
        )
        if file_path:
            self.config_file_path = file_path
            self.config_file_edit.setText(file_path)

    def load_files(self):
        """
        Load and process S2P measurement file and TOML configuration file.

        Process:
        1. Validates that both file paths are set
        2. Loads S2P file and extracts S-parameters:
           - Frequencies (converted to GHz)
           - S21 and S12 transmission parameters (averaged)
           - S11 reflection parameter
        3. Loads TOML configuration with material properties
        4. Applies model-specific settings (reflections for GBTC)
        5. Updates UI elements:
           - Layer selection dropdown
           - File information display
           - Measured parameters plots
           - Real-time plot initialization

        Raises:
            QMessageBox: Critical error if files are missing or loading fails

        Side Effects:
            - Sets self.frequencies, self.s21_s12_measured, self.s11_measured
            - Sets self.config with loaded configuration
            - Enables edit permittivity button
            - Updates file info text area
            - Initializes plots with measurement data
        """
        if not self.s2p_file_path:
            QMessageBox.critical(self, "Error", "Please select an S2P file")
            return

        if not self.config_file_path:
            QMessageBox.critical(self, "Error", "Please select a configuration file")
            return

        try:
            # Load S2P file
            mut = load_s2p_file(self.s2p_file_path, int(self.fws_edit.text()), int(self.fpo_edit.text()))
            self.frequencies = mut.f * 1e-9  # Convert to GHz

            # Extract measured S-parameters
            s21_measured_complex = mut.s[:, 1, 0]
            s12_measured_complex = mut.s[:, 0, 1]
            self.s21_s12_measured = (s21_measured_complex + s12_measured_complex) / 2.0
            self.s11_measured = mut.s[:, 0, 0]
            self.s22_measured = mut.s[:, 1, 1]

            # Load configuration
            self.config = load_config_from_toml(self.config_file_path)

            # Set num_reflections only if GBTC is selected
            if self.model_combo.currentText() == "GBTC":
                self.config['num_reflections'] = int(self.num_reflections_edit.text())

            self.config['sample_offset'] = (0, 0, 0)
            self.config['sample_attitude_deg'] = (0, 1, 0.)

            # Update layer selection ComboBox
            self.update_layer_selection()

            # Enable edit permittivity button
            self.edit_permittivity_btn.setEnabled(True)

            # Display information
            info = f"S2P file loaded successfully!\n"
            info += f"Number of frequency points: {len(self.frequencies)}\n"
            info += f"Frequency range: {self.frequencies[0]:.1f} - {self.frequencies[-1]:.1f} GHz\n"
            info += f"TOML configuration loaded: {Path(self.config_file_path).name}\n"
            info += f"Available layers: {len(self.config['mut'])}\n"

            # Change Validation frequency range
            self.freq_min_edit.setValue(self.frequencies[0])
            self.freq_max_edit.setValue(self.frequencies[-1])

            self.file_info_text.setPlainText(info)

            # Display measured parameters
            self.display_measured_parameters()

            # Initialize the real-time plot with thickness bounds - ADDED
            self.initialize_realtime_plot()

        except Exception as e:
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Error loading files:\n{str(e)}")

    def initialize_realtime_plot(self):
        """
        Initialize the real-time optimization progress plot with proper axis bounds.

        Sets up the plot display area for tracking optimization iterations:
        - Retrieves thickness min/max bounds from UI fields
        - Configures x-axis limits with 5% margin
        - Sets axis labels and title
        - Applies dark mode styling if active
        - Enables grid display

        Handles exceptions gracefully for invalid thickness values or
        when widgets have been deleted during cleanup.
        """
        try:
            if hasattr(self, 'realtime_ax') and self.realtime_ax is not None:
                # Get thickness bounds from UI
                thickness_min = self.thickness_min_edit.value()
                thickness_max = self.thickness_max_edit.value()
                thickness_num_pts = self.num_thickness_points_edit.value()

                # Set the bounds
                if thickness_num_pts > 1:
                    thickness_range = thickness_max - thickness_min
                    margin = thickness_range * 0.05  # 5% margin
                    self.realtime_ax.set_xlim(thickness_min - margin, thickness_max + margin)
                else:
                    margin = thickness_min * 0.05  # 5% margin
                    self.realtime_ax.set_xlim(thickness_min - margin, thickness_min + margin)

                # Set labels and title
                self.realtime_ax.set_xlabel('Thickness [mm]')
                self.realtime_ax.set_ylabel('Score')
                self.realtime_ax.set_title('Validation Error vs Thickness')

                # Add grid
                self.realtime_ax.grid(True, alpha=0.3)

                # Refresh canvas
                if hasattr(self, 'realtime_canvas') and self.realtime_canvas is not None:
                    self.realtime_canvas.draw()

        except (ValueError, RuntimeError):
            # Handle cases where thickness values are invalid or widgets are deleted
            pass

    def display_permittivity_options(self):
        """
        Show or hide permittivity optimization controls based on layer selection.

        Controls visibility of:
        - Number of epsilon starts field
        - Epsilon min/max range fields
        - Associated labels

        Hides all controls if 'None' is selected or no layer is chosen,
        otherwise displays them for permittivity optimization configuration.
        """
        hidden = self.layer_epsilon_combo.currentText() == 'None' or self.layer_epsilon_combo.currentText() == ''
        self.epsilon_label.setHidden(hidden)
        self.epsilon_im_label.setHidden(hidden)
        self.num_epsilon_starts_edit.setHidden(hidden)
        self.epsilon_min_edit.setHidden(hidden)
        self.epsilon_im_edit.setHidden(hidden)
        self.epsilon_max_edit.setHidden(hidden or self.num_epsilon_starts_edit.value() == 1)
        self.epsilon_min_edit.setPrefix('' if self.num_epsilon_starts_edit.value() == 1 else 'From  ')

    def update_layer_selection(self):
        """
        Update the layer selection ComboBox based on loaded configuration.

        Process:
        1. Clears existing layer combo box items
        2. Populates with layers from config['mut']
        3. Creates descriptive labels using:
           - Layer index
           - Layer name (if available)
           - Layer thickness (if available, converted to mm)
        4. Automatically selects epsilon layer (first layer with epsilon_r = 0)
        5. Updates thickness fields from selected layer

        Requires:
            - self.config must be loaded with 'mut' key containing layer definitions
        """
        if hasattr(self, 'config') and self.config and 'mut' in self.config:
            self.layer_thickness_combo.clear()
            self.layer_epsilon_combo.clear()
            self.layer_epsilon_combo.addItem('None')
            num_layers = len(self.config['mut'])
            sel_epsilon_layer = 0

            # Add layers with descriptions if available
            for i in range(num_layers):
                layer_info = self.config['mut'][i]
                if layer_info["epsilon_r"] == 0:
                    sel_epsilon_layer = i + 1

                # Create descriptive label
                label0 = f"Layer {i}"
                label = f"Layer {i}"
                if 'name' in layer_info:
                    label += f" ({layer_info['name']})"
                elif 'thickness' in layer_info:
                    thickness_mm = layer_info['thickness'] * 1000 if layer_info['thickness'] < 1 else layer_info[
                        'thickness']
                    label += f" ({thickness_mm:.3f}mm)"

                self.layer_thickness_combo.addItem(label)
                self.layer_epsilon_combo.addItem(label0)
                self.layer_epsilon_combo.setCurrentIndex(sel_epsilon_layer)

            # Set initial thickness from selected layer
            if num_layers > 0:
                self.update_thickness_from_selected_layer()

    def update_thickness_from_selected_layer(self):
        """
        Update thickness input fields based on the currently selected layer.

        Retrieves thickness from the selected layer in config and:
        1. Converts units (meters to mm) if thickness < 1
        2. Sets initial thickness value
        3. Sets min/max bounds as ±0.005mm around initial value
        4. Refreshes real-time plot with new thickness bounds

        Handles both meter and millimeter thickness units automatically.
        """
        if hasattr(self, 'config') and self.config and 'mut' in self.config:
            layer_index = self.layer_thickness_combo.currentIndex()
            if 0 <= layer_index < len(self.config['mut']):
                layer = self.config['mut'][layer_index]
                if 'thickness' in layer:
                    # Convert to mm if thickness is in meters (< 1 means likely in meters)
                    thickness_mm = layer['thickness'] * 1000

                    # Update the thickness fields with current layer thickness
                    # Set min/max as ±5% around initial value
                    self.thickness_min_edit.setValue(thickness_mm - thickness_mm*0.05)
                    self.thickness_max_edit.setValue(thickness_mm + thickness_mm*0.05)

                    # Update real-time plot bounds - ADDED
                    self.initialize_realtime_plot()

    def display_thickness_options(self):
        """
        Show or hide thickness optimization controls based on num points value.
        """
        self.thickness_max_edit.setVisible(self.num_thickness_points_edit.value() > 1)
        self.thickness_min_edit.setPrefix('' if self.num_thickness_points_edit.value() == 1 else 'From  ')

    def display_measured_parameters(self):
        """
        Display measured S-parameters in the Results tab plots.

        Creates a 2x3 subplot figure showing:
        - Row 1: S21/S12 transmission (magnitude in dB, phase in degrees)
        - Row 2: S11 reflection (magnitude in dB, phase in degrees)
        - Row 3: Placeholder plots for permittivity (to be filled after optimization)

        Process:
        1. Clears existing results figure
        2. Converts S-parameters to dB and degrees
        3. Applies frequency range filtering
        4. Plots measured data with appropriate styling
        5. Applies dark mode styling if enabled
        6. Adds legends and grid lines

        Handles exceptions and displays error messages if plotting fails.
        """
        try:
            # Create plots
            self.results_fig.clear()
            axes = self.results_fig.subplots(2, 3)

            # Convert to dB
            s21_s12_measured_db = 20. * log10(abs(self.s21_s12_measured))
            s11_measured_db = 20. * log10(abs(self.s11_measured))

            # Get frequency range
            freq_range = (float(self.freq_min_edit.value()), float(self.freq_max_edit.value()))
            freq_mask = (self.frequencies >= freq_range[0]) & (self.frequencies <= freq_range[1])

            # S21 Magnitude
            axes[0, 0].plot(self.frequencies, s21_s12_measured_db, linewidth=3,
                            label='Measured (S21+S12)/2', alpha=0.8)
            axes[0, 0].axvspan(freq_range[0], freq_range[1], alpha=0.15, label='Validation range')
            axes[0, 0].set_xlabel('Frequency [GHz]')
            axes[0, 0].set_ylabel('|(S21+S12)/2| [dB]')
            axes[0, 0].set_title('S21 Parameter - Measured Data')
            axes[0, 0].legend()
            axes[0, 0].grid(True, alpha=0.3)

            # S11 Magnitude
            axes[0, 1].plot(self.frequencies, s11_measured_db, linewidth=3,
                            label='Measured S11', alpha=0.8)
            axes[0, 1].axvspan(freq_range[0], freq_range[1], alpha=0.15, label='Validation range')
            axes[0, 1].set_xlabel('Frequency [GHz]')
            axes[0, 1].set_ylabel('|S11| [dB]')
            axes[0, 1].set_title('S11 Parameter - Measured Data')
            axes[0, 1].legend()
            axes[0, 1].grid(True, alpha=0.3)

            # Placeholder for permittivity
            axes[0, 2].text(0.5, 0.5, 'Real permittivity\nwill appear after\noptimization',
                            ha='center', va='center', transform=axes[0, 2].transAxes, fontsize=12)
            axes[0, 2].set_xlabel('Frequency [GHz]')
            axes[0, 2].set_ylabel("ε'r")
            axes[0, 2].set_title('Real part of permittivity')
            axes[0, 2].grid(True, alpha=0.3)

            # Placeholder for imaginary permittivity
            axes[1, 0].text(0.5, 0.5, 'Imaginary permittivity\nwill appear after\noptimization',
                            ha='center', va='center', transform=axes[1, 0].transAxes, fontsize=12)
            axes[1, 0].set_xlabel('Frequency [GHz]')
            axes[1, 0].set_ylabel('εr"')
            axes[1, 0].set_title('Imaginary part of permittivity')
            axes[1, 0].grid(True, alpha=0.3)

            # S21 complex plane
            axes[1, 1].scatter(real(self.s21_s12_measured[freq_mask]), imag(self.s21_s12_measured[freq_mask]),
                               alpha=0.8, s=30, marker='o')
            axes[1, 1].set_xlabel('Real part S21')
            axes[1, 1].set_ylabel('Imaginary part S21')
            axes[1, 1].set_title('S21 complex plane - Measured Data')
            axes[1, 1].grid(True, alpha=0.3)

            # S11 complex plane
            axes[1, 2].scatter(real(self.s11_measured[freq_mask]), imag(self.s11_measured[freq_mask]),
                               alpha=0.8, s=30, marker='o')
            axes[1, 2].set_xlabel('Real part S11')
            axes[1, 2].set_ylabel('Imaginary part S11')
            axes[1, 2].set_title('S11 complex plane - Measured Data')
            axes[1, 2].grid(True, alpha=0.3)

            # Update results text
            results_info = f"=== MEASURED DATA LOADED ===\n"
            results_info += f"S2P file: {Path(self.s2p_file_path).name}\n"
            results_info += f"Frequency points: {len(self.frequencies)}\n"
            results_info += f"Frequency range: {self.frequencies[0]:.1f} - {self.frequencies[-1]:.1f} GHz\n"
            results_info += f"Optimization range: {freq_range[0]:.1f} - {freq_range[1]:.1f} GHz\n"
            results_info += f"S21 magnitude range: {s21_s12_measured_db.min():.2f} to {s21_s12_measured_db.max():.2f} dB\n"
            results_info += f"S11 magnitude range: {s11_measured_db.min():.2f} to {s11_measured_db.max():.2f} dB\n"
            results_info += f"\nOptimization results will appear here after running optimization.\n"

            self.results_text.setPlainText(results_info)

            self.results_fig.tight_layout()
            self.results_canvas.draw()

        except Exception as e:
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Error displaying measured parameters:\n{str(e)}")

    def log_message(self, message):
        """
        Add a message to the log text area (thread-safe).

        Uses QTimer.singleShot to ensure UI updates are performed on the main thread,
        making it safe to call from worker threads during optimization.

        Args:
            message (str): Message text to append to the log
        """
        # Use QTimer.singleShot for thread-safe UI updates
        QTimer.singleShot(0, lambda: self._update_log(message))

    def _update_log(self, message):
        """
        Internal method to update log text widget.

        Called from the main thread via QTimer.singleShot.
        Handles RuntimeError gracefully if widget has been deleted.

        Args:
            message (str): Message to append
        """
        try:
            if hasattr(self, 'log_text') and self.log_text is not None:
                self.log_text.append(message)
        except RuntimeError:
            # Widget has been deleted, ignore
            pass

    def update_progress(self, value):
        """
        Update progress bar value (thread-safe).

        Uses QTimer.singleShot for thread-safe UI updates from worker threads.

        Args:
            value (int): Progress percentage (0-100)
        """
        QTimer.singleShot(0, lambda: self._update_progress_bar(value))

    def _update_progress_bar(self, value):
        """
        Internal method to update progress bar widget.

        Called from the main thread via QTimer.singleShot.
        Handles RuntimeError gracefully if widget has been deleted.

        Args:
            value (int): Progress value to set (0-100)
        """
        try:
            if hasattr(self, 'progress_bar') and self.progress_bar is not None:
                self.progress_bar.setValue(value)
        except RuntimeError:
            # Widget has been deleted, ignore
            pass

    def update_realtime_plot(self, thickness_mm, total_error):
        """
        Update real-time optimization progress plot with new data point (thread-safe).

        Adds a new point to the thickness vs error plot during optimization iterations.
        Uses QTimer.singleShot to ensure thread-safe UI updates.

        Args:
            thickness_mm (float): Current thickness value in millimeters
            total_error (float): Current total error metric value
        """
        # Use QTimer.singleShot for thread-safe UI updates
        QTimer.singleShot(0, lambda: self._update_plot(thickness_mm, total_error))

    def _update_plot(self, thickness_mm, total_error):
        """
        Internal method to update the real-time plot with new data.

        Process:
        1. Appends new thickness and error values to data lists
        2. Clears and redraws the plot with all accumulated data
        3. Highlights the best (minimum error) point if multiple points exist
        4. Maintains fixed X-axis bounds based on thickness min/max from UI
        5. Auto-adjusts Y-axis to fit all error values

        X-axis bounds are maintained to prevent axis jumping during optimization,
        providing a stable visualization experience.

        Args:
            thickness_mm (float): Thickness value in millimeters
            total_error (float): Total error metric value

        Handles RuntimeError if widgets have been deleted during cleanup.
        """
        try:
            if not hasattr(self, 'realtime_canvas') or self.realtime_canvas is None:
                return

            self.realtime_thickness_data.append(thickness_mm)
            self.realtime_error_data.append(total_error)

            # Update plot
            self.realtime_ax.clear()

            # Use the appropriate color for real-time plot based on mode
            self.realtime_ax.plot(self.realtime_thickness_data, self.realtime_error_data, linewidth=2, marker='o',
                                  markersize=4)
            self.realtime_ax.set_xlabel('Thickness [mm]')
            self.realtime_ax.set_ylabel('Score')
            self.realtime_ax.set_title('Validation Error vs Thickness')

            # Highlight minimum point if we have enough data
            if len(self.realtime_error_data) > 1:
                min_idx = array(self.realtime_error_data).argmin()
                min_thickness = self.realtime_thickness_data[min_idx]
                min_error = self.realtime_error_data[min_idx]
                self.realtime_ax.plot(min_thickness, min_error, 'ro', markersize=8,
                                      label=f'Best: {min_thickness:.5f}mm')
                self.realtime_ax.legend()

            # MAINTAIN X axis limits based on thickness bounds from UI - MODIFIED
            try:
                thickness_min = self.thickness_min_edit.value()
                thickness_max = self.thickness_max_edit.value()
                thickness_range = thickness_max - thickness_min
                margin = thickness_range * 0.02  # 2% margin
                self.realtime_ax.set_xlim(thickness_min - margin, thickness_max + margin)
            except (ValueError, AttributeError):
                # Fallback to auto-adjust if UI values are not available
                if len(self.realtime_thickness_data) > 1:
                    thickness_range = max(self.realtime_thickness_data) - min(self.realtime_thickness_data)
                    self.realtime_ax.set_xlim(min(self.realtime_thickness_data) - thickness_range * 0.1,
                                              max(self.realtime_thickness_data) + thickness_range * 0.1)

            # Auto-adjust Y axis
            if len(self.realtime_error_data) > 1:
                error_range = max(self.realtime_error_data) - min(self.realtime_error_data)
                if error_range > 0:
                    self.realtime_ax.set_ylim(min(self.realtime_error_data) - error_range * 0.1,
                                              max(self.realtime_error_data) + error_range * 0.1)

            self.realtime_canvas.draw()
        except RuntimeError:
            # Widget has been deleted, ignore
            pass

    def stop_optimization(self):
        self.worker.keep_working = False

    def start_optimization(self):
        """
        Start the optimization process in a background thread.

        Process:
        1. Validates that files have been loaded
        2. Validates that layers are available
        3. Disables UI controls and shows progress bar
        4. Clears previous optimization data and logs
        5. Initializes real-time plot with proper bounds
        6. Collects all optimization parameters from UI:
           - Frequency range
           - Thickness parameters (initial, min, max, number of points)
           - Permittivity parameters (min, max, number of starts)
           - Model selection (PW or GBTC)
           - Metric and error mode
           - Layer indices
        7. Validates layer indices
        8. Creates and starts OptimizationWorker thread
        9. Connects worker signals to UI update methods

        The optimization runs asynchronously to keep the UI responsive.
        Progress updates are sent via signals from the worker thread.

        Error Handling:
            Shows error dialogs if:
            - Files haven't been loaded
            - No layers are available
            - Layer indices are invalid
        """
        if self.frequencies is None:
            QMessageBox.critical(self, "Error", "Please load files first")
            return

        if self.layer_thickness_combo.count() == 0:
            QMessageBox.critical(self, "Error", "No layers available. Please load a valid TOML configuration file.")
            return

        # Disable button and show progress - MODIFIED
        self.optimize_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("%p% - Optimizing ...")

        # Clear previous data
        try:
            if hasattr(self, 'log_text') and self.log_text is not None:
                self.log_text.clear()
        except RuntimeError:
            pass

        self.realtime_thickness_data.clear()
        self.realtime_error_data.clear()

        # Initialize real-time plot with proper bounds - ADDED
        self.initialize_realtime_plot()

        # Get parameters
        freq_range = (self.freq_min_edit.value(), self.freq_max_edit.value())
        freq_step = int(self.freq_step_edit.value())

        initial_thickness = self.thickness_min_edit.value() * 1e-3  # Convert mm -> m
        num_thickness_points = int(self.num_thickness_points_edit.value())
        if num_thickness_points > 1:
            thickness_range = (self.thickness_min_edit.value() * 1e-3, self.thickness_max_edit.value() * 1e-3)
        else:
            thickness_range = (self.thickness_min_edit.value() * 1e-3, self.thickness_min_edit.value() * 1e-3)

        num_epsilon_starts = int(self.num_epsilon_starts_edit.value())
        if num_epsilon_starts:
            initial_epsilon_range = (self.epsilon_min_edit.value(), self.epsilon_max_edit.value())
        else:
            initial_epsilon_range = (self.epsilon_min_edit.value(), self.epsilon_min_edit.value())
        initial_im_espilon = self.epsilon_im_edit.value()

        fws = int(self.fws_edit.value())
        fpo = int(self.fpo_edit.value())
        metric = self.metric_combo.currentText()
        thickness_layer_index = self.layer_thickness_combo.currentIndex()
        if self.layer_epsilon_combo.currentText() != 'None':
            epsilon_layer_index = self.layer_epsilon_combo.currentIndex() - 1
        else:
            epsilon_layer_index = -1

        # Validate layer index
        if thickness_layer_index < 0 or thickness_layer_index >= len(self.config['mut']):
            QMessageBox.critical(self, "Error", f"Invalid layer index: {thickness_layer_index}")
            self.finish_optimization()
            return
        if epsilon_layer_index >= len(self.config['mut']):
            QMessageBox.critical(self, "Error", f"Invalid layer index: {epsilon_layer_index}")
            self.finish_optimization()
            return

        # Get selected model
        model_name = self.model_combo.currentText()
        model = PW if model_name == "PW" else GBTC

        # Start worker thread
        self.worker = OptimizationWorker(
            self, self.config, self.frequencies, self.s21_s12_measured, self.s11_measured, self.s22_measured,
            self.s2p_file_path, initial_epsilon_range, initial_im_espilon, thickness_range,
            fws, fpo, num_thickness_points, num_epsilon_starts, freq_range, freq_step, metric, model,
            thickness_layer_index, epsilon_layer_index,
            error_mode=self.error_mode_combo.currentIndex(), config_file_path=self.config_file_path
        )

        # Connect signals - MODIFIED to include progress_value
        self.worker.progress_update.connect(self.log_message)
        self.worker.progress_value.connect(self.update_progress)
        self.worker.plot_update.connect(self.update_realtime_plot)
        self.worker.finished.connect(self.optimization_finished)
        self.worker.error_occurred.connect(self.optimization_error)

        # Start the worker
        self.stop_btn.setVisible(True)
        self.optimize_btn.setVisible(False)
        self.worker.start()

    def optimization_finished(self, result):
        """
        Handle successful completion of optimization.

        Called automatically when the worker thread finishes successfully.

        Args:
            result (dict): Optimization results dictionary containing:
                - optimized_thickness: Final thickness value
                - best_epsilon_result: Best permittivity optimization
                - model: Model class used (PW or GBTC)
                - final_metric: Final error metrics
                - thickness_layer_index: Index of optimized layer
                - epsilon_layer_index: Index of epsilon layer

        Process:
        1. Stores the result for later access
        2. Calculates and displays final results with plots
        3. Re-enables UI controls
        """
        self.optimization_result = result
        self.calculate_final_results()
        self.finish_optimization()

    def optimization_error(self, error_message):
        """
        Handle errors that occur during optimization.

        Called automatically when the worker thread encounters an error.

        Args:
            error_message (str): Description of the error that occurred

        Actions:
        1. Logs the error message
        2. Shows error dialog to user
        3. Re-enables UI controls
        """
        self.log_message(error_message)
        QMessageBox.critical(self, "Error", error_message)
        self.finish_optimization()

    def finish_optimization(self):
        """
        Re-enable UI controls after optimization completes or fails.

        Performs cleanup:
        - Re-enables the optimization start button
        - Hides the progress bar
        - Resets progress bar value to 0

        Called by both optimization_finished() and optimization_error().
        """
        self.optimize_btn.setEnabled(True)
        self.optimize_btn.setVisible(True)
        self.stop_btn.setVisible(False)
        self.progress_bar.setVisible(False)
        self.progress_bar.setValue(0)

    def calculate_final_results(self):
        """
        Calculate and display final optimization results.

        Extracts information from the optimization result and:
        1. Formats a results summary showing:
           - Optimized thickness (in mm)
           - Model used
           - Layer indices optimized
           - Final metric values
        2. Displays the summary in the results text area
        3. Triggers calculation and plotting of final simulations

        Handles exceptions and displays error dialogs if calculation fails.
        """
        try:
            result = self.optimization_result

            # Display optimization results
            results_info = f"=== OPTIMIZATION RESULTS ===\n"
            results_info += f"Optimized thickness: {result['optimized_thickness'] * 1000:.5f} mm\n"
            results_info += f"Model used: {result['model'].__name__}\n"
            results_info += f"Frequency step: {result['freq_step']} sample(s)\n"
            results_info += f"Layer optimized for thickness: {result['thickness_layer_index']}\n"
            results_info += f"Layer optimized for epsilon: {result['epsilon_layer_index']}\n"
            results_info += f"Final S11 metric: {result['final_metric']:.6f}\n"
            results_info += f"Metric used: {result['metric']}\n"
            self.results_text.setPlainText(results_info)

            # Calculate final simulations for plotting
            self.calculate_and_plot_final_simulations()

        except Exception as e:
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Error calculating final results:\n{str(e)}")

    def calculate_and_plot_final_simulations(self):
        """
        Calculate final S-parameter simulations and create comprehensive result plots.

        Process:
        1. Extracts optimized parameters from results
        2. Creates final configuration with optimized thickness
        3. Loads and interpolates CSV permittivity data if needed
        4. Simulates S-parameters for all frequencies using optimized parameters
        5. Creates 2x3 subplot figure showing:
           - S21 magnitude and phase (measured vs optimized)
           - S11 magnitude and phase (measured vs optimized)
           - Complex plane plots for S21 and S11
           - Real and imaginary permittivity vs frequency
        6. Applies dark mode styling if active
        7. Adds legends, grids, and highlights optimization frequency range
        8. Switches to Results tab to display plots

        The plots provide comprehensive comparison between measured data
        and optimized simulations, along with extracted permittivity values.

        Handles exceptions and displays error dialogs if simulation fails.
        """
        try:
            result = self.optimization_result

            # Get the best epsilon result
            best_epsilon_result = result['best_epsilon_result']
            if best_epsilon_result is None:
                # estimation has been aborted
                return

            freq_subset = best_epsilon_result['frequencies']
            eps_opt = best_epsilon_result['eps_complex']

            self.log_message(f"Using best epsilon initial guess: {best_epsilon_result['initial_epsilon']:.6f}")

            # Final configuration with optimized thickness
            config_final = deepcopy(self.config)
            config_final['mut'][result['thickness_layer_index']]['thickness'] = result['optimized_thickness']

            # Interpolation for full simulation

            # Full simulation with optimized parameters
            s21_optimized = full_like(self.frequencies, nan, dtype=complex)
            s12_optimized = full_like(self.frequencies, nan, dtype=complex)
            s11_s22_optimized = full_like(self.frequencies, nan, dtype=complex)
            s11_s22_measured = full_like(self.frequencies, nan, dtype=complex)

            total_thickness = 0
            for mut in config_final['mut']:
                total_thickness += mut['thickness']

            # load csv file for permittivities if needed
            for i, mut in enumerate(config_final['mut']):
                if isinstance(mut['epsilon_r'], str):
                    filepath = mut['epsilon_r'].replace('CSV:', '').replace(' ', '')
                    # If path starts with ./ and we have a config file path, make it relative to config directory
                    if filepath.startswith('./') and self.config_file_path:
                        config_dir = Path(self.config_file_path).parent
                        resolved_path = config_dir / filepath[2:]  # Remove the './' prefix
                        filepath = str(resolved_path)

                    skip_header = 1
                    # check if thickness is stored in the file, if yes update the value
                    with open(filepath, 'r') as f:
                        f.readline()
                        second_line = f.readline().strip()
                        if second_line.startswith('#') and 'Thickness_mm' in second_line:
                            # Extract thickness in mm and store it in meter
                            skip_header = 2
                            thickness_mm = float(second_line.split()[1])
                            config_final['mut'][i]['thickness'] = thickness_mm * .001

                    _data = genfromtxt(filepath, delimiter=',', skip_header=skip_header)
                    # Interpolate CSV data to match frequency points
                    freq_csv = _data[:, 0]  # First column: frequency
                    eps_real_csv = _data[:, 1]  # Second column: real part
                    eps_imag_csv = _data[:, 2]  # Third column: imaginary part

                    # Interpolate to self.frequencies
                    eps_interp = interp1d(freq_csv, eps_real_csv + 1j * eps_imag_csv,
                                          kind='linear', fill_value="extrapolate")

                    # Replace string path with interpolation function
                    config_final['mut'][i]['epsilon_r'] = eps_interp

            # case of no permittivity estimation (only thickness validation)
            if not hasattr(eps_opt, '__len__') and real(eps_opt) < .01:
                eps_opt = config_final['mut'][result['epsilon_layer_index']]['epsilon_r']

            # case of only one complex (not array)
            if not hasattr(eps_opt, '__len__'):
                eps_opt = full_like(self.frequencies, eps_opt, dtype=complex)

            for k, freq_GHz in enumerate(self.frequencies):
                config_final['mut'][result['epsilon_layer_index']]['epsilon_r'] = eps_opt[k]
                s11_opt, s12_opt, s21_opt, s22_opt = result['model'].simulate(config_final, freq_GHz)
                s21_optimized[k] = s21_opt
                s12_optimized[k] = s12_opt
                s11_s22_optimized[k] = compute_s11_with_phase_correction(s11_opt, s22_opt, total_thickness, freq_GHz)
                s11_s22_measured[k] = compute_s11_with_phase_correction(self.s11_measured[k], self.s22_measured[k],
                                                                        total_thickness, freq_GHz)

            # Calculate average
            s21_s12_optimized = (s21_optimized + s12_optimized) / 2.0

            # Create comparison plots
            self.create_comparison_plots(eps_opt, self.frequencies, s21_s12_optimized, s11_s22_optimized, s11_s22_measured)

            # Store data for export
            self.eps_opt = eps_opt
            self.freq_est_opt = self.frequencies

        except Exception as e:
            traceback.print_exc()
            self.log_message(f"Error calculating final simulations: {str(e)}")

    def create_comparison_plots(self, eps_opt, freq_est_opt, s21_s12_optimized, s11_optimized, s11_measured):
        """
        Create comprehensive comparison plots showing measured vs optimized results.

        Generates a 2x3 subplot figure containing:
        - Row 1, Col 1: S21 magnitude (dB) - measured vs optimized
        - Row 1, Col 2: S11 magnitude (dB) - measured vs optimized
        - Row 1, Col 3: Real permittivity (ε') vs frequency
        - Row 2, Col 1: Imaginary permittivity (ε'') vs frequency
        - Row 2, Col 2: S21 complex plane scatter plot
        - Row 2, Col 3: S11 complex plane scatter plot

        Args:
            eps_opt (ndarray): Optimized complex permittivity values
            freq_est_opt (ndarray): Frequency array in GHz
            s21_s12_optimized (ndarray): Optimized S21/S12 transmission parameters
            s11_optimized (ndarray): Optimized S11 reflection parameters

        Features:
        - Highlights optimization frequency range with yellow shading
        - Applies dark/light mode styling
        - Adds legends and grid lines
        - Converts S-parameters to dB for magnitude plots
        - Automatically switches to Results tab after plotting
        """

        # Clear previous plots
        self.results_fig.clear()
        axes = self.results_fig.subplots(2, 3)

        # Convert to dB
        s21_s12_measured_db = 20. * log10(abs(self.s21_s12_measured))
        s21_s12_optimized_db = 20. * log10(abs(s21_s12_optimized))
        s11_optimized_db = 20. * log10(abs(s11_optimized))
        s11_measured_db = 20. * log10(abs(s11_measured))

        freq_range_opt = self.optimization_result['freq_range']
        freq_mask = (self.frequencies >= freq_range_opt[0]) & (self.frequencies <= freq_range_opt[1])

        # S21 Magnitude - Measured vs Optimized
        axes[0, 0].plot(self.frequencies, s21_s12_measured_db, linewidth=3, label='Measured', alpha=0.8)
        axes[0, 0].plot(self.frequencies, s21_s12_optimized_db, linewidth=2.5, label='Model')
        axes[0, 0].axvspan(freq_range_opt[0], freq_range_opt[1], alpha=0.15, label='Validation range')
        axes[0, 0].set_xlabel('Frequency [GHz]')
        axes[0, 0].set_ylabel('$|(S21+S12)/2|$ [dB]')
        axes[0, 0].set_title('S21 Parameter')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)

        # S11 Magnitude - Measured vs Optimized
        axes[0, 1].plot(self.frequencies, s11_measured_db, linewidth=3, label='Measured', alpha=0.8)
        axes[0, 1].plot(self.frequencies, s11_optimized_db, linewidth=2.5, label='Model')
        axes[0, 1].axvspan(freq_range_opt[0], freq_range_opt[1], alpha=0.15, label='Validation range')
        axes[0, 1].set_xlabel('Frequency [GHz]')
        axes[0, 1].set_ylabel('$|S11 \\cdot S22 \\cdot F|$ [dB]')
        axes[0, 1].set_title('S11, S22 Parameters')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)

        # Real permittivity - Optimized
        axes[0, 2].plot(freq_est_opt, real(eps_opt), linewidth=2.5, label='εr')
        axes[0, 2].axvspan(freq_range_opt[0], freq_range_opt[1], alpha=0.15,  label='Optimization range')
        axes[0, 2].set_xlabel('Frequency [GHz]')
        axes[0, 2].set_ylabel("ε'r")
        axes[0, 2].set_title('Real part of permittivity')
        axes[0, 2].legend()
        axes[0, 2].grid(True, alpha=0.3)
        axes[0, 2].ticklabel_format(style='plain', axis='y', useOffset=False)

        # Imaginary permittivity - Optimized
        axes[1, 0].plot(freq_est_opt, imag(eps_opt), linewidth=2.5, label='εr"')
        axes[1, 0].axvspan(freq_range_opt[0], freq_range_opt[1], alpha=0.15, label='Optimization range')
        axes[1, 0].set_xlabel('Frequency [GHz]')
        axes[1, 0].set_ylabel('εr"')
        axes[1, 0].set_title('Imaginary part of permittivity')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        axes[1, 0].ticklabel_format(style='plain', axis='y', useOffset=False)

        # S21 complex plane - Measured vs Optimized
        axes[1, 1].scatter(real(self.s21_s12_measured[freq_mask]), imag(self.s21_s12_measured[freq_mask]),
                           alpha=0.8, s=30, label='Measured', marker='o')
        axes[1, 1].scatter(real(s21_s12_optimized[freq_mask]), imag(s21_s12_optimized[freq_mask]),
                           alpha=0.7, s=25, label='Model', marker='s')
        axes[1, 1].set_xlabel('Real part S21')
        axes[1, 1].set_ylabel('Imaginary part S21')
        axes[1, 1].set_title('S21 complex plane')
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)

        # S11 complex plane - Measured vs Optimized
        axes[1, 2].scatter(real(s11_measured[freq_mask]), imag(s11_measured[freq_mask]),
                           alpha=0.8, s=30, label='Measured', marker='o')
        axes[1, 2].scatter(real(s11_optimized[freq_mask]), imag(s11_optimized[freq_mask]),
                           alpha=0.7, s=25, label='Model', marker='s')
        axes[1, 2].set_xlabel('Real part S11')
        axes[1, 2].set_ylabel('Imaginary part S11')
        axes[1, 2].set_title('S11 complex plane')
        axes[1, 2].legend()
        axes[1, 2].grid(True, alpha=0.3)

        self.results_fig.tight_layout()
        self.results_canvas.draw()

    def save_plots(self):
        """
        Save result plots to an image file.

        Opens a file save dialog allowing the user to save the results figure
        in multiple formats (PNG, PDF, or SVG). Uses high DPI (300) for quality.

        Checks if optimization results exist before attempting to save.

        Supported Formats:
            - PNG (Portable Network Graphics)
            - PDF (Portable Document Format)
            - SVG (Scalable Vector Graphics)

        Displays success or error messages via dialog boxes.
        """
        if self.optimization_result is None:
            QMessageBox.warning(self, "Warning", "No results to save")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Plots", "", "PNG files (*.png);;PDF files (*.pdf);;SVG files (*.svg)"
        )
        if file_path:
            try:
                self.results_fig.savefig(file_path, dpi=300, bbox_inches='tight')
                QMessageBox.information(self, "Success", f"Plots saved to {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error saving plots:\n{str(e)}")

    def export_permittivity(self):
        """
        Export optimized permittivity values to a CSV file.

        Creates a CSV file containing three columns:
        - Frequency_GHz: Frequency values in GHz
        - Epsilon_Real: Real part of complex permittivity (ε')
        - Epsilon_Imag: Imaginary part of complex permittivity (ε'')

        Checks if optimized permittivity data exists before exporting.
        Opens a file save dialog for the user to specify the output path.

        Displays success or error messages via dialog boxes.

        CSV Format Example:
            Frequency_GHz,Epsilon_Real,Epsilon_Imag
            1.5,3.2,0.05
            1.6,3.25,0.06
            ...
        """
        if not hasattr(self, 'eps_opt') or self.eps_opt is None:
            QMessageBox.warning(self, "Warning", "No optimized permittivity to export")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Permittivity", "", "CSV files (*.csv)"
        )
        if file_path:
            try:
                import csv
                with open(file_path, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Frequency_GHz', 'Epsilon_Real', 'Epsilon_Imag'])
                    for i, freq in enumerate(self.freq_est_opt):
                        writer.writerow([freq, real(self.eps_opt[i]), imag(self.eps_opt[i])])
                QMessageBox.information(self, "Success", f"Permittivity exported to {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error exporting permittivity:\n{str(e)}")


def create_arrow_icons():
    """
    Create SVG arrow icons for UI spin boxes and combo boxes.

    Generates four SVG files in a temporary directory:
    - arrow_up_dark.svg: Upward arrow for dark mode (light colored)
    - arrow_down_dark.svg: Downward arrow for dark mode (light colored)
    - arrow_up_light.svg: Upward arrow for light mode (dark colored)
    - arrow_down_light.svg: Downward arrow for light mode (dark colored)

    The icons are used in QSpinBox, QDoubleSpinBox, and QComboBox widgets
    to provide theme-appropriate arrow indicators.

    Returns:
        Path: Directory path containing the created icon files

    Directory:
        ~/.temp_icons/ in the user's home directory
    """
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
    """
    Configure Matplotlib global settings for dark mode.

    Sets matplotlib rcParams to create plots with dark backgrounds suitable
    for dark mode interfaces. Configures:
    - Figure and axes background colors (dark grays)
    - Text, tick, and label colors (light grays)
    - Grid and legend colors
    - Line color cycle (bright colors that contrast well with dark backgrounds)

    Color Palette:
        - Background: #2b2b2b (dark gray)
        - Axes background: #1e1e1e (darker gray)
        - Text/labels: #e0e0e0 (light gray)
        - Grid: #3d3d3d (medium gray)
        - Line colors: Bright blues, reds, greens, yellows, purples

    Called automatically when dark mode is detected.
    """
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
    """
    Configure Matplotlib global settings for light mode.

    Sets matplotlib rcParams to create plots with light backgrounds suitable
    for light mode interfaces. Configures:
    - Figure and axes background colors (white)
    - Text, tick, and label colors (dark grays)
    - Grid and legend colors
    - Line color cycle (saturated colors that contrast well with light backgrounds)

    Color Palette:
        - Background: #ffffff (white)
        - Axes background: #ffffff (white)
        - Text/labels: #2b2b2b (dark gray)
        - Grid: #d0d0d0 (light gray)
        - Line colors: Saturated blues, reds, greens, oranges, purples

    Called automatically when light mode is detected.
    """
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
    """
    Apply comprehensive Qt stylesheet to the entire application.

    Detects system theme (dark/light mode) and applies appropriate styling to
    all Qt widgets. Creates a consistent, modern look across the application.

    Process:
    1. Creates arrow icons for spin boxes and combo boxes
    2. Retrieves system accent color
    3. Detects dark/light mode based on window background lightness
    4. Configures matplotlib plot styling
    5. Applies extensive Qt stylesheet with:
       - Color schemes for dark/light mode
       - Widget-specific styling (buttons, inputs, tabs, scrollbars)
       - Hover and focus states
       - Custom button colors for specific actions

    Styled Widgets:
        - QMainWindow, QWidget: Base colors and fonts
        - QGroupBox: Borders, titles, accent colors
        - QLineEdit: Input fields with focus indicators
        - QSpinBox, QDoubleSpinBox: Number inputs with custom arrows
        - QComboBox: Dropdowns with custom styling
        - QPushButton: Buttons with hover/pressed states and role-specific colors
        - QTextEdit: Text areas with monospace font
        - QProgressBar: Progress indicators with accent color
        - QTabWidget, QTabBar: Tab navigation
        - QScrollBar: Custom scrollbars (vertical and horizontal)

    Button Roles:
        - load_files_btn: Gray for file loading
        - optimize_btn: Green for starting optimization
        - apply_btn: Blue for applying changes

    Args:
        self: QApplication instance to apply styling to
    """

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
            QPushButton#stop_btn {{ background-color: #b30904; padding: 8px; }}
            QPushButton#stop_btn:hover {{ background-color: #db3e39; }}
            QPushButton#stop_btn:pressed {{ background-color: #780805; }}
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
            QPushButton#stop_btn {{ background-color: #b30904; padding: 8px; }}
            QPushButton#stop_btn:hover {{ background-color: #db3e39; }}
            QPushButton#stop_btn:pressed {{ background-color: #780805; }}
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


def main():
    """
    Application entry point - initializes and runs the GUI.

    Process:
    1. Creates QApplication instance
    2. Sets Fusion style for consistent cross-platform appearance
    3. Applies global styling via setup_style()
    4. Creates OptimizationGUI main window
    5. Shows window in maximized state
    6. Starts Qt event loop

    The application will run until the user closes the window or
    the event loop is terminated. Exit code is returned to the system.

    Usage:
        python script_name.py

    Returns:
        int: System exit code (0 for normal termination)
    """
    app = QApplication(sys.argv)
    app.setApplicationName("PyCarMat Epsilon")
    app.setOrganizationName("IMT Atlantique")

    # Set application style
    app.setStyle('Fusion')
    setup_style(app)

    # Create and show the main window
    window = OptimizationGUI()
    window.show()
    sleep(.1)
    window.showMaximized()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()