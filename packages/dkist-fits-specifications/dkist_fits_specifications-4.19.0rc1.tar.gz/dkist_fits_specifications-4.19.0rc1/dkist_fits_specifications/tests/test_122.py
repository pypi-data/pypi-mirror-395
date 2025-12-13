from dkist_fits_specifications.spec122 import (
    define_122_schema_expansions,
    load_processed_spec122,
    load_raw_spec122,
    load_spec122,
)
from dkist_fits_specifications.utils.frozendict import frozendict


def test_load_raw_122():
    """
    Given: The raw SPEC-122 yamls
    When: Loading the raw yamls
    Then: The correct return types and structure are returned
    """
    spec = load_raw_spec122()
    assert isinstance(spec, frozendict)
    assert isinstance(spec["fits"], tuple)
    header, spec = spec["fits"]
    assert isinstance(header, frozendict)
    assert isinstance(spec["NAXIS"], frozendict)


def test_load_122():
    """
    Given: The raw SPEC-122 yamls
    When: Loading pre-processed spec sections
    Then: The section headers have been applied but expansion has NOT been done
    """
    spec = load_spec122()
    assert isinstance(spec, frozendict)
    assert isinstance(spec["fits"], frozendict)
    assert isinstance(spec["fits"]["NAXIS"], frozendict)

    # Make sure the header was applied
    assert spec["vbi"]["VBI__001"]["instrument_required"] == "VBI"
    assert spec["vbi"]["VBI__001"]["required"] is False

    # Make sure no expansion happened
    assert "NAXIS3" not in spec["fits"]
    assert "NAXIS<n>" in spec["fits"]
    assert "ZNAXIS<n>" in spec["compression"]
    assert "PC<i>_<j>" in spec["telescope"]


def test_load_processed_122():
    """
    Given: The raw SPEC-122 yamls and a header with an INSTRUME value
    When: Loading the fully-processed SPEC-122 schema
    Then: Expansion and conditional requiredness are correctly applied
    """
    spec = load_processed_spec122(INSTRUME="VBI")

    assert spec["vbi"]["VBI__001"]["required"] is True
    assert spec["visp"]["VISP_001"]["required"] is False

    # Make sure expansion worked. One key for each expansion index for each section *should* be fine
    # We use the max value for each index.
    assert "NAXIS3" in spec["fits"]
    assert "ZNAXIS3" in spec["compression"]
    assert "CRPIX3" in spec["telescope"]
    assert "PC3_3" in spec["telescope"]


def test_define_122_schema_expansion_duplication():
    """
    Given: the list of requested spec 122 expansions
    When: checking the indices for each expansion
    Then: None of them match (all expansions are unique)
    """
    expansions = define_122_schema_expansions()
    expansion_indices = [e.index for e in expansions]
    assert len(expansion_indices) == len(set(expansion_indices))
