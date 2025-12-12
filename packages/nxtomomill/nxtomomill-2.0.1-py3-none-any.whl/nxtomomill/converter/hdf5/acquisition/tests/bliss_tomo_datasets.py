"""Util to load dataset from gitlab.esrf.fr:tomo/tomo_test_data"""

import os
import pytest
import shutil
from tomoscan.tests.datasets import GitlabProject as _GitlabProject


_GitlabBlissTomoHolotomoDataset = _GitlabProject(
    branch_name="holotomo2",
    host="https://gitlab.esrf.fr",
    cache_dir=os.path.join(
        os.path.dirname(__file__),
        "__archive__",
    ),
    token=None,
    project_id=4166,  # https://gitlab.esrf.fr/tomo/tomo_test_data
)


@pytest.fixture
def holotomo2_simu_dataset(tmp_path):
    """
    Return a  bliss-tomo simulated dataset with latest holo-tomo sequence.
    """
    src_folder = _GitlabBlissTomoHolotomoDataset.get_dataset(
        os.path.join("simu", "bliss-2.3.0.dev0-tomo-2.9.0", "holotomo2")
    )
    dst_folder = os.path.join(tmp_path, "holotomo2")
    shutil.copytree(src_folder, dst_folder)
    return dst_folder
