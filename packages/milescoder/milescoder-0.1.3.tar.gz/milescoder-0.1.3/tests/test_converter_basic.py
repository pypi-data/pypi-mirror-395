import pytest
from milescoder.models import MILESData


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


def test_expected_encoded_string(miles_coder, minimal_test_data, expected_encoded_strings):
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