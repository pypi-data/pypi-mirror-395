from time import sleep

import matplotlib.pyplot as plt
import pyvisa
import numpy as np
from pycarmat.ressources.VNA.base import _VNA_

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


class KeysightVNA(_VNA_):
    """
    A class to interface with a Vector Network Analyzer (VNA).

    This class provides methods for configuring, controlling, and retrieving S-parameter
    measurements from a VNA using the PyVISA API. It supports real instrument
    communication but not yet a simulation mode.
    @todo: Simulation Mode
    """

    def __enter__(self):
        """
        Establishes a connection to the VNA when entering a context.

        Returns:
            KeysightVNA: The VNA instance with an active connection.

        Raises:
            ConnectionError: If the instrument cannot be accessed.
        """
        try:
            rm = pyvisa.ResourceManager()
            self.vna = rm.open_resource(self.ip)
            self.vna.timeout = 50000

        except pyvisa.VisaIOError as e:
            raise ConnectionError(str(e))
        return self

    def _reset(self):
        self.vna.write("*CLS")


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
            _trace1_format = 'REAL'
            _trace2_format = 'IMAG'
        elif return_format.upper() == 'DB':
            _trace1_format = 'MLOG'
            _trace2_format = 'PHAS'
        else:
            raise RuntimeError('Invalid format: %s' % return_format)

        # erase previous data
        self.vna.write('CALC:PAR:DEL:ALL')

        # create trace for the S-PARAMETERS
        _s_params = ('S11', 'S12', 'S21', 'S22')
        id_trace = 1

        self.vna.write('DISPLAY:WINDOW1:STATE ON')
        for s_param in _s_params:
            self.vna.write(f'CALC:PAR:DEF TRC{id_trace},{s_param}')
            self.vna.write(f'CALC:PAR:SEL TRC{id_trace}')
            self.vna.write(f'CALC:FORM {_trace1_format}')
            self.vna.write(f'DISP:WIND1:TRAC{id_trace}:FEED Trc{id_trace}')
            id_trace += 1

            self.vna.write(f'CALC:PAR:DEF TRC{id_trace},{s_param}')
            self.vna.write(f'CALC:PAR:SEL TRC{id_trace}')
            self.vna.write(f'CALC:FORM {_trace2_format}')
            self.vna.write(f'DISP:WIND1:TRAC{id_trace}:FEED Trc{id_trace}')
            id_trace += 1

        # Launch the sweep
        # enable SINGLE SWEEP
        self.vna.write('INIT1:CONT OFF')
        self.vna.write('INIT1:IMM')
        self.vna.query("*OPC?")

        num_pts = int(self.frequency_sweep[2])
        data_float = np.zeros((8, num_pts))
        trc_id = 1
        for s_param in _s_params:
            self.vna.write(f'CALC:PAR:SEL TRC{trc_id}')
            data_1_str = self.vna.query('CALC:DATA? FDATA')
            if num_pts == 0:
                num_pts = len(data_1_str.split(','))
                data_float = np.zeros((8, num_pts))
            data_float[trc_id-1, :] = np.array([float(x) for x in data_1_str.split(',')])

            trc_id += 1
            self.vna.write(f'CALC:PAR:SEL TRC{trc_id}')
            data_2_str = self.vna.query('CALC:DATA? FDATA')
            data_float[trc_id-1, :] = np.array([float(x) for x in data_2_str.split(',')])


            if data_float[trc_id-1, 0] == 45:
                print(f'NOPE for PHASE {s_param}')
            trc_id += 1


        data_s11_1 = data_float[0, :]
        data_s11_2 = data_float[1, :]

        data_s12_1 = data_float[2, :]
        data_s12_2 = data_float[3, :]

        data_s21_1 = data_float[4, :]
        data_s21_2 = data_float[5, :]

        data_s22_1 = data_float[6, :]
        data_s22_2 = data_float[7, :]

        # re-enable continuous sweep
        self.vna.write('INIT1:CONT ON')

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
            _trace1_format = 'REAL'
            _trace2_format = 'IMAG'
        elif return_format.upper() == 'DB':
            _trace1_format = 'MLOG'
            _trace2_format = 'PHAS'
        else:
            raise RuntimeError('Invalid format: %s' % return_format)

        # erase previous data
        self.vna.write('CALC:PAR:DEL:ALL')

        # enable SINGLE SWEEP
        self.vna.write('INIT1:CONT OFF')

        # create trace for the S-Parameter
        self.vna.write(f'CALC:PAR:DEF TRC1,{s_param}')
        self.vna.write('CALC:PAR:SEL TRC1')
        self.vna.write(f'CALC:FORM {_trace1_format}')

        self.vna.write(f'CALC:PAR:DEF TRC2,{s_param}')
        self.vna.write('CALC:PAR:SEL TRC2')
        self.vna.write(f'CALC:FORM {_trace2_format}')

        # Display sweep (visible only after the end of remote control
        self.vna.write('DISP:WIND1:STATE ON')
        self.vna.write('DISP:WIND1:TRAC1:FEED TRC1')
        self.vna.write('DISP:WIND1:TRAC2:FEED TRC2')

        # Launch the sweep
        self.vna.write('INIT1:IMM')
        self.vna.query("*OPC?")

        self.vna.write('CALC:PAR:SEL TRC1')
        data_1_str = self.vna.query('CALC:DATA? FDATA')
        data_1 = np.array([float(x) for x in data_1_str.split(',')])
        self.vna.write('CALC:PAR:SEL TRC2')
        data_2_str = self.vna.query('CALC:DATA? FDATA')
        data_2 = np.array([float(x) for x in data_2_str.split(',')])

        # re-enable continuous sweep
        self.vna.write('INIT1:CONT ON')

        if return_format.upper() == 'RI':
            return np.array(data_1) + 1j * np.array(data_2)
        elif return_format.upper() == 'DB':
            return {'mag': data_1, 'phase': data_2}
        else:
            return None

    def reset(self):
        # create trace for the S-Parameters
        # Supprimer toutes les traces existantes
        self.vna.write("*CLS")
        self.vna.write('CALC:PAR:DEL:ALL')

        self.vna.write('CALC:PAR:DEF TRC1,S11')
        self.vna.write('CALC:FORM MLOG')
        self.vna.write('CALC:PAR:DEF TRC2,S22')
        self.vna.write('CALC:PAR:SEL TRC2')
        self.vna.write('CALC:FORM MLOG')
        self.vna.write('DISP:WIND1:STATE ON')
        self.vna.write('DISP:WIND1:TRAC1:FEED TRC1')
        self.vna.write('DISP:WIND1:TRAC2:FEED TRC2')

        self.vna.write('CALC:PAR:DEF TRC3,S11')
        self.vna.write('CALC:PAR:SEL TRC3')
        self.vna.write('CALC:FORM PHAS')
        self.vna.write('CALC:PAR:DEF TRC4,S22')
        self.vna.write('CALC:PAR:SEL TRC4')
        self.vna.write('CALC:FORM PHAS')
        self.vna.write('DISP:WIND2:STATE ON')
        self.vna.write('DISP:WIND2:TRAC1:FEED TRC3')
        self.vna.write('DISP:WIND2:TRAC2:FEED TRC4')

        self.vna.write('CALC:PAR:DEF TRC5,S12')
        self.vna.write('CALC:PAR:SEL TRC5')
        self.vna.write('CALC:FORM MLOG')
        self.vna.write('CALC:PAR:DEF TRC6,S21')
        self.vna.write('CALC:PAR:SEL TRC6')
        self.vna.write('CALC:FORM MLOG')
        self.vna.write('DISP:WIND3:STATE ON')
        self.vna.write('DISP:WIND3:TRAC1:FEED TRC5')
        self.vna.write('DISP:WIND3:TRAC2:FEED TRC6')

        self.vna.write('CALC:PAR:DEF TRC7,S12')
        self.vna.write('CALC:PAR:SEL TRC7')
        self.vna.write('CALC:FORM PHAS')
        self.vna.write('CALC:PAR:DEF TRC8,S12')
        self.vna.write('CALC:PAR:SEL TRC8')
        self.vna.write('CALC:FORM PHAS')
        self.vna.write('DISP:WIND4:STATE ON')
        self.vna.write('DISP:WIND4:TRAC1:FEED TRC7')
        self.vna.write('DISP:WIND4:TRAC2:FEED TRC8')

    def wait_for_completion(self):
        """Wait until the VNA finishes its current operation."""
        import time
        while True:
            # OPC? retourne 1 quand toutes les opérations précédentes sont terminées
            done = int(self.vna.query("*OPC?"))
            print(done)
            if done:
                break
            time.sleep(0.1)

    def enable_trl_calibration(self, cal_kit: str):
        try:
            self.vna.write("*CLS")
            self.vna.write('CALC:PAR:DEL:ALL')
            import time

            # select calset
            self.vna.write(f'sense1:correction:collect:ckit:port:select "{cal_kit}"')
            print(self.vna.query('sense1:correction:collect:ckit:port1:select?'))

            self.vna.write('CALC:PAR:DEF TRC1,S11')
            self.vna.write('CALC:PAR:SEL TRC1')

            self.vna.write('sense1:correction:collect:method spartrl')

            return True
        except Exception as e:
            print(f"❌ Error during TRL cal: {e}")
            return False

    def save_trl_calibration(self):
        try:
            self.vna.write('CALC:PAR:SEL TRC1')
            self.vna.write('sense1:correction:collect:save')
            self.vna.query('*OPC?')

            # Turn on calibration
            self.turn_on_calibration()
            self.reset()
            return True, None
        except Exception as e:
            print(f"❌ Error during saving TRL cal: {e}")
            return False, e

    def perform_thru_measurement(self):
        try:
            # Select GOLA connector and the requested calibration kit
            self.vna.write('CALC:PAR:SEL TRC1')
            self.vna.write('sense1:correction:collect STAN4')
            self.vna.query('*OPC?')
            return True, None
        except Exception as e:
            print(f"❌ Error during TRL THRU: {e}")
            return False, e

    def perform_line_measurement(self):
        try:
            # Select GOLA connector and the requested calibration kit
            self.vna.write('CALC:PAR:SEL TRC1')
            self.vna.write('sense1:correction:collect STAN3')
            self.vna.query('*OPC?')
            return True, None
        except Exception as e:
            print(f"❌ Error during TRL LINE: {e}")
            return False, e

    def perform_reflect_measurement(self):
        try:
            # Select GOLA connector and the requested calibration kit
            self.vna.write('CALC:PAR:SEL TRC1')
            self.vna.write('sense1:correction:collect STAN1')
            self.vna.query('*OPC?')
            self.vna.write('sense1:correction:collect STAN2')
            self.vna.query('*OPC?')
            return True, None
        except Exception as e:
            print(f"❌ Error during TRL REFLECT: {e}")
            return False, e

    def turn_off_calibration(self) :
        """
        Turns off the current calibration.
        """
        self.vna.write('SENS1:CORR:STAT OFF')
        self.calibration_active = False

    def turn_on_calibration(self) -> bool:
        """
        Turns on calibration (if one is loaded).
        """
        self.vna.write('SENS1:CORR:STAT ON')
        cal_state = self.vna.query('SENS1:CORR:STAT?')
        self.calibration_active = (cal_state.strip() == '1')

        return self.calibration_active

