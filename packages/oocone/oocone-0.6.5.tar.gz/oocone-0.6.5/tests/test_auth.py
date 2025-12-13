"""Tests for oocone.Auth."""

import pytest

from oocone import Auth, errors
from tests import MockApiClient


async def test_login_successful(mock_api: MockApiClient) -> None:
    """Check that Auth._login() does not throw an exception with correct credentials."""
    auth = Auth(
        websession=mock_api.session,
        base_url=str(mock_api.server.make_url("/")),
        username="correct",
        password="correct",  # noqa: S106
    )
    await auth._login()


async def test_login_raise_on_failure(mock_api: MockApiClient) -> None:
    """Check that Auth._login() raises an exception for incorrect credentials."""
    auth = Auth(
        websession=mock_api.session,
        base_url=str(mock_api.server.make_url("/")),
        username="correct",
        password="incorrect",  # noqa: S106
    )
    with pytest.raises(errors.AuthenticationFailed):
        await auth._login()
