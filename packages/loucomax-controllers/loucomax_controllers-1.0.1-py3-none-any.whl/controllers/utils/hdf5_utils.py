# -- coding: utf-8 -*-

# builtin imports
import threading
from datetime import datetime

# Third-party imports
import matplotlib.pyplot as plt
import h5py
import numpy as np

# Static Class
class Hdf5Handler():

    @staticmethod
    def save_data_to_hdf5(save_filepath : str,
                           output_data: np.ndarray,
                            calibration: np.ndarray,
                             topology_data:np.ndarray=None,
                              project_name="Project",
                               object_name="Object",
                                analysis_name="XRF_Analysis",
                                 dataset_name="C-XRF Profile",
                                  mono_xrf_dataset_name="XRF profile",
                                   mono_xrf_data= None,
                                    summed_mono_xrf_data= None,
                                     calibration_mono_xrf= None,
                                      pictures_starting_point:dict={},
                                       profiles_positions_pictures:dict={},
                                        metadata:dict={}):
        """Save the data from MAXRF mapping to a given HDF5 file"""
        # Ensure thread safety when accessing the HDF5 file
        with threading.Lock():

            with h5py.File(save_filepath, 'a') as final_hdf5:

                project_group = final_hdf5.require_group(project_name)
                object_group = project_group.require_group(object_name)
                profile_group = object_group.require_group(analysis_name)
                mono_xrf_group_name = str(profile_group.name).replace("C-XRF", "XRF")
                mono_xrf_group = object_group.require_group(mono_xrf_group_name)
                try:
                    # Create the dataset if it does not exist
                    dataset = profile_group.require_dataset(dataset_name, shape=output_data.shape, dtype=output_data.dtype)
                    if topology_data is not None:
                        topology_dataset = profile_group.require_dataset('Map Topography', shape=topology_data.shape, dtype=topology_data.dtype)
                    
                    # Save the pictures of the starting point if provided
                    if pictures_starting_point is not None :
                        for key, picture in pictures_starting_point.items():
                            if picture is not None:
                                picture_dset = profile_group.create_dataset(f'Image Starting Point - {key}', data=picture, compression='gzip')
                                picture_dset.attrs.create('CLASS','IMAGE',dtype='S6')
                                picture_dset.attrs.create('IMAGE_SUBCLASS','IMAGE_TRUECOLOR',dtype='S16')
                                picture_dset.attrs.create('IMAGE_VERSION','1.2',dtype='S4')
                                picture_dset.attrs.create('INTERLACE_MODE','INTERLACE_PIXEL',dtype='S16')
                                picture_dset.attrs.create('IMAGE_MINMAXRANGE',[0, 255],dtype=np.uint8) 

                    # Save the pictures of the profiles positions if provided
                    if profiles_positions_pictures is not None :
                        for key, picture in profiles_positions_pictures.items():
                            if picture is not None:
                                picture_dset = profile_group.create_dataset(f'Image Profiles Position - {key}', data=picture, compression='gzip')
                                picture_dset.attrs.create('CLASS','IMAGE',dtype='S6')
                                picture_dset.attrs.create('IMAGE_SUBCLASS','IMAGE_TRUECOLOR',dtype='S16')
                                picture_dset.attrs.create('IMAGE_VERSION','1.2',dtype='S4')
                                picture_dset.attrs.create('INTERLACE_MODE','INTERLACE_PIXEL',dtype='S16')
                                picture_dset.attrs.create('IMAGE_MINMAXRANGE',[0, 255],dtype=np.uint8) 

                except TypeError :
                    # Dataset already exists, we then append the data
                    dataset = profile_group.get(dataset_name)
                    if topology_data is not None:
                        topology_dataset = profile_group.get('Map Topography')

                dataset[:] = output_data
                if topology_data is not None:
                    topology_dataset[:] = topology_data

                calib = profile_group.require_dataset("calibration", shape=calibration.shape, dtype=np.float64)
                calib[:] = calibration

                # If Mono XRF data is provided, create a dataset for it
                # and copy the data into it
                if (mono_xrf_data is not None) and (summed_mono_xrf_data is not None) and (calibration_mono_xrf is not None):
                    try:
                        # Create the dataset if it does not exist
                        mono_xrf_dataset = mono_xrf_group.require_dataset(mono_xrf_dataset_name, shape=mono_xrf_data.shape, dtype=np.float64)
                        summed_mono_xrf_dataset = mono_xrf_group.require_dataset("(Summed) "+mono_xrf_dataset_name, shape=summed_mono_xrf_data.shape, dtype=np.float64)
                    except TypeError as e:
                        # Dataset already exists, we then replace the data
                        print(f"TypeError : {e}")
                        mono_xrf_dataset = mono_xrf_group.get(mono_xrf_dataset_name)
                        summed_mono_xrf_dataset = mono_xrf_group.get("(Summed) "+mono_xrf_dataset_name)

                    mono_xrf_dataset[:] = mono_xrf_data
                    summed_mono_xrf_dataset[:] = summed_mono_xrf_data

                    calib_mono = mono_xrf_group.require_dataset("calibration", shape=(3,), dtype=np.float64)
                    calib_mono[:] = calibration_mono_xrf

                for attribute, value in metadata.items() :
                    if value is None:
                        value = ''
                    if "project" in attribute.lower() or "user" in attribute.lower() or "owner" in attribute.lower() :
                        project_group.attrs[attribute] = value
                    elif "object" in attribute.lower() or "sample" in attribute.lower() or "lab" in attribute.lower():
                        object_group.attrs[attribute] = value
                    else:
                        profile_group.attrs[attribute] = value
                        mono_xrf_group.attrs[attribute] = value

def main():
    # Example usage of the Hdf5Handler class
    save_filepath = "example_data.hdf5"
    output_data = np.random.rand(100, 100, 512)  # Simulated XRF data
    calibration = np.random.rand(3)
    mono_xrf_data = output_data.sum(axis=(0, 1))  # Simulated mono XRF data
    calibration_mono_xrf = np.random.rand(3)
    picture = np.random.rand(256, 256, 3) * 255  # Simulated RGB image
    picture2 = np.random.rand(256, 256, 3) * 255  # Simulated RGB image
    pictures_starting_point = {"Camera1": picture, "Camera2": picture2}
    metadata = {
        "project_name": "Example Project",
        "object_name": "Example Object",
        "user": "Example User",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    Hdf5Handler.save_data_to_hdf5(
        save_filepath,
        output_data,
        calibration,
        project_name="Example Project",
        object_name="Example Object",
        analysis_name="XRF Analysis",
        dataset_name="2D-XRF Mapping",
        mono_xrf_dataset_name="XRF point",
        mono_xrf_data=mono_xrf_data,
        calibration_mono_xrf=calibration_mono_xrf,
        pictures_starting_point=pictures_starting_point,
        metadata=metadata
    )

if __name__ == "__main__":

    main()
