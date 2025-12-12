import h5py
import numpy
import pint
from silx.io.utils import h5py_read_dataset
from silx.io.utils import open as open_hdf5
from tomoscan.io import HDF5File

from nxtomo.nxobject.nxobject import NXobject
from nxtomomill.utils.hdf5 import get_dataset_unit

__all__ = [
    "cast_and_check_array_1D",
    "create_nx_data_group",
    "link_nxbeam_to_root",
    "get_data_and_unit",
    "get_data",
    "concatenate",
]


def _is_iterable(value):
    if isinstance(value, (str, bytes)):
        return False
    try:
        iter(value)
    except TypeError:
        return False
    return True


def cast_and_check_array_1D(array, array_name):
    if not (array is None or isinstance(array, numpy.ndarray) or _is_iterable(array)):
        raise TypeError(
            f"{array_name} is expected to be None, or a sequence. Not {type(array)}"
        )
    if array is not None and not isinstance(array, numpy.ndarray):
        array = numpy.asarray(array)
    if array is not None and array.ndim > 1:
        raise ValueError(f"{array_name} is expected to be 0 or 1d not {array.ndim}")
    return array


def create_nx_data_group(file_path: str, entry_path: str, axis_scale: list):
    """
    Create the 'Nxdata' group at entry level with soft links on the NXDetector
    and NXsample.

    :param file_path:
    :param entry_path:
    :param axis_scale:
    :return:
    """
    if not isinstance(file_path, str):
        raise TypeError("file_path is expected to be a file")
    if not isinstance(entry_path, str):
        raise TypeError("entry_path is expected to be a file")
    if not _is_iterable(axis_scale):
        raise TypeError("axis_scale is expected to be a sequence")

    with HDF5File(file_path, mode="a") as h5f:
        entry_group = h5f[entry_path]

        nx_data_grp = entry_group.require_group("data")
        # link detector datasets:
        if not entry_path.startswith("/"):
            entry_path = "/" + entry_path
        for dataset in ("data", "image_key", "image_key_control"):
            dataset_path = "/".join((entry_path, "instrument", "detector", dataset))
            nx_data_grp[dataset] = h5py.SoftLink(dataset_path)
        # link rotation angle
        nx_data_grp["rotation_angle"] = h5py.SoftLink(
            "/".join((entry_path, "sample", "rotation_angle"))
        )

        # write NX attributes
        nx_data_grp.attrs["NX_class"] = "NXdata"
        nx_data_grp.attrs["signal"] = "data"
        nx_data_grp.attrs["SILX_style/axis_scale_types"] = axis_scale
        nx_data_grp["data"].attrs["interpretation"] = "image"


def link_nxbeam_to_root(file_path, entry_path):
    """
    Create the 'Nxdata' group at entry level with soft links on the NXDetector
    and NXsample.

    :param file_path:
    :param entry_path:
    :return:
    """
    if not isinstance(file_path, str):
        raise TypeError("file_path is expected to be a file")
    if not isinstance(entry_path, str):
        raise TypeError("entry_path is expected to be a file")

    if not entry_path.startswith("/"):
        entry_path = "/" + entry_path
    with HDF5File(file_path, mode="a") as h5f:
        entry_group = h5f[entry_path]
        entry_group["beam"] = h5py.SoftLink(
            "/".join((entry_path, "instrument", "beam"))
        )


def get_data_and_unit(
    file_path: str,
    data_path: str,
    default_unit: pint.Unit,
    from_dataset: str = "Unknown",
):
    with open_hdf5(file_path) as h5f:
        if data_path in h5f and isinstance(h5f[data_path], h5py.Dataset):
            dataset = h5f[data_path]
            unit = get_dataset_unit(
                dataset=dataset, default=default_unit, from_dataset=from_dataset
            )
            return h5py_read_dataset(dataset), unit
        else:
            return None, default_unit


def get_data(file_path, data_path):
    with open_hdf5(file_path) as h5f:
        if data_path in h5f:
            return h5py_read_dataset(h5f[data_path])
        else:
            return None


def concatenate(nx_objects, **kwargs):
    if len(nx_objects) == 0:
        return None
    else:
        if not isinstance(nx_objects[0], NXobject):
            raise TypeError("nx_objects are expected to be instances of NXobject")
        return type(nx_objects[0]).concatenate(nx_objects=nx_objects, **kwargs)
