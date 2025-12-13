"""Tests for the oocone.Enocoo.get_meter_table() method."""

import datetime as dt
from typing import Any

import pytest

from oocone import Auth, Enocoo
from oocone.model import MeterStatus, Quantity
from tests import TIMEZONE, conftest
from tests.conftest import MockApiParams

TODAY = dt.datetime.now(tz=TIMEZONE).date()
MIDNIGHT = dt.time(0, 0, 0)


def _expected_meter_table(date: dt.date, time: dt.time | None = None) -> list[MeterStatus]:
    if time is None:
        time = dt.time(12, 34, 56)
    expected_timestamp = dt.datetime.combine(date, time, tzinfo=TIMEZONE)
    return [
        MeterStatus(
            name="Verbrauch Kaltwasser H12W34 Bad",
            area="H12W34",
            meter_id="00000001",
            timestamp=expected_timestamp,
            reading=Quantity(value=1234.56, unit="m³"),
        ),
        MeterStatus(
            name="Verbrauch Kaltwasser H12W34 WC",
            area="H12W34",
            meter_id="00000002",
            timestamp=expected_timestamp,
            reading=Quantity(value=1234.56, unit="m³"),
        ),
        MeterStatus(
            name="Verbrauch Strom H12W34",
            area="H12W34",
            meter_id="00000003",
            timestamp=expected_timestamp,
            reading=Quantity(1234.56, unit="kWh"),
        ),
        MeterStatus(
            name="Verbrauch Wärme H12W34",
            area="H12W34",
            meter_id="00000004",
            timestamp=expected_timestamp,
            reading=Quantity(1234.56, unit="kWh"),
        ),
        MeterStatus(
            name="Verbrauch Warmwasser H12W34 Bad",
            area="H12W34",
            meter_id="00000005",
            timestamp=expected_timestamp,
            reading=Quantity(1234.56, unit="m³"),
        ),
        MeterStatus(
            name="Verbrauch Warmwasser H12W34 WC",
            area="H12W34",
            meter_id="00000006",
            timestamp=expected_timestamp,
            reading=Quantity(1234.56, unit="m³"),
        ),
    ]


async def test_without_params(mock_auth: Auth) -> None:
    """Check that the function returns data for the current day when called without parameters."""
    expected = _expected_meter_table(TODAY)

    enocoo = Enocoo(mock_auth, timezone=TIMEZONE)
    result = await enocoo.get_meter_table()

    assert result == expected


async def test_with_date_param(mock_auth: Auth) -> None:
    """Check that when called with a date param, the function returns data for that day."""
    date = dt.date(2012, 12, 12)
    expected = _expected_meter_table(date)

    enocoo = Enocoo(mock_auth, timezone=TIMEZONE)
    result = await enocoo.get_meter_table(date=date)

    assert result == expected


@pytest.mark.parametrize(
    ("allow_previous_day_until", "last_timestamp", "expected_result"),
    [
        # Shortly after midnight, the only data available are the ones for midnight. The enocoo
        # website does not list them on the page for the new day though, but on the page for the
        # previous day. The timestamp will still indicate the current date at 00:00.
        pytest.param(
            None,
            dt.datetime.combine(TODAY, MIDNIGHT),
            _expected_meter_table(TODAY, MIDNIGHT),
            id="midnight",
        ),
        # ------------------------------------------------------------------------------------------
        # ...except that is not entirely true: For the first 15 minutes after midnight, even the
        # data from midnight are not available, and instead we will see data from 15 minutes
        # earlier. Since that is not data from the current day, they are not returned by default.
        pytest.param(
            None,
            dt.datetime.combine(TODAY - dt.timedelta(days=1), dt.time(23, 45)),
            [],
            id="quarter-before-midnight-forbidden",
        ),
        # ------------------------------------------------------------------------------------------
        # ...except if the user explicitly opts into that.
        pytest.param(
            dt.time(23, 45),
            dt.datetime.combine(TODAY - dt.timedelta(days=1), dt.time(23, 45)),
            _expected_meter_table(TODAY - dt.timedelta(days=1), dt.time(23, 45)),
            id="quarter-before-midnight-allowed",
        ),
        # ------------------------------------------------------------------------------------------
        # ... but even if allow_previous_day_until is set: if the latest data are older than
        # allowed, they must not be returned.
        pytest.param(
            dt.time(23, 45),
            dt.datetime.combine(TODAY - dt.timedelta(days=1), dt.time(12, 00)),
            [],
            id="previous-noon-forbidden",
        ),
    ],
)
async def test_fallback_to_previous_day(
    allow_previous_day_until: dt.time | None,
    last_timestamp: dt.datetime,
    expected_result: list[MeterStatus],
    mock_auth: Auth,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Check that the method correctly implements fallback to the previous day."""
    original_new_meter_table_body = conftest._new_meter_table_body

    def patched_new_meter_table_body(
        *, logged_in: bool, date: dt.date, mock_api_params: MockApiParams
    ) -> bytes:
        if not logged_in:
            return original_new_meter_table_body(
                logged_in=logged_in, date=date, mock_api_params=mock_api_params
            )

        if date == TODAY:
            with (
                mock_api_params.response_data_path / "newMeterTable.noDataYetForCurrentDay.php"
            ).open("rb") as f:
                return f.read()
        elif date == TODAY - dt.timedelta(days=1):
            return original_new_meter_table_body(
                logged_in=logged_in,
                date=last_timestamp.date(),
                time=last_timestamp.time(),
                mock_api_params=mock_api_params,
            )
        else:
            msg = f"Date {date} should not be queried in this test"
            raise AssertionError(msg)

    monkeypatch.setattr(conftest, "_new_meter_table_body", patched_new_meter_table_body)

    enocoo = Enocoo(mock_auth, timezone=TIMEZONE)
    result = await enocoo.get_meter_table(allow_previous_day_until=allow_previous_day_until)

    assert result == expected_result


async def test_fallback_failing(
    mock_auth: Auth, mock_api_params: MockApiParams, monkeypatch: pytest.MonkeyPatch
) -> None:
    """
    Check that the method does not return data from a previous day.

    The fallback to the previous day is explained in ``test_fallback_to_midnight``. If the page for
    the previous day does not in fact return data for midnight of the current day, but in fact for
    the previous day, the method shall not return them.
    """
    original_new_meter_table_body = conftest._new_meter_table_body

    def patched_new_meter_table_body(*, logged_in: bool, date: dt.date, **kwargs: Any) -> bytes:
        if not logged_in:
            return original_new_meter_table_body(logged_in=logged_in, date=date, **kwargs)

        if date == TODAY:
            with (
                mock_api_params.response_data_path / "newMeterTable.noDataForCurrentDay.php"
            ).open("rb") as f:
                return f.read()
        elif date == TODAY - dt.timedelta(days=1):
            return original_new_meter_table_body(
                logged_in=logged_in, date=date, time=dt.time(10, 0, 0), **kwargs
            )
        else:
            msg = f"Date {date} should not be queried in this test"
            raise AssertionError(msg)

    monkeypatch.setattr(conftest, "_new_meter_table_body", patched_new_meter_table_body)

    enocoo = Enocoo(mock_auth, timezone=TIMEZONE)
    result = await enocoo.get_meter_table()

    assert result == []
