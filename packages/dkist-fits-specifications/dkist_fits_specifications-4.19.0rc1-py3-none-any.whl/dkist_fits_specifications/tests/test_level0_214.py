from dkist_fits_specifications.spec214.level0 import (
    load_level0_spec214,
    spec214_122_key_map,
)


def test_key_map():
    key_map = spec214_122_key_map()
    assert key_map["LINEWAV"] == "WAVELNTH"


def test_level0_spec():
    spec = load_level0_spec214(INSTRUME="visp")
    assert "WAVELNTH" in spec["fits"]
    assert spec["dataset"]["LINEWAV"]["rename"] == "WAVELNTH"

    assert "VSPNUMST" in spec["visp"]
    assert "VSPSTNUM" in spec["visp"]
    assert "IPTASK" in spec["dkist-op"]

    # Test expansion
    assert "NAXIS3" in spec["fits"]

    # Test instrument requiredness was applied for both 122 and 214 keys
    assert spec["visp"]["VSPARMID"]["required"] is True
    assert spec["visp"]["VISP_001"]["required"] is True
