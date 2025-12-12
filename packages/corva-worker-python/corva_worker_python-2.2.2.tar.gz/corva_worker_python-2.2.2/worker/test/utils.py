import traceback

import simplejson as json

from worker.state.mixins import RedisMixin


def file_to_json(file_name):
    with open(file_name, mode="r") as file:
        _json = json.load(file)
        return _json


def get_last_processed_timestamp(asset_id: int, state_key: str):
    """
    Get the last_processed_timestamp from state storage
    :param asset_id:
    :param state_key:
    """
    try:
        state_app = RedisMixin()
        state_app.asset_id = asset_id
        previous_state = state_app.load_state(state_key=state_key)
        return previous_state.get("last_processed_timestamp", None)
    except Exception:
        print("Error occurred while reading state from Redis!")
        traceback.print_exc()

    return None


def create_scheduler_events(asset_id, start_timestamp, end_timestamp, step):
    """
    Creating scheduler events
    :param asset_id:
    :param start_timestamp:
    :param end_timestamp:
    :param step:
    :return:
    """
    if start_timestamp > end_timestamp:
        raise ValueError(f"start_timestamp ({start_timestamp}) is greater than end_timestamp ({end_timestamp})!")
    if step <= 0 or step > 3600:
        raise ValueError(f"step ({step}) is outside the (0, 3600] range.")

    triggers = range(start_timestamp, end_timestamp, step)
    events = [
        [[{"asset_id": asset_id, "schedule_start": 1000 * trigger, "schedule_end": 1000 * (trigger + step)}]]
        for trigger in triggers
    ]
    return events
