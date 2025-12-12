"""data exchange (dx) configuration module"""

from __future__ import annotations
from nxtomo.nxobject.nxdetector import FieldOfView


__all__ = [
    "DXFileConfiguration",
]


class DXFileConfiguration:
    def __init__(self, input_file: str, output_file: str | None = None):
        self._input_file = input_file
        self._output_file = output_file
        self._file_extension = ".nx"
        self._copy_data = True
        self._input_entry = ("/",)
        self._output_entry = "entry0000"
        self._scan_range = (0, 180)
        self._pixel_size = (None, None)
        self._field_of_view = None
        self._sample_detector_distance = 1.0
        self._overwrite = True
        self._energy = None

    @property
    def input_file(self):
        return self._input_file

    @property
    def input_entry(self):
        return self._input_entry

    @input_entry.setter
    def input_entry(self, entry):
        self._input_entry = entry

    @property
    def output_file(self):
        return self._output_file

    @output_file.setter
    def output_file(self, output_file):
        self._output_file = output_file

    @property
    def output_entry(self):
        return self._output_entry

    @output_entry.setter
    def output_entry(self, entry):
        self._output_entry = entry

    @property
    def scan_range(self):
        return self._scan_range

    @scan_range.setter
    def scan_range(self, scan_range):
        self._scan_range = scan_range

    @property
    def copy_data(self):
        return self._copy_data

    @copy_data.setter
    def copy_data(self, copy):
        self._copy_data = copy

    @property
    def overwrite(self):
        return self._overwrite

    @overwrite.setter
    def overwrite(self, overwrite):
        self._overwrite = overwrite

    @property
    def sample_detector_distance(self) -> float | None:
        return self._sample_detector_distance

    @property
    def energy(self) -> float | None:
        return self._energy

    @energy.setter
    def energy(self, energy):
        self._energy = energy

    @sample_detector_distance.setter
    def sample_detector_distance(self, distance):
        self._sample_detector_distance = distance

    @property
    def field_of_view(self) -> FieldOfView | None:
        return self._field_of_view

    @field_of_view.setter
    def field_of_view(self, fov):
        self._field_of_view = fov

    @property
    def file_extension(self):
        return self._file_extension

    @file_extension.setter
    def file_extension(self, extension):
        self._file_extension = extension

    @property
    def pixel_size(self):
        return self._pixel_size

    @pixel_size.setter
    def pixel_size(self, pixel_size):
        self._pixel_size = pixel_size
