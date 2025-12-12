import re
from pydantic import BaseModel, Field, field_validator
from typing import Any, List, Optional
from enum import Enum


class MILESField(BaseModel):
    code: Optional[str] = None
    is_composition: bool = False
    is_element: bool = False
    is_enum: bool = False
    is_parent: bool = False
    is_string: bool = False
    is_grain_boundary: bool = False
    example: Optional[Any] = None
    enum: Optional[List[Any]] = None
    label: Optional[str] = None


def miles_field(
    default=None,
    code=None,
    is_parent=False,
    is_composition=False,
    is_string=False,
    is_element=False,
    is_enum=False,
    is_grain_boundary=False,
    example=None,
    enum=None,
    label=None,
    **kwargs,
):
    """Create a Pydantic field with MILES metadata."""
    miles_meta = MILESField(
        code=code,
        is_parent=is_parent,
        is_composition=is_composition,
        is_string=is_string,
        is_element=is_element,
        is_enum=is_enum,
        is_grain_boundary=is_grain_boundary,
        example=example,
        enum=enum,
        label=label,
    )

    # Store in both json_schema_extra AND in the field's metadata for redundancy
    json_schema_extra = kwargs.get("json_schema_extra", {})
    json_schema_extra["miles"] = miles_meta
    kwargs["json_schema_extra"] = json_schema_extra

    return Field(default=default, **kwargs)


class CompositionPart(BaseModel):
    element: str = miles_field(
        description="Chemical element symbol from the periodic table (e.g., 'Fe' for Iron)",
        example="Fe",
        max_length=2,
    )
    content: float = miles_field(
        description="Element content in atomic percent (At.%) or ppm (e.g., for the annealing atmosphere). If an element is found, the content can not be null or 0.0.",
        ge=0.0,
        example="18.0",
    )


class CrystalStructure(str, Enum):
    FCC = "FCC"
    BCC = "BCC"
    HCP = "HCP"
    other = "other"


class CrystalPhase(BaseModel):
    phase: Optional[CrystalStructure] = miles_field(
        default=None,
        is_enum=True,
        description="Crystal phase of any phase present in a major quantity, e.g., 'FCC','BCC' or 'HCP'",
        example="FCC",
    )
    composition: Optional[List[CompositionPart]] = miles_field(
        default=None,
        is_composition=True,
        description="Composition of the crystal phase, as a list of elements and their contents (At.%).",
        example=[
            {"element": "Fe", "content": 68.0},
            {"element": "Cr", "content": 18.0},
        ],
    )


# Adding a Material type with Enum somehow does not work
class L0Parameters(BaseModel):
    material: str = miles_field(
        code="MA",
        description="Material name or type, e.g., 'metal'",
        example="metal",
        enum=["metal"],
    )


class L1Parameters(BaseModel):
    metal: Optional[str] = miles_field(
        default=None,
        code="BM",
        description="Elemental symbol of main metal name or type, e.g., 'Mg' or 'Fe'. For alloys, the balance metal is meant.",
        example="Mg",
    )


CompositionArrayPart = List[CompositionPart]


class AlloyInfo(BaseModel):
    materialID: Optional[str] = miles_field(
        default=None,
        is_string=True,
        code="ID",
        label="Material ID",
        max_length=50,
        description="Commercial, standard name or UNS number of the alloy or metal",
        example="AA6061",
    )
    elementalComposition: Optional[List[CompositionPart]] = miles_field(
        default=None,
        code="EC",
        is_composition=True,
        description="Elemental (or chemical) composition of the alloy in atomic percent",
        example=[{"element": "Al", "content": 97.9}, {"element": "Mg", "content": 1.0}],
    )
    nominalComposition: Optional[List[CompositionPart]] = miles_field(
        default=None,
        code="NC",
        is_composition=True,
        description="Nominal composition of the alloy in atomic percent",
        example=[{"element": "Al", "content": 97.9}, {"element": "Mg", "content": 1.0}],
    )
    hardeningPrecipitates: Optional[List[CompositionArrayPart]] = miles_field(
        default=None,
        code="HP",
        is_composition=True,
        description="Composition of hardening precipitates present in the alloy",
        example=[
            [
                {"element": "Mg", "content": 50.0},
                {"element": "Si", "content": 50.0},
            ]
        ],
    )
    intermetallics: Optional[List[CompositionArrayPart]] = miles_field(
        default=None,
        code="IM",
        is_composition=True,
        description="Composition of intermetallic phases present in the alloy",
        example=[
            [
                {"element": "Al", "content": 66.7},
                {"element": "Cu", "content": 33.3},
            ]
        ],
    )
    dispersoidParticles: Optional[List[CompositionPart]] = miles_field(
        default=None,
        code="DI",
        is_composition=True,
        description="Composition of dispersoid particles in the alloy",
        example=[
            {"element": "Al", "content": 75.0},
            {"element": "Mn", "content": 25.0},
        ],
    )
    presenceOfMischmetal: Optional[bool] = miles_field(
        default=None,
        code="ME",
        description="Presence of Misch Metal in Mg alloys.",
        example=True,
    )

    temperCode: Optional[str] = miles_field(
        default=None,
        is_string=True,
        max_length=50,
        code="TC",
        description="Temper code for wrought Al alloys.",
        example="T6",
    )

    @field_validator("materialID", "temperCode")
    @classmethod
    def sanitize_string(cls, v: Optional[str]) -> Optional[str]:
        """Sanitize material ID to prevent injection attacks"""
        if not v:
            return v

        # Remove potentially dangerous characters, allow alphanumeric, dash, underscore, dot
        sanitized = re.sub(r"[^\w\-_.]", "", v)

        # Truncate to maximum length
        return sanitized[:50] if sanitized else None


