# coding: utf-8

from __future__ import annotations

import configparser
import logging

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

_logger = logging.getLogger(__name__)


__all__ = ["TomoFluoConfig", "generate_default_fluo_config"]


class TomoFluoConfig(ConfigBase, ConfigSourceSection):
    """
    Configuration class to provide to the fluo->nx converter .
    """

    # General section keys

    GENERAL_SECTION_DK = "GENERAL_SECTION"

    INPUT_FOLDER_DK = "input_folder"

    OUTPUT_FILE_DK = "output_file"

    DETECTOR_NAMES_DK = "detector_names"

    DIMENSION_DK = "dimension"

    FILE_EXTENSION_DK = "file_extension"

    OVERWRITE_DK = "overwrite"

    DATASET_BASENAME_DK = "dataset_basename"

    DATASET_FILE_INFO_DK = "dataset_info_file"

    LOG_LEVEL_DK = "log_level"

    TITLE_DK = "title"

    IGNORE_FILE_PATTERN_DK = "patterns_to_ignores"

    DUPLICATE_DATA_DK = "duplicate_data"

    EXTERNAL_LINK_RELATIVE_DK = "external_link_path"

    COMMENTS_GENERAL_SECTION = {
        GENERAL_SECTION_DK: "general information. \n",
        INPUT_FOLDER_DK: "Path to the folder containing the raw data folder and the fluofit/ subfolder. if not provided from the configuration file must be provided from the command line",
        OUTPUT_FILE_DK: "File produced by the converter. '.nx' extension recommended. If not provided from the configuration file must be provided from the command line",
        DIMENSION_DK: "Dimension of the experiment. 2 for 2D XRFCT, 3 for 3D XRFCT. Default is 3.",
        DETECTOR_NAMES_DK: "Define a list of (real or virtual) detector names used for the exp (space separated values - no comma). E.g. 'falcon xmap'. If not specified, all detectors are processed.",
        OVERWRITE_DK: "overwrite output files if exists without asking",
        FILE_EXTENSION_DK: "file extension. Ignored if the output file is provided and contains an extension",
        DATASET_BASENAME_DK: f"In 2D, the exact full name of the folder. In 3D, the folder name prefix (the program will search for folders named <prefix>_XXX where XXX is a nmber.) If not provided will take the name of {INPUT_FOLDER_DK}",
        DATASET_FILE_INFO_DK: f"path to .info file containing dataset information (Energy, ScanRange, TOMO_N...). If not will deduce it from {DATASET_BASENAME_DK}",
        LOG_LEVEL_DK: 'Log level. Valid levels are "debug", "info", "warning" and "error"',
        TITLE_DK: "NXtomo title",
        IGNORE_FILE_PATTERN_DK: "some file pattern leading to ignoring the file. Like reconstructed slice files.",
        DUPLICATE_DATA_DK: "If False then will create embed all the data into a single file avoiding external link to other file. If True then the decetor data will point to original tif files. In this case you must be carreful to keep relative paths valid. Warning: to read external dataset you nust be at the hdf5 file working directory. See external link resolution details: https://support.hdfgroup.org/documentation/hdf5/latest/group___h5_l.html#title5",
        EXTERNAL_LINK_RELATIVE_DK: "If 'duplicate_data' is set to False then you can specify if you want the link to original files to be 'relative' or 'absolute'",
    }

    LEVEL_GENERAL_SECTION = {
        INPUT_FOLDER_DK: OptionLevel.REQUIRED,
        OUTPUT_FILE_DK: OptionLevel.REQUIRED,
        DIMENSION_DK: OptionLevel.REQUIRED,
        DETECTOR_NAMES_DK: OptionLevel.REQUIRED,
        OVERWRITE_DK: OptionLevel.REQUIRED,
        FILE_EXTENSION_DK: OptionLevel.ADVANCED,
        DATASET_BASENAME_DK: OptionLevel.REQUIRED,
        DATASET_FILE_INFO_DK: OptionLevel.REQUIRED,
        LOG_LEVEL_DK: OptionLevel.REQUIRED,
        TITLE_DK: OptionLevel.ADVANCED,
        IGNORE_FILE_PATTERN_DK: OptionLevel.REQUIRED,
        DUPLICATE_DATA_DK: OptionLevel.REQUIRED,
        EXTERNAL_LINK_RELATIVE_DK: OptionLevel.ADVANCED,
    }

    # create comments

    COMMENTS = COMMENTS_GENERAL_SECTION
    COMMENTS.update(ConfigSourceSection.COMMENTS_SOURCE_SECTION_DK)

    SECTIONS_LEVEL = {
        GENERAL_SECTION_DK: OptionLevel.REQUIRED,
        ConfigSourceSection.SOURCE_SECTION_DK: OptionLevel.ADVANCED,
    }

    def __init__(self):
        super().__init__()
        self._set_freeze(False)
        # general information
        self._input_folder = None
        self._output_file = None
        self._dimension: int = 3
        self._detectors: tuple[str] = tuple()
        self._file_extension = FileExtension.NX
        self._overwrite = False
        self._dataset_basename = None
        self._log_level = logging.WARNING
        self._title = None
        self._ignore_file_patterns = Tomo.EDF.TO_IGNORE
        self._dataset_info_file = None
        self._duplicate_data = True
        self._external_path_type = PathType.RELATIVE

        # source
        self._instrument_name = None
        self._source_name = "ESRF"
        self._source_type = SourceType.SYNCHROTRON_X_RAY_SOURCE
        self._source_probe = ProbeType.X_RAY

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
    def dimension(self) -> int:
        return self._dimension

    @dimension.setter
    def dimension(self, dimension: int):
        self._dimension = int(dimension)

    @property
    def detectors(self) -> list:

        return self._detectors

    @detectors.setter
    def detectors(self, dets: tuple | str):
        self._detectors = convert_str_to_tuple(dets)

    @property
    def dataset_basename(self) -> str | None:
        return self._dataset_basename

    @dataset_basename.setter
    def dataset_basename(self, dataset_basename: str | None) -> None:
        if not isinstance(dataset_basename, (type(None), str)):
            raise TypeError(
                f"Dataset_basename is expected to be None or an instance of str. Not {type(dataset_basename)}"
            )
        self._dataset_basename = dataset_basename

    @property
    def dataset_info_file(self) -> str | None:
        return self._dataset_info_file

    @dataset_info_file.setter
    def dataset_info_file(self, file_path: str | None) -> None:
        if not isinstance(file_path, (type(None), str)):
            raise TypeError(
                f"info.file path is expected to be None or an instance of str. Not {type(file_path)}"
            )
        self._dataset_info_file = file_path

    @property
    def duplicate_data(self) -> bool:
        return self._duplicate_data

    @duplicate_data.setter
    def duplicate_data(self, duplicate: bool):
        if not isinstance(duplicate, bool):
            raise TypeError(
                f"Duplicate is expected to be a bool and not {type(duplicate)}"
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
            self.SOURCE_SECTION_DK: self._source_section_to_dict,
        }
        res = {}
        for section, callback in sections_callback.items():
            if (
                level == OptionLevel.ADVANCED
                or TomoFluoConfig.SECTIONS_LEVEL[section] == OptionLevel.REQUIRED
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
            self.DIMENSION_DK: (self.dimension if self.dimension is not None else ""),
            self.DETECTOR_NAMES_DK: (
                self.detectors if self.detectors is not None else ""
            ),
            self.OVERWRITE_DK: self.overwrite,
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
            dict_=res, level=level, level_ref=TomoFluoConfig.LEVEL_GENERAL_SECTION
        )

    @staticmethod
    def from_dict(dict_: dict):
        r"""
        Create a HDF5Config object and set it from values contained in the
        dictionary
        :param dict\_: settings dictionary
        :return: HDF5Config
        """
        config = TomoFluoConfig()
        config.load_from_dict(dict_)
        return config

    def load_from_dict(self, dict_: dict) -> None:
        """Load the configuration from a dictionary"""
        sections_loaders = {
            TomoFluoConfig.GENERAL_SECTION_DK: self.load_general_section,
            TomoFluoConfig.SOURCE_SECTION_DK: self.load_source_section,
        }
        for section_key, loaded_func in sections_loaders.items():
            if section_key in dict_:
                loaded_func(dict_[section_key])
            else:
                _logger.info(
                    f"No {section_key} section found. Will take default values"
                )

    def load_general_section(self, dict_: dict) -> None:
        self.input_folder = dict_.get(TomoFluoConfig.INPUT_FOLDER_DK, None)
        self.output_file = dict_.get(TomoFluoConfig.OUTPUT_FILE_DK, None)
        self.detectors = dict_.get(TomoFluoConfig.DETECTOR_NAMES_DK, None)
        self.dimension = dict_.get(TomoFluoConfig.DIMENSION_DK, 3)
        if self.detectors is not None:
            if self.detectors == "":
                self.detectors = None

        overwrite = dict_.get(TomoFluoConfig.OVERWRITE_DK, None)
        if overwrite is not None:
            self.overwrite = convert_str_to_bool(overwrite)

        file_extension = dict_.get(TomoFluoConfig.FILE_EXTENSION_DK, None)
        if file_extension not in (None, ""):
            self.file_extension = filter_str_def(file_extension)

        dataset_basename = dict_.get(TomoFluoConfig.DATASET_BASENAME_DK, None)
        if dataset_basename is not None:
            if dataset_basename == "":
                dataset_basename = None
            self.dataset_basename = dataset_basename

        dataset_info_file = dict_.get(TomoFluoConfig.DATASET_FILE_INFO_DK, None)
        if dataset_info_file is not None:
            if dataset_info_file == "":
                dataset_info_file = None
            self.dataset_info_file = dataset_info_file

        log_level = dict_.get(TomoFluoConfig.LOG_LEVEL_DK, None)
        if log_level is not None:
            self.log_level = log_level
        self.title = dict_.get(TomoFluoConfig.TITLE_DK)
        ignore_file_patterns = dict_.get(TomoFluoConfig.IGNORE_FILE_PATTERN_DK, None)
        if ignore_file_patterns is not None:
            if ignore_file_patterns == "":
                ignore_file_patterns = tuple()
            else:
                ignore_file_patterns = convert_str_to_tuple(ignore_file_patterns)
            self.ignore_file_patterns = ignore_file_patterns
        duplicate_data = dict_.get(TomoFluoConfig.DUPLICATE_DATA_DK, None)
        if duplicate_data is not None:
            self.duplicate_data = convert_str_to_bool(duplicate_data)
        external_path_type = dict_.get(TomoFluoConfig.EXTERNAL_LINK_RELATIVE_DK, None)
        if external_path_type is not None:
            self.external_path_type = external_path_type

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
            comments_fct=TomoFluoConfig.get_comments,
            logger=_logger,
        )

    @staticmethod
    def from_cfg_file(file_path: str, encoding=None):
        assert file_path is not None, "file_path should not be None"
        config_parser = configparser.ConfigParser(allow_no_value=True)
        config_parser.read(file_path, encoding=encoding)
        return TomoFluoConfig.from_dict(config_parser)

    @staticmethod
    def get_comments(key):
        return TomoFluoConfig.COMMENTS[key]


def generate_default_fluo_config(level: str = "required") -> dict:
    """generate a default configuration to convert fluo-tomo data (after PyMCA fit) to NXtomo"""
    return TomoFluoConfig().to_dict(level=level)
