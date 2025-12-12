# MILESCoder
A Python package for encoding and decoding MILES (Material Input Line Entry System) strings - a standardized notation system for describing comprehensive material properties in a compact, machine-readable format.

## 🌟 Features
- Bidirectional Conversion: Convert between structured JSON data and compact MILES strings
- Hierarchical Material Description: Support for 6 hierarchical layers (L0-L5) covering material properties from basic composition to advanced manufacturing parameters
- Type-Safe Models: Built with Pydantic v2 for robust data validation and type safety
- Comprehensive Material Coverage: Supports metals, alloys, surface treatments, corrosion testing, and additive manufacturing parameters
- Built to be extended: Automatic handling of new Pydantic models.

## 📦 Installation
```bash
pip install milescoder
```

## 🚀 Quick Start
```python
from milescoder import MILESCoder
from milescoder.models import MILESData, L0Parameters, L1Parameters, L2Parameters

# Initialize the coder
coder = MILESCoder()

# Create sample material data
data = MILESData(
    l0=L0Parameters(material="metal"),
    l1=L1Parameters(metal="Al"),
    l2=L2Parameters(
        alloy={
            "materialID": "AA6061",
            "nominalComposition": [
                {"element": "Al", "content": 97.9},
                {"element": "Mg", "content": 1.0},
                {"element": "Si", "content": 1.1}
            ]
        }
    )
)

# Encode to MILES string
miles_string = coder.encode(data)
print(miles_string)  # "0.1A/L0ME/L1Al/L2ID"AA6061"NCAlMg1.0Si1.1"

# Decode back to structured data
decoded_data = coder.decode(miles_string)
print(decoded_data)
```

## 🏗️ Architecture

### Layer Structure
The MILES system organizes material information into hierarchical layers:

- L0: Base material type (e.g., "metal")
- L1: Specific metal element (e.g., "Al", "Fe", "Mg")
- L2: Alloy composition, microstructure (EBSD), grain characteristics
- L3: Manufacturing processes, surface treatments, mechanical properties
- L4: Corrosion testing parameters, electrolyte composition, environmental conditions
- L5: Additive manufacturing parameters, powder characteristics

*Note: Currently only metallic base materials are implemented*

### Core Components
*MILESCoder Class*: The main encoder/decoder class that handles conversion between MILES strings and structured data:

```python
class MILESCoder:
    def encode(self, data: MILESData) -> str:
        """Encode MILES data to string representation."""
        
    def decode(self, miles_str: str) -> Dict[str, Any]:
        """Decode MILES string to structured data."""
```

*Pydantic Models*: Type-safe data models with comprehensive validation.

*Custom Field Factory*: The miles_field() function creates Pydantic fields with MILES-specific metadata:
```python
from milescoder.models import miles_field

# Example field with MILES metadata
material_id = miles_field(
    code="ID",                    # MILES encoding code
    is_string=True,              # String type flag
    max_length=50,               # Validation constraint
    description="Material identifier",
    example="AA6061"
)
```

## 📊 Supported Material Properties
### L2: Alloy & Microstructure
- Composition: Elemental and nominal compositions
- Microstructure: Crystal phases, grain structure, EBSD data
- Phases: Hardening precipitates, intermetallics, dispersoids
- Texture: Crystal orientation, IPF data, Schmid factors

### L3: Manufacturing & Properties
- Mechanical Properties: Hardness, yield strength, Young's modulus
- Heat Treatment: Annealing, quenching, tempering parameters
- Surface Processing: Rolling, extrusion, surface treatments
- Manufacturing Flags: Cast, forged, wrought, shot peened

### L4: Corrosion Testing
- Electrolytes: Complex solution compositions with SMILES notation
- Corrosion Types: Pitting, generalized, filiform, crevice
- Test Conditions: Temperature, pH, immersion time, cyclic exposure
- Biological Testing: In-vivo and in-vitro test parameters

### L5: Additive Manufacturing
- Laser Parameters: Power, speed, spot size, hatch spacing
- Process Control: Layer thickness, scanning strategy, atmosphere
- Powder Characteristics: Size distribution, preheat temperature
- Quality Metrics: Density, defect analysis

## 🔧 Advanced Usage
### Composition Handling
The package provides sophisticated composition parsing for various formats:
````py
# Elemental composition
composition = [
    {"element": "Fe", "content": 68.0},
    {"element": "Cr", "content": 18.0},
    {"element": "Ni", "content": 10.0}
]

# Compound composition with SMILES notation
electrolyte = [
    {"name": "Sodium Chloride", "smilesString": "[Na+].[Cl-]", "molarity": 0.1},
    {"name": "Water", "smilesString": "O", "molarity": 55.5}
]
````

### Crystal Structure Data
Support for crystallographic information:

````py
crystal_phase = {
    "phase": "FCC",
    "composition": [
        {"element": "Al", "content": 90.0},
        {"element": "Cu", "content": 10.0}
    ]
}

crystal_orientation = {
    "ipf": "X",
    "suborientation": [
        {"percent": 45.2, "millerIndices": [1, 1, 1]},
        {"percent": 30.8, "millerIndices": [1, 0, 0]}
    ]
}
````

### Complex Surface Treatments
Detailed surface modification parameters:
```py
surface_treatment = {
    "type": "SiC",
    "grade": 400
}

heat_treatment = {
    "heatTreatmentType": "annealing",
    "heatTreatmentTemperature": 400.0,
    "heatTreatmentTime": 2.0,
    "heatTreatmentAtmosphereComposition": [
        {"element": "H", "content": 1000.0}  # ppm
    ]
}
```

## 🔒 Security Features
- Input Sanitization: Automatic cleaning of string inputs to prevent injection attacks
- Validation: Comprehensive Pydantic validation for all data types
- Type Safety: Strong typing throughout the entire package
- Length Limits: Configurable maximum lengths for string fields

## 📚 Element Code System
The package includes a comprehensive element coding system for compact representation:
```py
element_codes = {
    "H": "Hh", "He": "He", "Li": "Li", "Be": "Be",
    "Fe": "Fe", "Al": "Al", "Cr": "Cr", "Ni": "Ni",
    # ... complete periodic table coverage
}
```

## 🔗 Version Compatibility
- Python: 3.9+
- Pydantic: v2.0+
- MILES Format: Version 0.1A

## 🤝 Contributing
Contributions are welcome! The package is designed to be extensible:

1. Add new layer parameters by extending the L*Parameters models
2. Implement custom field types with appropriate MILES metadata
3. Extend the encoding/decoding logic for new data patterns

## 📄 License
This project is licensed under the MIT License.

## 🔗 Related Projects
- MILES Web Application: Interactive web interface for MILES encoding/decoding
- MILES-GPT: AI-powered PDF extraction for automated MILES generation

*MILESCoder: Making material descriptions machine-readable for computational materials science.*

