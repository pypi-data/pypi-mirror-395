from worker import constants  # noqa: #402

constants.update(
    {
        "global": {
            "app-name": "WorkerTest.RedisMixin",
            "app-key": "worker_test-state_mixin",
            "event-type": "wits_stream",
            "query-limit": 3600,
        },
        "worker_test-state_mixin": {
            "redis-tester": {},
        },
    }
)