class SubOrientation(BaseModel):
    percent: Optional[float] = miles_field(
        default=None,
        description="Percentage of material with this sub-orientation",
        example=25.5,
    )
    millerIndices: Optional[List[int]] = miles_field(
        default=None,
        description="Miller indices defining the crystallographic orientation [h,k,l]",
        example=[1, 0, 0],
    )


class IPFEnum(str, Enum):
    X = "X"
    Y = "Y"
    Z = "Z"


class CrystalOrientation(BaseModel):
    ipf: Optional[IPFEnum] = miles_field(
        default=None,
        code="C",
        label="IPF",
        is_enum=True,
        description="Inverse pole figure direction or texture component",
        example="X",
    )
    suborientation: Optional[List[SubOrientation]] = miles_field(
        default=None,
        code="CO",
        description="List of sub-orientations with their respective percentages",
        example=[{"percent": 45.2, "millerIndices": [1, 1, 1]}],
    )


class GrainBoundary(BaseModel):
    grainInterface: List[List[CompositionPart]] = miles_field(
        default=None,
        description="Chemical compositions of the respective phases sharing a boundary, relating to secondary phases as defined by the intermetallics.",
        example=["Mg50.0Zn50.0", "Mg33.3Cu66.7"],
    )
    boundaryLength: float = miles_field(
        default=None,
        description="Length of the grain boundary for the respective interface in m/cm²",
        example=15.2,
    )


class Grains(BaseModel):
    grainAveragedMap: Optional[float] = miles_field(
        default=None,
        code="GA",
        description="Grain-averaged map value in micrometers",
        example=12.5,
    )
    grainBoundaryLength: Optional[float] = miles_field(
        default=None,
        code="BL",
        description="Total grain boundary length per unit area in m/cm²",
        example=0.85,
    )
    grainBoundaries: Optional[List[GrainBoundary]] = miles_field(
        default=None,
        code="GX",
        is_grain_boundary=True,
        description="List of grain boundaries between phases",
    )
    grainBoundaryPhase: Optional[List[CompositionPart]] = miles_field(
        default=None,
        code="GP",
        is_composition=True,
        description="The grain boundary phase decorating the grain boundaries. The value provides the phase stochiometry.",
        example=[
            {"element": "Al", "content": 66.7},
            {"element": "Cu", "content": 33.3},
        ],
    )
    grainBoundaryDepletionZone: Optional[float] = miles_field(
        default=None,
        code="GZ",
        description="Width of the depletion zone at grain boundaries in nanometers",
        example=50.0,
    )
    grainSize: Optional[float] = miles_field(
        default=None,
        code="GS",
        description="Average grain size in micrometers",
        example=25.3,
    )


class EBSD(BaseModel):
    crystalPhase: Optional[List[CrystalPhase]] = miles_field(
        default=None,
        code="CP",
        description="List of crystal phases present in the material",
    )

    crystalOrientation: Optional[CrystalOrientation] = miles_field(
        default=None,
        is_parent=True,
        description="Crystallographic texture and orientation information for grains.",
    )

    kernelAveragedMap: Optional[float] = miles_field(
        default=None,
        code="KA",
        description="Kernel averaged map information that reflects the level of dislocations locally providing an indication of residual strain. The value is the percentage of the largest misorientation angle of 6˚ of all misorientations 6° and under.",
        example=2.1,
    )
    lowAngleGrainBoundary: Optional[float] = miles_field(
        default=None,
        code="LA",
        description="Fraction of low-angle grain boundaries (< 15°) in percentage",
        example=0.15,
    )
    schmidFactor: Optional[float] = miles_field(
        default=None,
        code="SF",
        description="Schmid factor as obtained from EBSD analysis.",
        example=0.45,
        ge=0.0,
        le=0.5,
    )
    sigma3: Optional[float] = miles_field(
        default=None,
        code="ST",
        description="Fraction of Σ3 grain boundaries in percentage as obtained from EBSD analysis",
        example=0.08,
    )


