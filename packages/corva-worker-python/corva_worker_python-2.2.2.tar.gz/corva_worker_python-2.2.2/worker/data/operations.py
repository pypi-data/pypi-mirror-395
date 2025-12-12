import os
from typing import List, Literal, Tuple, Union

import numpy as np
import simplejson as json

from worker.data import math
from worker.data.api import API
from worker.data.enums import Environment, EventType
from worker.data.wits import WITS
from worker.exceptions import NotFound


def gather_data_for_period(
    asset_id: int, start: int, end: int, limit: int = 1800, collection: str = "wits", fields: str = None
) -> list:
    """
    Get the wits data from API for an asset over an interval
    :param asset_id: asset id
    :param start: start timestamp
    :param end: end timestamp
    :param limit: count of the data
    :param collection: any collection
    :param fields: fields to be filtered
    :return: a list of wits data
    """
    if start >= end:
        return []

    query = "{timestamp#gte#%s}AND{timestamp#lte#%s}" % (start, end)
    worker = API()

    wits_dataset = worker.get(
        path="/v1/data/corva",
        collection=collection,
        asset_id=asset_id,
        sort="{timestamp: 1}",
        limit=limit,
        query=query,
        fields=fields,
    ).data

    if not wits_dataset:
        return []

    return wits_dataset


def get_one_data_record(asset_id: int, timestamp_sort: int = -1, collection: str = "wits") -> dict:
    """
    Get the first or last wits record of a given asset
    :param asset_id:
    :param timestamp_sort:
    :param collection:
    :return:
    """
    api_worker = API()
    data = api_worker.get(
        path="/v1/data/corva/",
        collection=collection,
        asset_id=asset_id,
        sort="{timestamp:%s}" % timestamp_sort,
        limit=1,
    ).data

    if not data:
        return {}

    return data[0]


def delete_collection_data_of_asset_id(asset_id: int, collections: Union[str, list]):
    """
    Delete all the data of a collection for an asset id.
    :param asset_id:
    :param collections: a collection or a list of collections
    :return:
    """
    worker = API()

    if isinstance(collections, str):
        collections = [collections]

    for collection in collections:
        path = "/v1/data/corva/%s" % collection
        query = "{asset_id#eq#%s}" % asset_id

        # Looping a maximum of 2000 times. Tries to delete a maximum of 7.2 million records.
        for _ in range(2000):
            # Upon delete API returns the following response {"deleted_count": 10000}
            res = worker.delete(path=path, query=query, limit=3600, retry_count=1).data
            records_deleted = res.get("deleted_count") or 0

            # API currently deletes 10000 records at a time, if the deleted count is less than 3600, break loop
            if records_deleted < 3600:
                break


def point_main_envs(env: Literal["qa", "staging", "production", "local"]):
    """
    The purpose of this function is to point main environment variables to
    the provided environment. This method updates the following environment
    variables:
    - API_ROOT_URL
    - API_KEY
    - CACHE_URL

    :param env: the environment to point to
    :return:
    """
    if not env:
        return

    # validating the environment
    Environment(env)

    api_url = os.getenv(f"API_ROOT_URL_{env}") or os.getenv("API_ROOT_URL")
    api_key = os.getenv(f"API_KEY_{env}") or os.getenv("API_KEY")
    cache_url = os.getenv(f"CACHE_URL_{env}") or os.getenv("CACHE_URL")

    if not all([api_url, api_key, cache_url]):
        raise ValueError("Missing environment variables!")

    new_envs = {"API_ROOT_URL": api_url, "API_KEY": api_key, "CACHE_URL": cache_url}

    os.environ.update(new_envs)


def setup_api_worker(env: Literal["qa", "staging", "production", "local"], app_name: str) -> API:
    """
    Set up the Corva API worker
    :param env: environment ['local', 'qa', 'staging', 'production']
    :param app_name:
    :return: api worker
    """
    # validating the environment
    Environment(env)

    api_url = os.getenv(f"API_ROOT_URL_{env}") or os.getenv("API_ROOT_URL")
    api_key = os.getenv(f"API_KEY_{env}") or os.getenv("API_KEY")

    options = {"api_url": api_url, "api_key": api_key, "app_name": app_name}
    api_worker = API(**options)

    return api_worker


