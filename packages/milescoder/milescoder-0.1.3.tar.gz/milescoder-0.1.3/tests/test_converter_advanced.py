from pydantic import ValidationError
import pytest
from milescoder.models import MILESData
from milescoder.converter import MILESCoder


def test_encode_decode_roundtrip(miles_coder, sample_test_data):
    """Test that encoding and then decoding returns the original data."""
    encoded = miles_coder.encode(sample_test_data)
    decoded = miles_coder.decode(encoded)
    # Check some key fields
    assert decoded["l0"]["material"] == "metal"
    assert decoded["l1"]["metal"] == "Mg"
    assert decoded["l2"]["alloy"]["nominalComposition"][0]["element"] == "Al"
    assert decoded["l3"]["hardness"]["nanoHardnessValues"] == [1, 2, 3]
    assert decoded["l4"]["pitting"]["pittingDepth"] == 2
    assert decoded["l5"]["pillingBedworthRatio"] == 1.5


def test_minimal_data_roundtrip(miles_coder, minimal_test_data):
    """Test roundtrip with minimal data."""
    encoded = miles_coder.encode(minimal_test_data)
    decoded = miles_coder.decode(encoded)
    assert decoded["l0"]["material"] == "metal"
    assert decoded["l1"]["metal"] == "Al"


def test_expected_encoded_string(
    miles_coder, minimal_test_data, expected_encoded_strings
):
    """Test that encoding minimal data matches expected string."""
    encoded = miles_coder.encode(minimal_test_data)
    assert encoded == expected_encoded_strings["minimal"]


def test_missing_layer(miles_coder):
    """Test encoding/decoding with a missing layer."""
    data_dict = {
        "l0": {"material": "metal"},
        # l1 is missing
        "l2": {"alloy": {"nominalComposition": [{"element": "Al", "content": 0.1}]}},
    }
    data = MILESData(**data_dict)
    encoded = miles_coder.encode(data)
    decoded = miles_coder.decode(encoded)
    assert "l1" not in decoded
    assert decoded["l0"]["material"] == "metal"
    assert decoded["l2"]["alloy"]["nominalComposition"][0]["element"] == "Al"


def test_invalid_data_type(miles_coder):
    """Test that encoding invalid data raises an error."""
    with pytest.raises((AttributeError, TypeError)):
        miles_coder.encode("not a dict")


def test_complex_alloy_data(miles_coder):
    """Test encoding/decoding with complex alloy information."""
    data_dict = {
        "l0": {"material": "metal"},
        "l1": {"metal": "Al"},
        "l2": {
            "alloy": {
                "materialID": "AA6061",
                "elementalComposition": [
                    {"element": "Al", "content": 97.9},
                    {"element": "Mg", "content": 1.0},
                    {"element": "Si", "content": 0.6},
                ],
                "hardeningPrecipitates": [
                    [
                        {"element": "Mg", "content": 50.0},
                        {"element": "Si", "content": 50.0},
                    ]
                ],
                "temperCode": "T6",
            }
        },
    }
    data = MILESData(**data_dict)
    encoded = miles_coder.encode(data)
    decoded = miles_coder.decode(encoded)

    assert decoded["l0"]["material"] == "metal"
    assert decoded["l1"]["metal"] == "Al"
    assert decoded["l2"]["alloy"]["materialID"] == "AA6061"
    assert decoded["l2"]["alloy"]["temperCode"] == "T6"
    assert len(decoded["l2"]["alloy"]["elementalComposition"]) == 3
    assert decoded["l2"]["alloy"]["hardeningPrecipitates"][0][0]["element"] == "Mg"