class Spectroscopy(BaseModel):
    raman: Optional[List[float]] = miles_field(
        default=None,
        code="RA",
        description="Raman spectroscopy data with wavenumbers in cm⁻¹",
        example=[520.0, 1580.0, 2700.0],
    )
    ftir: Optional[List[float]] = miles_field(
        default=None,
        code="FT",
        label="FTIR",
        description="FTIR spectroscopy data with wavenumbers in cm⁻¹",
        example=[1650.0, 2900.0, 3400.0],
    )
    xrd: Optional[List[float]] = miles_field(
        default=None,
        code="XR",
        label="XRD",
        description="X-ray diffraction peak positions in 2θ degrees",
        example=[44.7, 65.0, 82.4],
    )


class L2Parameters(BaseModel):
    alloy: Optional[AlloyInfo] = miles_field(
        default=None,
        is_parent=True,
        description="Information about the alloy composition and phases",
    )
    ebsd: Optional[EBSD] = miles_field(
        default=None,
        is_parent=True,
        label="EBSD",
        description="Electron backscatter diffraction (EBSD) data about the microstructure",
    )
    grains: Optional[Grains] = miles_field(
        default=None,
        is_parent=True,
        description="Grain structure characteristics and measurements",
    )
    phaseNumber: Optional[int] = miles_field(
        default=None,
        code="CN",
        description="Number of distinct phases present in the material",
        example=2,
    )
    dendriteArmSpacing: Optional[float] = miles_field(
        default=None,
        code="DA",
        description="Dendrite arm spacing in micrometers",
        example=15.8,
    )
    intermetallicClustering: Optional[float] = miles_field(
        default=None,
        code="IC",
        description="Intermetallic clustering normally obtained from the peak of the radial distribution function using centroid positions for all particles (0-1 scale)",
        example=0.3,
    )
    geometricallyNecessaryDislocations: Optional[float] = miles_field(
        default=None,
        code="GD",
        description="Geometrically necessary dislocation density in m⁻²",
        example=1.0,
    )
    spectroscopy: Optional[Spectroscopy] = miles_field(
        default=None,
        is_parent=True,
        description="Spectroscopy data including Raman, FTIR, and XRD measurements",
    )


class Hardness(BaseModel):
    microHardnessValues: Optional[List[float]] = miles_field(
        default=None,
        code="HM",
        description="Microhardness measurements in HV or GPa",
        example=[2.5, 2.8, 2.6],
    )
    nanoHardnessValues: Optional[List[float]] = miles_field(
        default=None,
        code="HN",
        description="Nanohardness measurements in GPa",
        example=[3.2, 3.5, 3.1],
    )

    vickersHardnessValues: Optional[List[float]] = miles_field(
        default=None,
        code="HV",
        description="Vickers hardness measurements in HV",
        example=[180.0, 185.0, 178.0],
    )
    hardnessSeparationLength: Optional[float] = miles_field(
        default=None,
        code="HS",
        description="Separation length between hardness measurements in millimeters",
        example=0.01,
    )


class SurfaceTreatmentType(str, Enum):
    Al = "Al"
    SiC = "SiC"
    Al2O3 = "Al2O3"
    acidic_SiC = "acidic_SiC"
    diamond = "diamond"


class SurfaceTreatment(BaseModel):
    type: Optional[SurfaceTreatmentType] = miles_field(
        default=None,
        is_enum=True,
        description="Type of surface treatment applied",
        example="SiC",
    )
    grade: Optional[int] = miles_field(
        default=None,
        description="Grade or roughness level of the surface treatment",
        example=400,
    )


class HeatTreatmentType(str, Enum):
    annealing = "annealing"
    quenching = "quenching"
    tempering = "tempering"
    aging = "aging"


