"""
operation over the z serie WGN_01_0000_P_110_8128_D_129.h5

* step1: create one NXtomo per stage
* step2: remove flats of all the stages
* step3: sub sample the first NXtomo which projections will be used for flats
"""

import os
from nxtomomill.converter import from_h5_to_nx
from nxtomomill.io import TomoHDF5Config

# step 1: create one NXtomo per stage
config = TomoHDF5Config()
config.input_file = "WGN_01_0000_P_110_8128_D_129.h5"
config.output_file = "WGN_01_0000_P_110_8128_D_129.nx"
config.overwrite = True
convs = from_h5_to_nx(config)

os.remove("WGN_01_0000_P_110_8128_D_129.nx")

# step 2: remove flats from all stages (make them invalid)
from tomwer.core.scan.hdf5scan import HDF5TomoScan
from tomoscan.esrf.scan.hdf5scan import ImageKey
from tomwer.core.process.edit.imagekeyeditor import ImageKeyUpgraderTask

operations = {
    ImageKey.FLAT_FIELD: ImageKey.INVALID,
}

for file_path, data_path in convs:
    scan = HDF5TomoScan(file_path, data_path)
    task = ImageKeyUpgraderTask(
        inputs={
            "data": scan,
            "operations": {
                ImageKey.FLAT_FIELD: ImageKey.INVALID,
            },
        },
    )
    task.run()


# step 3: sub sample the first NXtomo and remove darks (unused)
import numpy
from nxtomomill.utils import change_image_key_control

# 3.1 remove darks of the 'ref' scan
scan = HDF5TomoScan("WGN_01_0000_P_110_8128_D_129_0000.nx", "entry0000")

task = ImageKeyUpgraderTask(
    inputs={
        "data": scan,
        "operations": {
            ImageKey.DARK_FIELD: ImageKey.INVALID,
        },
    },
)
task.run()
    

# 3.2 subsample 'ref' scan
from nxtomomill.nexus.nxtomo import NXtomo

nx_tomo = NXtomo().load(
    "WGN_01_0000_P_110_8128_D_129_0000.nx",
    "entry0000",
    detector_data_as="as_numpy_array",
)

nx_tomo.instrument.detector.data = nx_tomo.instrument.detector.data[::40]
nx_tomo.instrument.detector.image_key_control = nx_tomo.instrument.detector.image_key_control[::40]
nx_tomo.sample.rotation_angle = nx_tomo.sample.rotation_angle[::40]
nx_tomo.sample.x_translation.value = nx_tomo.sample.x_translation.value[::40]
nx_tomo.sample.y_translation.value = nx_tomo.sample.y_translation.value[::40]
nx_tomo.sample.z_translation.value = nx_tomo.sample.z_translation.value[::40]

nx_tomo.save("WGN_01_0000_P_110_8128_D_129_0000.nx", "entry0000", overwrite=True)

#frames_indexes = numpy.arange(101, 4602)

#change_image_key_control(
#    "WGN_01_0000_P_110_8128_D_129_0000.nx",
#    entry="entry0000",
#    frames_indexes=frames_indexes,
#    image_key_control_value=ImageKey.INVALID,
#)

#change_image_key_control(
#    "WGN_01_0000_P_110_8128_D_129_0000.nx",
#    entry="entry0000",
#    frames_indexes=frames_indexes[::40],
#    image_key_control_value=ImageKey.PROJECTION,
#)