def test_heat_treatment_data(miles_coder):
    """Test encoding/decoding with heat treatment information."""
    data_dict = {
        "l0": {"material": "metal"},
        "l1": {"metal": "Al"},
        "l3": {
            "heatTreatment": {
                "heatTreatmentType": "annealing",
                "heatTreatmentTime": 2.0,
                "heatTreatmentTemperature": 400.0,
            }
        },
    }
    data = MILESData(**data_dict)
    encoded = miles_coder.encode(data)
    decoded = miles_coder.decode(encoded)

    assert decoded["l3"]["heatTreatment"]["heatTreatmentType"] == "annealing"
    assert decoded["l3"]["heatTreatment"]["heatTreatmentTime"] == 2.0
    assert decoded["l3"]["heatTreatment"]["heatTreatmentTemperature"] == 400.0


def test_corrosion_data(miles_coder):
    """Test encoding/decoding with corrosion parameters."""
    data_dict = {
        "l0": {"material": "metal"},
        "l1": {"metal": "Mg"},
        "l4": {
            "generalizedCorrosion": {
                "corrosionRate": 1.8,
            },
            "pitting": {
                "pitting": True,
                "pittingDepth": 15.2,
                "pittingWidth": 25.8,
            },
            "electrolyte": {
                "pH": [7.0, 6.5],
                "electrolyteVolume": 250.0,
            },
            "corrosionTemperature": 25.0,
        },
    }
    data = MILESData(**data_dict)
    encoded = miles_coder.encode(data)
    decoded = miles_coder.decode(encoded)

    assert decoded["l4"]["generalizedCorrosion"]["corrosionRate"] == 1.8
    assert decoded["l4"]["pitting"]["pitting"] is True
    assert decoded["l4"]["pitting"]["pittingDepth"] == 15.2
    assert decoded["l4"]["electrolyte"]["pH"] == [7.0, 6.5]
    assert decoded["l4"]["corrosionTemperature"] == 25.0


def test_ebsd_and_crystal_phase_data(miles_coder):
    """Test encoding/decoding with EBSD and crystal phase information."""
    data_dict = {
        "l0": {"material": "metal"},
        "l1": {"metal": "Al"},
        "l2": {
            "ebsd": {
                "crystalPhase": [
                    {
                        "phase": "FCC",
                        "composition": [
                            {"element": "Al", "content": 90.0},
                            {"element": "Cu", "content": 10.0},
                        ],
                    }
                ],
                "schmidFactor": 0.45,
            }
        },
    }
    data = MILESData(**data_dict)
    encoded = miles_coder.encode(data)
    decoded = miles_coder.decode(encoded)

    assert decoded["l2"]["ebsd"]["crystalPhase"][0]["phase"] == "FCC"
    assert decoded["l2"]["ebsd"]["crystalPhase"][0]["composition"][0]["element"] == "Al"
    assert decoded["l2"]["ebsd"]["schmidFactor"] == 0.45


def test_grains_data(miles_coder):
    """Test encoding/decoding with grain information."""
    data_dict = {
        "l0": {"material": "metal"},
        "l1": {"metal": "Ti"},
        "l2": {
            "grains": {
                "grainSize": 25.3,
            },
            "ebsd": {
                "crystalOrientation": {
                    "ipf": "X",
                    "suborientation": [{"percent": 45.2, "millerIndices": [1, 1, 1]}],
                }
            },
        },
    }
    data = MILESData(**data_dict)
    encoded = miles_coder.encode(data)
    print(f"Encoded grains data: {encoded}")
    decoded = miles_coder.decode(encoded)
    print(f"Decoded grains data: {decoded}")

    assert decoded["l2"]["grains"]["grainSize"] == 25.3
    assert decoded["l2"]["ebsd"]["crystalOrientation"]["ipf"] == "X"
    assert (
        decoded["l2"]["ebsd"]["crystalOrientation"]["suborientation"][0]["percent"]
        == 45.2
    )


