from copy import deepcopy

from worker.data.serialization import serialization
from worker.wellbore.model.hole_section import HoleSection


@serialization
class Riser(HoleSection):
    SERIALIZED_VARIABLES = deepcopy(HoleSection.SERIALIZED_VARIABLES)
    SERIALIZED_VARIABLES.update({"external_flow_source_depth": float})

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.external_flow_source_depth = None

    def get_external_flow_source_depth(self):
        # If an external_flow_source_depth is not set, it is defaulted to the Riser bottom depth
        # This is only used for hydraulics, which will be implemented later.
        if self.external_flow_source_depth is None:
            self.external_flow_source_depth = self.bottom_depth

        return self.external_flow_source_depth
