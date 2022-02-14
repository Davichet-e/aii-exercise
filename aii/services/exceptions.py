class ServiceException(Exception):
    """Common base class for exception ocurred at Service level"""


class RetrieveNewsException(ServiceException):
    """Raised when an error occurr when retrieving the news from the url."""

    def __init__(self) -> None:
        super().__init__("An error ocurred retrieving the news from the url")


class NewsNotStoredException(ServiceException):
    """Raised when news are yet not stored."""

    def __init__(self) -> None:
        super().__init__("News are not stored.")


class InternalErrorException(ServiceException):
    """Raised when an internal error happens."""

    def __init__(self) -> None:
        super().__init__("An internal error ocurred.")
