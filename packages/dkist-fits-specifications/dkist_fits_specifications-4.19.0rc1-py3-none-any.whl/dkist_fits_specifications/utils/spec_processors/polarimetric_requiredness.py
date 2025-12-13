import logging
from typing import Any
from functools import partial

from dkist_fits_specifications.utils import frozendict
from dkist_fits_specifications.utils.spec_processors.requiredness_base import (
    _NOT_A_DKIST_INSTRUMENT,
    ConditionalRequirement,
)

logger = logging.getLogger(__name__)

# How this works:
# The top-level key is the SPEC-controlled instrument name. The value is a dict[str, Iterable and not str]
# This second-level dictionary defines a linking between header keys and values needed for a header to be considered
# "polarimetric". The logic is all([header[key] in second_level[key] for key in second_level.keys()]).
# For example, consider POLARIMETRIC_HEADER_REQUIREMENTS = {"instrument": {"key1": [1, 2], "key2": ["yes", "true"]}}
# In this case, a header would be considered polarimetric if:
# (header["key1"] == 1 or header["key1"] == 2) and (header["key2"] == "yes" or header["key2"] == "true")
POLARIMETRIC_HEADER_REQUIREMENTS = {
    # range(2, 2**16) is a hack to mean > 1
    "cryo-nirsp": {"CNMODNST": range(2, 2**16), "CNSPINMD": ["Continuous", "Stepped"]},
    "dl-nirsp": {"DLPOLMD": ["Full Stokes"]},
    "visp": {"VSPPOLMD": ["observe_polarimetric"]},
}


def _vbi_is_polarimetric(header: dict[str, Any]) -> False:
    """VBI is *always* non-polarimetric."""
    return False


def _header_match_is_polarimetric(instrument: str, header: dict[str, Any]) -> bool:
    """
    Determine if a header comes from a polarimetric dataset based on matching values with known polarimetric requirements.

    Requirements are defined in POLARIMETRIC_HEADER_REQUIREMENTS and have the form dict[str, dict[str, Iterable and not str]].
    The meaning of this form is {INSTRUMENT: {KEY: [polarimetric, values, ...], ...}, ...}. A header is considered
    polarimetric iff:

    `all(header[key] in POLARIMETRIC_HEADER_REQUIREMENTS[INSTRUMENT][key]
         for key in POLARIMETRIC_HEADER_REQUIREMENTS[INSTRUMENT].keys()])`

    Parameters
    ----------
    instrument
        Instrument name. Must match the controlled list in the SPEC

    header
        The header to check for polarimetrocity
    """
    requirements = POLARIMETRIC_HEADER_REQUIREMENTS[instrument]
    check_list = []
    for key, reqs in requirements.items():
        header_value = header[key]
        if isinstance(header_value, str):
            header_value = header_value.casefold()
            reqs = [v.casefold() for v in reqs]

        check_list.append(header_value in reqs)

    return all(check_list)


def _fallback_is_polarimetric(header: dict[str, Any]) -> False:
    """
    One-stop function for when we can't figure out what to do with a particular instrument.

    Logs a warning and returns False.
    """
    instrument = header.get("INSTRUME", _NOT_A_DKIST_INSTRUMENT).casefold()
    logger.warning(
        f"Checking polarimetric requiredness for instrument {instrument} is not currently supported."
    )
    return False


class PolarimetricRequired(ConditionalRequirement):

    """
    Conditional requirement that makes keys required if the dataset represents polarimetric data.

    spec_field:
      polarimetric_required: bool
    """

    instrument_to_polarimetric_func_mapping = {
        "vbi": _vbi_is_polarimetric,
        "visp": partial(_header_match_is_polarimetric, instrument="visp"),
        "cryo-nirsp": partial(_header_match_is_polarimetric, instrument="cryo-nirsp"),
        "dl-nirsp": partial(_header_match_is_polarimetric, instrument="dl-nirsp"),
    }

    def __init__(self, header: dict[str, Any]):
        super().__init__(header=header)
        instrument = self.header.get("INSTRUME", _NOT_A_DKIST_INSTRUMENT).casefold()

        is_polarimetric_function = self.instrument_to_polarimetric_func_mapping.get(
            instrument, _fallback_is_polarimetric
        )

        try:
            self.is_polarimetric = is_polarimetric_function(header=self.header)
        except Exception as e:
            logger.warning(
                f"Error encountered when checking polarimetric requiredness. Error was:\n{e}"
            )
            self.is_polarimetric = False

    def check_requiredness(self, spec_fields: frozendict[str, Any]) -> bool:
        """Check if the header was from a polarimetric dataset and the key is `polarimetric_required`."""
        return self.is_polarimetric and spec_fields.get("polarimetric_required", False)
