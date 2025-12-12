from itertools import groupby

from worker import constants
from worker.app.modules.__init__ import Module
from worker.data import operations
from worker.data.operations import get_config_by_id


class ActivityModule(Module):
    """
    This is an abstract base module that needs to be extended by an actual module.
    """

    # module_key is used for redis access and state of this module
    module_key = "activity_module"
    collection = "activity_module_collection"

    # override
    def run(self, wits_stream: list):
        """
        :param wits_stream: a wits stream event
        :return:
        """
        super().run(wits_stream)

        dataset = self.load_dataset(wits_stream)

        # this guarantees every group has the same config
        config_grouped_dataset = self.group_data_stream_based_on_config(dataset)

        for group in config_grouped_dataset:
            results = self.check_for_string_change(group)

            if self.should_run_processor(group):
                results = self.run_module(group, results)

            self.save_state()
            self.store_output(self.global_state["asset_id"], results)

    @staticmethod
    def group_data_stream_based_on_config(dataset):
        """Group our datasets by the metadata such as drillstring, and then reflatten to be a list of lists
        for processing"""

        groups = groupby(dataset, lambda x: x["metadata"])
        grouped_dataset = [list(dataset) for group, dataset in groups]

        return grouped_dataset

    # override
    def should_run_processor(self, event):
        running_string = constants.get("{}.{}.running-string".format(self.app_key, self.module_key))
        if running_string and self.state.get("active_string_type", "") in running_string:
            return True

        return False

    def check_for_string_change(self, data):
        """
        To check if the active string in the wellbore has been changed and
        export proper text to the output.
        Note that the last_exported_timestamp is not set here.
        Note that all the configs of this data have the same config properties.
        :param data:
        :return:
        """

        previous_string = self.state.get("active_string_id", "")
        running_string = constants.get("{}.{}.running-string".format(self.app_key, self.module_key))
        reset_config = constants.get("{}.{}.reset-config".format(self.app_key, self.module_key))

        if not running_string:
            return []

        if not data:
            return []

        first_wits = data[0]
        drillstring_id = first_wits.get("metadata", {}).get("drillstring", None)
        casing_id = first_wits.get("metadata", {}).get("casing", None)

        if drillstring_id:
            active_string_type = "drillstring"
            active_string_id = drillstring_id
        elif casing_id:
            active_string_type = "casing"
            active_string_id = casing_id
        else:
            active_string_type = None
            active_string_id = None

        if previous_string == active_string_id:
            return []

        main_structure = self.build_empty_output(first_wits)

        warning = None

        if active_string_type in running_string:
            if active_string_type not in reset_config:
                return []
        else:
            message = "This module does not run while {} is the active string in the well.".format(active_string_type)
            warning = {"message": message}

        res = self.configure_output_at_config_change(main_structure, active_string_type, active_string_id, warning)

        return [res]

    def configure_output_at_config_change(self, main_structure, active_string_type, active_string_id, warning=None):
        extra_elements = self.create_output_for_new_config(active_string_type, active_string_id)
        main_structure["data"] = operations.merge_dicts(main_structure["data"], extra_elements)

        if warning:
            main_structure["data"] = operations.merge_dicts(main_structure["data"], {"warning": warning})

        return main_structure

    def create_output_for_new_config(self, active_string_type, active_string_id):
        self.set_state("active_string_type", active_string_type)
        self.set_state("active_string_id", active_string_id)

        drillstring_number = None
        if active_string_type == "drillstring":
            drillstring = get_config_by_id(active_string_id, collection="data.drillstring")

            if drillstring:
                drillstring_number = drillstring.get("data", {}).get("id", None)

        self.set_state("drillstring_number", drillstring_number)

        return self.get_config_properties()

    def get_config_properties(self):
        properties = {
            "active_string_type": self.state.get("active_string_type", ""),
            "active_string_id": self.state.get("active_string_id", ""),
            "drillstring_number": self.state.get("drillstring_number", None),
        }

        return properties
