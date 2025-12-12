from testcase.app.app_partial_rerun_merger import AppPartialRerunMerger
from testcase.app.drilling_efficiency_app import DrillingEfficiency
from worker.data.api import API
from worker.event.event_handler import EventHandler
from worker.mixins.logging import Logger
from worker.state import RedisHandler

REDIS_CONNECTION = None


def lambda_handler(event, context):
    """
    This function is the main entry point of the AWS Lambda function
    :param event: a scheduler or kafka event
    :param context: AWS Context
    :return:
    """
    global REDIS_CONNECTION
    REDIS_CONNECTION = RedisHandler.setup_existing_connection(REDIS_CONNECTION)

    app = DrillingEfficiency()

    merger = AppPartialRerunMerger(app, API(), Logger.get_logger())

    event_handler = EventHandler(app, merger)
    event_handler.process(event)
