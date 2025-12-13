"""
Functions and variables common to all specifications.
"""
from typing import Any, Tuple, Optional, cast
from pathlib import Path
from functools import cache

import yaml

from dkist_fits_specifications.utils.frozendict import frozendict

__all__ = [
    "load_raw_spec",
    "raw_schema_type_hint",
    "schema_type_hint",
]

schema_type_hint = frozendict[str, frozendict[str, Any]]
"""
A type hint for a single validation schema.

The top-level frozendict key is a SPEC header key and the value is another frozendict of that key's schema keys.
E.g.:

{"SIMPLE" : {"required": False, "type": "bool", "values": [True]}, ...}

As returned by `.load_spec122` and `.load_spec214`.
"""

# For some reason using tuple and not typing.Tuple here causes the doc build to fail
raw_schema_type_hint = Tuple[frozendict[str, Any], schema_type_hint]
"""
A Type hint for a single raw schema, as loaded directly from a yaml file.

The first part of the tuple is a frozendict representing a section's header.
The second part of the tuple is a frozendict containing the section keys and their schema keys (see above).
E.g.:

({"spec122": {"section": "fits", "expand": False}}, {"SIMPLE": {...}, "BITPIX": {...}, ...})

This type is returned by the `.load_raw_spec122` and `.load_raw_spec214` methods.
"""


@cache
def load_raw_spec(
    base_path: Path, glob: Optional[str] = None
) -> frozendict[str, raw_schema_type_hint]:
    """
    Load raw schemas from the yaml files in ``base_path``.

    Parameters
    ----------
    glob
        A pattern to use to match a file, without the ``.yml`` file extension.
        Can be a section name like ``'wcs'``.

    Returns
    -------
    raw_schemas
        The schemas as loaded from the yaml files.
    """
    if glob is None:
        glob = "*"

    files = Path(base_path).glob(f"{glob}.yml")

    raw_schemas = {}
    for fname in files:
        schema_name = fname.stem
        with open(fname, encoding="utf8") as fobj:
            raw_schema = tuple(yaml.load_all(fobj, Loader=yaml.SafeLoader))

            # Because this function is cached, we want to strongly discourage
            # modification of the return values. We do this by wrapping the
            # expected tree of dicts into frozendict objects which disallow
            # modification
            frozen_header = {}
            for key, head in raw_schema[0].items():
                frozen_header[key] = frozendict(head)
            frozen_key_schemas = {}
            for key, schema in raw_schema[1].items():
                frozen_key_schemas[key] = frozendict(schema)
            raw_schema = (frozendict(frozen_header), frozendict(frozen_key_schemas))

        # Apply a more specific type hint to the loaded schema
        raw_schemas[schema_name] = cast(raw_schema_type_hint, raw_schema)

    return frozendict(raw_schemas)