class HeatTreatment(BaseModel):
    heatTreatmentType: Optional[HeatTreatmentType] = miles_field(
        default=None,
        code="HT",
        is_string=True,
        is_enum=True,
        description="Type of heat treatment applied",
        example="annealing",
    )
    heatTreatmentTime: Optional[float] = miles_field(
        default=None,
        code="TI",
        description="Duration of heat treatment process in hours.",
        example=2.0,
    )
    heatTreatmentTemperature: Optional[float] = miles_field(
        default=None,
        code="TE",
        description="Temperature during heat treatment in Celsius",
        example=400.0,
    )
    heatTreatmentAtmosphereComposition: Optional[List[CompositionPart]] = miles_field(
        default=None,
        code="HA",
        is_composition=True,
        description="Composition of the heat treatment atmosphere, including elemental symbols and their concentration in ppm.",
        example=[{"element": "H", "content": 1000.0}],
    )


class RolledSurface(BaseModel):
    numberRollingPasses: Optional[int] = miles_field(
        default=None,
        code="NP",
        description="Number of rolling passes applied to the surface",
        example=5,
    )
    gaugeReductionThickness: Optional[float] = miles_field(
        default=None,
        code="NG",
        description="Thickness of the sheet in millimeters",
        example=1.2,
    )


class ExtrusionMode(str, Enum):
    direct = "direct"
    backwards = "backwards"
    equichannel = "equichannel"


class CladLayer(BaseModel):
    cladLayerThickness: Optional[float] = miles_field(
        default=None,
        code="CL",
        description="Thickness of the clad layer in micrometers",
        example=100.0,
    )
    composition: Optional[List[CompositionPart]] = miles_field(
        default=None,
        code="EC",
        is_composition=True,
        description="Composition of the clad layer, including elemental symbols and their concentration in ppm.",
        example=[
            {"element": "Al", "content": 90.0},
            {"element": "Cu", "content": 10.0},
        ],
    )


class L3Parameters(BaseModel):
    hardness: Optional[Hardness] = miles_field(
        default=None,
        is_parent=True,
        description="Various hardness measurements and mapping parameters",
    )
    heatTreatment: Optional[HeatTreatment] = miles_field(
        default=None,
        is_parent=True,
        description="Details about the heat treatment process.",
    )
    breakingElongation: Optional[float] = miles_field(
        default=None,
        code="EG",
        description="Average elongation at break of the material in percentage",
        example=5.0,
    )
    youngsModulus: Optional[float] = miles_field(
        default=None, code="YM", description="Young's modulus in GPa", example=70.0
    )
    shearStress: Optional[float] = miles_field(
        default=None, code="SS", description="Shear stress in N/m²", example=150.0
    )
    yieldStrength: Optional[float] = miles_field(
        default=None, code="YS", description="Yield strength in GPa", example=250.0
    )
    abraded: Optional[SurfaceTreatment] = miles_field(
        default=None, code="AB", description="Details about the abrasion process."
    )
    deformedLayerThickness: Optional[float] = miles_field(
        default=None,
        code="DE",
        description="Thickness of the deformed surface layer in micrometers",
        example=5.2,
    )
    billetExtrusionRatio: Optional[float] = miles_field(
        default=None,
        code="BE",
        description="For extrusion applications – cross section ratio of billet/extrusion.",
        example=1.5,
    )
    extrusionSpeed: Optional[float] = miles_field(
        default=None,
        code="ES",
        description="Speed of the extrusion process in meters per second.",
        example=2.0,
    )
    extrusionMode: Optional[ExtrusionMode] = miles_field(
        default=None,
        code="EM",
        is_enum=True,
        is_string=True,
        description="Mode of the extrusion process.",
        example="direct",
    )
    extrusionTemperature: Optional[float] = miles_field(
        default=None,
        code="ET",
        description="Temperature during the extrusion process in Celsius.",
        example=400.0,
    )
    cast: Optional[bool] = miles_field(
        default=None,
        code="CA",
        description="Indicates if the material was cast",
        example=False,
    )
    coldDrawing: Optional[bool] = miles_field(
        default=None,
        code="CD",
        description="Indicates if cold drawing was applied",
        example=True,
    )
    drawn: Optional[bool] = miles_field(
        default=None,
        code="DR",
        description="Indicates if the material was drawn",
        example=False,
    )
    extruded: Optional[bool] = miles_field(
        default=None,
        code="EX",
        description="Indicates if the material was extruded",
        example=True,
    )
    forged: Optional[bool] = miles_field(
        default=None,
        code="FO",
        description="Indicates if the material was forged",
        example=False,
    )
    shingling: Optional[bool] = miles_field(
        default=None,
        code="SH",
        description="Indicates if shingling defects are present",
        example=False,
    )
    shotPeened: Optional[bool] = miles_field(
        default=None,
        code="SP",
        description="Indicates if shot peening was applied",
        example=True,
    )
    wrought: Optional[bool] = miles_field(
        default=None,
        code="WR",
        description="Indicates if the material was wrought",
        example=True,
    )
    oxideComposition: Optional[List[CompositionPart]] = miles_field(
        default=None,
        code="OC",
        is_composition=True,
        description="Composition of oxide layer on the surface",
        example=[{"element": "Al", "content": 40.0}, {"element": "O", "content": 60.0}],
    )
    oxideThickness: Optional[float] = miles_field(
        default=None,
        code="OX",
        description="Thickness of oxide layer in micrometers",
        example=3.2,
    )
    polished: Optional[SurfaceTreatment] = miles_field(
        default=None,
        code="PO",
        description="Details about the polishing process applied",
    )
    ionBeamMilling: Optional[bool] = miles_field(
        default=None,
        code="IB",
        description="Indicates if ion beam milling was used for surface preparation",
        example=True,
    )
    rolledSurface: Optional[RolledSurface] = miles_field(
        default=None,
        code="RO",
        is_parent=True,
        description="Parameters related to surface rolling treatment",
    )
    cladLayer: Optional[CladLayer] = miles_field(
        default=None,
        is_parent=True,
        description="Details about the cladding layer applied",
    )
    mechanicalStress: Optional[bool] = miles_field(
        default=None,
        code="ME",
        description="Indicates if mechanical stress is present or was applied",
        example=False,
    )
    organicCoating: Optional[bool] = miles_field(
        default=None,
        code="PA",
        description="Indicates if an organic coating is present",
        example=True,
    )
    organicCoatingThickness: Optional[float] = miles_field(
        default=None,
        code="PT",
        description="Thickness of organic coating in micrometers",
        example=5.0,
    )
    platingBathTemperature: Optional[float] = miles_field(
        default=None,
        code="ZT",
        description="The plating bath temperature of sacrificial metallic anode in Celsius",
        example=460.0,
    )
    platingBathImmersionTime: Optional[float] = miles_field(
        default=None,
        code="ZI",
        description="Immersion time in plating bath in seconds",
        example=3.5,
    )
    airKnifePressure: Optional[float] = miles_field(
        default=None,
        code="ZK",
        description="Air knife pressure for zinc coating control in bar",
        example=2.1,
    )
    stressCorrosion: Optional[bool] = miles_field(
        default=None,
        code="SC",
        description="Indicates that stress corrosion cracking is the form of degradation.",
        example=False,
    )