def test_spectroscopy_data(miles_coder):
    """Test encoding/decoding with spectroscopy information."""
    data_dict = {
        "l0": {"material": "metal"},
        "l1": {"metal": "Al"},
        "l2": {
            "spectroscopy": {
                "raman": [520.0, 1580.0],
                "ftir": [1650.0, 2900.0],
                "xrd": [44.7, 65.0],
            }
        },
    }
    data = MILESData(**data_dict)
    encoded = miles_coder.encode(data)
    decoded = miles_coder.decode(encoded)

    assert decoded["l2"]["spectroscopy"]["raman"] == [520.0, 1580.0]
    assert decoded["l2"]["spectroscopy"]["ftir"] == [1650.0, 2900.0]
    assert decoded["l2"]["spectroscopy"]["xrd"] == [44.7, 65.0]


def test_surface_treatment_data(miles_coder):
    """Test encoding/decoding with surface treatment information."""
    data_dict = {
        "l0": {"material": "metal"},
        "l1": {"metal": "Al"},
        "l3": {
            "abraded": {"type": "SiC", "grade": 400},
            "polished": {"type": "diamond", "grade": 1000},
            "shotPeened": True,
        },
    }
    data = MILESData(**data_dict)
    encoded = miles_coder.encode(data)
    decoded = miles_coder.decode(encoded)

    assert decoded["l3"]["abraded"]["type"] == "SiC"
    assert decoded["l3"]["abraded"]["grade"] == 400
    assert decoded["l3"]["polished"]["type"] == "diamond"
    assert decoded["l3"]["polished"]["grade"] == 1000
    assert decoded["l3"]["shotPeened"] is True


def test_biocompatibility_data(miles_coder):
    """Test encoding/decoding with biocompatibility information."""
    data_dict = {
        "l0": {"material": "metal"},
        "l1": {"metal": "Ti"},
        "l4": {
            "inVivoTest": "rat",
            "implantationSite": "subcutaneous",
        },
    }
    data = MILESData(**data_dict)
    encoded = miles_coder.encode(data)
    decoded = miles_coder.decode(encoded)

    assert decoded["l4"]["inVivoTest"] == "rat"
    assert decoded["l4"]["implantationSite"] == "subcutaneous"


def test_additive_manufacturing_data(miles_coder):
    """Test encoding/decoding with additive manufacturing information."""
    data_dict = {
        "l0": {"material": "metal"},
        "l1": {"metal": "Ti"},
        "l5": {
            "additiveManufacturingDensity": 7.8,
            "additiveManufacturingCoverGas": "Ar",
            "additiveManufacturingEnvironment": "N",
            "pillingBedworthRatio": 1.5,
        },
    }
    data = MILESData(**data_dict)
    encoded = miles_coder.encode(data)
    decoded = miles_coder.decode(encoded)

    assert decoded["l5"]["additiveManufacturingDensity"] == 7.8
    assert decoded["l5"]["additiveManufacturingCoverGas"] == "Ar"
    assert decoded["l5"]["additiveManufacturingEnvironment"] == "N"
    assert decoded["l5"]["pillingBedworthRatio"] == 1.5


class TestMILESCoderInitialization:
    """Test MILESCoder initialization and basic properties."""

    def test_initialization(self):
        """Test MILESCoder initialization."""
        coder = MILESCoder()
        assert coder.version == "0.1A"
        assert len(coder.layer_models) == 6
        assert 0 in coder.layer_models
        assert len(coder.element_codes) > 100  # Should have all elements

    def test_element_codes_coverage(self):
        """Test that element codes cover major elements."""
        coder = MILESCoder()
        # Test some common elements
        assert coder.element_codes["H"] == "Hh"
        assert coder.element_codes["Al"] == "Al"
        assert coder.element_codes["Fe"] == "Fe"
        assert coder.element_codes["Cu"] == "Cu"


