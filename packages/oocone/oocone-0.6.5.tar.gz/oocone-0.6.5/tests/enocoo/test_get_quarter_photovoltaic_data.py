"""Tests for the oocone.Enocoo.get_individual_consumption() method."""

import datetime as dt

import pytest
from syrupy.assertion import SnapshotAssertion

from oocone import Auth, Enocoo
from tests import TIMEZONE

FIFTEEN_MINUTES = dt.timedelta(seconds=720)


@pytest.mark.parametrize(
    "date",
    [
        pytest.param(dt.date(2024, 1, 1), id="regular day"),
        pytest.param(dt.date(2023, 10, 29), id="summer time to winter time"),
        pytest.param(dt.date(2024, 3, 31), id="winter time to summer time"),
    ],
)
async def test_daily(*, date: dt.date, snapshot: SnapshotAssertion, mock_auth: Auth) -> None:
    """Check that enocoo.get_quarter_photovoltaic_data returns daily data in expected format."""
    enocoo = Enocoo(mock_auth, TIMEZONE)

    actual = await enocoo.get_quarter_photovoltaic_data(during=date, interval="day")
    assert actual == snapshot


@pytest.mark.parametrize(
    "date",
    [pytest.param(dt.date(2024, 1, 1), id="January 2024")],
)
async def test_monthly(*, date: dt.date, snapshot: SnapshotAssertion, mock_auth: Auth) -> None:
    """Check that enocoo.get_quarter_photovoltaic_data returns monthly data in expected format."""
    enocoo = Enocoo(mock_auth, TIMEZONE)

    actual = await enocoo.get_quarter_photovoltaic_data(during=date, interval="month")
    assert actual == snapshot
