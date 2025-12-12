"""Exception classes for qciconnect package."""

class QciConnectClientError(Exception):
    """Exception class for errors from QciConnectClient."""


class InvalidIdentifierError(Exception):
    """Thrown when identifiers contain forbidden characters."""


class ResultError(Exception):
    """Exception class for errors related to results handling."""
