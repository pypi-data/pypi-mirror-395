"""Defines exceptions specific to this module."""


class OoconeError(Exception):
    """Base class for oocone."""


class ConnectionIssue(OoconeError):
    """Could not connect to the enocoo website."""


class AuthenticationFailed(OoconeError):
    """Authentication has failed."""


class UnexpectedResponse(OoconeError):
    """Got unexpected data back from the enocoo website."""


class OoconeMisuse(OoconeError):
    """The oocone API was misused."""