class Compound(BaseModel):
    name: Optional[str] = miles_field(
        default=None,
        is_string=True,
        max_length=100,
        code="CN",
        description="Name of the chemical compound",
        example="4,5-diaminopyrimidine",
    )
    smilesString: Optional[str] = miles_field(
        default=None,
        is_string=True,
        max_length=500,
        code="SM",
        description="SMILES notation for chemical structure",
        example="CCO",
    )
    molarity: Optional[float] = miles_field(
        default=None,
        description="Molarity of the compound in solution in mol/L",
        example=0.05,
    )

    @field_validator("name")
    @classmethod
    def sanitize_compound_name(cls, v: Optional[str]) -> Optional[str]:
        """Sanitize compound name to prevent injection attacks"""
        if not v:
            return v

        # Remove potentially dangerous characters, allow alphanumeric, dash, underscore, dot
        sanitized = re.sub(r"[^\w\-_.]", "", v)

        # Truncate to maximum length
        return sanitized[:50] if sanitized else None

    @field_validator("smilesString")
    @classmethod
    def sanitize_smiles_string(cls, v: Optional[str]) -> Optional[str]:
        """Sanitize SMILES string to prevent injection attacks"""
        if not v:
            return v

        # Remove potentially dangerous characters, allow alphanumeric, dash, underscore, dot
        sanitized = re.sub(r"[^\w\-_.()=+\[\]#@/:]+", "", v)

        # Truncate to maximum length
        return sanitized[:50] if sanitized else None


ElectrolyteComposition = List[Compound]


