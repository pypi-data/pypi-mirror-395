"""
Functions and schemas relating to specification 214, for level 1 FITS files.

The 214 schemas are more complex than the 122 ones, as they have more uses, and
are tightly coupled to the 122 schemas.
There are three main variants to the 214 schemas:

* The **raw schemas** as saved in the yaml files. Each 214 raw schema can
  reference a 122 schema, from which it can copy the 'type', 'default_value',
  'values', and 'format' fields for keys. A key can be marked as ``copy:
  true`` to indicate that the schema **and** the value should be the same in
  214 as 122, or it can be marked as ``copy: 'schema'`` to indicate that just
  the schema is the same for that key, but the value will be regenerated.
* The **full schemas**. The full schemas are processed to merge the values in
  the schema header, and any values from the corresponding 122 schema. These
  schemas contain a lot more fields than the 122 schemas do, as these schemas
  are also used to generate documentation describing the specification.
* The **validation schema**. These schemas (returned by `.load_processed_spec214`) are
  updated based on KEY:VALUE pairs from an actual header. This includes things
  like expanding <N> keys and setting conditional requiredness. They have all
  the extra fields present in the "full" schemas removed.

"""
import copy
from typing import Any, Optional
from pathlib import Path
from functools import cache

import astropy.units as u
import yamale  # type: ignore

from dkist_fits_specifications import spec122, validation_schema
from dkist_fits_specifications.utils import (
    frozendict,
    load_raw_spec,
    raw_schema_type_hint,
    schema_type_hint,
)

__all__ = [
    "load_raw_spec214",
    "load_full_spec214",
    "load_spec214",
    "expand_214_schema",
    "get_214_l0_only_keys",
]

from dkist_fits_specifications.utils.spec_processors.expansion import (
    ExpansionIndex,
    expand_schema,
)
from dkist_fits_specifications.utils.spec_processors.instrument_requiredness import (
    InstrumentRequired,
)
from dkist_fits_specifications.utils.spec_processors.polarimetric_requiredness import (
    PolarimetricRequired,
)
from dkist_fits_specifications.utils.spec_processors.requiredness_base import (
    ConditionalRequirement,
    update_schema_requiredness,
)

BASE_PATH = Path(__file__).parent / "schemas"

full_schema_214 = yamale.make_schema(Path(__file__).parent / "spec214_full_schema.yml")


def update_with_122(
    global_section_122: Optional[str], schema: schema_type_hint
) -> schema_type_hint:
    """
    Update the raw spec 214 schemas with information from the 122 schemas.

    Parameters
    ----------
    section_122
        The section in the 122 specifications to update the schema with.
    schema
        The schema to update, should be the body of a unprocessed 214 schema.

    Returns
    -------
    schema
        The updated 214 schema.
    """
    # Update the 214 schema with the data in the corresponding 122 schema
    import_keys = {
        "type",
        "default_value",
        "values",
        "values_range",
        "example_values",
        "format",
        "comment",
        "instrument_required",
    }

    for key, key_schema in schema.items():
        section_122 = key_schema.get("section_122", global_section_122)
        schema_122 = {}
        if section_122:
            schema_122 = spec122.load_spec122(section_122)[section_122]

        # Copy can be "schema" but that's all we care about here
        to_copy = bool(key_schema.get("copy", False))
        key_122 = key_schema.get("rename", key if to_copy else None)

        if key_122:
            if key_122 not in schema_122:
                print(
                    f"{key_122} is not in the 122 schema for {section_122},"
                    " although the 214 section references it."
                )
                continue
            key_schema_122 = schema_122[key_122]
            update_122 = dict(filter(lambda i: i[0] in import_keys, key_schema_122.items()))

            shared_keys = set(key_schema.keys()).intersection(set(update_122.keys()))
            if shared_keys:
                raise ValueError(f"Collision in 214 and 122 schemas for {key}: {shared_keys = }")

            schema[key] = {**key_schema, **update_122}

    return schema


def update_schema_with_header(raw_schema: tuple[dict, schema_type_hint]) -> schema_type_hint:
    """
    Merge the body of a schema with its header.

    Parameters
    ----------
    raw_schema
        The loaded version of a single yaml file.

    Returns
    -------
    schema
        The body of a schema, updated with the header.
    """
    header, raw_schemas = raw_schema
    header = dict(copy.deepcopy(header)["spec214"])
    # Remove the 122 section name
    header.pop("section_122")

    key_schemas = {}
    for key, key_schema in raw_schemas.items():
        updated_schema = {key: {**header, **key_schema}}
        # Expected takes the value of required unless overridden
        updated_schema[key]["expected"] = updated_schema[key].get(
            "expected", updated_schema[key]["required"]
        )
        yamale.validate(full_schema_214, [(updated_schema, None)])
        key_schemas.update(updated_schema)

    return key_schemas


