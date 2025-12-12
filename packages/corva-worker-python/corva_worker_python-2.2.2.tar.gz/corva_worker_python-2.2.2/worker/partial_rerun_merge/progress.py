"""
This module defines the progress of the partial reruns.
"""

from dataclasses import asdict, dataclass
from typing import List, Optional

import requests
import simplejson as json

from worker.data.api import API
from worker.data.enums import PartialRerunStatus


@dataclass
class DatasetProgress:
    """
    Represents the progress of a dataset.

    Attributes:
        dataset_id (int): The ID of the dataset.
        processed_timestamp (int): The timestamp when the dataset was processed.
        completed (bool): Whether the dataset processing is completed or not.
        dataset_name (str): The name of the dataset.
        dataset_type (str): The type of the dataset. Not used here.
    """

    dataset_id: int
    processed_timestamp: int
    completed: bool
    dataset_name: str
    dataset_type: str

    def is_completed(self) -> bool:
        """
        Returns a boolean indicating whether the progress has been completed.
        """
        return self.completed

    def is_started(self) -> bool:
        """
        Returns a boolean indicating whether the progress has been started.
        """
        return self.processed_timestamp > 0

    def mark_completed_at(self, processed_timestamp: int) -> None:
        """
        Marks the progress as completed and sets the processed timestamp.

        Args:
            processed_timestamp (int): The timestamp when the progress was processed.
        """
        self.completed = True
        self.processed_timestamp = processed_timestamp

    @classmethod
    def set_from_dict(cls, json_object: dict) -> "DatasetProgress":
        """Set the object from a dict.

        Args:
            json_object (dict): the input json

        Returns:
            _type_: DatasetProgress
        """
        return cls(**json_object)

    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of the Progress object.

        Returns:
            dict: A dictionary containing the dataset_id, processed_timestamp,
                    completed, and dataset_name attributes.
        """
        return asdict(self)

    def get_trimmed_dataset_name(self) -> str:
        """
        Returns the trimmed dataset name by splitting the dataset name
        with "#" delimiter and returning the last part.

        Example: "corva#circulation.volumetric" -> "circulation.volumetric"

        Returns:
            str: The trimmed dataset name.
        """
        return self.dataset_name.split("#")[-1]


class MergingProgress:
    """
    Represents the progress of merging a partial rerun for a specific app.

    Attributes:
        partial_well_rerun_id (int): The ID of the partial rerun.
        app_id (int): The ID of the app.
        status (PartialRerunStatus): The status of the partial rerun.
        dataset_progresses (List[DatasetProgress]): The progress of each dataset
            in the partial rerun.
        api: (Worker) The API object used to make requests to the Corva API.
        is_cache_update_completed (bool): Whether the cache update is completed.
    """

    def __init__(self, partial_well_rerun_id: int, app_id: int, api: API):
        """
        Initializes a new instance of the Progress class.

        Args:
            partial_rerun_id (int): The ID of the partial rerun.
            app_id (int): The ID of the application.
            api: The API object.

        Returns:
            None
        """
        self.partial_well_rerun_id = partial_well_rerun_id
        self.app_id = app_id
        self.status = PartialRerunStatus.MERGING
        self.dataset_progresses: List[DatasetProgress] = []

        self.api = api

        # getting and parsing the progress
        request = self.api.get(self.get_url_path()).data
        self.parse_progress(request)

        self.is_cache_update_completed = self.determine_if_cache_update_completed()

        # in case of failure, this will be set to the reason of failure
        self.fail_reason: Optional[str] = None

    def parse_progress(self, request: dict) -> None:
        """
        Parses the progress information retrieved from the API and populates the
        'dataset_progresses' list.

        Args:
            request (dict): The progress information retrieved from the API.

        Returns:
            None
        """
        progresses = request.get("included") or []

        for progress in progresses:
            if progress.get("type") != "partial_well_rerun_dataset_progress":
                continue

            attributes = progress.get("attributes") or {}

            dataset_progress = DatasetProgress.set_from_dict(attributes)
            self.dataset_progresses.append(dataset_progress)

    def complete_status(self) -> None:
        """
        Marks the partial rerun merge as completed.
        """
        self.status = PartialRerunStatus.COMPLETED

    def fail_status(self, reason: str) -> None:
        """
        Sets the status of the partial rerun to FAILED and provides a reason for the failure.

        Args:
            reason (str): The reason for failure.
        """
        self.status = PartialRerunStatus.FAILED
        self.fail_reason = reason

    def get_dataset_progress(self, dataset_name: str) -> Optional[DatasetProgress]:
        """
        Gets the progress of the dataset with the given name.

        Args:
            dataset_name (str): The name of the dataset.

        Returns:
            DatasetProgress: The progress of the dataset.
        """
        return next((dp for dp in self.dataset_progresses if dp.get_trimmed_dataset_name() == dataset_name), None)

    def is_collection_completed(self, collection_name: str) -> bool:
        """
        Checks if a collection with the given name has been completed.

        Args:
            collection_name (str): The name of the collection to check.

        Returns:
            bool: True if the collection has been completed, False otherwise.
        """
        for dataset_progress in self.dataset_progresses:
            if dataset_progress.get_trimmed_dataset_name() == collection_name:
                return dataset_progress.completed

        return False

    def determine_if_cache_update_completed(self) -> bool:
        """
        Checks if the cache update is completed.
        Since there is no collection named "cache", it checks if ANY collection is completed,
        and since cache update needs to be done once, therefore we need to know when the merge
        will continue in the next iteration, we need to check if the cache update is already completed.

        Returns:
            bool: True if the cache update has completed for all datasets, False otherwise.
        """
        return any(dataset_progress.is_started() for dataset_progress in self.dataset_progresses)

    def get_url_path(self) -> str:
        """
        Returns the URL path for the API request.

        Returns:
            str: URL Path for the API request.
        """
        return f"/v2/partial_reruns/{self.partial_well_rerun_id}/app_progress/{self.app_id}"

    def to_dict(self) -> dict:
        """
        Converts the merging progress to a dict.

        Returns:
            dict: progress as a dict.
        """
        dataset_progresses = [dataset_progress.to_dict() for dataset_progress in self.dataset_progresses]

        output = dict(app_progress=dict(status=self.status.value, dataset_progresses=dataset_progresses))

        if self.fail_reason:
            output["app_progress"]["fail_reason"] = self.fail_reason

        return output

    def update_status(self) -> requests.Response:
        """
        Sends the updated merging progress to the API.
        """
        url_path = self.get_url_path()
        body = json.dumps(self.to_dict())
        response = self.api.patch(url_path, data=body)
        return response.response
