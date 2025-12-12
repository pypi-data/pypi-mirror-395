import requests


class FedKitException(Exception):
    """Base exception for FedKit."""


class RemoteActorError(FedKitException):
    """An error while trying to access properties on a remote actor."""

    pass


class ParseError(FedKitException):
    """Generic error while parsing something."""


class ParseJSONError(ParseError):
    """An error while parsing JSON."""


class ParseUTF8Error(ParseError):
    """An error while parsing UTF-8."""


class ParseActivityError(ParseError):
    """An error while parsing an activity."""


class InvalidActivityError(FedKitException):
    """An error while parsing an activity."""


class FetchError(FedKitException):
    """
    An Error that occured while fetching a URL.
    """

    def __init__(self, url: str, r: requests.Response | None = None) -> None:
        resp_part = ""
        if r:
            resp_part = f", got HTTP {r.status_code}: {r.text}"
        self.message = f"Failed to fetch {url}{resp_part}"
        self.resp = r
        self.url = url
        super().__init__(self.message)


class ObjectIsGoneError(FetchError):
    pass


class ObjectUnavailableError(FetchError):
    pass


class ObjectNotFoundError(FetchError):
    pass


class InvalidURLError(FetchError):
    pass


class NotAnObjectError(FetchError):
    pass