if __name__ == '__main__':
    """
    Example usage of the VNA class.
    """

    from pycarmat.ressources.ESP import ESP30xController, UNIT

    with KeysightVNA(ip_address='192.168.0.5', reset_instr=True) as vna, \
                ESP30xController(serial_port='ASRL/dev/ttyUSB0') as esp:
        #esp.homing(axis=2)
        esp.homing(axis=1)

        print(vna.vna.query('*IDN?'))

        vna.set_sweep(75., 110., 1001, '1kHz')

        vna.enable_trl_calibration(cal_kit='CarmatW')

        input('Place reflector')
        esp.move_relative(axis=1, value=-2, motion_unit=UNIT.TRANSLATION_MM)
        vna.perform_reflect_measurement()
        input('Remove reflector')

        esp.move_absolute(axis=1, value=-1, motion_unit=UNIT.TRANSLATION_MM)
        vna.perform_line_measurement()

        esp.move_absolute(axis=1, value=0, motion_unit=UNIT.TRANSLATION_MM)
        vna.perform_thru_measurement()

        vna.save_trl_calibration()

        input('Place sample')
        res = vna.sweep(return_format='DB')
        _, ax = plt.subplots(2, 1)

        ax[0].plot(vna.frequencies_GHz, res['s11']['mag'])
        ax[0].plot(vna.frequencies_GHz, res['s22']['mag'])
        ax[1].plot(vna.frequencies_GHz, res['s12']['mag'])
        ax[1].plot(vna.frequencies_GHz, res['s21']['mag'])
        plt.show()
