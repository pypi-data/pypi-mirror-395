"""Tests for oocone._internal.scrape_timeseries."""

import datetime as dt
from itertools import chain, repeat

from oocone._internal import scrape_timeseries


def test_get_periods_per_hour_four_points_per_hour() -> None:
    """Check that with four points per hours, for 24 hours straight, all periods are 15 minutes."""
    hours = list(chain(*(repeat(hour, 4) for hour in range(24))))
    expected_periods = {hour: dt.timedelta(minutes=15) for hour in range(24)}

    periods = scrape_timeseries.get_periods_per_hour(hours)
    assert periods == expected_periods


def test_get_periods_per_hour_more_points_per_hour() -> None:
    """Check that if an hour contains five or six data points, periods are 12 and minutes."""
    hours = [0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3]
    expected_periods = {
        0: dt.timedelta(minutes=15),
        1: dt.timedelta(minutes=12),
        2: dt.timedelta(minutes=10),
        3: dt.timedelta(minutes=15),
    }

    periods = scrape_timeseries.get_periods_per_hour(hours)
    assert periods == expected_periods


def test_get_periods_per_hour_less_points_per_hour() -> None:
    """Check that if an hour contains less than four data points, periods are still 15 minutes."""
    hours = [0, 0, 0, 0, 1, 1, 2, 2, 2]
    expected_periods = {
        0: dt.timedelta(minutes=15),
        1: dt.timedelta(minutes=15),
        2: dt.timedelta(minutes=15),
    }

    periods = scrape_timeseries.get_periods_per_hour(hours)
    assert periods == expected_periods
