# coding: utf-8

"""
Application to create a default configuration file to be used by edf2nx application.

.. program-output:: nxtomomill edf-config --help

For a complete tutorial you can have a look at :ref:`edf2nxtutorial`
"""

import argparse
import logging

from nxtomomill.io import TomoEDFConfig, generate_default_edf_config

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)


def main(argv):
    """ """
    parser = argparse.ArgumentParser(description="Create a default configuration file")
    parser.add_argument("output_file", help="output .cfg file")
    parser.add_argument(
        "--level",
        "--option-level",
        help="Level of options to embed in the configuration file. Can be 'required' or 'advanced'.",
        default="required",
    )

    options = parser.parse_args(argv[1:])

    configuration = generate_default_edf_config(level=options.level)
    TomoEDFConfig.dict_to_cfg(file_path=options.output_file, dict_=configuration)
