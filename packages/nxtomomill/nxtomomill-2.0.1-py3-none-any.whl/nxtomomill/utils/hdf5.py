# coding: utf-8

import contextlib

import h5py
import pint
import logging
from .pintutils import get_unit

try:
    import hdf5plugin  # noqa F401
except ImportError:
    pass
from silx.io.url import DataUrl
from silx.io.utils import open as open_hdf5

_logger = logging.getLogger(__name__)

__all__ = ["EntryReader", "DatasetReader"]


class _BaseReader(contextlib.AbstractContextManager):
    def __init__(self, url: DataUrl):
        if not isinstance(url, DataUrl):
            raise TypeError(f"url should be an instance of DataUrl. Not {type(url)}")
        if url.scheme() not in ("silx", "h5py"):
            raise ValueError("Valid scheme are silx and h5py")
        if url.data_slice() is not None:
            raise ValueError(
                "Data slices are not managed. Data path should "
                "point to a bliss node (h5py.Group)"
            )
        self._url = url
        self._file_handler = None

    def __exit__(self, *exc):
        return self._file_handler.close()


class EntryReader(_BaseReader):
    """Context manager used to read a bliss node"""

    def __enter__(self):
        self._file_handler = open_hdf5(filename=self._url.file_path())
        if self._url.data_path() == "":
            entry = self._file_handler
        elif self._url.data_path() not in self._file_handler:
            raise KeyError(
                f"data path '{self._url.data_path()}' doesn't exists from '{self._url.file_path()}'"
            )
        else:
            entry = self._file_handler[self._url.data_path()]
        if not isinstance(entry, h5py.Group):
            raise ValueError("Data path should point to a bliss node (h5py.Group)")
        return entry


class DatasetReader(_BaseReader):
    """Context manager used to read a bliss node"""

    def __enter__(self):
        self._file_handler = open_hdf5(filename=self._url.file_path())
        entry = self._file_handler[self._url.data_path()]
        if not isinstance(entry, h5py.Dataset):
            raise ValueError(
                f"Data path ({self._url.path()}) should point to a dataset (h5py.Dataset)"
            )
        return entry


def get_dataset_unit(
    dataset: h5py.Dataset, default: pint.Unit, from_dataset: str
) -> pint.Unit:
    """
    Util function to return the pint Unit of a HDF5 dataset.
    This dataset must have `unit` or `units` defined else will fall back to the default unit

    :param from_dataset: information about the 'dataset' / metadata we are trying to access. For logging purpose in case of failure.
    """
    if not isinstance(dataset, h5py.Dataset):
        raise TypeError(
            f"dataset is expected to be an instance of {h5py.Dataset}. Got {type(dataset)}."
        )
    if "unit" in dataset.attrs:
        unit = dataset.attrs["unit"]
    elif "units" in dataset.attrs:
        unit = dataset.attrs["units"]
    else:
        _logger.info(f"no unit found for {from_dataset}. Take default unit: {default}")
        return default

    if hasattr(unit, "decode"):
        # handle Diamond dataset
        unit = unit.decode()

    return get_unit(unit=unit, default=default, from_dataset=from_dataset)
