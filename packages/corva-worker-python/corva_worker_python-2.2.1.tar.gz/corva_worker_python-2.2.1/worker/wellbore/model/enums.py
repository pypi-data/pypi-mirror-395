from enum import Enum

from worker.data.serialization import serialization
from worker.data.unit_conversions import KG_M3_to_PPG


@serialization
class HoleType(Enum):
    CASED_HOLE = "Cased Hole"
    OPEN_HOLE = "Open Hole"
    RISER_LESS = "Riserless"


@serialization
class PipeType(Enum):
    Unknown = "Unknown"
    DP = "Drillpipe"
    HWDP = "Heavy Weight Drillpipe"
    DC = "Drill Collar"
    STABILIZER = "Stabilizer"
    AGITATOR = "Agitator"
    PDM = "Positive Displacement Motor"
    MWD = "Measurement While Drilling"
    RSS = "Rotary Steerable System"
    BIT = "Bit"
    UNDERREAMER = "Under-reamer"
    FLOAT_COLLAR = "Float Collar"
    FLOAT_SHOE = "Float Shoe"
    CROSS_OVER = "Cross Over"
    TOE_SLEEVE = "Toe Sleeve"
    CASING_JOINTS = "Casing Joints"
    DV_TOOL = "Differential Valve Tool"
    ACP = "Annular Casing Packer"
    RISER = "Riser"

    @staticmethod
    def determine_type(family: str):
        family = family.lower()
        mapping = {
            "dp": PipeType.DP,
            "hwdp": PipeType.HWDP,
            "dc": PipeType.DC,
            "stabilizer": PipeType.STABILIZER,
            "agitator": PipeType.AGITATOR,
            "pdm": PipeType.PDM,
            "mwd": PipeType.MWD,
            "rss": PipeType.RSS,
            "bit": PipeType.BIT,
            "ur": PipeType.UNDERREAMER,
            "float_collar": PipeType.FLOAT_COLLAR,
            "float_shoe": PipeType.FLOAT_SHOE,
            "cross_over": PipeType.CROSS_OVER,
            "toe_sleeve": PipeType.TOE_SLEEVE,
            "casing_joints": PipeType.CASING_JOINTS,
            "dv_tool": PipeType.DV_TOOL,
            "acp": PipeType.ACP,
            "riser": PipeType.RISER,
        }
        _type = mapping.get(family)
        if not _type:
            _type = PipeType.Unknown

        return _type


@serialization
class PipeMaterial(Enum):
    Steel = {"density": 7850 * KG_M3_to_PPG, "modulus_of_elasticity": 29.9e6, "poisson_ratio": 0.30}
    Aluminium = {"density": 2700 * KG_M3_to_PPG, "modulus_of_elasticity": 10.5e6, "poisson_ratio": 0.32}
    Titanium = {"density": 4506 * KG_M3_to_PPG, "modulus_of_elasticity": 16.5e6, "poisson_ratio": 0.31}
    NonMagnetic = {"density": 7850 * KG_M3_to_PPG, "modulus_of_elasticity": 29.9e6, "poisson_ratio": 0.30}

    def get_density(self) -> float:
        """
        Get the density of the pipe material
        :return: pipe density PPG
        """
        return self["density"]

    def get_modulus_of_elasticity(self) -> float:
        """
        Get the pipe modulus of elasticity
        :return: modulus of elasticity in PSI
        """
        return self["modulus_of_elasticity"]

    def get_poisson_ratio(self) -> float:
        """
        Get the Poisson ratio
        :return: Poisson ratio
        """
        return self["poisson_ratio"]
