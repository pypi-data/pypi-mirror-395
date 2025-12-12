from copy import deepcopy

import numpy as np
from numpy import ndarray, zeros, tanh, abs
import skrf as rf
from scipy.interpolate import interp1d
from scipy.optimize import differential_evolution
from scipy.stats import linregress
from tqdm import tqdm


class PermittivityEstimation:
    """
    Class for permittivity estimation models using S-parameters.

    This class provides the framework for estimating complex permittivity of materials
    under test (MUT) using electromagnetic simulation and inverse optimization techniques.

    Attributes
    ----------
    model : class instance
        Forward model for the permittivity estimation.
    params : dict
        Configuration parameters for the estimation.
    s_idx : int
        Index of the sample layer to characterize in multi-layer configurations.
    """

    model_name: str = 'None'

    def __init__(self, params, model, unknown_sample_index=0):
        """
        Initialize the permittivity estimation model.

        Parameters
        ----------
        params : dict
            Dictionary containing all configuration options for frequency sweep and fitting.
            Must include 'frequencies_GHz' key with frequency array.
        model : class instance
            Forward model of the permittivity estimation.
        unknown_sample_index : int, optional
            Index of the sample to characterize in multi-layer slab configurations.
            Default is 0 (first layer).
        """
        self.params = deepcopy(params)
        self.model = model
        self.s_idx = unknown_sample_index

    @property
    def frequencies_GHz(self):
        """
        Get the frequency array in GHz.

        Returns
        -------
        array_like
            Frequency array in GHz from the parameters dictionary.
        """
        return self.params['frequencies_GHz']

    def _cost_function(self, eps: tuple, frequency_GHz: float, s_to_fit: ndarray, param: str = 's21',
                       phys_constraint: bool = False) -> float:
        """
        Compute the cost function for permittivity optimization.

        Calculates the error between simulated and measured S-parameters with
        physical constraints to ensure realistic permittivity values.

        Parameters
        ----------
        eps : tuple
            Two-element tuple containing (real_part, imaginary_part) of permittivity.
        frequency_GHz : float
            Operating frequency in GHz.
        s_to_fit : ndarray
            Reference S-parameter value (complex) for fitting.
        param : str, optional
            S-parameter to use for fitting ('s21' supported). Default is 's21'.
        phys_constraint: bool, optional
            Constrains the imaginary part to be negative

        Returns
        -------
        float
            Calculated cost function value including physical penalties.

        Notes
        -----
        The cost function includes:
        - Bidirectional error calculation between simulated and measured values
        - Handle physical penalties for non-physical permittivity values (Im(ε) ≤ 0)
        - Hyperbolic tangent normalization using coefficient_3d parameter
        """
        self.params['mut'][self.s_idx]['epsilon_r'] = eps[0] + 1j * eps[1]
        S11calc, _, S21calc, _ = self.model.simulate(frequency_GHz)
        coefficient_3d = self.params.get('coefficient_3d', 10)

        # Error calculation
        err1 = 1 - s_to_fit / S21calc
        err2 = 1 - S21calc / s_to_fit

        penalty = (1e10 if eps[1] > 0 else 0) if phys_constraint else 0

        # Final Cost Function
        return abs(tanh((1 / coefficient_3d) * abs(err1 * err2)) + penalty)

    def sweep(self, min_value_db: float = -60, use_bar: bool = True) -> rf.Network:
        """
        Perform frequency sweep simulation with dynamic range clipping.

        Simulates S-parameters across the frequency range defined in parameters,
        with optional clipping of low-amplitude values to prevent numerical issues.

        Parameters
        ----------
        min_value_db : float, optional
            Minimum amplitude level in dB. Values below this threshold are clipped
            to this level while preserving phase. Default is -60 dB.
        use_bar : bool, optional
            Whether to display a progress bar during simulation. Default is True.

        Returns
        -------
        skrf.Network
            Network object containing simulated S-parameters across frequency range.

        Notes
        -----
        - Supports frequency-dependent permittivity if specified in parameters
        - Automatically handles multi-layer configurations
        - Preserves phase information when clipping amplitude
        """
        frequencies_GHz = self.params['frequencies_GHz']

        # backup original param dict
        _params = deepcopy(self.params)

        # frequency sweep
        S = np.zeros((frequencies_GHz.shape[0], 2, 2), dtype=complex)
        if use_bar:
            bar = tqdm(total=len(frequencies_GHz), desc="%s model => Sweep" % self.model_name)
        else:
            bar = None

        for i, freq_GHz in enumerate(frequencies_GHz):
            if use_bar:
                bar.update(1)

            # Handle frequency-dependent permittivity
            for m, mut in enumerate(_params['mut']):
                if 'epsilon_r' in mut and hasattr(mut['epsilon_r'], "__len__"):
                    self.params['mut'][m]['epsilon_r'] = mut['epsilon_r'][i] + 0j

            S[i, 0, 0], S[i, 0, 1], S[i, 1, 0], S[i, 1, 1] = self._simulate(freq_GHz)

        # Apply dynamic range clipping
        id_1 = 20 * np.log10(np.abs(S[:, 0, 0])) < min_value_db
        id_2 = 20 * np.log10(np.abs(S[:, 0, 1])) < min_value_db
        id_3 = 20 * np.log10(np.abs(S[:, 1, 0])) < min_value_db
        id_4 = 20 * np.log10(np.abs(S[:, 1, 1])) < min_value_db

        S[id_1, 0, 0] = 10 ** (min_value_db / 20.) * np.exp(1j * np.angle(S[id_1, 0, 0]))
        S[id_2, 0, 1] = 10 ** (min_value_db / 20.) * np.exp(1j * np.angle(S[id_2, 0, 1]))
        S[id_3, 1, 0] = 10 ** (min_value_db / 20.) * np.exp(1j * np.angle(S[id_3, 1, 0]))
        S[id_4, 1, 1] = 10 ** (min_value_db / 20.) * np.exp(1j * np.angle(S[id_4, 1, 1]))

        # restore original param dict
        self.params = _params

        return rf.Network(s=S, f=frequencies_GHz, f_unit='GHz')

    def fit(self, s_params_to_fit: rf.Network | str, initial_guess: complex, method: str = 'Nelder-Mead',
            fit_options: dict | None = None, **kwargs) -> ndarray:
        """
        Estimate complex permittivity by inverse optimization over frequency band.

        Performs frequency-by-frequency optimization to extract permittivity values
        by minimizing the difference between measured and simulated S-parameters.

        Parameters
        ----------
        s_params_to_fit : skrf.Network or str
            Measured S-parameters as Network object or filepath to S2P file.
        initial_guess : complex
            Starting value for permittivity optimization (real + 1j*imag).
        method : str, optional
            Optimization algorithm for scipy.minimize. Default is 'Nelder-Mead'.
        fit_options : dict, optional
            Additional options passed to scipy.minimize optimizer.
        **kwargs : keyword arguments
            Additional fitting parameters:

            - half_win_size : int, optional
                Moving average window size for input data smoothing. Default is 0 (no smoothing).
            - use_parameter : str, optional
                S-parameter to fit against ('s11' or 's21'). Default is 's21'.
            - interpolate_to : int, optional
                Number of frequency points to interpolate data onto. Default is 0 (no interpolation).
            - idx_input : tuple, optional
                S-parameter matrix indices (i,j) to extract from network. Default is (1,0) for S21.
            - lambda_reg : float, optional
                Spectral regularization weight for smoothness constraint. Default is 0.00.
            - use_bar : bool, optional
                Whether to show progress bar. Default is True.

        Returns
        -------
        ndarray
            Array of shape (N, 2) containing permittivity estimates where:
            - Column 0: Real part of relative permittivity
            - Column 1: Imaginary part of relative permittivity (positive for losses)

        Notes
        -----
        - Uses spectral regularization to promote smoothness across frequency
        - Handles NaN values gracefully in input data
        - Supports both file input and direct Network objects
        - Previous frequency point results are used to improve convergence
        """
        # Extract keyword arguments with defaults
        half_win_size = kwargs.get('half_win_size', 0)
        lambda_reg = kwargs.get('lambda_reg', 0.)
        use_bar = kwargs.get('use_bar', True)
        use_parameter = kwargs.get('use_parameter', 's21')
        input_parameter = kwargs.get('input_parameter', 's21').lower()
        interpolate_to = kwargs.get('interpolate_to', 0)

        # Load S-parameters if string filepath provided (without filtering)
        if isinstance(s_params_to_fit, str):
            s_params_to_fit = filter_s2p(s_params_to_fit, half_window_size=0)

        # Get the initial frequency array from the data to fit
        frequencies_GHz = s_params_to_fit.f * 1e-9
        if input_parameter in ('s21', 's12'):
            # transmission measurement mode
            s_to_fit1 = s_params_to_fit.s[:, 1, 0]
            s_to_fit2 = s_params_to_fit.s[:, 0, 1]
        elif input_parameter in ('s11', 's22'):
            # reflection measurement mode
            s_to_fit1 = s_params_to_fit.s[:, 0, 0]
            s_to_fit2 = s_params_to_fit.s[:, 1, 1]
        else:
            raise AttributeError(f'Invalid input parameter: {input_parameter}')

        # backup original param dict
        _params = deepcopy(self.params)

        # fitting options
        if fit_options is None:
            fit_options = {}
        eps_re_min = fit_options.get('eps_re_min', 1.)
        eps_re_max = fit_options.get('eps_re_max', 10.)
        num_points = fit_options.get('num_points', 201)
        _fit_options = {
            'maxiter': fit_options.get('max_iter', 10000),
            'fatol': fit_options.get('func_tol', 1e-15),
            'xatol': (eps_re_max - eps_re_min) / (num_points -1),
            'maxfev': fit_options.get('max_fun_eval', 10000),
            'adaptive': fit_options.get('adaptive', False)
        }

        # Optional interpolation to different frequency grid
        if interpolate_to > 0:
            _frequencies_GHz = np.linspace(frequencies_GHz[0], frequencies_GHz[-1], interpolate_to, endpoint=True)

            fn1 = interp1d(frequencies_GHz, s_to_fit1, kind='cubic', bounds_error=False, fill_value="extrapolate")
            fn2 = interp1d(frequencies_GHz, s_to_fit2, kind='cubic', bounds_error=False, fill_value="extrapolate")
            s_to_fit1 = fn1(_frequencies_GHz)
            s_to_fit2 = fn2(_frequencies_GHz)
            frequencies_GHz = _frequencies_GHz

        # store the frequency array
        self.params['frequencies_GHz'] = frequencies_GHz

        # Apply moving average smoothing if requested
        if half_win_size > 1:
            s_to_fit1 = moving_average(s_to_fit1, half_win_size)
            s_to_fit2 = moving_average(s_to_fit2, half_win_size)
            frequencies_GHz_used = frequencies_GHz[half_win_size:-half_win_size]
        else:
            frequencies_GHz_used = frequencies_GHz

        # used data : mean between the two parameters (S21 & S12 or S11 & S22)
        s_to_fit = .5 * (s_to_fit1 + s_to_fit2)

        i_start = half_win_size
        bar = tqdm(total=len(frequencies_GHz_used), desc="%s model => Fit" % self.model_name) if use_bar else None

        # Frequency-by-frequency optimization
        epsilon_r = zeros((frequencies_GHz.shape[0], 2)) * np.nan

        # for the lower frequency, use initial guess given by the user
        eps_init = [initial_guess.real, initial_guess.imag]
        for i, freq_GHz in enumerate(frequencies_GHz_used):
            if use_bar:
                bar.update(1)

            i_full = i + i_start
            prev_eps = epsilon_r[i_full - 1] if i > 0 else None

            # Handle frequency-dependent permittivity in other layers
            if len(_params['mut']) > 1:
                for m, mut in enumerate(_params['mut']):
                    if 'epsilon_r' in mut and hasattr(mut['epsilon_r'], "__len__"):
                        self.params['mut'][m]['epsilon_r'] = mut['epsilon_r'][i] + 0j

            def objective(eps):
                """Combined objective function with data fitting and regularization."""
                loss = self._cost_function(
                    eps, frequency_GHz=freq_GHz, s_to_fit=s_to_fit[i], param=use_parameter,
                    phys_constraint=kwargs.get('phys_constraint', False)
                )

                # Spectral regularization for smoothness
                reg = 0
                if prev_eps is not None and not np.any(np.isnan(prev_eps)):
                    reg = lambda_reg * float(np.linalg.norm(eps - prev_eps))**2

                return loss + reg

            # Initialize optimization
            # result = minimize(objective, eps_init, method=method, options=_fit_options, tol=_fit_options['fatol'])
            result = differential_evolution(
                objective,
                bounds=[(1.0, 10.0), (-1.0, -0.001)]  # Limites pour [eps_real, eps_imag]
            )
            if result.success:
                epsilon_r[i + i_start, :] = result.x

                # for all other frequencies, the initial guess is the last estimated guess
                eps_init = result.x
            else:
                eps_init = [initial_guess.real, initial_guess.imag]

        # restore original param dict
        self.params = _params
        self.params['frequencies_GHz'] = frequencies_GHz

        return epsilon_r

    def linear_regression(self, epsilon_r: ndarray) -> (ndarray, tuple, tuple, tuple):
        """
        Perform linear regression on complex permittivity vs frequency.

        Fits linear trends to both real and imaginary parts of permittivity
        as functions of frequency, useful for material characterization and
        extrapolation beyond measured frequency range.

        Parameters
        ----------
        epsilon_r : ndarray
            Array of shape (N, 2) where:
            - Column 0: Real part of relative permittivity
            - Column 1: Imaginary part of relative permittivity

        Returns
        -------
        regressed_values : ndarray
            Complex-valued array of regressed permittivity at all frequencies.
        re_params : tuple
            Linear fit parameters (slope, intercept) for real part.
        im_params : tuple
            Linear fit parameters (slope, intercept) for imaginary part.
        std_errs : tuple
            Standard errors (real_std_err, imag_std_err) of the regressions.

        Notes
        -----
        - Automatically handles NaN values by masking them out
        - Uses scipy.stats.linregress for robust linear fitting
        - Returns complex permittivity as: real_fit - 1j * imag_fit
        - Useful for identifying frequency-dependent material properties
        """
        frequencies_GHz = self.params['frequencies_GHz']

        # Remove NaN values for regression
        mask = ~np.isnan(epsilon_r[:, 0])

        # Linear regression on real part
        re_slope, re_intercept, _, _, re_std_err = linregress(frequencies_GHz[mask], epsilon_r[mask, 0])

        # Linear regression on imaginary part
        im_slope, im_intercept, _, _, im_std_err = linregress(frequencies_GHz[mask], epsilon_r[mask, 1])

        # Reconstruct complex permittivity from linear fits
        regressed_values = re_slope * frequencies_GHz + re_intercept + 1j * (
                im_slope * frequencies_GHz + im_intercept
        )

        return regressed_values, (re_slope, re_intercept), (im_slope, im_intercept), (re_std_err, im_std_err)


