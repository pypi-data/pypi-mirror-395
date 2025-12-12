import pytest
from typing import List, Optional
from milescoder.models import HeatTreatmentType


class TestUtilityMethods:
    """Test utility methods in MILESCoder."""
    
    def test_extract_enum_value(self, miles_coder):
        """Test _extract_enum_value method."""
        # Test enum with .value
        enum_val = HeatTreatmentType.annealing
        result = miles_coder._extract_enum_value(enum_val)
        assert result == "annealing"
        
        # Test string with class prefix
        result = miles_coder._extract_enum_value("HeatTreatmentType.annealing")
        assert result == "annealing"
        
        # Test plain string
        result = miles_coder._extract_enum_value("plain_string")
        assert result == "plain_string"
        
        # Test None
        result = miles_coder._extract_enum_value(None)
        assert result == ""

    def test_element_encoding_decoding(self, miles_coder):
        """Test element encoding and decoding."""
        # Test encoding
        encoded = miles_coder._encode_element("Al")
        assert encoded == "Al"
        
        encoded = miles_coder._encode_element("N")
        assert encoded == "Nn"
        
        # Test composition encoding
        composition = [
            {"element": "Al", "content": 90.0},
            {"element": "Cu", "content": 10.0}
        ]
        encoded_comp = miles_coder._encode_element_composition(composition)
        assert "Al90.0Cu10.0" == encoded_comp

    def test_parse_composition_string(self, miles_coder):
        """Test _parse_composition_string method."""
        # Test simple composition
        result = miles_coder._parse_composition_string("Al90.0Cu10.0")
        assert len(result) == 2
        assert result[0]["element"] == "Al"
        assert result[0]["content"] == 90.0
        
        # Test composition with single content
        result = miles_coder._parse_composition_string("AlCu")
        assert len(result) == 2
        assert result[0]["content"] == 1
        assert result[1]["content"] == 1

    def test_field_type_utilities(self, miles_coder):
        """Test field type utility methods."""
        # Test _is_list_type
        assert miles_coder._is_list_type(List[str]) == True
        assert miles_coder._is_list_type(str) == False
        assert miles_coder._is_list_type(None) == False
        
        # Test _is_nested_list_type
        assert miles_coder._is_nested_list_type(List[List[str]]) == True
        assert miles_coder._is_nested_list_type(List[str]) == False

    def test_encode_field_with_no_miles_metadata(self, miles_coder):
        """Test _encode_field with field that has no miles metadata."""
        # Create a mock field_info without miles metadata
        class MockFieldInfo:
            def __init__(self):
                self.json_schema_extra = {}
        
        field_info = MockFieldInfo()
        result = miles_coder._encode_field("test_field", "test_value", field_info)
        assert result == []  # Should return empty list

    def test_surface_treatment_encoding(self, miles_coder):
        """Test surface treatment encoding edge cases."""
        # Test with just type, no grade
        result = miles_coder._encode_surface_treatment({"type": "SiC"}, "AB")
        assert result == 'AB"SiC"'
        
        # Test with type and grade
        result = miles_coder._encode_surface_treatment(
            {"type": "diamond", "grade": 400}, "PO"
        )
        assert 'PO"diamond"400' in result


class TestErrorHandling:
    """Test error handling and edge cases."""
    
    def test_decode_malformed_layer_strings(self, miles_coder):
        """Test decoding with malformed layer strings."""
        # Missing layer number
        result = miles_coder.decode("L/ME")
        assert result == {}
        
        # Non-numeric layer
        result = miles_coder.decode("LXME")
        assert result == {}

    def test_decode_with_missing_closing_quotes(self, miles_coder):
        """Test decoding with missing closing quotes."""
        # Should handle gracefully
        result = miles_coder.decode('L3HT"annealing')
        # Should still parse what it can
        assert "l3" in result

    def test_structure_layer_data_edge_cases(self, miles_coder):
        """Test _structure_layer_data with edge cases."""
        # Test with unknown layer number
        result = miles_coder._structure_layer_data({"unknown": "value"}, 99)
        assert result == {"unknown": "value"}
        
        # Test with empty data
        result = miles_coder._structure_layer_data({}, 2)
        assert result == {}

    def test_find_value_end_generic_edge_cases(self, miles_coder):
        """Test _find_value_end_generic with various edge cases."""
        known_codes = {"AB", "PO", "HT", "YM"}
        
        # Test with bracketed value
        result = miles_coder._find_value_end_generic("[123]rest", 0, known_codes)
        assert result == 5  # Should include the closing bracket
        
        # Test with parenthetical value
        result = miles_coder._find_value_end_generic("(123)rest", 0, known_codes)
        assert result == 5  # Should include the closing parenthesis

