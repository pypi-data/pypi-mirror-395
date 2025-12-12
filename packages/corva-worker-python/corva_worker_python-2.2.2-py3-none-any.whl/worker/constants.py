"""
this constants module can be overridden by your new constants module by importing
the this module and updating it like this:
    from worker import constants
    constants.update({
        ...
    })
"""

from worker.data.operations import get_data_by_path

parameters = {
    "global": {
        "app-name": "my-app",
        "app-key": "my-app-key",
        "event-type": "scheduler",
        "query-limit": 1000,
    },
}


def get(path, default=None):
    """
    Get the value at the specified path in the parameters dictionary.

    Args:
        path (str): The path to the value to retrieve.
        default (Any, optional): The default value to return if the path
            is not found. Defaults to None.

    Returns:
        Any: The value at the specified path, or the default value
            if the path is not found.
    """
    return get_data_by_path(data=parameters, path=path, default=default)


def update(additional_parameters):
    """
    The purpose of this method is to update the existing parameters data
    with the provided additional parameters. Note that the globals will
    be replaced if the additional parameters contains global node.
    :param additional_parameters:
    :return:
    """
    _globals = parameters.pop("global")
    additional_globals = additional_parameters.pop("global", {})
    _globals.update(additional_globals)
    parameters.update(additional_parameters)
    if _globals:
        parameters["global"] = _globals
