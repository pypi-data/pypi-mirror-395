import pytest

from dkist_fits_specifications.utils import frozendict
from dkist_fits_specifications.utils.spec_processors.expansion import (
    ExpansionIndex,
    expand_schema,
)


def test_expansion_index():
    """
    Given: a schema and a collection of ExpansionIndex instances
    When: when applying the expansions to the schema
    Then: expanded keys are replaced
    """
    # Single index size one expansion
    k_expansion = ExpansionIndex(index="k", size=1, values=range(1, 6))
    # Double index size two expansion
    nn_expansion = ExpansionIndex(index="nn", size=2, values=range(3, 6))
    # Single index larger size expansion
    q_expansion = ExpansionIndex(index="q", size=2, values=range(10, 16))
    # Custom range expansion
    custom_expansion_values = [1, 3, 6, 9, 13, 56]
    aa_expansion = ExpansionIndex(index="aa", size=2, values=custom_expansion_values)
    # Keys needing two expansions
    i_expansion = ExpansionIndex(index="i", size=1, values=range(1, 4))
    j_expansion = ExpansionIndex(index="j", size=1, values=range(1, 4))
    original_schema = frozendict(
        {
            "FOO<k>": {"a": 1, "b": 2},
            "OTHERKEY": {"c": 3, "d": 4},  # This key is not expanded
            "BAR<nn>": {"e": 5, "f": 6},
            "CUSTOM<aa>": {"g": 7, "h": 8},
            "PC<i>_<j>": {"i": 9, "j": 10},
            "QQQ<q>": {"k": 11, "l": 12},
        }
    )
    expanded_schema = expand_schema(
        schema=original_schema,
        expansions=[k_expansion, nn_expansion, aa_expansion, i_expansion, j_expansion, q_expansion],
    )

    for i in range(1, 6):
        assert f"FOO{i}" in expanded_schema
    for j in range(3, 6):
        assert f"BAR{str(j).zfill(2)}" in expanded_schema
    for k in custom_expansion_values:
        assert f"CUSTOM{str(k).zfill(2)}" in expanded_schema
    for q in range(10, 16):
        assert f"QQQ{q}" in expanded_schema
    assert "OTHERKEY" in expanded_schema
    for key in original_schema.keys():
        if "<" in key:
            assert key not in expanded_schema


def test_expansion_making_a_key_too_long():
    """
    Given: a schema and an expansion
    When: the expansion makes the keyword longer than allowed by FITS
    Then: an error is raised
    """
    k_expansion = ExpansionIndex(index="k", size=2, values=range(1, 12))
    schema = frozendict(
        {
            "FOOBARS<k>": {"a": 1, "b": 2},
        }
    )
    with pytest.raises(ValueError):
        _ = expand_schema(schema=schema, expansions=[k_expansion])


def test_expansion_with_values_greater_than_size():
    """
    Given: a schema and an expansion
    When: the expansion takes up more size than given by the 'size' keyword
    Then: an error is raised
    """
    with pytest.raises(ValueError):
        _ = ExpansionIndex(index="k", size=2, values=range(1, 101))
