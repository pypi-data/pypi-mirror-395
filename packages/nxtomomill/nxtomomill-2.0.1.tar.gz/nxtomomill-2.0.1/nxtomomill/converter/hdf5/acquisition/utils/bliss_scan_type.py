from __future__ import annotations

from silx.io.url import DataUrl
from silx.io.utils import open as open_hdf5

from nxtomomill.io.config import TomoHDF5Config
from nxtomomill.models.h52nx._acquisitionstep import AcquisitionStep
from nxtomomill.utils.io import deprecated

from ._scan_type_finder import ScanTypeFinder


@deprecated(reason="renamed", replacement="get_bliss_scan_type", since_version="2.0")
def get_entry_type(*args, **kwargs):
    return get_bliss_scan_type(*args, **kwargs)


def get_bliss_scan_type(
    url: DataUrl, configuration: TomoHDF5Config
) -> AcquisitionStep | None:
    """
    :param url: bliss scan url to type
    :return: return the step of the acquisition or None if cannot find it.
    """
    if not isinstance(url, DataUrl):
        raise TypeError(f"DataUrl is expected. Not {type(url)}")
    if url.data_slice() is not None:
        raise ValueError(
            "url is expected to reference a Bliss scan entry (no slices supported)"
        )
    scan_type_finder = ScanTypeFinder(configuration=configuration)

    with open_hdf5(url.file_path()) as h5f:
        if url.data_path() not in h5f:
            raise ValueError(f"Provided path does not exist: {url}")
        entry = h5f[url.data_path()]
        return scan_type_finder.find(entry)