def setup_redis_worker(env: Literal["qa", "staging", "production", "local"]):
    """
    Set up the Redis worker
    :param env: environment ['local', 'qa', 'staging', 'production']
    :return: redis worker
    """
    # validating the environment
    Environment(env)

    cache_url = os.getenv(f"CACHE_URL_{env}") or os.getenv("CACHE_URL")

    import redis

    redis_worker = redis.Redis.from_url(cache_url, decode_responses=True)

    return redis_worker


def get_config_by_id(string_id: str, collection: str) -> Union[dict, None]:
    """
    Get the drillstring or casingstring from API by providing mongodb _id
    :param string_id: mongodb _id of the drillstring
    :param collection:
    :return:
    """
    string = None
    try:
        string = API().get_by_id(path="/v1/data/corva/", collection=collection, id=string_id).data
    except NotFound:
        pass

    return string


def is_number(data):
    """
    Check and return True if data is a number, else return False
    :param data: Input can be string, number or nan
    :return: True or False
    """
    try:
        data_cast = float(data)
        if data_cast >= 0 or data_cast <= 0:  # to make sure it is a valid number
            return True

        return False
    except ValueError:
        return False
    except TypeError:
        return False


def is_finite(data):
    """
    Check if the given data is a finite number
    Note that the string representation of a number is not finite
    :param data:
    :return: True or False
    """
    try:
        return is_number(data) and np.isfinite(data)
    except (TypeError, ValueError):
        return False


def is_int(s: str) -> bool:
    """
    To check if the given string is an integer or not
    :param s:
    :return:
    """
    try:
        int(s)
        return True
    except ValueError:
        return False


def is_null(value) -> bool:
    """
    Will return True if the value is null, None, any variant of -999.25

    :param value:
    :return:
    """
    value = to_number(value)
    if value is None:
        return True

    if value >= 0:
        return False

    value = str(value)
    for each in ["-", ".", "0"]:
        value = value.replace(each, "")

    if value == "99925":
        return True

    return False


def to_number(data):
    """
    Check and return if the data can be cast to a number, else return None
    :param data: Input can be string, number or nan
    :return: A numbers
    """
    if is_number(data):
        return float(data)

    return None


def none_to_nan(data):
    """
    If data is a list, return list with None replaced with nan.
    If data is None, return nan
    :param data:
    :return:
    """
    if isinstance(data, list):
        return [np.nan if e is None else e for e in data]

    if data is None:
        return np.nan

    return data


def get_data_by_path(data: dict, path: str, func=lambda x: x, **kwargs):
    """
    To find the path to a key in a nested dictionary.
    Note that none of the keys should end up in a list
    :param data:
    :param path: path to the final key; example of the paths are:
        'data.X.Y'
        'data.bit_depth'
    :param func: the type of the data (int, str, float, ...)
    :param kwargs: pass default value in case the path not found;
    note that None is an acceptable default
    :return:
    """
    has_default = "default" in kwargs
    default = kwargs.pop("default", None)

    if not path:
        if has_default:
            return default

        raise KeyError("No key provided")

    keys = path.split(".")

    while keys:
        current_key = keys.pop(0)

        if current_key not in data:
            if has_default:
                return default

            raise KeyError(f"{current_key} not found in path")

        data = data.get(current_key)

    if data is None:
        return None

    return func(data)


def is_in_and_not_none(d: dict, key: str):
    """
    An structured way of getting data from a dict.
    :param d: the dictionary
    :param key:
    :return: True or False
    """
    if key in d.keys() and d[key] is not None:
        return True

    return False


