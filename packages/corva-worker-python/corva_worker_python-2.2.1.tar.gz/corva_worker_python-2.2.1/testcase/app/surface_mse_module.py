from typing import List

import numpy as np

from testcase.app.app_constants import constants
from worker import API
from worker.app import TimeActivityModule
from worker.data.operations import nanround
from worker.exceptions import Misconfigured


class SurfaceMSE(TimeActivityModule):
    module_key = "mse"
    collection = "drilling-efficiency.mse"

    module_state_fields = {
        "last_processed_timestamp": int,
        "last_exported_timestamp": int,
        "last_exported_depth": float,
        "active_string_type": str,
        "active_string_id": str,
        "drillstring_number": float,
    }

    # override
    def run_module(self, event, beginning_results):
        self.results = beginning_results

        valid_activities = constants.get(f"drilling-efficiency.{self.module_key}.drilling-activity")
        last_exported_timestamp = self.state.get("last_exported_timestamp", -1)

        valid_records = [
            r
            for r in event
            if r.get("data", {}).get("state", "") in valid_activities and r["timestamp"] > last_exported_timestamp
        ]
        if not valid_records:
            return self.results

        valid_timestamps = [r["timestamp"] for r in valid_records]

        drillstring = get_external_data(wits=valid_records[-1])
        bit_size = extract_bit_size(drillstring)

        updating_frequency_duration = constants.get(f"drilling-efficiency.{self.module_key}.export-duration")

        if last_exported_timestamp <= 0:
            last_exported_timestamp = min(valid_timestamps) - updating_frequency_duration

        max_timestamp = max(valid_timestamps)

        time_check = last_exported_timestamp
        while (time_check + updating_frequency_duration) <= max_timestamp:
            start = time_check  # start of the interval
            end = start + updating_frequency_duration  # end of the interval

            segment_data = [r for r in valid_records if start <= r.get("timestamp", 0) <= end]
            if not segment_data:
                continue

            mse = self.compute_average_mse(segment_data, bit_size)

            segment_last_hole_depth = segment_data[-1].get("data", {}).get("hole_depth")
            output = self.build_empty_output(segment_data[-1])
            output["data"] = {
                "surface_mse": nanround(mse, decimal_places=1),  # in psi
                "depth": segment_last_hole_depth,
            }

            self.results.append(output)

            self.set_state("last_exported_timestamp", time_check)
            self.set_state("last_exported_depth", segment_last_hole_depth)
            time_check = end

        self.debug(self.global_state.get("asset_id"), self.results)
        return self.results

    def compute_average_mse(self, wits_records: List[dict], bit_size: float) -> float:
        """
        Compute MSE for a list of drilling wits records
        :param wits_records: WITS records
        :param bit_size: bit size in INCH
        :return: MSE in PSI
        """
        channels = ["weight_on_bit", "rotary_rpm", "rotary_torque", "rop"]
        data = {k: [] for k in channels}
        for wits in wits_records:
            wits_data = wits.get("data", {})
            for ch in channels:
                data[ch].append(wits_data.get(ch))
        ave_data = {k: np.nanmean(data[k]) for k in channels}

        mse = compute_mse(
            bit_size,
            rop=ave_data["rop"],
            rpm=ave_data["rotary_rpm"],
            wob=ave_data["weight_on_bit"],
            torque=ave_data["rotary_torque"],
        )

        return mse


def get_external_data(wits: dict) -> dict:
    """
    TODO
    :param wits:
    :return:
    """
    drillstring__id = wits.get("metadata", {}).get("drillstring", None)
    if drillstring__id is None:
        raise Misconfigured(f"Wrong drillstring _id ({drillstring__id})!")

    worker = API()
    drillstring = worker.get_by_id(
        path="/v1/data/corva/", **{"collection": "data.drillstring", "id": drillstring__id}
    ).data  # dict
    return drillstring


def extract_bit_size(drillstring: dict) -> float:
    """
    Get the bit size from a drillstring.
    :param drillstring: the dictionary holding the drillstring info
    :return: bit size
    """
    components = drillstring.get("data", {}).get("components", [])
    bit = list(filter(lambda x: x["family"] == "bit", components))
    if not bit:
        raise Misconfigured(f"No bit in the drillstring: {drillstring}")
    return bit[0].get("size", None)


def compute_mse(bit_size, rop, rpm, wob, torque, factor=0.35):
    """
    Compute the MSE
    :param bit_size: bit size in INCH
    :param rop: WITS ROP in FOOT/HOUR
    :param rpm: WITS Rotary RPM in RPM
    :param wob: WITS Weight on Bit in KIPS
    :param torque: WITS Rotary Torque in K-FT-LBF
    :param factor: Based on the recommendation of Dupriest et. al. paper
    (Dupriest, Fred E., and William L. Koederitz. "Maximizing drill rates
     with real-time surveillance of mechanical specific energy."
     SPE/IADC Drilling Conference. Society of Petroleum Engineers, 2005.)
      a factor of <b>0.35</b> is applied for surface MSE.
    :return: MSE in PSI
    """
    bit_area = np.pi / 4 * bit_size**2

    if rop < 0:
        return None

    mse = factor * ((wob / bit_area) + (120 * np.pi * rpm * 1000 * torque) / (bit_area * rop))
    return mse
