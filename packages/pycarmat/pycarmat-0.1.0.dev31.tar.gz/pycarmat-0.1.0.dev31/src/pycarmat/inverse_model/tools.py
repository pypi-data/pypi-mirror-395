import numpy as np

from scipy import signal
from scipy.constants import c
from scipy.interpolate import interp1d
from scipy.stats import linregress

import skrf as rf

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib import pyplot as plt


class _Regression:
    def __init__(self, slope, intercept):
        self.slope = slope
        self.intercept = intercept


def compute_s11_with_phase_correction(s11, s22, thickness, freq_GHz):
    """
    Calculate S11 parameter with phase correction for total sample thickness.

    This method applies a phase correction to the S11*S22 product to account for
    the total propagation distance through the material under test.

    Args:
        s11 (complex): Simulated S11 parameter
        s22 (complex): Simulated S22 parameter
        thickness (float): Total thickness of the sample in meters
        freq_GHz (float): Frequency in GHz

    Returns:
        complex: Phase-corrected S11 value
    """
    k0 = 2 * np.pi * freq_GHz * 1e9 / c
    f = np.exp(-1j * k0 * thickness)
    return np.sqrt(abs(s11 * s22)) * np.exp(1j * np.angle(s11 * s22 * f))


def load_s2p_file(s2p_file, filter_window_length, filter_poly_order):
    mut = rf.Network(s2p_file)
    mut.s[:, 0, 0] = (smoothing(np.real(mut.s[:, 0, 0]), filter_window_length, filter_poly_order)
                      + 1j * smoothing(np.imag(mut.s[:, 0, 0]), filter_window_length, filter_poly_order))
    mut.s[:, 0, 1] = (smoothing(np.real(mut.s[:, 0, 1]), filter_window_length, filter_poly_order)
                      + 1j * smoothing(np.imag(mut.s[:, 0, 1]), filter_window_length, filter_poly_order))
    mut.s[:, 1, 0] = (smoothing(np.real(mut.s[:, 1, 0]), filter_window_length, filter_poly_order)
                      + 1j * smoothing(np.imag(mut.s[:, 1, 0]), filter_window_length, filter_poly_order))
    mut.s[:, 1, 1] = (smoothing(np.real(mut.s[:, 1, 1]), filter_window_length, filter_poly_order)
                      + 1j * smoothing(np.imag(mut.s[:, 1, 1]), filter_window_length, filter_poly_order))
    return rf.Network(s=mut.s, f=mut.f)


def load_parameters(filepath1, filepath2, smoothing_window, smoothing_poly):
    mut1 = rf.Network(filepath1)
    mut2 = rf.Network(filepath2)
    _s21 = .25 * (mut1.s[:, 1, 0] + mut1.s[:, 0, 1] + mut2.s[:, 1, 0] + mut2.s[:, 0, 1])
    _s11 = .5 * (mut1.s[:, 0, 0] + mut2.s[:, 0, 0])
    _s22 = .5 * (mut1.s[:, 1, 1] + mut2.s[:, 1, 1])
    s = np.zeros_like(mut1.s)
    s[:, 0, 0] = _s11
    s[:, 1, 0] = _s21
    s[:, 0, 1] = _s21
    s[:, 1, 1] = _s22
    s2 = deepcopy(s)
    s2[:, 0, 0] = smoothing(_s11, smoothing_window, smoothing_poly)
    s2[:, 1, 0] = smoothing(_s21, smoothing_window, smoothing_poly)
    s2[:, 0, 1] = smoothing(_s21, smoothing_window, smoothing_poly)
    s2[:, 1, 1] = smoothing(_s22, smoothing_window, smoothing_poly)
    return rf.Network(s=s, f=mut1.f, f_unit='Hz'), rf.Network(s=s2, f=mut1.f, f_unit='Hz')


def smoothing(sig, window_length: int = 51, poly_order: int = 3):
    sig_real_smooth = signal.savgol_filter(sig.real, window_length, poly_order)
    sig_imag_smooth = signal.savgol_filter(sig.imag, window_length, poly_order)
    return sig_real_smooth + 1j * sig_imag_smooth



def weighted_linear_regression(x, y, weights):
    """
    Perform a weighted linear regression y = a*x + b
    weights: array of weights (larger = more important)
    """
    # Convert to numpy arrays
    x = np.asarray(x)
    y = np.asarray(y)
    w = np.asarray(weights)

    # Weighted averages
    w_sum = np.sum(w)
    x_mean = np.sum(w * x) / w_sum
    y_mean = np.sum(w * y) / w_sum

    # Weighted slope and intercept
    cov_xy = np.sum(w * (x - x_mean) * (y - y_mean))
    var_x = np.sum(w * (x - x_mean)**2)

    slope = cov_xy / var_x
    intercept = y_mean - slope * x_mean

    return _Regression(slope, intercept)