def moving_average(data, half_window_size, full_length: bool = False):
    """
    Calculate moving average of a data series using convolution.

    Applies a uniform window to smooth noisy data while preserving
    the overall trend characteristics.

    Parameters
    ----------
    data : array_like
        Input data series to be smoothed.
    half_window_size : int
        Half-size of the moving average window. Must be positive integer.
    full_length : bool
        Return an array of the same dimension than data if True (padding with NaN)

    Returns
    -------
    ndarray
        Smoothed data series with length (len(data) - window_size + 1).

    Notes
    -----
    - Uses numpy.convolve with 'valid' mode for computation
    - Output length is reduced by (window_size - 1) points
    - All window weights are equal (uniform averaging)
    """
    i_start = half_window_size
    i_end = len(data) - half_window_size

    moving_avg = np.zeros_like(data, dtype=complex) * (np.nan + 0j * np.nan)
    for i in range(i_start, i_end):
        moving_avg[i] = np.mean(data[i-half_window_size:i+half_window_size])

    if not full_length:
        moving_avg = moving_avg[i_start:i_end]
    return moving_avg


def filter_s2p(s2p: rf.Network | str, half_window_size):
    """
    Apply moving average filter to S-parameter data.

    Smooths all four S-parameters of a 2-port network using moving average
    filtering to reduce measurement noise while preserving spectral features.

    Parameters
    ----------
    s2p : skrf.Network or str
        Input S-parameter data as Network object or filepath to S2P file.
    half_window_size : int
        Moving average window size. If < 1, no filtering is applied.

    Returns
    -------
    skrf.Network
        Filtered S-parameter network with same frequency grid as input.
        Unfiltered regions are filled with NaN values.

    Notes
    -----
    - Filtering reduces valid data range by (window_size - 1) points
    - Edge regions are set to NaN to maintain frequency grid consistency
    - All four S-parameters (S11, S12, S21, S22) are filtered identically
    """
    if isinstance(s2p, str):
        s_file = rf.Network(s2p)
        frequencies_GHz = s_file.f * 1e-9
    else:
        s_file = s2p
        frequencies_GHz = s_file.f * 1e-9

    if half_window_size < 1:
        return s_file

    # Initialize with NaN and fill filtered regions
    S = np.zeros((frequencies_GHz.shape[0], 2, 2), dtype=complex) * (np.nan + 0j * np.nan)
    S[:, 0, 0] = moving_average(s_file.s[:, 0, 0], half_window_size, full_length=True)
    S[:, 0, 1] = moving_average(s_file.s[:, 0, 1], half_window_size, full_length=True)
    S[:, 1, 0] = moving_average(s_file.s[:, 1, 0], half_window_size, full_length=True)
    S[:, 1, 1] = moving_average(s_file.s[:, 1, 1], half_window_size, full_length=True)

    return rf.Network(s=S, f=frequencies_GHz, f_unit='GHz')

