import doctest
from datetime import datetime
from zoneinfo import ZoneInfo

import pytest
from tzlocal import get_localzone

from preheat_open import time


@pytest.fixture
def date_ranges():
    dr1 = time.SubDateRange(datetime(2024, 1, 1), datetime(2024, 1, 5))
    dr2 = time.SubDateRange(datetime(2024, 1, 10), datetime(2024, 1, 15))
    dr3 = time.SubDateRange(datetime(2024, 1, 5), datetime(2024, 1, 10))
    dr4 = time.SubDateRange(datetime(2024, 1, 12), datetime(2024, 1, 20))
    return time.DateRange([dr1, dr2]), time.DateRange([dr3, dr4])


def test_add(date_ranges):
    ranges1, ranges2 = date_ranges
    combined = ranges1 + ranges2
    assert len(combined.ranges) == 3


def test_subtract(date_ranges):
    ranges1, ranges2 = date_ranges
    subtracted = ranges1 - ranges2
    assert len(subtracted.ranges) == 2
    local_tz = get_localzone()
    assert subtracted.ranges[0].start == datetime(2024, 1, 1, tzinfo=local_tz)
    assert subtracted.ranges[0].end == datetime(2024, 1, 5, tzinfo=local_tz)
    assert subtracted.ranges[1].start == datetime(2024, 1, 10, tzinfo=local_tz)
    assert subtracted.ranges[1].end == datetime(2024, 1, 12, tzinfo=local_tz)


@pytest.mark.parametrize(
    "date, expected",
    [
        (datetime(2024, 1, 3).astimezone(get_localzone()), True),
        (datetime(2024, 1, 8).astimezone(get_localzone()), False),
    ],
)
def test_contains(date_ranges, date, expected):
    ranges1, _ = date_ranges
    assert (date in ranges1) == expected


@pytest.mark.parametrize("expected_len", [1])
def test_intersection(date_ranges, expected_len):
    ranges1, ranges2 = date_ranges
    intersections = ranges1.intersection(ranges2)
    assert len(intersections.ranges) == expected_len


@pytest.mark.parametrize("expected_len", [1])
def test_gaps(date_ranges, expected_len):
    ranges1, _ = date_ranges
    gaps = ranges1.gaps()
    assert len(gaps.ranges) == expected_len


@pytest.mark.parametrize(
    "expected_start, expected_end",
    [
        (
            datetime(2024, 1, 1, tzinfo=get_localzone()),
            datetime(2024, 1, 15, tzinfo=get_localzone()),
        ),
    ],
)
def test_union(date_ranges, expected_start, expected_end):
    ranges1, _ = date_ranges
    union_range = ranges1.union()
    assert union_range.lstart == expected_start
    assert union_range.rend == expected_end


def test_time_resolution():
    res = ["raw", "minute", "hour", "day", "week", "month", "year"]
    for i, ri in enumerate(res):
        for j, rj in enumerate(res):
            assert (i < j) == (time.TimeResolution(ri) > time.TimeResolution(rj))

    assert time.TimeResolution("raw").pandas_alias is None
    assert time.TimeResolution("minute").pandas_alias == "5T"
    assert time.TimeResolution("hour").pandas_alias == "H"
    assert time.TimeResolution("day").pandas_alias == "D"


def test_doctests():
    """
    Run doctests for the time module.
    """
    results = doctest.testmod(time)
    assert (
        results.failed == 0
    ), f"Doctests failed: {results.failed} failed out of {results.attempted}"
