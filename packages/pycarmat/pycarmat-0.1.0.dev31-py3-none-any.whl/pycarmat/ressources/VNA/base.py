from time import sleep

import matplotlib.pyplot as plt
import pyvisa
import skrf as rf
import numpy as np
from scipy.interpolate import interp1d

def wrap(unwrapped_phase_rad: float | np.ndarray) -> float | np.ndarray:
    """
    Wraps the phase between -π and π.

    Args:
        unwrapped_phase_rad (float | np.ndarray): The unwrapped phase in radians.

    Returns:
        float | np.ndarray: The wrapped phase in radians, within the range [-π, π].

    Notes:
        - If `unwrapped_phase_rad` is a numpy array, the operation is applied element-wise.
        - This function is useful for handling phase discontinuities in signal processing.
    """
    return (unwrapped_phase_rad + np.pi) % (2 * np.pi) - np.pi


class _VNA_:
    """
    A class to interface with a Vector Network Analyzer (VNA).

    This class provides methods for configuring, controlling, and retrieving S-parameter
    measurements from a VNA using an API.
    """

    def __init__(self, ip_address: str, simulate: bool = False, load: str = None, reset_instr: bool = False):
        """
        Initializes the VNA connection and configures simulation mode if required.

        Args:
            ip_address (str): The IP address of the VNA for TCP/IP communication.
            simulate (bool, optional): If True, enables simulation mode. Default is False.
            load (str, optional): Path to an S2P file for simulation mode. Default is None.
            reset_instr (bool, optional): If True, resets the VNA to default settings. Default is False.

        """
        self.ip = f'TCPIP::{ip_address}::INSTR'
        print(self.ip)
        self.vna = None
        self.frequency_sweep = (0, 0, 0)
        self._simulate = simulate
        self._reset_instr = reset_instr
        self._sim_file = load

    def __enter__(self):
        """
        Establishes a connection to the VNA when entering a context.
        """
        return self

    def __exit__(self, *exc):
        """
        Closes the VNA connection when exiting a context.

        Args:
            *exc (tuple): Exception type, value, and traceback (if any), passed automatically by the context manager.
        """
        if self.vna is not None:
            self.reset()
            self.vna.close()
            self.vna = None

    @property
    def frequencies_GHz(self) -> np.ndarray:
        """
        Computes the frequency sweep in GHz as a numpy array.
        The frequencies are generated using `numpy.linspace` and the sweep settings defined in `frequency_sweep`.

        Returns:
            np.ndarray: A numpy array of frequencies in GHz, equally spaced between `freq_start` and `freq_end`.
        """
        freq_start, freq_end, num_points = self.frequency_sweep
        return np.linspace(freq_start, freq_end, int(num_points), endpoint=True)

    def _com_prep(self, timeout: float = 50000) -> None:
        """
        Prepares the communication settings for the VNA.

        Args:
            timeout (float, optional): The timeout value in milliseconds. Default is 50000 ms.
        """
        self.vna.visa_timeout = timeout
        self.vna.opc_timeout = timeout
        self.vna.instrument_status_checking = True
        self.vna.clear_status()

    def _load_s2p_data(self, s_param: str, return_format: str):
        """
        Loads S-parameter data from an S2P file or generates pseudo-random data for simulation.

        Args:
            s_param (str): The S-parameter to retrieve (e.g., 'S11', 'S12', 'S21', 'S22').
            return_format (str): The desired format for the data ('RI' or 'DB').

        Returns:
            tuple[list[float], list[float]]: The real/imaginary or magnitude/phase data.

        Raises:
            RuntimeError: If the frequency range of the S2P file does not match the required sweep.
        """
        if self._sim_file is None:
            if return_format.upper() == 'RI':
                data_1 = np.random.uniform(low=0.05, high=0.1, size=(self.frequency_sweep[2],))
            else:
                data_1 = np.random.uniform(low=-20, high=-1.5, size=(self.frequency_sweep[2],))
            data_2 = wrap(
                np.random.uniform(low=0.1, high=0.9, size=(1,)) * self.frequencies_GHz
                + np.random.uniform(low=-2, high=2, size=(1,)))
        else:
            s2p_data = rf.Network(self._sim_file)
            if np.min(s2p_data.f * 1e-9) != self.frequency_sweep[0] or \
                    np.max(s2p_data.f * 1e-9) != self.frequency_sweep[1]:
                raise RuntimeError('S2P file not in same frequency range')

            idxs = {'S11': (0, 0), 'S12': (0, 1), 'S21': (1, 0), 'S22': (1, 1)}
            i1, i2 = idxs[s_param]
            if return_format.upper() == 'RI':
                data_1 = np.real(s2p_data.s[:, i1, i2])
                data_2 = np.imag(s2p_data.s[:, i1, i2])
            else:
                data_1 = s2p_data.s_db[:, i1, i2]
                data_2 = np.angle(s2p_data.s[:, i1, i2], deg=True)

            _sim_freq_GHz = s2p_data.f * 1e-9
            interp_func1 = interp1d(_sim_freq_GHz, data_1, kind='cubic')
            interp_func2 = interp1d(_sim_freq_GHz, data_2, kind='cubic')
            data_1 = interp_func1(self.frequencies_GHz)
            data_2 = interp_func2(self.frequencies_GHz)

        return data_1.tolist(), data_2.tolist()

    def set_sweep(self, freq_start_GHz: float, freq_end_GHz: float, num_pts: int, bandwidth: str) -> None:
        """
        Configures the frequency sweep settings for the VNA.

        Args:
            freq_start_GHz (float): The starting frequency of the sweep in GHz.
            freq_end_GHz (float): The ending frequency of the sweep in GHz.
            num_pts (int): The number of points in the frequency sweep.
            bandwidth (float): Measure bandwidth in Hz
        """
        self.vna.write(f'SENS1:FREQ:START {freq_start_GHz} GHZ')
        self.vna.write(f'SENS1:FREQ:STOP {freq_end_GHz} GHZ')
        self.vna.write(f'SENS1:SWE:POIN {num_pts}')
        self.vna.write(f'SENS1:BWID:RES {bandwidth.upper()}')
        self.frequency_sweep = (freq_start_GHz, freq_end_GHz, num_pts)

    def sweep(self, return_format: str = 'RI') -> np.ndarray | tuple:
        """
        Performs a single frequency sweep measurement for all S-parameters.

        Args:
            return_format (str, optional): The format of the returned data ('RI' or 'DB'). Default is 'RI'.

        Returns:
            np.ndarray | dict: The measured data in the specified format.

        Raises:
            RuntimeError: If an invalid `return_format` is provided.
        """
        pass

    def single_sweep(self, s_param: str, return_format: str = 'RI') -> np.ndarray | tuple:
        """
        Performs a single frequency sweep measurement for a specified S-parameter.

        Args:
            s_param (str): The S-parameter to measure (e.g., 'S11', 'S12', 'S21', 'S22').
            return_format (str, optional): The format of the returned data ('RI' or 'DB'). Default is 'RI'.

        Returns:
            np.ndarray | dict: The measured data in the specified format.

        Raises:
            RuntimeError: If an invalid `return_format` is provided.
        """
        pass

    def measure(self, num_iterations: int = 1, return_format: str = 's2p', file_path: str = None, progress_bar=None) \
            -> np.ndarray | rf.Network:
        """
        Performs multiple VNA sweeps and returns the measured S-parameters.

        Args:
            num_iterations (int, optional): The number of frequency sweep iterations. Default is 1.
            return_format (str, optional): The output format ('s2p' or 'matrix'). Default is 's2p'.
            file_path (str, optional): Path to save the measured data as an S2P file.
            progress_bar (Any, optional): Progress Bar object. Must have those methods: setMaximum() and setValue().

        Returns:
            rf.Network | np.ndarray: The measured S-parameters in the specified format.

        Raises:
            ValueError: If an invalid `return_format` is specified.
        """
        results = np.zeros((self.frequency_sweep[2], 2, 2), dtype=complex)

        if progress_bar is not None:
            progress_bar.setMaximum(num_iterations)

        for i in range(num_iterations):
            results[:, 0, 0], results[:, 0, 1], results[:, 1, 0], results[:, 1, 1] = \
                self.sweep(return_format='RI')
            if progress_bar is not None:
                progress_bar.setValue(i)

        results /= float(num_iterations)

        s2p = rf.Network(s=results, f=self.frequencies_GHz * 1e9, f_unit='Hz')
        if file_path is not None:
            s2p.write_touchstone(file_path)
            print(f"S2P file created successfully: {file_path}")

        if return_format.lower() == 's2p':
            return s2p
        elif return_format.lower() == 'matrix':
            return results
        else:
            raise ValueError('Invalid return format: %s (valid: s2p, matrix)' % return_format)

    def reset(self):
        pass


    def enable_trl_calibration(self, cal_kit: str):
        pass

    def save_trl_calibration(self):
        pass

    def perform_thru_measurement(self):
        pass

    def perform_line_measurement(self):
        pass

    def perform_reflect_measurement(self):
        pass

    def turn_off_calibration(self) :
        """
        Turns off the current calibration.
        """
        pass

    def turn_on_calibration(self) -> bool:
        """
        Turns on calibration (if one is loaded).
        """
        pass