def rewrap_phase(phase, deg=False):
    """
    Rewrap phase data to remove discontinuities while preserving trends.

    Performs phase unwrapping relative to the first point, then rewraps
    to maintain continuity and standard phase range conventions.

    Parameters
    ----------
    phase : array_like
        Input phase data in radians (or degrees if deg=True).
    deg : bool, optional
        If True, input and output are in degrees. Default is False (radians).

    Returns
    -------
    ndarray
        Rewrapped phase data in range [-180°, 180°] (or [-π, π] for radians).

    Notes
    -----
    - First unwraps phase relative to initial value to remove 2π jumps
    - Then applies modulo operation to maintain standard phase range
    - Useful for S-parameter phase processing and visualization
    """
    factor = np.pi / 180 if deg else 1
    p = np.unwrap((phase - phase[0]) * factor)
    p = np.mod(p * 180 / np.pi + 180, 360) - 180
    return p


def add_noise(network: rf.Network, snr_db=40):
    """
    Add complex Gaussian noise to S-parameter measurements.

    Simulates measurement noise by adding complex white Gaussian noise
    to all S-parameters at a specified signal-to-noise ratio.

    Parameters
    ----------
    network : skrf.Network
        Original clean S-parameter network.
    snr_db : float, optional
        Signal-to-noise ratio in decibels. Default is 40 dB.

    Returns
    -------
    skrf.Network
        New Network object with additive noise applied to all S-parameters.

    Notes
    -----
    - Noise power is calculated relative to average signal power
    - Complex noise has equal power in real and imaginary components
    - Useful for testing robustness of permittivity extraction algorithms
    - Does not modify the original network object
    """
    noisy_network = network.copy()

    # Compute average signal power across all S-parameters
    signal_power = np.mean(np.abs(network.s) ** 2)

    # Convert SNR from dB to linear scale
    snr_linear = 10 ** (snr_db / 10)

    # Compute noise power per real/imaginary component
    noise_power = signal_power / snr_linear

    # Generate complex Gaussian noise
    noise_real = np.random.normal(scale=np.sqrt(noise_power / 2), size=network.s.shape)
    noise_imag = np.random.normal(scale=np.sqrt(noise_power / 2), size=network.s.shape)
    noise = noise_real + 1j * noise_imag

    # Add noise to the S-parameters
    noisy_network.s += noise

    return noisy_network, np.sqrt(noise_power / 2)