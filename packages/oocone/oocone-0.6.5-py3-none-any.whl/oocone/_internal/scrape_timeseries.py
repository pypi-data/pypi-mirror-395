import datetime as dt
import logging
from collections import Counter
from collections.abc import Iterable

logger = logging.getLogger(__name__)


def get_periods_per_hour(hours: list[int]) -> dict[int, dt.timedelta]:
    one_hour = dt.timedelta(hours=1)
    max_period = dt.timedelta(minutes=15)

    return {
        hour: min(one_hour / measurements_per_hour, max_period)
        for hour, measurements_per_hour in Counter(hours).items()
    }


def discard_unordered_hours[ValueT](
    hours: Iterable[int],
    values: Iterable[ValueT],
    date: dt.date,
    *,
    description: str,
    stop_after_midnight: bool = True,
) -> tuple[list[int], list[ValueT]]:
    filtered_hours = []
    filtered_values = []

    last_hour = None

    for hour, value in zip(hours, values, strict=False):
        if stop_after_midnight and last_hour == 23 and hour != last_hour:  # noqa: PLR2004
            # hour after midnight -> discard
            break
        if last_hour is not None and hour < last_hour:
            logger.warning(
                "Hours are unordered in daily %s reading for %s: hour %s follows hour %s."
                " %s metric is discarded.",
                description,
                date.isoformat(),
                hour,
                last_hour,
                description.capitalize(),
            )
            continue

        filtered_hours.append(hour)
        filtered_values.append(value)
        last_hour = hour

    return filtered_hours, filtered_values


def day_string_to_date(day_str: str, month: int, year: int) -> dt.date:
    r"""
    Convert a day string to an actual date.

    Args:
        day_str: a string returned by Enocoo APIs. Example: "So.\n 01."
        month: current month (1-2)
        year: current year

    """
    day = int(day_str.splitlines()[-1].strip().lstrip("0").rstrip("."))
    return dt.date(year, month, day)


def length_of_day(day: dt.date, timezone: dt.tzinfo) -> dt.timedelta:
    next_day = day + dt.timedelta(days=1)
    midnight = dt.datetime.combine(day, dt.time(0, 0), tzinfo=timezone)
    next_midnight = dt.datetime.combine(next_day, dt.time(0, 0), tzinfo=timezone)

    return next_midnight - midnight
