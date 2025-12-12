from copy import deepcopy

from numpy import nan, zeros, zeros_like, nanmedian, sum, isnan, full_like, asarray
from scipy.interpolate import interp1d
from scipy.optimize import minimize
from skrf import Network

from qosm.propagation import PW
from qosm import load_config_from_toml, filter_s2p

from pycarmat.inverse_model.analyse.analyze_angle_independence import analyze_angle_independence
from pycarmat.inverse_model.model import InverseProblem
from pycarmat.inverse_model.objective_functions.multi_params import cost_function
from pycarmat.inverse_model.tools import linear_regression, load_s2p_file, poly_fit_cplx


class EnhancedInverseProblem(InverseProblem):
    def __init__(self, config_file, score_fn, unknown_layer: int, unknown_thicknesses: tuple = (1, ),
                 raise_error: bool = False):
        super().__init__(config_file, cost_function, score_fn, unknown_layer, raise_error)
        self.unknown_thicknesses = unknown_thicknesses
        self.unknown_layer = unknown_layer

    def compute_weights(self, frequency_step: int = 1):
        _frequencies_ghz = self.frequencies_ghz[::frequency_step]
        weights = zeros_like(_frequencies_ghz)

        for i, angle_deg in enumerate(self.theta_y_deg_array):
            raw_signal = self.raw_data[i].s[::frequency_step, 1, 0]
            noise_estimate = abs(raw_signal - self.data[i, ::frequency_step, 1, 0])
            _weights = 1 / (noise_estimate + 1e-8)
            _weights = _weights
            weights += _weights
        weights /= len(self.theta_y_deg_array)
        weights /= sum(weights)

        return weights

    def sweep(self, model, frequency_step: int = 1, pbar=None):
        _frequencies_ghz = self.frequencies_ghz[::frequency_step]
        _frequencies_hz = _frequencies_ghz * 1e9
        _config = deepcopy(self.config_est) if self.config_est is not None else deepcopy(self.model)

        if pbar is not None:
            pbar.reset(_frequencies_ghz.shape[0])

        netw_dict = {}
        if 0. not in self.theta_y_deg_array:
            _config['sample_attitude_deg'] = (0, 0, 0)
            _i = 0
            _s = zeros((_frequencies_ghz.shape[0], 2, 2), dtype=complex)
            for k in range(_frequencies_ghz.shape[0]):
                _s[k, 0, 0], _s[k, 0, 1], _s[k, 1, 0], _s[k, 1, 1] = model.simulate(_config, _frequencies_ghz[_i])
                _i += frequency_step
            netw_dict[f'{0:.2f}'] = Network(s=_s, f=_frequencies_hz, f_unit='Hz')

        for i in range(len(self.theta_y_deg_array)):
            theta_deg = self.theta_y_deg_array[i]
            _config['sample_attitude_deg'] = (0, theta_deg, 0)
            _i = 0
            _s = zeros((_frequencies_ghz.shape[0], 2, 2), dtype=complex)
            for k in range(_frequencies_ghz.shape[0]):
                _s[k, 0, 0], _s[k, 0, 1], _s[k, 1, 0], _s[k, 1, 1] = model.simulate(_config, _frequencies_ghz[_i])
                _i += frequency_step

            netw_dict[f'{theta_deg:.2f}'] = Network(s=_s, f=_frequencies_hz, f_unit='Hz')

        if pbar is not None:
            pbar.close()

        return netw_dict

    def sweep_fit(self, model, initial_guess_values, frequency_step: int = 1, pbar=None, args=None,
                  use_linear_regression: bool = False, unknown_thicknesses = None):
        if args is None:
            args = {}
        self.model = model
        _frequencies_ghz = self.frequencies_ghz[::frequency_step]
        _e = zeros((_frequencies_ghz.shape[0], 2))
        if len(initial_guess_values) >= 3:
            _h = zeros((_frequencies_ghz.shape[0], 2 if len(initial_guess_values) == 4 else 1))
        else:
            _h = None

        if len(self.unknown_thicknesses) != len(initial_guess_values) - 2:
            raise AttributeError('Error')

        if pbar is not None:
            pbar.reset(_frequencies_ghz.shape[0])

        _i = 0
        self.fit_error = full_like(_frequencies_ghz, nan)
        for k in range(len(_frequencies_ghz)):
            res = self.fit(x=initial_guess_values, freq_idx=_i, model=model, args=args)
            guess = res['guess']
            if not res['success']:
                if self.raise_error:
                    raise RuntimeError("Unable to fit model")
                else:
                    _h[k, :] = (nan, nan) if len(initial_guess_values) >= 3 else (nan,)
                    _e[k, :] = (nan, nan)
            else:
                self.fit_error[k] = res['fun']
                _e[k, :] = (guess[0], guess[1])
                if len(guess) >= 3:
                    _h[k, :] = (guess[2], guess[3]) if len(guess) > 3 else (guess[2],)
                initial_guess_values = guess
            if pbar is not None:
                pbar.update(1)
            _i += frequency_step
        if pbar is not None:
            pbar.close()

        epsr_est_raw = interp1d(_frequencies_ghz, _e[:, 0] + 1j * _e[:, 1], kind='linear')
        wh = self.compute_weights(frequency_step=frequency_step)
        epsr_est = linear_regression(_frequencies_ghz, _e[:, 0], _e[:, 1], slope_mode='less', weights=wh)
        if len(initial_guess_values) >= 3:
            # h_est_mm = .5 * (nanmedian(_h, axis=0) + sum(_h * wh.reshape((-1, 1)), axis=0))
            h_est_mm = sum(_h * wh.reshape((-1, 1)), axis=0)
        else:
            h_est_mm = ()

        self.config_est = deepcopy(self.config)
        self.config_est['mut'][self.unknown_layer]['epsilon_r'] = epsr_est if use_linear_regression else epsr_est_raw
        for unknown_thickness, estimated_thck in zip(self.unknown_thicknesses, h_est_mm):
            self.config_est['mut'][unknown_thickness]['thickness'] = estimated_thck * .001

        if len(initial_guess_values) >= 3:
            return epsr_est, epsr_est_raw, h_est_mm
        else:
            return epsr_est, epsr_est_raw


    def fit(self, x, freq_idx, model, args=None):
        if args is None:
            args = {}
        freq_ghz = self.frequencies_ghz[freq_idx]

        if len(x) == 2:
            # only permittivity (real, imag)
            bounds = ([1, 20], [-10., -0.00001])
        elif len(x) == 3:
            # thickness, permittivity (real, imag)
            bounds = ([1, 10.], [-10., -1e-6], [0.0001, 50])
        else:
            # thickness1, thickness2, permittivity (real, imag)
            bounds = ([1, 10.], [-10., -1e-6], [0.0001, 50], [0.0001, 50])

        _args = {
            's21_meas': .5 * (self.data[:, freq_idx, 1, 0] + self.data[:, freq_idx, 0, 1]),
            's11_meas': None,
            'use_abs': True,
            'config': self.config,
            'unknown_layer': self.unknown_layer,
            'unknown_thicknesses': self.unknown_thicknesses,
            'theta_y_deg_array': self.theta_y_deg_array,
            'theta_weight_array': self.theta_weight_array,
            'model': model
        }
        if 'bounds' in args and len(args['bounds']) == len(x):
            bounds = args['bounds']

        for key, val in args.items():
            _args[key] = val

        res = minimize(
            self.cost_function.eval,
            x0=asarray(x),
            args=(freq_ghz, _args),
            bounds=bounds,
            options=self.options,
            method='Nelder-Mead'
        )
        guess = res.x
        return {
            'guess': guess,
            'success': res.success,
            'fun': res.fun,
        }

    def load_experimental_data(self,
                               s2p_path: str,
                               poly_fit_degree: int = 0,
                               filter_window_length: int = 51,
                               filter_poly_order: int = 5,
                               half_window_length: int = 0,
                               n_angles_to_use: int = 3):
        """
        Load experimental S21 measurements from S2P files.

        Parameters
        ----------
        poly_fit_degree : int
            Degree of polynomial fit to smooth S21 vs angle. If 0, no smoothing.
        filter_window_length: int
            Window size to smooth S21 vs frequency. Defaults to 101
        filter_poly_order: int
            Degree of polynomial fit to smooth S21 vs frequency. Defaults to 5
        """

        # Load raw data with auto-selection of angles
        _angles_deg, self.raw_data, self.filtered_data, _angle_weights, opts = analyze_angle_independence(
            s2p_path,
            n_angles_to_select=n_angles_to_use, use_pairs=True,
            smoothing_window=filter_window_length,
            smoothing_poly=filter_poly_order)
        _, _, _, _, self.angles_pairs = opts

        self.theta_y_deg_array = asarray(_angles_deg, dtype=float)
        self.theta_weight_array = asarray(_angle_weights, dtype=float)

        # Perform polyfit if requested
        if poly_fit_degree > 0:
            s21_wrt_angle = zeros((self.theta_y_deg_array.shape[0], self.frequencies_ghz.shape[0]), dtype=complex)
            s21_wrt_angle_poly = zeros((self.theta_y_deg_array.shape[0], self.frequencies_ghz.shape[0]),
                                          dtype=complex)
            for i, mut in enumerate(self.filtered_data):
                s21_wrt_angle[i, :] = deepcopy(mut.s[:, 1, 0])

            for j, freq_GHz in enumerate(self.frequencies_ghz):
                s21_wrt_angle_poly[:, j] = poly_fit_cplx(self.theta_y_deg_array, s21_wrt_angle[:, j],
                                                         deg=poly_fit_degree)

            for i, mut in enumerate(self.filtered_data):
                s = zeros_like(mut.s, dtype=complex)
                s[:, 1, 0] = s21_wrt_angle_poly[i, :]
                s[:, 0, 1] = s21_wrt_angle_poly[i, :]
                self.data_list.append(Network(s=s, f=mut.f))
        else:
            self.data_list = self.filtered_data

        # Prepare measurement array
        _data = zeros((len(self.theta_y_deg_array), len(self.frequencies_ghz), 2, 2), dtype=complex)
        for i, angle_deg in enumerate(self.theta_y_deg_array):
            for j, _ in enumerate(self.frequencies_ghz):
                _data[i, j, 0, 0] = self.data_list[i].s[j, 0, 0]
                _data[i, j, 0, 1] = self.data_list[i].s[j, 0, 1]
                _data[i, j, 1, 0] = self.data_list[i].s[j, 1, 0]
                _data[i, j, 1, 1] = self.data_list[i].s[j, 1, 1]
        self.data = _data

        # frequency array (GHz)
        self.frequencies_ghz = self.raw_data[0].f * 1e-9