class Electrolyte(BaseModel):
    electrolyteVolume: Optional[float] = miles_field(
        default=None,
        code="VO",
        description="Volume of the electrolyte for immersion experiments in cm³",
        example=250.0,
    )
    electrolyteComposition: Optional[ElectrolyteComposition] = miles_field(
        default=None,
        is_composition=True,
        code="EL",
        description="Detailed composition of the electrolyte solution",
        example=[{"smilesString": "NaCl", "molarity": 0.1}],
    )
    electrolyteRenewalFrequency: Optional[float] = miles_field(
        default=None,
        code="ER",
        description="Frequency of electrolyte renewal in hours",
        example=24.0,
    )
    pH: Optional[List[float]] = miles_field(
        default=None,
        code="PH",
        label="pH",
        description="Initial and final pH level of the electrolyte solution. When only one value is provided, the final pH is meant.",
        examples=[7.0, 6.5],
    )
    ratioElectrolyteSurface: Optional[float] = miles_field(
        default=None,
        code="VA",
        description="The ratio of electrolyte volume to sample surface area in mL/cm²",
        example=0.5,
    )
    inhibitionEfficiency: Optional[float] = miles_field(
        default=None,
        code="IE",
        description="Inhibition efficiency (IE) in percentage calculated from the formula IE%= 100*(I_corr-I_inhib)/I_corr.",
        example=88.7,
    )
    inhibitionEfficiencySymmetrical: Optional[float] = miles_field(
        default=None,
        code="IS",
        description="Symmetrical inhibition efficiency (IE_sym) in percentage. IEsym = IE if IE≥0 otherwise IEsym = -100(I_inhib-I_corr)/I_inhib.",
        example=92.5,
    )
    inhibitionPower: Optional[float] = miles_field(
        default=None,
        code="IP",
        description="Inhibition power (IP) calculated from the formula IP= 10log10(I_corr/I_inhib).",
        example=0.95,
    )


class Pitting(BaseModel):
    pitting: Optional[bool] = miles_field(
        default=None,
        code="PI",
        description="Indicates presence of pitting corrosion",
        example=False,
    )
    pittingDepth: Optional[float] = miles_field(
        default=None,
        code="PD",
        description="Average depth of pitting corrosion in micrometers",
        example=15.2,
    )
    pittingWidth: Optional[float] = miles_field(
        default=None,
        code="PW",
        description="Average width of pitting corrosion in micrometers",
        example=25.8,
    )
    pittingVolume: Optional[float] = miles_field(
        default=None,
        code="PV",
        description="Volume of material lost due to pitting in μm³",
        example=2500.0,
    )
    pittingExtremeValue: Optional[float] = miles_field(
        default=None,
        code="PE",
        description="Maximum pitting depth recorded in micrometers",
        example=35.1,
    )
    pittingDensity: Optional[float] = miles_field(
        default=None,
        code="PR",
        description="Number of pits per unit area (pits/cm²)",
        example=12.5,
    )


class GeneralizedCorrosion(BaseModel):
    generalizedCorrosion: Optional[bool] = miles_field(
        default=None,
        code="GE",
        description="Indicates presence of generalized corrosion",
        example=False,
    )
    corrosionRate: Optional[float] = miles_field(
        default=None,
        code="CR",
        description="General corrosion rate in mm/year",
        example=2.5,
    )
    corrosionDepth: Optional[float] = miles_field(
        default=None,
        code="CD",
        description="Average depth of general corrosion in micrometers",
        example=8.3,
    )


class Droplets(BaseModel):
    dropletSize: Optional[float] = miles_field(
        default=None,
        code="DS",
        description="Average size of water droplets in millimeters",
        example=2.0,
    )
    dropletDensity: Optional[float] = miles_field(
        default=None,
        code="DD",
        description="Number of droplets per unit area (droplets/dm²)",
        example=15.2,
    )
    relativeHumidity: Optional[float] = miles_field(
        default=None,
        code="RH",
        description="Relative humidity during testing in percentage",
        example=85.0,
    )
    dropletContactAngle: Optional[float] = miles_field(
        default=None,
        code="DA",
        description="Contact angle of droplets on surface in degrees",
        example=65.2,
    )
    dropletSurfaceAngle: Optional[float] = miles_field(
        default=None,
        code="SA",
        description="Angle of surface relative to horizontal in degrees",
        example=45.0,
    )


class FiliformCorrosion(BaseModel):
    filiformCorrosion: Optional[bool] = miles_field(
        default=None,
        code="FI",
        description="Indicates presence of filiform corrosion",
        example=False,
    )
    filiformSiteDensity: Optional[float] = miles_field(
        default=None,
        code="FD",
        description="Density of filiform corrosion initiation sites per as number per millimeter",
        example=5.2,
    )
    filiformLength: Optional[float] = miles_field(
        default=None,
        code="FL",
        description="Average length of filiform corrosion tracks in mm",
        example=8.5,
    )


