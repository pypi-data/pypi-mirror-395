from typing import Any

from dkist_fits_specifications.utils import frozendict
from dkist_fits_specifications.utils.spec_processors.requiredness_base import (
    _NOT_A_DKIST_INSTRUMENT,
    ConditionalRequirement,
)


class InstrumentRequired(ConditionalRequirement):
    """
    Conditional requirement that makes all keys related to the headers "INSTRUME" required.

    spec_field:
      instrument_required: str
    """

    def __init__(self, header: dict[str, Any]):
        super().__init__(header=header)
        self.instrument = self.header.get("INSTRUME", _NOT_A_DKIST_INSTRUMENT).casefold()

    def check_requiredness(self, spec_fields: frozendict[str, Any]) -> bool:
        """Check if the required instrument matches the instrument in the header."""
        # "false" is importantly different than _NOT_A_DKIST_INSTRUMENT
        return spec_fields.get("instrument_required", "false").casefold() == self.instrument
