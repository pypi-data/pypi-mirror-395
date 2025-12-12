from worker import constants
from worker.app.modules.__init__ import Module


class Scheduler(Module):
    """
    This is an abstract module that needs to be extended by actual modules.
    An example of this module would be running an app at the frequency of
    once every X seconds regardless of the activity.
    """

    module_key = "scheduler_module"
    collection = "scheduler_collection"
    module_state_fields = {"last_processed_timestamp": int}

    # override
    def run(self, wits_stream: list):
        super().run(wits_stream)

        dataset = self.load_dataset(wits_stream)

        results = []
        for el in dataset:
            if self.should_run_processor(el):
                results = self.run_module(el, results)

        self.save_state()
        self.store_output(self.global_state["asset_id"], results)

    # override
    def should_run_processor(self, event: dict):
        """
        check one wits event and test against the last processed timestamp
        :param event:
        :return:
        """
        timestamp = event.get("timestamp", 0)
        running_frequency = constants.get("{}.{}.running_frequency".format(self.app_key, self.module_key))
        if self.state.get("last_processed_timestamp", 0) + running_frequency <= timestamp:
            # update the last_processed_timestamp
            self.set_state("last_processed_timestamp", timestamp)
            return True

        return False
