"""
operation over the z serie WGN_01_0000_P_110_8128_D_129.h5

* step1: create one NXtomo per stage
* step2: remove dark and flat from the second acquisition. So the copy can be tested.
"""

import os
from nxtomomill.converter import from_h5_to_nx
from nxtomomill.io import TomoHDF5Config
from tomwer.core.scan.hdf5scan import HDF5TomoScan
from tomoscan.esrf.scan.hdf5scan import ImageKey
from tomwer.core.process.edit.imagekeyeditor import ImageKeyUpgraderTask


# step 1: create one NXtomo per stage
config = TomoHDF5Config()
config.input_file = "WGN_01_0000_P_110_8128_D_129.h5"
config.output_file = "WGN_01_0000_P_110_8128_D_129.nx"
config.overwrite = True
convs = from_h5_to_nx(config)

# remove unused nx
os.remove("WGN_01_0000_P_110_8128_D_129.nx")
os.remove("WGN_01_0000_P_110_8128_D_129_0002.nx")

# step 2: remove flats from all stages (make them invalid)
operations = {
    ImageKey.FLAT_FIELD: ImageKey.INVALID,
    ImageKey.DARK_FIELD: ImageKey.INVALID,
}

for file_path, data_path in convs[1:2]:
    scan = HDF5TomoScan(file_path, data_path)
    task = ImageKeyUpgraderTask(
        inputs={
            "data": scan,
            "operations": operations,
        },
    )
    task.run()