class TestEncodingEdgeCases:
    """Test encoding edge cases and error conditions."""

    def test_encode_empty_data(self, miles_coder):
        """Test encoding empty MILESData."""
        data = MILESData()
        encoded = miles_coder.encode(data)
        assert encoded == ""

    def test_encode_single_layer(self, miles_coder):
        """Test encoding single layer."""
        data = MILESData(l0={"material": "metal"})
        encoded = miles_coder.encode(data)
        assert "L0ME" in encoded

    def test_encode_boolean_fields(self, miles_coder):
        """Test encoding various boolean fields."""
        data = MILESData(
            l0={"material": "metal"},
            l3={
                "cast": True,
                "wrought": False,  # Should not appear in encoded string
                "shotPeened": True,
            },
        )
        encoded = miles_coder.encode(data)
        assert "CA" in encoded  # cast=True
        assert "SP" in encoded  # shotPeened=True
        # wrought=False should not appear

    def test_encode_numeric_fields(self, miles_coder):
        """Test encoding various numeric field types."""
        data = MILESData(
            l0={"material": "metal"},
            l3={
                "youngsModulus": 70.0,  # float
                "yieldStrength": 250,  # int
                "breakingElongation": 5.5,
            },
        )
        encoded = miles_coder.encode(data)
        assert "YM70.0" in encoded
        assert "YS250" in encoded
        assert "EG5.5" in encoded

    def test_encode_string_fields(self, miles_coder):
        """Test encoding string fields with quotes."""
        data = MILESData(
            l0={"material": "metal"},
            l3={"heatTreatment": {"heatTreatmentType": "annealing"}},
        )
        encoded = miles_coder.encode(data)
        assert 'HT"annealing"' in encoded

    def test_encode_element_fields(self, miles_coder):
        """Test encoding element fields."""
        data = MILESData(
            l0={"material": "metal"},
            l5={
                "additiveManufacturingCoverGas": "Ar",
                "additiveManufacturingEnvironment": "N",
            },
        )
        encoded = miles_coder.encode(data)
        assert "LGAr" in encoded
        assert "LENn" in encoded  # N gets encoded as Nn

    def test_encode_composition_lists(self, miles_coder):
        """Test encoding composition lists."""
        data = MILESData(
            l0={"material": "metal"},
            l2={
                "alloy": {
                    "nominalComposition": [
                        {"element": "Al", "content": 90.0},
                        {"element": "Cu", "content": 10.0},
                    ]
                }
            },
        )
        encoded = miles_coder.encode(data)
        assert "NC" in encoded
        assert "Al90.0Cu10.0" in encoded

    def test_encode_nested_composition_lists(self, miles_coder):
        """Test encoding nested composition lists (hardening precipitates)."""
        data = MILESData(
            l0={"material": "metal"},
            l2={
                "alloy": {
                    "hardeningPrecipitates": [
                        [
                            {"element": "Mg", "content": 50.0},
                            {"element": "Si", "content": 50.0},
                        ],
                        [
                            {"element": "Al", "content": 66.7},
                            {"element": "Cu", "content": 33.3},
                        ],
                    ]
                }
            },
        )
        encoded = miles_coder.encode(data)
        # Should have two HP entries
        hp_count = encoded.count("HP")
        assert hp_count == 2