def nanround(value, decimal_places=2):
    """
    Similar to python built-in round but considering None values as well
    :param value:
    :param decimal_places:
    :return:
    """
    if is_number(value):
        return round(value, decimal_places)

    return None


def merge_dicts(d1: dict, d2: dict) -> dict:
    """
    Merge two dictionaries
    Note: the 2nd item (d2) has a higher priority to write items with similar keys
    :param d1:
    :param d2:
    :return:
    """
    d = {**d1, **d2}
    return d


def equal(obj1: object, obj2: object, params: List[str]) -> bool:
    """
    To check if two objects are equal by comparing the given parameters.
    :param obj1:
    :param obj2:
    :param params:
    :return:
    """
    if type(obj1) is not type(obj2):
        return False

    return all(getattr(obj1, param) == getattr(obj2, param) for param in params)


def get_cleaned_event_and_type(event) -> Tuple[Union[list, dict], EventType]:
    """
    validate and flatten the events and organize the data into a desired format

    Task and generic events format is : dict => {}
    Scheduler events format is: list of list of dict => [[{}]]
    Kafka events format is: list of dict => [{}]
    The above formats can be used to determine the format

    :param event: a scheduler of kafka stream
    :return: event and event_type
    """

    if not event:
        raise ValueError("Empty events")

    if isinstance(event, (str, bytes, bytearray)):
        event = json.loads(event)

    if isinstance(event, dict):
        if event.get("event_type") == "partial-well-rerun-merge":
            return event, EventType.PARTIAL_RERUN

        if "task_id" in event:
            return event, EventType.TASK

        if "asset_id" in event:
            return event, EventType.GENERIC

        raise TypeError("Missing task_id or asset_id keys in event")

    if not isinstance(event, list):
        raise TypeError("Event is not a list or a dict")

    first_event = event[0]
    if isinstance(first_event, list):
        if first_event[0] and "schedule_start" in first_event[0]:
            return event, EventType.SCHEDULER

        raise Exception("Missing scheduler_start key in scheduler event")

    elif isinstance(first_event, dict):
        # new kafka stream format: list of json objects, each with metadata and records
        # event = [{"metadata": { ... }, "records": [ ... ]}, {"metadata": { ... }, "records": [ ... ]}]
        return event, EventType.STREAM

    raise TypeError("Event is not either a scheduler or kafka consumer")


def compute_time_step(records: Union[List[WITS], List[dict], List[float]], percent=50) -> Union[int, None]:
    """
    Compute the time step of the wits records
    If the intention is to split the data based on their activities a higher percent
    is recommended (such as 99%). For other cases 50% might work.

    :param records: a list of wits records in WITS or dict format, or a list of timestamps
    :param percent: this is an important parameter to get the correct time step
    :return:
    """
    if len(records) <= 3:
        return None

    if not 0 <= percent <= 100:
        raise ValueError(f"percent ({percent}) is out of [0, 100] range.")

    if isinstance(records[0], WITS):
        timestamps = [rec.timestamp for rec in records]
    elif isinstance(records[0], dict):
        timestamps = [rec.get("timestamp") for rec in records]
    else:
        timestamps = records

    timestamps = [timestamp for timestamp in timestamps if is_finite(timestamp)]

    # a list of time steps for all the timestamps
    diffs = np.diff(timestamps)

    time_step = math.percentile(diffs, percent)
    if not time_step:
        return None

    return int(time_step)


def compare_float(value1, value2, tolerance):
    """
    Compare two values based on the given tolerance
    :param value1: first number
    :param value2: second number
    :param tolerance: tolerance of the comparison
    :return: +1 when value1 > value2 + tolerance, -1 when value2 > value1 + tolerance, 0 otherwise
    """
    if value1 > value2 + tolerance:
        return 1

    if value2 > value1 + tolerance:
        return -1

    return 0


def is_stream_app():
    lambda_name = os.getenv("AWS_LAMBDA_FUNCTION_NAME")
    if not lambda_name:
        return False

    return "task" not in lambda_name.lower()
