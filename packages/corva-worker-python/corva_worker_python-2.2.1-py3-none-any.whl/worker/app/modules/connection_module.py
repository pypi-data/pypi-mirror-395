from worker.app.modules.activity_module import ActivityModule


class ConnectionModule(ActivityModule):
    """
    This is an abstract module that needs to be extended by actual modules.
    An example of this module would be running an app after a connection occur.
    """

    module_key = "connection_module"
    collection = "connection_collection"

    # override
    def process_module_state(self, state):
        state = super().process_module_state(state)

        if self.global_state.get("reset", False):
            # todo
            pass

        return state
