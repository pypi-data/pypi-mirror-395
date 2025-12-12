import time
from copy import deepcopy
from enum import Enum

import numpy as np

from worker.data.alert import Alerter
from worker.data.operations import equal, is_stream_app, nanround
from worker.data.serialization import serialization
from worker.data.unit_conversions import US_LIQUID_GAL_to_INCH3
from worker.mixins.logging import Logger
from worker.wellbore.model.element import Element
from worker.wellbore.model.enums import HoleType, PipeMaterial, PipeType


@serialization
class Pipe(Element):
    SERIALIZED_VARIABLES = {
        "top_depth": float,
        "bottom_depth": float,
        "length": float,
        "inner_diameter": float,
        "outer_diameter": float,
        "joint_length": float,
        "max_outer_diameter": float,
        "inner_diameter_tooljoint": float,
        "outer_diameter_tooljoint": float,
        "tool_joint_length_per_joint": float,
        "linear_mass_in_air": float,
        "order": float,
        "pipe_material": PipeMaterial,
        "grade": float,
        "tool_joint_length_ratio": float,
        "pipe_type": PipeType,
    }

    """
    The pipe object can be used for the following components directly:
    - drill pipe (DP)
    - drill collar (DC)
    - heavy weight drill pipe (HWDP)
    - subs
    - stabilizers

    This class is extended by the other drillpipe components.
    """

    def __init__(self, **kwargs):
        super(Pipe, self).__init__(**kwargs)

        self.inner_diameter = kwargs["inner_diameter"]
        self.outer_diameter = kwargs["outer_diameter"]

        self.joint_length = kwargs.get("component_length", kwargs.get("joint_length"))
        self.max_outer_diameter = kwargs.get("max_outer_diameter")
        self.inner_diameter_tooljoint = kwargs.get("inner_diameter_tooljoint")
        self.outer_diameter_tooljoint = kwargs.get("outer_diameter_tooljoint")
        self.tool_joint_length_per_joint = kwargs.get("length_tooljoint") or kwargs.get("tool_joint_length_per_joint")
        self.linear_mass_in_air = kwargs.get("linear_weight", kwargs.get("linear_mass_in_air"))
        self.order = kwargs.get("order")

        self.pipe_material = kwargs.get("material")
        self.grade = kwargs.get("grade")

        self.set_tool_joint_length_ratio()

        family = kwargs.get("family") or ""
        self.pipe_type = PipeType.determine_type(family)

    def get_max_outer_diameter(self):
        return self.max_outer_diameter or self.outer_diameter_tooljoint or self.outer_diameter

    def set_tool_joint_length_ratio(self):
        if self.tool_joint_length_per_joint is None or not self.joint_length:
            self.tool_joint_length_ratio = 0
        else:
            self.tool_joint_length_ratio = self.tool_joint_length_per_joint / self.joint_length

    def is_valid_tool_joint(self):
        """
        If there is a valid tool joint or not
        :return:
        """
        if self.outer_diameter_tooljoint is None:
            return False
        if self.inner_diameter_tooljoint is None:
            return False
        if not self.tool_joint_length_ratio:
            return False

        return True

    def get_pipe_id_area(self):
        """
        Compute the total inner area of the pipe body
        :return: inner area of the pipe body in INCH^2
        """
        return np.pi / 4 * (self.inner_diameter**2)

    def get_pipe_od_area(self):
        """
        Compute the total outer area of the pipe body
        :return: outer area of the pipe body in INCH^2
        """
        return np.pi / 4 * (self.outer_diameter**2)

    def get_pipe_tool_joint(self):
        """
        Create a pipe with its id and od equal to the tool joint values (if available)
        :return:
        """
        p = deepcopy(self)
        p.inner_diameter = p.inner_diameter_tooljoint or p.inner_diameter
        p.outer_diameter = p.outer_diameter_tooljoint or p.outer_diameter
        return p

    def compute_inner_area_tool_joint_adjusted(self):
        """
        Compute the inner area of the pipe adjusted for the tool joint
        :return: the area in INCH^2
        """
        area_body = self.get_pipe_id_area()  # in INCH^2
        if not self.is_valid_tool_joint():
            return area_body

        area_tj = np.pi / 4 * (self.inner_diameter_tooljoint**2)  # in INCH^2
        return area_body * (1 - self.tool_joint_length_ratio) + area_tj * self.tool_joint_length_ratio

    def compute_outer_area_tool_joint_adjusted(self):
        """
        Compute the outer area of the pipe adjusted for the tool joint
        :return: the area in INCH^2
        """
        area_body = self.get_pipe_od_area()  # in INCH^2
        if not self.is_valid_tool_joint():
            return area_body

        area_tj = np.pi / 4 * (self.outer_diameter_tooljoint**2)  # in INCH^2
        r = self.tool_joint_length_ratio
        return area_body * (1 - r) + area_tj * r

    def compute_inner_diameter_tool_joint_adjusted(self):
        """
        Compute the inner diameter of the pipe adjusting for the tool joint
        :return: the adjusted inner diameter of the pipe in INCH
        """
        di_body = self.inner_diameter
        if not self.is_valid_tool_joint():
            return di_body

        di_tj = self.inner_diameter_tooljoint
        r = self.tool_joint_length_ratio
        return di_body * (1 - r) + di_tj * r

    def compute_outer_diameter_tool_joint_adjusted(self):
        """
        Compute the outer diameter of the pipe adjusting for the tool joint
        :return: the adjusted outer diameter of the pipe in INCH
        """
        do_body = self.outer_diameter
        if not self.is_valid_tool_joint():
            return do_body

        do_tj = self.outer_diameter_tooljoint
        r = self.tool_joint_length_ratio
        return do_body * (1 - r) + do_tj * r

    def compute_body_cross_sectional_area_tj_adjusted(self):
        """
        Compute body cross sectional area adjusted for the tool joint
        :return: area in INCH^2
        """
        return self.compute_outer_area_tool_joint_adjusted() - self.compute_inner_area_tool_joint_adjusted()

    # override
    def compute_get_area(self):
        return self.compute_inner_area_tool_joint_adjusted()

    def compute_body_volume_tj_adjusted(self):
        """
        Compute body volume adjusted for the tool joint
        :return: volume in FOOT^3
        """
        return self.compute_body_cross_sectional_area_tj_adjusted() / 144 * self.length

    def compute_outer_volume_tj_adjusted(self):
        """
        Compute outer volume adjusted for the tool joint
        :return: volume in FOOT^3
        """
        return self.compute_outer_area_tool_joint_adjusted() / 144 * self.length

    def compute_inner_volume_tj_adjusted(self):
        """
        Compute inner volume adjusted for the tool joint
        :return: volume in FOOT^3
        """
        return self.compute_inner_area_tool_joint_adjusted() / 144 * self.length

    # override
    def compute_get_volume(self):
        return self.compute_inner_volume_tj_adjusted()

    def calculate_linear_mass(self):
        """
        Compute the pipe linear mass in air from pipe materials
        :return: pipe linear mass in LB/FOOT
        """
        density = self.pipe_material.get_density()  # PPG
        pipe_body_area = self.get_pipe_body_area()  # INCH^2
        linear_mass = density * pipe_body_area * (US_LIQUID_GAL_to_INCH3 * 12)  # lb/ft
        return linear_mass

    def __eq__(self, other):
        if not isinstance(other, (Pipe, Bit)):
            return False

        if self.eq_without_length(other) is False:
            return False

        return self.length == other.length

    def eq_without_length(self, other):
        params = [
            "pipe_type",
            "inner_diameter",
            "outer_diameter",
            "inner_diameter_tooljoint",
            "outer_diameter_tooljoint",
            "linear_mass_in_air",
        ]
        return equal(self, other, params)

    def eq_id_and_od(self, other):
        params = ["inner_diameter", "outer_diameter"]
        return equal(self, other, params)

    def __repr__(self):
        return (
            f"{self.pipe_type.name:13}"
            f"{nanround(self.inner_diameter, 2):>6} in / "
            f"{nanround(self.outer_diameter, 2):>6} in, "
            f"{nanround(self.linear_mass_in_air, 2):>6} lb/ft, "
            f"{super().__repr__()}"
        )


