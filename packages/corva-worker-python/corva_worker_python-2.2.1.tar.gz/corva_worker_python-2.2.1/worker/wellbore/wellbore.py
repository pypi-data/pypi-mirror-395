from copy import deepcopy
from typing import Union

import simplejson as json

from worker import API
from worker.data.json_encoder import JsonEncoder
from worker.data.operations import get_config_by_id, get_data_by_path, is_stream_app, nanround
from worker.data.serialization import serialization
from worker.mixins.logging import Logger
from worker.wellbore.model.annulus import Annulus
from worker.wellbore.model.drillstring import Drillstring
from worker.wellbore.model.drillstring_components import UnderReamer
from worker.wellbore.model.enums import HoleType
from worker.wellbore.model.hole import Hole
from worker.wellbore.model.hole_section import HoleSection


@serialization
class Wellbore:
    DEPTH_THRESHOLD = 50  # ft

    SERIALIZED_VARIABLES = {
        "original_drillstring": Drillstring,
        "original_hole": Hole,
        "bit_depth": float,
        "hole_depth": float,
        "last_hole_depth": float,
        "last_non_decreasing_hole_depth": float,
        "under_reamer_alert_timestamp": float,
    }

    def __init__(self, **kwargs):
        super().__init__()

        self.under_reamer: Union[UnderReamer, None] = None
        self.under_reamer_alert_timestamp: float = 0.0

        self.original_drillstring: Drillstring = kwargs.get("original_drillstring") or kwargs.get("drillstring")
        self.actual_drillstring: Drillstring = kwargs.get("actual_drillstring")

        # Explicitly checking if original_hole is not None, because bool of Hole with no sections evaluates to False
        self.original_hole: Hole = (
            kwargs.get("original_hole") if kwargs.get("original_hole") is not None else kwargs.get("hole")
        )
        self.actual_hole: Hole = kwargs.get("actual_hole")

        self.actual_annulus: Annulus = kwargs.get("actual_annulus")

        self.bit_depth: float = kwargs.get("bit_depth") or 0.0
        self.hole_depth: float = kwargs.get("hole_depth")

        self.last_hole_depth: float = kwargs.get("last_hole_depth") or self.hole_depth
        self.last_non_decreasing_hole_depth: float = (
            kwargs.get("last_non_decreasing_hole_depth") or self.last_hole_depth
        )

        mud_flow_in = kwargs.get("mud_flow_in") or 0.0

        self.update(mud_flow_in=mud_flow_in)

    @property
    def annulus(self):
        return self.actual_annulus

    def update(self, bit_depth: Union[float, dict] = None, hole_depth: float = None, mud_flow_in: float = None) -> None:
        """
        :param bit_depth: a wits dict (that will be used for both bit and hole depths) or actual bit depth
        :param hole_depth: actual hole depth value
        :param mud_flow_in: mud flow rate to check under-reamer activation condition
        :return:
        """
        if mud_flow_in is None:
            mud_flow_in = 0.0

        if self.original_drillstring is None:
            return

        if isinstance(bit_depth, dict):
            bit_depth = get_data_by_path(bit_depth, "data.bit_depth", float)
            hole_depth = get_data_by_path(bit_depth, "data.hole_depth", float)

        self.bit_depth = bit_depth or self.bit_depth or 0.0

        # a qc for the hole depth: if bit depth > hole depth override it with bit depth
        if hole_depth is None:
            hole_depth = self.hole_depth or self.original_hole.get_bottom_depth()

        hole_depth = max(hole_depth, self.bit_depth)
        self.hole_depth = hole_depth

        self.actual_drillstring = deepcopy(self.original_drillstring)
        self.actual_drillstring.update(self.bit_depth)

        self.last_non_decreasing_hole_depth = max(self.last_non_decreasing_hole_depth, self.hole_depth)

        self.actual_hole = deepcopy(self.original_hole)
        self.actual_hole.update(self.hole_depth)

        under_reamer: UnderReamer = self.actual_drillstring.get_under_reamer()
        if under_reamer:
            self.under_reamer = under_reamer
            self.under_reamer.alerted_at_timestamp = self.under_reamer_alert_timestamp
            self.add_under_reamer_sections(mud_flow_in)
            self.under_reamer_alert_timestamp = self.under_reamer.alerted_at_timestamp
            self.actual_hole.update(self.hole_depth)

        self.actual_annulus = Annulus(drillstring=self.actual_drillstring, hole=self.actual_hole)

        self.last_hole_depth = self.hole_depth

    def add_under_reamer_sections(self, mud_flow_rate):
        current_hole: HoleSection = self.actual_hole.find_section_at_measured_depth(
            self.under_reamer.top_depth + 0.0001
        )

        # Determine a valid start of reaming depth: either casing shoe or open hole top depth.
        if current_hole.hole_type == HoleType.CASED_HOLE:
            start_reaming_depth = current_hole.bottom_depth
        elif current_hole.inner_diameter < self.under_reamer.ur_opened_od:
            start_reaming_depth = current_hole.top_depth
        else:
            return

        activation_mode = self.under_reamer.activate_under_reamer(
            mud_flow_rate, start_reaming_depth, current_hole.hole_type
        )

        # If unactivated, do nothing
        if activation_mode == self.under_reamer.UnderReamerActivationType.UNACTIVATED:
            return

        # Activated for the first time
        if (
            activation_mode == self.under_reamer.UnderReamerActivationType.MUD_FLOW_RATE
            or activation_mode == self.under_reamer.UnderReamerActivationType.OPEN_HOLE
        ):
            drillstring = self.get_and_update_drill_string()

            # Update the original drillstring to match the chopped drillstring under-reamer component
            self.original_drillstring = Drillstring(drillstring)

            # Update API only if running a stream app
            if is_stream_app():
                drillstring = self.update_drillstring_api(drillstring)
                # If api request failed do not enlarge
                if not drillstring:
                    return

                Logger.debug(f"Updated API with under-reamer activation at depth {self.under_reamer.ur_opened_depth}")
            else:
                Logger.info(
                    f"Under-reamer was opened at {self.under_reamer.ur_opened_depth}. "
                    f"However, not updating the ur_opened_depth on drillstring on api "
                    f"because it was not triggered from Stream app"
                )

        reamed_length = self.under_reamer.bottom_depth - self.under_reamer.ur_opened_depth
        # If under reamer is shallower than the opened depth do nothing
        if reamed_length <= 0:
            return

        # This property is used for enabling split flow
        self.under_reamer.set_opened(True)

        ur_opened_od = self.under_reamer.ur_opened_od
        current_hole = self.actual_hole.find_section_at_measured_depth(self.under_reamer.ur_opened_depth + 0.01)

        # ENLARGEMENT
        # Enlarge the hole from previous run
        if current_hole.inner_diameter == ur_opened_od and current_hole.top_depth == self.under_reamer.ur_opened_depth:
            current_hole.set_length(reamed_length)
            return

        # Create a new reamed hole
        bottom_hole = deepcopy(current_hole)
        current_hole.set_bottom_depth(self.under_reamer.ur_opened_depth)
        current_hole.set_length()
        bottom_hole.set_top_depth(self.under_reamer.ur_opened_depth)
        bottom_hole.set_length()

        under_reamer_hole = HoleSection(
            inner_diameter=ur_opened_od, hole_type=HoleType.OPEN_HOLE, top_depth=0.0, bottom_depth=0, length=0
        )
        under_reamer_hole.set_length(reamed_length)

        # If the current hole is zero no need to add a new enlarged section, enlarge the current hole
        if current_hole.length <= 0.0:
            current_hole.inner_diameter = ur_opened_od
            current_hole.bottom_depth = self.under_reamer.bottom_depth
            current_hole.set_length()
            self.actual_hole.insert_section_after(bottom_hole, current_hole)
            return

        # Add enlarged hole section between opened depth and current under-reamer depth
        self.actual_hole.insert_section_after(under_reamer_hole, current_hole)
        self.actual_hole.insert_section_after(bottom_hole, under_reamer_hole)
        self.actual_hole.update(self.actual_hole.get_bottom_depth())

    def update_drillstring_api(self, drillstring: dict) -> Union[dict, None]:
        try:
            path = "/v1/data/corva/data.drillstring"
            res = API().post(path=path, data=json.dumps(drillstring, cls=JsonEncoder, ignore_nan=True))
            return res.data
        except Exception as e:
            Logger.error(e)

        return

    def get_and_update_drill_string(self):
        mongo_id = self.original_drillstring.mongo_id
        drillstring = get_config_by_id(mongo_id, collection="data.drillstring")

        ur_opened_depth = self.under_reamer.ur_opened_depth

        components = drillstring.get("data", {}).get("components", [])
        # Modify stringJson and post to api
        under_reamer_component = next((component for component in components if component.get("family") == "ur"), {})
        if not under_reamer_component:
            return

        under_reamer_component["ur_opened_depth"] = ur_opened_depth

        return drillstring

    def update_casing(self, casings: Hole) -> None:
        """
        If there is any update in the casings
        :param casings:
        :return:
        """
        self.original_hole.update_casings(casings)
        self.actual_hole.update_casings(casings)
        self.update()

    def trim_after_hole_depth_reduction(self, hole_depth: float) -> None:
        self.last_non_decreasing_hole_depth = hole_depth
        self.original_hole = deepcopy(self.actual_hole)

        self.actual_hole.sections = [sec for sec in self.actual_hole.sections if sec.top_depth <= hole_depth]
        if self.actual_hole:
            self.actual_hole[-1].bottom_depth = hole_depth
            self.actual_hole[-1].set_length()

        self.update(hole_depth, hole_depth)

    def compute_get_drillstring_body_volume_change(self, from_bit_depth: float, to_bit_depth: float) -> float:
        """
        Compute the change in the drillstring body volume between two bit depths
        :param from_bit_depth: start bit depth
        :param to_bit_depth: end bit depth
        :return: volume in FOOT^3
        """
        ds_from = deepcopy(self.original_drillstring)
        ds_from.update(from_bit_depth)
        body_volume_from = ds_from.compute_get_body_volume()

        ds_to = deepcopy(self.original_drillstring)
        ds_to.update(to_bit_depth)
        body_volume_to = ds_to.compute_get_body_volume()

        return body_volume_to - body_volume_from

    def compute_get_drillstring_outside_volume_change(self, from_bit_depth: float, to_bit_depth: float) -> float:
        """
        Compute the change in the drillstring solid volume between two bit depths using OD
        :param from_bit_depth: start bit depth
        :param to_bit_depth: end bit depth
        :return: volume in FOOT^3
        """
        ds_from = deepcopy(self.original_drillstring)
        ds_from.update(from_bit_depth)
        outside_volume_from = ds_from.compute_get_outside_volume()

        ds_to = deepcopy(self.original_drillstring)
        ds_to.update(to_bit_depth)
        outside_volume_to = ds_to.compute_get_outside_volume()

        return outside_volume_to - outside_volume_from

    def __repr__(self):
        return (
            f"Wellbore:\n"
            f"===Bit Depth / Hole Depth = {nanround(self.bit_depth)} / {nanround(self.hole_depth)}\n"
            f"===Drillstring:\n{self.actual_drillstring}\n"
            f"===Hole:\n{self.actual_hole}\n"
            f"===Annulus:\n{self.actual_annulus}\n\n"
            f"===Given Drillstring:\n{self.actual_drillstring}\n"
        )
