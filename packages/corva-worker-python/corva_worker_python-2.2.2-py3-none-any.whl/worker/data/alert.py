import simplejson as json

from worker import API
from worker.data.json_encoder import JsonEncoder
from worker.mixins.logging import LoggingMixin
from worker.mixins.rollbar import RollbarMixin


class Alert(LoggingMixin, RollbarMixin):
    """
    Alert class can be used to trigger alerts from a data app.
    An event based alert has to be created on the Corva UI with a unique identifier.

    How to use:
    1. Create an instance of Alert with the same unique identifier and asset_id.
    2. Call trigger_alert and pass the required parameters to trigger the alert.
    3. To trigger an alert on Corva, the well must be active and visible to the user. (Current rules)
    """

    def __init__(self, asset_id: int, identifier: str, last_trigger_timestamp=None, *args, **kwargs):
        self.asset_id = asset_id
        self.identifier = identifier
        self.last_trigger_timestamp = last_trigger_timestamp

        super().__init__(*args, **kwargs)

    def trigger_alert(self, timestamp: int, timestamp_read: int, context: dict):
        """
        Function used to trigger the alert for the unique identifier.

        :param timestamp: timestamp at which the event for the alert is detected
        :param timestamp_read: timestamp at which the wits record was read by the source app
        :param context: A dict of data to be sent to the alerts engine
        :return:
        """

        context = context or {}
        context.update(
            {
                "identifier": self.identifier,
                "asset_id": self.asset_id,
                "timestamp": timestamp,
                "timestamp_read": timestamp_read,
            }
        )

        api = API()
        try:
            trigger = api.post(
                "/v1/alerts/definitions/trigger/", data=json.dumps(context, cls=JsonEncoder, ignore_nan=True)
            ).data
            self.debug(self.asset_id, f"Triggered alert with context -> {context} and received response {trigger}")
            self.last_trigger_timestamp = timestamp

            return trigger
        except Exception as ex:
            message = f"Error while triggering alert for context {context} with exception {ex}"
            self.debug(self.asset_id, f"Failed to trigger alert with context -> {context}")
            self.track_error(message)


class Alerter:
    alerter = None
    asset_id = None

    @classmethod
    def set_asset_id(cls, asset_id):
        cls.asset_id = asset_id

    @classmethod
    def get_alerter(cls):
        if cls.alerter is None:
            cls.alerter = Alert(0, "")

        return cls.alerter

    @classmethod
    def trigger_alert(
        cls, identifier: str, message: str, timestamp: int = None, timestamp_read: int = None, context: dict = None
    ):
        if not cls.asset_id:
            return

        context = context or {}
        context.update({"message": message})

        cls.get_alerter().asset_id = cls.asset_id
        cls.get_alerter().identifier = identifier
        cls.get_alerter().trigger_alert(timestamp, timestamp_read, context)
