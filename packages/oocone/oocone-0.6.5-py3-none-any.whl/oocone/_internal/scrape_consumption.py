import datetime as dt
import json
import logging
import re
from typing import cast

from bs4 import BeautifulSoup
from bs4 import Tag as HtmlTag

from oocone._internal.scrape_timeseries import (
    day_string_to_date,
    discard_unordered_hours,
    get_periods_per_hour,
    length_of_day,
)
from oocone.auth import Auth
from oocone.errors import UnexpectedResponse
from oocone.model import Area, Consumption, ConsumptionType

logger = logging.getLogger(__name__)

_CONSUMPTION_CLASSES = {
    ConsumptionType.ELECTRICITY: "Stromverbrauch",
    ConsumptionType.HEAT: "Waerme",
    ConsumptionType.WATER_COLD: "Kaltwasser",
    ConsumptionType.WATER_HOT: "Warmwasser",
}

_CONSUMPTION_UNITS = {
    ConsumptionType.ELECTRICITY: "kWh",
    ConsumptionType.HEAT: "kWh",
    ConsumptionType.WATER_COLD: "m³",
    ConsumptionType.WATER_HOT: "m³",
}

NUM_MONTHS = 12


async def get_areas(auth: Auth) -> list[Area]:
    logger.debug("Scraping areas from consumption page...")
    _, soup = await auth.request("GET", "php/ownConsumption.php")
    return _parse_areas(soup)


def _parse_areas(soup: BeautifulSoup) -> list[Area]:
    areas = []
    area_selectors = soup.select('label[for="residence"]')
    if area_selectors:
        logger.debug(
            "Found area selection dropdown on consumption page. Parsing the dropdown menu..."
        )
        for selector in area_selectors:
            areas += _parse_areas_for_selector(cast("HtmlTag", selector.parent))
    else:
        logger.debug(
            "Did not find area selection dropdown. Trying to find a reference to a single area..."
        )
        areas.append(_parse_single_area(soup))

    return areas


def _parse_areas_for_selector(selection_form: HtmlTag) -> list[Area]:
    areas = []
    for list_item in selection_form.find_all("li"):
        area_link = cast("HtmlTag", list_item).find("a")
        if not isinstance(area_link, HtmlTag):
            msg = f"Expected <a> Tag in area selector dropdown, got {type(area_link)} instead."
            raise UnexpectedResponse(msg)

        areas.append(
            Area(
                name=area_link.text.strip(),
                id=str(area_link.attrs["id"]),
                data_available_since=_parse_german_date(str(area_link.attrs["data-valfrom"])),
                data_available_until=_parse_german_date(str(area_link.attrs["data-valto"])),
            )
        )

    return areas


def _parse_single_area(soup: BeautifulSoup) -> Area:
    if (
        match1 := re.search(
            r'var chosenResidenceId = "(\d+)";',
            "\n\n".join(script.text for script in soup.find_all("script")),
        )
    ) and (
        match2 := re.search(
            r"Wohneinheit: (H\d+W\d+)"
            r" \(Zugreifbarer Zeitraum: (\d{2}\.\d{2}\.\d{4}) - (\d{2}\.\d{2}\.\d{4})",
            soup.text,
        )
    ):
        return Area(
            id=match1.group(1),
            name=match2.group(1),
            data_available_since=_parse_german_date(match2.group(2)),
            data_available_until=_parse_german_date(match2.group(3)),
        )

    msg = "Failed to scrape single area ID from page"
    raise UnexpectedResponse(msg)


def _parse_german_date(date_string: str) -> dt.date:
    return dt.datetime.strptime(date_string, "%d.%m.%Y").date()  # noqa: DTZ007


async def get_daily_consumption(
    consumption_type: ConsumptionType, area_id: str, date: dt.date, timezone: dt.tzinfo, auth: Auth
) -> list[Consumption]:
    logger.debug(
        "Scraping daily %s consumption on %s for area with ID %s...",
        consumption_type,
        date,
        area_id,
    )
    response, _ = await auth.request(
        "GET",
        "php/getMeterDataWithParam.php",
        params={
            "AreaId": area_id,
            "from": date.isoformat(),
            "intVal": "Tag",
            "mClass": _CONSUMPTION_CLASSES[consumption_type],
        },
    )
    return _parse_daily_consumption(
        daily_consumption_json=await response.text(),
        unit=_CONSUMPTION_UNITS[consumption_type],
        date=date,
        timezone=timezone,
        values_are_integrated=(consumption_type == ConsumptionType.HEAT),
    )


