from worker.app import TimeActivityModule


class DisableModule(TimeActivityModule):
    """
    The purpose of this module is to check the disable functionality
    by turing it off from the testing section.
    """

    module_key = "mse"
    collection = "another-module.collection"
