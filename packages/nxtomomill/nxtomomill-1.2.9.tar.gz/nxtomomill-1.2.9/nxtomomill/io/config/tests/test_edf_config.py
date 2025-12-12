# coding: utf-8

import os
import pint
from tempfile import TemporaryDirectory

import pytest

from nxtomo.nxobject.nxdetector import FieldOfView
from nxtomo.nxobject.nxsource import ProbeType, SourceType
from nxtomomill import settings
from nxtomomill.io.config.edfconfig import TomoEDFConfig, generate_default_edf_config

_ureg = pint.get_application_registry()


def test_TomoEDFConfig_to_dict():
    """Test processing of the to_dict"""
    config = TomoEDFConfig()

    config_dict = config.to_dict()
    for key in (
        TomoEDFConfig.GENERAL_SECTION_DK,
        TomoEDFConfig.EDF_KEYS_SECTION_DK,
        TomoEDFConfig.FLAT_DARK_SECTION_DK,
        TomoEDFConfig.UNIT_SECTION_DK,
        TomoEDFConfig.SAMPLE_SECTION_DK,
        TomoEDFConfig.SOURCE_SECTION_DK,
        TomoEDFConfig.DETECTOR_SECTION_DK,
    ):
        assert key in config_dict

    TomoEDFConfig.from_dict(config_dict)

    with TemporaryDirectory() as folder:
        file_path = os.path.join(folder, "config.cfg")
        assert not os.path.exists(file_path)
        config.to_cfg_file(file_path)
        assert os.path.exists(file_path)
        config_loaded = TomoEDFConfig.from_cfg_file(file_path=file_path)

    assert config_loaded.to_dict() == config.to_dict()


def test_TomoEDFConfig_default_config():
    """insure default configuration generation works"""
    with TemporaryDirectory() as folder:
        file_path = os.path.join(folder, "config.cfg")
        assert not os.path.exists(file_path)
        config = generate_default_edf_config()
        assert isinstance(config, dict)
        TomoEDFConfig.from_dict(config).to_cfg_file(file_path=file_path)
        assert os.path.exists(file_path)


