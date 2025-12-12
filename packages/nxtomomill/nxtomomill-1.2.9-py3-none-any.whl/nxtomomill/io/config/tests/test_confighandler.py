# coding: utf-8

import os
import shutil
import tempfile
import unittest

from nxtomomill.io.config.confighandler import TomoHDF5ConfigHandler
from nxtomomill.io.config.hdf5config import TomoHDF5Config
from nxtomomill.io.framegroup import FrameGroup


class _ARParseMock(object):
    def __init__(self):
        self.config = None
        self.input_file = None
        self.output_file = None
        self.set_params = None
        self.align_titles = None
        self.proj_titles = None
        self.flat_titles = None
        self.dark_titles = None
        self.init_zserie_titles = None
        self.init_multi_tomo_titles = None
        self.init_titles = None
        self.init_back_and_forth_titles = None
        self.x_pixel_size_key = None
        self.y_pixel_size_key = None
        self.acq_expo_time_keys = None
        self.rot_angle_keys = None
        self.valid_camera_names = None
        self.translation_z_keys = None
        self.sample_y_keys = None
        self.sample_x_keys = None
        self.request_input = False
        self.raises_error = False
        self.duplicate_data = None
        self.ignore_sub_entries = None
        self.entries = None
        self.debug = False
        self.overwrite = False
        self.single_file = False
        self.no_master_file = False
        self.file_extension = None
        self.field_of_view = None
        self.sample_detector_distance_paths = None


class TestH5Config(unittest.TestCase):
    """
    Test the HDF5Config class
    """

    def setUp(self) -> None:
        self.folder = tempfile.mkdtemp()

    def tearDown(self) -> None:
        shutil.rmtree(self.folder)

    def test_creation_from_config_file(self):
        options = _ARParseMock()
        with self.assertRaises(ValueError):
            TomoHDF5ConfigHandler(argparse_options=options)

        input_file_path = os.path.join(self.folder, "output_file.cfg")
        input_config = TomoHDF5Config()
        input_config.to_cfg_file(input_file_path)

        options.config = input_file_path

        with self.assertRaises(ValueError):
            TomoHDF5ConfigHandler(argparse_options=options)

        # insure this is valid if we add an input file and an output file
        # from the command line
        options.input_file = "toto.h5"
        options.output_file = "toto.nx"
        TomoHDF5ConfigHandler(argparse_options=options)

        # try providing twice an input file
        input_config.input_file = "toto2.h5"
        input_config.to_cfg_file(input_file_path)

        with self.assertRaises(ValueError):
            TomoHDF5ConfigHandler(argparse_options=options)

        # or if we provide them from the configuration file
        options.input_file = None
        options.output_file = None
        input_config.input_file = "toto.h5"
        input_config.output_file = "toto.nx"
        input_config.to_cfg_file(input_file_path)
        TomoHDF5ConfigHandler(argparse_options=options)

        # try providing twice an output file
        input_config.input_file = None
        input_config.output_file = "toto2.nx"
        input_config.to_cfg_file(input_file_path)
        with self.assertRaises(ValueError):
            TomoHDF5ConfigHandler(argparse_options=options)

        # try another random para,eter
        input_config.output_file = None
        input_config.sample_x_keys = ("xtrans2",)
        options.sample_x_keys = "xtrans3"
        input_config.to_cfg_file(input_file_path)
        with self.assertRaises(ValueError):
            TomoHDF5ConfigHandler(argparse_options=options)

    def test_creation_from_cmd_line_opts(self):
        options = _ARParseMock()
        input_file_path = os.path.join(self.folder, "output_file.cfg")
        input_config = TomoHDF5Config()
        input_config.to_cfg_file(input_file_path)
        options.input_file = "toto.h5"
        options.output_file = "toto.nx"
        options.debug = True
        TomoHDF5ConfigHandler(argparse_options=options)

        options.config = input_config
        with self.assertRaises(ValueError):
            TomoHDF5ConfigHandler(argparse_options=options)


