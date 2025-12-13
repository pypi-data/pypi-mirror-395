from random import randint

import pytest
from astropy.io import fits

from dkist_fits_specifications.dataset_extras import load_processed_dataset_extra
from dkist_fits_specifications.spec214 import load_processed_spec214
from dkist_fits_specifications.utils.formatter import (
    reformat_dataset_extra_header,
    reformat_spec214_header,
)


@pytest.fixture
def header_with_all_214_sections() -> fits.Header:
    all_214_schemas = load_processed_spec214()
    header_dict = dict()
    for section in all_214_schemas.values():
        # Value doesn't matter at all, so just make it a random int
        header_dict.update({k: randint(1, 10) for k in section.keys()})

    # Manual intervention needed on these keys so header processors will work correctly
    del header_dict["END"]
    header_dict["DAAXES"] = 3
    header_dict["DEAXES"] = 2
    header_dict["DNAXIS"] = 5
    header_dict["NPROPOS"] = 10
    header_dict["NEXPERS"] = 11
    header_dict["NAXIS"] = 3
    header_dict["ZVAL1"] = 1
    header_dict["TFIELDS"] = 2
    header_dict["NSPECLNS"] = 13
    header = fits.Header(header_dict)

    header.add_history("This is a test history entry.")

    # Add a comment. Choosing "BUNIT" because it doesn't otherwise have a comment
    header.comments["BUNIT"] = "Wibble"
    # And overwrite a comment for a key that would get a default comment
    header.comments["TELTRACK"] = "NOT the default comment"

    return header


@pytest.fixture
def header_with_all_dataset_extra_sections() -> fits.Header:
    all_dataset_extras_schemas = load_processed_dataset_extra()
    header_dict = dict()
    for section in all_dataset_extras_schemas.values():
        # Value doesn't matter at all, so just make it a random int
        header_dict.update({k: randint(1, 10) for k in section.keys()})

    # Manual intervention needed on these keys so header processors will work correctly
    del header_dict["END"]
    header_dict["NAXIS"] = 3
    header_dict["ZVAL1"] = 1
    header_dict["TFIELDS"] = 2
    header = fits.Header(header_dict)

    header.add_history("This is a test history entry.")

    # Add a comment. Choosing "BUNIT" because it doesn't otherwise have a comment
    header.comments["BUNIT"] = "Wibble"
    # And overwrite a comment for a key that would get a default comment
    header.comments["TELTRACK"] = "NOT the default comment"

    return header


def test_214_formatter(header_with_all_214_sections):
    """
    Given: A 214 header with all possible schema sections
    When: Formatting the header
    Then: The dang thing runs and comments are preserved
    """
    output_header = reformat_spec214_header(header_with_all_214_sections)
    assert isinstance(output_header, fits.Header)
    assert output_header.comments["BUNIT"] == "Wibble"
    assert output_header.comments["TELTRACK"] == "NOT the default comment"

    # Make sure a default comment was set when no comments existed in input header
    assert output_header.comments["TAZIMUTH"] != ""

    # Make sure multiple history entries are preserved
    assert "This is a test history entry." in str(output_header["HISTORY"])
    assert str(output_header["HISTORY"]) != "This is a test history entry."


def test_dataset_extras_formatter(header_with_all_dataset_extra_sections):
    """
    Given: A dataset extras header with all possible schema sections
    When: Formatting the header
    Then: The dang thing runs and comments are preserved
    """
    output_header = reformat_dataset_extra_header(header_with_all_dataset_extra_sections)
    assert isinstance(output_header, fits.Header)
    assert output_header.comments["BUNIT"] == "Wibble"
    assert output_header.comments["TELTRACK"] == "NOT the default comment"

    # Make sure a default comment was set when no comments existed in input header
    assert output_header.comments["OBSPR_ID"] != ""

    # Make sure multiple history entries are preserved
    assert "This is a test history entry." in str(output_header["HISTORY"])
    assert str(output_header["HISTORY"]) != "This is a test history entry."