def test_TomoEDFConfig_setters():
    """test the different setters and getter of the EDFTomoConfig"""
    config = TomoEDFConfig()

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
        config.dataset_basename = 12.0
    config.dataset_basename = None
    config.dataset_basename = "test_"

    with pytest.raises(TypeError):
        config.dataset_info_file = 12.3
    config.dataset_info_file = None
    config.dataset_info_file = "my_info_file.info"

    config.overwrite = True

    with pytest.raises(TypeError):
        config.title = 12.0
    config.title = None
    config.title = "my title"

    with pytest.raises(TypeError):
        config.ignore_file_patterns = 12.0
    with pytest.raises(TypeError):
        config.ignore_file_patterns = "toto"
    with pytest.raises(TypeError):
        config.ignore_file_patterns = (1.0,)
    config.ignore_file_patterns = ("toto",)
    config.ignore_file_patterns = None

    # test header keys + dark and flat setters
    attributes_value = {
        "motor_position_keys": settings.Tomo.EDF.MOTOR_POS,
        "motor_mne_keys": settings.Tomo.EDF.MOTOR_MNE,
        "rotation_angle_keys": settings.Tomo.EDF.ROT_ANGLE,
        "dark_names": settings.Tomo.EDF.DARK_NAMES,
        "flat_names": settings.Tomo.EDF.REFS_NAMES,
    }
    for attr, key in attributes_value.items():
        setattr(config, attr, key)
        with pytest.raises(TypeError):
            setattr(config, attr, "toto")
        with pytest.raises(TypeError):
            setattr(config, attr, 12.20)
        with pytest.raises(TypeError):
            setattr(config, attr, (12.20,))

    # test units setters
    attributes_value = {
        "pixel_size_unit": _ureg.micrometer,
        "distance_unit": _ureg.meter,
        "energy_unit": _ureg.keV,
        "x_trans_unit": _ureg.meter,
        "y_trans_unit": _ureg.meter,
        "z_trans_unit": _ureg.meter,
    }
    for attr, key in attributes_value.items():
        # test providing an instance of a unit
        setattr(config, attr, key)
        # test providing a sting if of a unit
        setattr(config, attr, str(key))
        with pytest.raises(TypeError):
            setattr(config, attr, None)
        with pytest.raises(TypeError):
            setattr(config, attr, 12.0)

    # test sample setters
    config.sample_name = None
    with pytest.raises(TypeError):
        config.sample_name = (12,)
    with pytest.raises(TypeError):
        config.sample_name = 12.0
    config.sample_name = "my sample"

    with pytest.raises(TypeError):
        config.force_angle_calculation = "toto"
    config.force_angle_calculation = True

    with pytest.raises(TypeError):
        config.force_angle_calculation_endpoint = "toto"
    config.force_angle_calculation_endpoint = True

    with pytest.raises(TypeError):
        config.angle_calculation_rev_neg_scan_range = "toto"
    config.angle_calculation_rev_neg_scan_range = False

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

    config_dict = config.to_dict()
    general_section_dict = config_dict[TomoEDFConfig.GENERAL_SECTION_DK]
    assert general_section_dict[TomoEDFConfig.INPUT_FOLDER_DK] == "my_folder"
    assert general_section_dict[TomoEDFConfig.OUTPUT_FILE_DK] == "my_nx.nx"
    assert general_section_dict[TomoEDFConfig.FILE_EXTENSION_DK] == ".nx"
    assert general_section_dict[TomoEDFConfig.OVERWRITE_DK] is True
    assert general_section_dict[TomoEDFConfig.DATASET_BASENAME_DK] == "test_"
    assert (
        general_section_dict[TomoEDFConfig.DATASET_FILE_INFO_DK] == "my_info_file.info"
    )
    assert general_section_dict[TomoEDFConfig.TITLE_DK] == "my title"
    assert general_section_dict[TomoEDFConfig.IGNORE_FILE_PATTERN_DK] == ""

    edf_headers_section_dict = config_dict[TomoEDFConfig.EDF_KEYS_SECTION_DK]
    assert (
        edf_headers_section_dict[TomoEDFConfig.MOTOR_POSITION_KEY_DK]
        == settings.Tomo.EDF.MOTOR_POS
    )
    assert (
        edf_headers_section_dict[TomoEDFConfig.MOTOR_MNE_KEY_DK]
        == settings.Tomo.EDF.MOTOR_MNE
    )
    assert (
        edf_headers_section_dict[TomoEDFConfig.X_TRANS_KEY_DK]
        == settings.Tomo.EDF.X_TRANS
    )
    assert (
        edf_headers_section_dict[TomoEDFConfig.Y_TRANS_KEY_DK]
        == settings.Tomo.EDF.Y_TRANS
    )
    assert (
        edf_headers_section_dict[TomoEDFConfig.Z_TRANS_KEY_DK]
        == settings.Tomo.EDF.Z_TRANS
    )
    assert (
        edf_headers_section_dict[TomoEDFConfig.ROT_ANGLE_KEY_DK]
        == settings.Tomo.EDF.ROT_ANGLE
    )

    dark_flat_section_dict = config_dict[TomoEDFConfig.FLAT_DARK_SECTION_DK]
    assert (
        dark_flat_section_dict[TomoEDFConfig.DARK_NAMES_DK]
        == settings.Tomo.EDF.DARK_NAMES
    )
    assert (
        dark_flat_section_dict[TomoEDFConfig.FLAT_NAMES_DK]
        == settings.Tomo.EDF.REFS_NAMES
    )

    units_section_dict = config_dict[TomoEDFConfig.UNIT_SECTION_DK]
    assert units_section_dict[TomoEDFConfig.PIXEL_SIZE_EXPECTED_UNIT] == str(
        _ureg.micrometer
    )
    assert units_section_dict[TomoEDFConfig.DISTANCE_EXPECTED_UNIT] == str(_ureg.meter)
    assert units_section_dict[TomoEDFConfig.ENERGY_EXPECTED_UNIT] == str(_ureg.keV)
    assert units_section_dict[TomoEDFConfig.X_TRANS_EXPECTED_UNIT] == str(_ureg.meter)
    assert units_section_dict[TomoEDFConfig.Y_TRANS_EXPECTED_UNIT] == str(_ureg.meter)
    assert units_section_dict[TomoEDFConfig.Z_TRANS_EXPECTED_UNIT] == str(_ureg.meter)

    sample_section_dict = config_dict[TomoEDFConfig.SAMPLE_SECTION_DK]
    assert sample_section_dict[TomoEDFConfig.SAMPLE_NAME_DK] == "my sample"
    assert sample_section_dict[TomoEDFConfig.FORCE_ANGLE_CALCULATION] is True
    assert sample_section_dict[TomoEDFConfig.FORCE_ANGLE_CALCULATION_ENDPOINT] is True
    assert (
        sample_section_dict[TomoEDFConfig.FORCE_ANGLE_CALCULATION_REVERT_NEG_SCAN_RANGE]
        is False
    )

    source_section_dict = config_dict[TomoEDFConfig.SOURCE_SECTION_DK]
    assert source_section_dict[TomoEDFConfig.INSTRUMENT_NAME_DK] == "BMXX"
    assert source_section_dict[TomoEDFConfig.SOURCE_NAME_DK] == "XFEL"
    assert (
        source_section_dict[TomoEDFConfig.SOURCE_TYPE_DK]
        == SourceType.FIXED_TUBE_X_RAY.value
    )

    detector_section_dict = config_dict[TomoEDFConfig.DETECTOR_SECTION_DK]
    assert (
        detector_section_dict[TomoEDFConfig.FIELD_OF_VIEW_DK] == FieldOfView.HALF.value
    )
