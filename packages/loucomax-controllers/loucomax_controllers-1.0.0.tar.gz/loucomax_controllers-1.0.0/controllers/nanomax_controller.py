"""This module integrates classes for control of NANOMAX300 device
through the BSC203 controller (Thorlabs Devices)"""

__all__ = ["ZaberController"]

# Standard imports
import os
import configparser
import time
from typing import Literal
import logging
import clr

# DLL handling
clr.AddReference(os.path.join(os.path.dirname(__file__), "bin", "Thorlabs.MotionControl.DeviceManagerCLI.dll"))
clr.AddReference(os.path.join(os.path.dirname(__file__), "bin", "Thorlabs.MotionControl.GenericMotorCLI.dll"))
clr.AddReference(os.path.join(os.path.dirname(__file__), "bin", "ThorLabs.MotionControl.Benchtop.StepperMotorCLI.dll"))

# Imports from Thorlabs DLLs
from Thorlabs.MotionControl.DeviceManagerCLI import *
from Thorlabs.MotionControl.GenericMotorCLI import *
from Thorlabs.MotionControl.Benchtop.StepperMotorCLI import *
from System import Decimal  # necessary for real world units

# Sub-modules imports
from .abstractcontroller import AbsController

# logger configuration
logger = logging.getLogger(f'core.{__name__}')