class TestDecodingEdgeCases:
    """Test decoding edge cases and error conditions."""

    def test_decode_empty_string(self, miles_coder):
        """Test decoding empty string."""
        result = miles_coder.decode("")
        assert result == {}

    def test_decode_version_prefix(self, miles_coder):
        """Test decoding with version prefix."""
        result = miles_coder.decode("0.1A/L0ME/L1Al")
        assert result["l0"]["material"] == "metal"
        assert result["l1"]["metal"] == "Al"

    def test_decode_invalid_layer_format(self, miles_coder):
        """Test decoding with invalid layer format."""
        # Invalid layer should be skipped
        result = miles_coder.decode("INVALID/L0ME")
        assert "l0" in result
        assert result["l0"]["material"] == "metal"

    def test_decode_crystal_phases_multiple(self, miles_coder):
        """Test decoding multiple crystal phases."""
        encoded = 'L2CP"FCC"Al90.0Cu10.0CP"BCC"Fe100.0'
        result = miles_coder.decode(encoded)
        # The decoder puts crystal phases under ebsd
        assert len(result["l2"]["ebsd"]["crystalPhase"]) == 2
        assert result["l2"]["ebsd"]["crystalPhase"][0]["phase"] == "FCC"
        assert result["l2"]["ebsd"]["crystalPhase"][1]["phase"] == "BCC"

    def test_decode_complex_l3_parameters(self, miles_coder):
        """Test decoding complex L3 parameters."""
        encoded = "L0ME/L3YM70.0YS250CA"
        result = miles_coder.decode(encoded)
        assert result["l3"]["youngsModulus"] == 70.0
        assert result["l3"]["yieldStrength"] == 250
        assert result["l3"]["cast"] is True

    def test_decode_complex_l4_parameters(self, miles_coder):
        """Test decoding complex L4 parameters."""
        encoded = "L0ME/L4ET25.0PI"
        result = miles_coder.decode(encoded)
        assert result["l4"]["corrosionTemperature"] == 25.0
        assert result["l4"]["pitting"]["pitting"] is True

    def test_decode_with_unknown_codes(self, miles_coder):
        """Test decoding with unknown field codes."""
        encoded = "L0ME/L1Al/UNKNOWN123"
        result = miles_coder.decode(encoded)
        # Should still decode known parts
        assert result["l0"]["material"] == "metal"
        assert result["l1"]["metal"] == "Al"

    def test_decode_malformed_composition(self, miles_coder):
        """Test decoding malformed composition strings."""
        encoded = "L0ME/L2NCAlXXXCu10.0"  # Invalid content for Al
        result = miles_coder.decode(encoded)
        # Should handle gracefully, possibly skipping invalid entries
        assert "l0" in result
        assert result["l0"]["material"] == "metal"


