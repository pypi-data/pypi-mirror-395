import datetime
import os

from worker.data.operations import is_number


class LoggingMixin(object):
    LOGGING_LEVELS = [
        "all",  # Show all messages
        "debug",  # Show debug, info, warnings, errors, and fatal messages (Equal to all)
        "info",  # Show info, warnings, errors, and fatal messages
        "warn",  # Show warnings, errors, and fatal messages
        "error",  # Show errors and fatal messages
        "fatal",  # Show only fatal messages
        "off",  # No messages
    ]

    def __init__(self, *args, **kwargs):
        self.logging_level = os.getenv("LOGGING_LEVEL", "info").lower()
        self.logging_asset_id = os.getenv("LOGGING_ASSET_ID", 0)

        if self.logging_level not in self.LOGGING_LEVELS:
            self.logging_level = "off"

        if is_number(self.logging_asset_id):
            self.logging_asset_id = int(self.logging_asset_id)

        super().__init__(*args, **kwargs)

    def all(self, asset_id, text):
        self.call("all", asset_id, text)

    def debug(self, asset_id, text):
        self.call("debug", asset_id, text)

    def info(self, asset_id, text):
        self.call("info", asset_id, text)

    def warn(self, asset_id, text):
        self.call("warn", asset_id, text)

    def error(self, asset_id, text):
        self.call("error", asset_id, text)

    def fatal(self, asset_id, text):
        self.call("fatal", asset_id, text)

    def off(self, asset_id, text):
        pass

    def call(self, method, asset_id, text):
        if method == "off":
            return

        method_check = str(method) in self.LOGGING_LEVELS[self.LOGGING_LEVELS.index(self.logging_level) :]
        if not method_check:
            return

        asset_id_check = (asset_id == self.logging_asset_id) or (self.logging_asset_id == "all")
        if not asset_id_check:
            return

        self.log(asset_id, method, text)

    @staticmethod
    def log(asset_id, method="LOG", text=""):
        if not method:
            method = "LOG"

        utc_time = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")
        print(f"{utc_time} | {method.upper()} | asset_id_{asset_id} | {text}")


class Logger:
    logger = None
    asset_id = None

    @classmethod
    def set_asset_id(cls, asset_id):
        cls.asset_id = asset_id

    @classmethod
    def get_logger(cls):
        if cls.logger is None:
            cls.logger = LoggingMixin()

        return cls.logger

    @classmethod
    def all(cls, text):
        cls.get_logger().call("all", cls.asset_id, text)

    @classmethod
    def debug(cls, text):
        cls.get_logger().call("debug", cls.asset_id, text)

    @classmethod
    def info(cls, text):
        cls.get_logger().call("info", cls.asset_id, text)

    @classmethod
    def warn(cls, text):
        cls.get_logger().call("warn", cls.asset_id, text)

    @classmethod
    def error(cls, text):
        cls.get_logger().call("error", cls.asset_id, text)

    @classmethod
    def fatal(cls, text):
        cls.get_logger().call("fatal", cls.asset_id, text)

    @classmethod
    def off(cls, asset_id, text):
        pass

    @classmethod
    def log(cls, text):
        cls.get_logger().log(cls.asset_id, "LOG", text)