class NanoMaxController(AbsController):
    """
    This class provides an interface for controlling Thorlabs NanoMax300 stages
    connected to a BSC203 benchtop controller. It manages the connection,
    configuration, and movement of the X, Y, and Z axes, allowing for absolute
    and relative positioning, homing, and stopping of individual or all axes.

    Attributes:
        - _NANOMAX300_CHAN_ALLOC_MAP (dict): Maps controller channels to stage axes.
        - _NANOMAX300_ORIENTATION (dict): Stores orientation (+/-) for each axis.
        - controllers_config (configparser.ConfigParser): User-defined configuration.
        - axis_control (dict): Holds references to axis control objects for x, y, z.
        - connexion_established (bool): Connection status with the controller.

    Methods:
        - __init__(controllers_config):
            Initializes the controller with user configuration and prepares axis control.
        - start_connection():
            Establishes connection to the NanoMax300 stages via the BSC203 controller,
            initializes axis allocation, and enables device polling.
        - stop_connection():
            Disconnects from the controller and updates connection status.
        - is_connected() -> bool:
            Returns the current connection status.
        - move_to(direction, target_mm, move_timeout=60000):
            Moves the specified axis to an absolute position in millimeters.
        - move_relative_forward(direction, step_mm, move_timeout=60000):
            Moves the specified axis forward by a relative step in millimeters.
        - move_relative_backward(direction, step_mm, move_timeout=60000):
            Moves the specified axis backward by a relative step in millimeters.
        - home_axis(direction, home_timeout=60000):
            Homes the specified axis.
        - stop_movement(direction):
            Stops movement of the specified axis.
        - is_all_axes_homed() -> bool:
            Checks if all axes are homed.
        - home_all_axes(timeout=60000):
            Homes all axes sequentially.
        - get_xyz_pos() -> tuple[float, float, float]:
            Returns the current positions of all axes as a tuple.
        - get_dir_pos(direction) -> int:
            Returns the stored position of the specified axis.
            (Internal methods for configuration and axis allocation are also provided.)"""

    _NANOMAX300_CHAN_ALLOC_MAP =  {
        "1" : "y",
        "2" : "x",
        "3" : "z"
    }
    _NANOMAX300_ORIENTATION = {
        "x" : 0,
        "y" : 0,
        "z" : 0
    }

    def __init__(self, controllers_config:configparser.ConfigParser):

        # Configuration defined by the User in .cfg file
        self.controllers_config = controllers_config
        NanoMaxController._update_config(controllers_config)

        # Axis control (zaber axis)
        self.axis_control = {
            "x" : None,
            "y" : None,
            "z" : None
        }
        self.connexion_established = False

    def start_connection(self) -> None:
        """
        Start connection with NanoMax300 stages via the BSC203 benchtop controller
        """

        NanoMaxController._update_config(self.controllers_config)

        # Detect Thorlabs devices
        DeviceManagerCLI.BuildDeviceList()

        # Create new device
        # Connect, begin polling, and enable
        self.serial_no = "70470634"  # BSC203 benchtop controller serial number
        try :
            # Create the benchtop stepper motor controller
            self.bench_controller_device = BenchtopStepperMotor.CreateBenchtopStepperMotor(self.serial_no)
            self.bench_controller_device.Connect(self.serial_no)
        except Exception as e :
            logger.exception('Error while connecting to the NanoMax300 device : %s', e)
            raise ConnectionError("Error while connecting to the NanoMax300 device") from e
        time.sleep(0.25)  # wait statements are important to allow settings to be sent to the device

        self._init_axis_allocation()

        self.connexion_established = self.bench_controller_device.IsConnected

    def stop_connection(self):
        self.bench_controller_device.Disconnect(False)
        self.connexion_established = self.bench_controller_device.IsConnected

    def is_connected(self) -> bool:
        if hasattr(self, "bench_controller_device") :
            self.connexion_established = self.bench_controller_device.IsConnected
        return super().is_connected()

    @classmethod
    def _update_config(cls, config:configparser.ConfigParser) -> None:
        """Reading and interpreting the config file .cfg"""
        cls._update_alloc_map(config)
        cls._update_orientation(config)

    @classmethod
    def _update_alloc_map(cls, config:configparser.ConfigParser):
        """Reading and interpreting the config file .cfg
        
            Parameters related to :

                -   Allocation of each channel to axes X, Y and Z
        """
        try :
            cls._NANOMAX300_CHAN_ALLOC_MAP["1"] = config.get('NanoMax300', 'CHANNEL_1')
            cls._NANOMAX300_CHAN_ALLOC_MAP["2"]  = config.get('NanoMax300', 'CHANNEL_2')
            cls._NANOMAX300_CHAN_ALLOC_MAP["3"]  = config.get('NanoMax300', 'CHANNEL_3')
        except Exception as e :
            logger.exception('Error while reading Controllers.cfg file : %s', e)
            raise ValueError("Error while reading Controllers.cfg file") from e

    @classmethod
    def _update_orientation(cls, config:configparser.ConfigParser):
        """Reading and interpreting the config file .cfg
        
            Parameters related to :

                -   Orientation (+/-) of each axis 
        """
        try :
            cls._NANOMAX300_ORIENTATION["x"] = int(config.getint('NanoMax300',
                                                    'NANOMAX300_ORIENTATION_X'))
            cls._NANOMAX300_ORIENTATION["y"] = int(config.getint('NanoMax300',
                                                    'NANOMAX300_ORIENTATION_Y'))
            cls._NANOMAX300_ORIENTATION["z"] = int(config.getint('NanoMax300',
                                                    'NANOMAX300_ORIENTATION_Z'))

        except Exception as e :
            logger.exception('Error while reading Controllers.cfg file : %s', e)
            raise ValueError("Error while reading Controllers.cfg file") from e

    def _init_axis_allocation(self) -> None :
        # print(f'{self._NANOMAX300_CHAN_ALLOC_MAP=}')
        for index, val in self._NANOMAX300_CHAN_ALLOC_MAP.items():
            self.axis_control[val] = self.bench_controller_device.GetChannel(int(index))

        for stage_axis in self.axis_control.values():
            # Ensure that the device settings have been initialized
            if not stage_axis.IsSettingsInitialized():
                stage_axis.WaitForSettingsInitialized(10000)  # 10 second timeout
                assert stage_axis.IsSettingsInitialized() is True

            # Start polling and enable
            stage_axis.StartPolling(250)  # 250ms polling rate
            time.sleep(0.5)
            stage_axis.EnableDevice()
            time.sleep(0.25)  # Wait for device to enable

            # Load any configuration settings needed by the controller/stage
            channel_config = stage_axis.LoadMotorConfiguration(stage_axis.DeviceID)
            chan_settings = stage_axis.MotorDeviceSettings

            stage_axis.GetSettings(chan_settings)

            channel_config.DeviceSettingsName = 'NanoMax300'

            channel_config.UpdateCurrentConfiguration()

            stage_axis.SetSettings(chan_settings, True, False)

    def move_to(self, direction:Literal["x", "y", "z"], target_mm:float, move_timeout=60000):
        axis_control = self.axis_control[direction]
        axis_control.MoveTo(Decimal(target_mm), move_timeout)

    def move_relative_forward(self, direction:Literal["x", "y", "z"], step_mm:float, move_timeout=60000):
        axis_control = self.axis_control[direction]
        axis_control.MoveRelative(MotorDirection.Forward, Decimal(step_mm), move_timeout)

    def move_relative_backward(self, direction:Literal["x", "y", "z"], step_mm:float, move_timeout=60000):
        axis_control = self.axis_control[direction]
        axis_control.MoveRelative(MotorDirection.Backward, Decimal(step_mm), move_timeout)

    def home_axis(self, direction:Literal["x", "y", "z"], home_timeout=60000):
        self.axis_control[direction].Home(home_timeout)

    def stop_movement(self, direction:Literal["x", "y", "z"]) -> None:
        """Stop the movement of a given axis"""

        logger.debug(f'Stop {direction} movement')
        match direction:
            case "x":
                self._stop_x()
            case "y":
                self._stop_y()
            case "z":
                self._stop_z()
            case _:
                raise KeyError(f"Wrong direction provided to stop_movement() method, therefore emergency_stop() wass called.\tdirection entered : {direction}")

    def is_all_axes_homed(self):
        """Check if all axes are homed
        Returns False if any axis is not homed"""
        for idx in range(1, 4):
            channel = self.bench_controller_device.GetChannel(idx)
            if channel.NeedsHoming :
                return False

        return True

    def home_all_axes(self, timeout=60000):
        self.home_axis("x", timeout)
        self.home_axis("y", timeout)
        self.home_axis("z", timeout)

    def _stop_x(self, timeout=60000) -> None:
        """Stop X axis movement"""
        try :
            self.axis_control["x"].Stop(timeout)
        except AttributeError as attrerr:
            raise ConnectionError("The NanoMax300 stage is not connected. Impossible to send STOP X command") from attrerr

    def _stop_y(self, timeout=60000) -> None:
        """Stop Y axis movement"""
        try:
            self.axis_control["y"].Stop(timeout)
        except AttributeError as attrerr:
            raise ConnectionError("The NanoMax300 stage is not connected. Impossible to send STOP Y command") from attrerr

    def _stop_z(self, timeout=60000) -> None:
        """Stop Z axis movement"""
        try:
            self.axis_control["z"].Stop(timeout)
        except AttributeError as attrerr:
            raise ConnectionError("The NanoMax300 stage is not connected. Impossible to send STOP Z command") from attrerr

    def get_xyz_pos(self) -> tuple[float, float, float]:
        """Interogate the device to get all axes positions
        """
        if not self.is_connected():
            return (None, None, None)

        x_pos = str(self.get_dir_pos("x"))
        y_pos = str(self.get_dir_pos("y"))
        z_pos = str(self.get_dir_pos("z"))

        return (x_pos, y_pos, z_pos)

    def get_dir_pos(self, direction:Literal["x", "y", "z"]) -> int:
        """Get the given axis stored position 
        (does not interogate the device)
        """
        return self.axis_control[direction].DevicePosition

    def __repr__(self):
        return (f"<NanoMaxController("
                f"Connected={self.connexion_established}, "
                f"AxisControl={{'x': {self.axis_control['x']}, "
                f"'y': {self.axis_control['y']}, "
                f"'z': {self.axis_control['z']}}}, "
                f"Positions={self.get_xyz_pos()})>")

    def __str__(self):
        return (f"<NanoMaxController(\n"
                f"  Connected={self.connexion_established},\n"
                f"  AxisControl={{'x': {self.axis_control['x']},\n"
                f"               'y': {self.axis_control['y']},\n"
                f"               'z': {self.axis_control['z']}}},\n"
                f"  Positions={self.get_xyz_pos()}\n"
                f")>")

