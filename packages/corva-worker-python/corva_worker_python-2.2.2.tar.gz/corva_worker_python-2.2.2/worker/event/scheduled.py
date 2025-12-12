from typing import List, Union

from worker.event import Event, EventType


class SingleScheduledEvent:
    def __init__(self, single_stream_event: dict):
        self.asset_id = single_stream_event.get("asset_id") or 0

        self.start_time = single_stream_event.get("schedule_start", 0) / 1000
        self.end_time = single_stream_event.get("schedule_end", 0) / 1000
        self.schedule_id = single_stream_event.get("schedule")
        self.app_connection_id = single_stream_event.get("app_connection")

    def complete_event(self, api) -> None:
        """Sets schedule as completed."""
        if not self.schedule_id:
            return

        api.post(path=f"/scheduler/{self.schedule_id}/completed")


class ScheduledEvent(Event):
    """A scheduled event class that holds the events of a single asset_id."""

    def __init__(self, new_records: Union[SingleScheduledEvent, List[SingleScheduledEvent]]):
        super().__init__(EventType.SCHEDULER)

        if new_records:
            self.add_records(new_records)

        if self.records:
            self.app_connection_id = self.records[-1].app_connection_id

    def add_records(self, new_records: Union[SingleScheduledEvent, List[SingleScheduledEvent]]):
        if isinstance(new_records, SingleScheduledEvent):
            new_records = [new_records]

        if not self.records:
            self.asset_id = new_records[0].asset_id

        super().add_records(new_records)

    def complete_event(self, api) -> None:
        """
        Two steps can happen for scheduler events.
        1. Sets schedule as completed; this happens for all the events.
        2. If another lambda function is following your lambda then it should
           send a message to message producer as well.

        Args:
            api (API):
        """
        # Step 1: mark all the events as completed.
        for each in self.records:
            each.complete_event(api)

        # Step 2: in case another lambda function following your lambda
        self.post_to_message_producer(api)

    def build_message_producer_payload(self) -> dict:
        data = [{"timestamp": self.records[-1].start_time}]

        return {"app_connection_id": self.app_connection_id, "asset_id": self.asset_id, "data": data}