async def get_monthly_consumption(
    consumption_type: ConsumptionType, area_id: str, date: dt.date, timezone: dt.tzinfo, auth: Auth
) -> list[Consumption]:
    logger.debug(
        "Scraping monthly %s consumption on %s for area with ID %s...",
        consumption_type,
        date,
        area_id,
    )
    response, _ = await auth.request(
        "GET",
        "php/getMeterDataWithParam.php",
        params={
            "AreaId": area_id,
            "from": date.isoformat(),
            "intVal": "Monat",
            "mClass": _CONSUMPTION_CLASSES[consumption_type],
        },
    )
    return _parse_monthly_consumption(
        monthly_consumption_json=await response.text(),
        unit=_CONSUMPTION_UNITS[consumption_type],
        year=date.year,
        month=date.month,
        timezone=timezone,
    )


async def get_yearly_consumption(
    consumption_type: ConsumptionType,
    area_id: str,
    year_number: int,
    timezone: dt.tzinfo,
    auth: Auth,
) -> list[Consumption]:
    logger.debug(
        "Scraping yearly %s consumption in %s for area with ID %s...",
        consumption_type,
        year_number,
        area_id,
    )
    response, _ = await auth.request(
        "GET",
        "php/getMeterDataWithParam.php",
        params={
            "AreaId": area_id,
            "from": f"{year_number}-01-01",
            "intVal": "Jahr",
            "mClass": _CONSUMPTION_CLASSES[consumption_type],
        },
    )
    return _parse_yearly_consumption(
        yearly_consumption_json=await response.text(),
        unit=_CONSUMPTION_UNITS[consumption_type],
        year_number=year_number,
        timezone=timezone,
    )


def _parse_daily_consumption(
    *,
    daily_consumption_json: str,
    values_are_integrated: bool,
    unit: str,
    date: dt.date,
    timezone: dt.tzinfo,
) -> list[Consumption]:
    results = []

    json_data = json.loads(daily_consumption_json)
    hours = json_data[1]
    values = json_data[0]

    last_time = dt.datetime(
        date.year, date.month, date.day, hour=0, minute=0, second=0, tzinfo=timezone
    )
    last_hour = None
    last_value = 0

    hours, values = discard_unordered_hours(hours, values, date, description="consumption")
    periods_per_hour = get_periods_per_hour(hours)

    for hour, value in zip(hours, values, strict=False):
        period = periods_per_hour[hour]

        if hour == last_hour:
            time = last_time + period
        else:
            time = last_time.replace(hour=hour, minute=0)

        if values_are_integrated:
            consumption_value = float(value) - float(last_value)
        else:
            consumption_value = float(value)

        consumption = Consumption(start=time, period=period, value=consumption_value, unit=unit)
        results.append(consumption)

        last_time = time
        last_hour = hour
        last_value = value

    return results


def _parse_monthly_consumption(
    *,
    monthly_consumption_json: str,
    unit: str,
    year: int,
    month: int,
    timezone: dt.tzinfo,
) -> list[Consumption]:
    results = []

    json_data = json.loads(monthly_consumption_json)
    values = json_data[0]
    dates = [day_string_to_date(day_string, month, year) for day_string in json_data[1]]

    for date, value in zip(dates, values, strict=False):
        consumption = Consumption(
            start=dt.datetime.combine(date, dt.time(0, 0), tzinfo=timezone),
            period=length_of_day(date, timezone),
            value=value,
            unit=unit,
        )
        results.append(consumption)

    return results


def _parse_yearly_consumption(
    *,
    yearly_consumption_json: str,
    unit: str,
    year_number: int,
    timezone: dt.tzinfo,
) -> list[Consumption]:
    results = []

    month_names_to_number = {
        "Jan.": 1,
        "Feb.": 2,
        "Mär.": 3,
        "Apr.": 4,
        "Mai": 5,
        "Jun.": 6,
        "Jul.": 7,
        "Aug.": 8,
        "Sep.": 9,
        "Okt.": 10,
        "Nov.": 11,
        "Dez.": 12,
    }

    json_data = json.loads(yearly_consumption_json)
    month_names = json_data[1]
    values = json_data[0]

    for month_name, value in zip(month_names, values, strict=False):
        month = month_names_to_number[month_name]

        begin_of_month = dt.date(year_number, month, 1)
        begin_of_next_month = dt.date(
            year_number if month < NUM_MONTHS else year_number + 1,
            month + 1 if month < NUM_MONTHS else 1,
            1,
        )
        consumption = Consumption(
            start=dt.datetime.combine(begin_of_month, dt.time(tzinfo=timezone)),
            period=begin_of_next_month - begin_of_month,
            value=value,
            unit=unit,
        )
        results.append(consumption)

    return results
