# coding: utf-8

from __future__ import annotations

import configparser
import logging
from typing import Iterable

from silx.io.url import DataUrl

from nxtomomill import settings
from nxtomomill.io import utils
from nxtomomill.io.config.configbase import ConfigBase
from nxtomomill.io.framegroup import FrameGroup
from nxtomomill.utils.io import deprecated

_logger = logging.getLogger(__name__)


__all__ = [
    "TomoHDF5Config",
    "generate_default_h5_config",
]


def _example_fg_list(with_comment=True, with_prefix=False) -> str:
    """
    Print a simple example of providing a list of FrameGroup from str
    """

    fg_1 = FrameGroup(
        frame_type="projection",
        url=DataUrl(
            file_path="/path/to/file", data_path="/path/to/scan/node", scheme="silx"
        ),
        copy=True,
    )
    fg_2 = FrameGroup(
        frame_type="projection",
        url=DataUrl(
            file_path="/path/to/file2",
            data_path="/path_relative_to_file",
            scheme="silx",
        ),
    )
    if with_comment:
        comment = "# "
    else:
        comment = ""
    if with_prefix:
        prefix = "data_scans = "
    else:
        prefix = ""

    return """
{comment}{prefix}(
{comment}    {fg_1},
{comment}    {fg_2},
{comment})
""".format(
        prefix=prefix,
        comment=comment,
        fg_1=fg_1.str_representation(
            only_data_path=False, with_copy=True, with_prefix_key=True
        ),
        fg_2=fg_2.str_representation(
            only_data_path=True, with_copy=False, with_prefix_key=True
        ),
    )


