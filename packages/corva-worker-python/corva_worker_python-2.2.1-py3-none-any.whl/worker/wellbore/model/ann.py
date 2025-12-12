import numpy as np

from worker.data.operations import nanround
from worker.data.serialization import serialization
from worker.wellbore.model.drillstring_components import Pipe
from worker.wellbore.model.element import Element
from worker.wellbore.model.enums import HoleType
from worker.wellbore.model.hole_section import HoleSection


@serialization
class Ann(Element):
    """
    This class is extended to create annulus segment
    It can be done by passing arguments or pipe and hole section
    """

    SERIALIZED_VARIABLES = {
        "top_depth": float,
        "bottom_depth": float,
        "length": float,
        "inner_diameter_hole": float,
        "outer_diameter_pipe": float,
        "outer_diameter_tooljoint": float,
        "tool_joint_length_ratio": float,
        "hole_type": HoleType,
    }

    def __init__(self, **kwargs):
        super(Ann, self).__init__(**kwargs)

        for key in [
            "inner_diameter_hole",
            "outer_diameter_pipe",
            "outer_diameter_tooljoint",
            "tool_joint_length_ratio",
            "hole_type",
        ]:
            setattr(self, key, kwargs.get(key))

    def set_properties_from_pipe_section(self, pipe: Pipe):
        self.outer_diameter_pipe = pipe.outer_diameter
        self.outer_diameter_tooljoint = pipe.outer_diameter_tooljoint
        self.tool_joint_length_ratio = pipe.tool_joint_length_ratio

    def set_properties_from_hole(self, hole_section: HoleSection):
        self.inner_diameter_hole = hole_section.inner_diameter
        self.hole_type = hole_section.hole_type

    def compute_get_area_pipe_body(self) -> float:
        """
        Compute the annulus flow area consisting of the hole section and pipe body
        :return: area in INCH^2
        """
        return np.pi / 4 * (self.inner_diameter_hole**2 - self.outer_diameter_pipe**2)

    def compute_get_area_pipe_tooljoint(self) -> float:
        """
        Compute the annulus flow area consisting of the hole section and pipe tooljoint
        :return: area in INCH^2
        """
        return np.pi / 4 * (self.inner_diameter_hole**2 - self.outer_diameter_tooljoint**2)

    # override
    def compute_get_area(self) -> float:
        """
        Compute the total area of the hole section and return the result
        :return: cross sectional area of the hole section in INCH^2
        """
        area = self.compute_get_area_pipe_body()
        r = self.tool_joint_length_ratio
        if r > 0:
            area = r * self.compute_get_area_pipe_tooljoint() + (1 - r) * area
        return area

    # override
    def compute_get_volume(self):
        """
        This method computes and returns the total volume of the annulus section
        :return: volume in FOOT^3
        """
        area = self.compute_get_area()  # in INCH^2
        volume = area / 144 * self.length  # in FOOT^3
        return volume

    def eq_without_length(self, other):
        if not isinstance(other, Ann):
            return False

        if self.inner_diameter_hole != other.inner_diameter_hole:
            return False
        if self.outer_diameter_pipe != other.outer_diameter_pipe:
            return False
        if self.hole_type != other.hole_type:
            return False

        return True

    def __repr__(self):
        return (
            f"{nanround(self.inner_diameter_hole, 2):>6} in / {nanround(self.outer_diameter_pipe, 2):>6} in, "
            f"{super().__repr__()}"
        )
