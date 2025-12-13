"""Tests for the oocone.Enocoo.get_individual_consumption() method."""

import datetime as dt
import json

import pytest

from oocone import Auth, Enocoo
from oocone._internal.scrape_consumption import _CONSUMPTION_CLASSES as CONSUMPTION_CLASSES
from oocone.model import ConsumptionType
from tests import TIMEZONE
from tests.conftest import MOCK_API_DATASET_NAMES, MockApiParams


def _get_consumption_sum(  # noqa: PLR0913
    consumption_type: ConsumptionType,
    *,
    date: dt.date,
    interval: str,
    compensate_off_by_one: bool,
    area_id: str,
    mock_api_params: MockApiParams,
) -> float:
    def enocoo_response(request_date: dt.date) -> list:
        response_path = (
            mock_api_params.response_data_path
            / "getMeterDataWithParam.{consumption}.{area_id}.{date}.{interval}.php".format(  # noqa: UP032
                consumption=CONSUMPTION_CLASSES[consumption_type],
                area_id=area_id,
                date=request_date.isoformat(),
                interval=interval,
            )
        )

        with response_path.open("rb") as response_file:
            response = response_file.read()

        return json.loads(response)

    if consumption_type == ConsumptionType.HEAT and interval == "Tag":
        # Heat readings are integrated, so we need to calculate differences
        raw_readings, hours = enocoo_response(date)[:2]
        if raw_readings:  # readings are actually available
            readings_current_day = [raw_readings[0], raw_readings[-1] - raw_readings[0]]
        else:  # no readings for the current day are available
            readings_current_day = []
    else:
        readings_current_day, hours = enocoo_response(date)[:2]

        # Remove any next-day data that we might see
        while len(hours) >= 1 and hours[-1] == 0:
            hours.pop()
            readings_current_day.pop()

    if compensate_off_by_one:
        readings_next_day = enocoo_response(date + dt.timedelta(days=1))[0]
        relevant_readings = readings_current_day[1:] + readings_next_day[:1]
    else:
        relevant_readings = readings_current_day

    return sum(relevant_readings)


@pytest.mark.parametrize(
    "date",
    [
        pytest.param(dt.date(2024, 1, 1), id="regular day"),
        pytest.param(dt.date(2023, 10, 29), id="summer time to winter time"),
        pytest.param(dt.date(2024, 3, 31), id="winter time to summer time"),
    ],
)
@pytest.mark.parametrize(
    "consumption_type",
    [
        ConsumptionType.ELECTRICITY,
        ConsumptionType.WATER_COLD,
        ConsumptionType.WATER_HOT,
        ConsumptionType.HEAT,
    ],
)
@pytest.mark.parametrize("dataset", MOCK_API_DATASET_NAMES)
@pytest.mark.parametrize(
    "compensate_quirks",
    [
        pytest.param(False, id="uncompensated"),
        pytest.param(True, id="compensated"),
    ],
)
async def test_daily(  # noqa: PLR0913
    *,
    date: dt.date,
    consumption_type: ConsumptionType,
    compensate_quirks: bool,
    mock_auth: Auth,
    mock_api_params: MockApiParams,
    dataset: str,
) -> None:
    """Check that enocoo.get_individual_consumption returns daily data in expected format."""
    mock_api_params.dataset_name = dataset
    enocoo = Enocoo(mock_auth, TIMEZONE)

    for area in await enocoo.get_areas():
        consumption = await enocoo.get_individual_consumption(
            consumption_type=consumption_type,
            area_id=area.id,
            during=date,
            interval="day",
            compensate_off_by_one=compensate_quirks,
        )

        for hour in {cons.start.hour for cons in consumption}:
            period_sum = sum(
                [cons.period for cons in consumption if cons.start.hour == hour],
                start=dt.timedelta(),
            )
            assert period_sum == dt.timedelta(hours=1), (
                f"periods for hour {hour} should add up to one hour"
            )

        expected_sum = _get_consumption_sum(
            consumption_type,
            date=date,
            interval="Tag",
            compensate_off_by_one=compensate_quirks,
            area_id=area.id,
            mock_api_params=mock_api_params,
        )
        actual_sum = sum(cons.value for cons in consumption)
        assert actual_sum == expected_sum


@pytest.mark.parametrize("dataset", MOCK_API_DATASET_NAMES)
@pytest.mark.parametrize(
    "consumption_type",
    [
        ConsumptionType.ELECTRICITY,
        ConsumptionType.WATER_COLD,
        ConsumptionType.WATER_HOT,
        ConsumptionType.HEAT,
    ],
)
async def test_monthly(
    *,
    consumption_type: ConsumptionType,
    mock_auth: Auth,
    mock_api_params: MockApiParams,
    dataset: str,
) -> None:
    """Check that enocoo.get_individual_consumption returns monthly data in expected format."""
    date = dt.date(2024, 1, 1)
    mock_api_params.dataset_name = dataset
    enocoo = Enocoo(mock_auth, TIMEZONE)

    for area in await enocoo.get_areas():
        consumption = await enocoo.get_individual_consumption(
            consumption_type=consumption_type,
            area_id=area.id,
            during=date,
            interval="month",
        )

        expected_sum = _get_consumption_sum(
            consumption_type,
            date=date,
            interval="Monat",
            compensate_off_by_one=False,
            area_id=area.id,
            mock_api_params=mock_api_params,
        )
        actual_sum = sum(cons.value for cons in consumption)
        assert actual_sum == expected_sum


@pytest.mark.parametrize(
    "consumption_type",
    [
        ConsumptionType.ELECTRICITY,
        ConsumptionType.WATER_COLD,
        ConsumptionType.WATER_HOT,
        ConsumptionType.HEAT,
    ],
)
@pytest.mark.parametrize("dataset", MOCK_API_DATASET_NAMES)
async def test_yearly(
    consumption_type: ConsumptionType,
    mock_auth: Auth,
    dataset: str,
    mock_api_params: MockApiParams,
) -> None:
    """Check that enocoo.get_individual_consumption returns yearly data in expected format."""
    mock_api_params.dataset_name = dataset
    enocoo = Enocoo(mock_auth, TIMEZONE)

    for area in await enocoo.get_areas():
        consumption = await enocoo.get_individual_consumption(
            consumption_type=consumption_type,
            area_id=area.id,
            during=dt.date(2024, 1, 1),
            interval="year",
        )

        for reading in consumption:
            match reading.start.month:
                case 1 | 3 | 5 | 7 | 8 | 10 | 12:
                    assert reading.period == dt.timedelta(days=31)
                case 2:
                    assert reading.period == dt.timedelta(days=29)
                case 4 | 6 | 9 | 11:
                    assert reading.period == dt.timedelta(days=30)