class TestFrameUrls(unittest.TestCase):
    """Test frames urls"""

    def setUp(self) -> None:
        self.folder = tempfile.mkdtemp()

    def tearDown(self) -> None:
        shutil.rmtree(self.folder)

    def write_and_read_configuration(self, data_urls):
        configuration = TomoHDF5Config().to_dict()
        configuration[TomoHDF5Config.FRAME_TYPE_SECTION_DK][TomoHDF5Config.DATA_DK] = (
            FrameGroup.list_to_str(data_urls)
        )
        file_path = os.path.join(self.folder, "h52nx.cfg")
        TomoHDF5Config.dict_to_cfg(file_path=file_path, dict_=configuration)

        options = _ARParseMock()
        options.input_file = "toto.h5"
        options.output_file = "toto.nx"
        options.config = file_path
        config_handler = TomoHDF5ConfigHandler(options)
        return config_handler.configuration

    def test_local_paths(self):
        # TODO: test all option to read / write the configuration
        res_config = self.write_and_read_configuration(
            (
                FrameGroup(url="/entry0000/data/flats", frame_type="flat"),
                FrameGroup(url="/entry0000/data/projection1", frame_type="projection"),
                FrameGroup(url="/entry0000/data/projection2", frame_type="projection"),
                FrameGroup(url="/entry0000/data/alignment1", frame_type="alignment"),
                FrameGroup(url="/entry0000/data/alignment2", frame_type="alignment"),
                FrameGroup(url="/entry0000/data/darks", frame_type="dark"),
            )
        )
        self.assertNotEqual(res_config, None)
        self.assertEqual(len(res_config.data_frame_grps), 6)
        # check flats
        flat_url = res_config.data_frame_grps[0].url
        self.assertTrue(flat_url.file_path() in (None, ""))
        self.assertEqual(flat_url.data_path(), "/entry0000/data/flats")
        self.assertTrue(flat_url.data_slice() in (None, ""))
        # check projections
        projection_url_0 = res_config.data_frame_grps[1].url
        projection_url_1 = res_config.data_frame_grps[2].url
        self.assertTrue(projection_url_0.file_path() in (None, ""))
        self.assertEqual(projection_url_0.data_path(), "/entry0000/data/projection1")
        self.assertEqual(projection_url_0.data_slice(), None)
        self.assertTrue(projection_url_1.file_path() in (None, ""))
        self.assertEqual(projection_url_1.data_path(), "/entry0000/data/projection2")
        self.assertEqual(projection_url_1.data_slice(), None)

        # check darks
        dark_url = res_config.data_frame_grps[-1].url
        self.assertTrue(dark_url.file_path() in (None, ""))
        self.assertEqual(dark_url.data_path(), "/entry0000/data/darks")
        self.assertEqual(dark_url.data_slice(), None)

        # check alignments
        alignment_url_0 = res_config.data_frame_grps[3].url
        alignment_url_1 = res_config.data_frame_grps[4].url
        self.assertTrue(alignment_url_0.file_path() in (None, ""))
        self.assertEqual(alignment_url_0.data_path(), "/entry0000/data/alignment1")
        self.assertEqual(alignment_url_0.data_slice(), None)
        self.assertEqual(alignment_url_1.data_path(), "/entry0000/data/alignment2")

    def test_external_paths(self):
        """
        Check that DataUrl are handled.

        Warning: this also check data_slices but those are not handled.
        """
        res_config = self.write_and_read_configuration(
            (
                FrameGroup(
                    frame_type="flat",
                    url="silx:///myfile.h5?path=/entry0000/data/flats",
                ),
                FrameGroup(
                    frame_type="dark",
                    url="h5py:///data/file2.hdf5?path=/entry0000/data/darks",
                ),
                FrameGroup(frame_type="proj", url="h5py:///data/file3.hdf5?path=/data"),
                FrameGroup(
                    frame_type="proj",
                    url="silx:///data/file2.hdf5?path=/entry0000/data/projection2&slice=5:100",
                ),
                FrameGroup(
                    frame_type="alignment",
                    url="silx:///myfile.h5?path=/entry0000/data/alignment&slice=5",
                ),
            )
        )
        self.assertNotEqual(res_config, None)
        self.assertEqual(len(res_config.data_frame_grps), 5)
        # check flats
        flat_url = res_config.data_frame_grps[0]
        self.assertEqual(flat_url.url.file_path(), "/myfile.h5")
        self.assertEqual(flat_url.url.data_path(), "/entry0000/data/flats")
        self.assertEqual(flat_url.url.data_slice(), None)
        self.assertEqual(flat_url.url.scheme(), "silx")

        # check projections
        projection_url_0 = res_config.data_frame_grps[2].url
        projection_url_1 = res_config.data_frame_grps[3].url
        self.assertEqual(projection_url_0.file_path(), "/data/file3.hdf5")
        self.assertEqual(projection_url_0.data_path(), "/data")
        self.assertEqual(projection_url_0.data_slice(), None)
        self.assertEqual(projection_url_0.scheme(), "h5py")
        self.assertEqual(projection_url_1.file_path(), "/data/file2.hdf5")
        self.assertEqual(projection_url_1.data_path(), "/entry0000/data/projection2")
        self.assertEqual(projection_url_1.data_slice(), (slice(5, 100),))
        self.assertEqual(projection_url_1.scheme(), "silx")

        # check darks
        dark_url = res_config.data_frame_grps[1].url
        self.assertEqual(dark_url.file_path(), "/data/file2.hdf5")
        self.assertEqual(dark_url.data_path(), "/entry0000/data/darks")
        self.assertEqual(dark_url.data_slice(), None)
        self.assertEqual(dark_url.scheme(), "h5py")

        # check alignments
        alignment_url_0 = res_config.data_frame_grps[4].url
        self.assertEqual(alignment_url_0.file_path(), "/myfile.h5")
        self.assertEqual(alignment_url_0.data_path(), "/entry0000/data/alignment")
        self.assertEqual(alignment_url_0.data_slice(), (5,))
        self.assertEqual(alignment_url_0.scheme(), "silx")
