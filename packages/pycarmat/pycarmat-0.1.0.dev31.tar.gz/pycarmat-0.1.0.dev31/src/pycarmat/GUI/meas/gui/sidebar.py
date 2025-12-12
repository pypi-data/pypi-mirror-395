import os
from datetime import datetime
from time import sleep

from PySide6.QtWidgets import QVBoxLayout, QPushButton, QLineEdit, \
    QLabel, QComboBox, QFileDialog, QCheckBox, QProgressBar, QGroupBox, QGridLayout, QDoubleSpinBox, \
    QAbstractSpinBox
from numpy import arange

from skrf import Network
from pycarmat.ressources.ESP import ESP30xController, UNIT
from pycarmat.ressources.VNA import RohdeSchwarzVNA, KeysightVNA
from .axes_settings_gui import AxesSettingsWindow
from .core import Worker, Tab
from .trl_gui import TRLWindow


class QInt(QDoubleSpinBox):
    def __init__(self, default: int = 0., arrows: bool = True):
        super().__init__()
        self.setMaximum(90000)
        self.setDecimals(0)
        if not arrows:
            self.setButtonSymbols(QDoubleSpinBox.NoButtons)
        self.setValue(default)


class QDouble(QDoubleSpinBox):
    def __init__(self, default: float = 0., arrows: bool = False):
        super().__init__()
        self.setDecimals(3)
        self.setRange(-2000., 2000.)
        self.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)
        if not arrows:
            self.setButtonSymbols(QDoubleSpinBox.NoButtons)
        self.setValue(default)


class ResetWorker(Worker):
    def _run(self):
        ip_address = self.params['ip_address']
        simulate = self.params['simulate']
        __vna__ = RohdeSchwarzVNA if self.params['is_rs'] else KeysightVNA
        with __vna__(ip_address=ip_address, simulate=simulate) as vna:
            vna.reset()


class MeasureWorker(Worker):
    def _run(self):
        self._running = True

        ip_address = self.params['ip_address']
        simulate = self.params['simulate']
        range_freq_GHz = self.params['range_freq_GHz']
        num_freq_points = self.params['num_freq_points']
        meas_bandwidth = self.params['meas_bandwidth']
        num_meas = self.params['num_meas']
        trl_id = self.params['trl_id']
        band = self.params['band']
        angles_deg = self.params['angles']

        sub_folder = self.params['sub_folder']

        mat_name = self.params['mat_name']
        mat_thickness = self.params['mat_thickness']
        mat_thickness = f"_{mat_thickness}".replace(".", "-") if mat_thickness else ''

        if mat_name == '':
            self.error_signal.emit(str('Material name cannot be empty'))
            self.progress_signal.emit(0)
            self.finished.emit()
            return

        axis_rot = 2

        __vna__ = RohdeSchwarzVNA if self.params['is_rs'] else KeysightVNA

        today = datetime.today().strftime("%Y%m%d")  # Format YYYYMMDD
        with __vna__(ip_address=ip_address, simulate=simulate) as vna, \
              ESP30xController(serial_port='ASRL/dev/ttyUSB0', raise_error=False) as esp:

            results_dirpath = f'{sub_folder}/{band}/{today}/{mat_name}{mat_thickness}/trl{trl_id:02d}'
            os.makedirs(results_dirpath, exist_ok=self.params['overwrite'])

            for angle_deg in angles_deg:
                if esp.connected():
                    esp.clear_errors()
                    esp.move_absolute(axis=axis_rot, value=angle_deg, motion_unit=UNIT.ROTATION_DEG)
                    sleep(.5)
                    # ensure movement is done
                    esp.move_absolute(axis=axis_rot, value=angle_deg, motion_unit=UNIT.ROTATION_DEG)


                vna.set_sweep(freq_start_GHz=range_freq_GHz[0], freq_end_GHz=range_freq_GHz[1],
                              num_pts=num_freq_points,
                              bandwidth=meas_bandwidth)

                for i in range(num_meas):
                    if not self._running:
                        return

                    angle_str = f'{angle_deg:05.2f}'.replace('.', '-')
                    filename = f"{mat_name}_ang{angle_str}_{i:03d}.s2p"
                    if simulate:
                        sleep(1)
                    s2p = vna.measure(num_iterations=1, return_format='s2p',
                                      file_path=f'{results_dirpath}/{filename}')
                    self.result_signal.emit(s2p)
                    self.progress_signal.emit(i+1)

    def stop(self):
        self._running = False

