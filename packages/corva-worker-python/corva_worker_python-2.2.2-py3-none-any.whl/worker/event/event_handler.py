import itertools
from typing import Dict, Union

from worker.app import App
from worker.data.api import API
from worker.data.enums import EventType
from worker.data.operations import get_cleaned_event_and_type
from worker.event import Event
from worker.event.scheduled import ScheduledEvent, SingleScheduledEvent
from worker.event.stream import StreamEvent
from worker.exceptions import EventFormatError
from worker.partial_rerun_merge.merge import PartialRerunMerge

api = API()


class EventHandler:
    def __init__(self, app: App, merger: PartialRerunMerge):
        self.app: App = app
        self.event_type: EventType = None
        self.event_by_asset_id: Dict[int, Event] = None
        self.merger: PartialRerunMerge = merger

    def process(self, event: Union[str, dict]):
        """
        The whole process that is performed on an event including the
        loading, handling state, running, and completing the event.

        Args:
            event (Union[str, dict]): lambda handler event
        """
        self._load(event)
        self._run()

    def _load(self, event: Union[str, dict]):
        """
        Cleaning the event and group events based on their asset ids

        Args:
            event (Union[str, dict]): lambda handler event
        """
        event, event_type = get_cleaned_event_and_type(event)
        self.event_type = event_type
        self.event_by_asset_id = self.format_event(self.event_type, event)

    def _run(self):
        """Full run of the events based on their asset id"""
        for _asset_id, event in self.event_by_asset_id.items():
            if self.event_type == EventType.PARTIAL_RERUN:
                self.merger.perform_merge(event.get("data", {}))
                continue

            self.app.load(self.event_type, event)
            self.app.run_modules()
            self.app.save_state()
            event.complete_event(api)

    @staticmethod
    def format_event(event_type: EventType, event: Union[list, dict]) -> dict:
        """
        validate the wits_stream event, flatten and organize the data into a desired format
        :param event_type: type of event
        :param event: the wits or scheduler json event
        :return: a dict of records that are grouped by the asset_ids
        """
        if event_type == EventType.PARTIAL_RERUN:
            if not isinstance(event, dict):
                raise EventFormatError("Invalid event!")

            return {event["data"]["asset_id"]: event.copy()}

        elif event_type == EventType.SCHEDULER:
            if not isinstance(event[0], list):
                raise EventFormatError("Invalid event!")

            # Scheduler events type is 'list of lists'; flattening into a single list
            events = [SingleScheduledEvent(item) for sublist in event for item in sublist]
            merging_function = ScheduledEvent

        else:  # 'wits_stream'
            events = [StreamEvent(each) for each in event]
            merging_function = StreamEvent.merge

        # sorting is required otherwise we only capture the last group of each asset_id
        events.sort(key=lambda single_event: single_event.asset_id)
        groups = itertools.groupby(events, key=lambda single_event: single_event.asset_id)

        events_by_asset_id = {group: merging_function(list(dataset)) for group, dataset in groups}

        return events_by_asset_id
