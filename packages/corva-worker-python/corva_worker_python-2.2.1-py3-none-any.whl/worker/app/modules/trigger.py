from worker import constants
from worker.app.modules.__init__ import Module


class Trigger(Module):
    """
    This is an abstract module that needs to be extended by actual modules.
    The idea behind this module is that it runs once for a bunch of data
    only if the the time step is passed.
    """

    module_key = "trigger_module"
    collection = "trigger_collection"
    module_state_fields = {"last_processed_timestamp": int}

    # override
    def run(self, wits_stream: list):
        super().run(wits_stream)

        dataset = self.load_dataset(wits_stream)
        last_wits = dataset[-1]
        results = []
        if self.should_run_processor(last_wits):
            results = self.run_module(last_wits, results)

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
        if self.state.get("last_processed_timestamp", 0) + running_frequency < timestamp:
            # update the last_processed_timestamp
            self.set_state("last_processed_timestamp", timestamp)
            return True

        return False
