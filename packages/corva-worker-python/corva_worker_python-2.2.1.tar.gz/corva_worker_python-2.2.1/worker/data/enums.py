from enum import Enum, auto
from typing import List


class LambdaStates(Enum):
    """
    An enumeration of possible states for a Lambda function.

    Attributes:
        TIMED_OUT (str): The Lambda function timed out.
        SUCCEEDED (str): The Lambda function completed successfully.
        FAILED (str): The Lambda function failed to complete.
    """

    TIMED_OUT = "Lambda timed out."
    SUCCEEDED = "Lambda process succeeded."
    FAILED = "Lambda process failed."


class EventType(Enum):
    """
    Enum class representing the different types of events that can be handled.
    The values of this enum are used as the keys in the event dictionary.
    For instance in the worker apps, the 'event-type' in the constants file
    should be either 'wits_stream' or 'scheduler'. For partial rerun merge
    events, the 'event_type' node is set to 'partial-well-rerun-merge'.
    """

    STREAM = "wits_stream"
    SCHEDULER = "scheduler"
    PARTIAL_RERUN = "partial-well-rerun-merge"
    TASK = "task_event"
    GENERIC = "generic_event"


class ChannelStatus(Enum):
    """
    Enum class representing the status of a channel in WITS data.
    """

    ON = "on"
    OFF = "off"
    MISSING = "missing"


class DataStatus(Enum):
    """
    Enum representing the status of data.
    """

    VALID = "valid"
    MISSING = "missing"
    OVERRIDDEN = "overridden"


class Environment(Enum):
    """
    An enumeration of the different environments.
    """

    QA = "qa"
    STAGING = "staging"
    PRODUCTION = "production"
    LOCAL = "local"


class CollectionRecordDataScope(Enum):
    """
    This enumeration is used to indicate the type of the
    collection record scope.
    """

    BHA_OR_CASING = auto()  # Active BHA or Casing
    SINCE_START = auto()  # Since the start of the well
    FORMATION = auto()  # Active Formation
    FROM_LAST_CASING = auto()  # Since the last casing
    BHA = auto()  # Active BHA
    CURRENT = auto()  # A few minutes ago to current
    SEMI_CURRENT = auto()  # A couple of hours ago to current instant

    @classmethod
    def current_modes(cls) -> List["CollectionRecordDataScope"]:
        """
        Gets the items that are considered as current mode.
        """
        return [
            cls.CURRENT,
            cls.SEMI_CURRENT,
        ]

    @classmethod
    def not_current_modes(cls) -> List["CollectionRecordDataScope"]:
        """
        Gets the items that are not considered as current mode.
        """
        return [item for item in cls.__members__.values() if item not in cls.current_modes()]


class CountOfCollectionRecord(Enum):
    """
    An enumeration representing the count of collection records.

    Attributes:
        ONE_PER_BHA_OR_CASING: Represents one record per BHA or casing.
        ONE_PER_WELL: Represents one record per well.
    """

    ONE_PER_BHA_OR_CASING = auto()
    ONE_PER_WELL = auto()


class RerunMode(Enum):
    """
    An enumeration representing the mode of rerun.

    Attributes:
        REALTIME: When the rerun asset catches up with the original asset,
            so the end time of the rerun asset is the same as the original asset
        HISTORICAL: When an old portion of the original asset runs on the
            rerun asset, so the end time of the rerun asset is not the same as
            the end time of the original asset
    """

    REALTIME = "realtime"
    HISTORICAL = "historical"


class PartialRerunStatus(Enum):
    """
    An enumeration representing the different states of a partial rerun.
    Note that in this project, only the MERGING, FAILED and COMPLETED statuses are used.
    """

    INITIALIZED = "initialized"
    RUNNING = "running"
    PENDING_MERGE = "pending_merge"
    MERGE_INITIALIZED = "merge_initialized"
    FAILED = "failed"
    STOPPED = "stopped"
    MERGING = "merging"
    COMPLETED = "completed"
