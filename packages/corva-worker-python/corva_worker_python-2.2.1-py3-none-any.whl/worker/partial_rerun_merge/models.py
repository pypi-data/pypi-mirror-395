"""
This file contains the models for the configurations for
the collections and cache updates.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from worker.data.enums import CollectionRecordDataScope, CountOfCollectionRecord


@dataclass
class CollectionMergingModel:
    """
    A model representing a collection of records.

    Attributes:
        collection_name (str):
            The name of the collection.

        record_scope (Optional[CollectionRecordDataScope], optional):
            The scope of the records to be included in the collection.
            Defaults to CollectionRecordDataScope.CURRENT.

        count (Optional[CountOfCollectionRecord], optional):
            The count of records to be included in the collection.
            Defaults to None.

        merging_method (Optional[str], optional):
            The name of the method used to merge the records in the collection.
            Defaults to None.
    """

    collection_name: str
    record_scope: Optional[CollectionRecordDataScope] = CollectionRecordDataScope.CURRENT
    count: Optional[CountOfCollectionRecord] = None
    merging_method: Optional[str] = None


@dataclass
class MergingSchemaModel:
    """
    A class representing the schema for merging collections and modules.

    Attributes:
        collections (List[CollectionMergingModel]): A list of
            CollectionMergingModel objects representing the collections
            to be merged.
        modules (List): A list of module objects representing the modules
            that their cache needs to be updated.
    """

    collections: List[CollectionMergingModel] = field(default_factory=list)
    modules: Optional[List] = None


class RerunMergeCacheUpdater:
    """
    A generic model representing a cache update for a module.
    A module just need to override the `update_cache` method.
    """

    @classmethod
    def update_cache(cls, merger: "PartialRerunMerge") -> None:
        """
        Updates the cache with the given rerun mode, original asset ID, and rerun asset ID.

        Args:
            merger: The merger object.
        """
        raise NotImplementedError

    @classmethod
    def default_updater(cls, original_asset_cache: dict, rerun_asset_cache: dict) -> dict:
        """
        The default cache updater.

        Args:
            original_asset_cache: The original asset cache.
            rerun_asset_cache: The rerun asset cache.

        Returns:
            The updated cache.
        """
        # Remove the asset ID and company ID from the rerun asset cache.
        rerun_asset_cache.pop("asset_id", None)
        rerun_asset_cache.pop("company_id", None)

        original_asset_cache.update(rerun_asset_cache)

        return original_asset_cache