def preprocess_schema(
    raw_schema: raw_schema_type_hint, include_level0=False
) -> frozendict[str, Any]:
    """
    Convert a single raw schema or a full 214 schema.

    Parameters
    ----------
    raw_schema
        The loaded version of a single yaml file.

    Returns
    -------
    schema
        The body of a schema, updated with the header and the relevant values
        from the 122 schema where appropriate.
    """
    global_section_122 = raw_schema[0]["spec214"].get("section_122")

    # Merge in the keys in the header with all the keys
    schema = update_schema_with_header(raw_schema)  # makes a nested copy

    merged_spec = update_with_122(global_section_122, schema)
    if not include_level0:
        for key, spec in tuple(merged_spec.items()):
            if spec.get("level0_only", False):
                merged_spec.pop(key)

    # Ensure the units in the comments are correct.
    # This performs two functions:
    # 1) Make sure all keys with units in their schema have units in the FITS comments.
    # 2) Ensure that if a unit is changed between 122 and 214 the comment is updated.
    frozenspec = {}
    for key, info in merged_spec.items():
        unit = info.get("units", None)
        comment = info.get("comment", "")
        # It seems astropy doesn't support a string representation of u.one
        if unit and unit != "dimensionless":
            unit = u.Unit(unit)
            unit_str = f"[{unit:fits}]"
            if not comment.startswith(unit_str):
                if comment.startswith("["):
                    _, comment = comment.split("]", maxsplit=1)
                comment = f"{unit_str} {comment.strip()}".strip()
                info["comment"] = comment

        frozenspec[key] = frozendict(info)

    return frozendict(frozenspec)


