from typing import Dict, Any, List, Optional, Union, get_args, get_origin
from .models import (
    Compound,
    L0Parameters,
    L1Parameters,
    L2Parameters,
    L3Parameters,
    L4Parameters,
    L5Parameters,
    MILESData,
)
import re


class MILESCoder:
    """Generic encoder/decoder for MILES data using Pydantic model metadata."""

    def __init__(self):
        """Initialize the coder with layer models and element codes."""
        self.version = "0.1A"

        self.layer_models = {
            0: L0Parameters,
            1: L1Parameters,
            2: L2Parameters,
            3: L3Parameters,
            4: L4Parameters,
            5: L5Parameters,
        }
        self.element_codes = self._get_element_codes()

    def _get_element_codes(self) -> Dict[str, str]:
        """Generate element mapping for composition encoding."""
        return {
            # Period 1
            "H": "Hh",
            "He": "He",
            # Period 2
            "Li": "Li",
            "Be": "Be",
            "B": "Bb",
            "C": "Cc",
            "N": "Nn",
            "O": "Oo",
            "F": "Ff",
            "Ne": "Ne",
            # Period 3
            "Na": "Na",
            "Mg": "Mg",
            "Al": "Al",
            "Si": "Si",
            "P": "Pp",
            "S": "Ss",
            "Cl": "Cl",
            "Ar": "Ar",
            # Period 4
            "K": "Kk",
            "Ca": "Ca",
            "Sc": "Sc",
            "Ti": "Ti",
            "V": "Vv",
            "Cr": "Cr",
            "Mn": "Mn",
            "Fe": "Fe",
            "Co": "Co",
            "Ni": "Ni",
            "Cu": "Cu",
            "Zn": "Zn",
            "Ga": "Ga",
            "Ge": "Ge",
            "As": "As",
            "Se": "Se",
            "Br": "Br",
            "Kr": "Kr",
            # Period 5
            "Rb": "Rb",
            "Sr": "Sr",
            "Y": "Yy",
            "Zr": "Zr",
            "Nb": "Nb",
            "Mo": "Mo",
            "Tc": "Tc",
            "Ru": "Ru",
            "Rh": "Rh",
            "Pd": "Pd",
            "Ag": "Ag",
            "Cd": "Cd",
            "In": "In",
            "Sn": "Sn",
            "Sb": "Sb",
            "Te": "Te",
            "I": "Ii",
            "Xe": "Xe",
            # Period 6
            "Cs": "Cs",
            "Ba": "Ba",
            "La": "La",
            "Ce": "Ce",
            "Pr": "Pr",
            "Nd": "Nd",
            "Pm": "Pm",
            "Sm": "Sm",
            "Eu": "Eu",
            "Gd": "Gd",
            "Tb": "Tb",
            "Dy": "Dy",
            "Ho": "Ho",
            "Er": "Er",
            "Tm": "Tm",
            "Yb": "Yb",
            "Lu": "Lu",
            "Hf": "Hf",
            "Ta": "Ta",
            "W": "Ww",
            "Re": "Re",
            "Os": "Os",
            "Ir": "Ir",
            "Pt": "Pt",
            "Au": "Au",
            "Hg": "Hg",
            "Tl": "Tl",
            "Pb": "Pb",
            "Bi": "Bi",
            "Po": "Po",
            "At": "At",
            "Rn": "Rn",
            # Period 7
            "Fr": "Fr",
            "Ra": "Ra",
            "Ac": "Ac",
            "Th": "Th",
            "Pa": "Pa",
            "U": "Uu",
            "Np": "Np",
            "Pu": "Pu",
            "Am": "Am",
            "Cm": "Cm",
            "Bk": "Bk",
            "Cf": "Cf",
            "Es": "Es",
            "Fm": "Fm",
            "Md": "Md",
            "No": "No",
            "Lr": "Lr",
            "Rf": "Rf",
            "Db": "Db",
            "Sg": "Sg",
            "Bh": "Bh",
            "Hs": "Hs",
            "Mt": "Mt",
            "Ds": "Ds",
            "Rg": "Rg",
            "Cn": "Cn",
            "Nh": "Nh",
            "Fl": "Fl",
            "Mc": "Mc",
            "Lv": "Lv",
            "Ts": "Ts",
            "Og": "Og",
        }

    # ENCODING METHODS

    def encode(self, data: MILESData) -> str:
        """Encode MILES data to string representation."""
        result = []
        data_dict = data.model_dump(exclude_none=True)

        for layer_key in ["l0", "l1", "l2", "l3", "l4", "l5"]:
            if layer_key not in data_dict or not data_dict[layer_key]:
                continue

            layer_num = int(layer_key[1])
            layer_data = data_dict[layer_key]
            layer_str = self._encode_layer(layer_data, layer_num)

            if layer_str:
                result.append(layer_str)

        encoded_string = "/".join(result)
        return f"{self.version}/{encoded_string}" if encoded_string else ""

    def _encode_layer(self, layer_data: Dict[str, Any], layer_num: int) -> str:
        """Encode a single layer based on its number and data."""
        parts = [f"L{layer_num}"]
        
        # Special handling for L0 and L1 layers
        if layer_num == 0:
            return self._encode_l0_layer(layer_data, parts)
        elif layer_num == 1:
            return self._encode_l1_layer(layer_data, parts)

        # Generic encoding for L2+ layers using model metadata
        model_class = self.layer_models.get(layer_num)
        if not model_class:
            return ""

        for field_name, field_info in model_class.model_fields.items():
            if field_name not in layer_data or layer_data[field_name] is None:
                continue

            encoded_parts = self._encode_field(
                field_name, layer_data[field_name], field_info
            )
            parts.extend(encoded_parts)

        return "".join(parts)

    def _encode_l0_layer(self, layer_data: Dict[str, Any], parts: List[str]) -> str:
        """Encode L0 layer with material type."""
        if "material" in layer_data:
            material_value = layer_data["material"]
            if material_value == "metal":
                parts.append("ME")
            else:
                parts.append(material_value.upper()[:2])
        return "".join(parts)

    def _encode_l1_layer(self, layer_data: Dict[str, Any], parts: List[str]) -> str:
        """Encode L1 layer with metal type."""
        if "metal" in layer_data:
            parts.append(layer_data["metal"])
        return "".join(parts)

    def _encode_field(self, field_name: str, value: Any, field_info) -> List[str]:
        """Encode a field using its metadata and type information."""
        parts = []
        miles_meta = getattr(field_info, "json_schema_extra", {}).get("miles")

        if not miles_meta:
            return parts

        code = miles_meta.code
        is_parent = miles_meta.is_parent
        is_composition = miles_meta.is_composition
        is_string = miles_meta.is_string
        is_element = miles_meta.is_element
        is_enum = miles_meta.is_enum
        field_type = self._get_field_type(field_info)        

        # Special handling for grain boundaries
        if field_name == "grainBoundaries" and value and code:
            grain_boundary_parts = self._encode_grain_boundaries(value, code)
            parts.extend(grain_boundary_parts)
            return parts
        
        # Special handling for IPF field (crystal orientation)
        if field_name == "ipf" and value and code:
            enum_value = self._extract_enum_value(value)
            encoded_value = f"{code}{enum_value}"
            print(f"IPF field encoded as: {encoded_value}")
            parts.append(encoded_value)
            return parts
            

        # Special handling for suborientation field
        if field_name == "suborientation" and value and code:
            suborientation_parts = self._encode_suborientation_list(value, code)
            parts.extend(suborientation_parts)
            return parts

        # Type-based encoding dispatch
        if isinstance(value, bool):
            if value:
                if code:
                    parts.append(code)
            return parts
        elif isinstance(value, (int, float)):
            if code:
                parts.append(f"{code}{value}")
        elif isinstance(value, str):
            if is_element and code:
                encoded_element = self._encode_element(value)
                parts.append(f"{code}{encoded_element}")
            elif is_string and code:
                clean_value = self._extract_enum_value(value) if is_enum else value
                parts.append(f'{code}"{clean_value}"') if clean_value != "" else None
            elif code:
                clean_value = self._extract_enum_value(value) if is_enum else value
                parts.append(f"{code}{clean_value}")
        elif isinstance(value, list):
            parts.extend(
                self._encode_list_field(value, code, is_composition, field_type)
            )
        elif isinstance(value, dict):
            parts.extend(
                self._encode_dict_field(value, code, is_parent, field_info, field_type)
            )
        elif is_enum:
            # Handle enum instances directly using the is_enum flag
            clean_value = self._extract_enum_value(value)
            if code:
                if is_string:
                    parts.append(f'{code}"{clean_value}"')
                else:
                    parts.append(f"{code}{clean_value}")

        return parts


    def _encode_grain_boundaries(self, grain_boundaries: List[Dict[str, Any]], code: str) -> List[str]:
        """
        Encode grain boundaries list into GX pattern.
        Example: [{"grainInterface": [[{"element": "Mg", "content": 50.0}, {"element": "Zn", "content": 50.0}], 
                                    [{"element": "Mg", "content": 33.3}, {"element": "Cu", "content": 66.7}]], 
                "boundaryLength": 15.2}] 
        -> ["GX(MgZn50.0/MgCu66.7)15.2"]
        """
        parts = []
        
        for boundary in grain_boundaries:
            if isinstance(boundary, dict):
                grain_interface = boundary.get("grainInterface", [])
                boundary_length = boundary.get("boundaryLength", 0)
                
                if grain_interface and len(grain_interface) >= 2:
                    # grain_interface is now a list of composition lists
                    comp1 = grain_interface[0]  # First composition list
                    comp2 = grain_interface[1]  # Second composition list
                    
                    # Encode compositions using existing element encoding logic
                    encoded_comp1 = self._encode_element_composition(comp1)
                    encoded_comp2 = self._encode_element_composition(comp2)
                    
                    # Create GX pattern: GX(comp1,comp2)length
                    encoded_boundary = f"{code}({encoded_comp1},{encoded_comp2}){boundary_length}"
                    parts.append(encoded_boundary)
        
        return parts

    def _encode_suborientation_list(
        self, suborientation_list: List[Dict[str, Any]], code: str
    ) -> List[str]:
        """
        Encode suborientation list into CO pattern.
        Example: [{percent: 2.0, millerIndices: [1,2,0]}] -> ["CO2.0(120)"]

        Args:
            suborientation_list: List of suborientation dictionaries
            code: The encoding code (should be "CO")

        Returns:
            List of encoded suborientation strings
        """
        parts = []

        for suborientation in suborientation_list:
            if isinstance(suborientation, dict):
                percent = suborientation.get("percent", 0)
                miller_indices = suborientation.get("millerIndices", [])

                # Convert miller indices to string
                miller_str = "".join(str(index) for index in miller_indices)

                # Create encoded part: CO + percent + (miller_indices)
                encoded_part = f"{code}{percent}({miller_str})"
                parts.append(encoded_part)

        return parts

    def _encode_list_field(
        self, value: List[Any], code: str, is_composition: bool, field_type
    ) -> List[str]:
        """Encode list fields based on their content type and metadata."""
        if not code:
            return []

        if is_composition:
            # Check if this is a nested list type (List[List[ElementContent]])
            if self._is_nested_list_type(field_type):
                return self._encode_nested_composition_list(value, code)
            else:
                return self._encode_composition_list(value, code)
        else:
            return self._encode_generic_list(value, code, field_type)

    def _encode_composition_list(self, value: List[Any], code: str) -> List[str]:
        """Encode single composition lists (like nominalComposition)."""
        if not value:
            return []

        # Check if this is a compound composition
        if isinstance(value[0], dict) and (
            "smilesString" in value[0] or "molarity" in value[0]
        ):
            compound_array = self._encode_compound_composition(value)
            return [f"{code}{compound_array}"]
        else:
            # Regular element composition
            comp_str = self._encode_element_composition(value)
            return [f"{code}{comp_str}"]

    def _encode_generic_list(
        self, value: List[Any], code: str, field_type
    ) -> List[str]:
        """Encode generic list fields."""
        print(
            f"Encoding generic list for code '{code}' with value: {value}"
        )  # Debugging line
        parts = []
        for item in value:
            parts.append(f"{code}")
            if isinstance(item, dict):
                for key, val in item.items():
                    if val is not None and isinstance(val, str):
                        clean_val = self._extract_enum_value(val)
                        parts.append(f'"{clean_val}"')
                    if val is not None and isinstance(val, (int, float)):
                        parts.append(f"{val}")
                    if key == "composition":
                        comp_str = self._encode_element_composition(val)
                        parts.append(f"{comp_str}")                    
                    if key == "millerIndices" and isinstance(val, list):
                        miller_str = "".join(str(i) for i in val)
                        parts.append(f"({miller_str})")
            else:
                parts.append(f"{item}")
        return parts

    def _encode_dict_field(
        self, value: Dict[str, Any], code: str, is_parent: bool, field_info, field_type
    ) -> List[str]:
        """Encode dictionary fields based on their type and metadata."""
        if is_parent:
            return self._encode_parent_dict(value, code, field_info)
        else:
            return self._encode_typed_dict(value, code, field_type)

    def _encode_parent_dict(
        self, value: Dict[str, Any], code: str, field_info
    ) -> List[str]:
        """Encode parent container dictionaries."""
        parts = []
        if code:
            parts.append(code)

        nested_model = self._get_field_type(field_info)
        nested_parts = self._encode_nested_dict(value, nested_model)
        parts.extend(nested_parts)
        return parts

    def _encode_typed_dict(
        self, value: Dict[str, Any], code: str, field_type
    ) -> List[str]:
        """Encode typed dictionaries (like SurfaceTreatment)."""
        if not code:
            return []

        # Check for specific model types
        if field_type and hasattr(field_type, "__name__"):
            if field_type.__name__ == "SurfaceTreatment":
                return [self._encode_surface_treatment(value, code)]
            elif field_type.__name__ == "compound":
                return [self._encode_compound(value, code)]

        # Generic dict encoding
        parts = []
        for key, val in value.items():
            if val is not None:
                parts.append(f"{code}{key}:{val}")
        return parts


    def _extract_enum_value(self, enum_value: Any) -> str:
        """
        Extract string value from enum, handling different enum representations.
        
        Args:
            enum_value: The enum value to extract
            
        Returns:
            str: Clean enum value without class prefixes
        """
        if enum_value is None:
            return ""
        
        # Handle enum instances with .value attribute
        if hasattr(enum_value, "value"):
            return str(enum_value.value)
        
        # Handle enum instances with .name attribute
        if hasattr(enum_value, "name"):
            return str(enum_value.name)
        
        # Handle string representations that might include class names
        enum_str = str(enum_value)
        
        # Remove enum class prefixes (e.g., "HeatTreatmentType.annealing" -> "annealing")
        if "." in enum_str:
            return enum_str.split(".")[-1]
        
        return enum_str

    def _encode_surface_treatment(self, value: Dict[str, Any], code: str) -> str:
        """Encode surface treatment: {"type": "diamond", "grade": 1} -> PO"diamond"1."""
        treatment_type = value.get("type", "")
        
        # Use the robust enum extraction method
        clean_treatment_type = self._extract_enum_value(treatment_type)
        
        encoded_value = f'{code}"{clean_treatment_type}"'

        for key, val in value.items():
            if key != "type" and val is not None:
                encoded_value += str(val)

        return encoded_value

    def _encode_nested_dict(
        self, nested_data: Dict[str, Any], nested_model_class
    ) -> List[str]:
        """Recursively encode nested dictionaries using their model metadata."""
        if not nested_model_class or not hasattr(nested_model_class, "model_fields"):
            return []

        parts = []
        for key, value in nested_data.items():
            if value is None or key not in nested_model_class.model_fields:
                continue

            field_info = nested_model_class.model_fields[key]
            encoded_parts = self._encode_field(key, value, field_info)
            parts.extend(encoded_parts)

        return parts

    def _encode_nested_composition_list(
        self, value: List[List[Any]], code: str
    ) -> List[str]:
        """Encode nested composition lists (like hardening precipitates, intermetallics)."""
        if not value:
            return []

        parts = []
        for composition_list in value:
            if composition_list:  # Skip empty composition lists
                comp_str = self._encode_element_composition(composition_list)
                parts.append(f"{code}{comp_str}")

        return parts

    def _encode_element(self, element: str) -> str:
        """Encode element using element code."""
        return self.element_codes.get(element, element)

    def _encode_element_composition(self, composition: List[Dict[str, Any]]) -> str:
        """Encode element composition using element codes."""
        return "".join(
            [
                f"{self.element_codes.get(part['element'], part['element'])}"
                f"{'' if part.get('content', 1) == 1 else part.get('content', 1)}"
                for part in composition
                if isinstance(part, dict) and "element" in part
            ]
        )

    def _encode_compound_composition(self, composition: List[Compound]) -> str:
        """Encode compound composition array."""
        return "".join(
            [self._encode_compound(compound_obj, "SM") for compound_obj in composition]
        )

    def _encode_composition_with_string(
        self,
        value: Dict[str, Any],
        code: str,
        composition_key: str = "composition",
        string_key: str = "phase",
    ) -> str:
        """
        Encode objects with composition and string properties.
        Format: CODE"composition""string" or CODE"string" if only string is provided

        Args:
            value: Dictionary containing the object data
            code: The encoding code prefix
            composition_key: Key name for the composition property (default: "composition")
            string_key: Key name for the string property (default: "phase")
        """
        string_value = value.get(string_key, "")
        composition = value.get(composition_key, "")

        # Encode composition if it's a list of elements
        if composition and isinstance(composition, list):
            composition_str = self._encode_element_composition(composition)
        else:
            composition_str = str(composition) if composition else ""

        if composition_str and string_value:
            return f'{code}"{string_value}"{composition_str}'
        elif string_value:
            return f'{code}"{string_value}"'
        elif composition_str:
            return f"{code}{composition_str}"
        else:
            return None

    def _encode_compound(self, compound_obj: Dict[str, Any], code: str = "SM") -> str:
        """Encode single compound object: CN"string"SM"string"[molarity]."""
        compound_name = compound_obj.get("name", "")
        smiles_string = compound_obj.get("smilesString", "")
        molarity = compound_obj.get("molarity", 0)

        name_part = f'CN"{compound_name}"' if compound_name else ""
        smiles_part = f'{code}"{smiles_string}"' if smiles_string else ""

        return f"{name_part}{smiles_part}[{molarity}]"

    # DECODING METHODS

    def decode(self, miles_str: str) -> Dict[str, Any]:
        """Decode MILES string to structured data."""
        if not miles_str:
            return {}
        
        cleaned_str = self._remove_version_prefix(miles_str)

        layers = cleaned_str.split("/")
        result = {}

        for layer_str in layers:
            if not layer_str.strip():
                continue

            try:
                layer_num, layer_data = self._parse_layer_str(layer_str)
                structured_data = self._structure_layer_data(layer_data, layer_num)
                result[f"l{layer_num}"] = structured_data
            except Exception as e:
                print(f"Error parsing layer '{layer_str}': {e}")
                continue

        return result

    def _remove_version_prefix(self, miles_str: str) -> str:
        """Remove version prefix from MILES string."""
        # Check if string starts with version pattern (e.g., "0.1A/")
        if re.match(r"^\d+\.\d+[A-Z]/", miles_str):
            # Find first slash and return everything after it
            slash_index = miles_str.find("/")
            if slash_index != -1:
                return miles_str[slash_index + 1:]
        
        return miles_str
    
    def _parse_layer_str(self, layer_str: str) -> tuple:
        """Parse layer string into layer number and flat data."""
        match = re.match(r"L(\d+)(.*)", layer_str)
        if not match:
            raise ValueError(f"Invalid layer format: {layer_str}")

        layer_num = int(match.group(1))
        content = match.group(2)

        # Special handling for L0 and L1
        if layer_num == 0:
            return layer_num, self._parse_l0_content(content)
        elif layer_num == 1:
            return layer_num, self._parse_l1_content(content)

        # Generic parsing for L2+ layers
        return layer_num, self._extract_tokens(content, layer_num)

    def _parse_l0_content(self, content: str) -> Dict[str, Any]:
        """Parse L0 layer content."""
        if content == "ME":
            return {"material": "metal"}
        else:
            return {"material": content.lower()}

    def _parse_l1_content(self, content: str) -> Dict[str, Any]:
        """Parse L1 layer content."""
        return {"metal": content} if content else {}

    def _extract_tokens(self, content: str, layer_num: int) -> Dict[str, Any]:
        """Extract field tokens from content using model knowledge."""
        model_class = self.layer_models.get(layer_num)
        if not model_class:
            return {"raw_content": content} if content else {}

        # Collect all known codes and their field info
        known_codes = set()
        code_to_field_info = {}
        self._collect_all_codes(model_class, known_codes, code_to_field_info)

        # Add special IPF codes for crystal orientation in L2
        if layer_num == 2:
            known_codes.update({"CX", "CY", "CZ"})
            # Map IPF codes to the IPF field info
            ipf_field_info = self._find_ipf_field_info(model_class)
            if ipf_field_info:
                code_to_field_info["CX"] = ("ipf", ipf_field_info)
                code_to_field_info["CY"] = ("ipf", ipf_field_info)
                code_to_field_info["CZ"] = ("ipf", ipf_field_info)

        tokens = {}
        pos = 0

        while pos < len(content):
            # Special handling for crystal orientation patterns (CX, CY, CZ followed by CO)
            if pos + 2 <= len(content) and content[pos : pos + 2] in ["CX", "CY", "CZ"]:
                crystal_orientation_end = self._parse_crystal_orientation_block(
                    content, pos, tokens
                )
                pos = crystal_orientation_end
                continue

            # Special handling for grain boundary patterns (GX followed by parentheses)
            if pos + 2 <= len(content) and content[pos : pos + 2] == "GX":
                grain_boundary_end = self._parse_grain_boundary_block(content, pos, tokens)
                pos = grain_boundary_end
                continue

            code, field_name, field_info = self._find_next_code(
                content, pos, known_codes, code_to_field_info
            )

            if not code:
                pos += 1
                continue

            # Check if this is a boolean field (no value expected)
            is_boolean_field = self._is_boolean_field(field_info)
            
            if is_boolean_field:
                # Boolean field - no value to parse, just set to True
                tokens[field_name] = True
                pos += 2  # Move past the code
                continue

            # Extract and parse value
            value_start = pos + 2
            value_end = self._find_value_end_generic(content, value_start, known_codes)
            raw_value = content[value_start:value_end]

            # Special handling for compound arrays that start after EL
            if (
                code == "EL"
                and raw_value.startswith("SM")
                or raw_value.startswith("CN")
            ):
                # This is an electrolyteComposition field with compound array
                parsed_value = self._parse_compound_array(raw_value)
            elif code == "CP" and raw_value.startswith('"'):
                # This is a crystalPhase field with possible multiple phases
                parsed_value = self._parse_crystal_phase(raw_value)
            else:
                parsed_value = self._parse_value(raw_value, field_name, field_info)

            self._assign_parsed_value(tokens, field_name, parsed_value, field_info)

            pos = value_end

        return tokens


    def _parse_grain_boundary_block(self, content: str, start_pos: int, tokens: dict) -> int:
        """
        Parse grain boundary block pattern: GX(comp1,comp2)length
        Example: GX(MgZn50.0,MgCu66.7)15.2 -> grain boundary object with composition objects
        """
        # Move past "GX"
        pos = start_pos + 2
        
        # Look for opening parenthesis
        if pos >= len(content) or content[pos] != '(':
            return pos
        
        pos += 1  # Skip opening parenthesis
        
        # Find the closing parenthesis
        paren_end = content.find(')', pos)
        if paren_end == -1:
            return len(content)
        
        # Extract compositions between parentheses
        compositions_str = content[pos:paren_end]
        
        # Split by comma to get two compositions
        if ',' not in compositions_str:
            return paren_end + 1
        
        comp1_str, comp2_str = compositions_str.split(',', 1)
        
        # Parse encoded compositions back to structured composition objects
        comp1_objects = self._parse_composition_string(comp1_str)
        comp2_objects = self._parse_composition_string(comp2_str)
        
        # Create grain interface with composition objects
        grain_interface = [comp1_objects, comp2_objects]
        
        pos = paren_end + 1  # Move past closing parenthesis
        
        # Parse boundary length (numeric value after parentheses)
        length_start = pos
        while pos < len(content) and (content[pos].isdigit() or content[pos] == '.'):
            pos += 1
        
        length_str = content[length_start:pos]
        boundary_length = float(length_str) if length_str else 0.0
        
        # Create grain boundary object
        grain_boundary = {
            "grainInterface": grain_interface,
            "boundaryLength": boundary_length
        }
        
        # Add to grainBoundaries list in tokens
        if "grainBoundaries" not in tokens:
            tokens["grainBoundaries"] = []
        
        tokens["grainBoundaries"].append(grain_boundary)
        
        return pos

    def _parse_crystal_orientation_block(
    self, content: str, start_pos: int, tokens: dict
) -> int:
        """
        Parse crystal orientation block pattern: CY + multiple CO entries.
        Example: CYCO2.0(120)CO10.0(200) -> {ipf: "Y", suborientation: [...]}

        Args:
            content: The full content string
            start_pos: Position where the crystal orientation block starts (at CX/CY/CZ)
            tokens: Dictionary to store parsed results

        Returns:
            Position after the crystal orientation block
        """
        # Extract IPF value (X, Y, or Z)
        ipf_code = content[start_pos : start_pos + 2]
        ipf_value = ipf_code[1]  # Extract X, Y, or Z

        # Initialize crystal orientation structure
        self._create_crystal_orientation_structure(tokens, ipf_value)

        # Move past the IPF code
        pos = start_pos + 2

        # Parse suborientation entries (CO patterns)
        suborientation_list = []

        while pos < len(content) - 1:
            # Look for CO pattern
            if pos + 2 <= len(content) and content[pos : pos + 2] == "CO":
                pos += 2  # Skip "CO"

                # Parse percent value until opening parenthesis
                percent_start = pos
                while pos < len(content) and content[pos] != "(":
                    pos += 1

                if pos >= len(content):
                    break

                percent_str = content[percent_start:pos]
                try:
                    percent = float(percent_str)
                except ValueError:
                    break

                # Parse miller indices in parentheses
                if content[pos] == "(":
                    pos += 1  # Skip opening parenthesis
                    miller_start = pos
                    while pos < len(content) and content[pos] != ")":
                        pos += 1

                    if pos >= len(content):
                        break

                    miller_str = content[miller_start:pos]
                    miller_indices = [
                        int(digit) for digit in miller_str if digit.isdigit()
                    ]
                    pos += 1  # Skip closing parenthesis

                    # Add suborientation entry
                    suborientation_entry = {
                        "percent": percent,
                        "millerIndices": miller_indices,
                    }
                    suborientation_list.append(suborientation_entry)
                    
                    # After closing parenthesis, check if the next characters are another CO
                    # If not, we've reached the end of the crystal orientation block
                    if pos + 2 > len(content) or content[pos : pos + 2] != "CO":
                        break
                else:
                    break
            else:
                # No more CO patterns found, end of crystal orientation block
                break

        # Assign suborientation list to the crystal orientation structure
        if suborientation_list:
            tokens["ebsd"]["crystalOrientation"]["suborientation"] = suborientation_list

        return pos

    def _find_ipf_field_info(self, model_class):
        """Find the IPF field info within the model hierarchy."""
        # Look for EBSD -> CrystalOrientation -> IPF field structure
        for field_name, field_info in model_class.model_fields.items():
            miles_meta = getattr(field_info, "json_schema_extra", {}).get("miles")

            if miles_meta and miles_meta.is_parent:
                nested_model = self._get_field_type(field_info)
                if nested_model and hasattr(nested_model, "model_fields"):
                    # Check if this nested model has crystalOrientation
                    for (
                        nested_field_name,
                        nested_field_info,
                    ) in nested_model.model_fields.items():
                        if nested_field_name == "crystalOrientation":
                            crystal_orientation_model = self._get_field_type(
                                nested_field_info
                            )
                            if crystal_orientation_model and hasattr(
                                crystal_orientation_model, "model_fields"
                            ):
                                ipf_field_info = (
                                    crystal_orientation_model.model_fields.get("ipf")
                                )
                                if ipf_field_info:
                                    return ipf_field_info
        return None

    def _create_crystal_orientation_structure(
        self, tokens: dict, ipf_value: str
    ) -> None:
        """Create the nested structure for crystal orientation IPF value."""
        # Create ebsd structure if it doesn't exist
        if "ebsd" not in tokens:
            tokens["ebsd"] = {}

        # Create crystalOrientation structure if it doesn't exist
        if "crystalOrientation" not in tokens["ebsd"]:
            tokens["ebsd"]["crystalOrientation"] = {}

        # Set the IPF value
        tokens["ebsd"]["crystalOrientation"]["ipf"] = ipf_value

    def _collect_all_codes(
        self, model_class, known_codes: set, code_to_field_info: dict
    ) -> None:
        """Recursively collect all codes from model and nested models."""
        for field_name, field_info in model_class.model_fields.items():
            miles_meta = getattr(field_info, "json_schema_extra", {}).get("miles")

            if miles_meta and miles_meta.code:
                known_codes.add(miles_meta.code)
                code_to_field_info[miles_meta.code] = (field_name, field_info)

            # Recursively collect from nested models
            if miles_meta and miles_meta.is_parent:
                nested_model = self._get_field_type(field_info)
                if nested_model and hasattr(nested_model, "model_fields"):
                    self._collect_all_codes(
                        nested_model, known_codes, code_to_field_info
                    )

    def _find_next_code(
        self, content: str, pos: int, known_codes: set, code_to_field_info: dict
    ) -> tuple:
        """Find the next known code and return code, field_name, field_info."""
        if pos + 2 <= len(content):
            potential_code = content[pos : pos + 2]
            if potential_code in known_codes:
                field_name, field_info = code_to_field_info[potential_code]
                return potential_code, field_name, field_info

        return None, None, None

    def _find_compound_array_end(
        self, content: str, start: int, known_codes: set
    ) -> int:
        """Find the end of a compound array by looking for non-SM codes."""
        pos = start
        while pos < len(content) - 1:
            # Look for next known code
            if pos + 2 <= len(content):
                potential_code = content[pos : pos + 2]
                if potential_code in known_codes and (
                    potential_code != "SM" and potential_code != "CN"
                ):
                    # Make sure we're not inside quotes
                    quotes_before = content[start:pos].count('"')
                    if quotes_before % 2 == 0:  # Even number means we're outside quotes
                        return pos
            pos += 1

        return len(content)

    def _find_value_end_generic(
        self, content: str, start: int, known_codes: set
    ) -> int:
        """
        Generic value end detection based on content patterns.
        Enhanced to handle crystal phase patterns properly.
        """
        # Handle quoted strings for crystal phases
        if start < len(content) and content[start] == '"':
            return self._find_crystal_phase_end(content, start, known_codes)

        # Handle compound arrays that start with SM
        if (
            start < len(content)
            and start + 2 <= len(content)
            and content[start : start + 2] == "SM"
        ):
            return self._find_compound_array_end(content, start, known_codes)

        # Handle bracketed values
        if start < len(content) and content[start] in "[(":
            close_char = "]" if content[start] == "[" else ")"
            end = content.find(close_char, start)
            return end + 1 if end != -1 else len(content)

        # Look for next code while respecting quoted sections
        return self._find_next_code_position(content, start, known_codes)

    def _find_crystal_phase_end(
        self, content: str, start: int, known_codes: set
    ) -> int:
        """
        Find the end of a crystal phase value that starts with a quote.
        Handles patterns like "FCC"Mg0.2Ca0.2 followed by the next code.
        """
        # Find the closing quote for the phase name
        quote_end = content.find('"', start + 1)
        if quote_end == -1:
            return len(content)

        # After the closing quote, look for composition until the next known code
        pos = quote_end + 1

        # Parse composition characters until we hit the next code
        while pos < len(content) - 1:
            # Check if we've reached a known code
            if pos + 2 <= len(content):
                potential_code = content[pos : pos + 2]
                if potential_code in known_codes:
                    # Found the next code, so end the crystal phase value here
                    return pos
            pos += 1

        return len(content)

    def _find_quoted_string_end(self, content: str, start: int) -> int:
        """Find end of quoted string, handling compound patterns."""
        quote_end = content.find('"', start + 1)
        if quote_end == -1:
            return len(content)

        # Check for bracketed value after quote (compound pattern)
        if quote_end + 1 < len(content) and content[quote_end + 1] == "[":
            bracket_end = content.find("]", quote_end + 2)
            return bracket_end + 1 if bracket_end != -1 else quote_end + 1

        # Check for numeric value after quote (surface treatment grade pattern)
        pos = quote_end + 1
        while pos < len(content) and (content[pos].isdigit() or content[pos] == "."):
            pos += 1

        # If we found digits after the quote, include them
        if pos > quote_end + 1:
            return pos

        return quote_end + 1

    def _find_next_code_position(
        self, content: str, start: int, known_codes: set
    ) -> int:
        """Find position of next code, respecting quoted sections."""
        pos = start
        in_quotes = False

        while pos < len(content) - 1:
            if content[pos] == '"':
                in_quotes = not in_quotes

            if not in_quotes and pos + 2 <= len(content):
                potential_code = content[pos : pos + 2]
                if potential_code in known_codes:
                    return pos

            pos += 1

        return len(content)

    def _parse_value(self, raw_value: str, field_name: str, field_info=None) -> Any:
        """Parse raw value based on type information and content patterns."""
        if not raw_value:
            return True  # Boolean flag for fields with no value

        field_type = self._get_field_type(field_info) if field_info else None
        miles_meta = (
            getattr(field_info, "json_schema_extra", {}).get("miles")
            if field_info
            else None
        )

        # Type-based parsing
        if field_type and hasattr(field_type, "__name__"):
            type_name = field_type.__name__

            if type_name == "SurfaceTreatment":
                return self._parse_surface_treatment(raw_value)
            elif type_name == "Compound":
                return self._parse_single_compound(raw_value)
            elif type_name == "CrystalPhase":
                return self._parse_crystal_phase(raw_value)

        # Metadata-based parsing
        if miles_meta:
            if (
                miles_meta.is_string
                and raw_value.startswith('"')
                and raw_value.endswith('"')
            ):
                return raw_value[1:-1]  # Remove quotes
            elif miles_meta.is_composition:
                if raw_value.startswith("SM"):
                    return self._parse_compound_array(raw_value)
                else:
                    return self._parse_composition_string(raw_value)
            elif miles_meta.is_element:
                return self._parse_element_string(raw_value)

        # Pattern-based parsing
        return self._parse_by_pattern(raw_value)

    def _parse_surface_treatment(self, raw_value: str) -> Dict[str, Any]:
        """Parse surface treatment pattern: "type"grade -> {"type": "...", "grade": ...}."""

        match = re.match(r'"([^"]+)"(.*)$', raw_value)
        if match:
            result = {"type": match.group(1)}
            remaining = match.group(2)

            if remaining:
                if re.match(r"^\d+$", remaining):
                    result["grade"] = int(remaining)
                elif re.match(r"^\d*\.\d+$", remaining):
                    result["grade"] = float(remaining)
                else:
                    result["value"] = remaining

            return result

        # Fallback for just quoted string
        if raw_value.startswith('"') and raw_value.endswith('"'):
            return {"type": raw_value[1:-1]}

        return {"type": raw_value}

    def _parse_single_compound(self, raw_value: str) -> Dict[str, Any]:
        """Parse single compound pattern: CN"string"SM"string"[value] -> {"name": "...", "smilesString": "...", "molarity": ...}."""
        # Pattern 1: Full compound with both name and SMILES: CN"name"SM"smiles"[molarity]
        full_match = re.match(r'CN"(.+?)"SM"(.+?)"\[(\d*\.?\d+)\]$', raw_value)
        if full_match:
            return {
                "name": full_match.group(1),
                "smilesString": full_match.group(2),
                "molarity": float(full_match.group(3)),
            }
        
        # Pattern 2: Only name with molarity: CN"name"[molarity]
        name_only_match = re.match(r'CN"(.+?)"\[(\d*\.?\d+)\]$', raw_value)
        if name_only_match:
            return {
                "name": name_only_match.group(1),
                "smilesString": "",
                "molarity": float(name_only_match.group(2)),
            }
        
        # Pattern 3: Only SMILES with molarity: SM"smiles"[molarity]
        smiles_only_match = re.match(r'SM"(.+?)"\[(\d*\.?\d+)\]$', raw_value)
        if smiles_only_match:
            return {
                "name": "",
                "smilesString": smiles_only_match.group(1),
                "molarity": float(smiles_only_match.group(2)),
            }

        # Handle empty compound field - return empty dict to trigger validation error
        # instead of returning an empty dict that passes validation
        return {"name": "", "smilesString": "", "molarity": 0.0}

    def _parse_compound_array(self, compound_array_str: str) -> List[Dict[str, Any]]:
        """Parse compound array string like 'CN"NaCl"SM"NaCl"[0.05]' or 'CN"NaCl"[0.05]' or 'SM"NaCl"[0.05]'."""
        compound_list = []
        
        # Pattern 1: Full compound with both name and SMILES: CN"name"SM"smiles"[molarity]
        full_pattern = r'CN"([^"]+)"SM"([^"]+)"\[(\d*\.?\d+)\]'
        full_matches = re.finditer(full_pattern, compound_array_str)
        
        for match in full_matches:
            compound_name = match.group(1)
            smiles_string = match.group(2)
            molarity = float(match.group(3))
            compound_list.append(
                {
                    "name": compound_name,
                    "smilesString": smiles_string,
                    "molarity": molarity,
                }
            )
        
        # Pattern 2: Only name with molarity: CN"name"[molarity]
        # Only match if not already matched by full pattern
        remaining_str = compound_array_str
        for match in re.finditer(full_pattern, compound_array_str):
            remaining_str = remaining_str.replace(match.group(0), "")
        
        name_only_pattern = r'CN"([^"]+)"\[(\d*\.?\d+)\]'
        name_only_matches = re.finditer(name_only_pattern, remaining_str)
        
        for match in name_only_matches:
            compound_name = match.group(1)
            molarity = float(match.group(2))
            compound_list.append(
                {
                    "name": compound_name,
                    "smilesString": "",
                    "molarity": molarity,
                }
            )
        
        # Pattern 3: Only SMILES with molarity: SM"smiles"[molarity]
        # Only match if not already matched by full pattern
        smiles_only_pattern = r'SM"([^"]+)"\[(\d*\.?\d+)\]'
        smiles_only_matches = re.finditer(smiles_only_pattern, remaining_str)
        
        for match in smiles_only_matches:
            smiles_string = match.group(1)
            molarity = float(match.group(2))
            compound_list.append(
                {
                    "name": "",
                    "smilesString": smiles_string,
                    "molarity": molarity,
                }
            )

        return compound_list

    def _parse_crystal_phase(self, raw_value: str) -> Dict[str, Any]:
        """
        Parse single crystal phase pattern: "phase"composition -> {"phase": "...", "composition": [...]}
        This method handles ONE crystal phase occurrence.
        """

        # Pattern for phase with composition: "FCC"Mg0.2Ca0.2
        # This pattern captures the phase in quotes and any following composition
        pattern = r'^"([^"]+)"(.*)$'
        match = re.match(pattern, raw_value)

        if match:
            phase = match.group(1)
            composition_str = match.group(2)

            if composition_str:
                composition = self._parse_composition_string(composition_str)
            else:
                composition = []

            result = {"phase": phase, "composition": composition}
            print(f"Parsed crystal phase: {result}")
            return result

        # Fallback for unquoted phase (plain text like 'FCC')
        if raw_value:
            result = {"phase": raw_value}
            print(f"Parsed plain text phase: {result}")
            return result

        # Empty fallback
        return {"phase": ""}

    def _parse_by_pattern(self, raw_value: str) -> Any:
        """Generic pattern-based parsing for common value types."""
        # compound array pattern
        if raw_value.startswith("SM") and "SM" in raw_value[2:]:
            return self._parse_compound_array(raw_value)

        # Quoted strings
        if raw_value.startswith('"') and raw_value.endswith('"'):
            return raw_value[1:-1]

        # Numeric values
        if re.match(r"^-?\d*\.?\d+$", raw_value):
            return float(raw_value) if "." in raw_value else int(raw_value)

        # Bracketed values
        if raw_value.startswith("[") and raw_value.endswith("]"):
            inner = raw_value[1:-1]
            try:
                return float(inner) if "." in inner else int(inner)
            except ValueError:
                return inner

        # Parenthetical values (miller indices)
        if raw_value.startswith("(") and raw_value.endswith(")"):
            inner = raw_value[1:-1]
            if all(c.isdigit() for c in inner):
                return [int(c) for c in inner]
            return inner

        # Key-value pairs
        if ":" in raw_value:
            key, value = raw_value.split(":", 1)
            return {key: value}

        return raw_value

    def _parse_element_string(self, element_str: str) -> str:
        """Parse element string using element codes."""
        reverse_element_codes = {v: k for k, v in self.element_codes.items()}
        return reverse_element_codes.get(element_str, element_str)

    def _parse_composition_string(self, comp_str: str) -> List[Dict[str, Any]]:
        """Parse composition string like 'FeCr18Ni10' or 'Mg2.1' into element/content pairs."""
        composition = []
        reverse_element_codes = {v: k for k, v in self.element_codes.items()}

        pos = 0
        while pos < len(comp_str):
            # Try to match 2-letter element code first
            if pos + 2 <= len(comp_str):
                potential_code = comp_str[pos : pos + 2]
                if potential_code in reverse_element_codes:
                    element = reverse_element_codes[potential_code]
                    pos += 2

                    # Get the content value
                    content_start = pos
                    while pos < len(comp_str) and (
                        comp_str[pos].isdigit() or comp_str[pos] == "."
                    ):
                        pos += 1

                    content_str = comp_str[content_start:pos]
                    content = (
                        1
                        if not content_str
                        else (
                            float(content_str)
                            if "." in content_str
                            else int(content_str)
                        )
                    )

                    composition.append({"element": element, "content": content})
                    continue

            # Try single letter element or two-letter element symbol
            if pos < len(comp_str) and comp_str[pos].isupper():
                # Check for two-letter element symbol first
                if pos + 1 < len(comp_str) and comp_str[pos + 1].islower():
                    two_letter = comp_str[pos : pos + 2]
                    if two_letter in self.element_codes:
                        element = two_letter
                        pos += 2
                    else:
                        # Check single letter element
                        element_candidate = comp_str[pos]
                        if element_candidate in self.element_codes:
                            element = element_candidate
                            pos += 1
                        else:
                            # Skip unrecognized element
                            pos += 1
                            continue
                else:
                    # Single letter element
                    element_candidate = comp_str[pos]
                    if element_candidate in self.element_codes:
                        element = element_candidate
                        pos += 1
                    else:
                        # Skip unrecognized element
                        pos += 1
                        continue

                # Get the content value
                content_start = pos
                while pos < len(comp_str) and (
                    comp_str[pos].isdigit() or comp_str[pos] == "."
                ):
                    pos += 1

                content_str = comp_str[content_start:pos]
                content = (
                    1
                    if not content_str
                    else (
                        float(content_str) if "." in content_str else int(content_str)
                    )
                )

                composition.append({"element": element, "content": content})
            else:
                pos += 1  # Skip unrecognized character

        return composition

    def _assign_parsed_value(
        self, tokens: dict, field_name: str, parsed_value: Any, field_info
    ) -> None:
        """
        Assign parsed value to tokens based on field type and metadata.
        Enhanced crystal phase handling for List[CrystalPhase].
        """
        if not field_info:
            tokens[field_name] = parsed_value
            return

        field_type = self._get_field_type(field_info)
        miles_meta = getattr(field_info, "json_schema_extra", {}).get("miles")

        if miles_meta and miles_meta.is_parent and parsed_value is True:
            print(f"Skipping boolean True value for parent field '{field_name}'")
            return

        # Special handling for crystal phase lists (List[CrystalPhase])
        if field_name == "crystalPhase":
            # Each parsed crystal phase should be a dict, add it to the list
            if isinstance(parsed_value, dict):
                if field_name in tokens:
                    # Append to existing list
                    if isinstance(tokens[field_name], list):
                        tokens[field_name].append(parsed_value)
                    else:
                        tokens[field_name] = [tokens[field_name], parsed_value]
                else:
                    tokens[field_name] = [parsed_value]
            elif isinstance(parsed_value, list):
                # If somehow we get a list, extend or set appropriately
                if field_name in tokens:
                    if isinstance(tokens[field_name], list):
                        tokens[field_name].extend(parsed_value)
                    else:
                        tokens[field_name] = [tokens[field_name]] + parsed_value
                else:
                    tokens[field_name] = parsed_value
            return

        # Special handling for electrolyteComposition - convert to compound arrays
        if field_name == "electrolyteComposition":
            if isinstance(parsed_value, list) and parsed_value:
                if isinstance(parsed_value[0], dict) and "element" in parsed_value[0]:
                    # Convert element composition to compound composition
                    compound_list = []
                    for element_data in parsed_value:
                        compound_list.append(
                            {
                                "name": element_data.get("element", ""),
                                "smilesString": element_data.get("element", ""),
                                "molarity": element_data.get("content", 1.0),
                            }
                        )
                    tokens[field_name] = compound_list
                    return

        # Handle composition fields - both single compositions and lists of compositions
        if miles_meta and miles_meta.is_composition:
            # Check if this is a nested list type (List[List[ElementContent]])
            if self._is_nested_list_type(field_type):
                # This is a list of composition lists (like hardening precipitates, intermetallics)
                # Each parsed_value becomes a separate composition list in the outer list
                if field_name in tokens:
                    if not isinstance(tokens[field_name], list):
                        tokens[field_name] = [tokens[field_name]]
                    tokens[field_name].append(parsed_value)
                else:
                    tokens[field_name] = [parsed_value]
            elif self._is_list_type(field_type):
                # This is a single composition list (like nominalComposition)
                # Accumulate all elements into one list
                if field_name in tokens:
                    if isinstance(tokens[field_name], list) and isinstance(
                        parsed_value, list
                    ):
                        tokens[field_name].extend(parsed_value)
                    else:
                        tokens[field_name] = parsed_value
                else:
                    tokens[field_name] = parsed_value
            else:
                # Single composition field
                tokens[field_name] = parsed_value

        # Handle list fields that should not accumulate (single assignment)
        elif self._is_single_assignment_field(field_name):
            tokens[field_name] = parsed_value

        # Handle regular list fields that should accumulate
        elif self._is_list_type(field_type):
            self._append_or_set(tokens, field_name, parsed_value)

        # Handle single value fields
        else:
            tokens[field_name] = parsed_value

    def _is_nested_list_type(self, field_type) -> bool:
        """Check if a field type is a nested list type (List[List[...]])."""
        if field_type is None:
            return False

        origin = get_origin(field_type)
        if origin is list or origin is List:
            args = get_args(field_type)
            if args:
                inner_type = args[0]
                inner_origin = get_origin(inner_type)
                return inner_origin is list or inner_origin is List

        return False

    def _is_single_assignment_field(self, field_name: str) -> bool:
        """Check if field should only be assigned once (not accumulated)."""
        single_assignment_fields = [
            "electrolyteComposition",
            "inVitroTest",
            "composition",
            "nominalComposition",
            "heatTreatmentAtmosphereComposition",
        ]
        return field_name in single_assignment_fields

    def _append_or_set(self, tokens: dict, field_name: str, value: Any) -> None:
        """Append to list or set value based on current state."""
        if field_name in tokens:
            if not isinstance(tokens[field_name], list):
                tokens[field_name] = [tokens[field_name]]
            tokens[field_name].append(value)
        else:
            tokens[field_name] = [value] if value is not True else True

    def _structure_layer_data(
        self, flat_data: Dict[str, Any], layer_num: int
    ) -> Dict[str, Any]:
        """Structure flat data using model hierarchy."""
        model_class = self.layer_models.get(layer_num)
        if not model_class:
            return flat_data

        structured = {}
        used_fields = set()

        # Identify parent fields and their children
        for field_name, field_info in model_class.model_fields.items():
            miles_meta = getattr(field_info, "json_schema_extra", {}).get("miles")

            if miles_meta and miles_meta.is_parent:
                # This is a parent field - collect its children
                child_model = self._get_field_type(field_info)
                if child_model and hasattr(child_model, "model_fields"):
                    parent_data = {}
                    for child_name in child_model.model_fields.keys():
                        if child_name in flat_data:
                            parent_data[child_name] = flat_data[child_name]
                            used_fields.add(child_name)

                    if parent_data:
                        structured[field_name] = parent_data

        # Add remaining fields at top level
        for key, value in flat_data.items():
            if key not in used_fields:
                # Skip fields that are just boolean flags with no meaningful data
                if key == "smiles" and value == {}:
                    continue
                structured[key] = value

        return structured

    # UTILITY METHODS

    def _get_field_type(self, field_info) -> Optional[type]:
        """Get the actual type from a field annotation."""
        annotation = field_info.annotation
        origin = get_origin(annotation)

        if origin is Union:
            # Handle Optional[Type] -> Type
            args = get_args(annotation)
            for arg in args:
                if arg is not type(None):
                    return arg

        return annotation if isinstance(annotation, type) else None

    def _get_list_element_type(self, field_type):
        """Extract the element type from a List type annotation."""
        if field_type is None:
            return None

        origin = get_origin(field_type)
        if origin is list or origin is List:
            args = get_args(field_type)
            if args:
                return args[0]

        return None

    def _is_list_type(self, field_type) -> bool:
        """Check if a field type is a list type."""
        if field_type is None:
            return False

        origin = get_origin(field_type)
        return origin is list or origin is List

    def _is_boolean_field(self, field_info) -> bool:
        """Check if a field is a boolean type that expects no value."""
        if not field_info:
            return False
        
        # Get the field type
        field_type = self._get_field_type(field_info)
        
        # Check if it's a boolean type
        return field_type is bool