@serialization
class MWD(Pipe):
    # TODO extra items to be implemented later
    pass


@serialization
class PDM(Pipe):
    # TODO extra items to be implemented later
    pass


@serialization
class RSS(Pipe):
    # TODO extra items to be implemented later
    pass


@serialization
class Agitator(Pipe):
    pass


@serialization
class Bit(Element):
    SERIALIZED_VARIABLES = {
        "top_depth": float,
        "bottom_depth": float,
        "length": float,
        "size": float,
        "tfa": float,
        "pipe_type": PipeType,
    }

    # TODO extra items to be implemented later
    def __init__(self, **kwargs):
        super(Bit, self).__init__(**kwargs)

        self.size = float(kwargs["size"])
        self.tfa = float(kwargs["tfa"])
        self.pipe_type = PipeType.BIT

    # override
    def compute_get_area(self):
        return 0

    # override
    def compute_get_volume(self):
        return 0

    def __repr__(self):
        return (
            f"{self.pipe_type.name:13}"
            f"{nanround(self.size, 2)} in - "
            f"tfa={nanround(self.tfa, 2)} in^2, "
            f"{super().__repr__()}"
        )


@serialization
class UnderReamer(Pipe):
    SERIALIZED_VARIABLES = deepcopy(Pipe.SERIALIZED_VARIABLES)
    SERIALIZED_VARIABLES.update(
        {
            "activation_logic": str,
            "ur_opened_od": float,
            "ur_opened_depth": float,
            "flow_rate": float,
            "_is_opened": bool,
            "tfa": float,
            "alerted_at_timestamp": float,
        }
    )

    class UnderReamerActivationType(Enum):
        ALREADY_ACTIVATED = "already_activated"
        MUD_FLOW_RATE = "flowrate_activated"
        OPEN_HOLE = "open_hole_activated"
        UNACTIVATED = "did_not_activate"

    @serialization
    class ActivationLogic(Enum):
        OPEN_HOLE_ACTIVATED = "open_hole_activated"
        FLOW_ACTIVATED = "flow_activated"
        DEPTH_ACTIVATION = "depth_activation"

    def __init__(self, **kwargs):
        super(UnderReamer, self).__init__(**kwargs)

        self._is_opened: bool = False
        self.alerted_at_timestamp: float = 0.0
        self.ALERT_BACKOFF_TIME = 3600

        self.tfa = float(kwargs["tfa"])
        self.ur_opened_depth = kwargs.get("ur_opened_depth")
        self.ur_opened_od = float(kwargs["ur_opened_od"])
        self.flow_rate = float(kwargs.get("flow_rate"))
        self.activation_logic = self.ActivationLogic(kwargs["activation_logic"])
        self.pipe_type = PipeType.UNDERREAMER

    @property
    def discharge_coefficient(self) -> float:
        return 0.95

    @property
    def is_opened(self) -> bool:
        """
        This property is needed for enabling split flow
        :return:
        """
        return self._is_opened and self.tfa > 0.0

    def set_opened(self, opened: bool):
        self._is_opened = opened

    def get_activation_type(self, mud_flow_rate: float):
        opened_depth = self.ur_opened_depth or 10_000_000.0

        # if it was activated before no need to check how it was activated just use `ur_opened_depth` key
        if self.top_depth >= opened_depth:
            return self.UnderReamerActivationType.ALREADY_ACTIVATED

        # if it was never activated and logic is open hole
        if self.activation_logic == self.ActivationLogic.OPEN_HOLE_ACTIVATED and not self.ur_opened_depth:
            return self.UnderReamerActivationType.OPEN_HOLE

        # if it was never activated and logic is flow activated
        if mud_flow_rate > self.flow_rate and not self.ur_opened_depth:
            return self.UnderReamerActivationType.MUD_FLOW_RATE

        # Otherwise unactivated
        return self.UnderReamerActivationType.UNACTIVATED

    def activate_under_reamer(self, mud_flow_rate, start_reaming_depth, hole_type: HoleType):
        activation_mode = self.get_activation_type(mud_flow_rate)

        if activation_mode == self.UnderReamerActivationType.UNACTIVATED:
            self.ur_opened_depth = None
            return activation_mode

        # If OpenHole activated then set the opened depth to lastCasingDepth
        if activation_mode == self.UnderReamerActivationType.OPEN_HOLE:
            if start_reaming_depth is None:
                Logger.warn("Unable to find the last casing depth")
                self.ur_opened_depth = None
                return self.UnderReamerActivationType.UNACTIVATED

            # No need to raise Alert here
            if start_reaming_depth >= self.top_depth:
                self.ur_opened_depth = None
                return self.UnderReamerActivationType.UNACTIVATED

            self.ur_opened_depth = start_reaming_depth
            return activation_mode

        # If mud activated then set the opened depth as top depth of UR
        if self.ur_opened_depth is None:
            self.ur_opened_depth = self.top_depth

        # Check if under-reamer was opened in cased hole
        if self.ur_opened_depth <= start_reaming_depth and hole_type == HoleType.CASED_HOLE:
            self.trigger_alert(self.ur_opened_depth, start_reaming_depth)
            self.ur_opened_depth = None
            return self.UnderReamerActivationType.UNACTIVATED

        return activation_mode

    def trigger_alert(self, ur_opened_depth, start_reaming_depth):
        identifier = "ur_opened_in_cased_hole"
        message = (
            f"Attempted to open under-reamer inside cased hole at {ur_opened_depth}. "
            f"Last casing shoe depth of {start_reaming_depth}. "
        )

        current_timestamp = time.time()

        if (current_timestamp > self.alerted_at_timestamp + self.ALERT_BACKOFF_TIME) and is_stream_app():
            Alerter.trigger_alert(identifier, message)
            self.alerted_at_timestamp = current_timestamp
            Logger.warn(f"Alert created. identifier: {identifier}, message: {message}")
        else:
            Logger.info(
                f"Alert created. identifier: {identifier}, message: {message}"
                f"However, not triggering alert because it was not triggered from Stream app"
            )

    def __repr__(self):
        return (
            f"{super().__repr__()}"
            f"opened_od={nanround(self.ur_opened_od, 2)} in - "
            f"tfa={nanround(self.tfa, 2)} in^2, "
        )