class TomoHDF5Config(ConfigBase):
    """
    Configuration class to provide to the convert from h5 to nx
    """

    # note: sections names are expected to be upper case, sections keys are expected to be lower case

    # General section keys

    GENERAL_SECTION_DK = "GENERAL_SECTION"

    INPUT_FILE_DK = "input_file"

    OUTPUT_FILE_DK = "output_file"

    OVERWRITE_DK = "overwrite"

    FILE_EXTENSION_DK = "file_extension"

    LOG_LEVEL_DK = "log_level"

    RAISES_ERROR_DK = "raises_error"

    NO_INPUT_DK = "no_input"

    SINGLE_FILE_DK = "single_file"

    NO_MASTER_FILE_DK = "no_master_file"

    FIELD_OF_VIEW_DK = "field_of_view"

    HANDLE_MACHINE_CURRENT = "create_control_data"

    IGNORE_BLISS_TOMO_CONFIG = "ignore_bliss_tomo_config"

    COMMENTS_GENERAL_SECTION = {
        GENERAL_SECTION_DK: "general information. \n",
        INPUT_FILE_DK: "input file if not provided must be provided from the command line",
        OUTPUT_FILE_DK: "output file name. If not provided will use the input file basename and the file extension",
        OVERWRITE_DK: "overwrite output files if exists without asking",
        FILE_EXTENSION_DK: "file extension. Ignored if the output file is provided and contains an extension",
        LOG_LEVEL_DK: 'Log level. Valid levels are "debug", "info", "warning" and "error"',
        RAISES_ERROR_DK: "raise an error when met one. Otherwise continue and display an error log",
        NO_INPUT_DK: "Ask or not the user for any inputs (if missing information)",
        SINGLE_FILE_DK: "If True then will create a single file for all found sequences. "
        "If false create one nexus file per sequence and one master file with links to each sequence",
        IGNORE_BLISS_TOMO_CONFIG: "On recent bliss file (2023) a dedicated group specify datasets to be used for tomography. Defining for example translations, rotation, etc. If True then this group will be ignored and conversion will fallback on using path list provided in the KEYS section",
        FIELD_OF_VIEW_DK: "Force output to be a `Full` or a `Half` acquisition. If not provided we parse raw data to try to find this information.",
        HANDLE_MACHINE_CURRENT: "Generate control/data (aka machine current). This part will need to interpolate from existing values and can take time in some cases.",
        NO_MASTER_FILE_DK: "Avoid creating the master file",
    }

    # KEYS SECTION

    KEYS_SECTION_DK = "KEYS_SECTION"

    VALID_CAMERA_DK = "valid_camera_names"

    ROT_ANGLE_DK = "rotation_angle_keys"

    SAMPLE_X_KEYS_DK = "sample_x_keys"

    SAMPLE_Y_KEYS_DK = "sample_y_keys"

    TRANSLATION_Z_KEYS_DK = "translation_z_keys"

    TRANSLATION_Y_KEYS_DK = "translation_y_keys"

    DIODE_KEYS_DK = "diode_keys"

    ACQUISITION_EXPO_TIME_KEYS_DK = "exposure_time_keys"

    COMMENTS_KEYS_SECTION = {
        KEYS_SECTION_DK: "Identify specific path and datasets names to retrieve information from the bliss file. \n",
        VALID_CAMERA_DK: "Nxtomomill will try to deduce cameras from  dataset "
        "metadata and shape if none provided (default)."
        "If provided take the one requested. unix "
        "shell-style wildcards are managed",
        ROT_ANGLE_DK: "List of key to look for in order to find rotation angle",
        SAMPLE_X_KEYS_DK: "List of keys / paths to look for in order to find translation in x",
        SAMPLE_Y_KEYS_DK: "List of keys / paths to look for in order to find translation in y",
        TRANSLATION_Z_KEYS_DK: "List of /paths keys to look for in order to find translation in z",
        TRANSLATION_Y_KEYS_DK: "Key used to deduce the estimated center of rotation for half acquisition",
        DIODE_KEYS_DK: "List of keys to look for diode (if any)",
        ACQUISITION_EXPO_TIME_KEYS_DK: "List of keys to look for the exposure time",
    }

    # ENTRIES AND TITLES SECTION

    ENTRIES_AND_TITLES_SECTION_DK = "ENTRIES_AND_TITLES_SECTION"

    ENTRIES_DK = "entries"

    SUB_ENTRIES_TO_IGNORE = "sub_entries_to_ignore"

    INIT_TITLES_DK = "init_titles"

    ZSERIE_INIT_TITLES_DK = "zserie_init_titles"

    MULTITOMO_INIT_TITLES_DK = "multitomo_init_titles"

    DARK_TITLES_DK = "dark_titles"

    FLAT_TITLES_DK = "flat_titles"

    FLAT_TILES_ALIASES = ("ref_titles",)

    PROJ_TITLES_DK = "proj_titles"

    ALIGNMENT_TITLES_DK = "alignment_titles"

    SAMPLE_DETECTOR_DISTANCE_DK = "sample_detector_distance"

    SOURCE_SAMPLE_DISTANCE_DK = "source_sample_distance"

    SAMPLE_X_PIXEL_SIZE_KEYS_DK = "sample_x_pixel_size_keys"

    SAMPLE_Y_PIXEL_SIZE_KEYS_DK = "sample_y_pixel_size_keys"

    DETECTOR_X_PIXEL_SIZE_KEYS_DK = "detector_x_pixel_size_keys"

    DETECTOR_Y_PIXEL_SIZE_KEYS_DK = "detector_y_pixel_size_keys"

    COMMENTS_ENTRIES_TITLES_SECTION = {
        ENTRIES_AND_TITLES_SECTION_DK: "optional section \n"
        "# define titles meaning. Titles allows frame type deduction for each group.\n",
        ENTRIES_DK: "List of root entries (sequence initialization) to convert. If not provided will convert all root entries",
        SUB_ENTRIES_TO_IGNORE: "List of sub entries (non-root) to ignore",
        ACQUISITION_EXPO_TIME_KEYS_DK: "List of keys to look for the exposure time",
        INIT_TITLES_DK: "List of title to consider the group/entry as a initialization (sequence start). Ignored if dark_groups, flat_groups, projection_groups ... are provided.",
        ZSERIE_INIT_TITLES_DK: "List of title to consider the group/entry as a zseries initialization (sequence start). Ignored if dark_groups, flat_groups, projection_groups ... are provided.",
        MULTITOMO_INIT_TITLES_DK: "List of title to consider the group/entry as a multi-tomo initialization (sequence start). Ignored if dark_groups, flat_groups, projection_groups ... are provided.",
        DARK_TITLES_DK: "List of title to consider the group/entry as a dark.  Ignored if dark_groups, flat_groups, projection_groups ... are provided.",
        FLAT_TITLES_DK: "List of title to consider the group/entry as a reference / flat.  Ignored if dark_groups, flat_groups, projection_groups ... are provided.",
        PROJ_TITLES_DK: "List of title to consider the group/entry as a projection.  Ignored if dark_groups, flat_groups, projection_groups ... are provided.",
        ALIGNMENT_TITLES_DK: "List of title to consider the group/entry as an alignment.  Ignored if dark_groups, flat_groups, projection_groups ... are provided.",
        DETECTOR_X_PIXEL_SIZE_KEYS_DK: "List of keys / paths to look for the x **detector** pixel size",
        DETECTOR_Y_PIXEL_SIZE_KEYS_DK: "List of keys / paths to look for the y **detector** pixel size",
        SAMPLE_X_PIXEL_SIZE_KEYS_DK: "List of keys / paths to look for the x **sample** pixel size",
        SAMPLE_Y_PIXEL_SIZE_KEYS_DK: "List of keys / paths to look for the y **sample** pixel size",
        SAMPLE_DETECTOR_DISTANCE_DK: "List of keys / paths to look for sample to detector distance",
        SOURCE_SAMPLE_DISTANCE_DK: "List of keys / paths to look for source to sample distance",
    }

    # FRAMES TYPE SECTION

    FRAME_TYPE_SECTION_DK = "FRAME_TYPE_SECTION"

    DATA_DK = "data_scans"

    DEFAULT_DATA_COPY_DK = "default_data_copy"

    COMMENTS_FRAME_TYPE_SECTION = {
        FRAME_TYPE_SECTION_DK: "optional section\n"
        "# Allows to define scan to be used for NXTomo conversion\n"
        "# The sequence order will follow the order provided.\n",
        DATA_DK: "list of scans to be converted. Frame type should be "
        "provided for each scan.\n# Expected format is:\n"
        "# * `frame_type` (mandatory): values can be `projection`, `flat`, "
        "`dark`, `alignment` or `init`. \n"
        "# * `entry` (mandatory): DataUrl with path to the scan to integrate. "
        "If the scan is contained in the input_file then you can only provide "
        "path/name of the scan. \n"
        "# * copy (optional): you can provide a different behavior for the "
        "this scan (should we duplicate data or not) \n",
        DEFAULT_DATA_COPY_DK: "You can duplicate data inside the input file or create a link to the original frames. "
        "In this case you should keep the relative position of the files",
    }

    # PCO Tomo specific section
    MULTITOMO_SECTION_DK = "MULTITOMO_SECTION"

    MULTITOMO_START_ANGLE_OFFSET_DK = "start_angle_offset_in_degree"

    MULTITOMO_SCAN_RANGE_DK = "angle_interval_in_degree"

    MULTITOMO_N_NXTOMO_DK = "n_nxtomo"

    MULTITOMO_SHIFT_ANGLES_DK = "shift_angles"

    COMMENTS_MULTITOMO_SECTION = {
        MULTITOMO_SECTION_DK: "pcotomo specific section (handled for first version of the pcotomo: bliss < 1.9)\n",
        MULTITOMO_START_ANGLE_OFFSET_DK: f"If provided then acquisition parameters `nb_loop` and `nb_tomo` will be ignored. Instead `tomo_n` NXtomo will be created from multi-tomo (also aka pcotomo). All angles before `{MULTITOMO_START_ANGLE_OFFSET_DK}` will be ignored",
        MULTITOMO_SCAN_RANGE_DK: f"Angle interval - range to create if '{MULTITOMO_START_ANGLE_OFFSET_DK}' is provided. 180 or 360 is expected",
        MULTITOMO_N_NXTOMO_DK: f"If '{MULTITOMO_START_ANGLE_OFFSET_DK}' provided then specify the number of NXtomo to create. If -1 provided then will create as much NXtomo as possible",
        MULTITOMO_SHIFT_ANGLES_DK: f"shift all angle NXtomo angle to `{MULTITOMO_SCAN_RANGE_DK}` interval by shifting them of {MULTITOMO_START_ANGLE_OFFSET_DK} + {MULTITOMO_SCAN_RANGE_DK}",
    }

    # extra params section

    EXTRA_PARAMS_SECTION_DK = "EXTRA_PARAMS_SECTION"

    EXTRA_PARAMS_ENERGY_DK = "energy_kev"
    EXTRA_PARAMS_ENERGY_DK_ALIASES = ("energy",)
    EXTRA_PARAMS_SAMPLE_X_PIXEL_SIZE_DK = "x_sample_pixel_size_m"
    EXTRA_PARAMS_SAMPLE_X_PIXEL_SIZE_DK_ALIASES = (
        "x_pixel_size",
        "x_sample_pixel_size",
    )
    EXTRA_PARAMS_SAMPLE_Y_PIXEL_SIZE_DK = "y_sample_pixel_size_m"
    EXTRA_PARAMS_SAMPLE_Y_PIXEL_SIZE_DK_ALIASES = (
        "y_pixel_size",
        "y_sample_pixel_size",
    )
    EXTRA_PARAMS_DETECTOR_X_PIXEL_SIZE_DK = "x_detector_pixel_size_m"
    EXTRA_PARAMS_DETECTOR_Y_PIXEL_SIZE_DK = "y_detector_pixel_size_m"
    EXTRA_PARAMS_SAMPLE_DETECTOR_DISTANCE = "detector_sample_distance_m"
    EXTRA_PARAMS_SAMPLE_DETECTOR_DISTANCE_ALIASES = ("detector_sample_distance",)
    EXTRA_PARAMS_SOURCE_SAMPLE_DISTANCE = "source_sample_distance_m"
    EXTRA_PARAMS_SOURCE_SAMPLE_DISTANCE_ALIASES = ("source_sample_distance",)

    EXTRA_PARAMS_DEFAULT_VALID_KEYS = (
        EXTRA_PARAMS_ENERGY_DK,
        EXTRA_PARAMS_SAMPLE_X_PIXEL_SIZE_DK,
        EXTRA_PARAMS_SAMPLE_Y_PIXEL_SIZE_DK,
        EXTRA_PARAMS_DETECTOR_X_PIXEL_SIZE_DK,
        EXTRA_PARAMS_DETECTOR_Y_PIXEL_SIZE_DK,
        EXTRA_PARAMS_SAMPLE_DETECTOR_DISTANCE,
        EXTRA_PARAMS_SOURCE_SAMPLE_DISTANCE,
    )

    EXTRA_PARAMS_VALID_KEYS = (
        *EXTRA_PARAMS_DEFAULT_VALID_KEYS,
        *EXTRA_PARAMS_ENERGY_DK_ALIASES,
        *EXTRA_PARAMS_SAMPLE_X_PIXEL_SIZE_DK_ALIASES,
        *EXTRA_PARAMS_SAMPLE_Y_PIXEL_SIZE_DK_ALIASES,
        *EXTRA_PARAMS_SAMPLE_DETECTOR_DISTANCE_ALIASES,
        *EXTRA_PARAMS_SOURCE_SAMPLE_DISTANCE_ALIASES,
    )

    EXTRA_PARAMS_ALIASES = {
        EXTRA_PARAMS_ENERGY_DK: EXTRA_PARAMS_ENERGY_DK_ALIASES,
        EXTRA_PARAMS_SAMPLE_X_PIXEL_SIZE_DK: EXTRA_PARAMS_SAMPLE_X_PIXEL_SIZE_DK_ALIASES,
        EXTRA_PARAMS_SAMPLE_Y_PIXEL_SIZE_DK: EXTRA_PARAMS_SAMPLE_Y_PIXEL_SIZE_DK_ALIASES,
        EXTRA_PARAMS_SAMPLE_DETECTOR_DISTANCE: EXTRA_PARAMS_SAMPLE_DETECTOR_DISTANCE_ALIASES,
        EXTRA_PARAMS_SOURCE_SAMPLE_DISTANCE: EXTRA_PARAMS_SOURCE_SAMPLE_DISTANCE_ALIASES,
    }

    COMMENTS_EXTRA_PARAMS_SECTION = {
        EXTRA_PARAMS_SECTION_DK: "optional section\n"
        "# you can predefined values which are missing in the input .h5 file\n"
        f"# Handled parameters are {EXTRA_PARAMS_DEFAULT_VALID_KEYS}"
    }

    COMMENTS = COMMENTS_GENERAL_SECTION
    COMMENTS.update(COMMENTS_KEYS_SECTION)
    COMMENTS.update(COMMENTS_ENTRIES_TITLES_SECTION)
    COMMENTS.update(COMMENTS_FRAME_TYPE_SECTION)
    COMMENTS.update(COMMENTS_MULTITOMO_SECTION)
    COMMENTS.update(COMMENTS_EXTRA_PARAMS_SECTION)

    __isfrozen = False
    # to ease API and avoid setting wrong attributes we 'freeze' the attributes
    # see https://stackoverflow.com/questions/3603502/prevent-creating-new-attributes-outside-init

    @staticmethod
    def get_extra_params_default_unit(key) -> str:
        """return the default unit for the extra parameters that can be defined by the user"""
        if key in (
            TomoHDF5Config.EXTRA_PARAMS_SAMPLE_DETECTOR_DISTANCE,
            TomoHDF5Config.EXTRA_PARAMS_SOURCE_SAMPLE_DISTANCE,
            TomoHDF5Config.EXTRA_PARAMS_SAMPLE_X_PIXEL_SIZE_DK,
            TomoHDF5Config.EXTRA_PARAMS_SAMPLE_Y_PIXEL_SIZE_DK,
            TomoHDF5Config.EXTRA_PARAMS_DETECTOR_X_PIXEL_SIZE_DK,
            TomoHDF5Config.EXTRA_PARAMS_DETECTOR_Y_PIXEL_SIZE_DK,
        ):
            return "m"
        elif key in (TomoHDF5Config.EXTRA_PARAMS_ENERGY_DK):
            return "keV"
        else:
            raise ValueError(f"No default unit for {key}")

    def __init__(self):
        super().__init__()
        self._set_freeze(False)
        # general information
        self._input_file = None
        self._raises_error = False
        self._no_input = False
        self._single_file = False
        self._no_master_file = True
        self._bam_single_file = False
        self._handle_machine_current = True
        # a single file is create by default if there is only one entry per file.
        # but we can enfore multi-file writing
        self._ignore_bliss_tomo_config = False
        # on recent ebs tomo (2023) we have a tomo_config group which specify
        # the dataset to use for rotation, translation... if set to True then this group will be ignore
        # and we will fallback on checking the list of provided paths

        # information regarding keys and paths
        self._valid_camera_names = settings.Tomo.H5.VALID_CAMERA_NAMES
        self._rot_angle_keys = settings.Tomo.H5.ROT_ANGLE_KEYS
        self._sample_x_keys = settings.Tomo.H5.SAMPLE_X_KEYS
        self._sample_y_keys = settings.Tomo.H5.SAMPLE_Y_KEYS
        self._translation_z_keys = settings.Tomo.H5.TRANSLATION_Z_KEYS
        self._translation_y_keys = settings.Tomo.H5.TRANSLATION_Y_KEYS
        self._diode_keys = settings.Tomo.H5.DIODE_KEYS
        self._expo_time_keys = settings.Tomo.H5.ACQ_EXPO_TIME_KEYS
        self._sample_detector_distance_keys = (
            settings.Tomo.H5.SAMPLE_DETECTOR_DISTANCE_KEYS
        )
        self._source_sample_distance_keys = settings.Tomo.H5.SOURCE_SAMPLE_DISTANCE_KEYS
        self._machine_current_keys = settings.Tomo.H5.MACHINE_CURRENT_KEYS

        # information regarding titles
        self._entries = None
        self._sub_entries_to_ignore = None
        self._init_titles = settings.Tomo.H5.INIT_TITLES
        self._zserie_init_titles = settings.Tomo.H5.ZSERIE_INIT_TITLES
        self._multitomo_init_titles = settings.Tomo.H5.MULTITOMO_INIT_TITLES
        self._back_and_forth_init_titles = settings.Tomo.H5.BACK_AND_FORTH_INIT_TITLES
        self._dark_titles = settings.Tomo.H5.DARK_TITLES
        self._flat_titles = settings.Tomo.H5.FLAT_TITLES
        self._projection_titles = settings.Tomo.H5.PROJ_TITLES
        self._alignment_titles = settings.Tomo.H5.ALIGNMENT_TITLES
        self._sample_x_pixel_size_paths = settings.Tomo.H5.SAMPLE_X_PIXEL_SIZE_KEYS
        self._sample_y_pixel_size_paths = settings.Tomo.H5.SAMPLE_Y_PIXEL_SIZE_KEYS
        self._detector_x_pixel_size_paths = settings.Tomo.H5.DETECTOR_X_PIXEL_SIZE_KEYS
        self._detector_y_pixel_size_paths = settings.Tomo.H5.DETECTOR_Y_PIXEL_SIZE_KEYS

        # information regarding frames types definition
        self._data_grps_urls = tuple()
        self._default_copy_behavior = False

        # specific information regarding multi-tomo
        self._multitomo_start_angle_offset = None
        # once all the multitomo will be split we can take a sub section of it starting at _multitomo_start_angle and covering _multitomo_angle_interval.
        self._multitomo_scan_range = 360
        # must be in degree. If set to None will go until the end
        self._multitomo_shift_angles = False
        # if True will shift angles of (- _multitomo_start_angle)
        self._multitomo_n_nxtomo = -1
        # how many nx_tomo we want to create if multi-tomo start angle is provided. If set to -1 algorithm will compute how many NXtomo we can create based on scan_range and acquisition rotation_angle

        # should we check for tomo_n contain in the init sequence
        self._check_tomo_n = True

        # extra options
        self._param_already_defined = {}

        self._set_freeze(True)

    @property
    def sample_x_keys(self) -> Iterable:
        return self._sample_x_keys

    @sample_x_keys.setter
    def sample_x_keys(self, keys) -> None:
        if not isinstance(keys, Iterable) or isinstance(keys, str):
            raise TypeError("'keys' should be an Iterable")
        for elmt in keys:
            if not isinstance(elmt, str):
                raise TypeError("keys elmts are expected to be str")
        self._sample_x_keys = keys

    @property
    def sample_y_keys(self) -> Iterable:
        return self._sample_y_keys

    @sample_y_keys.setter
    def sample_y_keys(self, keys) -> None:
        if not isinstance(keys, Iterable) or isinstance(keys, str):
            raise TypeError("'keys' should be an Iterable")
        for elmt in keys:
            if not isinstance(elmt, str):
                raise TypeError("keys elmts are expected to be str")
        self._sample_y_keys = keys

    @property
    def input_file(self) -> str | None:
        return self._input_file

    @input_file.setter
    def input_file(self, input_file: str | None):
        if not isinstance(input_file, (str, type(None))):
            raise TypeError(
                f"'input_file' should be None or an instance of Iterable. Not {type(input_file)}"
            )
        elif input_file in ("", None):
            self._input_file = None
        else:
            if "/mnt/multipath-shares" in input_file:
                # no simple workaround. abspath return a path with '/mnt/multipath-shares'
                _logger.info(
                    "looks like raw data is given with '/mnt/multipath-shares' prefix. Icat will fail on it. Must remove it. No proper other handling found :()"
                )
                # small workaround to fix abspath. Should not be the case anymore so raise an error
                input_file = input_file.replace("/mnt/multipath-shares", "")
            self._input_file = input_file

    @property
    def raises_error(self):
        return self._raises_error

    @raises_error.setter
    def raises_error(self, raises_error: bool):
        if not isinstance(raises_error, bool):
            raise TypeError("'raises_error' should be a boolean")
        self._raises_error = raises_error

    @property
    def no_input(self):
        return self._no_input

    @no_input.setter
    def no_input(self, no_input):
        if not isinstance(no_input, bool):
            raise TypeError("'raises_error' should be a boolean")
        self._no_input = no_input

    @property
    def request_input(self) -> bool:
        return not self._no_input

    @request_input.setter
    def request_input(self, request: bool):
        assert isinstance(request, bool), "request should be a bool"
        self._no_input = not request

    @property
    def single_file(self):
        return self._single_file

    @single_file.setter
    def single_file(self, single_file):
        if not isinstance(single_file, bool):
            raise TypeError("'single_file' should be a boolean")
        self._single_file = single_file

    @property
    def bam_single_file(self):
        return self._bam_single_file

    @bam_single_file.setter
    def bam_single_file(self, bam: bool):
        if not isinstance(bam, bool):
            raise TypeError("'bam' should be a boolean")
        self._bam_single_file = bam

    @property
    def no_master_file(self) -> bool:
        """Option to avoid creating a master file at the end of the conversion"""
        return self._no_master_file

    @no_master_file.setter
    def no_master_file(self, no_master_file: bool) -> None:
        self._no_master_file = no_master_file

    @property
    def handle_machine_current(self):
        return self._handle_machine_current

    @handle_machine_current.setter
    def handle_machine_current(self, handle_machine_current: bool):
        if not isinstance(handle_machine_current, bool):
            raise TypeError("'handle_machine_current' should be a boolean")
        self._handle_machine_current = handle_machine_current

    @property
    def ignore_bliss_tomo_config(self) -> bool:
        return self._ignore_bliss_tomo_config

    @ignore_bliss_tomo_config.setter
    def ignore_bliss_tomo_config(self, ignore: bool):
        assert isinstance(ignore, bool), "ignore is expected to be a boolean"
        self._ignore_bliss_tomo_config = ignore

    # Keys section

    @property
    def valid_camera_names(self) -> tuple | None:
        return self._valid_camera_names

    @valid_camera_names.setter
    def valid_camera_names(self, names: Iterable | None) -> None:
        if names == "None":
            self._valid_camera_names = None
        elif isinstance(names, str):
            raise TypeError("'names' should be None or an instance of Iterable")
        elif not isinstance(names, (Iterable, type(None))):
            raise TypeError("'names' should be None or an instance of Iterable")
        else:
            assert not isinstance(names, str), f"'{names}'"
            self._valid_camera_names = names

    @property
    def translation_y_keys(self) -> str:
        return self._translation_y_keys

    @translation_y_keys.setter
    def translation_y_keys(self, keys) -> None:
        if not isinstance(keys, Iterable) or isinstance(keys, str):
            raise TypeError("'keys' should be an Iterable")
        else:
            for elmt in keys:
                if not isinstance(elmt, str):
                    raise TypeError("keys elmts are expected to be str")
            self._translation_y_keys = keys

    @property
    def diode_keys(self) -> Iterable:
        return self._diode_keys

    @diode_keys.setter
    def diode_keys(self, keys: Iterable) -> None:
        if not isinstance(keys, Iterable):
            raise TypeError("'keys' should be an Iterable")
        self._diode_keys = keys

    @property
    def exposition_time_keys(self) -> Iterable:
        return self._expo_time_keys

    @exposition_time_keys.setter
    def exposition_time_keys(self, keys: Iterable) -> None:
        if not isinstance(keys, Iterable):
            raise TypeError("'keys' should be an Iterable")
        self._expo_time_keys = keys

    # entries section
    @property
    def entries(self) -> tuple | None:
        return self._entries

    @entries.setter
    def entries(self, entries: tuple | None):
        if not isinstance(entries, (type(None), tuple)):
            raise ValueError("entries should be None or an instance of Iterable")
        elif entries is None:
            self._entries = None
        else:
            entries = self._parse_frame_urls(entries)
            entries = tuple([self._fix_entry_name(entry) for entry in entries])
            if len(entries) == 0:
                self._entries = None
            else:
                self._entries = entries

    @staticmethod
    def _fix_entry_name(entry: DataUrl):
        """simple util function to insure the entry start by a "/"""
        if not isinstance(entry, DataUrl):
            raise TypeError("entry is expected to be a DataUrl")
        if not entry.data_path().startswith("/"):
            entry = DataUrl(
                scheme=entry.scheme(),
                data_slice=entry.scheme(),
                file_path=entry.file_path(),
                data_path="/" + entry.data_path(),
            )
        return entry

    @property
    def sub_entries_to_ignore(self) -> tuple | None:
        return self._sub_entries_to_ignore

    @sub_entries_to_ignore.setter
    def sub_entries_to_ignore(self, entries: tuple | None):
        if not isinstance(entries, (type(None), tuple)):
            raise ValueError("entries should be None or an instance of Iterable")
        elif entries is None:
            self._sub_entries_to_ignore = None
        else:
            entries = self._parse_frame_urls(entries)
            entries = tuple([self._fix_entry_name(entry) for entry in entries])
            self._sub_entries_to_ignore = entries

    # titles section
    @property
    def init_titles(self) -> Iterable | None:
        return self._init_titles

    @init_titles.setter
    def init_titles(self, titles: Iterable | None) -> None:
        if titles is None:
            self._init_titles = None
        elif not isinstance(titles, Iterable):
            raise TypeError("'titles' should be None or an Iterable")
        self._init_titles = tuple(titles)

    @property
    def zserie_init_titles(self) -> Iterable | None:
        return self._zserie_init_titles

    @zserie_init_titles.setter
    def zserie_init_titles(self, titles: Iterable | None) -> None:
        if titles is None:
            self._zserie_init_titles = None
        elif not isinstance(titles, Iterable):
            raise TypeError("'titles' should be None or an Iterable")
        self._zserie_init_titles = titles

    @property
    @deprecated(
        replacement="multitomo_init_titles",
        reason="replacement of pcotomo by multitomo",
        since_version="1.2",
    )
    def pcotomo_init_titles(self) -> Iterable | None:
        return self.multitomo_init_titles

    @property
    def multitomo_init_titles(self) -> Iterable | None:
        return self._multitomo_init_titles

    @pcotomo_init_titles.setter
    @deprecated(
        replacement="multitomo_init_titles",
        reason="replacement of pcotomo by multitomo",
        since_version="1.2",
    )
    def pcotomo_init_titles(self, titles: Iterable | None) -> None:
        self.multitomo_init_titles = titles

    @multitomo_init_titles.setter
    def multitomo_init_titles(self, titles: Iterable | None) -> None:
        if titles is None:
            self._multitomo_init_titles = None
        elif not isinstance(titles, Iterable):
            raise TypeError("'titles' should be None or an Iterable")
        self._multitomo_init_titles = titles

    @property
    def back_and_forth_init_titles(self):
        return self._back_and_forth_init_titles

    @back_and_forth_init_titles.setter
    def back_and_forth_init_titles(self, titles: Iterable[str] | None) -> None:
        self._back_and_forth_init_titles = titles

    @property
    def dark_titles(self) -> Iterable | None:
        return self._dark_titles

    @dark_titles.setter
    def dark_titles(self, titles: Iterable | None) -> None:
        if titles is None:
            self._dark_titles = None
        elif not isinstance(titles, Iterable):
            raise TypeError("'titles' should be None or an Iterable")
        self._dark_titles = titles

    @property
    def flat_titles(self) -> Iterable | None:
        return self._flat_titles

    @flat_titles.setter
    def flat_titles(self, titles: Iterable | None) -> None:
        if titles is None:
            self._flat_titles = None
        elif not isinstance(titles, Iterable):
            raise TypeError("'titles' should be None or an Iterable")
        self._flat_titles = titles

    @property
    def projections_titles(self) -> Iterable | None:
        return self._projection_titles

    @projections_titles.setter
    def projections_titles(self, titles: Iterable | None) -> None:
        if titles is None:
            self._projection_titles = None
        elif not isinstance(titles, Iterable):
            raise TypeError("'titles' should be None or an Iterable")
        self._projection_titles = titles

    @property
    def alignment_titles(self) -> Iterable | None:
        return self._alignment_titles

    @alignment_titles.setter
    def alignment_titles(self, titles: Iterable | None) -> None:
        if titles is None:
            self._alignment_titles = None
        elif not isinstance(titles, Iterable):
            raise TypeError("'titles' should be None or an Iterable")
        self._alignment_titles = titles

    @property
    def sample_x_pixel_size_paths(self) -> Iterable:
        return self._sample_x_pixel_size_paths

    @sample_x_pixel_size_paths.setter
    def sample_x_pixel_size_paths(self, paths):
        if not isinstance(paths, Iterable):
            raise TypeError("'paths should be an Iterable")
        self._sample_x_pixel_size_paths = paths

    @property
    def sample_y_pixel_size_paths(self) -> Iterable:
        return self._sample_y_pixel_size_paths

    @sample_y_pixel_size_paths.setter
    def sample_y_pixel_size_paths(self, paths):
        if not isinstance(paths, Iterable):
            raise TypeError("'paths should be an Iterable")
        self._sample_y_pixel_size_paths = paths

    @property
    def detector_x_pixel_size_paths(self) -> Iterable:
        return self._detector_x_pixel_size_paths

    @detector_x_pixel_size_paths.setter
    def detector_x_pixel_size_paths(self, paths):
        if not isinstance(paths, Iterable):
            raise TypeError("'paths should be an Iterable")
        self._detector_x_pixel_size_paths = paths

    @property
    def detector_y_pixel_size_paths(self) -> Iterable:
        return self._detector_y_pixel_size_paths

    @detector_y_pixel_size_paths.setter
    def detector_y_pixel_size_paths(self, paths):
        if not isinstance(paths, Iterable):
            raise TypeError("'paths should be an Iterable")
        self._detector_y_pixel_size_paths = paths

    @property
    def sample_detector_distance_paths(self):
        return self._sample_detector_distance_keys

    @sample_detector_distance_paths.setter
    def sample_detector_distance_paths(self, paths):
        if not isinstance(paths, Iterable):
            raise TypeError("'paths should be an Iterable")
        self._sample_detector_distance_keys = paths

    @property
    def source_sample_distance_paths(self):
        return self._source_sample_distance_keys

    @source_sample_distance_paths.setter
    def source_sample_distance_paths(self, paths):
        if not isinstance(paths, Iterable):
            raise TypeError("'paths should be an Iterable")
        self._source_sample_distance_keys = paths

    # frame type definition

    def _parse_frame_urls(self, urls: tuple):
        """
        Insure urls is None or a list of valid DataUrl
        """
        if urls in ("", None):
            return tuple()
        res = []
        for i_url, url in enumerate(urls):
            if isinstance(url, str):
                if url == "":
                    continue
                elif utils.is_url_path(url):
                    url = DataUrl(path=url)
                else:
                    url = DataUrl(data_path=url, scheme="silx")
            if not isinstance(url, DataUrl):
                raise ValueError(
                    "urls tuple should contains DataUrl. "
                    f"Not {type(url)} at index {i_url}"
                )
            else:
                res.append(url)
        return tuple(res)

    @property
    def data_frame_grps(self) -> tuple:
        return self._data_grps_urls

    @data_frame_grps.setter
    def data_frame_grps(self, frame_grps: tuple):
        for frame_grp in frame_grps:
            if not isinstance(frame_grp, FrameGroup):
                raise TypeError(
                    "frame_grps is expected to contain only "
                    f"instances of FrameGroup. Not {type(frame_grp)}"
                )
        self._data_grps_urls = frame_grps

    @property
    def default_copy_behavior(self) -> bool:
        return self._default_copy_behavior

    @default_copy_behavior.setter
    def default_copy_behavior(self, copy_: bool):
        if not isinstance(copy_, bool):
            raise TypeError("`copy_` should be a boolean")
        else:
            self._default_copy_behavior = copy_

    # pcotomo specific parameters

    @property
    @deprecated(
        since_version="1.2",
        replacement="multitomo_scan_range",
        reason="replacement of pcotomo by multitomo",
    )
    def pcotomo_start_angle_offset(self) -> float:
        return self.multitomo_start_angle_offset

    @property
    def multitomo_start_angle_offset(self) -> float:
        """
        If provided then `nb_loop` and `nb_turn` values will be ignored and splitting will be done as follow:

        * take a subselection of the NXtomo based on pcotomo_start_angle_offset and tomo_n
        * split this sub selection to tomo_n NXtomo
        * shift angle if requested

        Angle is expected to be in degree (when set).
        **The offset is always relative to the first projection angle value**
        """
        return self._multitomo_start_angle_offset

    @pcotomo_start_angle_offset.setter
    @property
    @deprecated(
        since_version="1.2",
        replacement="multitomo_scan_range",
        reason="replacement of pcotomo by multitomo",
    )
    def pcotomo_start_angle_offset(self, start_angle: float | None) -> None:
        self.multitomo_start_angle_offset = start_angle

    @multitomo_start_angle_offset.setter
    def multitomo_start_angle_offset(self, start_angle: float | None) -> None:
        if start_angle is None:
            self._multitomo_start_angle_offset = None
        else:
            self._multitomo_start_angle_offset = float(start_angle)

    @property
    @deprecated(
        since_version="1.2",
        replacement="multitomo_scan_range",
        reason="replacement of pcotomo by multitomo",
    )
    def pcotomo_scan_range(self) -> float | None:
        return self.multitomo_scan_range

    @property
    def multitomo_scan_range(self) -> float | None:
        """
        if we want to take a subset of the NXtomo for the multitomo we can define an interval.
        Interval must be in degree.
        If None we expect to take the full interval.
        """
        return self._multitomo_scan_range

    @pcotomo_scan_range.setter
    @deprecated(
        since_version="1.2",
        replacement="multitomo_scan_range",
        reason="replacement of pcotomo by multitomo",
    )
    def pcotomo_scan_range(self, interval: float | None):
        self.multitomo_scan_range = interval

    @multitomo_scan_range.setter
    def multitomo_scan_range(self, interval: float | None):
        if interval is None:
            self._multitomo_scan_range = None
        else:
            self._multitomo_scan_range = float(interval)

    @property
    @deprecated(
        since_version="1.2",
        replacement="multitomo_shift_angles",
        reason="replacement of pcotomo by multitomo",
    )
    def pcotomo_shift_angles(self) -> bool:
        return self.multitomo_shift_angles

    @property
    def multitomo_shift_angles(self):
        return self._multitomo_shift_angles

    @pcotomo_shift_angles.setter
    @deprecated(
        since_version="1.2",
        replacement="multitomo_shift_angles",
        reason="replacement of pcotomo by multitomo",
    )
    def pcotomo_shift_angles(self, shift: bool):
        self.multitomo_shift_angles = shift

    @multitomo_shift_angles.setter
    def multitomo_shift_angles(self, shift: bool):
        if not isinstance(shift, bool):
            raise TypeError(f"Shift is expected to be a bool. Not {type(shift)}")
        self._multitomo_shift_angles = shift

    @property
    @deprecated(
        since_version="1.2",
        replacement="multitomo_n_nxtomo",
        reason="replacement of pcotomo by multitomo",
    )
    def pcotomo_n_nxtomo(self) -> int:
        return self.multitomo_n_nxtomo

    @property
    def multitomo_n_nxtomo(self) -> int:
        return self._multitomo_n_nxtomo

    @pcotomo_n_nxtomo.setter
    @deprecated(
        since_version="1.2",
        replacement="multitomo_n_nxtomo",
        reason="replacement of pcotomo by multitomo",
    )
    def pcotomo_n_nxtomo(self, n_nxtomo: int):
        self.multitomo_n_nxtomo = n_nxtomo

    @multitomo_n_nxtomo.setter
    def multitomo_n_nxtomo(self, n_nxtomo: int):
        if not isinstance(n_nxtomo, int):
            raise TypeError(
                f"tomo_n is expected to be a int when {type(n_nxtomo)} provided"
            )
        self._multitomo_n_nxtomo = n_nxtomo

    # parameters already defined

    @property
    def param_already_defined(self) -> dict:
        return self._param_already_defined

    @param_already_defined.setter
    def param_already_defined(self, params: dict):
        if not isinstance(params, dict):
            raise TypeError("dict expected")
        else:
            self._param_already_defined = params

    # utils functions

    @property
    def is_using_titles(self) -> bool:
        return not self.is_using_urls

    @property
    def is_using_urls(self) -> bool:
        """
        Return true if we want to use urls for darks, flats, projections
        instead of titles
        """
        return not (len(self.data_frame_grps) == 0)

    @property
    def check_tomo_n(self):
        return self._check_tomo_n

    @check_tomo_n.setter
    def check_tomo_n(self, check: bool):
        if not isinstance(check, bool):
            raise TypeError("'check' is expected to be a boolean")
        self._check_tomo_n = check

    def clear_titles(self):
        """
        set all titles to empty tuple
        """
        self.dark_titles = tuple()
        self.flat_titles = tuple()
        self.projections_titles = tuple()
        self.alignment_titles = tuple()

    def clear_entries_and_subentries(self):
        """
        clear entries and sub_entries_to_ignore
        """
        self.entries = None
        self.sub_entries_to_ignore = None

    # to_dict / from_dict functions

    def to_dict(self) -> dict:
        """convert the configuration to a dictionary"""
        return {
            self.GENERAL_SECTION_DK: {
                self.INPUT_FILE_DK: self.input_file or "",
                self.OUTPUT_FILE_DK: self.output_file or "",
                self.OVERWRITE_DK: self.overwrite,
                self.FILE_EXTENSION_DK: self.file_extension.value,
                self.LOG_LEVEL_DK: logging.getLevelName(self.log_level).lower(),
                self.RAISES_ERROR_DK: self.raises_error,
                self.NO_INPUT_DK: self.no_input,
                self.SINGLE_FILE_DK: self.single_file,
                self.NO_MASTER_FILE_DK: self.no_master_file,
                self.IGNORE_BLISS_TOMO_CONFIG: self._ignore_bliss_tomo_config,
                self.FIELD_OF_VIEW_DK: (
                    self.field_of_view.value if self.field_of_view else ""
                ),
                self.HANDLE_MACHINE_CURRENT: self.handle_machine_current,
            },
            self.KEYS_SECTION_DK: {
                TomoHDF5Config.VALID_CAMERA_DK: self.valid_camera_names or "",
                TomoHDF5Config.ROT_ANGLE_DK: self.rotation_angle_keys,
                TomoHDF5Config.SAMPLE_X_KEYS_DK: self.sample_x_keys,
                TomoHDF5Config.SAMPLE_Y_KEYS_DK: self.sample_y_keys,
                TomoHDF5Config.TRANSLATION_Z_KEYS_DK: self.translation_z_keys,
                TomoHDF5Config.TRANSLATION_Y_KEYS_DK: self.translation_y_keys,
                TomoHDF5Config.DIODE_KEYS_DK: self.diode_keys,
                TomoHDF5Config.ACQUISITION_EXPO_TIME_KEYS_DK: self.exposition_time_keys,
                TomoHDF5Config.SAMPLE_X_PIXEL_SIZE_KEYS_DK: self.sample_x_pixel_size_paths,
                TomoHDF5Config.SAMPLE_Y_PIXEL_SIZE_KEYS_DK: self.sample_y_pixel_size_paths,
                TomoHDF5Config.DETECTOR_X_PIXEL_SIZE_KEYS_DK: self.detector_x_pixel_size_paths,
                TomoHDF5Config.DETECTOR_Y_PIXEL_SIZE_KEYS_DK: self.detector_y_pixel_size_paths,
                TomoHDF5Config.SAMPLE_DETECTOR_DISTANCE_DK: self.sample_detector_distance_paths,
                TomoHDF5Config.SOURCE_SAMPLE_DISTANCE_DK: self.source_sample_distance_paths,
            },
            self.ENTRIES_AND_TITLES_SECTION_DK: {
                TomoHDF5Config.ENTRIES_DK: self.entries or "",
                TomoHDF5Config.SUB_ENTRIES_TO_IGNORE: self.sub_entries_to_ignore or "",
                TomoHDF5Config.INIT_TITLES_DK: self.init_titles or "",
                TomoHDF5Config.ZSERIE_INIT_TITLES_DK: self.zserie_init_titles or "",
                TomoHDF5Config.MULTITOMO_INIT_TITLES_DK: self.multitomo_init_titles
                or "",
                TomoHDF5Config.DARK_TITLES_DK: self.dark_titles or "",
                TomoHDF5Config.FLAT_TITLES_DK: self.flat_titles or "",
                TomoHDF5Config.PROJ_TITLES_DK: self.projections_titles or "",
                TomoHDF5Config.ALIGNMENT_TITLES_DK: self.alignment_titles or "",
            },
            self.FRAME_TYPE_SECTION_DK: {
                TomoHDF5Config.DATA_DK: FrameGroup.list_to_str(self.data_frame_grps),
                TomoHDF5Config.DEFAULT_DATA_COPY_DK: self.default_copy_behavior,
            },
            self.MULTITOMO_SECTION_DK: {
                TomoHDF5Config.MULTITOMO_START_ANGLE_OFFSET_DK: self.multitomo_start_angle_offset,
                TomoHDF5Config.MULTITOMO_N_NXTOMO_DK: self.multitomo_n_nxtomo,
                TomoHDF5Config.MULTITOMO_SCAN_RANGE_DK: self.multitomo_scan_range,
                TomoHDF5Config.MULTITOMO_SHIFT_ANGLES_DK: self.multitomo_shift_angles,
            },
            self.EXTRA_PARAMS_SECTION_DK: self._param_already_defined,
        }

    @staticmethod
    def from_dict(dict_: dict):
        r"""
        Create a HDF5Config object and set it from values contained in the
        dictionary
        :param\_: settings dictionary
        :return: HDF5Config
        """
        config = TomoHDF5Config()
        config.load_from_dict(dict_)
        return config

    def load_from_dict(self, dict_: dict) -> None:
        """Load the configuration from a dictionary"""
        # Convert keys to upper case (expected to be section names: always in ipper case)
        dict_ = {key.upper(): value for key, value in dict_.items()}

        # general section
        if TomoHDF5Config.GENERAL_SECTION_DK in dict_:
            self.load_general_section(dict_[TomoHDF5Config.GENERAL_SECTION_DK])
        else:
            _logger.error(f"No {TomoHDF5Config.GENERAL_SECTION_DK} section found")

        # keys section
        if TomoHDF5Config.KEYS_SECTION_DK in dict_:
            self.load_keys_section(dict_[TomoHDF5Config.KEYS_SECTION_DK])
        else:
            mess = f"No {TomoHDF5Config.KEYS_SECTION_DK} section found"
            if TomoHDF5Config.ENTRIES_AND_TITLES_SECTION_DK not in dict_:
                _logger.error(mess)
            else:
                _logger.info(mess)

        # entries and titles section
        if TomoHDF5Config.ENTRIES_AND_TITLES_SECTION_DK in dict_:
            self.load_entries_titles_section(
                dict_[TomoHDF5Config.ENTRIES_AND_TITLES_SECTION_DK]
            )
        else:
            mess = f"No {TomoHDF5Config.ENTRIES_AND_TITLES_SECTION_DK} section found"
            if TomoHDF5Config.KEYS_SECTION_DK not in dict_:
                _logger.error(mess)
            else:
                _logger.info(mess)

        # frame type section
        if TomoHDF5Config.FRAME_TYPE_SECTION_DK in dict_:
            self.load_frame_type_section(dict_[TomoHDF5Config.FRAME_TYPE_SECTION_DK])
        else:
            _logger.error(f"No {TomoHDF5Config.FRAME_TYPE_SECTION_DK} section found")

        if TomoHDF5Config.MULTITOMO_SECTION_DK in dict_:
            self.load_multitomo_section(
                dict_.get(
                    TomoHDF5Config.MULTITOMO_SECTION_DK,
                    dict_.get(
                        "PCOTOMO_SECTION", {}
                    ),  # backward compatibility for nxtomomill < 1.2
                )
            )
        else:
            _logger.info(f"No {TomoHDF5Config.MULTITOMO_SECTION_DK} section found")

        # extra params section
        if TomoHDF5Config.EXTRA_PARAMS_SECTION_DK in dict_:
            self.load_extra_params_section(
                dict_[TomoHDF5Config.EXTRA_PARAMS_SECTION_DK]
            )
        else:
            _logger.error(f"No {TomoHDF5Config.EXTRA_PARAMS_SECTION_DK} section found")

    def load_general_section(self, dict_):
        self.input_file = dict_.get(TomoHDF5Config.INPUT_FILE_DK, None)
        self.output_file = dict_.get(TomoHDF5Config.OUTPUT_FILE_DK, None)
        overwrite = dict_.get(TomoHDF5Config.OVERWRITE_DK, None)
        if overwrite is not None:
            self.overwrite = utils.convert_str_to_bool(overwrite)
        file_extension = dict_.get(TomoHDF5Config.FILE_EXTENSION_DK, None)
        if file_extension is not None:
            self.file_extension = utils.filter_str_def(file_extension)
        log_level = dict_.get(TomoHDF5Config.LOG_LEVEL_DK, None)
        if log_level is not None:
            self.log_level = log_level
        raises_error = dict_.get(TomoHDF5Config.RAISES_ERROR_DK, None)
        if raises_error is not None:
            self.raises_error = utils.convert_str_to_bool(raises_error)
        no_input = dict_.get(TomoHDF5Config.NO_INPUT_DK, None)
        if no_input is not None:
            self.no_input = utils.convert_str_to_bool(no_input)
        single_file = dict_.get(TomoHDF5Config.SINGLE_FILE_DK, None)
        if single_file is not None:
            self.single_file = utils.convert_str_to_bool(single_file)
        handle_machine_current = dict_.get(TomoHDF5Config.HANDLE_MACHINE_CURRENT, None)
        no_master_file = dict_.get(TomoHDF5Config.NO_MASTER_FILE_DK, None)
        if no_master_file is not None:
            self.no_master_file = utils.convert_str_to_bool(no_master_file)
        if handle_machine_current is not None:
            self.handle_machine_current = utils.convert_str_to_bool(
                handle_machine_current
            )
        ignore_bliss_tomo_config = dict_.get(
            TomoHDF5Config.IGNORE_BLISS_TOMO_CONFIG, None
        )
        if ignore_bliss_tomo_config is not None:
            self._ignore_bliss_tomo_config = utils.convert_str_to_bool(
                ignore_bliss_tomo_config
            )
        field_of_view = dict_.get(TomoHDF5Config.FIELD_OF_VIEW_DK, None)
        if field_of_view is not None:
            if field_of_view == "":
                field_of_view = None
            self.field_of_view = field_of_view

    def load_keys_section(self, dict_):
        # handle valid camera names. empty string is consider as a valid value
        valid_camera_names = dict_.get(TomoHDF5Config.VALID_CAMERA_DK, None)
        if valid_camera_names in ("", "none", "None", None):
            valid_camera_names = None
        else:
            valid_camera_names = utils.convert_str_to_tuple(
                valid_camera_names, none_if_empty=True
            )
        self.valid_camera_names = valid_camera_names
        # handle rotation angles.
        rotation_angle_keys = dict_.get(TomoHDF5Config.ROT_ANGLE_DK, None)
        if rotation_angle_keys is not None:
            rotation_angle_keys = utils.convert_str_to_tuple(
                rotation_angle_keys, none_if_empty=True
            )
            self.rotation_angle_keys = rotation_angle_keys
        # handle x translation
        sample_x_keys = dict_.get(TomoHDF5Config.SAMPLE_X_KEYS_DK, None)
        if sample_x_keys is not None:
            sample_x_keys = utils.convert_str_to_tuple(
                sample_x_keys, none_if_empty=True
            )
            self.sample_x_keys = sample_x_keys
        # handle y translation
        sample_y_keys = dict_.get(TomoHDF5Config.SAMPLE_Y_KEYS_DK, None)
        if sample_y_keys is not None:
            sample_y_keys = utils.convert_str_to_tuple(
                sample_y_keys, none_if_empty=True
            )
            self.sample_y_keys = sample_y_keys
        # handle z translation
        translation_z_keys = dict_.get(TomoHDF5Config.TRANSLATION_Z_KEYS_DK, None)
        if translation_z_keys is not None:
            translation_z_keys = utils.convert_str_to_tuple(
                translation_z_keys, none_if_empty=True
            )
            self.translation_z_keys = translation_z_keys
        # handle y rotation keys
        translation_y_keys = dict_.get(TomoHDF5Config.TRANSLATION_Y_KEYS_DK, None)
        if translation_y_keys is not None:
            translation_y_keys = utils.convert_str_to_tuple(
                translation_y_keys, none_if_empty=True
            )
            self.translation_y_keys = translation_y_keys
        # handle diode keys
        diode_keys = dict_.get(TomoHDF5Config.DIODE_KEYS_DK, None)
        if diode_keys is not None:
            diode_keys = utils.convert_str_to_tuple(diode_keys, none_if_empty=True)
            self.diode_keys = diode_keys
        # handle exposure time
        exposition_time_keys = dict_.get(
            TomoHDF5Config.ACQUISITION_EXPO_TIME_KEYS_DK, None
        )
        if exposition_time_keys is not None:
            exposition_time_keys = utils.convert_str_to_tuple(
                exposition_time_keys, none_if_empty=True
            )
            self.exposition_time_keys = exposition_time_keys
        # handle x sample pixel paths
        x_sample_pixel_size_paths = dict_.get(
            TomoHDF5Config.SAMPLE_X_PIXEL_SIZE_KEYS_DK, None
        )
        if x_sample_pixel_size_paths is not None:
            x_sample_pixel_size_paths = utils.convert_str_to_tuple(
                x_sample_pixel_size_paths, none_if_empty=True
            )
            self.sample_x_pixel_size_paths = x_sample_pixel_size_paths
        # handle y sample pixel paths
        y_sample_pixel_size_paths = dict_.get(
            TomoHDF5Config.SAMPLE_Y_PIXEL_SIZE_KEYS_DK, None
        )
        if y_sample_pixel_size_paths is not None:
            y_sample_pixel_size_paths = utils.convert_str_to_tuple(
                y_sample_pixel_size_paths, none_if_empty=True
            )
            self.sample_y_pixel_size_paths = y_sample_pixel_size_paths
        # handle x detector pixel paths
        x_detector_pixel_size_paths = dict_.get(
            TomoHDF5Config.DETECTOR_X_PIXEL_SIZE_KEYS_DK, None
        )
        if x_detector_pixel_size_paths is not None:
            x_detector_pixel_size_paths = utils.convert_str_to_tuple(
                x_detector_pixel_size_paths, none_if_empty=True
            )
            self.detector_x_pixel_size_paths = x_detector_pixel_size_paths
        # handle y detector pixel paths
        y_detector_pixel_size_paths = dict_.get(
            TomoHDF5Config.DETECTOR_Y_PIXEL_SIZE_KEYS_DK, None
        )
        if y_detector_pixel_size_paths is not None:
            y_detector_pixel_size_paths = utils.convert_str_to_tuple(
                y_detector_pixel_size_paths, none_if_empty=True
            )
            self.detector_y_pixel_size_paths = y_detector_pixel_size_paths
        # handle sample detector distance paths
        sample_detector_distance_paths = dict_.get(
            TomoHDF5Config.SAMPLE_DETECTOR_DISTANCE_DK, None
        )
        if sample_detector_distance_paths is not None:
            sample_detector_distance_paths = utils.convert_str_to_tuple(
                sample_detector_distance_paths, none_if_empty=True
            )
            self.sample_detector_distance_paths = sample_detector_distance_paths
        # handle source to sample distance paths
        source_sample_distance_paths = dict_.get(
            TomoHDF5Config.SOURCE_SAMPLE_DISTANCE_DK, None
        )
        if source_sample_distance_paths is not None:
            source_sample_distance_paths = utils.convert_str_to_tuple(
                source_sample_distance_paths, none_if_empty=True
            )
            self.source_sample_distance_paths = source_sample_distance_paths

    def load_entries_titles_section(self, dict_):
        # handle entries to convert
        entries = dict_.get(TomoHDF5Config.ENTRIES_DK)
        if entries is not None:
            entries = utils.convert_str_to_tuple(entries, none_if_empty=True)
            self.entries = entries
        # handle init titles. empty string is consider as a valid value
        init_titles = dict_.get(TomoHDF5Config.INIT_TITLES_DK, None)
        if init_titles is not None:
            init_titles = utils.convert_str_to_tuple(init_titles, none_if_empty=True)
            self.init_titles = init_titles
        # handle zserie init titles. empty string is consider as a valid value
        zserie_init_titles = dict_.get(TomoHDF5Config.ZSERIE_INIT_TITLES_DK, None)
        if zserie_init_titles is not None:
            zserie_init_titles = utils.convert_str_to_tuple(
                zserie_init_titles,
                none_if_empty=True,
            )
            self.zserie_init_titles = zserie_init_titles

        # handle multi-tomo init titles
        multitomo_init_titles = dict_.get(TomoHDF5Config.MULTITOMO_INIT_TITLES_DK, None)
        if multitomo_init_titles is not None:
            multitomo_init_titles = utils.convert_str_to_tuple(
                multitomo_init_titles,
                none_if_empty=True,
            )
            self.multitomo_init_titles = multitomo_init_titles
        # handle dark titles. empty string is consider as a valid value
        dark_titles = dict_.get(TomoHDF5Config.DARK_TITLES_DK, None)
        if dark_titles is not None:
            dark_titles = utils.convert_str_to_tuple(dark_titles, none_if_empty=True)
            self.dark_titles = dark_titles
        # handle ref titles. empty string is consider as a valid value
        flat_titles_dks = [
            TomoHDF5Config.FLAT_TITLES_DK,
        ]
        flat_titles_dks.extend(TomoHDF5Config.FLAT_TILES_ALIASES)
        flat_title_key_picked = None
        # handle flat titles
        for alias in flat_titles_dks:
            flat_titles = dict_.get(alias, None)
            if flat_titles is not None:
                if flat_title_key_picked is not None:
                    _logger.warning(
                        f"flat titles are provided twice under {flat_title_key_picked} and {alias}. Please clean your configuration file. {flat_title_key_picked} will be used"
                    )
                else:
                    flat_titles = utils.convert_str_to_tuple(
                        flat_titles, none_if_empty=True
                    )
                    self.flat_titles = flat_titles
                    flat_title_key_picked = alias
        if (
            flat_title_key_picked is not None
            and flat_title_key_picked != TomoHDF5Config.FLAT_TITLES_DK
        ):
            _logger.warning(
                f"{flat_title_key_picked} will be removed in the future. Please use {TomoHDF5Config.FLAT_TITLES_DK} instead"
            )
        # handle projection titles. empty string is consider as a valid value
        proj_titles = dict_.get(TomoHDF5Config.PROJ_TITLES_DK, None)
        if proj_titles is not None:
            proj_titles = utils.convert_str_to_tuple(proj_titles, none_if_empty=True)
            self.projections_titles = proj_titles
        # handle alignment titles. empty string is consider as a valid value
        alignment_titles = dict_.get(TomoHDF5Config.ALIGNMENT_TITLES_DK, None)
        if alignment_titles is not None:
            alignment_titles = utils.convert_str_to_tuple(
                alignment_titles, none_if_empty=True
            )
            self.alignment_titles = alignment_titles

    def load_frame_type_section(self, dict_):
        # urls
        data_urls = dict_.get(TomoHDF5Config.DATA_DK, None)
        if data_urls is not None:
            data_urls = utils.convert_str_to_frame_grp(data_urls)
            self.data_frame_grps = data_urls
        default_copy_behavior = dict_.get(TomoHDF5Config.DEFAULT_DATA_COPY_DK, None)
        if default_copy_behavior is not None:
            self.default_copy_behavior = default_copy_behavior == "True"

    @deprecated(
        since_version="1.2",
        reason="rename pcotomo to multitomo",
        replacement="load_multitomo_section",
    )
    def load_pcotomo_section(self, dict_):
        return self.load_multitomo_section(dict_=dict_)

    def load_multitomo_section(self, dict_):
        multitomo_start_angle_offset = dict_.get(
            TomoHDF5Config.MULTITOMO_START_ANGLE_OFFSET_DK, None
        )
        if multitomo_start_angle_offset not in (None, "None", "none", "NONE"):
            self.multitomo_start_angle_offset = float(multitomo_start_angle_offset)
        if TomoHDF5Config.MULTITOMO_SCAN_RANGE_DK in dict_:
            multitomo_angle_interval = dict_.get(TomoHDF5Config.MULTITOMO_SCAN_RANGE_DK)
            if multitomo_angle_interval in (None, "None", "none", "NONE"):
                self.multitomo_scan_range = None
            else:
                self.multitomo_scan_range = multitomo_angle_interval
        if TomoHDF5Config.MULTITOMO_N_NXTOMO_DK in dict_:
            multitomo_tomo_n = dict_.get(TomoHDF5Config.MULTITOMO_N_NXTOMO_DK)
            if multitomo_tomo_n not in ("", None, "None", "none", "NONE"):
                self.multitomo_n_nxtomo = int(multitomo_tomo_n)
        multitomo_shift_angles = dict_.get(
            TomoHDF5Config.MULTITOMO_SHIFT_ANGLES_DK, None
        )
        if multitomo_shift_angles is not None:
            if multitomo_shift_angles in (True, "True"):
                self.multitomo_shift_angles = True
            elif multitomo_shift_angles in (False, "False"):
                self.multitomo_shift_angles = False

    def load_extra_params_section(self, dict_):
        for key, value in dict_.items():
            if key in TomoHDF5Config.EXTRA_PARAMS_VALID_KEYS:
                self._param_already_defined.update({key: value})
            else:
                _logger.warning(f"{key} is not a handled key")

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
            comments_fct=TomoHDF5Config.get_comments,
            logger=_logger,
        )

    @staticmethod
    def from_cfg_file(file_path: str, encoding=None):
        assert file_path is not None, "file_path should not be None"
        config_parser = configparser.ConfigParser(allow_no_value=True)
        config_parser.read(file_path, encoding=encoding)
        return TomoHDF5Config.from_dict(config_parser)

    @staticmethod
    def get_comments(key):
        return TomoHDF5Config.COMMENTS[key]


def generate_default_h5_config() -> dict:
    """generate a default configuration for converting hdf5 to nx"""
    return TomoHDF5Config().to_dict()
