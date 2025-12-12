from copy import deepcopy

from numpy import asarray, nan, linspace, isscalar, zeros, full_like
from qosm import load_config_from_toml, filter_s2p
from scipy.interpolate import interp1d
from scipy.optimize import minimize
import skrf as rf

from pycarmat.inverse_model.tools import linear_regression_from_interp, load_s2p_file, linear_regression


class CostFunction:
    def __init__(self, fn, score_fn):
        self.fn = fn
        self.score_fn = score_fn

    def eval(self, x, freq_ghz, kwargs):
        return self.fn(x, freq_ghz, self.score_fn, kwargs)

class InverseProblem:
    def __init__(self, config_file, cost_fn, score_fn, unknown_layer: int = 0, raise_error: bool = False):
        self.cost_function = CostFunction(cost_fn, score_fn)

        self.theta_y_deg_array = (0, )
        self.theta_weight_array = (1, )
        self.frequencies_ghz = []
        self.unknown_layer = unknown_layer

        # Data containers
        self.raw_data = []
        self.filtered_data = []
        self.data_list = []
        self.data = []
        self.angles_pairs = {}
        self.model = None
        self.fit_error = None
        self.raise_error = raise_error

        # initial config
        if isinstance(config_file, dict):
            self.config = config_file
        else:
            self.config = load_config_from_toml(config_file, load_csv=True)
        self.frequencies_ghz = linspace(
            float(self.config['sweep']['range'][0]),
            float(self.config['sweep']['range'][1]),
            int(self.config['sweep']['num_points']),
            True
        )
        for layer in self.config['mut']:
            if not isscalar(layer['epsilon_r']):
                layer['epsilon_r'] = linear_regression_from_interp(self.frequencies_ghz, layer['epsilon_r'])

        # estimated config
        self.config_est = None

        # Options
        self.options = {
            'maxiter': 10000,
            'xatol': 1./201.,
            'fatol': 1e-10,
            'adaptive': False
        }

    def set_tol(self, x_tol, f_tol, adaptive: bool = True):
        self.options['xatol'] = x_tol
        self.options['fatol'] = f_tol
        self.options['adaptive'] = adaptive

    def sweep(self, model, frequency_step: int = 1, pbar=None):
        _frequencies_ghz = self.frequencies_ghz[::frequency_step]
        _config = deepcopy(self.config_est) if self.config_est is not None else deepcopy(self.model)

        if pbar is not None:
            pbar.reset(_frequencies_ghz.shape[0])

        _i = 0
        _s = zeros((len(_frequencies_ghz), 2, 2), dtype=complex)
        for k in range(len(_frequencies_ghz)):
            _s[k, 0, 0], _s[k, 0, 1], _s[k, 1, 0], _s[k, 1, 1] = model.simulate(_config, _frequencies_ghz[_i])
            _i += frequency_step

        if pbar is not None:
            pbar.close()

        net = rf.Network(s=_s, f=_frequencies_ghz*1e9, f_unit='Hz')
        return net


    def sweep_fit(self, model, initial_guess_values, frequency_step: int = 1, pbar=None, args=None,
                  use_linear_regression: bool = False):
        if args is None:
            args = {}
        self.model = model
        _frequencies_ghz = self.frequencies_ghz[::frequency_step]
        _e = zeros((_frequencies_ghz.shape[0], 2))

        if pbar is not None:
            pbar.reset(_frequencies_ghz.shape[0])

        _i = 0
        self.fit_error = full_like(_frequencies_ghz, nan)
        for k in range(len(_frequencies_ghz)):
            res = self.fit(x=initial_guess_values, freq_idx=_i, model=model, args=args)
            if not res['success']:
                if self.raise_error:
                    raise RuntimeError("Unable to fit model")
                else:
                    _e[k, :] = (nan, nan)
            else:
                self.fit_error[k] = res['fun']
                _e[k, :] = res['epsilon_r']
                initial_guess_values = res['guess']
            if pbar is not None:
                pbar.update(1)
            _i += frequency_step
        if pbar is not None:
            pbar.close()

        n_points = len(_frequencies_ghz)
        if n_points >= 3:
            interp_kind = 'quadratic'
        elif n_points == 2:
            interp_kind = 'linear'
        else:  # n_points == 1
            interp_kind = 'nearest'

        epsr_est_raw = interp1d(_frequencies_ghz, _e[:, 0] + 1j * _e[:, 1], kind=interp_kind, fill_value="extrapolate")
        epsr_est = linear_regression(_frequencies_ghz, _e[:, 0], _e[:, 1], slope_mode='less')

        if self.config_est is None:
            self.config_est = deepcopy(self.config)

        if len(self.config_est['mut']) > 1:
            # multi-layer case
            self.config_est['mut'][self.unknown_layer]['epsilon_r'] = epsr_est \
                if use_linear_regression else epsr_est_raw
        else:
            # single-layer case
            self.unknown_layer = 0
            self.config_est['mut'][0]['epsilon_r'] = epsr_est if use_linear_regression else epsr_est_raw

        return epsr_est, epsr_est_raw

    def fit(self, x, freq_idx, model, args=None):
        if args is None:
            args = {}
        freq_ghz = self.frequencies_ghz[freq_idx]
        bounds = ([1, 20], [-10., -1e-6])

        _args = {
            's21_meas': .5 * (self.data[:, freq_idx, 1, 0] + self.data[:, freq_idx, 0, 1]),
            's11_meas': None,
            'use_abs': True,
            'config': self.config,
            'unknown_layer': self.unknown_layer,
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

        return {
            'epsilon_r': (res.x[0], res.x[1]),
            'thickness_mm': (nan,),
            'guess': res.x,
            'success': res.success,
            'fun': res.fun,
        }

    def load_experimental_data(self,
                               s2p_path: str,
                               poly_fit_degree: int = 0,
                               filter_window_length: int = 51,
                               filter_poly_order: int = 5,
                               half_window_length: int = 0):
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
        self.raw_data = rf.Network(s2p_path)
        if half_window_length > 0:
            self.filtered_data = (filter_s2p(s2p_path, half_window_length, extrapolate=True), )
        else:
            self.filtered_data = (load_s2p_file(s2p_path, filter_window_length, filter_poly_order), )
        self.theta_y_deg_array = asarray((0, ), dtype=float)
        self.theta_weight_array = asarray((1, ), dtype=float)
        sizes = self.filtered_data[0].s.shape
        self.data = zeros((1, sizes[0], sizes[1], sizes[2]), dtype=complex)
        self.data[0, :, :, :] = self.filtered_data[0].s
        self.frequencies_ghz = self.raw_data.f * 1e-9