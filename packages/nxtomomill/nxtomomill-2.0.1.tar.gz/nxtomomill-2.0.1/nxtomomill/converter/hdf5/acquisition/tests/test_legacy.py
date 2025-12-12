from __future__ import annotations

import os
from pathlib import Path

import numpy
import pint
import pytest
from nxtomo.application.nxtomo import NXtomo
from nxtomo.nxobject.nxdetector import ImageKey

from nxtomomill import converter
from nxtomomill.io.config import TomoHDF5Config
from nxtomomill.tests.datasets import GitlabDataset

_ureg = pint.get_application_registry()


@pytest.fixture(scope="class")
def S59_68p41b_16mm_6p5mm_F8_0001_Dataset() -> Path:
    scan_dir = GitlabDataset.get_dataset("h5_datasets")
    assert scan_dir is not None
    return Path(os.path.join(scan_dir, "legacy", "S59_68p41b_16mm_6p5mm_F8_0001.h5"))


@pytest.fixture(scope="class")
def WGN_01_0000_P_110_8128_D_129_Dataset():
    scan_dir = GitlabDataset.get_dataset("h5_datasets")
    assert scan_dir is not None
    return Path(os.path.join(scan_dir, "legacy", "WGN_01_0000_P_110_8128_D_129.h5"))


def test_S59_68p41b_16mm_6p5mm_F8_0001_dataset(
    S59_68p41b_16mm_6p5mm_F8_0001_Dataset, tmp_path
):
    """test 'S59_68p41b_16mm_6p5mm_F8_0001.h5' legacy dataset"""
    output_file = tmp_path / "S59_68p41b_16mm_6p5mm_F8_0001.nx"
    assert not os.path.exists(output_file), "output_file exists already"
    configuration = TomoHDF5Config()

    configuration.output_file = str(output_file)
    configuration.input_file = str(S59_68p41b_16mm_6p5mm_F8_0001_Dataset)
    configuration.raises_error = False
    configuration.no_master_file = False
    configuration.single_file = True

    result = converter.from_h5_to_nx(configuration=configuration)
    assert len(result) == 1

    assert os.path.exists(output_file)

    nxtomo = NXtomo().load(*result[0])

    nxtomo.energy = 70.0 * _ureg.keV
    n_frames = 10252

    assert len(nxtomo.sample.x_translation) == n_frames
    assert len(nxtomo.sample.y_translation) == n_frames
    assert len(nxtomo.sample.z_translation) == n_frames
    assert len(nxtomo.instrument.detector.count_time) == n_frames
    assert len(nxtomo.instrument.detector.image_key) == n_frames
    assert len(nxtomo.instrument.detector.image_key_control) == n_frames
    assert nxtomo.instrument.detector.field_of_view.value == "Full"

    N_PROJ = 10000

    # check image keys
    expected_image_key = numpy.concatenate(
        [
            [ImageKey.DARK_FIELD] * 50,
            [ImageKey.FLAT_FIELD] * 101,
            [ImageKey.PROJECTION] * N_PROJ,
            [ImageKey.FLAT_FIELD] * 101,
        ]
    )
    numpy.testing.assert_array_equal(
        nxtomo.instrument.detector.image_key_control, expected_image_key
    )

    # check angles
    expected_angles = numpy.concatenate(
        [
            [0] * 151,
            numpy.linspace(0, 360, N_PROJ, endpoint=False),
            [0] * 101,
        ]
    )
    assert len(expected_angles) == n_frames
    numpy.testing.assert_almost_equal(
        nxtomo.sample.rotation_angle.to(_ureg.degree).magnitude,
        expected_angles,
        decimal=1,
    )

    assert nxtomo.instrument.detector.distance == 105 * _ureg.millimeter
    assert nxtomo.instrument.source.distance == -145000 * _ureg.millimeter

    assert nxtomo.instrument.detector.x_pixel_size == 6.5 * _ureg.micrometer
    assert nxtomo.instrument.detector.y_pixel_size == 6.5 * _ureg.micrometer


def test_WGN_01_0000_P_110_8128_D_129(WGN_01_0000_P_110_8128_D_129_Dataset, tmp_path):
    """test 'WGN_01_0000_P_110_8128_D_129' legacy dataset"""
    output_file = tmp_path / "WGN_01_0000_P_110_8128_D_129_Dataset.nx"
    assert not os.path.exists(output_file), "output_file exists already"
    configuration = TomoHDF5Config()

    configuration.output_file = str(output_file)
    configuration.input_file = str(WGN_01_0000_P_110_8128_D_129_Dataset)
    configuration.raises_error = False
    configuration.no_master_file = False
    configuration.single_file = True

    result = converter.from_h5_to_nx(configuration=configuration)
    assert len(result) == 3

    assert os.path.exists(output_file)

    nxtomo = NXtomo().load(*result[0])

    nxtomo.energy = 80.0 * _ureg.keV
    n_frames = 4602

    assert len(nxtomo.sample.x_translation) == n_frames
    assert len(nxtomo.sample.y_translation) == n_frames
    assert len(nxtomo.sample.z_translation) == n_frames
    assert len(nxtomo.instrument.detector.count_time) == n_frames
    assert len(nxtomo.instrument.detector.image_key) == n_frames
    assert len(nxtomo.instrument.detector.image_key_control) == n_frames
    assert nxtomo.instrument.detector.field_of_view.value == "Full"

    N_PROJ = 4500

    # check image keys
    expected_image_key = numpy.concatenate(
        [
            [ImageKey.DARK_FIELD] * 100,
            [ImageKey.FLAT_FIELD] * 2,
            [ImageKey.PROJECTION] * N_PROJ,
        ]
    )
    numpy.testing.assert_array_equal(
        nxtomo.instrument.detector.image_key_control, expected_image_key
    )

    # check angles
    expected_angles = numpy.concatenate(
        [
            [0] * 102,
            numpy.linspace(0, 180, N_PROJ, endpoint=False),
        ]
    )
    assert len(expected_angles) == n_frames
    numpy.testing.assert_almost_equal(
        nxtomo.sample.rotation_angle.to(_ureg.degree).magnitude,
        expected_angles,
        decimal=1,
    )

    # note: saved value is indeed 0...
    assert nxtomo.instrument.detector.distance == 0 * _ureg.millimeter
    assert nxtomo.instrument.source.distance == -20000 * _ureg.millimeter

    assert nxtomo.instrument.detector.x_pixel_size == 6.5 * _ureg.micrometer
    assert nxtomo.instrument.detector.y_pixel_size == 6.5 * _ureg.micrometer
