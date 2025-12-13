import pytest

from dkist_fits_specifications.dataset_extras import (
    load_full_dataset_extra,
    load_processed_dataset_extra,
    load_sparse_dataset_extra,
)
from dkist_fits_specifications.spec214 import load_full_spec214
from dkist_fits_specifications.utils import frozendict


def test_update_with_214():
    """
    Given: The dataset extras schema files
    When: Loading the full schema
    Then: Fields that should be copied from 214 keys are correctly copied
    """
    dataset_extra_spec = load_full_dataset_extra()
    spec_214 = load_full_spec214(include_level0=True)
    import_keys = [
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
    ]
    for section in dataset_extra_spec.keys():
        for key, schema in dataset_extra_spec[section].items():
            if "section_214" in schema:
                schema_214 = spec_214[schema["section_214"]][key]
                for schema_key in import_keys:
                    if schema_key in schema_214:
                        assert (
                            schema[schema_key] == schema_214[schema_key]
                        ), f"Value for '{schema_key}' do not match for {key}"


def test_not_increasing_requiredness_of_214_keys():
    """
    Given: The full schema for 214 and dataset extras
    When: Comparing keys that are the same in both schemas
    Then: Ensure that any non-required keys in 214 are NOT required in dataset extras
    """
    dataset_extra_spec = load_full_dataset_extra()
    spec_214 = load_full_spec214(include_level0=True)
    tightened_keys = []
    for section in dataset_extra_spec.keys():
        for key, schema in dataset_extra_spec[section].items():
            if "section_214" in schema:
                schema_214 = spec_214[schema["section_214"]][key]
                if (schema_214["required"], schema["required"]) == (
                    False,
                    True,
                ):
                    tightened_keys.append(key)

    assert len(tightened_keys) == 0, f"Tightened requiredness on keys {tightened_keys}"


def test_load_full_dataset_extra():
    """
    Given: The dataset extras schema files
    When: Loading the full schema with `load_full_dataset_extra`
    Then: The schemas load and are valid
    """
    spec = load_full_dataset_extra()
    assert isinstance(spec, frozendict)
    assert isinstance(spec["fits"], frozendict)
    assert isinstance(spec["fits"]["NAXIS"], frozendict)

    # No sections should be empty
    for key in spec:
        assert spec[key], f"The {key} section is empty"


def test_load_sparse_dataset_extra():
    """
    Given: The dataset extras schema files
    When: Loading the sparse schema
    Then: The schemas load, are valid, and don't contain any "non-sparse" keys
    """
    spec = load_sparse_dataset_extra()
    assert isinstance(spec, frozendict)
    assert isinstance(spec["fits"], frozendict)
    assert isinstance(spec["fits"]["NAXIS"], frozendict)

    for section_schema in spec.values():
        for key, key_schema in section_schema.items():
            assert "description" not in key_schema
            assert "units" not in key_schema
            assert "fitsreference" not in key_schema
            assert "title" not in key_schema
            assert "summary" not in key_schema
            assert "long_description" not in key_schema


def test_load_processed_dataset_extra_with_no_header():
    """
    Given: Spec schemas produced by `load_sparse_dataset_extra` and `load_processed_dataset_extra` WITHOUT an input header
    When: Comparing the two schemas
    Then: They are the same modulo expansion keys (really just NAXIS in this case)
    """
    non_processed_spec = load_sparse_dataset_extra()
    processed_spec = load_processed_dataset_extra()

    thawed_non_processed_spec = {
        k: {k2: dict(v2) for k2, v2 in v.items()} for k, v in non_processed_spec.items()
    }
    thawed_processed_spec = {
        k: {k2: dict(v2) for k2, v2 in v.items()} for k, v in processed_spec.items()
    }

    assert thawed_non_processed_spec.keys() == thawed_processed_spec.keys()

    # yml level. e.g., 'pac'
    for k, v in thawed_processed_spec.items():
        expansion_prefixes_to_rm = [
            kk.split("<")[0] for kk in non_processed_spec[k].keys() if "<" in kk
        ]
        non_processed_spec_expansion_removed = {
            kk: vv
            for kk, vv in thawed_non_processed_spec[k].items()
            if not any([kk.startswith(ek) for ek in expansion_prefixes_to_rm])
        }
        processed_spec_expansion_removed = {
            kk: vv
            for kk, vv in v.items()
            if not any([kk.startswith(ek) for ek in expansion_prefixes_to_rm])
        }

        assert (
            processed_spec_expansion_removed.keys() == non_processed_spec_expansion_removed.keys()
        )

        # key level. e.g., 'STOKES'
        for k2, v2 in processed_spec_expansion_removed.items():

            # spec_fields level. e.g., 'required`
            for k3, v3 in v2.items():
                assert non_processed_spec_expansion_removed[k2][k3] == v3


def test_expanded_dataset_extra_schema():
    """
    Given: A header with axis and compression values indicating multiple axes
    When: Using that header to process the dataset extras spec
    Then: The correct expansions are applied
    """
    schemas = load_processed_dataset_extra(
        NAXIS=3,
        ZIMAGE=True,
        ZVAL1=1,
        ZVAL2=2,
        ZVAL3=3,
        TFIELDS=5,
    )
    assert "NAXIS1" in schemas["fits"]
    assert "NAXIS2" in schemas["fits"]
    assert "NAXIS3" in schemas["fits"]
    assert "ZNAXIS1" in schemas["compression"]
    assert "ZNAXIS2" in schemas["compression"]
    assert "ZNAXIS3" in schemas["compression"]
    assert "ZTILE1" in schemas["compression"]
    assert "ZTILE2" in schemas["compression"]
    assert "ZTILE3" in schemas["compression"]
    assert "ZNAME3" in schemas["compression"]
    assert "TFORM4" in schemas["compression"]


@pytest.mark.parametrize("instrument", ["visp", "cryo-nirsp", "dl-nirsp"])
def test_dataset_extra_instrument_required(instrument):
    """
    Given: An instrument table yaml and a header with INSTRUME set to that instrument
    When: Building the dataset extra schema
    Then: All keys from the instrument table are set to "required"
    """
    glob_name = instrument.lower().replace("-", "")
    instrument_schema = load_processed_dataset_extra(glob=glob_name, INSTRUME=instrument)[glob_name]
    for spec_fields in instrument_schema.values():
        assert spec_fields.get("required", False)


@pytest.mark.parametrize("instrument", ["cryo-nirsp", "dl-nirsp", "visp"])
def test_dataset_extra_instrument_not_required(instrument):
    """
    Given: An instrument table yaml and a header with INSTRUME set to NOT that instrument
    When: Building the dataset extra schema
    Then: All keys from the instrument table are NOT set to "required"
    """
    glob_name = instrument.lower().replace(
        "-", ""
    )  # For cryo and dl b/c the yamls don't have dashes

    instrument_schema = load_processed_dataset_extra(glob=glob_name, INSTRUME="notthedkist")[
        glob_name
    ]
    for spec_key_fields in instrument_schema.values():
        assert not spec_key_fields.get("required", True)