# No cache here as load_raw_spec is cached
def load_raw_spec214(glob: Optional[str] = None) -> frozendict[str, raw_schema_type_hint]:
    """
    Load the raw 214 schemas from the yaml files.

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
    return load_raw_spec(BASE_PATH, glob)


@cache
def load_full_spec214(
    glob: Optional[str] = None, include_level0: bool = False
) -> frozendict[str, schema_type_hint]:
    """
    Return the full loaded schemas for DKIST Specification 214

    Parameters
    ----------
    glob
        A pattern to use to match a file, without the ``.yml`` file extension.
        Can be a section name like ``'wcs'``.

    """

    raw_schemas = load_raw_spec214(glob)

    schemas = {}
    for schema_name, raw_schema in raw_schemas.items():
        schema = preprocess_schema(raw_schema, include_level0=include_level0)
        yamale.validate(full_schema_214, [(schema, None)])
        schemas[schema_name] = schema

    return frozendict(schemas)


@cache
def get_214_l0_only_keys() -> list[str]:
    """Return a list of keys marked as "level0_only" in the 214 schemas."""

    raw_schemas = load_raw_spec214()

    schemas = {}
    for schema_name, raw_schema in raw_schemas.items():
        schema = preprocess_schema(raw_schema, include_level0=True)
        yamale.validate(full_schema_214, [(schema, None)])
        schemas[schema_name] = schema

    level0_only_keys = []

    for schema_name, full_schema in schemas.items():
        for key, key_schema in full_schema.items():
            if key_schema.get("level0_only", False):
                level0_only_keys.append(key)

    return level0_only_keys


@cache
def load_spec214(glob: Optional[str] = None) -> frozendict[str, schema_type_hint]:
    """
    Load the simple schema version of 214 for validation or generation.

    Parameters
    ----------
    glob
        A pattern to use to match a file, without the ``.yml`` file extension.
        Can be a section name like ``'wcs'``.
    """

    full_schemas = load_full_spec214(glob)

    # Extract the keys from the base schema.
    allowed_keys = validation_schema.includes["key"].dict.keys()

    schemas = {}
    for schema_name, full_schema in full_schemas.items():
        schema = {}
        for key, key_schema in full_schema.items():
            filtered_schema = dict(filter(lambda i: i[0] in allowed_keys, key_schema.items()))
            schema[key] = frozendict(filtered_schema)
        # Validate the schema against the simple schema
        yamale.validate(validation_schema, [(schema, None)])
        schemas[schema_name] = frozendict(schema)

    return frozendict(schemas)


def load_processed_spec214(
    glob: Optional[str] = None, **header: dict[str, Any]
) -> dict[str, schema_type_hint]:
    """
    Load the 214 schema, processed based on a FITS header.

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
    If you expand the schema with a single header from a dataset, the expanded
    schema should be valid for all the files in that dataset.
    """
    schemas = load_spec214(glob)
    processed_schemas = {}
    for section, schema in schemas.items():
        processed_schemas[section] = process_spec214_section(schema, **header)

    return processed_schemas


def process_spec214_section(schema: schema_type_hint, **header: dict[str, Any]) -> schema_type_hint:
    """
    Apply expansions and requiredness to a single section of the 214 schema.

    This is a separate function from `load_processed_spec214` to allow it to be used elsewhere in this package.
    """
    schema = update_214_schema_requiredness(schema, **header)
    schema = expand_214_schema(schema, **header)

    return schema


def define_214_schema_expansions(**header: dict[str, Any]) -> list[ExpansionIndex]:
    """
    Collate the list of schema expansions to apply for spec 214
    """
    expansion_list = []
    # If the header is compressed we need to expand based on the image axes not the table axes
    if "DAAXES" in header.keys() and header.get("DEAXES", 0) != 0:
        k_expansion = ExpansionIndex(
            index="k",
            size=1,
            values=range(header["DAAXES"] + 1, header["DAAXES"] + header["DEAXES"] + 1),
        )
        expansion_list.append(k_expansion)
    if "DNAXIS" in header.keys():
        d_expansion = ExpansionIndex(index="d", size=1, values=range(1, header["DNAXIS"] + 1))
        expansion_list.append(d_expansion)
    if "NPROPOS" in header.keys():
        rr_expansion = ExpansionIndex(index="rr", size=2, values=range(1, header["NPROPOS"] + 1))
        expansion_list.append(rr_expansion)
    if "NEXPERS" in header.keys():
        ee_expansion = ExpansionIndex(index="ee", size=2, values=range(1, header["NEXPERS"] + 1))
        expansion_list.append(ee_expansion)
    if "NAXIS" in header.keys():
        n_expansion = ExpansionIndex(index="n", size=1, values=range(1, header["NAXIS"] + 1))
        i_expansion = ExpansionIndex(index="i", size=1, values=range(1, header["NAXIS"] + 1))
        j_expansion = ExpansionIndex(index="j", size=1, values=range(1, header["NAXIS"] + 1))
        expansion_list.extend([n_expansion, i_expansion, j_expansion])
    # Compression keys
    if "ZIMAGE" in header:
        # The z index for ZNAMEz and ZVALz do not have a key which tells you how
        # many keys you have.
        zval = [k for k in header.keys() if k.startswith("ZVAL")]
        z_max = max([int(k[-1]) for k in zval])
        z_expansion = ExpansionIndex(index="z", size=1, values=range(1, z_max + 1))
        f_expansion = ExpansionIndex(index="f", size=1, values=range(1, header["TFIELDS"] + 1))
        expansion_list.extend([z_expansion, f_expansion])
    pp_expansion = ExpansionIndex(index="pp", size=2, values=[1, 2, 5, 10, 25, 75, 90, 95, 98, 99])
    expansion_list.append(pp_expansion)
    if "NSPECLNS" in header:
        sl_expansion = ExpansionIndex(index="sl", size=2, values=range(1, header["NSPECLNS"] + 1))
        expansion_list.append(sl_expansion)
    return expansion_list


def expand_214_schema(
    schema: schema_type_hint, **header: dict[str, Any]
) -> dict[str, frozendict[str, Any]]:
    """
    Given a 214 header expand all known indices.
    """
    return expand_schema(schema=schema, expansions=define_214_schema_expansions(**header))


def define_214_conditional_requiredness(**header: dict[str, Any]) -> list[ConditionalRequirement]:
    """
    Collate the list of conditional requirements to apply for spec 214
    """
    requirements_list = []

    instrument_requirement = InstrumentRequired(header)
    requirements_list.append(instrument_requirement)

    polarimetric_requirement = PolarimetricRequired(header)
    requirements_list.append(polarimetric_requirement)

    return requirements_list


def update_214_schema_requiredness(
    schema: schema_type_hint, **header: dict[str, Any]
) -> dict[str, frozendict[str, Any]]:
    """
    Given a 214 header, update the "required" spec field based on presence/values of spec fields that indicate conditional requiredness.
    """
    return update_schema_requiredness(
        schema=schema, requirements=define_214_conditional_requiredness(**header)
    )
