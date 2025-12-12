import os
from typing import List, Union

import redis
import simplejson as json

from worker.data.json_encoder import JsonEncoder
from worker.mixins.logging import Logger


class RedisHandler:
    redis_ttl = os.getenv("REDIS_TTL", 90 * 24 * 3600)  # 90 days
    _redis_connection = None

    @classmethod
    def _get_redis_connection(cls) -> redis.client.Redis:
        """
        Setup redis and get connection if one does not exist already
        :return:
        """
        # Use previous connection if cached
        if cls._redis_connection:
            Logger.debug("Using existing connection")
            return cls._redis_connection

        # If connection does not exist, create a new one
        cls._redis_connection = cls._new_redis_connection()

        return cls._redis_connection

    @classmethod
    def _new_redis_connection(cls) -> redis.client.Redis:
        """
        Creates a new Redis connection
        :return:
        """
        cache_url = os.getenv("CACHE_URL", None)

        if not cache_url:
            raise Exception("redis key (CACHE_URL) not found in Environment Variables.")

        _redis_connection = redis.Redis.from_url(cache_url)

        if not _redis_connection:
            raise Exception(f"Could not connect to Redis with URL: {cache_url}")

        client_id = _redis_connection.client_id()
        Logger.log(f"Created a new connection with {client_id=}")
        return _redis_connection

    @classmethod
    def setup_existing_connection(cls, existing_connection: Union[redis.client.Redis, None]) -> redis.client.Redis:
        """
        Set the internal connection variable to existing connection provided in this function
        The returned output should be saved to a global variable if it is intended to cache the
        connection across lambda invokes
        :param existing_connection:
        :return:
        """
        cls._redis_connection = existing_connection
        return cls._get_redis_connection()

    @classmethod
    def load_state(cls, state_key: str) -> dict:
        """
        Load state from redis
        :return:
        """
        state = cls._get_redis_connection().get(state_key)
        if state:
            return json.loads(state)

        return {}

    @classmethod
    def save_state(cls, state: dict, state_key: str, **kwargs):
        """
        Save the state to redis. Uses redis_ttl from kwargs if passed, fallbacks to env var then default 90 days
        :param state:
        :param state_key:
        :return:
        """
        # Using redis ttl from kwargs if passed in.
        redis_ttl = kwargs.pop("redis_ttl", cls.redis_ttl)
        cls._get_redis_connection().set(
            state_key, value=json.dumps(state, cls=JsonEncoder, ignore_nan=True), ex=redis_ttl
        )

    @classmethod
    def delete_states(cls, state_keys: List[str]):
        """
        Delete the states corresponding to given keys
        :param state_keys: a list of redis keys
        :return:
        """
        cls._get_redis_connection().delete(*state_keys)
