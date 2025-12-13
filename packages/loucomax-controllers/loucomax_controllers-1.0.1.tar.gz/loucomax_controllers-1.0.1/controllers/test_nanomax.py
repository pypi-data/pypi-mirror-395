
from amptek_controller import AmptekDevice
from LouCOMAX_Controllers.controllers.nanomax_controller import NanoMaxController
from utils import Hdf5Handler
import configparser
import numpy as np
import time

def cube_scan_origin(amptek_controller: AmptekDevice, dwell_time, start_xyz, roi, x_pixel_size, x_pixel_num, y_pixel_size, y_pixel_num, z_pixel_size, z_pixel_num):
    
    hdf5_filepath = r"C:\Users\CXRF\Code\depthpaint-c-xrf-interface\corapp\tests\results\3d_scan\test_confocal_align.hdf5"

    amptek_controller.start_connection()
    print((x_pixel_num, y_pixel_num, z_pixel_num))
    data_cube = np.zeros((x_pixel_num, y_pixel_num, z_pixel_num))

    # Hdf5Handler.create_empty_hdf5(hdf5_filepath, data_cube.shape, group_name="Test confocal alignment")

    config = configparser.ConfigParser()
    config_filepath = r"C:\Users\CXRF\Code\depthpaint-c-xrf-interface\corapp\configurations\main_config.cfg"
    config.read(config_filepath)

    nanomax_controller = NanoMaxController(config)
    nanomax_controller.start_connection()

    start_x, start_y, start_z = start_xyz
    print(f'{start_x=}, {start_y=}, {start_z=}')
    
    nanomax_controller.move_to("x", start_x)
    nanomax_controller.move_to("y", start_y)
    nanomax_controller.move_to("z", start_z)

    amptek_controller.enable_mca_mcs()
    time.sleep(0.1)
    maximum = 0
    max_xyz = (0., 0., 0.)
    
    t_start = time.perf_counter()
    
    for x in range(x_pixel_num):
        print(f'Time spent : {time.perf_counter() - t_start}')
        max_chan, int_spectrum, _ = amptek_controller.get_spectrum(get_status=False, clear_spectrum=True)
        for y in range(y_pixel_num):
            max_chan, int_spectrum, _ = amptek_controller.get_spectrum(get_status=False, clear_spectrum=True)
            for z in range(z_pixel_num):
                
                # max_chan, int_spectrum, _ = amptek_controller.get_spectrum(get_status=False, clear_spectrum=True)
                time.sleep(dwell_time / 1000)
                max_chan, int_spectrum, _ = amptek_controller.get_spectrum(get_status=False, clear_spectrum=True)

                current_xyz = nanomax_controller.get_xyz_pos()
                # Change the ROI here
                sum_spectrum = sum(int_spectrum[roi[0] : roi[1]])

                if sum_spectrum > maximum :
                    maximum = sum_spectrum
                    max_xyz = current_xyz
                    print(f'{maximum=}, {max_xyz=}')

                x_index = int(x)
                y_index = int(y)
                z_index = int(z)
                data_cube[x_index,y_index,z_index] = sum_spectrum

                nanomax_controller.move_relative_forward("z", z_pixel_size)
                print(f'{x, y, z}, {maximum=}, {current_xyz=}')

            nanomax_controller.move_relative_forward("y", y_pixel_size)
            nanomax_controller.move_to("z", start_z)

        Hdf5Handler.save_data_to_hdf5(hdf5_filepath, data_cube, [0,1,0], project_name="Test confocal alignment")
        nanomax_controller.move_relative_forward("x", x_pixel_size)
        nanomax_controller.move_to("y", start_y)

    amptek_controller.disable_mca_mcs()
    amptek_controller.stop_connection()

    print(f'{maximum=}, {max_xyz=}')
    # Hdf5Handler.visualize_3d_mapping(hdf5_filepath, data_cube.shape, group_name="Test confocal alignment")

    return data_cube

def cube_scan_center(amptek_controller: AmptekDevice, dwell_time, center, roi, x_pixel_size, x_range, y_pixel_size, y_range, z_pixel_size, z_range):
    """Start a cube scan around the given center"""
    x_origin = center[0] - x_range / 2
    y_origin = center[1] - y_range / 2
    z_origin = center[2] - z_range / 2

    x_pixel_num = round(x_range / x_pixel_size)
    y_pixel_num = round(y_range / y_pixel_size)
    z_pixel_num = round(z_range / z_pixel_size)

    return cube_scan_origin(amptek_controller,
                            dwell_time=dwell_time,
                            start_xyz=(x_origin, y_origin, z_origin),
                            roi=roi,
                                x_pixel_size=x_pixel_size, x_pixel_num=x_pixel_num,
                                y_pixel_size=y_pixel_size, y_pixel_num=y_pixel_num,
                                z_pixel_size=z_pixel_size, z_pixel_num=z_pixel_num
                                )

def test_cube_scan_center():
    import matplotlib.pyplot as plt
    import numpy as np

    idvendor_cxrf = "0x10c4"
    idproduct_cxrf = "0x842a"
    researched_sn_cxrf = "36133"

    amptek_cxrf_controller = AmptekDevice(idvendor_cxrf,
                                            idproduct_cxrf,
                                            researched_sn_cxrf,
                                            maxrf_device=False)

    data_cube = cube_scan_center(amptek_cxrf_controller,
                                    dwell_time=50,
                                    center=(3.690, 3.950, 2.900),
                                    roi=[0, 511],
                                    x_pixel_size=0.020, x_range=0.100,
                                    y_pixel_size=0.020, y_range=0.200,
                                    z_pixel_size=0.020, z_range=0.200)

    print("data cube shape : ", data_cube.shape)

if __name__ == "__main__":
    
    test_cube_scan_center()
