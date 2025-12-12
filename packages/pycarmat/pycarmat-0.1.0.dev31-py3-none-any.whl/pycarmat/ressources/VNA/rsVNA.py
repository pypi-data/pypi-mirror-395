import matplotlib.pyplot as plt
import RsInstrument
import numpy as np
from pycarmat.ressources.VNA.base import _VNA_


class RohdeSchwarzVNA(_VNA_):
    """
    A class to interface with a Vector Network Analyzer (VNA).

    This class provides methods for configuring, controlling, and retrieving S-parameter
    measurements from a VNA using the RsInstrument API. It supports real instrument
    communication as well as a simulation mode.
    """

    def __enter__(self):
        """
        Establishes a connection to the VNA when entering a context.

        Returns:
            VNA: The VNA instance with an active connection.

        Raises:
            ConnectionError: If the instrument cannot be accessed.
        """
        try:
            self.vna = RsInstrument.RsInstrument(self.ip, reset=self._reset_instr, id_query=True,
                                                 options=f'Simulate={self._simulate}')
        except RsInstrument.Internal.InstrumentErrors.ResourceError as e:
            raise ConnectionError(str(e))
        return self

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

    def set_sweep(self, freq_start_GHz: float, freq_end_GHz: float, num_pts: int, bandwidth: str) -> None:
        """
        Configures the frequency sweep settings for the VNA.

        Args:
            freq_start_GHz (float): The starting frequency of the sweep in GHz.
            freq_end_GHz (float): The ending frequency of the sweep in GHz.
            num_pts (int): The number of points in the frequency sweep.
            bandwidth (float): Measure bandwidth in Hz
        """
        self.vna.write_str(f':SENSe1:FREQuency:STARt {freq_start_GHz} GHZ')
        self.vna.write_str(f':SENSe1:FREQuency:STOP {freq_end_GHz} GHZ')
        self.vna.write_str(f':SENSe1:SWEep:POINts {num_pts}')
        self.vna.write_str(f':SENSe1:BWIDth:RESolution {bandwidth.upper()}')
        self.vna.write_str(':SENSe1:BWIDth:RESolution:DREDuction OFF')
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
        if return_format.upper() == 'RI':
            _cmp_ctrl = 0
            _trace1_format = 'REAL'
            _trace2_format = 'IMAG'
        elif return_format.upper() == 'DB':
            _cmp_ctrl = -999
            _trace1_format = 'MLOG'
            _trace2_format = 'PHAS'
        else:
            raise RuntimeError('Invalid format: %s' % return_format)

        # erase previous data
        self.vna.write_str('CALCulate:PARameter:DELete:ALL')

        # enable SINGLE SWEEP
        self.vna.write_str('INIT1:CONT OFF')

        # create trace for the S-
        _s_params = ('S11', 'S12', 'S21', 'S22')
        id_trace = 1

        for s_param in _s_params:
            self.vna.write_str(f'CALC1:PAR:SDEF "Trc{id_trace}","{s_param}"')
            self.vna.write_str(f'CALC1:PAR:MEAS "Trc{id_trace}","{s_param}"')
            self.vna.write_str(f'CALC1:PAR:SEL "Trc{id_trace}"')
            self.vna.write_str(f'CALC1:FORM {_trace1_format}')
            id_trace += 1

            self.vna.write_str(f'CALC1:PAR:SDEF "Trc{id_trace}","{s_param}"')
            self.vna.write_str(f'CALC1:PAR:MEAS "Trc{id_trace}","{s_param}"')
            self.vna.write_str(f'CALC1:PAR:SEL "Trc{id_trace}"')
            self.vna.write_str(f'CALC1:FORM {_trace2_format}')
            id_trace += 1

        # Launch the sweep
        self.vna.write_str('INIT1')

        _cmp_ctrl = (0 if return_format.upper() == 'RI' else -999)
        data_s11_1 = [_cmp_ctrl, ]
        data_s11_2 = None
        data_s12_1 = [_cmp_ctrl, ]
        data_s12_2 = None
        data_s21_1 = [_cmp_ctrl, ]
        data_s21_2 = None
        data_s22_1 = [_cmp_ctrl, ]
        data_s22_2 = None
        data_float_read = [0, ]
        while (np.min(data_s11_1) == _cmp_ctrl or np.min(data_s12_1) == _cmp_ctrl or np.min(data_s21_1) == _cmp_ctrl or
               np.min(data_s22_1) == _cmp_ctrl or np.sum(np.isnan(data_float_read)) > 0):
            data_str = self.vna.query_str('CALC:DATA:DALL? FDATA')
            if data_str == 'Simulating':
                data_s11_1, data_s11_2 = self._load_s2p_data('S11', return_format)
                data_s12_1, data_s12_2 = self._load_s2p_data('S12', return_format)
                data_s21_1, data_s21_2 = self._load_s2p_data('S21', return_format)
                data_s22_1, data_s22_2 = self._load_s2p_data('S22', return_format)
            elif data_str:
                data_float_read = [float(d) for d in data_str.split(',')]
                if len(data_float_read) != (8 * self.frequency_sweep[2]):
                    continue

                data_float = np.array(data_float_read).reshape((-1, self.frequency_sweep[2]))

                data_s11_1 = data_float[0, :]
                data_s11_2 = data_float[1, :]

                data_s12_1 = data_float[2, :]
                data_s12_2 = data_float[3, :]

                data_s21_1 = data_float[4, :]
                data_s21_2 = data_float[5, :]

                data_s22_1 = data_float[6, :]
                data_s22_2 = data_float[7, :]

        # re-enable continuous sweep
        self.vna.write_str('INIT1:CONT ON')

        # Display sweep (visible only after the end of remote control
        self.vna.write_str('DISPLAY:WINDOW1:STATE ON')
        self.vna.write_str('DISP:WIND1:TRAC1:FEED "Trc1"')
        self.vna.write_str('DISP:WIND1:TRAC2:FEED "Trc2"')
        self.vna.write_str('DISP:WIND1:TRAC3:FEED "Trc3"')
        self.vna.write_str('DISP:WIND1:TRAC4:FEED "Trc4"')
        self.vna.write_str('DISP:WIND1:TRAC5:FEED "Trc5"')
        self.vna.write_str('DISP:WIND1:TRAC6:FEED "Trc6"')
        self.vna.write_str('DISP:WIND1:TRAC7:FEED "Trc7"')
        self.vna.write_str('DISP:WIND1:TRAC8:FEED "Trc8"')

        if return_format.upper() == 'RI':
            return (
                data_s11_1 + 1j * data_s11_2,
                data_s12_1 + 1j * data_s12_2,
                data_s21_1 + 1j * data_s21_2,
                data_s22_1 + 1j * data_s22_2
            )

        elif return_format.upper() == 'DB':
            return {
                's11': {'mag': data_s11_1, 'phase': data_s11_2},
                's12': {'mag': data_s12_1, 'phase': data_s12_2},
                's21': {'mag': data_s21_1, 'phase': data_s21_2},
                's22': {'mag': data_s22_1, 'phase': data_s22_2},
            }
        else:
            return None

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
        if return_format.upper() == 'RI':
            _cmp_ctrl = 0
            _trace1_format = 'REAL'
            _trace2_format = 'IMAG'
        elif return_format.upper() == 'DB':
            _cmp_ctrl = -999
            _trace1_format = 'MLOG'
            _trace2_format = 'PHAS'
        else:
            raise RuntimeError('Invalid format: %s' % return_format)

        # erase previous data
        self.vna.write_str('CALCulate:PARameter:DELete:ALL')

        # enable SINGLE SWEEP
        self.vna.write_str('INIT1:CONT OFF')

        # create trace for the S-Parameter
        self.vna.write_str(f'CALC1:PAR:SDEF "Trc1","{s_param}"')
        self.vna.write_str(f'CALC1:PAR:MEAS "Trc1","{s_param}"')
        self.vna.write_str('CALC1:PAR:SEL "Trc1"')
        self.vna.write_str(f'CALC1:FORM {_trace1_format}')

        self.vna.write_str(f'CALC1:PAR:SDEF "Trc2","{s_param}"')
        self.vna.write_str(f'CALC1:PAR:MEAS "Trc2","{s_param}"')
        self.vna.write_str('CALC1:PAR:SEL "Trc2"')
        self.vna.write_str(f'CALC1:FORM {_trace2_format}')

        # Launch the sweep
        self.vna.write_str('INIT1')

        # Display sweep (visible only after the end of remote control
        self.vna.write_str('DISPLAY:WINDOW1:STATE ON')
        self.vna.write_str('DISP:WIND1:TRAC1:FEED "Trc1"')
        self.vna.write_str('DISP:WIND1:TRAC2:FEED "Trc2"')

        _cmp_ctrl = (0 if return_format.upper() == 'RI' else -999)
        data_1 = np.ones((self.frequency_sweep[2],)) * _cmp_ctrl
        data_2 = np.zeros((self.frequency_sweep[2],))
        while np.min(data_1) == _cmp_ctrl:
            data_str = self.vna.query_str('CALC:DATA:DALL? FDATA')
            if data_str == 'Simulating':
                data_1, data_2 = self._load_s2p_data(s_param, return_format)
            elif data_str:
                data_float = [float(d) for d in data_str.split(',')]
                data_1 = data_float[0:self.frequency_sweep[2]]
                data_2 = data_float[self.frequency_sweep[2]:]

        # re-enable continuous sweep
        self.vna.write_str('INIT1:CONT ON')

        if return_format.upper() == 'RI':
            return np.array(data_1) + 1j * np.array(data_2)
        elif return_format.upper() == 'DB':
            return {'mag': data_1, 'phase': data_2}
        else:
            return None

    def reset(self):
        # create trace for the S-Parameters
        self.vna.write_str('CALCulate:PARameter:DELete:ALL')
        self.vna.write_str(f'CALC1:PAR:SDEF "Trc1","S11"')
        self.vna.write_str(f'CALC1:FORM MLOG')

        self.vna.write_str(f'CALC1:PAR:SDEF "Trc2","S22"')
        self.vna.write_str(f'CALC1:FORM MLOG')

        self.vna.write_str('DISPLAY:WINDOW1:STATE ON')
        self.vna.write_str('DISP:WIND1:TRAC1:FEED "Trc1"')
        self.vna.write_str('DISP:WIND1:TRAC2:FEED "Trc2"')

        self.vna.write_str(f'CALC1:PAR:SDEF "Trc3","S11"')
        self.vna.write_str(f'CALC1:FORM PHAS')

        self.vna.write_str(f'CALC1:PAR:SDEF "Trc4","S22"')
        self.vna.write_str(f'CALC1:FORM PHAS')

        self.vna.write_str('DISPLAY:WINDOW2:STATE ON')
        self.vna.write_str('DISP:WIND2:TRAC1:FEED "Trc3"')
        self.vna.write_str('DISP:WIND2:TRAC2:FEED "Trc4"')

        self.vna.write_str(f'CALC1:PAR:SDEF "Trc5","S12"')
        self.vna.write_str(f'CALC1:FORM MLOG')

        self.vna.write_str(f'CALC1:PAR:SDEF "Trc6","S21"')
        self.vna.write_str(f'CALC1:FORM MLOG')

        self.vna.write_str('DISPLAY:WINDOW3:STATE ON')
        self.vna.write_str('DISP:WIND3:TRAC1:FEED "Trc5"')
        self.vna.write_str('DISP:WIND3:TRAC2:FEED "Trc6"')

        self.vna.write_str(f'CALC1:PAR:SDEF "Trc7","S12"')
        self.vna.write_str(f'CALC1:FORM PHAS')

        self.vna.write_str(f'CALC1:PAR:SDEF "Trc8","S21"')
        self.vna.write_str(f'CALC1:FORM PHAS')

        self.vna.write_str('DISPLAY:WINDOW4:STATE ON')
        self.vna.write_str('DISP:WIND4:TRAC1:FEED "Trc7"')
        self.vna.write_str('DISP:WIND4:TRAC2:FEED "Trc8"')

    def enable_trl_calibration(self, cal_kit: str):
        try:
            self.reset()
            # Select GOLA connector and the requested calibration kit
            self.vna.write_str(":SENSe1:CORRection:COLLect:METHod TRL")
            self.vna.write_str(f"SENSe1:CORRection:CKIT:SELect 'GOLA', '{cal_kit}'")

            return True
        except Exception as e:
            print(f"❌ Error during TRL cal: {e}")
            return False

    def save_trl_calibration(self):
        try:
            self.vna.write_str(":SENSe1:CORRection:COLLect:SAVE:SELected")

            # Turn on calibration
            self.turn_on_calibration()
            return True, None
        except Exception as e:
            print(f"❌ Error during saving TRL cal: {e}")
            return False, e

    def perform_thru_measurement(self):
        try:
            # Select GOLA connector and the requested calibration kit
            self.vna.write_str(":SENSe1:CORRection:COLLect:ACQuire:SELected THRough, 1, 2")
            return True, None
        except Exception as e:
            print(f"❌ Error during TRL THRU: {e}")
            return False, e

    def perform_line_measurement(self):
        try:
            # Select GOLA connector and the requested calibration kit
            self.vna.write_str(":SENSe1:CORRection:COLLect:ACQuire:SELected LINE, 1, 2")
            return True, None
        except Exception as e:
            print(f"❌ Error during TRL LINE: {e}")
            return False, e

    def perform_reflect_measurement(self):
        try:
            # Select GOLA connector and the requested calibration kit
            self.vna.write_str(":SENSe1:CORRection:COLLect:ACQuire:SELected REFL, 1")
            self.vna.write_str(":SENSe1:CORRection:COLLect:ACQuire:SELected REFL, 2")
            return True, None
        except Exception as e:
            print(f"❌ Error during TRL REFLECT: {e}")
            return False, e

    def turn_off_calibration(self) :
        """
        Turns off the current calibration.
        """
        self.vna.write_str(':SENSe1:CORRection:STAT OFF')
        self.calibration_active = False

    def turn_on_calibration(self) -> bool:
        """
        Turns on calibration (if one is loaded).
        """
        self.vna.write_str(':SENSe1:CORRection:STAT ON')
        cal_state = self.vna.query_str(':SENSe1:CORRection:STAT?')
        self.calibration_active = (cal_state.strip() == '1')

        return self.calibration_active


if __name__ == '__main__':
    """
    Example usage of the VNA class.
    """

    with RohdeSchwarzVNA(ip_address='192.168.0.4') as vna:
        print(vna.vna.query('*IDN?'))
        vna.set_sweep(75., 110., 1001, '1kHz')
        """vna.enable_trl_calibration(cal_kit='CarmatW')
        vna.perform_reflect_measurement()
        vna.perform_line_measurement()
        vna.perform_thru_measurement()"""

        res = vna.sweep(return_format='DB')
        _, ax = plt.subplots(2, 1)

        ax[0].plot(vna.frequencies_GHz, res['s11']['mag'])
        ax[0].plot(vna.frequencies_GHz, res['s22']['mag'])
        ax[1].plot(vna.frequencies_GHz, res['s12']['mag'])
        ax[1].plot(vna.frequencies_GHz, res['s21']['mag'])
        plt.show()