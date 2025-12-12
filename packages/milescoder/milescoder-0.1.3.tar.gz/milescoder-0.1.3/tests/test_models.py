import pytest
from pydantic import ValidationError
from milescoder.models import (
    MILESData,
    CompositionPart,
    AlloyInfo,
    CrystalPhase,
    CrystalStructure,
    L0Parameters,
    L1Parameters,
    L2Parameters,
    L3Parameters,
    L4Parameters,
    L5Parameters,
    Compound,
    Electrolyte,
    HeatTreatmentType,
    SurfaceTreatmentType,
    ExtrusionMode,
    AnimalModel,
    ImplantationSite,
    IPFEnum,
    ScanningStrategy,
    miles_field,
    MILESField,
    MILESConversionRequest,
    JSONConversionRequest,
    MILESConversionResponse,
    JSONConversionResponse,
)


class TestMILESField:
    """Test MILESField model."""

    def test_miles_field_creation(self):
        """Test MILESField model creation."""
        field = MILESField(
            code="MA",
            is_composition=True,
            is_element=False,
            is_enum=True,
            is_parent=False,
            is_string=True,
            label="Material",
        )
        assert field.code == "MA"
        assert field.is_composition is True
        assert field.is_element is False
        assert field.is_enum is True
        assert field.is_parent is False
        assert field.is_string is True
        assert field.label == "Material"

    def test_miles_field_defaults(self):
        """Test MILESField with defaults."""
        field = MILESField()
        assert field.code is None
        assert field.is_composition is False
        assert field.is_element is False
        assert field.is_enum is False
        assert field.is_parent is False
        assert field.is_string is False
        assert field.label is None


class TestMilesFieldFunction:
    """Test miles_field function."""

    def test_miles_field_function_basic(self):
        """Test miles_field function with basic parameters."""
        field = miles_field(code="MA", description="Test field", example="test")
        # Access the MILESField object attributes
        miles_metadata = field.json_schema_extra["miles"]
        assert miles_metadata.code == "MA"
        assert miles_metadata.example == "test"

    def test_miles_field_function_with_enum(self):
        """Test miles_field function with enum parameter."""
        field = miles_field(code="MA", enum=["metal", "ceramic"], example="metal")
        miles_metadata = field.json_schema_extra["miles"]
        assert miles_metadata.enum == ["metal", "ceramic"]
        assert miles_metadata.example == "metal"


class TestCompositionPart:
    """Test CompositionPart model."""

    def test_valid_composition_part(self):
        """Test valid composition part creation."""
        comp = CompositionPart(element="Fe", content=18.0)
        assert comp.element == "Fe"
        assert comp.content == 18.0

    def test_composition_part_validation_error(self):
        """Test composition part with invalid content."""
        with pytest.raises(ValidationError):
            CompositionPart(element="Fe", content=-1.0)


class TestCrystalPhase:
    """Test CrystalPhase model."""

    def test_crystal_phase_with_all_fields(self):
        """Test crystal phase with all fields."""
        phase = CrystalPhase(
            phase=CrystalStructure.FCC,
            composition=[
                {"element": "Al", "content": 50.0},
                {"element": "Cu", "content": 50.0},
            ],
        )
        assert phase.phase == CrystalStructure.FCC
        assert len(phase.composition) == 2

    def test_crystal_phase_minimal(self):
        """Test crystal phase with minimal data."""
        phase = CrystalPhase()
        assert phase.phase is None
        assert phase.composition is None


class TestCompound:
    """Test Compound model validation."""

    def test_compound_valid(self):
        """Test valid compound creation."""
        compound = Compound(name="ethanol", smilesString="CCO", molarity=0.05)
        assert compound.name == "ethanol"
        assert compound.smilesString == "CCO"
        assert compound.molarity == 0.05

    def test_compound_validation_sanitization(self):
        """Test compound name and SMILES string sanitization."""
        # Test name sanitization
        compound = Compound(name="test<script>alert('xss')</script>name")
        assert "<script>" not in compound.name

        # Test SMILES string sanitization
        compound2 = Compound(smilesString="C<script>CO")
        assert "<script>" not in compound2.smilesString


