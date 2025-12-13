import datetime as dt
import json
import logging
from typing import Any

from oocone._internal.scrape_timeseries import (
    day_string_to_date,
    discard_unordered_hours,
    get_periods_per_hour,
    length_of_day,
)
from oocone.auth import Auth
from oocone.model import PhotovoltaicSummary, Quantity

logger = logging.getLogger(__name__)


async def get_daily_photovoltaic_data(
    date: dt.date, timezone: dt.tzinfo, auth: Auth
) -> list[PhotovoltaicSummary]:
    logger.debug("Scraping daily photovoltaic data on %s...", date)
    response, _ = await auth.request(
        "GET",
        "php/getPVDataDetails.php",
        params={
            "from": date.isoformat(),
            "intVal": "Tag",
            "diagType": "GesamtverbrauchUndErzeugung",
        },
    )
    return _parse_daily_photovoltaic_data(
        data=await response.text(),
        unit="kWh",
        date=date,
        timezone=timezone,
    )


async def get_monthly_photovoltaic_data(
    date: dt.date, timezone: dt.tzinfo, auth: Auth
) -> list[PhotovoltaicSummary]:
    logger.debug("Scraping monthly photovoltaic data on %s...", date)
    response, _ = await auth.request(
        "GET",
        "php/getPVDataDetails.php",
        params={
            "from": date.isoformat(),
            "intVal": "Monat",
            "diagType": "GesamtverbrauchUndErzeugung",
        },
    )
    return _parse_monthly_photovoltaic_data(
        data=await response.text(),
        unit="kWh",
        year=date.year,
        month=date.month,
        timezone=timezone,
    )


def _parse_daily_photovoltaic_data(
    *,
    data: str,
    unit: str,
    date: dt.date,
    timezone: dt.tzinfo,
) -> list[PhotovoltaicSummary]:
    results = []

    json_data = json.loads(data)
    raw_values = zip(*(json_data[0:4]), strict=True)
    hours = json_data[4]

    last_time = dt.datetime(
        date.year, date.month, date.day, hour=0, minute=0, second=0, tzinfo=timezone
    )
    last_hour = None

    hours, values = discard_unordered_hours(
        hours, raw_values, date, description="photovoltaic data"
    )
    periods_per_hour = get_periods_per_hour(hours)

    for hour, value in zip(hours, values, strict=False):
        period = periods_per_hour[hour]

        if hour == last_hour:
            time = last_time + period
        else:
            time = last_time.replace(hour=hour, minute=0)

        summary = PhotovoltaicSummary(
            start=time,
            period=period,
            consumption=Quantity(value=float(value[0]), unit=unit),
            generation=Quantity(value=float(value[1]), unit=unit),
            self_sufficiency=_quantity_or_none(value[2], unit="%"),
            own_consumption=_quantity_or_none(value[3], unit="%"),
        )
        results.append(summary)

        last_time = time
        last_hour = hour

    return results


def _parse_monthly_photovoltaic_data(
    *,
    data: str,
    unit: str,
    year: int,
    month: int,
    timezone: dt.tzinfo,
) -> list[PhotovoltaicSummary]:
    results = []

    json_data = json.loads(data)
    values = zip(*(json_data[0:4]), strict=True)
    dates = [day_string_to_date(day_string, month, year) for day_string in json_data[4]]

    for date, value in zip(dates, values, strict=False):
        summary = PhotovoltaicSummary(
            start=dt.datetime.combine(date, dt.time(0, 0), tzinfo=timezone),
            period=length_of_day(date, timezone=timezone),
            consumption=Quantity(value=float(value[0]), unit=unit),
            generation=Quantity(value=float(value[1]), unit=unit),
            self_sufficiency=_quantity_or_none(value[2], unit="%"),
            own_consumption=_quantity_or_none(value[3], unit="%"),
        )
        results.append(summary)

    return results


def _quantity_or_none(value: Any, unit: str) -> Quantity | None:
    if value is None:
        return None
    return Quantity(value=float(value), unit=unit)
