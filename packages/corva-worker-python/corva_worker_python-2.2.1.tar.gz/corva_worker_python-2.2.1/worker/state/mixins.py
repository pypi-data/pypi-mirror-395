import os
import sys
from functools import cached_property
from typing import List, Optional, Union

import simplejson as json

from worker.data.json_encoder import JsonEncoder
from worker.mixins.logging import LoggingMixin
from worker.mixins.rollbar import RollbarMixin
from worker.state import RedisHandler


class RedisMixin(LoggingMixin, RollbarMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.state = {}

    @cached_property
    def _size_limits(self):
        state_storage_limit_fatal = os.getenv("STATE_STORAGE_CRITICAL_LIMIT", 1_000.0)  # 1 MB
        state_storage_limit_warning = os.getenv("STATE_STORAGE_WARNING_LIMIT", 100.0)  # 100 kB
        size_limits = {"fatal": float(state_storage_limit_fatal), "warning": float(state_storage_limit_warning)}
        return size_limits

    def load_state(self, state_key: Union[str, None] = None, raise_warnings: bool = False) -> dict:
        """
        Load the state from redis
        :param state_key:
        :param raise_warnings: Set to True if size limits warnings should be printed
        :return:
        """
        if not state_key:
            state_key = self.get_formatted_state_key(self.asset_id, self.app_key, self.module_key)

        state = RedisHandler.load_state(state_key)
        size_object = self.check_state_size(state, state_key, raise_warnings=raise_warnings)

        self.debug(self.asset_id, f"Retrieved state of size {size_object} kb")
        self.state = state
        return state

    def save_state(self, state_key: Union[str, None] = None, raise_warnings: bool = True, **kwargs) -> None:
        """
        Save the state to redis
        :param state_key:
        :param raise_warnings: Set to True if size limits warnings should be printed
        :return:
        """
        if not state_key:
            state_key = self.get_formatted_state_key(self.asset_id, self.app_key, self.module_key)

        size_object = self.check_state_size(self.state, state_key, raise_warnings=raise_warnings)
        RedisHandler.save_state(self.state, state_key, **kwargs)
        self.debug(self.asset_id, f"Saved state of size {size_object} kb")

    def delete_states(self, state_keys: Union[List[str], str]):
        """
        Delete state for current module
        :param state_keys:
        :return:
        """
        if not isinstance(state_keys, list):
            state_keys = [state_keys]

        RedisHandler.delete_states(state_keys)
        self.debug(None, "Deleted state from Redis")

    @staticmethod
    def get_formatted_state_key(asset_id: int, app_key: str, module_key: Optional[str] = None) -> str:
        """
        Returns the state key in Corva naming format
        :param asset_id:
        :param module_key:
        :param app_key:
        :return:
        """
        state_key = "corva/{0}.{1}".format(asset_id, app_key)

        if module_key:
            return "{0}.{1}".format(state_key, module_key)

        return state_key

    def check_state_size(self, state, state_key, raise_warnings=True):
        """
        Check the size of the state dictionary and generate warnings if necessary
        :param state:
        :param state_key:
        :param raise_warnings:
        :return:
        """
        size_object = sys.getsizeof(json.dumps(state, cls=JsonEncoder, ignore_nan=True)) / 1024

        if not raise_warnings:
            return size_object

        size_limit = self._size_limits["fatal"]
        if size_object > size_limit:
            message = f"State_key {state_key} is of size {size_object} kb > {size_limit} kb."
            self.fatal(self.asset_id, message)
            self.track_message(message, level="critical")
            return size_object

        size_limit = self._size_limits["warning"]
        if size_object > size_limit:
            message = f"State_key {state_key} is of size {size_object} kb > {size_limit} kb."
            self.warn(self.asset_id, message)
            return size_object

        return size_object
