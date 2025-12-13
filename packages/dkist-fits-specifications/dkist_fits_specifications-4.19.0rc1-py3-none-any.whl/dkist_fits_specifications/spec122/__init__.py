"""
Functions and schemas relating to specification 122, the level 0 FITS files.

The 122 schemas have a singular variant, they are all NAXIS=3.
However, the yaml files still are written with the indices corresponding to NAXIS (``n, i, j``).
These indices are expanded by the loading function so the returned schema always has ``NAXIS = 3``.

The yamls are written with the indices, to reduce duplication and to make it
easier for 214 to use the raw (unprocessed) schemas.
"""
import copy
from typing import Any, Optional
from pathlib import Path
from functools import cache

import yamale  # type: ignore

from dkist_fits_specifications import validation_schema
from dkist_fits_specifications.utils import (
    frozendict,
    load_raw_spec,
    raw_schema_type_hint,
    schema_type_hint,
)

__all__ = ["load_raw_spec122", "load_spec122"]

from dkist_fits_specifications.utils.spec_processors.expansion import (
    ExpansionIndex,
    expand_schema,
)
from dkist_fits_specifications.utils.spec_processors.instrument_requiredness import (
    InstrumentRequired,
)
from dkist_fits_specifications.utils.spec_processors.requiredness_base import (
    ConditionalRequirement,
    update_schema_requiredness,
)

base_path = Path(__file__).parent / "schemas"


def preprocess_schema(schema: schema_type_hint) -> schema_type_hint:
    """
    Convert the loaded raw schemas to the 122 schema.

    This simply means applying each section's header to its keys.

    Parameters
    ----------
    raw_schema
        The loaded version of a single yaml file.

    Returns
    -------
    schema
        The body of a schema, updated as needed from the yaml files.
    """
    header, raw_schemas = schema
    header = dict(copy.deepcopy(header)["spec122"])
    header.pop("section")

    # Thaw the schema
    schema = dict(raw_schemas)
    for key, key_schema in schema.items():
        updated_schema = {key: {**header, **key_schema}}
        # Rather than put expected in all the files, default it to required
        updated_schema[key]["expected"] = key_schema.get("expected", key_schema["required"])
        updated_schema[key] = frozendict(updated_schema[key])
        schema.update(updated_schema)
    return frozendict(schema)


# No cache here as load_raw_spec is cached
def load_raw_spec122(glob: Optional[str] = None) -> frozendict[str, raw_schema_type_hint]:
    """
    Load the raw 122 schemas from the yaml files.

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
    return load_raw_spec(base_path, glob)


@cache
def load_spec122(glob: Optional[str] = None) -> frozendict[str, schema_type_hint]:
    """
    Return the loaded schemas for DKIST Specification 122

    Parameters
    ----------
    glob
        A pattern to use to match a file, without the ``.yml`` file extension.
        Can be a section name like ``'wcs'``.
    """

    raw_schemas = load_raw_spec122(glob=glob)
    schemas = {}
    for schema_name, raw_schema in raw_schemas.items():
        # 122 only uses the second document
        schema = preprocess_schema(raw_schema)
        yamale.validate(validation_schema, [(schema, None)])
        schemas[schema_name] = schema

    return frozendict(schemas)


def load_processed_spec122(
    glob: Optional[str] = None, **header: dict[str, Any]
) -> dict[str, schema_type_hint]:
    """
    Load the 122 schema, processed based on a FITS header.

    This function currently expands the schema and applies conditional requiredness

    Parameters
    ----------
    glob
        A pattern to use to match a file, without the ``.yml`` file extension.
        Can be a section name like ``'wcs'``.

    header
       A FITS header to be used to expand the schema as needed.

    Notes
    -----
    If you process the schema with a single header from a dataset, the processed
    schema should be valid for all the files in that dataset.
    """
    schemas = load_spec122(glob)
    processed_schemas = {}
    for section, schema in schemas.items():
        processed_schemas[section] = process_spec122_section(schema, **header)

    return processed_schemas


def process_spec122_section(schema: schema_type_hint, **header: dict[str, Any]) -> schema_type_hint:
    """
    Apply expansions and requiredness to a single section of the 122 schema.

    This is a separate function from `load_processed_spec122` to allow it to be used elsewhere in this package.
    """
    schema = update_122_schema_requiredness(schema, **header)
    schema = expand_122_schema(schema)

    return schema


def define_122_schema_expansions() -> list[ExpansionIndex]:
    # 122 always has 3 axes, but we encode the yamls independent of the number,
    # to match 214 which might have a variable number of axes.
    n_expansion = ExpansionIndex(index="n", size=1, values=range(1, 4))
    i_expansion = ExpansionIndex(index="i", size=1, values=range(1, 4))
    j_expansion = ExpansionIndex(index="j", size=1, values=range(1, 4))
    return [n_expansion, i_expansion, j_expansion]


def expand_122_schema(schema: schema_type_hint) -> dict[str, frozendict[str, Any]]:
    """
    Given a 122 header expand all known indices.
    """
    return expand_schema(schema=schema, expansions=define_122_schema_expansions())


def define_122_conditional_requiredness(**header: dict[str, Any]) -> list[ConditionalRequirement]:
    """
    Collate the list of conditional requirements to apply for spec 122
    """
    requirements_list = []

    instrument_requirement = InstrumentRequired(header)
    requirements_list.append(instrument_requirement)

    return requirements_list


def update_122_schema_requiredness(
    schema: schema_type_hint, **header: dict[str, Any]
) -> dict[str, frozendict[str, Any]]:
    """
    Given a 122 header, update the "required" spec field based on presence/values of spec fields that indicate conditional requiredness.
    """
    return update_schema_requiredness(
        schema=schema, requirements=define_122_conditional_requiredness(**header)
    )
