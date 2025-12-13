"""
Functions and schemas relating to specifications for the Dataset Extras fits files.
"""
import copy
from typing import Any
from pathlib import Path
from functools import cache

import astropy.units as u
import yamale  # type: ignore

from dkist_fits_specifications import spec214, validation_schema
from dkist_fits_specifications.utils import (
    frozendict,
    load_raw_spec,
    raw_schema_type_hint,
    schema_type_hint,
)
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

BASE_PATH = Path(__file__).parent / "schemas"

full_schema_dataset_extras = yamale.make_schema(Path(__file__).parent / "dataset_extras_schema.yml")


def update_schema_with_header(raw_schema: tuple[dict, schema_type_hint]) -> dict[str, Any]:
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
    header = dict(copy.deepcopy(header)["dsextra"])

    key_schemas = {}
    for key, key_schema in raw_schemas.items():
        updated_schema = {key: {**header, **key_schema}}
        # Expected takes the value of required unless overridden
        updated_schema[key]["expected"] = updated_schema[key].get(
            "expected", updated_schema[key]["required"]
        )
        key_schemas.update(updated_schema)

    return key_schemas


def update_extra_with_214(schema: dict[str, Any]) -> dict[str, Any]:
    """
    Update the raw dataset extra schemas with information from the 214 schemas.

    Parameters
    ----------
    schema
        The schema to update, should be the body of an unprocessed dataset extra schema.

    Returns
    -------
    schema
        The updated dataset extra schema.
    """
    # Update the dataset extra schema with the data in the corresponding 214 schema keys
    import_keys = {
        "type",
        "values",
        "values_range",
        "example_values",
        "format",
        "comment",
        "instrument_required",
        "expand",
        "description",
        "units",
    }

    for key, key_schema in schema.items():
        section_214 = key_schema.get("section_214", None)
        schema_214 = {}
        if section_214:
            schema_214 = spec214.load_full_spec214(section_214, include_level0=True)[section_214]

        to_copy = bool(key_schema.get("copy", False))
        if to_copy:
            if key not in schema_214:
                raise ValueError(
                    f"Cannot find '{key}' in 214 section '{section_214}', but dataset extras expects it to exist."
                )

            key_schema_214 = schema_214[key]
            update_214 = dict(filter(lambda i: i[0] in import_keys, key_schema_214.items()))

            shared_keys = set(key_schema.keys()).intersection(set(update_214.keys()))
            if shared_keys:
                raise ValueError(
                    f"Collision in dataset extra and 214 schemas for {key}: {shared_keys = }"
                )

            schema[key] = {**key_schema, **update_214}

    return schema


def preprocess_schema(raw_schema: raw_schema_type_hint) -> frozendict[str, Any]:
    """
    Convert a single raw schema or a full dataset extra schema.

    Parameters
    ----------
    raw_schema
        The loaded version of a single yaml file.

    Returns
    -------
    schema
        The body of a schema, updated with the header and the relevant values
        from the 214 schema where appropriate.
    """
    # Merge in the keys in the header with all the keys
    schema = update_schema_with_header(raw_schema)  # makes a nested copy
    merged_spec = update_extra_with_214(schema)

    # Validate after we've updated with 214 keys. Saves a lot of redundant entries in the key schemas
    yamale.validate(full_schema_dataset_extras, [(merged_spec, None)])

    # Ensure the units in the comments are correct.
    # This performs two functions:
    # 1) Make sure all keys with units in their schema have units in the FITS comments.
    # 2) Ensure that if a unit is changed between 214 and dataset extra the comment is updated.
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


# No cache here; load_raw_spec is cached
def load_raw_dataset_extra(glob: str | None = None) -> frozendict[str, raw_schema_type_hint]:
    """
    Load the raw dataset extra schemas from the yaml files.

    Parameters
    ----------
    glob
        A pattern to use to match a file, without the ``.yml`` file extension.
        Can be a section name like ``'gos'``. `None` grabs all schema.

    Returns
    -------
    raw_schemas
        The schemas as loaded from the yaml files.
    """
    return load_raw_spec(BASE_PATH, glob)


