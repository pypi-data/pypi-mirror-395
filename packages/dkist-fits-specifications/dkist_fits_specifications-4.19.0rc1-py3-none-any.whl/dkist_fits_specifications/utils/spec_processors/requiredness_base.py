from abc import ABC, abstractmethod
from typing import Any

from dkist_fits_specifications.utils import frozendict, schema_type_hint

# Defined as a random string so we don't accidentally confuse ourselves in tests where we want to
# use a fake instrument name
_NOT_A_DKIST_INSTRUMENT = "67197693JustAFallbackInstrument062757b16"


class ConditionalRequirement(ABC):
    """
    A class definition for capturing a single type of conditional requiredness.

    These classes are instantiated with a header and then can be used to check the requiredness of any key in the schema
    """

    def __init__(self, header: dict[str:Any]):
        self.header = header

    @abstractmethod
    def check_requiredness(self, spec_fields: frozendict[str, Any]) -> bool:
        """Given the schema for a single key, check if this key needs to be required."""
        pass


def update_schema_requiredness(
    schema: schema_type_hint, requirements: list[ConditionalRequirement]
) -> dict[str, frozendict[str, Any]]:
    """
    Modify a schema's `required` values based on conditional requirements.

    If ANY of the conditional requiredness requirements are met then the key is set to "required."
    """
    updated_schema = dict()
    for fits_keyword_name, spec_fields in schema.items():
        thawed_fields = dict(spec_fields)

        if any([requirement.check_requiredness(spec_fields) for requirement in requirements]):
            thawed_fields["required"] = True

        updated_schema[fits_keyword_name] = frozendict(thawed_fields)

    return updated_schema
