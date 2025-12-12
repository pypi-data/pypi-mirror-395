from typing import List, Optional

from worker import constants, exceptions
from worker.app.modules import Module
from worker.app.modules.time_activity_module import TimeActivityModule
from worker.data.enums import EventType, RerunMode
from worker.data.operations import gather_data_for_period
from worker.event import Event
from worker.event.scheduled import ScheduledEvent
from worker.event.stream import StreamEvent
from worker.mixins.logging import LoggingMixin
from worker.mixins.rollbar import RollbarMixin
from worker.partial_rerun_merge.models import RerunMergeCacheUpdater
from worker.state.mixins import RedisMixin
from worker.state.state import State


class App(RedisMixin, LoggingMixin, RollbarMixin):
    """
    The apps is designed to receive the events of a single asset
    """

    app_key = constants.get("global.app-key")
    app_name = constants.get("global.app-name")

    app_state_fields = {"asset_id": int, "last_processed_timestamp": int}

    def __init__(self, *args, **kwargs):
        self.module_key = None

        self.event_type: EventType = None

        self.asset_id = None
        self.event = None  # event records

        super().__init__(*args, **kwargs)

    def load(self, event_type: EventType, event: Event):
        """
        :param event_type:
        :param event: a scheduler event or wits stream; belong to one asset
        :return:
        """
        self.event_type = event_type

        self.asset_id = event.asset_id

        self.state = self.load_state()

        max_lookback_seconds = self.get_max_lookback_seconds()
        event = self.load_event(event, max_lookback_seconds)

        valid_stream_collections = self.get_valid_stream_collections()
        self.event = self.filter_event_for_collections(
            self.event_type, valid_stream_collections, event
        )  # event records

        self.log_event(self.event, max_lookback_seconds)  # event records

    def log_event(self, event: List[dict], max_lookback_seconds: int):
        self.debug(self.asset_id, "WITS input to {0} -> {1}".format(self.app_name, event))

        if not event:
            return

        batch_size = len(event)
        start_time = event[0].get("timestamp")
        end_time = event[-1].get("timestamp")

        self.log(
            self.asset_id,
            text=(
                f"Received {batch_size} elements from {start_time} to {end_time}. "
                f"{max_lookback_seconds} seconds of initial data are lookback."
            ),
        )

    @staticmethod
    def get_valid_stream_collections():
        valid_collections = constants.get("global.valid-stream-collections", [])
        if not isinstance(valid_collections, (str, list)):
            raise TypeError("Incorrect type of valid-stream-collections in global constants")

        if isinstance(valid_collections, str):
            valid_collections = [valid_collections]
        return valid_collections

    def get_max_lookback_seconds(self):
        """
        For each module (mostly in time-base modules), the time of processing does not
        match the last time of the event so extra data is required to look back and get
        the data so the processing can start from where it left off.
        :return:
        """

        time_modules = [module for module in self.get_modules() if issubclass(module, TimeActivityModule)]
        maximum_lookback = 0
        for module in time_modules:
            module_lookback = constants.get(
                "{}.{}.lookback-duration".format(self.app_key, module.module_key), default=0
            )
            maximum_lookback = max(module_lookback, maximum_lookback)

        return maximum_lookback

    def load_event(self, event: Event, max_lookback_seconds: int) -> List[dict]:
        if self.event_type == EventType.SCHEDULER:
            return self.load_scheduler_event(self.asset_id, event, max_lookback_seconds)

        if self.event_type == EventType.STREAM:
            return self.load_wits_stream_event(self.asset_id, event, max_lookback_seconds)

        return None

    @staticmethod
    def filter_event_for_collections(event_type: EventType, valid_stream_collections: list, event: list) -> list:
        """
        This function filters the incoming event based on a list of valid collections

        :param event_type: Type of incoming event.
        :param valid_stream_collections: List of valid collections
        :param event: List of data records
        :return: List of records whose collection is one of the allowed event collections
        """

        # If event type is scheduler or event_collections is empty, return the entire event
        if event_type == EventType.SCHEDULER or not valid_stream_collections:
            return event

        # Filtering the event based on valid collections
        event = [record for record in event if record.get("collection") in valid_stream_collections]
        return event

    def filter_event_for_duplicates(self, event) -> list:
        last_processed_timestamp = self.state.get("last_processed_timestamp") or 0

        # If event is a single record and greater than the last processed timestamp, return the event
        if len(event) == 1 and event[0].get("timestamp") > last_processed_timestamp:
            return event

        # If length of unique timestamps is same as length of event and the first record timestamp is also greater than
        # last_processed_timestamp, then return the event
        unique_timestamps = set([record.get("timestamp") for record in event])
        if len(unique_timestamps) == len(event) and event[0].get("timestamp") > last_processed_timestamp:
            return event

        # Filtering the events for duplicates, once we identify that duplicates exist.
        filtered_events = []
        for each_record in event:
            if each_record.get("timestamp") > last_processed_timestamp:
                filtered_events.append(each_record)
                last_processed_timestamp = each_record.get("timestamp")

        return filtered_events

    def load_scheduler_event(self, asset_id: int, event: ScheduledEvent, max_lookback_seconds: int) -> List[dict]:
        """
        To load a scheduler event and get the wits stream data
        :param asset_id: The asset to load
        :param event: A cleaned event
        :param max_lookback_seconds: Maximum amount of time to look back prior to the scheduler event to cover gaps
        :return: list of WITS data between the last processed timestamp and the final event item timestamp
        """

        start_timestamp = self.state.get("last_processed_timestamp", event[0].start_time - 1)
        end_timestamp = event[-1].start_time

        # the event is converted from scheduler to wits stream
        scheduler_event = gather_data_for_period(
            asset_id=asset_id,
            start=start_timestamp - max_lookback_seconds,
            end=end_timestamp,
            limit=constants.get("global.query-limit"),
            fields=constants.get("global.wits_query_fields", None),
        )

        return scheduler_event

    def load_wits_stream_event(self, asset_id: int, event: StreamEvent, max_lookback_seconds: int) -> List[dict]:
        """
        To load a wits stream event and get more data if necessary
        :param asset_id: The asset to load
        :param event: A cleaned event
        :param max_lookback_seconds: Maximum amount of time to look back prior to WITS data to cover gaps
        :return: list of WITS data between the first event timestamp and the first timestamp
        """
        records = event.records

        # First filtering original event for duplicates
        records = self.filter_event_for_duplicates(records)

        # If all record timestamps are before the last processed timestamp,
        # the first timestamp will be the last processed timestamp from cache
        if not records:
            first_timestamp = self.state.get("last_processed_timestamp") or 0
        else:
            first_timestamp = records[0].get("timestamp")

        if not first_timestamp:
            return records

        if max_lookback_seconds:
            # Subtract one from the timestamp so that we don't reselect the final data item that was sent in the event
            end_timestamp = first_timestamp - 1

            previous_events = gather_data_for_period(
                asset_id=asset_id,
                start=first_timestamp - max_lookback_seconds,
                end=end_timestamp,
                limit=constants.get("global.query-limit"),
                fields=constants.get("global.wits_query_fields", None),
            )

            records = previous_events + records

        return records

    @staticmethod
    def determine_asset_id(event: list) -> int:
        try:
            return int(event[0]["asset_id"])
        except Exception:
            raise Exception(f"Event does not contain asset_id: {event}")

    def load_state(self, state_key: Optional[str] = None, raise_warnings: bool = False) -> dict:
        previous_state = super().load_state(state_key=state_key, raise_warnings=raise_warnings)

        state = State(self.app_state_fields, previous_state)

        if not state.get("asset_id", None):
            state["asset_id"] = self.asset_id

        return state

    def get_modules(self) -> List[Module]:
        raise NotImplementedError("No modules found")

    def get_active_modules(self) -> List[Module]:
        return [module for module in self.get_modules() if module.enabled]

    def run_modules(self):
        if not self.event:  # event records
            return

        for module_type in self.get_active_modules():
            try:
                module = module_type(self.state, rollbar=self.rollbar)
            except Exception:
                raise exceptions.Misconfigured(
                    "Module {0} not able to initialize for asset_id {1}".format(module_type, self.asset_id)
                )

            try:
                module.run(self.event)  # event records
            except Exception as ex:
                message = f"Error in module {module_type.module_key}"
                ex.args += (message,)  # Adding message to existing Exception
                raise

        last_processed_timestamp = self.event[-1].get("timestamp")  # event records
        self.state["last_processed_timestamp"] = last_processed_timestamp

    @classmethod
    def update_cache(cls, merger: "PartialRerunMerge") -> None:
        """
        This function updates the cache of the original asset with the rerun asset's cache

        If in any app that is extending this class, it needs to be overridden, it can be done so.

        :param merger: PartialRerunMerge object
        :return: None
        """
        if merger.rerun_mode == RerunMode.HISTORICAL:
            return

        original_asset_id = merger.original_asset_id
        rerun_asset_id = merger.rerun_asset_id

        redis_handler = RedisMixin()
        redis_handler.asset_id = original_asset_id

        original_state_key = redis_handler.get_formatted_state_key(original_asset_id, cls.app_key)
        rerun_state_key = redis_handler.get_formatted_state_key(rerun_asset_id, cls.app_key)

        original_state = redis_handler.load_state(original_state_key)
        rerun_state = redis_handler.load_state(rerun_state_key)

        original_state = RerunMergeCacheUpdater.default_updater(original_state, rerun_state)

        redis_handler.state = original_state
        redis_handler.save_state(original_state_key)
