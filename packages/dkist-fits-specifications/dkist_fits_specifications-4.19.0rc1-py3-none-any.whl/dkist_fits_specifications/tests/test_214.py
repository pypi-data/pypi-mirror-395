from typing import Any

import pytest

from dkist_fits_specifications.spec214 import (
    define_214_schema_expansions,
    get_214_l0_only_keys,
    load_full_spec214,
    load_processed_spec214,
    load_spec214,
)
from dkist_fits_specifications.utils.frozendict import frozendict


def test_load_full_214():
    spec = load_full_spec214()
    visp = spec["visp"]
    assert "VSPNUMST" not in visp
    assert "VSPSTNUM" not in visp
    assert "IPTASK" not in spec["dkist-op"]
    assert isinstance(spec, frozendict)
    assert isinstance(spec["fits"], frozendict)
    assert isinstance(spec["fits"]["NAXIS"], frozendict)

    # No sections should be empty
    for key in spec:
        assert spec[key], f"The {key} section is empty"


def test_load_214():
    spec = load_spec214()
    assert isinstance(spec, frozendict)
    assert isinstance(spec["fits"], frozendict)
    assert isinstance(spec["fits"]["NAXIS"], frozendict)


def test_load_processed_214_with_no_header():
    """
    Given: Spec schemas produced by `load_spec214` and `load_processed_spec214` WITHOUT an input header
    When: Comparing the two schemas
    Then: They are the same modulo expansion keys
    """
    non_processed_spec = load_spec214()
    processed_spec = load_processed_spec214()

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


def test_expanded_schema():
    schemas = load_processed_spec214(
        DAAXES=2,
        DEAXES=1,
        NAXIS=3,
        DNAXIS=5,
        ZIMAGE=True,
        ZVAL1=1,
        ZVAL2=2,
        ZVAL3=3,
        TFIELDS=5,
        NPROPOS=2,
        NEXPERS=5,
        INSTRUME="notthedkist",
    )
    assert "DINDEX3" in schemas["dataset"]
    assert "NAXIS1" in schemas["fits"]
    assert "DTYPE5" in schemas["dataset"]
    assert "EXPRID05" in schemas["dkist-id"]
    assert "PROPID02" in schemas["dkist-id"]
    for percentile in [1, 10, 25, 75, 90, 95, 98, 99]:
        assert f"DATAP{str(percentile).zfill(2)}" in schemas["stats"]
    assert "ZNAME3" in schemas["compression"]
    assert "TFORM4" in schemas["compression"]
    assert "CRPIX3" in schemas["telescope"]
    assert "CRPIX3A" in schemas["telescope"]
    assert "NBIN3" in schemas["camera"]
    for i in range(1, 4):
        for j in range(1, 4):
            assert f"PC{i}_{j}" in schemas["telescope"]


def test_expanded_schema_deaxes0():
    schemas = load_processed_spec214(
        DAAXES=2,
        DEAXES=0,
        NAXIS=2,
        DNAXIS=2,
        NPROPOS=2,
        NEXPERS=5,
        INSTRUME="notthedkist",
    )
    assert "DEAXES" in schemas["dataset"]
    assert "DINDEX1" not in schemas["dataset"]


def test_define_214_schema_expansion_duplication():
    """
    Given: the list of requested spec 214 expansions
    When: checking the indices for each expansion
    Then: None of them match (all expansions are unique)
    """
    expansions = define_214_schema_expansions(
        DAAXES=2,
        DEAXES=1,
        NAXIS=3,
        DNAXIS=5,
        ZIMAGE=True,
        ZVAL1=1,
        ZVAL2=2,
        ZVAL3=3,
        TFIELDS=5,
        NPROPOS=2,
        NEXPERS=5,
        INSTRUME="notthedkist",
    )
    expansion_indices = [e.index for e in expansions]
    assert len(expansion_indices) == len(set(expansion_indices))


@pytest.mark.parametrize("instrument", ["vbi", "vtf"])
def test_instrument_required(instrument):
    """
    Given: An instrument table yaml and a header with INSTRUME set to that instrument
    When: Building the 214 schema
    Then: All keys from the instrument table are set to "required"
    """
    instrument_schema = load_processed_spec214(glob=instrument.lower(), INSTRUME=instrument)[
        instrument.lower()
    ]
    for spec_fields in instrument_schema.values():
        assert spec_fields.get("required", False)


