import time
import logging
from serial import SerialException
from enum import Enum
import pyvisa


class UNIT(Enum):
    """
    Enumeration for different motion units supported by the ESP300 controller.
    """
    ENCODER_COUNT = '00'
    MOTOR_STEP = '01'
    TRANSLATION_MM = '02'
    TRANSLATION_UM = '03'
    ROTATION_DEG = '07'
    ROTATION_RAD = '09'
    ROTATION_MRAD = '10'
    ROTATION_URAD = '11'


class ESP30xController:
    """
    A controller class for interfacing with the Newport ESP300 motion controller via serial communication.

    This class provides methods to control motorized stages, move axes to absolute or relative positions,
    and perform homing operations.
    """

    @staticmethod
    def detect(get_info: bool = False):
        rm = pyvisa.ResourceManager()
        if get_info:
            return rm.list_resources_info('ASRL?*::INSTR')
        else:
            return rm.list_resources('ASRL?*::INSTR')

    def __init__(self, serial_port: str = 'ASRL1', raise_error: bool = True):
        """
        Initializes the ESP300Controller instance. The serial port can be retrieve by using ESP300Controller.detect().

        Args:
            serial_port (str): The serial port to connect to the ESP300 device (default is 'COM1').
            raise_error (bool): If True, exceptions are raised for connection errors; otherwise, errors are logged.
        """
        self.esp301 = None
        self._serial_port = serial_port
        self._baud_rate = 19200  # The ESP300 operates at a fixed baud rate of 19200.
        self._raise_error = raise_error

    def __enter__(self):
        """
        Establishes a serial connection to the ESP300 when entering a context.

        Returns:
            ESP300Controller: The current instance, allowing the use of 'with ESP300Controller() as esp:'.

        Raises:
            SerialException: If the serial connection cannot be established (unless raise_error is False).
        """
        try:
            rm = pyvisa.ResourceManager()
            self.esp301 = rm.open_resource('%s::INSTR' % self._serial_port,
                                           resource_pyclass=pyvisa.resources.SerialInstrument,
                                           baud_rate=self._baud_rate, read_termination='\n')
            self.esp301.read_termination = '\r'
            self.esp301.baud_rate = self._baud_rate
        except SerialException as e:
            logging.error(f"Failed to connect to ESP300: {e}")
            if self._raise_error:
                raise
        return self

    def __exit__(self, *exc):
        """
        Closes the serial connection when exiting the context manager.
        """
        if self.esp301 is not None:
            self.esp301.close()

    def connected(self):
        return self.esp301 is not None

    def clear_errors(self):
        err = 1
        if self.esp301 is None:
            return
        while err != 0:
            err = int(self.esp301.query("TE?"))

    def get_motion_status(self):
        try:
            status = int(self.query("1MD?"))
        except:
            status = 0

        if status == 0:
            return 1  # moving
        return 0

    def _wait_completion(self, axis: int):
        """
        Waits for the completion of the current motion command before executing further commands.

        Sends a '1WS' command to request completion status and repeatedly checks until motion is finished.
        """
        self.send_command(f'{axis}WS')  # Request wait-for-completion mode
        while self.get_motion_status():
            time.sleep(0.5)

    # alias of send_command
    def write(self, command: str) -> None:
        self.send_command(command)

    def send_command(self, command: str) -> None:
        """
        Sends a command to the ESP300 controller and retrieves the response.

        Args:
            command (str): The command string to send.

        Returns:
            str: The response received from the ESP300 device.
        """
        if self.esp301 is None:
            return
        self.esp301.write(command)

    def query(self, command: str) -> str:
        if self.esp301 is None:
            return "Fail"
        return self.esp301.query(command)

    def homing(self, axis: int):
        """
        Performs a homing operation on the specified axis.

        Args:
            axis (int): The axis number to home.

        This method enables the motor, initiates the homing procedure, waits for its completion,
        and then disables the motor.
        """
        self.send_command(f'{axis}MO')  # Enable motor
        self.send_command(f'{axis}OR')  # Start homing sequence
        self._wait_completion(axis)
        self.send_command(f'{axis}MF')  # Disable motor

    def move_absolute(self, axis: int, value: float, motion_unit: UNIT):
        """
        Moves the specified axis to an absolute position.

        Args:
            axis (int): The axis number to move.
            value (float): The target position.
            motion_unit (UNIT): The unit of motion (e.g., rotation degrees or translation millimeters).

        This method enables the motor, sets the motion unit, moves the axis to the target position,
        waits for completion, and then disables the motor.
        """
        self.send_command(f'{axis}MO')  # Enable motor
        self.send_command(f'{axis}SN{motion_unit.value}')  # Set motion unit
        self.send_command(f'{axis}PA {value}')  # Move to absolute position
        self._wait_completion(axis)
        self.send_command(f'{axis}MF')  # Disable motor

    def move_relative(self, axis: int, value: float, motion_unit: UNIT):
        """
        Moves the specified axis by a relative amount from its current position.

        Args:
            axis (int): The axis number to move.
            value (float): The relative movement amount.
            motion_unit (UNIT): The unit of motion (e.g., rotation degrees or translation millimeters).

        This method enables the motor, sets the motion unit, moves the axis by the specified amount,
        waits for completion, and then disables the motor.
        """
        self.send_command(f'{axis}MO')  # Enable motor
        self.send_command(f'{axis}SN{motion_unit.value}')  # Set motion unit
        self.send_command(f'{axis}PR {value}')  # Move relative to current position
        self._wait_completion(axis)
        self.send_command(f'{axis}MF')  # Disable motor


if __name__ == '__main__':
    """
    Example usage of the ESP300Controller class.
    """
    print(ESP300Controller.detect())

    with ESP300Controller(raise_error=False) as esp:
        esp.clear_errors()

        # homing
        esp.homing(axis=1)

        # Set platform rotation to +10 deg
        esp.move_absolute(axis=1, value=10.0, motion_unit=UNIT.ROTATION_DEG)

        # Rotate platform of -2 deg from current position
        esp.move_relative(axis=1, value=10.0, motion_unit=UNIT.ROTATION_DEG)
