class HeliosException(Exception):
    """Base exception for helios_websocket_api."""

    pass


class HeliosInvalidInputException(HeliosException):
    """Exception for wrong input."""

    pass


class HeliosApiException(HeliosException):
    """Exception for api errors."""

    pass


class HeliosWebsocketException(HeliosApiException):
    """Exception for websocket errors."""

    pass
