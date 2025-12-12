import os
import reprlib


class RollbarMixin(object):
    def __init__(self, *args, **kwargs):
        self.rollbar = kwargs.pop("rollbar", None)
        super().__init__(*args, **kwargs)

    def is_rollbar(self) -> bool:
        """
        To check if rollbar is available or not
        :return: if rollbar is available
        """
        return self.rollbar and self.rollbar.SETTINGS.get("enabled")

    def track_message(self, message: str, level: str):
        """
        To send a message to rollbar
        :param message:
        :param level: any of the following levels:
        ['critical', 'error', 'warning', 'info', 'debug', 'ignored']
        :return:
        """
        # Levels:
        if not self.is_rollbar():
            print(f"{level} - {message}")
            return

        level = level.lower()

        self.rollbar.report_message(message, level)

    def track_error(self, message: str = None):
        if not self.is_rollbar():
            raise

        self.rollbar.report_exc_info(extra_data=message, level="error")


def payload_handler(payload: dict, **kw) -> dict:  # kw is currently unused
    """
    This is a rollbar payload handler which will be called on every payload being sent to rollbar
    This handler has to be added to rollbar instance after init

    Rollbar already applies a shortening transform to the payload using reprlib and custom sizes defined in rollbar init
    But it somehow seems to miss nested lists which is a usual format in our apps using corva-worker-python
    This payload handler applies the same reprlib to the lists missed by rollbar's shortener

    Use like -> rollbar.events.add_payload_handler(payload_handler)
    To pause trimming set REDUCED_ROLLBAR_PAYLOAD to False or false in env variables

    :param payload: Payload automatically captured based on exc, args and locals
    :param kw:
    :return: Trimmed payload
    """
    reduced_rollbar_payload_flag = os.getenv("REDUCED_ROLLBAR_PAYLOAD", "true").lower()

    # If REDUCED_ROLLBAR_PAYLOAD is set to False or false in env variables, trimming will be paused
    if reduced_rollbar_payload_flag == "false":
        return payload

    try:
        payload_frames = payload["data"]["body"]["trace"].pop("frames", [])
    except KeyError:
        return payload

    # All the locals are nested inside frames.
    # Smartly payload reduce size
    for frame in payload_frames:
        local_vars = frame.get("locals", {})

        # Instantiating repr from reprlib. Using this to trim nested datasets
        _repr = reprlib.Repr()

        # Setting custom max sizes for dict and list
        setattr(_repr, "maxdict", 10)
        setattr(_repr, "maxlist", 2)

        for key, value in local_vars.items():
            # Applying trim to only dicts and lists.
            # If there are other nested data types, they will be trimmed based on default repr limits
            if isinstance(value, (dict, list)):
                local_vars[key] = _repr.repr(value)

    payload["data"]["body"]["trace"]["frames"] = payload_frames
    return payload