class TestAlloyInfo:
    """Test AlloyInfo model validation."""

    def test_alloy_info_material_id_sanitization(self):
        """Test material ID sanitization."""
        alloy = AlloyInfo(materialID="AA<script>6061</script>")
        assert "<script>" not in alloy.materialID

    def test_alloy_info_temper_code_sanitization(self):
        """Test temper code sanitization."""
        alloy = AlloyInfo(temperCode="T<script>6</script>")
        assert "<script>" not in alloy.temperCode


class TestEnums:
    """Test all enum classes."""

    def test_crystal_structure_enum(self):
        """Test CrystalStructure enum values."""
        assert CrystalStructure.FCC == "FCC"
        assert CrystalStructure.BCC == "BCC"
        assert CrystalStructure.HCP == "HCP"
        assert CrystalStructure.other == "other"

    def test_heat_treatment_type_enum(self):
        """Test HeatTreatmentType enum values."""
        assert HeatTreatmentType.annealing == "annealing"
        assert HeatTreatmentType.quenching == "quenching"
        assert HeatTreatmentType.tempering == "tempering"
        assert HeatTreatmentType.aging == "aging"

    def test_surface_treatment_type_enum(self):
        """Test SurfaceTreatmentType enum values."""
        assert SurfaceTreatmentType.Al == "Al"
        assert SurfaceTreatmentType.SiC == "SiC"
        assert SurfaceTreatmentType.Al2O3 == "Al2O3"

    def test_animal_model_enum(self):
        """Test AnimalModel enum values."""
        assert AnimalModel.rat == "rat"
        assert AnimalModel.mouse == "mouse"
        assert AnimalModel.human == "human"

    def test_ipf_enum(self):
        """Test IPFEnum values."""
        assert IPFEnum.X == "X"
        assert IPFEnum.Y == "Y"
        assert IPFEnum.Z == "Z"


class TestLayerModels:
    """Test all layer parameter models."""

    def test_l0_parameters(self):
        """Test L0Parameters model."""
        l0 = L0Parameters(material="metal")
        assert l0.material == "metal"

    def test_l1_parameters(self):
        """Test L1Parameters model."""
        l1 = L1Parameters(metal="Al")
        assert l1.metal == "Al"

    def test_l2_parameters_complete(self):
        """Test L2Parameters with comprehensive data."""
        l2 = L2Parameters(
            alloy={
                "materialID": "AA6061",
                "nominalComposition": [{"element": "Al", "content": 97.0}],
                "hardeningPrecipitates": [[{"element": "Mg", "content": 50.0}]],
            },
            ebsd={"crystalPhase": [{"phase": "FCC"}], "schmidFactor": 0.45},
            grains={
                "grainSize": 25.3,
                "grainOrientation": {
                    "ipf": "X",
                    "suborientation": [{"percent": 45.2, "millerIndices": [1, 1, 1]}],
                },
            },
            spectroscopy={
                "raman": [520.0, 1580.0],
                "ftir": [1650.0, 2900.0],
                "xrd": [44.7, 65.0],
            },
        )
        # Use attribute access
        assert l2.alloy.materialID == "AA6061"
        assert l2.ebsd.schmidFactor == 0.45
        assert l2.grains.grainSize == 25.3

    def test_l3_parameters_complete(self):
        """Test L3Parameters with comprehensive data."""
        l3 = L3Parameters(
            hardness={
                "nanoHardnessValues": [3.2, 3.5, 3.1],
                "microHardnessValues": [2.5, 2.8, 2.6],
                "vickersHardnessValues": [180.0, 185.0, 178.0],
            },
            heatTreatment={
                "heatTreatmentType": "annealing",
                "heatTreatmentTime": 2.0,
                "heatTreatmentTemperature": 400.0,
            },
            youngsModulus=70.0,
            cast=True,
            abraded={"type": "SiC", "grade": 400},
            polished={"type": "diamond", "grade": 1000},
        )
        # Use attribute access
        assert l3.hardness.nanoHardnessValues == [3.2, 3.5, 3.1]
        assert l3.heatTreatment.heatTreatmentType == "annealing"
        assert l3.youngsModulus == 70.0

    def test_l4_parameters_complete(self):
        """Test L4Parameters with comprehensive corrosion data."""
        l4 = L4Parameters(
            pitting={
                "pitting": True,
                "pittingDepth": 15.2,
                "pittingWidth": 25.8,
                "pittingVolume": 2500.0,
            },
            generalizedCorrosion={
                "generalizedCorrosion": True,
                "corrosionRate": 2.5,
                "corrosionDepth": 8.3,
            },
            electrolyte={
                "pH": [7.0, 6.5],
                "electrolyteVolume": 250.0,
                "electrolyteComposition": [
                    {"name": "NaCl", "smilesString": "NaCl", "molarity": 0.1}
                ],
            },
            filiformCorrosion={
                "filiformCorrosion": True,
                "filiformSiteDensity": 5.2,
                "filiformLength": 8.5,
            },
            droplets={"dropletSize": 2.0, "relativeHumidity": 85.0},
            inVivoTest="rat",
            implantationSite="subcutaneous",
        )
        # Use attribute access
        assert l4.pitting.pittingDepth == 15.2
        assert l4.generalizedCorrosion.corrosionRate == 2.5
        assert l4.inVivoTest == "rat"

    def test_l5_parameters_complete(self):
        """Test L5Parameters with additive manufacturing data."""
        l5 = L5Parameters(
            pillingBedworthRatio=1.28,
            additiveManufacturingDensity=0.98,
            additiveManufacturingCoverGas="Ar",
            additiveManufacturingEnvironment="Ar",
            additiveManufacturingHatchSpacing=80.0,
            additiveManufacturingLaserSpotSize=50.0,
            additiveManufacturingLaserPower=200.0,
            additiveManufacturingLaserSpeed=1000.0,
            additiveManufacturingLayerThickness=30.0,
            additiveManufacturingScanningStrategy="zigzag",
            waam=False,
        )
        assert l5.pillingBedworthRatio == 1.28
        assert l5.additiveManufacturingLaserPower == 200.0
        assert l5.additiveManufacturingScanningStrategy == "zigzag"


