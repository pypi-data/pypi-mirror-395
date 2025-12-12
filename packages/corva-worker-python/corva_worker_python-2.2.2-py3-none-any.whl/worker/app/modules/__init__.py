from typing import Union

import simplejson as json

from worker import constants
from worker.data.api import API
from worker.data.enums import RerunMode
from worker.data.json_encoder import JsonEncoder
from worker.mixins.logging import LoggingMixin
from worker.mixins.rollbar import RollbarMixin
from worker.partial_rerun_merge.models import RerunMergeCacheUpdater
from worker.state.mixins import RedisMixin
from worker.state.state import State


class Module(RedisMixin, LoggingMixin, RollbarMixin):
    """
    This is an abstract base module that needs to be extended by an actual module.
    """

    # module_key is used for redis access and state of this module
    app_key = constants.get("global.app-key")
    app_name = constants.get("global.app-name")
    module_key = "module"
    collection = "collection"
    module_state_fields = {"last_processed_timestamp": int}

    enabled = True

    def __init__(self, global_state, *args, **kwargs):
        self.asset_id = global_state.get("asset_id")

        self.global_state = global_state

        super().__init__(*args, **kwargs)

    def run(self, wits_stream: list):
        """
        :param wits_stream: a wits stream event
        :return:
        """
        # load the state
        state = self.get_state()
        self.state = self.process_module_state(state)

        # subclasses should implement their own run

    def should_run_processor(self, event):
        raise Exception("This method need to be implemented by subclasses!")

    def get_state(self, state_key: [str, None] = None, raise_warnings: bool = False) -> dict:
        current_state = super().load_state(state_key=state_key, raise_warnings=raise_warnings)
        return State(self.module_state_fields, current_state)

    @staticmethod
    def process_module_state(state):
        return state

    def set_state(self, key, value):
        self.state[key] = value

    def load_dataset(self, event):
        return event

    def run_module(self, dataset: Union[list, dict], beginning_results: list) -> list:
        raise Exception("Not implemented")

    def get_last_exported_timestamp_from_collection(self, asset_id, query=None, less_than=None):
        """
        Query the module collection for this asset_id + module, sorted by timestamp descending,
        limit 1, grab the last item's timestamp. Default to 0 if no records found.
        @asset_id:
        @less_than: the timestamp before which you want to get
        """
        if less_than:
            query = query or ""
            query += "AND{timestamp#lt#%s}" % less_than

        worker = API()
        last_document = worker.get(
            path="/v1/data/corva",
            query=query,
            collection=self.collection,
            asset_id=asset_id,
            sort="{timestamp: -1}",
            limit=1,
        ).data

        if not last_document:
            return 0

        last_document = last_document[0]
        last_processed_timestamp = last_document.get("timestamp", 0)

        return last_processed_timestamp

    @staticmethod
    def gather_first_wits_timestamp_since(asset_id: int, since: int, activity_fields=None, operator="eq") -> int:
        """
        Query the Wits collection for this asset_id where state in wits_states and timestamp >= since
        """

        query = "{timestamp#%s#%s}" % ("gt", since)

        operator = operator.lower()

        if activity_fields:
            if operator == "eq" and isinstance(activity_fields, list):
                operator = "in"

            if operator in ("in", "nin"):
                if not isinstance(activity_fields, list):
                    activity_fields = [activity_fields]

                # Put each state into a formatted string for querying
                activity_fields = ["'{0}'".format(state) for state in activity_fields]
                activity_fields = "[{0}]".format(",".join(activity_fields))
            else:
                activity_fields = "'{0}'".format(activity_fields)

            query += "AND{data.state#%s#%s}" % (operator, activity_fields)

        worker = API()
        first_wits_since = worker.get(
            path="/v1/data/corva", collection="wits", asset_id=asset_id, sort="{timestamp: 1}", limit=1, query=query
        ).data

        if not first_wits_since:
            return 0

        first_wits_since = first_wits_since[0]
        first_wits_since_timestamp = first_wits_since.get("timestamp", 0)

        return first_wits_since_timestamp

    @staticmethod
    def gather_maximum_timestamp(event, start, activity_fields):
        """
        get the maximum time stamp of a stream of data
        :param event: a stream of data  that the majority is wits collection
        :param start:
        :param activity_fields:
        :return:
        """
        maximum_timestamp = start
        for data in event:
            if data.get("collection") == "wits" and data.get("data", {}).get("state", None) in activity_fields:
                maximum_timestamp = max(data.get("timestamp", 0), maximum_timestamp)

        return maximum_timestamp

    def gather_minimum_timestamp(self, asset_id: int, event: list):
        minimum = self.get_last_exported_timestamp_from_collection(asset_id)

        if not minimum:
            minimum = event[0]["timestamp"] - 1800

        return minimum

    def gather_collections_for_period(self, asset_id, start, end, query=None):
        limit = constants.get("global.query-limit")

        query = query or ""
        if query:
            query += "AND"

        query += "{timestamp#gte#%s}AND{timestamp#lte#%s}" % (start, end)

        worker = API()
        dataset = worker.get(
            path="/v1/data/corva",
            collection=self.collection,
            asset_id=asset_id,
            query=query,
            sort="{timestamp: 1}",
            limit=limit,
        ).data

        if not dataset:
            return []

        return dataset

    def store_output(self, asset_id, output):
        """
        to store/post results
        :param asset_id: asset id of the well
        :param output: an array of json objects to be posted
        :return: None
        """

        if not asset_id or not output or not self.collection:
            return

        output = self.format_output(output)

        self.debug(asset_id, "{0} output -> {1}".format(self.module_key, output))

        worker = API()
        worker.post(path="/v1/data/corva", data=output)

    def build_empty_output(self, wits: dict) -> dict:
        """
        Building an empty output result.
        :param wits: one wits record
        :return:
        """
        output = {
            "timestamp": int(wits.get("timestamp")),
            "company_id": int(wits.get("company_id")),
            "asset_id": int(wits.get("asset_id")),
            "provider": str(wits.get("provider", "corva")),
            "version": 1,
            "collection": self.collection,
            "data": {},
        }

        enable_output_type_field = constants.get(
            "{}.{}.enable-output-type-field".format(self.app_key, self.module_key), False
        )

        if not enable_output_type_field:
            return output

        # If a specific module enforces type field in the output collection,
        # build_empty_output adds an additional type field to the output.
        # This can be enforced by setting "enable-output-type-field" to True in the module app constants.
        output.update({"type": self.module_key})

        return output

    @staticmethod
    def format_output(output):
        output = json.dumps(output, cls=JsonEncoder, ignore_nan=True)
        return output

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

        original_state_key = redis_handler.get_formatted_state_key(original_asset_id, cls.app_key, cls.module_key)
        rerun_state_key = redis_handler.get_formatted_state_key(rerun_asset_id, cls.app_key, cls.module_key)

        original_state = redis_handler.load_state(original_state_key)
        rerun_state = redis_handler.load_state(rerun_state_key)

        original_state = RerunMergeCacheUpdater.default_updater(original_state, rerun_state)

        redis_handler.state = original_state
        redis_handler.save_state(original_state_key)
