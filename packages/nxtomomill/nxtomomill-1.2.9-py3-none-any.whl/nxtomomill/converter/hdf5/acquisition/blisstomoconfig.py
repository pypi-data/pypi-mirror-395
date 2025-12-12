from __future__ import annotations

import h5py
from silx.io.utils import h5py_read_dataset

__all__ = [
    "TomoConfig",
]


class TomoConfig:
    """
    hold motor used for tomography acquisition according to https://tomo.gitlab-pages.esrf.fr/bliss-tomo/master/modelization_sample_stage.html convension
    """

    def __init__(self) -> None:
        self._rotation = None
        self._sample_u = None
        self._sample_v = None
        self._sample_x = None
        self._sample_y = None
        self._translation_x = None
        self._translation_y = None
        self._translation_z = None
        self._tomo_detector = None

    @property
    def rotation(self) -> str | None:
        return self._rotation

    @rotation.setter
    def rotation(self, motor: str | None):
        self._rotation = motor

    @property
    def sample_u(self) -> str | None:
        return self._sample_u

    @sample_u.setter
    def sample_u(self, motor: str | None):
        self._sample_u = motor

    @property
    def sample_v(self) -> str | None:
        return self._sample_v

    @sample_v.setter
    def sample_v(self, motor: str | None):
        self._sample_v = motor

    @property
    def sample_x(self) -> str | None:
        return self._sample_x

    @sample_x.setter
    def sample_x(self, motor: str | None):
        self._sample_x = motor

    @property
    def sample_y(self) -> str | None:
        return self._sample_y

    @sample_y.setter
    def sample_y(self, motor: str | None):
        self._sample_y = motor

    @property
    def translation_x(self) -> str | None:
        return self._translation_x

    @translation_x.setter
    def translation_x(self, motor: str | None):
        self._translation_x = motor

    @property
    def translation_y(self) -> str | None:
        return self._translation_y

    @translation_y.setter
    def translation_y(self, motor: str | None):
        self._translation_y = motor

    @property
    def translation_z(self) -> str | None:
        return self._translation_z

    @translation_z.setter
    def translation_z(self, motor: str | None):
        self._translation_z = motor

    @property
    def tomo_detector(self) -> str | None:
        return self._tomo_detector

    @tomo_detector.setter
    def tomo_detector(self, detector_name):
        self._tomo_detector = detector_name

    def __str__(self) -> str:
        return "tomo_config:" + " ; ".join(
            [
                f"rotation={self.rotation}",
                f"sample_u={self.sample_u}",
                f"sample_v={self.sample_v}",
                f"sample_x={self.sample_x}",
                f"sample_y={self.sample_y}",
                f"tomo_detector={self.tomo_detector}",
                f"translation_x={self.translation_x}",
                f"translation_y={self.translation_y}",
                f"translation_z={self.translation_z}",
            ]
        )

    @staticmethod
    def from_technique_group(technique_group: h5py.Group):
        """
        get rotation motor and thinks like this from the 'tomoconfig'.
        This can retrieve one or several dataset name or a single one.
        In the case of several dataset name we get (real_motor_name, bliss_alias)

        If the motor moves then this is pretty simple the real motor_name dataset exists.
        But if the motors does not move during the bliss scan (scalar value) then the real_motor_name dataset doesn't exists and
        the bliss alias does. This is why we need to keep both and check both during the 'standard process'...
        """
        if not isinstance(technique_group, h5py.Group):
            raise TypeError(
                f"instrument_group is expected to be an instance of {h5py.Group}. {type(technique_group)} provided"
            )
        if "tomoconfig" not in technique_group:
            raise KeyError("could find 'tomoconfig' key")
        else:
            tomo_config_group = technique_group.get("tomoconfig")

        def get_dataset(group, dataset_name, default):
            if dataset_name not in group:
                return default
            else:
                return h5py_read_dataset(group[dataset_name])

        tomo_config = TomoConfig()
        tomo_config.rotation = get_dataset(tomo_config_group, "rotation", None)
        tomo_config.sample_u = get_dataset(tomo_config_group, "sample_u", None)
        tomo_config.sample_v = get_dataset(tomo_config_group, "sample_v", None)
        tomo_config.sample_x = get_dataset(tomo_config_group, "sample_x", None)
        tomo_config.sample_y = get_dataset(tomo_config_group, "sample_y", None)
        tomo_config.tomo_detector = get_dataset(tomo_config_group, "detector", None)
        # translation x == sample_u
        tomo_config.translation_x = get_dataset(
            tomo_config_group, "sample_u", None
        )  # Needs translation X mapping
        tomo_config.translation_y = get_dataset(
            tomo_config_group, "translation_y", None
        )
        tomo_config.translation_z = get_dataset(
            tomo_config_group, "translation_z", None
        )

        return tomo_config