class TestMILESData:
    """Test MILESData main model."""

    def test_miles_data_empty(self):
        """Test empty MILESData creation."""
        data = MILESData()
        assert data.l0 is None
        assert data.l1 is None
        assert data.l2 is None
        assert data.l3 is None
        assert data.l4 is None
        assert data.l5 is None

    def test_miles_data_full(self):
        """Test MILESData with all layers."""
        data = MILESData(
            l0={"material": "metal"},
            l1={"metal": "Al"},
            l2={"alloy": {"materialID": "AA6061"}},
            l3={"youngsModulus": 70.0},
            l4={"corrosionTemperature": 25.0},
            l5={"pillingBedworthRatio": 1.28},
        )
        # Use attribute access instead of dictionary access
        assert data.l0.material == "metal"
        assert data.l1.metal == "Al"
        assert data.l2.alloy.materialID == "AA6061"
        assert data.l3.youngsModulus == 70.0
        assert data.l4.corrosionTemperature == 25.0
        assert data.l5.pillingBedworthRatio == 1.28


class TestAPIModels:
    """Test API request/response models."""

    def test_miles_conversion_request(self):
        """Test MILESConversionRequest model."""
        request = MILESConversionRequest(miles="L0ME/L1Al")
        assert request.miles == "L0ME/L1Al"

    def test_miles_conversion_response(self):
        """Test MILESConversionResponse model."""
        response = MILESConversionResponse(miles="L0ME/L1Al")
        assert response.miles == "L0ME/L1Al"

    def test_json_conversion_request(self):
        """Test JSONConversionRequest model."""
        data = MILESData(l0={"material": "metal"})
        request = JSONConversionRequest(body=data)
        # Use attribute access
        assert request.body.l0.material == "metal"

    def test_json_conversion_response(self):
        """Test JSONConversionResponse model."""
        data = MILESData(l0={"material": "metal"})
        response = JSONConversionResponse(data=data)
        # Use attribute access
        assert response.data.l0.material == "metal"
