from typing import List, Union

from worker import constants
from worker.data.operations import get_data_by_path
from worker.event import Event, EventType


class StreamEvent(Event):
    """A stream event class that holds the events of a single asset_id."""

    def __init__(self, event: dict, is_posting_to_message_producer: bool = False):
        super().__init__(EventType.STREAM)

        self.metadata = event.get("metadata") or {}
        self.records = event.get("records") or []

        self.asset_id = 0
        if self.records:
            self.asset_id = self.records[0].get("asset_id")

        app_key = constants.get("global.stream_app_key")
        self.app_connection_id = get_data_by_path(
            self.metadata, f"apps.{app_key}.app_connection_id", func=int, default=None
        )

    @classmethod
    def merge(cls, events: List["StreamEvent"]) -> Union["StreamEvent", None]:
        """Merge stream events of the same asset id into one"""
        if not events:
            return None

        merged_event = events[0]
        for each in events[1:]:
            merged_event.add(each)

        return merged_event

    def add(self, other: "StreamEvent"):
        if self.asset_id != other.asset_id:
            raise Exception(f"Events of different assets can not be merged; {self.asset_id} and {other.asset_id}!")

        self.add_records(other.records)

    def build_message_producer_payload(self) -> dict:
        return {"app_connection_id": self.app_connection_id, "asset_id": self.asset_id, "data": self.records}

    def complete_event(self, api) -> None:
        self.post_to_message_producer(api)
