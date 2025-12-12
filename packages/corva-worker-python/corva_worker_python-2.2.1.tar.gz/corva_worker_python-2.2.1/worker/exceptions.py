class CorvaException(Exception):
    pass


class Misconfigured(Exception):
    pass


class APIError(CorvaException):
    pass


class NotFound(CorvaException):
    pass


class Forbidden(CorvaException):
    pass


class MissingConfigError(Exception):
    pass


class EventFormatError(Exception):
    pass