def main():

    config = configparser.ConfigParser()
    config.add_section('NanoMax300')
    config.set('NanoMax300', 'channel_1', 'y')
    config.set('NanoMax300', 'channel_2', 'x')
    config.set('NanoMax300', 'channel_3', 'z')
    config.set('NanoMax300', 'nanomax300_orientation_x', '0')
    config.set('NanoMax300', 'nanomax300_orientation_y', '0')
    config.set('NanoMax300', 'nanomax300_orientation_z', '0')

    nanomax_controller = NanoMaxController(config)
    print(nanomax_controller)

from amptek_controller import AmptekDevice
from utils import Hdf5Handler
import numpy as np
import h5py
import matplotlib.pyplot as plt

def cube_scan_meshgrid(hdf5_filepath, bounds:tuple, dwell_time, roi_energy, step_size_um:int):
    """Start a cube scan around the given center"""


    config = configparser.ConfigParser()
    config_filepath = r"C:\Users\CXRF\Code\depthpaint-c-xrf-interface\corapp\configurations\main_config.cfg"
    config.read(config_filepath)

    cxrf_controller =  AmptekDevice(config, maxrf_device=False)
    cxrf_controller.start_connection()
    cxrf_controller.set_calibration(-0.017286111111104674, 0.030652777777777862, 0, 1)
    nanomax_controller = NanoMaxController(config)
    nanomax_controller.start_connection()

    cxrf_controller.enable_mca_mcs()
    time.sleep(0.1)

    # Define the starting meshgrid
    a = int((bounds[0][1] - bounds[0][0])*1000 // step_size_um)
    b = int((bounds[1][1] - bounds[1][0])*1000 // step_size_um)
    c = 10
    print(f'{a}x{b}x{c} = {a*b*c} points to scan')
    x_start = np.linspace(bounds[0][0], bounds[0][1], num=a)
    y_start = np.linspace(bounds[1][0], bounds[1][1], num=b)
    z_start = np.linspace(bounds[2][0], bounds[2][1], num=c)
    points = np.array(np.meshgrid(x_start, y_start, z_start)).T.reshape(-1, 3).tolist()

    print(f'Starting cube scan with {len(points)} points')

    data_cube = np.zeros((a, b, c), dtype=np.int32)

    step_x_mm = round((bounds[0][1] - bounds[0][0]) / a, 3)
    step_y_mm = round((bounds[1][1] - bounds[1][0]) / b, 3)
    step_z_mm = round((bounds[2][1] - bounds[2][0]) / c, 3)
    print(f'{bounds=} {step_x_mm=}, {step_y_mm=}, {step_z_mm=}')

    count = 0
    for point in points:
        count += 1
        x, y, z = point
        x = round(x, 3)
        y = round(y, 3)
        z = round(z, 3)
        nanomax_controller.move_to("x", x)
        nanomax_controller.move_to("y", y)
        nanomax_controller.move_to("z", z)
        _, int_spectrum, _ = cxrf_controller.get_spectrum(get_status=False, clear_spectrum=True)
        time.sleep(dwell_time / 1000)
        _, int_spectrum, _ = cxrf_controller.get_spectrum(get_status=False, clear_spectrum=True, energy_roi=roi_energy)
        sum_spectrum = sum(int_spectrum)
        x_index = int((x - bounds[0][0]) / step_x_mm)
        y_index = int((y - bounds[1][0]) / step_y_mm)
        z_index = int((z - bounds[2][0]) / step_z_mm)
        if x_index >= data_cube.shape[0] :
            x_index = data_cube.shape[0] - 1
        if y_index >= data_cube.shape[1] :
            y_index = data_cube.shape[1] - 1
        if z_index >= data_cube.shape[2] :
            z_index = data_cube.shape[2] - 1
        print(f'Point scanned ({count}/{len(points)}) : {(x, y, z)}, sum_spectrum : {sum_spectrum}, stored at index : {x_index, y_index, z_index}')
        data_cube[x_index, y_index, z_index] = sum_spectrum

        Hdf5Handler.save_data_to_hdf5(hdf5_filepath, data_cube, np.array([0,1,0]), project_name="Test confocal alignment")

    # visualize_3d_mapping(hdf5_filepath)
    cxrf_controller.disable_mca_mcs()
    cxrf_controller.stop_connection()
    return data_cube

def visualize_3d_mapping(hdf5_filepath):
    with h5py.File(hdf5_filepath, 'r') as hdf5_file:
        data_cube = hdf5_file.get("/Test confocal alignment/Object/XRF_Analysis/C-XRF Profile")
        if data_cube is None :
            raise ValueError(f"Could not find dataset inside hdf5file : {hdf5_filepath}")
        

        x = list(np.arange(0, data_cube.shape[0])) * data_cube.shape[1] * data_cube.shape[2]
        x.sort()
        y = list(np.arange(0, data_cube.shape[1])) * data_cube.shape[2] 
        y.sort()
        y = y * data_cube.shape[0]
        z = list(np.arange(0, data_cube.shape[2]))
        z.sort()
        z = z * data_cube.shape[1] * data_cube.shape[0]
        c = data_cube[:, :, :]

        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        scatter = ax.scatter(x,y,z,c=c)
        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')

        # produce a legend with the unique colors from the scatter
        legend1 = ax.legend(*scatter.legend_elements(),
                            loc='lower left', title="Values")
        ax.add_artist(legend1)

        plt.show()

if __name__ == "__main__":
    hdf5_filepath=r"C:\Users\CXRF\Desktop\test_confocal_cube_scan_6.hdf5"
    
    # cube_scan_meshgrid(hdf5_filepath=hdf5_filepath,
    #                     bounds=((3.46, 3.56), (4.34, 4.46), (0.300, 1.30)),
    #                     dwell_time=1000,
    #                     roi_energy=(7.9, 9.0),
    #                     step_size_um=10)
    
    visualize_3d_mapping(hdf5_filepath)

    # config = configparser.ConfigParser()
    # config_filepath = r"C:\Users\CXRF\Code\depthpaint-c-xrf-interface\corapp\configurations\main_config.cfg"
    # config.read(config_filepath)
    # nanomax_controller = NanoMaxController(config)
    # nanomax_controller.start_connection()

    # time.sleep(5)
    # nanomax_controller.move_to("y", 1.0)
    # time.sleep(2)
    # nanomax_controller.move_to("y", 4.0)
    # time.sleep(2)
    # nanomax_controller.move_to("y", 8.0)
    # time.sleep(2)
    # nanomax_controller.move_to("y", 0.0)