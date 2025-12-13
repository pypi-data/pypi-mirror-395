import datetime as dt
import logging

from bs4 import Tag

from oocone import errors
from oocone._internal.html_table import parse_table
from oocone.auth import Auth
from oocone.model import MeterStatus, Quantity

logger = logging.getLogger(__name__)


async def get_meter_table(date: dt.date, timezone: dt.tzinfo, auth: Auth) -> list[MeterStatus]:
    logger.debug("Scraping meter table for %s...", date)
    _, soup = await auth.request(
        "POST",
        "php/newMeterTable.php",
        data={"dateParam": date.isoformat()},
    )
    html_table = soup.find("table")
    if not isinstance(html_table, Tag):
        msg = f"Expected table as Tag but found {type(html_table)}"
        raise errors.UnexpectedResponse(msg)
    meter_table = parse_table(html_table)

    result = []
    for row in meter_table.rows:
        try:
            if row["Zeitpunkt"] == "" or row["Einheit"] == "":
                continue

            meter_status = MeterStatus(
                name=row["Bezeichnung"],
                area=row["Fläche"],
                meter_id=row["Zähler-Nr."],
                timestamp=_parse_timestamp(row["Zeitpunkt"], timezone),
                reading=Quantity(
                    value=_parse_reading(row["Zählerstand"]),
                    unit=_parse_unit(row["Einheit"]),
                ),
            )
        except Exception as e:
            raise errors.UnexpectedResponse from e

        result.append(meter_status)

    return result


def _parse_timestamp(timestamp: str, timezone: dt.tzinfo) -> dt.datetime:
    dateformat = r"%d.%m.%Y %H:%M:%S"
    return dt.datetime.strptime(timestamp, dateformat).replace(tzinfo=timezone)


def _parse_reading(reading: str) -> float:
    # The reading uses german number formatting with a comma as the decimal separator and a
    # dot as the thousands separator. The convention used by float is a dot as the decimal
    # separator and comma as the thousands separator.abs

    reading = reading.replace(".", "")  # we don't need a thousands separator here
    reading = reading.replace(",", ".")

    return float(reading)


def _parse_unit(text: str) -> str:
    if text == "m3":
        result = "m³"
    else:
        result = text

    return result