class TestUtilityMethods:
    """Test utility methods in the converter."""

    def test_get_element_codes_coverage(self, miles_coder):
        """Test that all expected elements have codes."""
        codes = miles_coder._get_element_codes()
        
        # Test some key elements
        assert codes["H"] == "Hh"
        assert codes["Al"] == "Al"
        assert codes["Fe"] == "Fe"
        assert codes["Ti"] == "Ti"
        
        # Test edge cases
        assert codes["U"] == "Uu"  # Two-letter code for single letter
        assert codes["W"] == "Ww"

    def test_encode_element_all_types(self, miles_coder):
        """Test element encoding for various element types."""
        # Test single letter elements
        assert miles_coder._encode_element("H") == "Hh"
        assert miles_coder._encode_element("C") == "Cc"
        
        # Test two letter elements
        assert miles_coder._encode_element("Al") == "Al"
        assert miles_coder._encode_element("Ti") == "Ti"
        
        # Test unknown element (should return as-is)
        assert miles_coder._encode_element("Xx") == "Xx"

    def test_extract_enum_value_all_cases(self, miles_coder):
        """Test enum value extraction for all cases."""
        from milescoder.models import HeatTreatmentType, IPFEnum
        
        # Test enum with .value
        enum_val = HeatTreatmentType.annealing
        assert miles_coder._extract_enum_value(enum_val) == "annealing"
        
        # Test enum with .name (if different from .value)
        ipf_val = IPFEnum.X
        assert miles_coder._extract_enum_value(ipf_val) == "X"
        
        # Test string with class prefix
        assert miles_coder._extract_enum_value("HeatTreatmentType.annealing") == "annealing"
        
        # Test plain string
        assert miles_coder._extract_enum_value("plain_string") == "plain_string"
        
        # Test None
        assert miles_coder._extract_enum_value(None) == ""

    def test_get_field_type_all_cases(self, miles_coder):
        """Test field type extraction for various annotation types."""
        from typing import Optional, List, Union
        from milescoder.models import L0Parameters
        
        # Get a field info object to test with
        field_info = L0Parameters.model_fields["material"]
        field_type = miles_coder._get_field_type(field_info)
        # Should extract the actual type from Optional[str]
        assert field_type is not None

    def test_is_list_type_detection(self, miles_coder):
        """Test list type detection."""
        from typing import List, Optional
        from milescoder.models import CompositionPart
        
        # Mock field types for testing
        class MockFieldInfo:
            def __init__(self, annotation):
                self.annotation = annotation
        
        # Test List type
        list_field = MockFieldInfo(List[CompositionPart])
        assert miles_coder._is_list_type(list_field.annotation) == True
        
        # Test Optional type
        optional_field = MockFieldInfo(Optional[str])
        assert miles_coder._is_list_type(optional_field.annotation) == False
        
        # Test regular type
        str_field = MockFieldInfo(str)
        assert miles_coder._is_list_type(str_field.annotation) == False

    def test_is_nested_list_type_detection(self, miles_coder):
        """Test nested list type detection."""
        from typing import List
        from milescoder.models import CompositionPart
        
        class MockFieldInfo:
            def __init__(self, annotation):
                self.annotation = annotation
        
        # Test nested list
        nested_field = MockFieldInfo(List[List[CompositionPart]])
        assert miles_coder._is_nested_list_type(nested_field.annotation) == True
        
        # Test single list
        single_field = MockFieldInfo(List[CompositionPart])
        assert miles_coder._is_nested_list_type(single_field.annotation) == False