@cache
def load_full_dataset_extra(glob: str | None = None) -> frozendict[str, schema_type_hint]:
    """
    Return the full loaded schemas for dataset extras

    Parameters
    ----------
    glob
        A pattern to use to match a file, without the ``.yml`` file extension.
        Can be a section name like ``'gos'``. `None` grabs all schema.

    """

    raw_schemas = load_raw_dataset_extra(glob)

    schemas = {}
    for schema_name, raw_schema in raw_schemas.items():
        schema = preprocess_schema(raw_schema)
        yamale.validate(full_schema_dataset_extras, [(schema, None)])
        schemas[schema_name] = schema

    return frozendict(schemas)


@cache
def load_sparse_dataset_extra(glob: str | None = None) -> frozendict[str, schema_type_hint]:
    # This is equivalent to `spec214.load_spec214`, but with a better name to explicitly label the point of each
    # `load_*_dataset_extra` function.
    """
    Load the simple schema version of dataset extra for validation or generation.

    I.e., the schema produced by this function is the "full" schema (see `load_full_dataset_extra`) with keys
    metadata not in the "spec_validation_schema" removed.

    The removed schema keys are those used for documentation and header formatting.

    Parameters
    ----------
    glob
        A pattern to use to match a file, without the ``.yml`` file extension.
        Can be a section name like ``'wcs'``.
    """

    full_schemas = load_full_dataset_extra(glob)

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


def load_processed_dataset_extra(
    glob: str | None = None, **header: dict[str, Any]
) -> dict[str, schema_type_hint]:
    """
    Load the dataset extras schema, processed based on a FITS header.

    This function applies conditional requiredness

    Parameters
    ----------
    glob
        A pattern to use to match a file, without the ``.yml`` file extension.
        Can be a section name like ``'wcs'``.

    header
       A FITS header to be used to expand the schema as needed.
    """
    schemas = load_sparse_dataset_extra(glob)
    processed_schemas = {}
    for section, schema in schemas.items():
        processed_schemas[section] = process_dataset_extra_section(schema, **header)

    return processed_schemas


def process_dataset_extra_section(
    schema: schema_type_hint, **header: dict[str, Any]
) -> schema_type_hint:
    """
    Apply requiredness to a single section of the dataset extras schema.
    """
    schema = update_dataset_extra_schema_requiredness(schema, **header)
    schema = expand_dataset_extra_schema(schema, **header)

    return schema


def define_dataset_extra_schema_expansions(**header: dict[str, Any]) -> list[ExpansionIndex]:
    """
    Collate the list of schema expansions to apply for dataset extras.
    """
    expansion_list = []
    if "NAXIS" in header.keys():
        n_expansion = ExpansionIndex(index="n", size=1, values=range(1, header["NAXIS"] + 1))
        expansion_list.append(n_expansion)

    # Compression keys
    if "ZIMAGE" in header:
        # The z index for ZNAMEz and ZVALz do not have a key which tells you how
        # many keys you have.
        zval = [k for k in header.keys() if k.startswith("ZVAL")]
        z_max = max([int(k[-1]) for k in zval])
        z_expansion = ExpansionIndex(index="z", size=1, values=range(1, z_max + 1))
        f_expansion = ExpansionIndex(index="f", size=1, values=range(1, header["TFIELDS"] + 1))
        expansion_list.extend([z_expansion, f_expansion])

    return expansion_list


def expand_dataset_extra_schema(
    schema: schema_type_hint, **header: dict[str, Any]
) -> dict[str, frozendict[str, Any]]:
    """
    Given a dataset extras header expand all known indices.
    """
    return expand_schema(schema=schema, expansions=define_dataset_extra_schema_expansions(**header))


def define_dataset_extra_conditional_requiredness(
    **header: dict[str, Any]
) -> list[ConditionalRequirement]:
    """
    Collate the list of conditional requirements to apply for dataset extras
    """
    requirements_list = []

    instrument_requirement = InstrumentRequired(header)
    requirements_list.append(instrument_requirement)

    return requirements_list


def update_dataset_extra_schema_requiredness(
    schema: schema_type_hint, **header: dict[str, Any]
) -> dict[str, frozendict[str, Any]]:
    """
    Given a header, update the "required" spec field based on presence/values of spec fields that indicate conditional requiredness.
    """

    return update_schema_requiredness(
        schema=schema, requirements=define_dataset_extra_conditional_requiredness(**header)
    )