class Sidebar(Tab):

    def __init__(self, gui_elements: tuple, **kargs):
        super().__init__(gui_elements, **kargs)

        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        self._previous_dir_path = 'none'
        self._vna_locked = False

        self.group_box = QGroupBox("Enable VNA sweep")
        self.group_box.setCheckable(True)  # Allows toggling
        self.group_box.setChecked(True)  # Initially expanded
        self.group_box.toggled.connect(self.set_status)

        group_layout = QGridLayout(self.group_box)

        self.group_box_con = QGroupBox("Connection")
        self.group_box_con.setCheckable(False)
        self.group_box_con.setChecked(True)
        group_layout_con = QGridLayout(self.group_box_con)
        group_layout_con.addWidget(QLabel("IP Address"), 0, 0)
        self.ip_address = QLineEdit("192.168.0.4")
        group_layout_con.addWidget(self.ip_address, 0, 1)

        self.simulate_switch = QCheckBox("Simulate")
        self.simulate_switch.stateChanged.connect(self.set_default_root_dir)
        group_layout_con.addWidget(self.simulate_switch, 1, 1)
        group_layout.addWidget(self.group_box_con, 0, 0)

        def brand_combo_changed(index: int):
            self.ip_address.setText("192.168.0.4" if index == 0 else "192.168.0.5")

        self.brand_combo = QComboBox()
        self.brand_combo.addItems(["R&S", "Keysight"])
        group_layout_con.addWidget(self.brand_combo, 1, 0)
        self.brand_combo.currentIndexChanged.connect(brand_combo_changed)
        self.brand_combo.setCurrentIndex(1)

        self.group_box_sweep = QGroupBox("Sweep settings")
        self.group_box_sweep.setCheckable(False)
        self.group_box_sweep.setChecked(True)
        group_layout_sweep = QGridLayout(self.group_box_sweep)
        group_layout_sweep.addWidget(QLabel("Band"), 3, 0)
        self.band_combo = QComboBox()
        self.band_combo.addItems(["J-Band", "W-Band", "D-Band", "sTHz-Band"])
        group_layout_sweep.addWidget(self.band_combo, 3, 1)

        group_layout_sweep.addWidget(QLabel("Num. Points"), 4, 0)
        self.num_points = QInt(1001)
        group_layout_sweep.addWidget(self.num_points, 4, 1)

        group_layout_sweep.addWidget(QLabel("Meas. Bandwidth"), 5, 0)
        self.meas_bandwidth = QComboBox()
        self.meas_bandwidth.addItems(["1 kHz", "10 kHz", "100 kHz"])
        group_layout_sweep.addWidget(self.meas_bandwidth, 5, 1)

        group_layout.addWidget(QLabel(''), 1, 0)
        group_layout.addWidget(self.group_box_sweep, 2, 0)

        self.group_box_meas = QGroupBox("Meas. settings")
        self.group_box_meas.setCheckable(False)
        self.group_box_meas.setChecked(True)
        group_layout_meas = QGridLayout(self.group_box_meas)
        group_layout_meas.addWidget(QLabel("TRL index"), 6, 0)
        self.trl_index = QInt(1)
        group_layout_meas.addWidget(self.trl_index, 6, 1)
        self.trl_button = QPushButton("TRL")
        self.trl_button.clicked.connect(lambda: TRLWindow(band_settings={
            'num_points': int(self.num_points.text()),
            'meas_bandwidth': self.meas_bandwidth.currentText(),
            'band_id': self.band_combo.currentIndex()
        }, ip_address=self.ip_address.text(), is_rs=self.brand_combo.currentIndex() == 0).exec())
        group_layout_meas.addWidget(self.trl_button, 6, 2)

        group_layout_meas.addWidget(QLabel("Number of sweep(s)"), 7, 0)
        self.num_meas = QInt(1)
        group_layout_meas.addWidget(self.num_meas, 7, 1, 1, 2)

        group_layout_meas.addWidget(QLabel("Material name"), 8, 0)
        self.material_name = QLineEdit("")
        group_layout_meas.addWidget(self.material_name, 8, 1, 1, 2)

        group_layout_meas.addWidget(QLabel("Material thickness [mm]"), 9, 0)
        self.material_thickness = QLineEdit("0")
        group_layout_meas.addWidget(self.material_thickness, 9, 1, 1, 2)

        group_layout_meas.addWidget(QLabel("Angle(s) [°]"), 10, 0)
        self.material_angle_start = QDoubleSpinBox(suffix='°', prefix='From: ', decimals=1, minimum=-45, maximum=45)
        self.material_angle_end = QDoubleSpinBox(suffix='°', prefix='to: ', decimals=1, minimum=-45, maximum=45)
        self.material_angle_step = QDoubleSpinBox(suffix='°', prefix='step: ', decimals=1, value=1, minimum=0)
        group_layout_meas.addWidget(self.material_angle_start, 10, 1)
        group_layout_meas.addWidget(self.material_angle_end, 11, 1)
        group_layout_meas.addWidget(self.material_angle_step, 12, 1)

        self.angle_reset_button = QPushButton("Reset")
        self.angle_homing_button = QPushButton("Homing")
        self.angle_reset_button.clicked.connect(self.reset_angle)
        self.angle_homing_button.clicked.connect(self.homing_angle)
        group_layout_meas.addWidget(self.angle_reset_button, 10, 0)
        group_layout_meas.addWidget(self.angle_homing_button, 11, 0)


        group_layout.addWidget(QLabel(''), 3, 0)
        group_layout.addWidget(self.group_box_meas, 4, 0)

        self.group_box_output = QGroupBox("Output")
        self.group_box_output.setCheckable(False)
        self.group_box_output.setChecked(True)
        group_layout_output = QGridLayout(self.group_box_output)
        self.choose_dir_button = QPushButton("Project data dir.")
        self.choose_dir_button.clicked.connect(self.choose_root_dir)
        self.sub_folder = QLineEdit('')
        self.sub_folder.setReadOnly(True)
        self.set_default_root_dir()
        self.overwrite_switch = QCheckBox("Replace files if exists")
        group_layout_output.addWidget(self.choose_dir_button, 11, 0)
        group_layout_output.addWidget(self.sub_folder, 11, 1)
        group_layout_output.addWidget(self.overwrite_switch, 12, 1)

        group_layout.addWidget(QLabel(''), 5, 0)
        group_layout.addWidget(self.group_box_output, 6, 0)

        group_layout.addWidget(QLabel(''), 7, 0)
        self.start_button = QPushButton("Start")
        self.start_button.setStyleSheet("background-color: #339955; color: #fff; padding:10px")
        self.start_button.clicked.connect(self.measure_s2p)
        group_layout.addWidget(self.start_button, 8, 0)

        self.stop_button = QPushButton("Stop")
        self.stop_button.setStyleSheet("background-color: #993355; color: #fff; padding:10px")
        self.stop_button.clicked.connect(self.stop_measure)
        self.stop_button.setVisible(False)
        group_layout.addWidget(self.stop_button, 9, 0)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        group_layout.addWidget(self.progress_bar, 10, 0)

        group_layout.addWidget(QLabel(''), 11, 0)
        self.reset_button = QPushButton("Reset VNA Display")
        self.reset_button.setStyleSheet("background-color: #36185c; color: #fff; padding:10px")
        self.reset_button.clicked.connect(self.reset_vna)
        group_layout.addWidget(self.reset_button, 12, 0)

        layout.addWidget(self.group_box)

        self.load_s2p_button = QPushButton("Load s2p")
        self.load_s2p_button.setStyleSheet("background-color: #2266aa; color: #fff;")
        self.load_s2p_button.clicked.connect(self.load_s2p_file)
        layout.addWidget(self.load_s2p_button)

        layout.addStretch()

        with ESP30xController(serial_port='ASRL/dev/ttyUSB0', raise_error=False) as esp:
            if esp.connected():
                stage1_model_name = esp.query('1ID?').split(',')[0]
                stage2_model_name = esp.query('1ID?').split(',')[0]
                if 'Unknown' in stage1_model_name:
                    stage1_model_name = None
                if 'Unknown' in stage2_model_name:
                    stage2_model_name = None
                detected_esp_stage_models = (stage1_model_name, stage2_model_name)
                print(detected_esp_stage_models)
                if stage1_model_name is None or stage2_model_name is None:
                    AxesSettingsWindow(self, detected_esp_stage_models).exec()
            else:
                self.deactivate_eps(axis1=True, axis2=True)

    def deactivate_eps(self, axis1=False, axis2=False):
        if axis1:
            self.trl_button.setVisible(True)
        if axis2:
            self.angle_reset_button.setVisible(False)
            self.angle_homing_button.setVisible(False)
            self.material_angle_start.setVisible(False)
            self.material_angle_end.setVisible(False)
            self.material_angle_step.setVisible(False)

    def set_default_root_dir(self):
        previous_chosen_dirpath = self._previous_dir_path if self._previous_dir_path != 'none' else './measures'
        default_dir = './simulate' if self.simulate_switch.isChecked() else previous_chosen_dirpath
        self.sub_folder.setText(default_dir)
        self.choose_dir_button.setEnabled(not self.simulate_switch.isChecked())

    def choose_root_dir(self):
        default_dir = 'simulate' if self.simulate_switch.isChecked() else 'measures'
        dir_path = QFileDialog.getExistingDirectory(self, "Select root dir", f"./{default_dir}")
        if dir_path:
            self._previous_dir_path = dir_path
            self.sub_folder.setText(dir_path)

    def load_s2p_file(self):
        self.progress_bar.setValue(0)
        file_path, _ = QFileDialog.getOpenFileName(self, "Select s2p File", "", "Touchstone Files (*.s2p)")
        if file_path:
            self.group_box.setChecked(False)
            ntw = Network(file_path)
            self.tabs[1].update_graph(ntw)
            self.tabs[0].setCurrentIndex(0)

    def reset_vna(self):
        params = {
            'ip_address': self.ip_address.text(),
            'simulate': self.simulate_switch.isChecked(),
            'is_rs': self.brand_combo.currentIndex() == 0
        }

        worker = ResetWorker(self, params)
        worker.finished.connect(self.release_vna)

        self.tabs[0].setCurrentIndex(0)
        self._start_worker(worker)
        self.lock_vna()

    @staticmethod
    def homing_angle():
        with ESP30xController(serial_port='ASRL/dev/ttyUSB0', raise_error=False) as esp:
            if esp.connected():
                esp.clear_errors()
                esp.homing(axis=2)

    @staticmethod
    def reset_angle():
        with ESP30xController(serial_port='ASRL/dev/ttyUSB0', raise_error=False) as esp:
            if esp.connected():
                esp.clear_errors()
                esp.move_absolute(axis=2, value=0, motion_unit=UNIT.ROTATION_DEG)

    def measure_s2p(self):
        if self._vna_locked:
            return

        range_freq_GHz = {
            'J-Band': (220., 330.),
            'W-Band': (75., 110.),
            'D-Band': (110., 170.),
            'sTHz-Band': (500., 750.)
        }

        band = self.band_combo.currentText()
        params = {
            'band': band,
            'ip_address': self.ip_address.text(),
            'simulate': self.simulate_switch.isChecked(),
            'range_freq_GHz': range_freq_GHz[band],
            'num_freq_points': int(self.num_points.value()),
            'meas_bandwidth': self.meas_bandwidth.currentText(),
            'num_meas': int(self.num_meas.value()),
            'mat_name': self.material_name.text(),
            'mat_thickness': self.material_thickness.text(),
            'trl_id': int(self.trl_index.value()),
            'overwrite': self.overwrite_switch.isChecked(),
            'angles': arange(self.material_angle_start.value(),
                             self.material_angle_end.value() + self.material_angle_step.value(),
                             self.material_angle_step.value()),
            'sub_folder': self.sub_folder.text(),
            'is_rs': self.brand_combo.currentIndex() == 0
        }

        self.progress_bar.setMaximum(int(self.num_meas.text()))

        worker = MeasureWorker(self, params)
        worker.result_signal.connect(lambda ntw: self.tabs[1].update_graph(ntw))
        worker.finished.connect(self.release_vna)

        self.tabs[0].setCurrentIndex(0)
        self._start_worker(worker)
        self.lock_vna()

    def stop_measure(self):
        if self.worker is not None:
            self.worker.stop()

    def lock_vna(self):
        self._vna_locked = True
        self.group_box_con.setEnabled(False)
        self.group_box_sweep.setEnabled(False)
        self.group_box_meas.setEnabled(False)
        self.group_box_output.setEnabled(False)
        self.start_button.setVisible(False)
        self.stop_button.setVisible(True)
        self.progress_bar.setValue(0)

    def release_vna(self):
        self._vna_locked = False
        self.group_box_con.setEnabled(True)
        self.group_box_sweep.setEnabled(True)
        self.group_box_meas.setEnabled(True)
        self.group_box_output.setEnabled(True)
        self.start_button.setVisible(True)
        self.stop_button.setVisible(False)

    def set_status(self):
        bg_color = '339955' if self.group_box.isChecked() else '444'
        txt_color = 'fff' if self.group_box.isChecked() else '111'
        self.start_button.setStyleSheet(f'background-color: #{bg_color}; color: #{txt_color}; padding:10px')
