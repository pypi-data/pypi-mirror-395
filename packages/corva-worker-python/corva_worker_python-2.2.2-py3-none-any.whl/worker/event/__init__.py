import abc
from functools import cached_property

import simplejson as json

from worker import constants
from worker.data.enums import EventType
from worker.data.json_encoder import JsonEncoder


class Event(abc.ABC):
    """An event class that holds the events of a single asset_id."""

    def __init__(self, event_type: EventType):
        self.event_type: EventType = event_type

        self.asset_id: int = None
        self.records = []
        self.app_connection_id = None

    def add_records(self, new_records: list) -> None:
        self.records.extend(new_records)

    @abc.abstractmethod
    def complete_event(self, api) -> None:
        raise NotImplementedError

    def __len__(self):
        return len(self.records)

    def __getitem__(self, index: int):
        return self.records[index]

    @cached_property
    def is_posting_to_message_producer(self) -> bool:
        """
        Whether to post to message producer for the wits stream and scheduler events or not.
        If there is no lambda app following your app then this should be false,
        because this process is intracting with the API which slows the process down.
        """
        is_posting: bool = constants.get("global.post-to-message-producer", False)
        return is_posting

    @abc.abstractmethod
    def build_message_producer_payload(self) -> dict:
        raise NotImplementedError

    def post_to_message_producer(self, api):
        if not self.is_posting_to_message_producer or not self.app_connection_id:
            return

        payload = self.build_message_producer_payload()
        api.post(path="/v1/message_producer", data=json.dumps(payload, cls=JsonEncoder, ignore_nan=True))
