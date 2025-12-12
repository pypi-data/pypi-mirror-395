from enum import Enum

from worker.data.serialization import serialization


class PipeMovementStatus(Enum):
    UNCLASSIFIED = -1
    IN_SLIPS = 0
    STATIC = 1
    ON_BOTTOM = 2
    PULL_OUT_OF_HOLE = 3
    RUN_IN_HOLE = 4
    DRILLING = 5

    def is_moving_out(self) -> bool:
        move_actions = [
            PipeMovementStatus.PULL_OUT_OF_HOLE,
        ]
        return self in move_actions

    def is_moving_in(self) -> bool:
        move_actions = [PipeMovementStatus.RUN_IN_HOLE, PipeMovementStatus.DRILLING]
        return self in move_actions

    def is_moving(self) -> bool:
        return self.is_moving_in() or self.is_moving_out()


class PumpStatus(Enum):
    OFF = 0
    ON = 1


class RotationStatus(Enum):
    OFF = 0
    ON = 1


@serialization
class Activity(bytes, Enum):
    ROTARY_DRILLING = ("Rotary Drilling", PipeMovementStatus.DRILLING, PumpStatus.ON, RotationStatus.ON)
    SLIDE_DRILLING = ("Slide Drilling", PipeMovementStatus.DRILLING, PumpStatus.ON, RotationStatus.OFF)

    RUN_IN_HOLE = ("Run in Hole", PipeMovementStatus.RUN_IN_HOLE, PumpStatus.OFF, RotationStatus.OFF)
    WASHING_DOWN = ("Washing Down", PipeMovementStatus.RUN_IN_HOLE, PumpStatus.ON, RotationStatus.OFF)
    DRY_REAMING_DOWN = ("Dry Reaming Down", PipeMovementStatus.RUN_IN_HOLE, PumpStatus.OFF, RotationStatus.ON)
    REAMING_DOWN = ("Reaming Down", PipeMovementStatus.RUN_IN_HOLE, PumpStatus.ON, RotationStatus.ON)

    PULL_OUT_OF_HOLE = ("Pull out of Hole", PipeMovementStatus.PULL_OUT_OF_HOLE, PumpStatus.OFF, RotationStatus.OFF)
    WASHING_UP = ("Washing Up", PipeMovementStatus.PULL_OUT_OF_HOLE, PumpStatus.ON, RotationStatus.OFF)
    DRY_REAMING_UP = ("Dry Reaming Up", PipeMovementStatus.PULL_OUT_OF_HOLE, PumpStatus.OFF, RotationStatus.ON)
    REAMING_UP = ("Reaming Up", PipeMovementStatus.PULL_OUT_OF_HOLE, PumpStatus.ON, RotationStatus.ON)

    STATIC_OFF_BOTTOM = ("Static Off Bottom", PipeMovementStatus.STATIC, PumpStatus.OFF, RotationStatus.OFF)
    CIRCULATING = ("Circulating", PipeMovementStatus.STATIC, PumpStatus.ON, RotationStatus.OFF)
    DRY_ROTARY_OFF_BOTTOM = ("Dry Rotary Off Bottom", PipeMovementStatus.STATIC, PumpStatus.OFF, RotationStatus.ON)
    ROTARY_OFF_BOTTOM = ("Rotary Off Bottom", PipeMovementStatus.STATIC, PumpStatus.ON, RotationStatus.ON)

    STATIC_ON_BOTTOM = ("Static On Bottom", PipeMovementStatus.ON_BOTTOM, PumpStatus.OFF, RotationStatus.OFF)
    CIRCULATING_ON_BOTTOM = ("Circulating On Bottom", PipeMovementStatus.ON_BOTTOM, PumpStatus.ON, RotationStatus.OFF)
    DRY_ROTARY_ON_BOTTOM = ("Dry Rotary On Bottom", PipeMovementStatus.ON_BOTTOM, PumpStatus.OFF, RotationStatus.ON)
    CIRCULATING_AND_ROTARY_ON_BOTTOM = (
        "Circ. & Rot. On Bottom",
        PipeMovementStatus.ON_BOTTOM,
        PumpStatus.ON,
        RotationStatus.ON,
    )

    IN_SLIPS = ("In Slips", PipeMovementStatus.IN_SLIPS, PumpStatus.OFF, RotationStatus.OFF)

    UNCLASSIFIED = ("Unclassified", PipeMovementStatus.DRILLING, PumpStatus.OFF, RotationStatus.OFF)

    def __new__(cls, activity_name: str, pipe_movement_status, pump_status, rotation_status):
        obj = bytes.__new__(cls)

        obj._value_ = activity_name  # using the activity name as the main value
        obj.pipe_movement_status = pipe_movement_status
        obj.pump_status = pump_status
        obj.rotation_status = rotation_status

        return obj

    def is_pipe_moving(self) -> bool:
        return self.pipe_movement_status.is_moving()

    def is_pipe_moving_out(self) -> bool:
        return self.pipe_movement_status.is_moving_out()

    def is_pipe_moving_in(self) -> bool:
        return self.pipe_movement_status.is_moving_in()

    def is_pumping(self) -> bool:
        return self.pump_status == PumpStatus.ON

    def is_rotating(self) -> bool:
        return self.rotation_status == RotationStatus.ON

    def is_drilling(self) -> bool:
        return self.pipe_movement_status == PipeMovementStatus.DRILLING

    def is_reaming(self) -> bool:
        """
        Pipe moves up and down with rotation
        :return:
        """
        movement_status = self.pipe_movement_status in [
            PipeMovementStatus.PULL_OUT_OF_HOLE,
            PipeMovementStatus.RUN_IN_HOLE,
        ]
        rotation_status = self.rotation_status == RotationStatus.ON
        return movement_status and rotation_status

    def is_tripping(self) -> bool:
        """
        Pipe moves up and down
        :return:
        """
        if self == self.RUN_IN_HOLE or self == self.PULL_OUT_OF_HOLE:
            return True
        return False

    def __eq__(self, other):
        return self is other

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return self.value