@pytest.mark.parametrize("instrument", ["cryo-nirsp", "dl-nirsp", "vbi", "visp", "vtf"])
def test_instrument_not_required(instrument):
    """
    Given: An instrument table yaml and a header with INSTRUME set to NOT that instrument
    When: Building the 214 schema
    Then: All keys from the instrument table are NOT set to "required"
    """
    glob_name = instrument.lower().replace(
        "-", ""
    )  # For cryo and dl b/c the yamls don't have dashes

    instrument_schema = load_processed_spec214(glob=glob_name, INSTRUME="notthedkist")[glob_name]
    for spec_key_fields in instrument_schema.values():
        assert not spec_key_fields.get("required", True)


@pytest.fixture(scope="session")
def cryo_polarimetric_headers() -> dict[str, Any]:
    return {"INSTRUME": "cryo-nirsp", "CNMODNST": 2, "CNSPINMD": "Stepped"}


@pytest.fixture(scope="session")
def dl_polarimetric_headers() -> dict[str, Any]:
    return {"INSTRUME": "dl-nirsp", "DLPOLMD": "Full Stokes"}


@pytest.fixture(scope="session")
def visp_polarimetric_headers() -> dict[str, Any]:
    return {"INSTRUME": "visp", "VSPPOLMD": "observe_polarimetric"}


@pytest.mark.parametrize(
    "header_fixture",
    [
        pytest.param("cryo_polarimetric_headers", id="cryo-nirsp"),
        pytest.param("dl_polarimetric_headers", id="dl-nirsp"),
        pytest.param("visp_polarimetric_headers", id="visp"),
    ],
)
def test_polarimetric_required(header_fixture, request):
    """
    Given: The 214 tables and a header corresponding to a polarimetric dataset
    When: Building the 214 schema
    Then: All keys marked `polarimetric_required` have `required` set to True
    """
    header_vals = request.getfixturevalue(header_fixture)
    pol_schema = load_processed_spec214(glob="pac", **header_vals)["pac"]

    target_keys = ["POL_NOIS", "POL_SENS", "STOKES"]
    for spec_key in target_keys:
        assert pol_schema[spec_key].get("required", False)


@pytest.fixture(scope="session")
def cryo_non_polarimetric_headers() -> dict[str, Any]:
    return {"INSTRUME": "cryo-nirsp", "CNMODNST": 1, "CNSPINMD": "Foo"}


@pytest.fixture(scope="session")
def dl_non_polarimetric_headers() -> dict[str, Any]:
    return {"INSTRUME": "dl-nirsp", "DLPOLMD": "Stokes-I"}


@pytest.fixture(scope="session")
def visp_non_polarimetric_headers() -> dict[str, Any]:
    return {"INSTRUME": "visp", "VSPPOLMD": "observe_intensity"}


@pytest.fixture(scope="session")
def vbi_non_polarimetric_headers() -> dict[str, Any]:
    return {"INSTRUME": "vbi"}


@pytest.mark.parametrize(
    "header_fixture",
    [
        pytest.param("cryo_non_polarimetric_headers", id="cryo-nirsp"),
        pytest.param("dl_non_polarimetric_headers", id="dl-nirsp"),
        pytest.param("visp_non_polarimetric_headers", id="visp"),
        pytest.param("vbi_non_polarimetric_headers", id="vbi"),
    ],
)
def test_polarimetric_not_required(header_fixture, request):
    """
    Given: The 214 tables and a header corresponding to a NON-polarimetric dataset
    When: Building the 214 schema
    Then: All keys marked `polarimetric_required` have `required` set to False
    """
    header_vals = request.getfixturevalue(header_fixture)
    pol_schema = load_processed_spec214(glob="pac", **header_vals)["pac"]

    target_keys = ["POL_NOIS", "POL_SENS"]
    for spec_key in target_keys:
        assert not pol_schema[spec_key].get("required", True)


"""def test_spec_122_section():
    schemas = load_expanded_spec214(DAAXES=2, DEAXES=1, NAXIS=2, DNAXIS=5, INSTRUME="notthedkist")
    assert 'copy122' in schemas
    assert 'DATE-OBS' in schemas['copy122']"""


def test_level0_only_keys():
    """
    Given: SPEC-0214
    When: Requesting the header keys marked as `level0_only`
    Then: The correct set of keys are returned
    """
    keys = get_214_l0_only_keys()
    assert set(keys) == {
        "CNMODCST",
        "CNMODANG",
        "CNOFFANG",
        "CNCNDR",
        "CNCRAMP",
        "IPTASK",
        "VSPNUMST",
        "VSPSTNUM",
        "DLMODN",
        "DLMDANG",
        "DLSTNUM",
        "DLCURDAT",
        "DLCAMCUR",
    }
