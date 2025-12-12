from typing import Dict, Union

import numpy as np

from worker.data import operations
from worker.data.activity import Activity
from worker.data.enums import ChannelStatus, DataStatus


class Channel(float):
    def __new__(cls, value=None, status=None):
        # If only a valid value is passed, data status is automatically set to VALID
        # If None is passed as value, then data status is automatically set to MISSING
        # If both value and data status are passed, then it uses the passed data status
        if value is None:
            return None

        if not isinstance(value, float):
            try:
                value = float(value)
            except ValueError or TypeError:
                return None

        if value is not None and not status:
            status = DataStatus.VALID

        ch = float.__new__(cls, value)
        ch._status = status
        return ch

    @property
    def status(self) -> DataStatus:
        """
        - Status can be valid of missing
        - Data status is only available for non None wits attributes
        - Missing represents a value that has been forward filled or interpolated

        :return: DataStatus
        """
        return self._status


class WITS:
    """
    - Create a wits object by WITS.set_wits(dataset: Union[list, dict])
    - Access any wits data attribute by wits.hole_depth
    - Access any data status of a wits data attribute by wits.hole_depth.status
    - Data status is only available for non None wits attributes
    """

    data = {
        "entry_at": int,
        "hole_depth": Channel,
        "bit_depth": Channel,
        "block_height": Channel,
        "hook_load": Channel,
        "weight_on_bit": Channel,
        "rop": Channel,
        "rotary_rpm": Channel,
        "rotary_torque": Channel,
        "mud_flow_in": Channel,
        "mud_flow_out_percent": Channel,
        "standpipe_pressure": Channel,
        "diff_press": Channel,
        "pump_spm_1": Channel,
        "pump_spm_2": Channel,
        "pump_spm_3": Channel,
        "pump_spm_4": Channel,
        "pump_spm_total": Channel,
        "trip_tank_volume_1": Channel,
        "trip_tank_volume_2": Channel,
        "active_pit_volume": Channel,
        "lag_depth": Channel,
        "state": Activity,
        "boost_pump_flow_in": Channel,
        "annular_back_pressure": Channel,
    }
    metadata = {"drillstring": str}
    spm_channels = ["pump_spm_1", "pump_spm_2", "pump_spm_3", "pump_spm_4"]
    status = {}

    def __init__(self, wits_json: dict = None, **kwargs):
        if not wits_json:
            wits_json = {}

        # Serialize functionality in Worker unpacks all the attributes. If that's how the class is called, repack.
        if kwargs:
            wits_json.update(dict(kwargs))
            wits_json.pop("_wits_", None)

        self.wits_json = wits_json

        data = wits_json.get("data", {})
        data_raw = wits_json.get("data_raw", {})

        metadata = wits_json.get("metadata", {})
        status = wits_json.get("status", {})

        for key in self.data.keys():
            # If type is not Channel or if the value is None, just setattr
            if self.data.get(key) != Channel or data.get(key, None) is None:
                setattr(self, key, data.get(key, None))
                continue

            key_data_status = DataStatus.VALID.value
            # If key is in data_raw, there are 2 possibilities - Missing (Value is None or -999.25) or Overridden
            if key in data_raw:
                key_data_status = DataStatus.OVERRIDDEN.value
                # If key in data_raw and value is null (None or -999.25), then we just setattr None
                if operations.is_null(data_raw.get(key, None)):
                    setattr(self, key, data.get(key, None))
                    continue

            # If type is Channel and (key not in data_raw or (key in data_raw and value is not null))
            setattr(self, key, Channel(data.get(key), DataStatus(data.get(f"{key}_data_status", key_data_status))))

        for key in self.metadata.keys():
            setattr(self, key, metadata.get(key, None))
        for key in self.status.keys():
            setattr(self, key, status.get(key, None))

        setattr(self, "timestamp", wits_json.get("data").get("entry_at"))
        setattr(self, "timestamp_read", wits_json.get("timestamp_read"))

        if getattr(self, "pump_spm_total") is None:
            self.set_pump_spm_total()

        setattr(self, "total_trip_tank_volume", self.get_total_trip_tank_volume())

    def __getattr__(self, item):
        return None

    def __setattr__(self, key, value):
        """
        When trying to set an attribute it automatically tries to typecast the value.
        :param key: key
        :param value: value
        :return:
        """
        if key not in {**self.data, **self.status}.keys():
            self.__dict__[key] = value
            return

        data_type = {**self.data, **self.status}.get(key)
        try:
            if not isinstance(value, Channel):
                value = data_type(value)
            self.__dict__[key] = value
        except TypeError:
            self.__dict__[key] = None
        except ValueError:
            self.__dict__[key] = None

    def __iter__(self):
        yield self

    @classmethod
    def set_wits(cls, dataset: Union[list, dict]):
        """
        Class method to create WITS objects using a dict or a list of dicts

        :param dataset: wits record or a list of wits records
        :return: WITS object or a list of WITS objects
        """
        if isinstance(dataset, dict):
            return cls(dataset)

        if isinstance(dataset, list):
            return [cls(record) for record in dataset]

    def get_as_dict(self) -> [None, dict]:
        """
        Get the wits record as a dictionary

        :return: wits record as a dict
        """
        if not self.wits_json:
            return None

        self.wits_json.pop("data_raw", None)
        self.wits_json["data"] = {key: getattr(self, key) for key in self.data}
        self.wits_json["data"].update(
            {
                f"{key}_data_status": getattr(self, key).status.value
                for key in self.data
                if self.data.get(key) == Channel and getattr(self, key) is not None
            }
        )
        # convert state from Activity type to str
        self.wits_json["data"]["state"] = self.wits_json["data"]["state"].value
        self.wits_json["status"] = {key: getattr(self, key) for key in self.status}

        return self.wits_json

    def get_wits_data(self, columns=None) -> dict:
        """
        Get the data part of the wits record as a dictionary

        :param columns: Specify if you only want a select list of columns
        :return: data part of wits record as a dict
        """
        if not columns:
            data = {key: getattr(self, key) for key in self.data}
            return data

        data = {key: getattr(self, key) for key in columns}
        return data

    def spm_status(self, low_spm_threshold: float) -> [ChannelStatus, None]:
        """
        Get spm status. Compares total of all SPM channels against SPM threshold.

        :param low_spm_threshold: threshold
        :return: None if channels are unavailable, OFF if less than threshold and ON if greater
        """

        # If all SPM channels are empty, return None
        if not any(operations.is_number(getattr(self, spm_channel)) for spm_channel in self.spm_channels):
            return ChannelStatus.MISSING

        if getattr(self, "pump_spm_total") > low_spm_threshold:
            return ChannelStatus.ON

        return ChannelStatus.OFF

    def mud_flow_in_status(self, low_mud_flow_in_threshold: float) -> [ChannelStatus, None]:
        """
        Get flow rate status. Compares mud flow in channel against flow rate threshold.

        :param low_mud_flow_in_threshold: threshold
        :return: None if channel is unavailable, OFF if less than threshold and ON if greater
        """
        if not operations.is_number(self.mud_flow_in):
            return ChannelStatus.MISSING

        if self.mud_flow_in > low_mud_flow_in_threshold:
            return ChannelStatus.ON

        return ChannelStatus.OFF

    def check_channel_availability(self, required_wits_channels: list) -> bool:
        """
        This function checks if all the required channels are available in the wits record

        :param required_wits_channels: List of required channels
        :return: Boolean value. True if all the required channels are available, else False
        """
        return all(
            operations.is_in_and_not_none(self.get_wits_data(required_wits_channels), channel)
            for channel in required_wits_channels
        )

    def set_pump_spm_total(self):
        """This function sets the pump_spm_total attribute value based on individual spm values"""

        pump_spm_total = sum(
            getattr(self, spm_channel)
            for spm_channel in self.spm_channels
            if (getattr(self, spm_channel) and getattr(self, spm_channel) >= 0)
        )

        setattr(self, "pump_spm_total", pump_spm_total)

    def get_total_trip_tank_volume(self) -> float:
        """
        This function returns the total trip tank volume if more than one trip tanks are available

        :return: Total trip tank volume
        """
        ttk1 = self.trip_tank_volume_1 or 0
        ttk2 = self.trip_tank_volume_2 or 0

        return ttk1 + ttk2

    def validate_range(self, channel_range_map: Dict[str, Dict]):
        """
        This method can be used to validate the range of the given channels and apply the proper operation on the data
        :param channel_range_map: a dictionary of channel to operation and range ([min, max]) mapping
        example:
            {
                "mud_flow_out_percent": {"range": [0, 100], "operation": "clip"}
            }
            options for 'operation': ['clip', None]
        :return: None,
        """
        for channel, properties in channel_range_map.items():
            orig_value = getattr(self, channel, None)
            if orig_value is None:
                continue

            valid_range = properties.get("range")
            operation = properties.get("operation", None)

            new_value = None

            if operation == "clip":
                new_value = np.clip(orig_value, *valid_range)
            elif operation is None:
                if valid_range[0] <= orig_value <= valid_range[-1]:
                    new_value = orig_value
            else:
                raise ValueError("Invalid operation provided!")

            setattr(self, channel, new_value)


def serialize(obj: Union[list, WITS]) -> Union[list, dict, None]:
    """
    This function is used to serialize a WITS object or a list of WITS objects.
    Use WITS.set_wits(dataset: Union[list, dict]) to deserialize.

    :param obj: WITS object(s) to serialize.
    :return: return a serialized object
    """
    if isinstance(obj, list):
        s_obj = [each.get_as_dict() for each in obj]
        return s_obj

    if isinstance(obj, WITS):
        s_obj = obj.get_as_dict()
        return s_obj

    return None
