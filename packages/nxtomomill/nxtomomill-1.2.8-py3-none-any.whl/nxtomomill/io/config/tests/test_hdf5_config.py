# coding: utf-8

import os
import shutil
import tempfile
import unittest

from nxtomomill import settings
from nxtomomill.io.config import TomoHDF5Config


class TestH5Config(unittest.TestCase):
    """
    Test the HDF5Config class
    """

    def setUp(self) -> None:
        self.folder = tempfile.mkdtemp()

    def tearDown(self) -> None:
        shutil.rmtree(self.folder)

    def test_generate_default_config(self):
        """
        Insure we can generate a default configuration
        """
        config = TomoHDF5Config()
        config.input_file = "toto.h5"
        config.output_file = "toto.nx"
        output = config.to_dict()

        self.assertEqual(type(output), dict)
        # check titles values
        titles_dict = output[TomoHDF5Config.ENTRIES_AND_TITLES_SECTION_DK]
        self.assertEqual(
            titles_dict[TomoHDF5Config.INIT_TITLES_DK], settings.Tomo.H5.INIT_TITLES
        )
        self.assertEqual(
            titles_dict[TomoHDF5Config.ZSERIE_INIT_TITLES_DK],
            settings.Tomo.H5.ZSERIE_INIT_TITLES,
        )
        self.assertEqual(
            titles_dict[TomoHDF5Config.PROJ_TITLES_DK], settings.Tomo.H5.PROJ_TITLES
        )
        self.assertEqual(
            titles_dict[TomoHDF5Config.FLAT_TITLES_DK], settings.Tomo.H5.FLAT_TITLES
        )
        self.assertEqual(
            titles_dict[TomoHDF5Config.DARK_TITLES_DK], settings.Tomo.H5.DARK_TITLES
        )
        self.assertEqual(
            titles_dict[TomoHDF5Config.ALIGNMENT_TITLES_DK],
            settings.Tomo.H5.ALIGNMENT_TITLES,
        )
        # check sample pixel size
        keys_dict = output[TomoHDF5Config.KEYS_SECTION_DK]
        self.assertEqual(
            keys_dict[TomoHDF5Config.SAMPLE_X_PIXEL_SIZE_KEYS_DK],
            settings.Tomo.H5.SAMPLE_X_PIXEL_SIZE_KEYS,
        )
        self.assertEqual(
            keys_dict[TomoHDF5Config.SAMPLE_Y_PIXEL_SIZE_KEYS_DK],
            settings.Tomo.H5.SAMPLE_Y_PIXEL_SIZE_KEYS,
        )
        self.assertEqual(
            keys_dict[TomoHDF5Config.DETECTOR_X_PIXEL_SIZE_KEYS_DK],
            settings.Tomo.H5.DETECTOR_X_PIXEL_SIZE_KEYS,
        )
        self.assertEqual(
            keys_dict[TomoHDF5Config.DETECTOR_Y_PIXEL_SIZE_KEYS_DK],
            settings.Tomo.H5.DETECTOR_Y_PIXEL_SIZE_KEYS,
        )
        # check translation
        self.assertEqual(
            keys_dict[TomoHDF5Config.SAMPLE_X_KEYS_DK], settings.Tomo.H5.SAMPLE_X_KEYS
        )
        self.assertEqual(
            keys_dict[TomoHDF5Config.SAMPLE_Y_KEYS_DK], settings.Tomo.H5.SAMPLE_Y_KEYS
        )
        self.assertEqual(
            keys_dict[TomoHDF5Config.TRANSLATION_Z_KEYS_DK],
            settings.Tomo.H5.TRANSLATION_Z_KEYS,
        )
        # others
        if settings.Tomo.H5.VALID_CAMERA_NAMES is None:
            self.assertEqual(keys_dict[TomoHDF5Config.VALID_CAMERA_DK], "")
        else:
            self.assertEqual(
                keys_dict[TomoHDF5Config.VALID_CAMERA_DK],
                settings.Tomo.H5.VALID_CAMERA_NAMES,
            )
        self.assertEqual(
            keys_dict[TomoHDF5Config.ROT_ANGLE_DK], settings.Tomo.H5.ROT_ANGLE_KEYS
        )
        self.assertEqual(
            keys_dict[TomoHDF5Config.DIODE_KEYS_DK], settings.Tomo.H5.DIODE_KEYS
        )
        self.assertEqual(
            keys_dict[TomoHDF5Config.TRANSLATION_Y_KEYS_DK],
            settings.Tomo.H5.TRANSLATION_Y_KEYS,
        )
        self.assertEqual(
            keys_dict[TomoHDF5Config.ACQUISITION_EXPO_TIME_KEYS_DK],
            settings.Tomo.H5.ACQ_EXPO_TIME_KEYS,
        )

        # check input and output file
        general_information = output[TomoHDF5Config.GENERAL_SECTION_DK]
        self.assertEqual(general_information[TomoHDF5Config.INPUT_FILE_DK], "toto.h5")
        self.assertEqual(general_information[TomoHDF5Config.OUTPUT_FILE_DK], "toto.nx")

    def test_to_dict(self):
        """test the `to_dict` function"""
        config = TomoHDF5Config()
        output_dict = config.to_dict()
        self.assertEqual(type(output_dict), dict)
        # check sections
        for section in (
            TomoHDF5Config.GENERAL_SECTION_DK,
            TomoHDF5Config.KEYS_SECTION_DK,
            TomoHDF5Config.EXTRA_PARAMS_SECTION_DK,
            TomoHDF5Config.FRAME_TYPE_SECTION_DK,
            TomoHDF5Config.ENTRIES_AND_TITLES_SECTION_DK,
        ):
            with self.subTest(section=section):
                self.assertTrue(section in output_dict)
        # check titles keys
        for key in (
            TomoHDF5Config.ALIGNMENT_TITLES_DK,
            TomoHDF5Config.PROJ_TITLES_DK,
            TomoHDF5Config.ZSERIE_INIT_TITLES_DK,
            TomoHDF5Config.INIT_TITLES_DK,
            TomoHDF5Config.FLAT_TITLES_DK,
            TomoHDF5Config.DARK_TITLES_DK,
        ):
            with self.subTest(key=key):
                self.assertTrue(
                    key in output_dict[TomoHDF5Config.ENTRIES_AND_TITLES_SECTION_DK]
                )
        # check sample pixel size
        for key in (
            TomoHDF5Config.SAMPLE_X_PIXEL_SIZE_KEYS_DK,
            TomoHDF5Config.SAMPLE_Y_PIXEL_SIZE_KEYS_DK,
            TomoHDF5Config.DETECTOR_X_PIXEL_SIZE_KEYS_DK,
            TomoHDF5Config.DETECTOR_Y_PIXEL_SIZE_KEYS_DK,
        ):
            with self.subTest(key=key):
                self.assertTrue(key in output_dict[TomoHDF5Config.KEYS_SECTION_DK])
        # translation keys
        for key in (
            TomoHDF5Config.SAMPLE_X_KEYS_DK,
            TomoHDF5Config.SAMPLE_Y_KEYS_DK,
            TomoHDF5Config.TRANSLATION_Z_KEYS_DK,
        ):
            with self.subTest(key=key):
                self.assertTrue(key in output_dict[TomoHDF5Config.KEYS_SECTION_DK])
        # others
        for key in (
            TomoHDF5Config.VALID_CAMERA_DK,
            TomoHDF5Config.ROT_ANGLE_DK,
            TomoHDF5Config.TRANSLATION_Y_KEYS_DK,
            TomoHDF5Config.DIODE_KEYS_DK,
            TomoHDF5Config.ACQUISITION_EXPO_TIME_KEYS_DK,
        ):
            with self.subTest(key=key):
                self.assertTrue(key in output_dict[TomoHDF5Config.KEYS_SECTION_DK])

    def test_from_dict(self):
        """test the `from_dict` function"""
        valid_camera_names = ("frelon", "totocam")
        alignment_titles = ("this is an alignment",)
        sample_x_keys = ("tx", "x")
        config = TomoHDF5Config.from_dict(
            {
                TomoHDF5Config.KEYS_SECTION_DK: {
                    TomoHDF5Config.VALID_CAMERA_DK: valid_camera_names,
                    TomoHDF5Config.SAMPLE_X_KEYS_DK: sample_x_keys,
                },
                TomoHDF5Config.ENTRIES_AND_TITLES_SECTION_DK: {
                    TomoHDF5Config.ALIGNMENT_TITLES_DK: alignment_titles
                },
            }
        )
        self.assertEqual(config.valid_camera_names, valid_camera_names)
        self.assertEqual(config.alignment_titles, alignment_titles)
        self.assertEqual(config.sample_x_keys, sample_x_keys)

    def test_from_dict_lowercase(self):
        """Test `from_dict` method with lower case sections"""
        ref_dict = TomoHDF5Config().to_dict()
        lower_dict = {k.lower(): v for k, v in ref_dict.items()}

        config = TomoHDF5Config.from_dict(lower_dict)
        self.assertEqual(config.to_dict(), ref_dict)

    def test_raises_errors(self):
        """
        Insure a type error is raised if an invalid type is passed to the
        HDF5Config class
        :return:
        """
        with self.assertRaises(TypeError):
            TomoHDF5Config.from_dict(
                {
                    TomoHDF5Config.ENTRIES_AND_TITLES_SECTION_DK: {
                        TomoHDF5Config.DARK_TITLES_DK: 1213
                    }
                }
            )

    def test_to_and_from_cfg_file(self):
        """
        Insure we can dump the configuration to a .cfg file and that we
        can read it back
        """
        file_path = os.path.join(self.folder, "output_file.cfg")
        input_config = TomoHDF5Config()
        input_config.to_cfg_file(file_path)
        self.assertTrue(os.path.exists(file_path))
        loaded_config = TomoHDF5Config.from_cfg_file(file_path=file_path)
        self.assertTrue(isinstance(loaded_config, TomoHDF5Config))
