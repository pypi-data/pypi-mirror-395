# coding: utf-8

import os

import pytest

from nxtomo.nxobject.nxdetector import FieldOfView
from nxtomo.nxobject.nxsource import ProbeType, SourceType
from nxtomomill.io.config.fluoconfig import TomoFluoConfig, generate_default_fluo_config


def test_TomoFluoConfig_to_dict(tmp_path):
    """Test processing of the to_dict"""
    config = TomoFluoConfig()

    config_dict = config.to_dict()
    for key in (
        TomoFluoConfig.GENERAL_SECTION_DK,
        TomoFluoConfig.SOURCE_SECTION_DK,
    ):
        assert key in config_dict

    TomoFluoConfig.from_dict(config_dict)

    file_path = os.path.join(tmp_path, "config.cfg")
    assert not os.path.exists(file_path)
    config.to_cfg_file(file_path)
    assert os.path.exists(file_path)
    config_loaded = TomoFluoConfig.from_cfg_file(file_path=file_path)

    assert config_loaded.to_dict() == config.to_dict()


def test_TomoFluoConfig_default_config(tmp_path):
    """insure default configuration generation works"""
    file_path = os.path.join(tmp_path, "config.cfg")
    assert not os.path.exists(file_path)
    config = generate_default_fluo_config()
    assert isinstance(config, dict)
    TomoFluoConfig.from_dict(config).to_cfg_file(file_path=file_path)
    assert os.path.exists(file_path)


def test_TomoFluoConfig_setters():
    """test the different setters and getter of the EDFTomoConfig"""
    config = TomoFluoConfig()

    # try to test a new attribut (insure class is frozeen)
    with pytest.raises(AttributeError):
        config.new_attrs = "toto"

    # test general section setters
    with pytest.raises(TypeError):
        config.input_folder = 12.0
    config.input_folder = "my_folder"
    with pytest.raises(TypeError):
        config.output_file = 12.0
    config.output_file = "my_nx.nx"

    config.file_extension = ".nx"

    with pytest.raises(TypeError):
        config.detectors = 12.0
    config.detectors = None
    config.detectors = "test_"

    with pytest.raises(TypeError):
        config.dataset_basename = 12.0
    config.dataset_basename = None
    config.dataset_basename = "test_"

    config.overwrite = True

    with pytest.raises(TypeError):
        config.title = 12.0
    config.title = None
    config.title = "my title"

    # test source setters
    config.instrument_name = None
    config.instrument_name = "BMXX"
    with pytest.raises(TypeError):
        config.instrument_name = 12.3

    config.source_name = None
    config.source_name = "ESRF"
    with pytest.raises(TypeError):
        config.source_name = 12.2
    config.source_name = "XFEL"

    config.source_type = None
    config.source_type = SourceType.FIXED_TUBE_X_RAY.value
    config.source_type = SourceType.FIXED_TUBE_X_RAY
    with pytest.raises(ValueError):
        config.source_type = "trsts"
    with pytest.raises(TypeError):
        config.source_type = 123

    config.source_probe = None
    config.source_probe = ProbeType.ELECTRON
    config.source_probe = "positron"
    with pytest.raises(TypeError):
        config.source_probe = 123

    # test detector setters
    config.field_of_view = None
    with pytest.raises(TypeError):
        config.field_of_view = 12
    with pytest.raises(ValueError):
        config.field_of_view = "toto"
    config.field_of_view = FieldOfView.FULL.value
    config.field_of_view = FieldOfView.HALF
    # TO DO : add test on detector setter

    config_dict = config.to_dict()
    general_section_dict = config_dict[TomoFluoConfig.GENERAL_SECTION_DK]
    assert general_section_dict[TomoFluoConfig.INPUT_FOLDER_DK] == "my_folder"
    assert general_section_dict[TomoFluoConfig.OUTPUT_FILE_DK] == "my_nx.nx"
    assert general_section_dict[TomoFluoConfig.FILE_EXTENSION_DK] == ".nx"
    assert general_section_dict[TomoFluoConfig.OVERWRITE_DK] is True
    assert general_section_dict[TomoFluoConfig.DATASET_BASENAME_DK] == "test_"
    assert general_section_dict[TomoFluoConfig.TITLE_DK] == "my title"

    source_section_dict = config_dict[TomoFluoConfig.SOURCE_SECTION_DK]
    assert source_section_dict[TomoFluoConfig.INSTRUMENT_NAME_DK] == "BMXX"
    assert source_section_dict[TomoFluoConfig.SOURCE_NAME_DK] == "XFEL"
    assert (
        source_section_dict[TomoFluoConfig.SOURCE_TYPE_DK]
        == SourceType.FIXED_TUBE_X_RAY.value
    )
