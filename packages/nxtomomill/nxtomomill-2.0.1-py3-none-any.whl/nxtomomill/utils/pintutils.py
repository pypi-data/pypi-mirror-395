"""pint utils"""

from __future__ import annotations

import pint
import logging
from pint.errors import UndefinedUnitError

_logger = logging.getLogger(__name__)

_ureg = pint.get_application_registry()


VALID_CURRENT_VALUES: tuple[str] = [
    str(unit) for unit in (_ureg.ampere, _ureg.kiloampere, _ureg.milliampere)
]
VALID_ENERGY_VALUES: tuple[str] = [
    str(unit)
    for unit in (_ureg.joule, _ureg.eV, _ureg.keV, _ureg.meV, _ureg.GeV, _ureg.kJ)
]
VALID_METRIC_VALUES: tuple[str] = [
    str(unit)
    for unit in (
        _ureg.nanometer,
        _ureg.micrometer,
        _ureg.millimeter,
        _ureg.centimeter,
        _ureg.meter,
    )
]


def get_unit(unit: str, default: pint.Unit, from_dataset: str) -> pint.Unit:
    """
    Convert given unit as an str to a pint unit. Else fallback to 'default'
    """
    if not isinstance(unit, str):
        raise TypeError(f"'unit' is expected to be a {str}. Got {type(unit)}")
    if not isinstance(default, pint.Unit):
        raise TypeError(
            f"'default' is expected to be a {pint.Unit}. Got {type(default)}"
        )

    # special cases (some string that can exists and that are not handled by pint)
    if unit.lower() in ("mev", "megaelectronvolt"):
        unit = _ureg.keV * 1e3
    elif unit.lower() in ("gev", "gigaelectronvolt"):
        unit = _ureg.keV * 1e6
    elif unit == "microns":
        unit = "um"

    try:
        unit = _ureg(unit)
    except UndefinedUnitError:
        _logger.warning(
            f"Undefined unit: {unit} from {from_dataset}. Fallback on default unit {default}"
        )
        return default
    else:
        return unit
