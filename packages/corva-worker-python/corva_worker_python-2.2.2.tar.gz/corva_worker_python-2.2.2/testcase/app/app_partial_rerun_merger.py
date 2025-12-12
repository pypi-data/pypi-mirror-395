from worker.partial_rerun_merge.merge import PartialRerunMerge
from worker.partial_rerun_merge.models import CollectionMergingModel, MergingSchemaModel

collections = [{"collection_name": "drilling-efficiency.mse"}]

collections = [CollectionMergingModel(**collection) for collection in collections]


SCHEMA = MergingSchemaModel(collections=collections, modules=None)


class AppPartialRerunMerger(PartialRerunMerge):
    def __init__(self, app, api, logger):
        # adding the required modules to the schema
        schema = SCHEMA
        # app itself has a cache so it needs to be added to the schema as well
        schema.modules = [app] + app.get_active_modules()

        super().__init__(schema, api, logger)
