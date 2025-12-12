# coding: utf-8

"""
Application to create a default configuration file to be used by fluo2nx application.

.. program-output:: nxtomomill fluo-config --help

"""

import argparse
import logging

from nxtomomill.io import TomoFluoConfig, generate_default_fluo_config

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

    configuration = generate_default_fluo_config(level=options.level)
    TomoFluoConfig.dict_to_cfg(file_path=options.output_file, dict_=configuration)
