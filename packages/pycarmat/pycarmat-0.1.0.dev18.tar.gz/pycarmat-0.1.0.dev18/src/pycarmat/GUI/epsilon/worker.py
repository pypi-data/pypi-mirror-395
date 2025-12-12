import traceback
import warnings
from copy import deepcopy
from pathlib import Path

from numpy import genfromtxt, asarray
from qosm.propagation import PW

from scipy.interpolate import interp1d

from pycarmat.inverse_model.score_functions.metrics import tanh_score_1d, lsq_score, l2_score, tanh_score_nd, r2_score
from pycarmat.inverse_model.model import InverseProblem
from pycarmat.inverse_model.tools import compute_s11_with_phase_correction
from pycarmat.inverse_model.objective_functions.epsilon import cost_function

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)

from numpy import full_like, nan, abs, zeros, linspace, array, sqrt, mean, corrcoef, isnan, real, imag, \
    angle, exp, pi
from PySide6.QtCore import QThread, Signal


def compute_complex_correlation(measured_complex, simulated_complex, is_complex=True):
    """
    Calculate correlation coefficient for complex-valued S-parameters.

    Computes the average correlation between real and imaginary parts separately,
    then returns their mean. NaN values are replaced with 0.

    Args:
        measured_complex (ndarray): Measured complex S-parameter values
        simulated_complex (ndarray): Simulated complex S-parameter values

    Returns:
        float: Average correlation coefficient between 0 (no correlation) and 1 (perfect correlation)
    """
    real_measured = real(measured_complex)
    real_simulated = real(simulated_complex)
    real_corr = corrcoef(real_measured, real_simulated)[0, 1]
    if isnan(real_corr):
        real_corr = 0.0

    if is_complex:
        imag_measured = imag(measured_complex)
        imag_simulated = imag(simulated_complex)
        imag_corr = corrcoef(imag_measured, imag_simulated)[0, 1]
        if isnan(imag_corr):
            imag_corr = 0.0

        return (real_corr + imag_corr) / 2.0
    else:

        return real_corr


