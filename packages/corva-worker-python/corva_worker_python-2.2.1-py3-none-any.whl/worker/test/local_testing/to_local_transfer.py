import argparse
import os
from functools import cached_property

import simplejson as json
from tqdm import tqdm

from worker.data import operations
from worker.data.json_encoder import JsonEncoder
from worker.mixins.logging import LoggingMixin

API_DATA_PATH = "/v1/data/corva/"
API_ASSET_PATH = "/v1/assets/"


def generate_transfer_parser():
    """
    Creating the supporting arguments
    :return:
    """
    parser = argparse.ArgumentParser(description="Run your tests locally on an asset.")
    parser.add_argument(
        "-v",
        "--source_environment",
        "--env",
        type=str,
        required=True,
        help="source environment, options: 'qa', 'staging', 'production'",
    )
    parser.add_argument("-a", "--source_asset_id", "--id", type=int, required=True, help="set source asset_id")
    parser.add_argument(
        "-s",
        "--start_timestamp",
        "--start",
        type=int,
        required=False,
        default=None,
        help="start timestamp for the main collections to be copied over",
    )
    parser.add_argument(
        "-e",
        "--end_timestamp",
        "--end",
        type=int,
        required=False,
        default=None,
        help="end timestamp for the main collections to be copied over",
    )
    parser.add_argument(
        "-c",
        "--config_collections",
        "--config",
        type=json.loads,
        required=False,
        default=None,
        help="setting a new config collection list that override the existing one",
    )
    parser.add_argument(
        "-m",
        "--main_collections",
        "--main",
        type=json.loads,
        required=False,
        default=None,
        help="setting a new main collection list that override the existing one",
    )
    return parser


