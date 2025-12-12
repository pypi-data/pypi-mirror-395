# coding: utf-8

from __future__ import annotations

import pint
import configparser
import logging

from typing import Iterable

from nxtomo.nxobject.nxsource import ProbeType, SourceType

from nxtomomill.io.config.optionlevel import OptionLevel, filter_options_level_items
from nxtomomill.io.config.configbase import ConfigBase, ConfigSourceSection

from nxtomomill.io.utils import (
    PathType,
    convert_str_to_bool,
    convert_str_to_tuple,
    filter_str_def,
)
from nxtomomill.settings import Tomo
from nxtomomill.utils import FileExtension
from nxtomomill.utils.pintutils import (
    VALID_CURRENT_VALUES,
    VALID_ENERGY_VALUES,
    VALID_METRIC_VALUES,
)

_ureg = pint.get_application_registry()
_logger = logging.getLogger(__name__)


__all__ = ["TomoEDFConfig", "generate_default_edf_config"]


class TomoEDFConfig(ConfigBase, ConfigSourceSection):
    """
    Configuration class to provide to the convert from h5 to nx
    """

    # General section keys

    GENERAL_SECTION_DK = "GENERAL_SECTION"

    INPUT_FOLDER_DK = "input_folder"

    OUTPUT_FILE_DK = "output_file"

    FILE_EXTENSION_DK = "file_extension"

    OVERWRITE_DK = "overwrite"

    DELETE_EDF_SOURCE_FILES = "delete_edf_source_file"

    OUTPUT_CHECKS = "output_checks"

    DATASET_BASENAME_DK = "dataset_basename"

    DATASET_FILE_INFO_DK = "dataset_info_file"

    LOG_LEVEL_DK = "log_level"

    TITLE_DK = "title"

    IGNORE_FILE_PATTERN_DK = "patterns_to_ignores"

    DUPLICATE_DATA_DK = "duplicate_data"

    EXTERNAL_LINK_RELATIVE_DK = "external_link_path"

    COMMENTS_GENERAL_SECTION = {
        GENERAL_SECTION_DK: "general information. \n",
        INPUT_FOLDER_DK: "Folder containing .edf files. if not provided from the configuration file must be provided from the command line",
        OUTPUT_FILE_DK: "output file name. If not provided from the configuration file must be provided from the command line",
        OVERWRITE_DK: "overwrite output files if exists without asking",
        FILE_EXTENSION_DK: "file extension. Ignored if the output file is provided and contains an extension",
        DELETE_EDF_SOURCE_FILES: "remove EDF source files once the conversion is complete. Works only if 'duplicate_data' is True (this is the case by default)",
        OUTPUT_CHECKS: "Once the conversion is done some checks can be done to check the validity of the conversion. Expected as a list of elements. Possibles tests are: 'compare-output-volume'",
        DATASET_BASENAME_DK: f"dataset file prefix. Usde to determine projections file and info file. If not provided will take the name of {INPUT_FOLDER_DK}",
        DATASET_FILE_INFO_DK: f"path to .info file containing dataset information (Energy, ScanRange, TOMO_N...). If not will deduce it from {DATASET_BASENAME_DK}",
        LOG_LEVEL_DK: 'Log level. Valid levels are "debug", "info", "warning" and "error"',
        TITLE_DK: "NXtomo title",
        IGNORE_FILE_PATTERN_DK: "some file pattern leading to ignoring the file. Like reconstructed slice files.",
        DUPLICATE_DATA_DK: "If False then will create embed all the data into a single file avoiding external link to other file. If True then the detector data will point to original edf files. In this case you must be carreful to keep relative paths valid. Warning: to read external dataset you nust be at the hdf5 file working directory. See external link resolution details: https://support.hdfgroup.org/documentation/hdf5/latest/group___h5_l.html#title5",
        EXTERNAL_LINK_RELATIVE_DK: "If 'duplicate_data' is set to False then you can specify if you want the link to original files to be 'relative' or 'absolute'",
    }

    LEVEL_GENERAL_SECTION = {
        INPUT_FOLDER_DK: OptionLevel.REQUIRED,
        OUTPUT_FILE_DK: OptionLevel.REQUIRED,
        OVERWRITE_DK: OptionLevel.REQUIRED,
        FILE_EXTENSION_DK: OptionLevel.ADVANCED,
        DELETE_EDF_SOURCE_FILES: OptionLevel.ADVANCED,
        OUTPUT_CHECKS: OptionLevel.ADVANCED,
        DATASET_BASENAME_DK: OptionLevel.REQUIRED,
        DATASET_FILE_INFO_DK: OptionLevel.REQUIRED,
        LOG_LEVEL_DK: OptionLevel.REQUIRED,
        TITLE_DK: OptionLevel.ADVANCED,
        IGNORE_FILE_PATTERN_DK: OptionLevel.REQUIRED,
        DUPLICATE_DATA_DK: OptionLevel.REQUIRED,
        EXTERNAL_LINK_RELATIVE_DK: OptionLevel.ADVANCED,
    }

    # EDF KEYS SECTION

    EDF_KEYS_SECTION_DK = "EDF_KEYS_SECTION"

    MOTOR_POSITION_KEY_DK = "motor_position_key"

    MOTOR_MNE_KEY_DK = "motor_mne_key"

    X_TRANS_KEY_DK = "x_translation_key"

    Y_TRANS_KEY_DK = "y_translation_key"

    Z_TRANS_KEY_DK = "z_translation_key"

    ROT_ANGLE_KEY_DK = "rot_angle_key"

    COMMENTS_KEYS_SECTION = {
        EDF_KEYS_SECTION_DK: "section to define EDF keys to pick from headers to deduce information like rotation angle.\n",
        MOTOR_POSITION_KEY_DK: "motor position key",
        MOTOR_MNE_KEY_DK: "key to retrieve indices of each motor in metadata",
        X_TRANS_KEY_DK: "key to be used for x translation",
        Y_TRANS_KEY_DK: "key to be used for y translation",
        Z_TRANS_KEY_DK: "key to be used for z translation",
        ROT_ANGLE_KEY_DK: "key to be used for rotation angle",
    }

    LEVEL_KEYS_SECTION = {
        MOTOR_POSITION_KEY_DK: OptionLevel.REQUIRED,
        MOTOR_MNE_KEY_DK: OptionLevel.REQUIRED,
        X_TRANS_KEY_DK: OptionLevel.REQUIRED,
        Y_TRANS_KEY_DK: OptionLevel.REQUIRED,
        Z_TRANS_KEY_DK: OptionLevel.REQUIRED,
        ROT_ANGLE_KEY_DK: OptionLevel.REQUIRED,
    }

    # DARK AND FLAT SECTION

    FLAT_DARK_SECTION_DK = "DARK_AND_FLAT_SECTION"

    DARK_NAMES_DK = "dark_names_prefix"

    FLAT_NAMES_DK = "flat_names_prefix"

    COMMENTS_DARK_FLAT_SECTION = {
        FLAT_DARK_SECTION_DK: "section to define dark and flat detection. \n",
        DARK_NAMES_DK: "prefix of dark field file(s)",
        FLAT_NAMES_DK: "prefix of flat field file(s)",
    }

    LEVEL_DARK_FLAT_SECTION = {
        DARK_NAMES_DK: OptionLevel.REQUIRED,
        FLAT_NAMES_DK: OptionLevel.REQUIRED,
    }

    # UNITS SECTION

    UNIT_SECTION_DK = "UNIT_SECTION"

    PIXEL_SIZE_EXPECTED_UNIT = "expected_unit_for_pixel_size"

    DISTANCE_EXPECTED_UNIT = "expected_unit_for_distance"

    ENERGY_EXPECTED_UNIT = "expected_unit_for_energy"

    X_TRANS_EXPECTED_UNIT = "expected_unit_for_x_translation"

    Y_TRANS_EXPECTED_UNIT = "expected_unit_for_y_translation"

    Z_TRANS_EXPECTED_UNIT = "expected_unit_for_z_translation"

    MACHINE_CURRENT_EXPECTED_UNIT = "expected_unit_for_machine_current"

    COMMENTS_UNIT_SECTION_DK = {
        UNIT_SECTION_DK: "Details units system used on SPEC side to save data. All will ne converted to NXtomo default (SI at the exception of energy-keV) \n",
        PIXEL_SIZE_EXPECTED_UNIT: f"Size used to save pixel size. Must be in of {VALID_METRIC_VALUES}",
        DISTANCE_EXPECTED_UNIT: f"Unit used by SPEC to save sample to detector distance. Must be in of {VALID_METRIC_VALUES}",
        ENERGY_EXPECTED_UNIT: f"Unit used by SPEC to save energy. Must be in of {VALID_ENERGY_VALUES}",
        X_TRANS_EXPECTED_UNIT: f"Unit used by SPEC to save x translation. Must be in of {VALID_METRIC_VALUES}",
        Y_TRANS_EXPECTED_UNIT: f"Unit used by SPEC to save y translation. Must be in of {VALID_METRIC_VALUES}",
        Z_TRANS_EXPECTED_UNIT: f"Unit used by SPEC to save z translation. Must be in of {VALID_METRIC_VALUES}",
        MACHINE_CURRENT_EXPECTED_UNIT: f"Unit used by SPEC to save machine current (also aka SRcurrent). Must be in of {VALID_CURRENT_VALUES}",
    }

    LEVEL_UNIT_SECTION = {
        PIXEL_SIZE_EXPECTED_UNIT: OptionLevel.ADVANCED,
        DISTANCE_EXPECTED_UNIT: OptionLevel.ADVANCED,
        ENERGY_EXPECTED_UNIT: OptionLevel.ADVANCED,
        X_TRANS_EXPECTED_UNIT: OptionLevel.ADVANCED,
        Y_TRANS_EXPECTED_UNIT: OptionLevel.ADVANCED,
        Z_TRANS_EXPECTED_UNIT: OptionLevel.ADVANCED,
    }

    # SAMPLE SECTION

    SAMPLE_SECTION_DK = "SAMPLE_SECTION"

    SAMPLE_NAME_DK = "sample_name"

    FORCE_ANGLE_CALCULATION = "force_angle_calculation"

    FORCE_ANGLE_CALCULATION_ENDPOINT = "angle_calculation_endpoint"

    FORCE_ANGLE_CALCULATION_REVERT_NEG_SCAN_RANGE = (
        "angle_calculation_rev_neg_scan_range"
    )

    COMMENTS_SAMPLE_SECTION_DK = {
        SAMPLE_SECTION_DK: "section dedicated to sample definition.\n",
        SAMPLE_NAME_DK: "name of the sample",
        FORCE_ANGLE_CALCULATION: "Should the rotation angle be computed from scan range and numpy.linspace or should we try to load it from .edf header.",
        FORCE_ANGLE_CALCULATION_ENDPOINT: "If rotation angles have to be calculated set numpy.linspace endpoint parameter to this value. If True then the rotation angle value of the last projection will be equal to the `ScanRange` value",
        FORCE_ANGLE_CALCULATION_REVERT_NEG_SCAN_RANGE: "Invert rotation angle values in the case of negative `ScanRange` value",
    }

    LEVEL_SAMPLE_SECTION = {
        SAMPLE_NAME_DK: OptionLevel.ADVANCED,
        FORCE_ANGLE_CALCULATION: OptionLevel.REQUIRED,
        FORCE_ANGLE_CALCULATION_ENDPOINT: OptionLevel.REQUIRED,
        FORCE_ANGLE_CALCULATION_REVERT_NEG_SCAN_RANGE: OptionLevel.ADVANCED,
    }

    # DETECTOR SECTION

    DETECTOR_SECTION_DK = "DETECTOR_SECTION"

    FIELD_OF_VIEW_DK = "field_of_view"

    COMMENTS_DETECTOR_SECTION_DK = {
        DETECTOR_SECTION_DK: "section dedicated to detector definition \n",
        FIELD_OF_VIEW_DK: "Detector field of view. Must be in `Half` or `Full`",
    }

    LEVEL_DETECTOR_SECTION = {
        FIELD_OF_VIEW_DK: OptionLevel.ADVANCED,
    }

    # create comments

    COMMENTS = COMMENTS_GENERAL_SECTION
    COMMENTS.update(COMMENTS_KEYS_SECTION)
    COMMENTS.update(COMMENTS_DARK_FLAT_SECTION)
    COMMENTS.update(COMMENTS_UNIT_SECTION_DK)
    COMMENTS.update(COMMENTS_SAMPLE_SECTION_DK)
    COMMENTS.update(ConfigSourceSection.COMMENTS_SOURCE_SECTION_DK)
    COMMENTS.update(COMMENTS_DETECTOR_SECTION_DK)

    SECTIONS_LEVEL = {
        GENERAL_SECTION_DK: OptionLevel.REQUIRED,
        EDF_KEYS_SECTION_DK: OptionLevel.REQUIRED,
        FLAT_DARK_SECTION_DK: OptionLevel.REQUIRED,
        UNIT_SECTION_DK: OptionLevel.ADVANCED,
        SAMPLE_SECTION_DK: OptionLevel.REQUIRED,
        ConfigSourceSection.SOURCE_SECTION_DK: OptionLevel.ADVANCED,
        DETECTOR_SECTION_DK: OptionLevel.ADVANCED,
    }

    def __init__(self):
        super().__init__()
        self._set_freeze(False)
        # general information
        self._input_folder = None
        self._output_file = None
        self._file_extension = FileExtension.NX
        self._overwrite = False
        self._delete_edf_source_files = False
        self._output_checks = tuple()
        self._dataset_basename = None
        self._log_level = logging.WARNING
        self._title = None
        self._ignore_file_patterns = Tomo.EDF.TO_IGNORE
        self._dataset_info_file = None
        self._duplicate_data = True
        self._external_path_type = PathType.RELATIVE

        # edf header keys
        self._motor_position_keys = Tomo.EDF.MOTOR_POS
        self._motor_mne_keys = Tomo.EDF.MOTOR_MNE
        self._x_trans_keys = Tomo.EDF.X_TRANS
        self._y_trans_keys = Tomo.EDF.Y_TRANS
        self._z_trans_keys = Tomo.EDF.Z_TRANS
        self._rot_angle_keys = Tomo.EDF.ROT_ANGLE
        self._machine_current_keys = Tomo.EDF.MACHINE_CURRENT

        # dark and flat
        self._dark_names = Tomo.EDF.DARK_NAMES
        self._flat_names = Tomo.EDF.REFS_NAMES

        # units
        self._pixel_size_unit = _ureg.micrometer
        self._distance_unit = _ureg.millimeter
        self._energy_unit = _ureg.keV
        self._x_trans_unit = _ureg.millimeter
        self._y_trans_unit = _ureg.millimeter
        self._z_trans_unit = _ureg.millimeter
        self._machine_current_unit = _ureg.milliampere

        # sample
        self._sample_name = None
        self._force_angle_calculation = True
        # there is too many EDF headers containing the rotation angle set to 0
        # when it shouldn't be. To ease usage we are 'ignoring' those keys by default...
        self._force_angle_calculation_endpoint = False
        self._force_angle_calculation_revert_neg_scan_range = True

        # source
        self._instrument_name = None
        self._source_name = "ESRF"
        self._source_type = SourceType.SYNCHROTRON_X_RAY_SOURCE
        self._source_probe = ProbeType.X_RAY

        # detector
        self._field_of_view = None

        self._set_freeze(True)

    @property
    def input_folder(self) -> str | None:
        return self._input_folder

    @input_folder.setter
    def input_folder(self, folder: str | None) -> None:
        if not isinstance(folder, (type(None), str)):
            raise TypeError(
                f"folder is expected to be None or an instance of str. Not {type(folder)}"
            )
        self._input_folder = folder

    @property
    def dataset_basename(self) -> str | None:
        return self._dataset_basename

    @dataset_basename.setter
    def dataset_basename(self, dataset_basename: str | None) -> None:
        if not isinstance(dataset_basename, (type(None), str)):
            raise TypeError(
                f"dataset_basename is expected to be None or an instance of str. Not {type(dataset_basename)}"
            )
        self._dataset_basename = dataset_basename

    @property
    def dataset_info_file(self) -> str | None:
        return self._dataset_info_file

    @dataset_info_file.setter
    def dataset_info_file(self, file_path: str | None) -> None:
        if not isinstance(file_path, (type(None), str)):
            raise TypeError(
                f"file_path is expected to be None or an instance of str. Not {type(file_path)}"
            )
        self._dataset_info_file = file_path

    @property
    def duplicate_data(self) -> bool:
        return self._duplicate_data

    @duplicate_data.setter
    def duplicate_data(self, duplicate: bool):
        if not isinstance(duplicate, bool):
            raise TypeError(
                f"duplicate is expected to be a bool and not {type(duplicate)}"
            )
        self._duplicate_data = duplicate

    @property
    def external_path_type(self) -> PathType:
        return self._external_path_type

    @external_path_type.setter
    def external_path_type(self, path_type: str | PathType):
        self._external_path_type = PathType(path_type)

    @property
    def title(self) -> str | None:
        return self._title

    @title.setter
    def title(self, title: str | None) -> None:
        if not isinstance(title, (type(None), str)):
            raise TypeError(
                f"title is expected to be None or an instance of str. Not {type(title)}"
            )
        self._title = title

    @property
    def delete_edf_source_files(self) -> bool:
        return self._delete_edf_source_files

    @delete_edf_source_files.setter
    def delete_edf_source_files(self, delete: bool) -> None:
        if not isinstance(delete, bool):
            raise TypeError("'delete' is expected to be a bool")
        self._delete_edf_source_files = delete

    @property
    def output_checks(self) -> tuple:
        return self._output_checks

    @output_checks.setter
    def output_checks(self, checks: tuple | None) -> None:
        if checks is None:
            self._output_checks = tuple()
        elif not isinstance(checks, tuple):
            raise TypeError("'checks' is expected to be None or a tuple")
        else:
            self._output_checks = checks

    @property
    def ignore_file_patterns(self) -> tuple:
        return self._ignore_file_patterns

    @ignore_file_patterns.setter
    def ignore_file_patterns(self, patterns: tuple | list | None):
        if not isinstance(patterns, (type(None), tuple, list)):
            raise TypeError("patterns is expected to be a tuple or a list")
        if patterns is None:
            self._ignore_file_patterns = tuple()
        else:
            for elmt in patterns:
                if not isinstance(elmt, str):
                    raise TypeError("patterns elmts are expected to be str")
            self._ignore_file_patterns = tuple(patterns)

    @property
    def motor_position_keys(self) -> tuple:
        return self._motor_position_keys

    @motor_position_keys.setter
    def motor_position_keys(self, keys: tuple | list | None) -> None:
        if not isinstance(keys, (type(None), tuple, list)):
            raise TypeError(
                "keys is expected to be None or an instance of list or tuple"
            )
        if keys is None:
            self._motor_position_keys = tuple()
        else:
            for elmt in keys:
                if not isinstance(elmt, str):
                    raise TypeError("keys elmts are expected to be str")
            self._motor_position_keys = tuple(keys)

    @property
    def motor_mne_keys(self) -> tuple:
        return self._motor_mne_keys

    @motor_mne_keys.setter
    def motor_mne_keys(self, keys: tuple | list | None) -> None:
        if not isinstance(keys, (type(None), tuple, list)):
            raise TypeError(
                "keys is expected to be None or an instance of list or tuple"
            )
        if keys is None:
            self._motor_mne_keys = tuple()
        else:
            for elmt in keys:
                if not isinstance(elmt, str):
                    raise TypeError("keys elmts are expected to be str")
            self._motor_mne_keys = tuple(keys)

    @property
    def dark_names(self) -> tuple:
        return self._dark_names

    @dark_names.setter
    def dark_names(self, names: tuple | list | None) -> None:
        if not isinstance(names, (type(None), tuple, list)):
            raise TypeError("names is expected to be a tuple or a list")
        if names is None:
            self._dark_names = tuple()
        else:
            for elmt in names:
                if not isinstance(elmt, str):
                    raise TypeError("names elmts are expected to be str")
            self._dark_names = tuple(names)

    @property
    def flat_names(self) -> tuple:
        return self._flat_names

    @flat_names.setter
    def flat_names(self, names: tuple | list | None) -> None:
        if not isinstance(names, (type(None), tuple, list)):
            raise TypeError("names is expected to be a tuple or a list")
        if names is None:
            self._flat_names = tuple()
        else:
            for elmt in names:
                if not isinstance(elmt, str):
                    raise TypeError("names elmts are expected to be str")
            self._flat_names = tuple(names)

    @property
    def pixel_size_unit(self) -> pint.Unit:
        return self._pixel_size_unit

    @pixel_size_unit.setter
    def pixel_size_unit(self, unit: pint.Unit | str) -> None:
        if not isinstance(unit, (pint.Unit, str)):
            raise TypeError("unit is expected to be an instance of pint.Unit")
        if isinstance(unit, str):
            unit = pint.Unit(unit)
        self._pixel_size_unit = unit

    @property
    def distance_unit(self) -> pint.Unit:
        return self._distance_unit

    @distance_unit.setter
    def distance_unit(self, unit: pint.Unit | str) -> None:
        if not isinstance(unit, (pint.Unit, str)):
            raise TypeError("unit is expected to be an instance of pint.Unit")
        if isinstance(unit, str):
            unit = pint.Unit(unit)
        self._distance_unit = unit

    @property
    def energy_unit(self) -> pint.Unit:
        return self._energy_unit

    @energy_unit.setter
    def energy_unit(self, unit: pint.Unit | str) -> None:
        if not isinstance(unit, (pint.Unit, str)):
            raise TypeError("unit is expected to be an instance of pint.Unit")
        if isinstance(unit, str):
            unit = pint.Unit(unit)
        self._energy_unit = unit

    @property
    def x_trans_keys(self):
        return self._x_trans_keys

    @x_trans_keys.setter
    def x_trans_keys(self, keys: Iterable) -> None:
        if not isinstance(keys, Iterable) or isinstance(keys, str):
            raise TypeError("'keys' should be an Iterable")

        for elmt in keys:
            if not isinstance(elmt, str):
                raise TypeError("keys elmts are expected to be str")
        self._x_trans_keys = keys

    @property
    def x_trans_unit(self) -> pint.Unit:
        return self._x_trans_unit

    @x_trans_unit.setter
    def x_trans_unit(self, unit: pint.Unit | str) -> None:
        if not isinstance(unit, (pint.Unit, str)):
            raise TypeError("unit is expected to be an instance of pint.unit")
        if isinstance(unit, str):
            unit = pint.Unit(unit)
        self._x_trans_unit = unit

    @property
    def y_trans_keys(self):
        return self._y_trans_keys

    @y_trans_keys.setter
    def y_trans_keys(self, keys: Iterable) -> None:
        if not isinstance(keys, Iterable) or isinstance(keys, str):
            raise TypeError("'keys' should be an Iterable")

        for elmt in keys:
            if not isinstance(elmt, str):
                raise TypeError("keys elmts are expected to be str")
        self._y_trans_keys = keys

    @property
    def y_trans_unit(self) -> pint.Unit:
        return self._y_trans_unit

    @y_trans_unit.setter
    def y_trans_unit(self, unit: pint.Unit | str) -> None:
        if not isinstance(unit, (pint.Unit, str)):
            raise TypeError("unit is expected to be an instance of pint.Unit")
        if isinstance(unit, str):
            unit = pint.Unit(unit)
        self._y_trans_unit = unit

    @property
    def z_trans_keys(self):
        return self._z_trans_keys

    @z_trans_keys.setter
    def z_trans_keys(self, keys: Iterable) -> None:
        if not isinstance(keys, Iterable) or isinstance(keys, str):
            raise TypeError("'keys' should be an Iterable")

        for elmt in keys:
            if not isinstance(elmt, str):
                raise TypeError("keys elmts are expected to be str")
        self._z_trans_keys = keys

    @property
    def z_trans_unit(self) -> pint.Unit:
        return self._z_trans_unit

    @z_trans_unit.setter
    def z_trans_unit(self, unit: pint.Unit | str) -> None:
        if not isinstance(unit, (pint.Unit, str)):
            raise TypeError("unit is expected to be an instance of pint.Unit")
        if isinstance(unit, str):
            unit = pint.Unit(unit)
        self._z_trans_unit = unit

    @property
    def machine_current_unit(self) -> pint.Unit:
        return self._machine_current_unit

    @machine_current_unit.setter
    def machine_current_unit(self, unit):
        if not isinstance(unit, (str, pint.Unit)):
            raise TypeError("unit is expected to be an instance of pint.Unit")
        if isinstance(unit, str):
            unit = pint.Unit(unit)
        self._machine_current_unit = unit

    @property
    def sample_name(self) -> str | None:
        return self._sample_name

    @sample_name.setter
    def sample_name(self, name: str | None) -> None:
        if not isinstance(name, (type(None), str)):
            raise TypeError("name is expected to be None or an instance of str")
        self._sample_name = name

    @property
    def force_angle_calculation(self) -> bool:
        return self._force_angle_calculation

    @force_angle_calculation.setter
    def force_angle_calculation(self, force: bool):
        if not isinstance(force, bool):
            raise TypeError(
                f"force is expected to be an instance of bool. Not {type(force)}  - {force}"
            )
        self._force_angle_calculation = force

    @property
    def force_angle_calculation_endpoint(self) -> bool:
        return self._force_angle_calculation_endpoint

    @force_angle_calculation_endpoint.setter
    def force_angle_calculation_endpoint(self, endpoint: bool) -> None:
        if not isinstance(endpoint, bool):
            raise TypeError(
                f"endpoint is expected to be an instance of bool. Not {type(endpoint)}"
            )
        self._force_angle_calculation_endpoint = endpoint

    @property
    def angle_calculation_rev_neg_scan_range(self) -> bool:
        return self._force_angle_calculation_revert_neg_scan_range

    @angle_calculation_rev_neg_scan_range.setter
    def angle_calculation_rev_neg_scan_range(self, revert: bool):
        if not isinstance(revert, bool):
            raise TypeError(
                f"revert is expected to be an instance of bool. Not {type(revert)}"
            )
        self._force_angle_calculation_revert_neg_scan_range = revert

    @property
    def instrument_name(self) -> str | None:
        return self._instrument_name

    @instrument_name.setter
    def instrument_name(self, name: str | None):
        if not isinstance(name, (type(None), str)):
            raise TypeError("name is expected to be None or an instance of str")
        self._instrument_name = name

    @property
    def source_name(self) -> str | None:
        return self._source_name

    @source_name.setter
    def source_name(self, name: str | None) -> None:
        if not isinstance(name, (type(None), str)):
            raise TypeError("name is expected to be None or an instance of str")
        self._source_name = name

    @property
    def source_type(self) -> SourceType | None:
        return self._source_type

    @source_type.setter
    def source_type(self, source_type: SourceType | str | None):
        if not isinstance(source_type, (type(None), str, SourceType)):
            raise TypeError(
                "source_type is expected to be None or an instance of SourceType or str"
            )
        if source_type is None:
            self._source_type = None
        else:
            self._source_type = SourceType(source_type)

    @property
    def source_probe(self) -> ProbeType | None:
        return self._source_probe

    @source_probe.setter
    def source_probe(self, source_probe: ProbeType | str | None):
        if not isinstance(source_probe, (type(None), str, ProbeType)):
            raise TypeError(
                "source_probe is expected to be None or an instance of ProbeType or str"
            )
        if source_probe is None:
            self._source_probe = None
        else:
            self._source_probe = ProbeType(source_probe)

    def to_dict(self, level="advanced") -> dict:
        """convert the configuration to a dictionary"""
        level = OptionLevel(level)
        sections_callback = {
            self.GENERAL_SECTION_DK: self._general_section_to_dict,
            self.EDF_KEYS_SECTION_DK: self._edf_keys_section_to_dict,
            self.FLAT_DARK_SECTION_DK: self._flat_keys_section_to_dict,
            self.UNIT_SECTION_DK: self._unit_section_to_dict,
            self.SAMPLE_SECTION_DK: self._sample_section_to_dict,
            self.SOURCE_SECTION_DK: self._source_section_to_dict,
            self.DETECTOR_SECTION_DK: self._detector_section_to_dict,
        }
        res = {}
        for section, callback in sections_callback.items():
            if (
                level == OptionLevel.ADVANCED
                or TomoEDFConfig.SECTIONS_LEVEL[section] == OptionLevel.REQUIRED
            ):
                res[section] = callback(level=level)
        return res

    def _general_section_to_dict(self, level) -> dict:
        res = {
            self.INPUT_FOLDER_DK: (
                self.input_folder if self.input_folder is not None else ""
            ),
            self.OUTPUT_FILE_DK: (
                self.output_file if self.output_file is not None else ""
            ),
            self.OVERWRITE_DK: self.overwrite,
            self.DELETE_EDF_SOURCE_FILES: self.delete_edf_source_files,
            self.OUTPUT_CHECKS: self.output_checks,
            self.FILE_EXTENSION_DK: self.file_extension.value,
            self.DATASET_BASENAME_DK: (
                self.dataset_basename if self.dataset_basename is not None else ""
            ),
            self.DATASET_FILE_INFO_DK: (
                self.dataset_info_file if self.dataset_info_file is not None else ""
            ),
            self.LOG_LEVEL_DK: logging.getLevelName(self.log_level).lower(),
            self.TITLE_DK: self.title if self.title is not None else "",
            self.IGNORE_FILE_PATTERN_DK: (
                self.ignore_file_patterns
                if self.ignore_file_patterns != tuple()
                else ""
            ),
            self.DUPLICATE_DATA_DK: self.duplicate_data,
            self.EXTERNAL_LINK_RELATIVE_DK: self.external_path_type.value,
        }
        return filter_options_level_items(
            dict_=res, level=level, level_ref=TomoEDFConfig.LEVEL_GENERAL_SECTION
        )

    def _edf_keys_section_to_dict(self, level) -> dict:
        res = {
            self.MOTOR_POSITION_KEY_DK: (
                self.motor_position_keys if self.motor_position_keys != tuple() else ""
            ),
            self.MOTOR_MNE_KEY_DK: (
                self.motor_mne_keys if self.motor_mne_keys != tuple() else ""
            ),
            self.ROT_ANGLE_KEY_DK: (
                self.rotation_angle_keys if self.rotation_angle_keys != tuple() else ""
            ),
            self.X_TRANS_KEY_DK: (
                self.x_trans_keys if self.x_trans_keys != tuple() else ""
            ),
            self.Y_TRANS_KEY_DK: (
                self.y_trans_keys if self.y_trans_keys != tuple() else ""
            ),
            self.Z_TRANS_KEY_DK: (
                self.z_trans_keys if self.z_trans_keys != tuple() else ""
            ),
        }
        return filter_options_level_items(
            dict_=res, level=level, level_ref=TomoEDFConfig.LEVEL_KEYS_SECTION
        )

    def _flat_keys_section_to_dict(self, level) -> dict:
        res = {
            self.DARK_NAMES_DK: self.dark_names if self.dark_names != tuple() else "",
            self.FLAT_NAMES_DK: self.flat_names if self.dark_names != tuple() else "",
        }
        return filter_options_level_items(
            dict_=res, level=level, level_ref=TomoEDFConfig.LEVEL_DARK_FLAT_SECTION
        )

    def _unit_section_to_dict(self, level) -> dict:
        res = {
            self.PIXEL_SIZE_EXPECTED_UNIT: str(self.pixel_size_unit),
            self.DISTANCE_EXPECTED_UNIT: str(self.distance_unit),
            self.ENERGY_EXPECTED_UNIT: str(self.energy_unit),
            self.X_TRANS_EXPECTED_UNIT: str(self.x_trans_unit),
            self.Y_TRANS_EXPECTED_UNIT: str(self.y_trans_unit),
            self.Z_TRANS_EXPECTED_UNIT: str(self.z_trans_unit),
            self.MACHINE_CURRENT_EXPECTED_UNIT: str(self.machine_current_unit),
        }
        return filter_options_level_items(
            dict_=res, level=level, level_ref=TomoEDFConfig.LEVEL_UNIT_SECTION
        )

    def _sample_section_to_dict(self, level) -> dict:
        res = {
            self.SAMPLE_NAME_DK: (
                self.sample_name if self.sample_name is not None else ""
            ),
            self.FORCE_ANGLE_CALCULATION: self.force_angle_calculation,
            self.FORCE_ANGLE_CALCULATION_ENDPOINT: self.force_angle_calculation_endpoint,
            self.FORCE_ANGLE_CALCULATION_REVERT_NEG_SCAN_RANGE: self.angle_calculation_rev_neg_scan_range,
        }
        return filter_options_level_items(
            dict_=res, level=level, level_ref=TomoEDFConfig.LEVEL_SAMPLE_SECTION
        )

    def _source_section_to_dict(self, level) -> dict:
        res = {
            self.INSTRUMENT_NAME_DK: self.instrument_name or "",
            self.SOURCE_NAME_DK: self.source_name or "",
            self.SOURCE_TYPE_DK: (
                self.source_type.value if self.source_type is not None else ""
            ),
            self.SOURCE_PROBE_DK: (
                self.source_probe.value if self.source_probe is not None else ""
            ),
        }
        return filter_options_level_items(
            dict_=res, level=level, level_ref=TomoEDFConfig.LEVEL_SOURCE_SECTION
        )

    def _detector_section_to_dict(self, level) -> dict:
        res = {
            self.FIELD_OF_VIEW_DK: (
                self.field_of_view.value if self.field_of_view is not None else ""
            ),
        }
        return filter_options_level_items(
            dict_=res, level=level, level_ref=TomoEDFConfig.LEVEL_DETECTOR_SECTION
        )

    @staticmethod
    def from_dict(dict_: dict):
        r"""
        Create a HDF5Config object and set it from values contained in the
        dictionary
        :param dict\_: settings dictionary
        :return: HDF5Config
        """
        config = TomoEDFConfig()
        config.load_from_dict(dict_)
        return config

    def load_from_dict(self, dict_: dict) -> None:
        """Load the configuration from a dictionary"""
        sections_loaders = {
            TomoEDFConfig.GENERAL_SECTION_DK: self.load_general_section,
            TomoEDFConfig.EDF_KEYS_SECTION_DK: self.load_keys_section,
            TomoEDFConfig.FLAT_DARK_SECTION_DK: self.load_flat_dark_section,
            TomoEDFConfig.UNIT_SECTION_DK: self.load_unit_section,
            TomoEDFConfig.SAMPLE_SECTION_DK: self.load_sample_section,
            TomoEDFConfig.SOURCE_SECTION_DK: self.load_source_section,
            TomoEDFConfig.DETECTOR_SECTION_DK: self.load_detector_section,
        }
        for section_key, loaded_func in sections_loaders.items():
            if section_key in dict_:
                loaded_func(dict_[section_key])
            else:
                _logger.info(
                    f"No {section_key} section found. Will take default values"
                )

    def load_general_section(self, dict_: dict) -> None:
        self.input_folder = dict_.get(TomoEDFConfig.INPUT_FOLDER_DK, None)
        self.output_file = dict_.get(TomoEDFConfig.OUTPUT_FILE_DK, None)
        overwrite = dict_.get(TomoEDFConfig.OVERWRITE_DK, None)
        if overwrite is not None:
            self.overwrite = convert_str_to_bool(overwrite)

        delete_edf_source_files = dict_.get(TomoEDFConfig.DELETE_EDF_SOURCE_FILES, None)
        if delete_edf_source_files is not None:
            self.delete_edf_source_files = convert_str_to_bool(delete_edf_source_files)

        output_checks = dict_.get(TomoEDFConfig.OUTPUT_CHECKS, None)
        if output_checks is not None:
            self.output_checks = convert_str_to_tuple(output_checks)

        file_extension = dict_.get(TomoEDFConfig.FILE_EXTENSION_DK, None)
        if file_extension not in (None, ""):
            self.file_extension = filter_str_def(file_extension)

        dataset_basename = dict_.get(TomoEDFConfig.DATASET_BASENAME_DK, None)
        if dataset_basename is not None:
            if dataset_basename == "":
                dataset_basename = None
            self.dataset_basename = dataset_basename

        dataset_info_file = dict_.get(TomoEDFConfig.DATASET_FILE_INFO_DK, None)
        if dataset_info_file is not None:
            if dataset_info_file == "":
                dataset_info_file = None
            self.dataset_info_file = dataset_info_file

        log_level = dict_.get(TomoEDFConfig.LOG_LEVEL_DK, None)
        if log_level is not None:
            self.log_level = log_level
        self.title = dict_.get(TomoEDFConfig.TITLE_DK)
        ignore_file_patterns = dict_.get(TomoEDFConfig.IGNORE_FILE_PATTERN_DK, None)
        if ignore_file_patterns is not None:
            if ignore_file_patterns == "":
                ignore_file_patterns = tuple()
            else:
                ignore_file_patterns = convert_str_to_tuple(ignore_file_patterns)
            self.ignore_file_patterns = ignore_file_patterns
        duplicate_data = dict_.get(TomoEDFConfig.DUPLICATE_DATA_DK, None)
        if duplicate_data is not None:
            self.duplicate_data = convert_str_to_bool(duplicate_data)
        external_path_type = dict_.get(TomoEDFConfig.EXTERNAL_LINK_RELATIVE_DK, None)
        if external_path_type is not None:
            self.external_path_type = external_path_type

    def load_keys_section(self, dict_: dict) -> None:
        motor_position_keys = dict_.get(TomoEDFConfig.MOTOR_POSITION_KEY_DK, None)
        if motor_position_keys is not None:
            if motor_position_keys == "":
                motor_position_keys = tuple()
            else:
                motor_position_keys = convert_str_to_tuple(motor_position_keys)
            self.motor_position_keys = motor_position_keys

        motor_mne_keys = dict_.get(TomoEDFConfig.MOTOR_MNE_KEY_DK, None)
        if motor_mne_keys is not None:
            if motor_mne_keys == "":
                motor_mne_keys = tuple()
            else:
                motor_mne_keys = convert_str_to_tuple(motor_mne_keys)
            self.motor_mne_keys = motor_mne_keys

        rotation_angle_keys = dict_.get(TomoEDFConfig.ROT_ANGLE_KEY_DK, None)
        if rotation_angle_keys is not None:
            if rotation_angle_keys == "":
                rotation_angle_keys = tuple()
            else:
                rotation_angle_keys = convert_str_to_tuple(rotation_angle_keys)
            self.rotation_angle_keys = rotation_angle_keys

        x_trans_keys = dict_.get(TomoEDFConfig.X_TRANS_KEY_DK, None)
        if x_trans_keys is not None:
            if x_trans_keys == "":
                x_trans_keys = tuple()
            else:
                x_trans_keys = convert_str_to_tuple(x_trans_keys)
            self.x_trans_keys = x_trans_keys

        y_trans_keys = dict_.get(TomoEDFConfig.Y_TRANS_KEY_DK, None)
        if y_trans_keys is not None:
            if y_trans_keys == "":
                y_trans_keys = tuple()
            else:
                y_trans_keys = convert_str_to_tuple(y_trans_keys)
            self.y_trans_keys = y_trans_keys

        z_trans_keys = dict_.get(TomoEDFConfig.Z_TRANS_KEY_DK, None)
        if z_trans_keys is not None:
            if z_trans_keys == "":
                z_trans_keys = tuple()
            else:
                z_trans_keys = convert_str_to_tuple(z_trans_keys)
            self.z_trans_keys = z_trans_keys

    def load_flat_dark_section(self, dict_: dict) -> None:
        dark_names = dict_.get(TomoEDFConfig.DARK_NAMES_DK, None)
        if dark_names is not None:
            if dark_names == "":
                dark_names = tuple()
            else:
                dark_names = convert_str_to_tuple(dark_names)
            self.dark_names = dark_names

        flat_names = dict_.get(TomoEDFConfig.FLAT_NAMES_DK, None)
        if flat_names is not None:
            if flat_names == "":
                flat_names = tuple()
            else:
                flat_names = convert_str_to_tuple(flat_names)
            self.flat_names = flat_names

    def load_unit_section(self, dict_: dict) -> None:
        if TomoEDFConfig.PIXEL_SIZE_EXPECTED_UNIT in dict_:
            self.pixel_size_unit = pint.Unit(
                dict_.get(TomoEDFConfig.PIXEL_SIZE_EXPECTED_UNIT)
            )
        if TomoEDFConfig.DISTANCE_EXPECTED_UNIT in dict_:
            self.distance_unit = pint.Unit(
                dict_.get(TomoEDFConfig.DISTANCE_EXPECTED_UNIT)
            )
        if TomoEDFConfig.ENERGY_EXPECTED_UNIT in dict_:
            self.energy_unit = pint.Unit(dict_.get(TomoEDFConfig.ENERGY_EXPECTED_UNIT))
        if TomoEDFConfig.X_TRANS_EXPECTED_UNIT in dict_:
            self.x_trans_unit = pint.Unit(
                dict_.get(TomoEDFConfig.X_TRANS_EXPECTED_UNIT)
            )
        if TomoEDFConfig.Y_TRANS_EXPECTED_UNIT in dict_:
            self.y_trans_unit = pint.Unit(
                dict_.get(TomoEDFConfig.Y_TRANS_EXPECTED_UNIT)
            )
        if TomoEDFConfig.Z_TRANS_EXPECTED_UNIT in dict_:
            self.z_trans_unit = pint.Unit(
                dict_.get(TomoEDFConfig.Z_TRANS_EXPECTED_UNIT)
            )
        if TomoEDFConfig.MACHINE_CURRENT_EXPECTED_UNIT in dict_:
            self.machine_current_unit = pint.Unit(
                dict_.get(TomoEDFConfig.MACHINE_CURRENT_EXPECTED_UNIT)
            )

    def load_sample_section(self, dict_: dict) -> None:
        if TomoEDFConfig.SAMPLE_NAME_DK in dict_:
            self.sample_name = dict_.get(TomoEDFConfig.SAMPLE_NAME_DK)

        force_angle_calculation = dict_.get(TomoEDFConfig.FORCE_ANGLE_CALCULATION, None)
        if force_angle_calculation is not None:
            self.force_angle_calculation = convert_str_to_bool(force_angle_calculation)

        force_angle_calculation_endpoint = dict_.get(
            TomoEDFConfig.FORCE_ANGLE_CALCULATION_ENDPOINT, None
        )
        if force_angle_calculation_endpoint is not None:
            self.force_angle_calculation_endpoint = convert_str_to_bool(
                force_angle_calculation_endpoint
            )

        angle_calculation_rev_neg_scan_range = dict_.get(
            TomoEDFConfig.FORCE_ANGLE_CALCULATION_REVERT_NEG_SCAN_RANGE, None
        )
        if angle_calculation_rev_neg_scan_range is not None:
            self.angle_calculation_rev_neg_scan_range = convert_str_to_bool(
                angle_calculation_rev_neg_scan_range
            )

    def load_detector_section(self, dict_: dict) -> None:
        field_of_view = dict_.get(TomoEDFConfig.FIELD_OF_VIEW_DK, None)
        if field_of_view is not None:
            if field_of_view == "":
                field_of_view = None
            self.field_of_view = field_of_view

    def to_cfg_file(self, file_path: str):
        # TODO: add some generic information like:provided order of the tuple
        # will be the effective one. You can provide a key from it names if
        # it is contained in the positioners group
        # maybe split in sub section ?
        self.dict_to_cfg(file_path=file_path, dict_=self.to_dict())

    @staticmethod
    def dict_to_cfg(file_path, dict_):
        """ """
        return ConfigBase._dict_to_cfg(
            file_path=file_path,
            dict_=dict_,
            comments_fct=TomoEDFConfig.get_comments,
            logger=_logger,
        )

    @staticmethod
    def from_cfg_file(file_path: str, encoding=None):
        assert file_path is not None, "file_path should not be None"
        config_parser = configparser.ConfigParser(allow_no_value=True)
        config_parser.read(file_path, encoding=encoding)
        return TomoEDFConfig.from_dict(config_parser)

    @staticmethod
    def get_comments(key):
        return TomoEDFConfig.COMMENTS[key]


def generate_default_edf_config(level: str = "required") -> dict:
    """generate a default configuration for converting spec-edf to NXtomo"""
    return TomoEDFConfig().to_dict(level=level)