def linear_regression(x, y_real, y_imag, slope_mode='two-sided', weights=None):
    if weights is None:
        res_re = linregress(x, y_real, alternative=slope_mode)
        res_im = linregress(x, y_imag, alternative=slope_mode)
    else:
        res_re = weighted_linear_regression(x, y_real, weights=weights)
        res_im = weighted_linear_regression(x, y_imag, weights=weights)

    res = res_re.intercept + res_re.slope * x + 1j * (
          res_im.intercept + res_im.slope * x
    )
    return interp1d(x, res, kind='linear', fill_value="extrapolate")

def linear_regression_from_interp(x, fn):
    res_re = linregress(x, np.real(fn(x)))
    res_im = linregress(x, np.imag(fn(x)))
    res = res_re.intercept + res_re.slope * x + 1j * (
          res_im.intercept + res_im.slope * x
    )
    return interp1d(x, res, kind='linear', fill_value="extrapolate")


def poly_fit_cplx(x, y, deg=10):
    coeffs_re = np.polyfit(x, np.real(y), deg)
    coeffs_im = np.polyfit(x, np.imag(y), deg)
    y_fit = np.poly1d(coeffs_re)(x) + np.poly1d(coeffs_im)(x) * 1j
    return y_fit


def display_s21(obj, data=None):
    frequencies_ghz = obj.frequencies_ghz

    _, ax = plt.subplots(obj.theta_y_deg_array.shape[0], 2, figsize=(20, 10))
    for i, angle in enumerate(obj.theta_y_deg_array):
        angle_str = f'{angle:.2f}'
        ax[i, 0].plot(frequencies_ghz, obj.raw_data[i].s_db[:, 1, 0], linewidth=2, alpha=.4, label='raw data')
        ax[i, 0].plot(frequencies_ghz, obj.data[i].s_db[:, 1, 0], linewidth=2, label='processed data')
        if data is not None:
            ax[i, 0].plot(frequencies_ghz, data[angle_str].s_db[:, 1, 0], linewidth=2, label='estimated data')

        ax[i, 0].set_xlabel('Frequency (GHz)', fontsize=15)
        ax[i, 0].set_ylabel(f'$\\theta = {angle}$°\n|S21| (dB)', fontsize=15)
        ax[i, 0].legend()

        ax[i, 1].plot(frequencies_ghz, np.angle(obj.raw_data[i].s[:, 1, 0]), linewidth=2, alpha=.4, label='raw data')
        ax[i, 1].plot(frequencies_ghz, np.angle(obj.data[i].s[:, 1, 0]), linewidth=2, label='processed data')
        if data is not None:
            ax[i, 1].plot(frequencies_ghz, np.angle(data[angle_str].s[:, 1, 0]), linewidth=2, label='estimated data')
        ax[i, 1].set_xlabel('Frequency (GHz)', fontsize=15)
        ax[i, 1].set_ylabel(f'$\\angle$ S21 (rad)', fontsize=15)
        ax[i, 1].legend()

def display_s11(obj, data):
    frequencies_ghz = obj.frequencies_ghz

    _, ax = plt.subplots(2, 1, figsize=(20, 10))
    ax[0].plot(frequencies_ghz, obj.raw_data[0].s_db[:, 0, 0], linewidth=2, alpha=.4, label='raw data')
    ax[0].plot(frequencies_ghz, obj.data[0].s_db[:, 0, 0], linewidth=2, label='processed data')
    ax[0].plot(frequencies_ghz, data['0.00'].s_db[:, 0, 0], linewidth=2, label='estimated data')

    ax[0].set_xlabel('Frequency (GHz)', fontsize=15)
    ax[0].set_ylabel(f'|S11| (dB)', fontsize=15)
    ax[0].legend()

    ax[1].plot(frequencies_ghz, np.unwrap(np.angle(obj.raw_data[0].s[:, 0, 0])), linewidth=2, alpha=.4, label='raw data')
    ax[1].plot(frequencies_ghz, np.unwrap(np.angle(obj.data[0].s[:, 0, 0])), linewidth=2, label='processed data')
    ax[1].plot(frequencies_ghz, np.unwrap(np.angle(data['0.00'].s[:, 0, 0])), linewidth=2, label='estimated data')
    ax[1].set_xlabel('Frequency (GHz)', fontsize=15)
    ax[1].set_ylabel(f'$\\angle$ S11 (rad)', fontsize=15)
    ax[1].legend()
