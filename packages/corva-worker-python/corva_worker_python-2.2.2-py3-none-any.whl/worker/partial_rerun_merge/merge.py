import math as pymath
import os
import time
from typing import List, Literal, Optional

import requests
import simplejson as json

from worker.data.api import API
from worker.data.enums import RerunMode
from worker.partial_rerun_merge.models import MergingSchemaModel
from worker.partial_rerun_merge.progress import DatasetProgress, MergingProgress


class PartialRerunMerge:
    """
    Class for performing partial rerun merge operation.
    """

    MAX_TIMESTAMP = 9999999999
    MAX_API_GET_LIMIT = int(os.getenv("PARTIAL_RERUN_MAX_API_GET_LIMIT", 5_000))
    # A default value for the maximum number of records for a heavy collection.
    MAX_RECORDS_COUNT = 10
    # A default value for the maximum number of records to be posted in a batch.
    POST_BATCH_SIZE = int(os.getenv("PARTIAL_RERUN_POST_BATCH_SIZE", int(MAX_API_GET_LIMIT / 5)))
    REMAINING_SECONDS_THRESHOLD = 45

    @property
    def REMAINING_SECONDS_THRESHOLD_HALF(self) -> int:
        """
        Gets the half of the remaining seconds threshold.
        :return: the half of the remaining seconds threshold
        """
        return self.REMAINING_SECONDS_THRESHOLD // 2

    def __init__(
        self,
        schema: MergingSchemaModel,
        api: API,
        logger,
    ):
        """
        Constructor for PartialRerunMerge
        """
        self.schema = schema

        self.api = api
        self.logger = logger

        remaining_seconds_threshold = os.getenv("PARTIAL_RERUN_REMAINING_SECONDS_THRESHOLD")
        if remaining_seconds_threshold:
            self.REMAINING_SECONDS_THRESHOLD = int(remaining_seconds_threshold)

        # the following attributes are set in the preprocess method
        self.partial_well_rerun_id: Optional[int] = None
        self.app_id: Optional[int] = None
        self.original_asset_id: Optional[int] = None
        self.rerun_asset_id: Optional[int] = None
        self.start_timestamp: Optional[int] = None
        self.end_timestamp: Optional[int] = None
        self.rerun_mode: Optional[RerunMode] = None
        self.run_until: Optional[int] = None

        self.start_hole_depth: Optional[float] = None
        self.end_hole_depth: Optional[float] = None

        self.merging_progress: Optional[MergingProgress] = None

    def perform_merge(self, event: dict) -> None:
        """
        Performs a merge operation by updating the cache state,
        merging collections, and updating the status.

        :param event: the event which should be the data part of
            a an event dict, or a python sdk partial rerun event object
            that is converted to a dict

        :raises Exception: if an error occurs during the merge operation
        """
        self.preprocess(event)

        try:
            self.merge_cache_state()
            self.merge_collections()
        except Exception as ex:
            self.logger.error(f"An error occurred during the merge operation: {ex}")
            self.merging_progress.fail_status(str(ex))

        self.update_status()

    def preprocess(self, event: dict) -> None:
        """
        Performs any necessary preprocessing before the merge operation.

        :param event: the event which should be the data part of
            a an event dict, or a python sdk partial rerun event object
            that is converted to a dict
        """
        self.partial_well_rerun_id = event["partial_well_rerun_id"]
        self.app_id = event["app_id"]
        self.original_asset_id = event["asset_id"]
        self.rerun_asset_id = event["rerun_asset_id"]

        segment = event.get("source_type")
        if segment != "drilling":
            raise ValueError(f"Invalid source type: {segment}")

        self.run_until = event["run_until"]

        self.start_timestamp = event["start"]
        start_wits = self.get_wits_at_or(self.rerun_asset_id, self.start_timestamp, "after")

        if end := event.get("end"):
            self.end_timestamp = end
            end_wits = self.get_wits_at_or(self.rerun_asset_id, self.end_timestamp, "before")
        else:
            end_wits = self.get_wits_at_or(self.rerun_asset_id, self.MAX_TIMESTAMP, "before")
            self.end_timestamp = end_wits.get("timestamp")

        if not self.end_timestamp:
            self.end_timestamp = self.MAX_TIMESTAMP

        self.start_hole_depth = start_wits.get("data", {}).get("hole_depth")
        self.end_hole_depth = end_wits.get("data", {}).get("hole_depth")

        self.rerun_mode = RerunMode(event["rerun_mode"])

        self.merging_progress = MergingProgress(self.partial_well_rerun_id, self.app_id, self.api)

    def merge_cache_state(self) -> None:
        """
        Handles the merging of cache state.
        """
        try:
            if self.merging_progress.is_cache_update_completed:
                return

            for module in self.schema.modules:
                module.update_cache(merger=self)
        except Exception as ex:
            error_message = f"Failed to update cache state: {ex}"
            raise Exception(error_message)

    def merge_collections(self) -> None:
        """
        Handles the merging of collections. Update this method as per your requirements.
        """
        is_completed = True

        for collection in self.schema.collections:
            collection_name = collection.collection_name
            self.logger.debug(f"Started merging collection: {collection_name}")

            try:
                if not self.has_time_to_continue_merging():
                    self.logger.debug("Not enough time to continue merging. Stopping.")
                    is_completed = False
                    break

                if self.merging_progress.is_collection_completed(collection_name):
                    self.logger.debug(f"Collection {collection_name} is already completed or failed. Skipping.")
                    continue

                if collection.merging_method:
                    col_is_completed = getattr(self, collection.merging_method)(collection_name)

                else:
                    col_is_completed = self.default_merging_method(collection_name)

                if not col_is_completed:
                    is_completed = False

            except Exception as ex:
                error_message = f"Failed to merge collection '{collection_name}': {ex}"
                raise Exception(error_message)

        if is_completed:
            self.merging_progress.complete_status()

    def default_merging_method(
        self,
        collection_name: str,
        downsample_count: Optional[int] = None,
        downsample_ratio: Optional[float] = None,
        skip_progress: Optional[bool] = False,
    ) -> bool:
        """
        Handles the merging of collections in current mode.
        It copies the data from the rerun asset to the original asset, with
        the 'timestamp' being in the range of the start and end timestamps.

        Args:
            collection_name (str): the collection name
            downsample_count (Optional[int]): the downsample count. Defaults to None.
            downsample_ratio (Optional[float]): the downsample ratio. Defaults to None.
            skip_progress (Optional[bool]): whether to skip the progress. Defaults to False.
        """
        dataset_progress = self.merging_progress.get_dataset_progress(collection_name)
        if not dataset_progress:
            if not skip_progress:
                return True
            dataset_progress = DatasetProgress(0, -1, False, collection_name, "time")

        start_time = self.start_timestamp
        if dataset_progress.is_started():
            start_time = dataset_progress.processed_timestamp + 1

        is_completed = False

        # delete all the data of the original asset within the time range
        is_delete_finished = self._delete_data(collection_name, self.original_asset_id, start_time, self.end_timestamp)
        if not is_delete_finished:
            return is_completed

        while start_time <= self.end_timestamp:
            if not self.has_time_to_continue_merging():
                self.logger.warn("Not enough time to continue merging. Stopping.")
                break

            updated_data = self._get_data(collection_name, self.rerun_asset_id, start_time, self.end_timestamp, "once")
            original_records_count = len(updated_data)
            if not updated_data:
                dataset_progress.mark_completed_at(self.end_timestamp)
                is_completed = True
                break

            last_timestamp = updated_data[-1]["timestamp"]

            if downsample_count is not None or downsample_ratio is not None:
                updated_data = choose_items(updated_data, downsample_count, downsample_ratio)

            self._move_records(collection_name, updated_data)

            dataset_progress.processed_timestamp = last_timestamp

            if original_records_count < self.MAX_API_GET_LIMIT:
                dataset_progress.mark_completed_at(self.end_timestamp)
                is_completed = True
                break

            start_time = last_timestamp + 1

        return is_completed

    def _move_records(self, collection_name: str, records: List[dict]) -> None:
        """
        Moves records from a rerun asset to the original asset within a specified time range.

        Args:
            collection_name (str): The name of the collection to move records from.
            records (List[dict]): The list of records to move.

        Returns:
            None
        """
        # changing the asset_id of the records to the original asset_id
        # and dropping _id key from the records
        for record in records:
            record["asset_id"] = self.original_asset_id

            # since we insert the data from the rerun asset into the original
            # asset we need to drop the '_id' field to avoid data transfer and
            # instead create new records
            record.pop("_id", None)

        # post the records to the original asset
        self._post_data(collection_name, records)
        self.logger.debug(f"   --> {collection_name}, copied {len(records)} records")

    def update_status(self) -> requests.Response:
        """
        Handles the updating of status. Update this method as per your requirements.
        """
        return self.merging_progress.update_status()

    def has_time_to_continue_merging(self, apply_half: Optional[bool] = False) -> bool:
        """
        Checks if there is enough time to continue merging.
        :param apply_half: whether to apply half of the remaining seconds threshold
        :return: True if there is enough time, False otherwise
        """
        if not self.run_until:
            return True

        remaining_seconds = self._get_remaining_seconds()
        threshold = self.REMAINING_SECONDS_THRESHOLD_HALF if apply_half else self.REMAINING_SECONDS_THRESHOLD
        return remaining_seconds > threshold

    def _get_remaining_seconds(self) -> float:
        """
        Gets the remaining seconds before the Lambda function times out.
        :return: the remaining seconds
        """
        return self.run_until - time.time()

    def get_wits_at_or(self, asset_id: int, timestamp: Optional[int], direction: Literal["before", "after"]) -> dict:
        """
        Get a record of the wits collection at or before/after the given timestamp

        :param asset_id: ID of the asset
        :param timestamp: start or end timestamp or None
        :param direction: "before" or "after"
        :return: A dictionary containing the record information
        :raises ValueError: if the provided direction is not "before" or "after"
        """

        collection_name = "wits"
        query = sort = None

        if direction == "before":
            query = "{timestamp#lte#%s}" % timestamp
            sort = "{timestamp:-1}"
        elif direction == "after":
            query = "{timestamp#gte#%s}" % timestamp
            sort = "{timestamp:1}"
        else:
            raise ValueError(f"Invalid direction: {direction}")

        res = self.api.get(
            path="/v1/data/corva/",
            collection=collection_name,
            asset_id=asset_id,
            query=query,
            sort=sort,
            limit=1,
        ).data

        if not res:
            return {}

        return res[0]

    def _get_data(
        self,
        collection_name: str,
        asset_id: int,
        start_timestamp: Optional[int] = None,
        end_timestamp: Optional[int] = None,
        get_mode: Literal["once", "all"] = "all",
    ) -> List[dict]:
        """
        Gets the data from the given collection.

        Args:
            collection_name (str): collection name
            asset_id (int): asset ID
            start_timestamp (Optional[int]): start timestamp
            end_timestamp (Optional[int]): end timestamp
            get_mode (Literal["once", "all"]): get mode

        Returns:
            List[dict]: list of data
        """

        sort = "{timestamp:1}"

        records = []

        start_query = "{timestamp#gte#%s}" % (start_timestamp or 0)
        end_query = "{timestamp#lte#%s}" % (end_timestamp or self.MAX_TIMESTAMP)

        while True:
            query = "%sAND%s" % (start_query, end_query)

            res = self.api.get(
                path="/v1/data/corva/",
                collection=collection_name,
                asset_id=asset_id,
                query=query,
                sort=sort,
                limit=self.MAX_API_GET_LIMIT,
            ).data

            if not res:
                break

            records.extend(res)

            last_timestamp = res[-1]["timestamp"]

            if get_mode == "once" or len(res) < self.MAX_API_GET_LIMIT or last_timestamp >= end_timestamp:
                break

            start_query = "{timestamp#gte#%s}" % (last_timestamp + 1)

        return records

    def _post_data(self, collection_name: str, records: List[dict]):
        """
        Posts the given data to the given collection.

        Args:
            collection_name (str): collection name
            records (List[dict]): list of records
        """
        for i in range(0, len(records), self.POST_BATCH_SIZE):
            data = json.dumps(records[i : i + self.POST_BATCH_SIZE])
            self.api.post(
                path=f"/v1/data/corva/{collection_name}",
                data=data,
            )
            self.sleep()

    def _delete_data(
        self, collection_name: str, asset_id: int, start_timestamp: int, end_timestamp: Optional[int] = None
    ) -> bool:
        """
        Deletes data from a specified collection within a given time range.

        Parameters
        ----------
        collection_name : str
            The name of the collection to delete data from.
        asset_id : int
            The ID of the asset to delete data for.
        start_timestamp : int
            The start timestamp of the time range to delete data for.
        end_timestamp : Optional[int], optional
            The end timestamp of the time range to delete data for. If not provided, the maximum timestamp is used.

        Returns
        -------
        A boolean indicating whether all data was deleted.

        """
        end_timestamp = end_timestamp or self.MAX_TIMESTAMP

        query = "{asset_id#eq#%s}AND{timestamp#gte#%s}AND{timestamp#lte#%s}" % (
            asset_id,
            start_timestamp,
            end_timestamp,
        )

        while True:
            if not self.has_time_to_continue_merging(apply_half=True):
                self.logger.debug("Not enough time to continue deleting. Stopping.")
                return False

            res = self.api.delete(
                path=f"/v1/data/corva/{collection_name}",
                query=query,
                limit=self.MAX_API_GET_LIMIT,
            )

            deleted_count = res.data.get("deleted_count", 0)
            if deleted_count < self.MAX_API_GET_LIMIT:
                break

            self.sleep()

        return True

    def sleep(self, seconds: Optional[int] = 1) -> None:
        """
        Sleeps for a few seconds after each API call.
        """
        time.sleep(seconds)


def choose_items(
    records: List,
    max_records_count: Optional[int] = None,
    max_records_ratio: Optional[float] = None,
) -> List:
    """
    Choose a subset of records from a list of records; the first and last
    records an inclusive.

    Args:
        records (List): A list of records.
        max_records_count (Optional[int]): The maximum number of records
            to choose. If None, all records are chosen.
        max_records_ratio (Optional[float]): The maximum ratio of records
            to choose. If None, all records are chosen.

    Returns:
        List: A list of chosen records.
    """
    if max_records_count is None and max_records_ratio is None:
        return records

    # only one of max_records_count and max_records_ratio can be provided
    if max_records_count is not None and max_records_ratio is not None:
        raise ValueError("Only one of max_records_count and max_records_ratio can be provided.")

    if max_records_ratio is not None:
        max_records_count = int(len(records) * max_records_ratio)

    if max_records_count <= 0 or len(records) <= max_records_count or len(records) < 3:
        return records

    step = pymath.ceil((len(records) - 2) / max_records_count)

    chosen_records = [
        records[0],
        *(records[tracker] for tracker in range(1, len(records) - 1, step)),
        records[-1],
    ]

    return chosen_records