class ToLocalTransfer(LoggingMixin):
    # config collection: this can be modified in __init__
    CONFIG_COLLECTIONS = [
        "data.surface-equipment",
        "data.actual_survey",
        "data.plan_survey",
        # in the following collections the setting timestamps need to be removed
        # but for the purpose of this test analysis is not important.
        "data.casing",
        "data.drillstring",
        "data.mud",
        # not required for most of the cases
        # "data.formations",
        # "data.pressure-gradient",
        # "data.npt-events",
        # "data.costs",
        # "data.well-sections",
    ]

    # collections other than configs: this can be modified in __init__
    MAIN_COLLECTIONS = ["wits"]

    def __init__(self, args):
        super().__init__()

        self.source_env = None
        self.source_asset_id = None
        self.source_company_id = None

        self.local_env = "local"
        self.local_asset_id = None

        # this is used to avoid copying configs if it is not a new well
        self.is_new_well = True

        self.app_name = os.getenv("APP_NAME", "LocalTesting")

        # The purpose of this variable is to change the config _ids
        # For instance when the wits records are copied over to local
        # the drillstring node under metadata is still referring to source
        # _id so keeping a mapping is required to replace the _ids.
        # In addition this variable is stored on local redis.
        self.config_id_mapper = {}

        self.start_timestamp = None
        self.end_timestamp = None

        if args is None:
            parser = generate_transfer_parser()
            args = parser.parse_args()

        self.initialize(args)

    def initialize(self, args):
        if args.config_collections:
            self.CONFIG_COLLECTIONS = args.config_collections

        if args.main_collections:
            self.MAIN_COLLECTIONS = args.main_collections

        self.source_env = args.source_environment
        self.source_asset_id = args.source_asset_id

        self.start_timestamp = args.start_timestamp
        self.end_timestamp = args.end_timestamp

    def run(self):
        self.setup_local_well()
        self.store_config_data()
        self.store_other_collections()

    @cached_property
    def source_api_worker(self):
        return operations.setup_api_worker(self.source_env, self.app_name)

    @cached_property
    def local_api_worker(self):
        return operations.setup_api_worker(self.local_env, self.app_name)

    @cached_property
    def local_redis_worker(self):
        return operations.setup_redis_worker(self.local_env)

    def _get_well_properties(self):
        path = "%s?ids[]=%s" % (API_ASSET_PATH, self.source_asset_id)

        well_properties = self.source_api_worker.get(path=path)
        if well_properties.count != 1:
            raise Exception(f"Count mismatch: there should be only one asset! {well_properties.count} found!")

        well_properties = well_properties.data[0]

        if well_properties["asset_type"] != "well":
            raise Exception("Not a well")

        self.well_name = well_properties["name"]
        self.source_company_id = well_properties["company_id"]

    def setup_local_well(self):
        """
        Set up the local well. If the well is not already setup, a new one will be created.
        :return:
        """
        self._get_well_properties()

        path = "%s?order=asc&page=1&per_page=100&search=%s&sort=name&types[]=well" % (API_ASSET_PATH, self.well_name)
        wells = self.local_api_worker.get(path=path)

        found = False
        if wells.count >= 1:
            well = wells.data[0]
            well_name2 = well["name"]
            if self.well_name == well_name2:
                found = True
                print("Found local asset!")

        if not found:
            print("Well not found! Trying to create a new asset ...")
            data = {
                "name": self.well_name,
                "parent_asset_id": None,
                "company_id": 1,
                "visibility": "visible",
                "asset_type": "well",
                "type": "Asset::Well",
            }
            data_json = json.dumps(data, cls=JsonEncoder, ignore_nan=True)
            well = self.local_api_worker.post(path=API_ASSET_PATH, data=data_json).data
            print("Well is created!")

        self.is_new_well = not found
        self.local_asset_id = well["id"]
        print(f"Local asset_id={self.local_asset_id}")

    def store_config_data(self):
        """
        Store the config collection data into local database
        :return:
        """
        if not self.is_new_well:
            print("Not a new well.")
            config_id_mapper = self.local_redis_worker.get(self.get_config_mapper_redis_key())
            if config_id_mapper:
                self.config_id_mapper = json.loads(config_id_mapper)
                print("Copying configs are skipped.")
                return

        # maps the source to local ids in a dict of dicts in the format {collection:{source_id: local_id}}
        config_id_mapper = {}

        # get records
        print("Copying configs to local ...")
        print(f"{'Collection':30} {'Count':10} {'Post':10} ")
        print(f"{'-' * 30:30} {'-' * 10:10} {'-' * 10:10} ")

        count_records = 0
        for col in self.CONFIG_COLLECTIONS:
            records = []
            print(f"{col:30} ", end="")
            col_data = self.source_api_worker.get(
                path=API_DATA_PATH, collection=col, asset_id=self.source_asset_id, limit=10000
            )
            print(f"{col_data.count:>10} ", end="")
            if col_data.count < 1:
                print()
                continue

            records.extend(col_data.data)

            source_ids = [record["_id"] for record in records]

            for record in records:
                record["company_id"] = 1
                record["asset_id"] = self.local_asset_id
                record.pop("_id", None)

            # post
            results = self.local_api_worker.post(
                path=API_DATA_PATH, data=json.dumps(records, cls=JsonEncoder, ignore_nan=True)
            )
            print(f"{'successful':10} ", end="\n")

            local_ids = results.data["ids"]
            count_records += len(local_ids)

            if len(source_ids) != len(local_ids):
                raise IndexError(
                    f"Number of source ids ({len(source_ids)}) does not match local ids ({len(local_ids)})"
                )

            collection_id_mapper = {source_ids[i]: local_ids[i] for i in range(len(source_ids))}
            config_id_mapper[col] = collection_id_mapper

        print(f"{count_records} records are posted!")
        self.debug(self.local_asset_id, f"id Mapper: {config_id_mapper}")

        self.config_id_mapper = config_id_mapper
        self.local_redis_worker.set(
            self.get_config_mapper_redis_key(), json.dumps(self.config_id_mapper, cls=JsonEncoder, ignore_nan=True)
        )

    def store_other_collections(self, show_progress: bool = True):
        """
        Store the other config data on local
        :param show_progress: to show progress bar or not
        :return:
        """
        collections = self.MAIN_COLLECTIONS

        # to remove duplicate collections
        collections = list(set(collections))

        start_timestamp = self.start_timestamp
        end_timestamp = self.end_timestamp

        for col in collections:
            # Finding the start and end if not available.
            if not start_timestamp:
                res = self.source_api_worker.get(
                    path=API_DATA_PATH, collection=col, asset_id=self.source_asset_id, sort="{timestamp:+1}", limit=1
                )

                if res.count < 1:
                    continue
                start_timestamp = res.data[0].get("timestamp")

            if not end_timestamp:
                res = self.source_api_worker.get(
                    path=API_DATA_PATH, collection=col, asset_id=self.source_asset_id, sort="{timestamp:-1}", limit=1
                )
                end_timestamp = res.data[0].get("timestamp")

            res = self.local_api_worker.get(
                path=API_DATA_PATH, collection=col, asset_id=self.local_asset_id, sort="{timestamp:-1}", limit=1
            )
            if res.count > 0:
                ts = res.data[0].get("timestamp", 0)
            else:
                ts = start_timestamp - 1

            print(f"'{col}' collection, Source Range: [{start_timestamp}, {end_timestamp}], Local Start: {ts}")

            limit = 3600 if col == "wits" else 100

            pbar = tqdm(total=100, ncols=100, disable=not show_progress)

            proceed = True
            while proceed:
                query = "{timestamp#gt#%s}AND{timestamp#lte#%s}" % (ts, end_timestamp)

                res = self.source_api_worker.get(
                    path=API_DATA_PATH,
                    collection=col,
                    asset_id=self.source_asset_id,
                    query=query,
                    sort="{timestamp:+1}",
                    limit=limit,
                )

                count = res.count
                if count < 1:
                    break

                records = res.data

                data_str = json.dumps(records)
                data_str = data_str.replace('"company_id": %s' % self.source_company_id, '"company_id": %s' % 1)
                data_str = data_str.replace(
                    '"asset_id": %s' % self.source_asset_id, '"asset_id": %s' % self.local_asset_id
                )
                if col == "wits":
                    for config_name, mapped_ids in self.config_id_mapper.items():
                        for id_source, id_local in mapped_ids.items():
                            data_str = data_str.replace(id_source, id_local)

                records = json.loads(data_str)

                for record in records:
                    record.pop("_id", None)

                res = self.local_api_worker.post(path=API_DATA_PATH, data=json.dumps(records))

                pbar_added = round((records[-1]["timestamp"] - ts) / (end_timestamp - start_timestamp) * 100)
                pbar.update(pbar_added)

                ts = records[-1]["timestamp"]

            pbar.update(100 - pbar.n)

    def get_config_mapper_redis_key(self):
        return "%s-config_id_mapper" % self.local_asset_id