class OptimizationWorker(QThread):
    """Worker thread for optimization calculations"""
    progress_update = Signal(str)  # For log messages
    progress_value = Signal(int)  # For progress bar value (0-100) - ADDED
    plot_update = Signal(float, float)  # thickness_mm, total_error
    finished = Signal(dict)  # optimization results
    error_occurred = Signal(str)  # error message

    def __init__(self, parent, config, frequencies, s21_s12_measured, s11_measured, s22_measured, s2p_file_path,
                 initial_epsilon_range, initial_im_espilon, thickness_range, fws, fpo, num_points,
                 num_epsilon_starts, freq_range, metric, model, thickness_layer_index, epsilon_layer_index,
                 error_mode=0, config_file_path=None):
        super().__init__()
        self.parent = parent
        self.config = config
        self.frequencies = frequencies
        self.s21_s12_measured = s21_s12_measured
        self.s11_measured = s11_measured
        self.s22_measured = s22_measured
        self.s2p_file_path = s2p_file_path
        self.initial_epsilon_range = initial_epsilon_range
        self.initial_im_espilon = initial_im_espilon
        self.thickness_range = thickness_range
        self.fws = fws
        self.fpo = fpo
        self.num_points = num_points
        self.num_epsilon_starts = num_epsilon_starts
        self.freq_range = freq_range
        self.metric = metric
        self.model = model
        self.thickness_layer_index = thickness_layer_index
        self.epsilon_layer_index = epsilon_layer_index
        self.error_mode = error_mode
        self.config_file_path = config_file_path
        self.thickness_results = {}
        self.keep_working = False

    def run(self):
        try:
            if self.epsilon_layer_index > -1:
                self.progress_update.emit(f"Starting mono-layer optimization with multi-start estimation")
            else:
                self.progress_update.emit(f"Starting mono-layer optimization")
            self.progress_update.emit(f"Model: {self.model.__name__}")
            self.progress_update.emit(f"Layer index to optimize thickness: {self.thickness_layer_index}")
            if self.epsilon_layer_index > -1:
                self.progress_update.emit(f"Layer index to optimize permittivity: {self.epsilon_layer_index}")
            self.progress_update.emit(f"Optimization metric: {self.metric}")
            self.progress_update.emit(f"Frequency range: {self.freq_range[0]}-{self.freq_range[1]} GHz")
            if self.epsilon_layer_index > -1:
                self.progress_update.emit(
                    f"Epsilon range: {self.initial_epsilon_range[0]:.2f}-{self.initial_epsilon_range[1]:.2f}")
                self.progress_update.emit(f"Number of epsilon starts: {self.num_epsilon_starts}")
            self.keep_working = True
            result = self.optimize_layer_parameters()
            self.progress_update.emit(f"\nOptimization completed!")
            self.progress_update.emit(f"Optimized thickness [mm]: {result['optimized_thickness'] * 1000:.6f}")

            # Set progress to 100% when finished - ADDED
            self.progress_value.emit(100)

            self.finished.emit(result)

        except Exception as e:
            traceback.print_exc()
            self.error_occurred.emit(f"Error during optimization: {str(e)}")

    def optimize_layer_parameters(self):
        """
        Optimize layer parameters (thickness and/or permittivity) using multi-start estimation.

        This method performs a grid search over thickness values, optionally estimating
        permittivity at each point using multiple initial guesses (multi-start approach).
        For each thickness value, it evaluates the objective function and stores results.
        Can optimize:
        - Thickness only (when epsilon_layer_index = -1)
        - Thickness and permittivity simultaneously (when epsilon_layer_index >= 0)

        Returns:
            dict: Optimization results containing:
                - optimized_thickness (float): Best thickness value in meters
                - final_metric (tuple): Error metrics (S21_error, S11_error) at optimal point
                - initial_metric (tuple): Error metrics at initial thickness
                - freq_range (tuple): Frequency range used (min_GHz, max_GHz)
                - metric (str): Metric used ('r2' or 'correlation')
                - epsilon_range (tuple): Permittivity range for multi-start
                - num_epsilon_starts (int): Number of initial epsilon values tested
                - best_epsilon_result (dict): Best permittivity estimation result
                - model: Electromagnetic model used (PW or GBTC)
                - epsilon_layer_index (int): Index of layer for permittivity optimization
                - thickness_layer_index (int): Index of layer for thickness optimization
        """
        self.progress_update.emit(
            f"Optimization bounds: [{self.thickness_range[0] * 1000:.3f}, {self.thickness_range[1] * 1000:.6f}] mm")

        # Initialize results storage
        self.thickness_results = {}

        # Create list of initial epsilon values for multi-start
        if self.epsilon_layer_index > -1:
            initial_epsilon_list = linspace(self.initial_epsilon_range[0], self.initial_epsilon_range[1],
                                            self.num_epsilon_starts)
        else:
            initial_epsilon_list = (-1,)

        thickness_array = linspace(self.thickness_range[0], self.thickness_range[1], self.num_points, endpoint=True)
        error_array = zeros((self.num_points, 2))

        # Initial error calculation

        for i, thickness in enumerate(thickness_array):
            if not self.keep_working:
                return {
                'optimized_thickness': nan,
                'final_metric': (nan, nan),
                'freq_range': self.freq_range,
                'metric': self.metric,
                'epsilon_range': self.initial_epsilon_range,
                'num_epsilon_starts': self.num_epsilon_starts,
                'best_epsilon_result': None,
                'model': self.model,
                'epsilon_layer_index': self.epsilon_layer_index,
                'thickness_layer_index': self.thickness_layer_index
            }
            # Update progress bar (0-100%) - ADDED
            progress_percent = int((i / len(thickness_array)) * 100)
            self.progress_value.emit(progress_percent)

            res = self.compute_objective_function(initial_epsilon_list, thickness)
            error_array[i, :] = res
            if self.error_mode == 0:
                total_error = res[1]  # only S11
            elif self.error_mode == 1:
                total_error = res[0]  # only S21
            else:
                total_error = sqrt((res[0] ** 2 + res[1] ** 2) / 2.0)
            thickness_mm = thickness * 1e3

            # Emit plot update signal
            self.plot_update.emit(thickness_mm, total_error)

            # IMPROVED progress message - ADDED
            progress_msg = f'Point {i + 1}/{len(thickness_array)}: thickness={thickness_mm:.6f} mm -> error={total_error:.5f}'
            self.progress_update.emit(progress_msg)

        min_index = array(error_array[:, 0] + error_array[:, 1]).argmin()
        optimized_thickness = thickness_array[min_index]

        if optimized_thickness not in self.thickness_results:
            best_epsilon_result = None
            self.error_occurred.emit(f"Error during optimization: No solution found")
        else:
            best_epsilon_result = self.thickness_results[optimized_thickness]

        return {
            'optimized_thickness': optimized_thickness,
            'final_metric': error_array[min_index],
            'freq_range': self.freq_range,
            'metric': self.metric,
            'epsilon_range': self.initial_epsilon_range,
            'num_epsilon_starts': self.num_epsilon_starts,
            'best_epsilon_result': best_epsilon_result,
            'model': self.model,
            'epsilon_layer_index': self.epsilon_layer_index,
            'thickness_layer_index': self.thickness_layer_index
        }

    def resolve_csv_file_path(self, filepath):
        """
        Resolve CSV file path, handling relative paths starting with ./

        If the path starts with './' and a config file path is available, the path
        is resolved relative to the directory containing the TOML config file.
        Otherwise, the path is returned as-is.

        Args:
            filepath (str): CSV file path, potentially with 'CSV:' prefix or relative path

        Returns:
            str: Resolved absolute or relative file path

        Examples:
            With config at /home/user/configs/setup.toml:
            - './data.csv' -> '/home/user/configs/data.csv'
            - '/abs/path/data.csv' -> '/abs/path/data.csv'
            - 'data.csv' -> 'data.csv'
        """
        # Clean the filepath
        filepath = filepath.replace('CSV:', '').replace(' ', '').strip()

        # If path starts with ./ and we have a config file path, make it relative to config directory
        if filepath.startswith('./') and self.config_file_path:
            config_dir = Path(self.config_file_path).parent
            resolved_path = config_dir / filepath[2:]  # Remove the './' prefix
            return str(resolved_path)

        return filepath

    def compute_objective_function(self, initial_epsilon_list, thickness):
        """
        Compute the objective function for layer optimization with multi-start permittivity estimation.

        This method evaluates the error between measured and simulated S-parameters for a given
        thickness value. If permittivity estimation is enabled, it tries multiple initial epsilon
        values and selects the one giving the best results (multi-start approach).

        The process:
        1. Apply frequency range filtering
        2. Update layer thickness in configuration
        3. Load CSV permittivity files if specified (with relative path support)
        4. For each initial epsilon value:
           - Estimate permittivity using InverseProblem model
           - Simulate S-parameters using the electromagnetic model
           - Calculate error metrics (R² or correlation)
        5. Return the best error found

        Args:
            initial_epsilon_list (array-like): List of initial permittivity values for multi-start.
                                               Use (-1,) to skip permittivity estimation.
            thickness (float): Layer thickness to evaluate in meters

        Returns:
            tuple: Error metrics (S21_error, S11_error) where lower values indicate better fit
        """

        # Select frequency range if specified
        if self.freq_range is not None:
            freq_mask = (self.frequencies >= self.freq_range[0]) & (self.frequencies <= self.freq_range[1])
            freq_subset = self.frequencies[freq_mask]
            s21_s12_meas_subset = self.s21_s12_measured[freq_mask]
            s11_meas_subset = self.s11_measured[freq_mask]
            s22_meas_subset = self.s22_measured[freq_mask]
        else:
            freq_subset = self.frequencies
            s21_s12_meas_subset = self.s21_s12_measured
            s11_meas_subset = self.s11_measured
            s22_meas_subset = self.s22_measured

        # Update configuration with new thickness
        config = deepcopy(self.config)
        config['mut'][self.thickness_layer_index]['thickness'] = thickness

        total_thickness = 0
        for mut in config['mut']:
            total_thickness += mut['thickness']

        # load csv file for each permittivity if needed
        for i, mut in enumerate(config['mut']):
            if isinstance(mut['epsilon_r'], str):
                filepath = self.resolve_csv_file_path(mut['epsilon_r'])
                _data = genfromtxt(filepath, delimiter=',', skip_header=1)
                # Interpolate CSV data to match frequency points
                freq_csv = _data[:, 0]  # First column: frequency
                eps_real_csv = _data[:, 1]  # Second column: real part
                eps_imag_csv = _data[:, 2]  # Third column: imaginary part

                # Interpolate to self.frequencies
                eps_interp = interp1d(freq_csv, eps_real_csv + 1j * eps_imag_csv,
                                      kind='cubic', fill_value="extrapolate")

                # Replace string path with interpolation function
                config['mut'][i]['epsilon_r'] = eps_interp

        best_error = (1.0, 1.0)
        best_result = None
        eps_complex = 0j
        estimator = InverseProblem(config_file=config, unknown_layer=self.epsilon_layer_index,
                                   cost_fn=cost_function, score_fn=tanh_score_1d)
        estimator.load_experimental_data(self.s2p_file_path, filter_window_length=self.fws,
                                         filter_poly_order=self.fpo)

        # Multi-start: try different initial epsilon values
        for initial_epsilon in initial_epsilon_list:
            if not self.keep_working:
                return 1
            if initial_epsilon > -1:
                try:
                    # Permittivity estimation
                    res = estimator.sweep_fit(PW, (initial_epsilon, self.initial_im_espilon))

                    eps_interp = res[1]

                    # Interpolation for frequencies of interest (in case of freq_est != self.frequencies)
                    config['mut'][self.epsilon_layer_index]['epsilon_r'] = eps_interp
                    eps_complex = eps_interp(self.frequencies)
                except RuntimeError:
                    continue

            elif hasattr(config['mut'][self.epsilon_layer_index]['epsilon_r'], '__call__'):
                eps_complex = config['mut'][self.epsilon_layer_index]['epsilon_r'](self.frequencies)

            # Simulate S21 and S11
            s21_simulated = full_like(freq_subset, nan, dtype=complex)
            s12_simulated = full_like(freq_subset, nan, dtype=complex)
            s11_simulated = full_like(freq_subset, nan, dtype=complex)

            for k, freq_GHz in enumerate(freq_subset):
                s11_sim, s12_sim, s21_sim, s22_sim = self.model.simulate(config, freq_GHz)
                s21_simulated[k] = s21_sim
                s12_simulated[k] = s12_sim
                s11_simulated[k] = compute_s11_with_phase_correction(s11_sim, s22_sim, total_thickness, freq_GHz)
                s11_meas_subset[k] = compute_s11_with_phase_correction(s11_meas_subset[k], s22_meas_subset[k],
                                                                       total_thickness, freq_GHz)

            # Calculate average and metrics
            s21_s12_simulated = (s21_simulated + s12_simulated) / 2.0
            use_only_abs_s11 = False
            if self.metric == 'r2':
                r2_s21 = r2_score(s21_s12_meas_subset, s21_s12_simulated)
                if use_only_abs_s11:
                    r2_s11 = r2_score(abs(s11_meas_subset), abs(s11_simulated), is_complex=False)
                else:
                    r2_s11 = r2_score(s11_meas_subset, s11_simulated, is_complex=True)
                r2_s21 = max(r2_s21, -1.0)
                r2_s11 = max(r2_s11, -1.0)
                error = (1.0 - (r2_s21 + 1.0) / 2.0, 1.0 - (r2_s11 + 1.0) / 2.0)
            elif self.metric == 'L2':
                if use_only_abs_s11:
                    error = (l2_score(s21_s12_meas_subset, s21_s12_simulated),
                             l2_score(s11_meas_subset, s11_simulated))
                else:
                    error = (l2_score(s21_s12_meas_subset, s21_s12_simulated),
                             l2_score(abs(s11_meas_subset), abs(s11_simulated)))
            elif self.metric == 'tanh':
                if use_only_abs_s11:
                    error = (tanh_score_nd(s21_s12_meas_subset, s21_s12_simulated, alpha=1.),
                             tanh_score_nd(s11_meas_subset, s11_simulated, alpha=1.))
                else:
                    error = (tanh_score_nd(s21_s12_meas_subset, s21_s12_simulated, alpha=1.),
                             tanh_score_nd(abs(s11_meas_subset), abs(s11_simulated), alpha=1.))
            elif self.metric == 'lsq':
                if use_only_abs_s11:
                    error = (lsq_score(s21_s12_meas_subset, s21_s12_simulated),
                             lsq_score(s11_meas_subset, s11_simulated))
                else:
                    error = (lsq_score(s21_s12_meas_subset, s21_s12_simulated),
                             lsq_score(abs(s11_meas_subset), abs(s11_simulated)))
            else:  # correlation
                corr_s21 = compute_complex_correlation(s21_s12_meas_subset, s21_s12_simulated)
                if use_only_abs_s11:
                    corr_s11 = compute_complex_correlation(abs(s11_meas_subset), abs(s11_simulated), is_complex=False)
                else:
                    corr_s11 = compute_complex_correlation(s11_meas_subset, s11_simulated)
                error = (1.0 - corr_s21, 1 - corr_s11)

            # Keep best result
            if self.error_mode == 0:
                total_error = error[1]  # only S11
                best_total_error = best_error[1]
            elif self.error_mode == 1:
                total_error = error[0]  # onlyS 21
                best_total_error = best_error[0]
            else:
                total_error = .5 * (error[0] + error[1])
                best_total_error = .5 * (best_error[0] + best_error[1])

            if total_error < best_total_error:
                best_error = error
                best_result = {
                    'initial_epsilon': initial_epsilon,
                    'frequencies_subset': freq_subset,
                    'frequencies': self.frequencies,
                    'eps_complex': eps_complex,
                }

        # Store best result
        if best_result is not None:
            self.thickness_results[thickness] = best_result

        return best_error

