# coding: utf-8

from __future__ import annotations
import configparser
import logging
from typing import Iterable


from nxtomomill.io.config.optionlevel import OptionLevel, filter_options_level_items
from nxtomo.nxobject.nxdetector import FieldOfView
from nxtomomill.utils import FileExtension
from nxtomo.nxobject.nxsource import ProbeType, SourceType

__all__ = ["ConfigBase", "ConfigSourceSection"]


class ConfigSourceSection:
    # SOURCE SECTION

    SOURCE_SECTION_DK = "SOURCE_SECTION"

    INSTRUMENT_NAME_DK = "instrument_name"

    SOURCE_NAME_DK = "source_name"

    SOURCE_TYPE_DK = "source_type"

    SOURCE_PROBE_DK = "source_probe"

    COMMENTS_SOURCE_SECTION_DK = {
        SOURCE_SECTION_DK: "section dedicated to source definition.\n",
        INSTRUMENT_NAME_DK: "name of the instrument",
        SOURCE_NAME_DK: "name of the source",
        SOURCE_TYPE_DK: f"type of the source. Must be one of {[item.value for item in SourceType]}",
        SOURCE_PROBE_DK: f"source probe. Must be one of {[item.value for item in ProbeType]}",
    }

    LEVEL_SOURCE_SECTION = {
        INSTRUMENT_NAME_DK: OptionLevel.ADVANCED,
        SOURCE_NAME_DK: OptionLevel.ADVANCED,
        SOURCE_TYPE_DK: OptionLevel.ADVANCED,
        SOURCE_PROBE_DK: OptionLevel.ADVANCED,
    }

    def load_source_section(self, dict_: dict) -> None:
        if self.INSTRUMENT_NAME_DK in dict_:
            self.instrument_name = dict_.get(self.INSTRUMENT_NAME_DK)
        if self.SOURCE_NAME_DK in dict_:
            self.source_name = dict_.get(self.SOURCE_NAME_DK)
        if self.SOURCE_TYPE_DK in dict_:
            self.source_type = dict_[self.SOURCE_TYPE_DK]
        if self.SOURCE_PROBE_DK in dict_:
            self.source_probe = dict_[self.SOURCE_PROBE_DK]

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
            dict_=res, level=level, level_ref=self.LEVEL_SOURCE_SECTION
        )


class ConfigBase:
    __isfrozen = False
    # to ease API and avoid setting wrong attributes we 'freeze' the attributes
    # see https://stackoverflow.com/questions/3603502/prevent-creating-new-attributes-outside-init

    def __init__(self) -> None:
        self._output_file = None
        self._overwrite = False
        self._file_extension = FileExtension.NX
        self._log_level = logging.WARNING
        self._field_of_view = None
        self._machine_current_keys = None

    def __setattr__(self, __name, __value):
        if self.__isfrozen and not hasattr(self, __name):
            raise AttributeError("can't set attribute", __name)
        else:
            super().__setattr__(__name, __value)

    @property
    def output_file(self) -> str | None:
        return self._output_file

    @output_file.setter
    def output_file(self, output_file: str | None):
        if not isinstance(output_file, (str, type(None))):
            raise TypeError("'input_file' should be None or an instance of Iterable")
        elif output_file == "":
            self._output_file = None
        else:
            self._output_file = output_file

    @property
    def overwrite(self) -> bool:
        return self._overwrite

    @overwrite.setter
    def overwrite(self, overwrite: bool) -> None:
        if not isinstance(overwrite, bool):
            raise TypeError("'overwrite' should be a boolean")
        else:
            self._overwrite = overwrite

    @property
    def file_extension(self) -> FileExtension:
        return self._file_extension

    @file_extension.setter
    def file_extension(self, file_extension: str):
        self._file_extension = FileExtension(file_extension)

    @property
    def log_level(self):
        return self._log_level

    @log_level.setter
    def log_level(self, level: str):
        self._log_level = getattr(logging, level.upper())

    def _set_freeze(self, freeze=True):
        self.__isfrozen = freeze

    @property
    def field_of_view(self) -> FieldOfView | None:
        return self._field_of_view

    @field_of_view.setter
    def field_of_view(self, fov: FieldOfView | str | None):
        if fov is None:
            self._field_of_view = fov
        elif isinstance(fov, str):
            self._field_of_view = FieldOfView(fov.title())
        elif isinstance(fov, FieldOfView):
            self._field_of_view = fov
        else:
            raise TypeError(
                f"fov is expected to be None, a string or FieldOfView. Not {type(fov)}"
            )

    @property
    def rotation_angle_keys(self) -> Iterable:
        return self._rot_angle_keys

    @rotation_angle_keys.setter
    def rotation_angle_keys(self, keys: Iterable):
        if not isinstance(keys, Iterable) or isinstance(keys, str):
            raise TypeError("'keys' should be an Iterable")
        else:
            for elmt in keys:
                if not isinstance(elmt, str):
                    raise TypeError("keys elmts are expected to be str")
            self._rot_angle_keys = keys

    @property
    def translation_z_keys(self) -> Iterable:
        return self._translation_z_keys

    @translation_z_keys.setter
    def translation_z_keys(self, keys) -> None:
        if not isinstance(keys, Iterable) or isinstance(keys, str):
            raise TypeError("'keys' should be an Iterable")
        else:
            for elmt in keys:
                if not isinstance(elmt, str):
                    raise TypeError("keys elmts are expected to be str")
            self._translation_z_keys = keys

    @property
    def machine_current_keys(self) -> Iterable:
        return self._machine_current_keys

    @machine_current_keys.setter
    def machine_current_keys(self, keys: Iterable) -> None:
        self._machine_current_keys = keys

    def to_dict(self) -> dict:
        """convert the configuration to a dictionary"""
        raise NotImplementedError("Base class")

    def load_from_dict(self, dict_: dict) -> None:
        """Load the configuration from a dictionary"""
        raise NotImplementedError("Base class")

    @staticmethod
    def from_dict(dict_: dict):
        raise NotImplementedError("Base class")

    def to_cfg_file(self, file_path: str):
        # TODO: add some generic information like:provided order of the tuple
        # will be the effective one. You can provide a key from it names if
        # it is contained in the positioners group
        # maybe split in sub section ?
        self.dict_to_cfg(file_path=file_path, dict_=self.to_dict())

    @staticmethod
    def dict_to_cfg(file_path, dict_):
        """ """
        raise NotImplementedError("Base class")

    @staticmethod
    def _dict_to_cfg(file_path, dict_, comments_fct, logger):
        """ """
        if not file_path.lower().endswith((".cfg", ".config", ".conf")):
            logger.warning("add a valid extension to the output file")
            file_path += ".cfg"
        config = configparser.ConfigParser(allow_no_value=True)
        config.optionxform = str
        for section_name, values in dict_.items():
            config.add_section(section_name)
            config.set(section_name, "# " + comments_fct(section_name), None)
            for key, value in values.items():
                # adopt nabu design: comments are set prior to the key
                config.set(section_name, "# " + comments_fct(key), None)
                config.set(section_name, key, str(value))

        with open(file_path, "w") as config_file:
            config.write(config_file)

    @staticmethod
    def from_cfg_file(file_path: str, encoding=None):
        raise NotImplementedError("Base class")

    @staticmethod
    def get_comments(key):
        raise NotImplementedError("Base class")

    def __str__(self):
        return str(self.to_dict())