class TestComplexScenarios:
    """Test complex real-world scenarios."""

    def test_aerospace_aluminum_alloy(self, miles_coder):
        """Test encoding/decoding aerospace aluminum alloy data."""
        data_dict = {
            "l0": {"material": "metal"},
            "l1": {"metal": "Al"},
            "l2": {
                "alloy": {
                    "materialID": "AA7075",
                    "nominalComposition": [
                        {"element": "Al", "content": 87.1},
                        {"element": "Zn", "content": 5.6},
                        {"element": "Mg", "content": 2.5},
                        {"element": "Cu", "content": 1.6},
                    ],
                    "temperCode": "T6",
                }
            },
            "l3": {
                "youngsModulus": 71.7,
                "yieldStrength": 503,
                "ultimateTensileStrength": 572,
                "heatTreatment": {
                    "heatTreatmentType": "quenching",
                    "heatTreatmentTemperature": 465.0,
                    "heatTreatmentTime": 2.0,
                },
            },
        }
        data = MILESData(**data_dict)
        encoded = miles_coder.encode(data)
        decoded = miles_coder.decode(encoded)

        assert decoded["l0"]["material"] == "metal"
        assert decoded["l1"]["metal"] == "Al"
        assert decoded["l2"]["alloy"]["materialID"] == "AA7075"
        assert decoded["l2"]["alloy"]["temperCode"] == "T6"
        assert decoded["l3"]["youngsModulus"] == 71.7
        assert decoded["l3"]["yieldStrength"] == 503

    def test_biomedical_titanium_implant(self, miles_coder):
        """Test encoding/decoding biomedical titanium implant data."""
        data_dict = {
            "l0": {"material": "metal"},
            "l1": {"metal": "Ti"},
            "l2": {
                "alloy": {
                    "materialID": "Ti6Al4V",
                    "nominalComposition": [
                        {"element": "Ti", "content": 89.0},
                        {"element": "Al", "content": 6.0},
                        {"element": "V", "content": 4.0},
                    ],
                }
            },
            "l3": {
                "youngsModulus": 113.8,
                "polished": {"type": "SiC", "grade": 2000},
            },
            "l4": {
                "inVivoTest": "rat",
                "implantationSite": "bone",
            },
        }
        data = MILESData(**data_dict)
        encoded = miles_coder.encode(data)
        decoded = miles_coder.decode(encoded)

        assert decoded["l0"]["material"] == "metal"
        assert decoded["l1"]["metal"] == "Ti"
        assert decoded["l2"]["alloy"]["materialID"] == "Ti6Al4V"
        assert decoded["l3"]["youngsModulus"] == 113.8
        assert decoded["l4"]["inVivoTest"] == "rat"
        assert decoded["l4"]["implantationSite"] == "bone"

    def test_additive_manufactured_steel(self, miles_coder):
        """Test encoding/decoding additive manufactured steel data."""
        data_dict = {
            "l0": {"material": "metal"},
            "l1": {"metal": "Fe"},
            "l2": {
                "alloy": {
                    "materialID": "316L",
                    "nominalComposition": [
                        {"element": "Fe", "content": 65.0},
                        {"element": "Cr", "content": 17.0},
                        {"element": "Ni", "content": 12.0},
                        {"element": "Mo", "content": 2.5},
                    ],
                }
            },
            "l3": {
                "youngsModulus": 200.0,
                "heatTreatment": {
                    "heatTreatmentType": "annealing",
                    "heatTreatmentTemperature": 650.0,
                    "heatTreatmentTime": 4.0,
                },
            },
            "l5": {
                "additiveManufacturingDensity": 7.9,
                "additiveManufacturingCoverGas": "Ar",
                "pillingBedworthRatio": 2.1,
            },
        }
        data = MILESData(**data_dict)
        encoded = miles_coder.encode(data)
        decoded = miles_coder.decode(encoded)

        assert decoded["l0"]["material"] == "metal"
        assert decoded["l1"]["metal"] == "Fe"
        assert decoded["l2"]["alloy"]["materialID"] == "316L"
        assert decoded["l3"]["youngsModulus"] == 200.0
        assert decoded["l5"]["additiveManufacturingDensity"] == 7.9
        assert decoded["l5"]["additiveManufacturingCoverGas"] == "Ar"


class TestErrorHandling:
    """Test error handling and edge cases in the converter."""

    def test_decode_empty_string(self, miles_coder):
        """Test decoding empty string."""
        result = miles_coder.decode("")
        assert result == {}

    def test_decode_invalid_format(self, miles_coder):
        """Test decoding completely invalid format."""
        result = miles_coder.decode("invalid-format-string")
        assert result == {}

    def test_decode_malformed_version(self, miles_coder):
        """Test decoding with malformed version prefix."""
        result = miles_coder.decode("invalid.version/L0ME")
        # Should still parse the layer part
        assert "l0" in result

    def test_encode_none_values(self, miles_coder):
        """Test encoding with None values."""
        data = MILESData(l0={"material": "metal"}, l1=None)
        encoded = miles_coder.encode(data)
        assert "L1" not in encoded

    def test_parse_composition_with_invalid_elements(self, miles_coder):
        """Test parsing composition with invalid element codes."""
        # This tests _parse_composition_string error handling
        result = miles_coder._parse_composition_string("XxYy50.0")  # Invalid elements
        # Should handle gracefully, possibly returning empty or skipping invalid parts
        assert isinstance(result, list)

    def test_parse_surface_treatment_malformed(self, miles_coder):
        """Test parsing malformed surface treatment."""
        result = miles_coder._parse_surface_treatment("malformed-input")
        assert isinstance(result, dict)
        assert "type" in result

    def test_find_value_end_at_string_end(self, miles_coder):
        """Test finding value end when at end of string."""
        result = miles_coder._find_value_end_generic("GS25.3", 2, {"GS"})
        assert result == 6  # Should go to end of string

    def test_collect_codes_with_circular_references(self, miles_coder):
        """Test that circular model references don't cause infinite recursion."""
        # This tests the seen_models protection in _collect_all_codes
        from milescoder.models import L2Parameters

        known_codes = set()
        code_to_field_info = {}
        # Should not raise RecursionError
        miles_coder._collect_all_codes(L2Parameters, known_codes, code_to_field_info)
        assert len(known_codes) > 0