class ImplantationSite(str, Enum):
    joint_replacement = "joint_replacement"
    bone = "bone"
    spine = "spine"
    small_bones_joints = "small_bones_joints"
    cranio_maxillofacial = "cranio_maxillofacial"
    dental = "dental"
    arteries = "arteries"
    heart = "heart"
    pacemaker = "pacemaker"
    defibrillator = "defibrillator"
    tendon = "tendon"
    ligament = "ligament"
    subcutaneous = "subcutaneous"
    muscle = "muscle"
    ureteral = "ureteral"
    bladder = "bladder"
    gastrointestinal = "gastrointestinal"
    nerves = "nerves"
    brain = "brain"


class AnimalModel(str, Enum):
    rat = "rat"
    mouse = "mouse"
    rabbit = "rabbit"
    guinea_pig = "guinea_pig"
    dog = "dog"
    cat = "cat"
    non_human_primate = "non_human_primate"
    human = "human"


class L4Parameters(BaseModel):
    pitting: Optional[Pitting] = miles_field(
        default=None,
        is_parent=True,
        description="Parameters related to pitting corrosion analysis",
    )
    crevice: Optional[bool] = miles_field(
        default=None,
        code="CC",
        description="Indicates presence of crevice corrosion conditions",
        example=True,
    )
    experimentDuration: Optional[float] = miles_field(
        default=None,
        code="ED",
        description="Duration of the experiment in minutes",
        example=168.0,
    )
    electrolyte: Optional[Electrolyte] = miles_field(
        default=None,
        is_parent=True,
        description="Electrolyte solution parameters and composition",
    )
    corrosionTemperature: Optional[float] = miles_field(
        default=None,
        code="ET",
        description="Temperature during corrosion testing in Celsius",
        example=25.0,
    )
    generalizedCorrosion: Optional[GeneralizedCorrosion] = miles_field(
        default=None,
        is_parent=True,
        description="Parameters for generalized corrosion analysis",
    )
    filiformCorrosion: Optional[FiliformCorrosion] = miles_field(
        default=None,
        is_parent=True,
        description="Parameters related to filiform corrosion",
    )
    immersionTime: Optional[float] = miles_field(
        default=None,
        code="IM",
        description="Sample immersion time in hours",
        example=24.0,
    )
    breakDownPotential: Optional[float] = miles_field(
        default=None,
        code="IB",
        description="Breakdown potential in V vs reference electrode",
        example=-0.65,
    )
    referenceElectrode: Optional[str] = miles_field(
        default=None,
        is_string=True,
        max_length=50,
        code="RE",
        description="Type of reference electrode used in electrochemical measurements",
        example="Ag/AgCl",
    )
    corrosionCurrent: Optional[float] = miles_field(
        default=None,
        code="IC",
        description="Corrosion current at OCP in μA/cm²",
        example=1.2e-6,
    )
    cyclicEnvironment: Optional[bool] = miles_field(
        default=None,
        code="CY",
        description="Indicates if cyclic environmental conditions were used",
        example=True,
    )
    droplets: Optional[Droplets] = miles_field(
        default=None,
        is_parent=True,
        description="Parameters related to droplet exposure conditions",
    )
    anaerobicEnvironment: Optional[bool] = miles_field(
        default=None,
        code="AN",
        description="Indicates if testing was performed under anaerobic conditions",
        example=False,
    )
    electrodeSurfaceArea: Optional[float] = miles_field(
        default=None,
        code="SE",
        description="Surface area of working electrode in cm²",
        example=1.0,
    )
    inVivoTest: Optional[AnimalModel] = miles_field(
        default=None,
        code="IV",
        is_string=True,
        is_enum=True,
        description="Animal model for in-vivo tests",
        example="rat",
    )
    implantationSite: Optional[ImplantationSite] = miles_field(
        default=None,
        code="IW",
        is_string=True,
        is_enum=True,
        description="Description of implantation site for in vivo test",
        example="subcutaneous_tissue",
    )
    inVitroTest: Optional[List[Compound]] = miles_field(
        default=None,
        code="IT",
        is_composition=True,
        description="Description of in-vitro test conditions or results",
        example=[
            {"smilesString": "O", "molarity": 55.5},
            {"smilesString": "[Na+].[Cl-]", "molarity": 0.142},
            {"smilesString": "[K+].[Cl-]", "molarity": 0.005},
            {"smilesString": "[Ca+2].[Cl-].[Cl-]", "molarity": 0.0025},
            {"smilesString": "[Mg+2].[Cl-].[Cl-]", "molarity": 0.0015},
            {"smilesString": "[Na+].[Na+].[O-]P(=O)([O-])[O-]", "molarity": 0.001},
            {"smilesString": "[Na+].[Na+].C(=O)([O-])[O-]", "molarity": 0.004},
        ],
    )
    blistering: Optional[float] = miles_field(
        default=None,
        code="ZB",
        description="Blistering of the layer where the value the maximum blister size in millimeters after 1000 hours of exposure in salt spray tests.",
        example=1.0,
    )
    edgeCreep: Optional[float] = miles_field(
        default=None,
        code="ZC",
        description="Edge creep where the value is expressed in millimeters after 1000 hours of exposure in salt spray tests.",
        example=0.5,
    )
    massLoss: Optional[float] = miles_field(
        default=None,
        code="ZM",
        description="Mass Loss in g/m²/day after 1000 hours of exposure in salt spray tests.",
        example=15.2,
    )
    redRustFormation: Optional[float] = miles_field(
        default=None,
        code="ZR",
        description="The time at which the first red rust formation covers around 5% of the surface.",
        example=2.1,
    )
    surfaceStress: Optional[bool] = miles_field(
        default=None,
        code="SU",
        description="Indicates if surface stress affects corrosion behavior",
        example=True,
    )


