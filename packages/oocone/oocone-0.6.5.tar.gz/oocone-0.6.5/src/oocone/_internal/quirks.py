"""Contains various functions for handling quirks of the enocoo portal."""

import asyncio
import dataclasses
import datetime as dt
import itertools
from collections.abc import Awaitable, Callable

from oocone.model import Consumption, PhotovoltaicSummary

type QuirkyDataType = Consumption | PhotovoltaicSummary
type FetchCallable[T] = Callable[[dt.date], Awaitable[list[T]]]


async def get_off_by_one_compensated_data[DataT: QuirkyDataType](
    fetch_data: FetchCallable[DataT],
    date: dt.date,
    timezone: dt.tzinfo,
) -> list[DataT]:
    """
    Compensates for an off by one data point bug in the enocoo EMS.

    The enocoo EMS has this bug where energy usage is off by one sample, i.e.  15 minutes. Because
    of this especially, the sum of the daily consumption numbers does does not add up to the actual
    difference of the meter at 00:00 on two consecutive days. Concretely this means that the first
    consumption sample of a given day belongs to the previous day (and in turn that any consumption
    after 23:45 of any given day shows up in the statistics for the day *after* that).
    Unfortunately, this means that for a complete day, we will need to make two requests towards the
    enocoo API instead of one.
    To go as easy as possible on the API, two measures are implemented:

     2. checks against the current date: when requesting data, we never ask for data of a day that
        has not begun yet. This means that we only ask query data for "the next day" when filling
        in the last hour of the day, not any time before that.

    In addition, oocone users should implement a caching mechanism, as `ha_enocoo` does for example.
    """
    original_day = date
    next_day = original_day + dt.timedelta(days=1)
    now = dt.datetime.now(tz=timezone)

    async def fetch_data_omitting_future(date: dt.date) -> list[DataT]:
        if date > now.date():  # date is in the future, no point in querying enocoo for data
            return []

        return await fetch_data(date)

    off_by_one_data, next_day_data = await asyncio.gather(
        fetch_data_omitting_future(original_day), fetch_data_omitting_future(next_day)
    )
    off_by_one_data += next_day_data[:1]

    return [
        dataclasses.replace(
            point_with_correct_data,
            start=point_with_correct_timing.start,
            period=point_with_correct_timing.period,
        )
        for point_with_correct_timing, point_with_correct_data in itertools.pairwise(
            off_by_one_data
        )
    ]