class TestEncodingEdgeCases:
    """Test edge cases in encoding."""

    def test_encode_empty_lists(self, miles_coder):
        """Test encoding empty lists."""
        data = MILESData(
            l0={"material": "metal"},
            l2={"alloy": {"nominalComposition": []}},  # Empty composition
        )
        encoded = miles_coder.encode(data)
        # Should handle gracefully
        assert "L0ME" in encoded

    def test_encode_zero_values(self, miles_coder):
        """Test encoding with zero numeric values."""
        data = MILESData(l0={"material": "metal"}, l3={"youngsModulus": 0.0})
        encoded = miles_coder.encode(data)
        assert "YM0.0" in encoded

    def test_encode_very_long_strings(self, miles_coder):
        """Test encoding with very long string values."""
        long_string = "A" * 1000  # Exceeds 50 character limit

        with pytest.raises(ValidationError) as exc_info:
            MILESData(
                l0={"material": "metal"}, l2={"alloy": {"materialID": long_string}}
            )

        # Check that it's specifically a string_too_long error
        assert "string_too_long" in str(exc_info.value)
        assert "at most 50 characters" in str(exc_info.value)

    def test_valid_string_length_accepted(self, miles_coder):
        """Test that strings within length limits are accepted."""
        valid_string = "A" * 50  # Exactly at the limit

        # Should not raise an error
        data = MILESData(
            l0={"material": "metal"}, l2={"alloy": {"materialID": valid_string}}
        )

        encoded = miles_coder.encode(data)
        assert valid_string in encoded

    def test_encode_special_characters_in_strings(self, miles_coder):
        """Test encoding strings with special characters."""
        data = MILESData(
            l0={"material": "metal"}, l2={"alloy": {"materialID": "AA-6061/T6"}}
        )
        encoded = miles_coder.encode(data)
        assert "AA-6061T6" in encoded

    def test_encode_nested_empty_dicts(self, miles_coder):
        """Test encoding with nested empty dictionaries."""
        data = MILESData(
            l0={"material": "metal"}, l3={"heatTreatment": {}}  # Empty dict
        )
        encoded = miles_coder.encode(data)
        # Should handle gracefully
        assert "L0ME" in encoded


class TestComplexDecoding:
    """Test complex decoding scenarios."""

    def test_decode_multiple_crystal_phases(self, miles_coder):
        """Test decoding multiple crystal phases in sequence."""
        encoded = 'L2CP"FCC"Al90.0CP"BCC"Fe100.0'
        result = miles_coder.decode(encoded)

        # Should have parsed both crystal phases
        assert "l2" in result
        crystal_phases = result["l2"]["ebsd"]["crystalPhase"]
        assert len(crystal_phases) == 2
        assert crystal_phases[0]["phase"] == "FCC"
        assert crystal_phases[1]["phase"] == "BCC"

    def test_decode_mixed_field_types_in_sequence(self, miles_coder):
        """Test decoding various field types in sequence."""
        encoded = 'L3YM70.0CA"diamond"1000HT"annealing"'
        result = miles_coder.decode(encoded)

        assert result["l3"]["youngsModulus"] == 70.0
        assert result["l3"]["cast"] == True  # Boolean field
        # Add more assertions based on your field definitions

    def test_decode_with_all_special_characters(self, miles_coder):
        """Test decoding with all types of special characters."""
        encoded = 'L2NC"Material-ID/123"Al90.0Cu10.0'
        result = miles_coder.decode(encoded)
        # Should handle special characters in quoted strings
        # Add assertions based on expected behavior
