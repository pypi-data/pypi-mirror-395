# The modules of this files are used for (de)serialization of any object
#
# The only things you need to do is to add '@serialization' decorator to
# the class. If the class is an enum that's enough. For other class types,
# you need to specify the variables that need to be serialized as a dict:
# variable name as key -> variable type as value
# the name of it should be 'SERIALIZED_VARIABLES'
#
# At the end you can use:
# 'obj2json' to serialize, and
# 'json2obj' to deserialize
#


import json
from enum import Enum
from typing import Union

from worker.data.two_way_dict import TwoWayDict

# This registry object keeps a list of classes that subscribed to serialization.
registry = TwoWayDict()


# This method is used as a decorator of the class that wants to be serialized
def serialization(cls):
    registry[cls] = f"_{cls.__name__.lower()}_"
    return cls


class Encoder(json.JSONEncoder):
    """
    This class is used to encode: object --> json string
    """

    def default(self, obj):
        cls = obj.__class__

        if cls in registry:
            cls_tag = registry[cls]
            d = {cls_tag: True}

            # enum types
            if issubclass(cls, Enum):
                d["name"] = obj.name
                return d

            # class instances
            # 1. classes with serialize method
            if hasattr(obj, "serialize"):
                d.update(obj.serialize())
                return d

            # 2. classes without it
            for var_name in cls.SERIALIZED_VARIABLES.keys():
                value = getattr(obj, var_name)
                d[var_name] = value
            return d

        return json.JSONEncoder.default(self, obj)


def obj2json(obj: object, output_format=str) -> Union[str, dict]:
    """
    Convert an object to JSON. The object class should have been decorated
    with serialization function.
    :param obj:
    :param output_format: str, or dict
    :return:
    """
    output = json.dumps(obj, cls=Encoder)
    if output_format == str:
        return output
    if output_format == dict:
        return json.loads(output)
    raise TypeError("output_format should be str or dict.")


def _set_from_json(cls, data: str):
    if isinstance(data, str):
        data = json.loads(data)

    # getitem of an enum is the best way of de-serializing it
    if issubclass(cls, Enum):
        return cls[data["name"]]

    return cls(**data)


def _json_to_obj_hook(j_str):
    cls_tags = [tag for tag in registry.values() if isinstance(tag, str)]
    for tag in cls_tags:
        if tag in j_str:
            cls = registry.get(tag)
            return _set_from_json(cls, j_str)

    return j_str


def json2obj(json_str: Union[str, dict]):
    if json_str is None:
        return None

    if not isinstance(json_str, (str, dict)):
        raise TypeError(f"Wrong json format: {type(json_str)}. Acceptable formats are str and dict.")

    if isinstance(json_str, dict):
        json_str = json.dumps(json_str)

    return json.loads(json_str, object_hook=_json_to_obj_hook)