class ScanningStrategy(str, Enum):
    zigzag = "zigzag"
    meander = "meander"
    contour = "contour"
    raster = "raster"
    spiral = "spiral"


class L5Parameters(BaseModel):
    pillingBedworthRatio: Optional[float] = miles_field(
        default=None,
        code="PB",
        description="Pilling-Bedworth ratio for oxide formation defined as the ratio of the density of the oxide volume compared to the metal",
        example=1.28,
    )
    additiveManufacturingDensity: Optional[float] = miles_field(
        default=None,
        code="LD",
        description="Density of additively manufactured part relative to full density, in percentage",
        example=0.98,
    )
    additiveManufacturingCoverGas: Optional[str] = miles_field(
        default=None,
        code="LG",
        is_element=True,
        description="Cover gas used during additive manufacturing, using the elemental symbol for the main gas, e.g. Ar for Argon.",
        example="Ar",
    )
    additiveManufacturingEnvironment: Optional[str] = miles_field(
        default=None,
        code="LE",
        is_element=True,
        description="Atmosphere during additive manufacturing process, e.g. Ar for Argon.",
        example="Ar",
    )
    additiveManufacturingHatchSpacing: Optional[float] = miles_field(
        default=None,
        code="LH",
        description="Hatch spacing in additive manufacturing in micrometers",
        example=80.0,
    )
    additiveManufacturingLaserSpotSize: Optional[float] = miles_field(
        default=None,
        code="LL",
        description="Laser spot diameter in micrometers",
        example=50.0,
    )
    additiveManufacturingLaserPower: Optional[float] = miles_field(
        default=None,
        code="LP",
        description="Laser power setting in Watts",
        example=200.0,
    )
    additiveManufacturingLaserSpeed: Optional[float] = miles_field(
        default=None,
        code="LS",
        description="Laser scanning speed in mm/s",
        example=1000.0,
    )
    additiveManufacturingLayerThickness: Optional[float] = miles_field(
        default=None,
        code="LT",
        description="Powder bed layer thickness in additive manufacturing in micrometers",
        example=30.0,
    )
    additiveManufacturingScanningStrategy: Optional[ScanningStrategy] = miles_field(
        default=None,
        code="LX",
        is_string=True,
        is_enum=True,
        description="Laser scanning pattern or strategy used",
        example="zigzag",
    )
    additiveManufacturingPowderSizeDistribution: Optional[float] = miles_field(
        default=None,
        code="PD",
        description="Average powder particle size in micrometers",
        example=25.0,
    )
    additiveManufacturingPreheatTemperature: Optional[float] = miles_field(
        default=None,
        code="PT",
        description="Preheat temperature of the powder bed prior to heating in Celsius",
        example=200.0,
    )
    waam: Optional[bool] = miles_field(
        default=None,
        code="LW",
        label="WAAM",
        description="Indicates if wire arc additive manufacturing (WAAM) was used",
        example=False,
    )


class MILESData(BaseModel):
    l0: Optional[L0Parameters] = None
    l1: Optional[L1Parameters] = None
    l2: Optional[L2Parameters] = None
    l3: Optional[L3Parameters] = None
    l4: Optional[L4Parameters] = None
    l5: Optional[L5Parameters] = None


# API Models


class MILESConversionRequest(BaseModel):
    miles: str


class JSONConversionRequest(BaseModel):
    body: MILESData


class MILESConversionResponse(BaseModel):
    miles: str


class JSONConversionResponse(BaseModel):
    data: MILESData
