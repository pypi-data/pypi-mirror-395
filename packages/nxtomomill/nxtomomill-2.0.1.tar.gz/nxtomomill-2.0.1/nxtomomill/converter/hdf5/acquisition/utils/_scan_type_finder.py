from __future__ import annotations

import logging
import h5py
from silx.io.utils import h5py_read_dataset

from nxtomo.nxobject.nxdetector import ImageKey
from nxtomomill.models.h52nx._acquisitionstep import AcquisitionStep
from nxtomomill.io.config import TomoHDF5Config

_logger = logging.getLogger(__name__)


class ScanTypeFinder:
    """Util class to find the type of a bliss scan (entry)"""

    def __init__(self, configuration: TomoHDF5Config):
        self._configuration = configuration

    def find(self, entry: h5py.Group):
        if not isinstance(entry, h5py.Group):
            raise ValueError(
                f"Expected path is not related to a h5py.Group ({entry}) when expect to target a bliss entry."
            )
        return (
            self.get_entry_type_from_technique_img_key(entry)
            or self.get_entry_type_from_scan_category(entry)
            or self.get_entry_type_from_title(entry)
        )

    def get_entry_type_from_title(self, entry: h5py.Group):
        """
        try to determine the entry type from the title
        """
        try:
            title = h5py_read_dataset(entry["title"])
        except Exception:
            _logger.error(f"fail to find title for {entry.name}, skip this group")
            return None
        else:
            init_titles = list(self._configuration.init_titles)
            init_titles.extend(self._configuration.zseries_init_titles)
            init_titles.extend(self._configuration.multitomo_init_titles)
            init_titles.extend(self._configuration.back_and_forth_init_titles)

            step_titles = {
                AcquisitionStep.INITIALIZATION: init_titles,
                AcquisitionStep.DARK: self._configuration.dark_titles,
                AcquisitionStep.FLAT: self._configuration.flat_titles,
                AcquisitionStep.PROJECTION: self._configuration.projection_titles,
                AcquisitionStep.ALIGNMENT: self._configuration.alignment_titles,
            }

            for step, titles in step_titles.items():
                for title_start in titles:
                    if title.startswith(title_start):
                        return step
            return None

    def get_entry_type_from_technique_img_key(
        self, entry: h5py.Group
    ) -> AcquisitionStep | None:
        """
        try to determine entry type from the scan/technique sub groups.
        If this is a flat then we expect to have a "flat" group. If this is a set of projection we expect to have a "proj" group.
        For now alignment / return are unfilled
        """
        group_technique = entry.get("technique", dict())
        if "image_key" not in group_technique:
            return None

        image_key = h5py_read_dataset(group_technique["image_key"])
        if image_key is None:
            return None
        else:
            try:
                image_key = ImageKey(image_key)
            except ValueError:
                _logger.error(f"unrecognized image key: '{image_key}'")
                return None
            else:
                connections = {
                    ImageKey.DARK_FIELD: AcquisitionStep.DARK,
                    ImageKey.FLAT_FIELD: AcquisitionStep.FLAT,
                    ImageKey.PROJECTION: AcquisitionStep.PROJECTION,
                    ImageKey.ALIGNMENT: AcquisitionStep.ALIGNMENT,
                }
                return connections.get(image_key, None)

    def get_entry_type_from_scan_category(
        self, entry: h5py.Group
    ) -> AcquisitionStep | None:
        if "scan_category" in entry.get("technique", {}):
            return AcquisitionStep.INITIALIZATION
        else:
            return None
