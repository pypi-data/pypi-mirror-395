import numpy as np

from worker.data.operations import equal, nanround
from worker.data.serialization import serialization
from worker.wellbore.model.element import Element
from worker.wellbore.model.enums import HoleType


@serialization
class HoleSection(Element):
    SERIALIZED_VARIABLES = {
        "top_depth": float,
        "bottom_depth": float,
        "length": float,
        "inner_diameter": float,
        "hole_type": HoleType,
    }

    def __init__(self, **kwargs):
        super(HoleSection, self).__init__(**kwargs)
        self.inner_diameter = kwargs["inner_diameter"]
        self.hole_type = kwargs.get("hole_type")

    def __eq__(self, other):
        params = ["inner_diameter", "length", "hole_type"]
        return equal(self, other, params)

    def eq_without_length(self, other):
        params = ["inner_diameter", "hole_type"]
        return equal(self, other, params)

    # override
    def compute_get_area(self) -> float:
        """
        Compute the total area of the hole section and return the result
        :return: cross sectional area of the hole section in INCH^2
        """
        return np.pi / 4 * self.inner_diameter**2

    # override
    def compute_get_volume(self) -> float:
        """
        Compute the volume of the hole section
        :return: volume of the hole section in FOOT^3
        """
        volume = self.compute_get_area() * self.length  # in INCH^2 * FOOT
        volume /= 144  # in FOOT^3
        return volume

    def __repr__(self):
        return f"{nanround(self.inner_diameter, 2):>6} in, " f"{super().__repr__()}, " f"{self.hole_type.value}"
