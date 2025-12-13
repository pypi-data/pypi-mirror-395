"""
Functions for formatting FITS headers.
"""
import textwrap
from typing import Any
from functools import partial

from astropy.io import fits

from dkist_fits_specifications.dataset_extras import (
    expand_dataset_extra_schema,
    load_full_dataset_extra,
    load_raw_dataset_extra,
)
from dkist_fits_specifications.spec214 import (
    expand_214_schema,
    load_full_spec214,
    load_raw_spec214,
)

__all__ = [
    "reformat_spec214_header",
    "reformat_dataset_extra_header",
    "HEADER_SECTION_ORDER_214",
    "HEADER_SECTION_ORDER_DATASET_EXTRAS",
]

from dkist_fits_specifications.utils import schema_type_hint

HEADER_SECTION_ORDER_214 = [
    "fits",
    "telescope",
    "datacenter",
    "dataset",
    "stats",
    "dkist-id",
    "dkist-op",
    "camera",
    "pac",
    "ao",
    "wfc",
    "ws",
    "vbi",
    "visp",
    "cryonirsp",
    "dlnirsp",
    "vtf",
    "compression",
]

HEADER_SECTION_ORDER_DATASET_EXTRAS = [
    "fits",
    "common",
    "aggregate",
    "ip_task",
    "gos",
    "wavecal",
    "atlas",
    "visp",
    "cryonirsp",
    "dlnirsp",
    "compression",
]


def _get_comment(key, spec, input_header):
    """
    Get the comment from the various places the comment could be.

    Order of precedence is:

    1. Any comment in the input header
    2. The `comment` field in a key's schema
    3. Empty
    """
    # `input_header.comments` contains *all* keys and if the key doesn't have a comment the value is ""
    OG_comment = input_header.comments[key]
    return OG_comment or spec[key].get("comment") or None


def symmetrically_pad(string, width=72, filler="-"):
    """
    Pad a string with filler on both the left and right.
    """
    # If we have more than one line, then wrap the lines and pad each individual line
    if len(string) > width:
        # subtract from width 2 to always have one filler at each end
        lines = textwrap.wrap(string, width=width - 2)
        return "".join(map(partial(symmetrically_pad, width=width, filler=filler), lines))

    string = f" {string} "
    left_pad = int((width - len(string)) / 2)
    string = f"{string :{filler}>{left_pad + len(string)}}"
    string = f"{string :{filler}<{width}}"
    return string


def format_spec_section(
    input_header: fits.Header,
    section_name: str,
    spec: schema_type_hint,
    spec_preamble: dict[str, Any],
    output_header: fits.Header,
) -> None:
    """
    Format a single section of the spec and place it into `output_header`.
    """
    # Skip a section if we have no keys for that section
    if not any([key in input_header for key in spec.keys()]):
        return

    # Don't mess around with default FITS keys
    if section_name not in ["fits", "compression"]:
        output_header.add_blank(after=-1)
        output_header.add_comment(symmetrically_pad(spec_preamble["title"]), after=-1)
        if "summary" in spec_preamble:
            output_header.add_comment(
                symmetrically_pad(spec_preamble["summary"], filler=" "), after=-1
            )
        output_header.add_comment("-" * 72, after=-1)

    for key in spec.keys():
        if key not in input_header or key in output_header:
            continue
        if key == "HISTORY":
            history_entry = str(input_header[key]).replace("\n", " ")
            output_header.add_history(value=history_entry)
        else:
            output_header.append(
                fits.Card(
                    key=key,
                    value=input_header[key],
                    comment=_get_comment(key, spec, input_header),
                ),
                end=True,
            )


def reformat_spec214_header(input_header):
    """
    Using the information in the yamls reformat a 214 FITS header.

    This adds title and summary fields in the yamls as comment blocks between
    the sections as well as ordering the keys according to their order in the
    specifications.
    """
    spec214 = load_full_spec214()
    output_header = fits.Header()
    for section in HEADER_SECTION_ORDER_214:
        spec = spec214[section]
        spec = expand_214_schema(spec, **dict(input_header))
        spec_preamble = load_raw_spec214(section)[section][0]["spec214"]

        format_spec_section(
            input_header=input_header,
            spec=spec,
            spec_preamble=spec_preamble,
            section_name=section,
            output_header=output_header,
        )

    unformatted_keys = set(input_header.keys()).difference(output_header.keys())
    if unformatted_keys:
        raise ValueError(
            "Some keys have not been formatted, which means"
            f" they are not present in the specification:\n {unformatted_keys}"
        )
    return output_header


def reformat_dataset_extra_header(input_header):
    """
    Using the information in the yamls reformat a dataset extras FITS header.

    This adds title and summary fields in the yamls as comment blocks between
    the sections as well as ordering the keys according to their order in the
    specifications.
    """
    extra_spec = load_full_dataset_extra()
    output_header = fits.Header()
    for section in HEADER_SECTION_ORDER_DATASET_EXTRAS:
        spec = extra_spec[section]
        spec = expand_dataset_extra_schema(spec, **dict(input_header))
        spec_preamble = load_raw_dataset_extra(section)[section][0]["dsextra"]

        format_spec_section(
            input_header=input_header,
            spec=spec,
            spec_preamble=spec_preamble,
            section_name=section,
            output_header=output_header,
        )

    unformatted_keys = set(input_header.keys()).difference(output_header.keys())
    if unformatted_keys:
        raise ValueError(
            "Some keys have not been formatted, which means"
            f" they are not present in the specification:\n {unformatted_keys}"
        )
    return output_header
