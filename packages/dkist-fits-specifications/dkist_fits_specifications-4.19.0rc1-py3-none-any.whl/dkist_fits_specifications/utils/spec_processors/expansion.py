from typing import Any, Iterable
from dataclasses import dataclass

from dkist_fits_specifications.utils import frozendict, schema_type_hint


@dataclass
class ExpansionIndex:
    """
    A class for defining a FITS schema expansion.

    index: the string to be substituted, omitting the surrounding '<', '>'
    size: how many (zero-padded) characters to use for the substituted integer
    values: the iterable of integers to be used as substitution for the index

    Example:
        Using the expansion of:
        ExpansionIndex(index="a", size=3, values=range(1, 6))

        on the keyword 'KEY<a>' would produce the expanded set of keys:
        ['KEY001', 'KEY002', 'KEY003', 'KEY004', 'KEY005']

    """

    index: str
    values: Iterable
    size: int = None

    def __post_init__(self):
        if len(str(max(self.values))) > self.size:
            raise ValueError(
                f"The maximum expansion value ({max(self.values)}) does not fit within the prescribed size ({self.size})."
            )

    def _expanded_keys(self, key: str) -> list[str]:
        """Generate schema entries for expanded keys."""
        return [key.replace(f"<{self.index}>", str(i).zfill(self.size)) for i in self.values]

    def generate(self, keys: list[str]) -> list[str]:
        """Generate the new keys to be added."""
        return_keys = []
        for key in keys:
            if f"<{self.index}>" in key:
                return_keys.extend(self._expanded_keys(key=key))
        long_keys = [k for k in return_keys if len(k) > 8]
        if long_keys:
            raise ValueError(
                f"FITS keywords cannot be more than 8 characters in length. {long_keys} are too long."
            )
        return return_keys


def expand_schema(
    schema: schema_type_hint, expansions: list[ExpansionIndex]
) -> dict[str, frozendict[str, Any]]:
    """Perform a schema expansion given a schema and a list of ExpansionIndexes to apply."""
    expanded_schema = dict()
    for fits_keyword_name, spec_fields in schema.items():
        if "<" not in fits_keyword_name:
            expanded_schema.update({fits_keyword_name: spec_fields})
        else:
            expanded_fits_keywords = [fits_keyword_name]
            for expansion in expansions:
                expanded_fits_keywords.extend(expansion.generate(keys=expanded_fits_keywords))
            expanded_schema.update({k: spec_fields for k in expanded_fits_keywords if "<" not in k})
    return expanded_schema
