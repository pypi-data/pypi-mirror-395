"""
time.py

This module defines classes and functions for handling date and time ranges, time resolutions, and time-related utilities.

Classes:
    SubDateRange
    TimeResolution
    DateRange

Functions:
    timestep_start

Examples:
    >>> from datetime import datetime
    >>> from preheat_open.time import TimeResolution, SubDateRange, DateRange, timestep_start
    >>> tr = TimeResolution.HOUR
    >>> print(tr.pandas_alias)
    H
    >>> sdr = SubDateRange(datetime(2023, 1, 1), datetime(2023, 1, 2))
    >>> str(sdr).startswith('[2023-01-01 00:00:00')
    True
    >>> dr = DateRange([sdr], resolution=TimeResolution.DAY)
    >>> '2023-01-01--2023-01-02' in str(dr)
    True
"""

from __future__ import annotations

import math
from datetime import datetime, timedelta, tzinfo
from enum import Enum
from functools import total_ordering
from typing import Generator, List, Optional, TypeVar, Union, cast
from zoneinfo import ZoneInfo

import pandas as pd
from tzlocal import get_localzone


@total_ordering
class TimeResolution(Enum):
    """
    Enum representing different time resolutions.

    Attributes:
        RAW: Raw time resolution.
        MIN5: 5-minute time resolution.
        HOUR: Hourly time resolution.
        DAY: Daily time resolution.
        WEEK: Weekly time resolution.
        MONTH: Monthly time resolution.
        YEAR: Yearly time resolution.

    Examples:
        >>> tr = TimeResolution.HOUR
        >>> print(tr)
        TimeResolution.HOUR
        >>> print(tr.pandas_alias)
        H
    """

    RAW = "raw"
    MIN5 = "minute"
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"

    def __init__(self, *args):
        self._order = len(self.__class__.__members__)

    def __str__(self):
        """
        Returns a string representation of the TimeResolution enum.

        :return: The name of the enum member.
        :rtype: str
        """
        return f"{self.__class__.__name__}.{self.name}"

    def __repr__(self):
        """
        Returns a string representation of the TimeResolution enum.

        :return: The name of the enum member.
        :rtype: str
        """
        return f"{self.__class__.__name__}.{self.name}"

    def __hash__(self):
        """
        Returns the hash of the TimeResolution enum.

        :return: The hash of the enum member.
        :rtype: int
        """
        return hash(self.name)

    @property
    def pandas_alias(self) -> str:
        """
        Returns the pandas alias for the time resolution.

        :return: The pandas alias.
        :rtype: str
        """
        lookup = {
            TimeResolution.RAW: None,
            TimeResolution.MIN5: "5T",
            TimeResolution.HOUR: "H",
            TimeResolution.DAY: "D",
            TimeResolution.WEEK: "7D",
            TimeResolution.MONTH: "MS",
            TimeResolution.YEAR: "YS",
        }
        return lookup[self]

    @property
    def total_seconds(self) -> int:
        """
        Returns the total number of seconds for the time resolution.

        :return: The total number of seconds.
        :rtype: int
        """
        lookup = {
            TimeResolution.RAW: 5,
            TimeResolution.MIN5: 300,
            TimeResolution.HOUR: 3600,
            TimeResolution.DAY: 86400,
            TimeResolution.WEEK: 604800,
            TimeResolution.MONTH: 2592000,  # 30 days
            TimeResolution.YEAR: 31536000,  # 365 days
        }
        return lookup[self]

    @property
    def timedelta(self):
        """
        Returns the timedelta for the time resolution.

        :return: The timedelta.
        :rtype: timedelta
        """
        return timedelta(seconds=self.total_seconds)

    def __eq__(self, other) -> bool:
        """
        Checks if this TimeResolution is equal to another.

        :param other: Another TimeResolution or string.
        :type other: TimeResolution | str
        :return: True if equal, False otherwise.
        :rtype: bool
        """
        if isinstance(other, str):
            other = self.__class__(other)
        return self is other

    def __lt__(self, other) -> bool:
        """
        Checks if this TimeResolution is less than another.

        :param other: Another TimeResolution or string.
        :type other: TimeResolution | str
        :return: True if less than, False otherwise.
        :rtype: bool
        """
        if isinstance(other, str):
            other = self.__class__(other)
        return self._order > other._order


T = TypeVar("T", bound=Union[datetime, None])


def _norm(
    dt: T, resolution: TimeResolution | None = None, tz: tzinfo | None = None
) -> T:
    if dt is None:
        return cast(T, None)
    if dt.tzinfo is None:
        dt = dt.astimezone(tz) if tz else dt.astimezone(get_localzone())
    if resolution:
        dt = timestep_start(resolution, dt)
    return dt


class SubDateRange:
    """
    Represents a range of dates with a start and an end.

    If input datetimes are tz-naive, the tzinfo will be replaced with UTC. If they're tz-aware, the existing tzinfo will be converted to UTC.

    :param start: The starting date of the range.
    :type start: Optional[datetime]
    :param end: The ending date of the range.
    :type end: Optional[datetime]

    Examples:
        >>> from datetime import datetime
        >>> sdr = SubDateRange(datetime(2023, 1, 1), datetime(2023, 1, 2))
        >>> '[2023-01-01 00:00:00' in str(sdr)
        True
        >>> sdr.tz_aware
        True
    """

    def __init__(
        self, start: Optional[datetime] = None, end: Optional[datetime] = None
    ):
        """
        Initialize a SubDateRange object.
        :param start: The starting date of the range.
        :type start: Optional[datetime]
        :param end: The ending date of the range.
        :type end: Optional[datetime]
        """

        self.start = _norm(start)
        self.end = _norm(end)
        self.check_start_end()

    def __repr__(self) -> str:
        return f"[{self.start}, {self.end}]"

    @property
    def tz_aware(self) -> bool:
        """
        Checks if the SubDateRange is timezone-aware.

        :return: True if timezone-aware, False otherwise.
        :rtype: bool
        """
        return (self.start is not None and self.start.tzinfo is not None) or (
            self.end is not None and self.end.tzinfo is not None
        )

    @property
    def tzinfo(self) -> Optional[tzinfo]:
        """
        Returns the tzinfo of the SubDateRange.

        :return: The tzinfo of the SubDateRange.
        :rtype: Optional[tzinfo]
        """
        if self.start is not None and self.start.tzinfo is not None:
            return self.start.tzinfo
        if self.end is not None and self.end.tzinfo is not None:
            return self.end.tzinfo
        return None

    def check_start_end(self):
        """
        Ensure start is before end and they are not equal.

        :raises TypeError: If the start date is after the end date or both are equal.
        """
        if self.start is not None and self.end is not None:
            if self.end < self.start:
                raise TypeError(
                    f"End date ({self.end}) cannot be before start date ({self.start})"
                )
            elif self.start == self.end:
                raise TypeError(f"Start and end dates cannot be equal: {self.start}")
        if (self.start is not None and self.end is not None) and (
            self.start.tzinfo != self.end.tzinfo
        ):
            raise TypeError("Start and end dates must have the same tzinfo.")
        if not self.tz_aware and not self.empty:
            raise TypeError("Both start and end dates must be timezone-aware.")

    def overlap(self, other: SubDateRange) -> Optional[SubDateRange]:
        """
        Returns the overlapping portion of two SubDateRange objects.
        If there's no overlap, returns None.

        :param other: Another SubDateRange object.
        :type other: SubDateRange
        :return: The overlapping SubDateRange or None if no overlap.
        :rtype: Optional[SubDateRange]
        """
        other = other.astimezone(self.tzinfo)
        latest_start = (
            max(self.start, other.start)
            if self.start and other.start
            else self.start or other.start
        )
        earliest_end = (
            min(self.end, other.end)
            if self.end and other.end
            else self.end or other.end
        )
        if latest_start is None or earliest_end is None or latest_start < earliest_end:
            return SubDateRange(latest_start, earliest_end)
        return None

    def merge(self, other: SubDateRange) -> SubDateRange:
        """
        Merge this range with another, assuming they overlap.

        :param other: The other SubDateRange to merge with.
        :type other: SubDateRange
        :return: A new merged SubDateRange.
        :rtype: SubDateRange
        :raises ValueError: If the ranges do not overlap.
        """
        other = other.astimezone(self.tzinfo)
        if self.overlap(other):
            start = None
            if self.start is not None and other.start is not None:
                start = min(self.start, other.start)
            else:
                start = self.start if self.start is not None else other.start

            end = None
            if self.end is not None and other.end is not None:
                end = max(self.end, other.end)
            else:
                end = self.end if self.end is not None else other.end

            return SubDateRange(start=start, end=end)
        else:
            raise ValueError(f"Ranges do not overlap: {self} and {other}")

    def __sub__(self, other: SubDateRange) -> List[SubDateRange]:
        """
        Subtract another range from this range.

        :param other: The other SubDateRange to subtract.
        :type other: SubDateRange
        :return: A list of SubDateRange objects representing the non-overlapping ranges.
        :rtype: List[SubDateRange]
        """
        other = other.astimezone(self.tzinfo)
        if overlap := self.overlap(other):
            if self.start == overlap.start and self.end == overlap.end:
                return []
            elif self.start == overlap.start:
                return [SubDateRange(overlap.end, self.end)]
            elif self.end == overlap.end:
                return [SubDateRange(self.start, overlap.start)]
            else:
                return [
                    SubDateRange(self.start, overlap.start),
                    SubDateRange(overlap.end, self.end),
                ]
        return [self]

    def __contains__(self, date: Union[datetime, SubDateRange, "DateRange"]) -> bool:
        """
        Check if a specific date or DateRange is contained within this range.

        :param date: A datetime object, SubDateRange, or DateRange.
        :type date: Union[datetime, SubDateRange, DateRange]
        :return: True if contained, False otherwise.
        :rtype: bool
        """
        if isinstance(date, datetime):
            date = _norm(date)
            return (self.start is None or self.start <= date) and (
                self.end is None or date < self.end
            )
        elif isinstance(date, SubDateRange):
            return (
                self.start is None
                or (date.start is not None and self.start <= date.start)
            ) and (self.end is None or (date.end is not None and self.end >= date.end))
        elif isinstance(date, DateRange):
            return all(dr in self for dr in date.ranges)
        return False

    def __lt__(self, other: SubDateRange) -> bool:
        """
        Compare SubDateRange objects based on their start date.

        :param other: Another SubDateRange to compare with.
        :type other: SubDateRange
        :return: True if this range starts before the other range.
        :rtype: bool
        """
        if self.start is None:
            return other.start is not None
        if other.start is None:
            return False
        return self.start < other.start

    def __str__(self):
        """
        Returns a string representation of the SubDateRange object.

        :return: A string in the format "[start, end]".
        :rtype: str
        """
        return f"[{self.start}, {self.end}]"

    def astimezone(self, tz: Optional[tzinfo] = None) -> "SubDateRange":
        """
        Convert the SubDateRange to a new timezone.

        :param tz: The new timezone.
        :type tz: Optional[tzinfo]
        :return: The SubDateRange with start and end converted to the new timezone.
        :rtype: SubDateRange
        """
        if self.start is not None:
            self.start = self.start.astimezone(tz)
        if self.end is not None:
            self.end = self.end.astimezone(tz)

        return self

    @property
    def empty(self) -> bool:
        """
        Checks if the SubDateRange is empty.

        :return: True if empty, False otherwise.
        :rtype: bool
        """
        return self.start is None and self.end is None


class DateRange:
    """
    Represents a collection of SubDateRange objects.

    :param ranges: A list of SubDateRange objects.
    :type ranges: List[SubDateRange]
    :param resolution: The time resolution of the DateRange.
    :type resolution: TimeResolution

    Examples:
        >>> from datetime import datetime
        >>> from preheat_open.time import SubDateRange, DateRange, TimeResolution
        >>> sdr = SubDateRange(datetime(2023, 1, 1), datetime(2023, 1, 2))
        >>> dr = DateRange([sdr], resolution=TimeResolution.DAY)
        >>> print(dr)
        DateRange(2023-01-01--2023-01-02, continuous, resolution=TimeResolution.DAY)
    """

    def __init__(
        self,
        ranges: list[SubDateRange] | None = None,
        resolution: TimeResolution = TimeResolution.RAW,
        start: datetime | None = None,
        end: datetime | None = None,
        tz: Optional[tzinfo] = None,
    ):
        """
        Initialize a DateRange object.

        :param ranges: A list of SubDateRange objects.
        :type ranges: List[SubDateRange]
        :param resolution: The time resolution of the DateRange.
        :type resolution: TimeResolution
        :param start: Optional start datetime.
        :type start: Optional[datetime]
        :param end: Optional end datetime.
        :type end: Optional[datetime]
        """
        self.ranges = ranges or []
        self.resolution = resolution

        start = _norm(dt=start, resolution=resolution, tz=tz)
        end = _norm(dt=end, resolution=resolution, tz=tz)

        if start is not None or end is not None:
            self.ranges.append(SubDateRange(start, end))
        self.ranges.sort()
        self.remove_overlaps()

    def __repr__(self) -> str:
        """
        Returns a string representation of the DateRange object.

        :return: A string describing the DateRange.
        :rtype: str
        """
        if self.empty:
            return f"{self.__class__.__name__}(empty)"
        start = (
            min(r.start for r in self.ranges if r.start is not None)
            if not all(r.start is None for r in self.ranges)
            else None
        )
        end = (
            max(r.end for r in self.ranges if r.end is not None)
            if not all(r.end is None for r in self.ranges)
            else None
        )
        start_str = start.strftime("%Y-%m-%d") if start else "None"
        end_str = end.strftime("%Y-%m-%d") if end else "None"
        segmented = "segmented" if self.segmented else "continuous"
        return f"{self.__class__.__name__}({start_str}--{end_str}, {segmented}, resolution={self.resolution.__repr__()})"

    def to_pandas_date_range(self):
        """
        Convert the DateRange to a pandas DateRange object.

        :return: A pandas DateRange object.
        :rtype: pandas.core.indexes.datetimes.DatetimeIndex
        """
        return pd.date_range(
            start=self.lstart,
            end=self.rend,
            freq=self.resolution.pandas_alias,
            inclusive="left",
        )

    @property
    def lstart(self) -> Optional[datetime]:
        """
        Returns the start date of the DateRange.

        :return: The start date.
        :rtype: Optional[datetime]
        """
        if self.ranges:
            return min(
                (r.start for r in self.ranges if r.start is not None), default=None
            )
        return None

    @property
    def rend(self) -> Optional[datetime]:
        """
        Returns the end date of the DateRange.

        :return: The end date.
        :rtype: Optional[datetime]
        """
        if self.ranges:
            return max((r.end for r in self.ranges if r.end is not None), default=None)
        return None

    @property
    def tz_aware(self) -> bool:
        """
        Checks if the DateRange is timezone-aware.

        :return: True if timezone-aware, False otherwise.
        :rtype: bool
        """
        if self.ranges:
            return all(r.tz_aware for r in self.ranges)
        return False

    def astimezone(self, tz: Optional[tzinfo] = None) -> "DateRange":
        """
        Convert the DateRange to a new timezone.

        :param tz: The new timezone.
        :type tz: Optional[tzinfo]
        """
        for r in self.ranges:
            r.astimezone(tz)

        return self

    @property
    def empty(self) -> bool:
        """
        Checks if the DateRange is empty.

        :return: True if empty, False otherwise.
        :rtype: bool
        """
        for r in self.ranges:
            if not r.empty:
                return False
        return True

    @property
    def segmented(self) -> bool:
        """
        Checks if the DateRange is segmented.

        :return: True if segmented, False otherwise.
        :rtype: bool
        """
        return len(self.ranges) > 1

    def remove_overlaps(self):
        """
        Remove overlapping ranges by merging them.
        """
        if self.ranges:
            range_iter = iter(self.ranges)
            merged_ranges = [next(range_iter)]

            for current_range in range_iter:
                overlap = merged_ranges[-1].overlap(current_range)
                if overlap is None:
                    merged_ranges.append(current_range)
                else:
                    merged_ranges[-1] = merged_ranges[-1].merge(current_range)

            self.ranges = merged_ranges

    def __merge_resolutions(self, other: "DateRange") -> TimeResolution:
        """
        Determine the resolution of the merged DateRange.

        :param other: Another DateRange object.
        :type other: DateRange
        :return: The resolution of the merged DateRange.
        :rtype: Optional[TimeResolution]
        """
        if self.resolution == other.resolution:
            return self.resolution
        elif self.resolution == TimeResolution.RAW and self.empty:
            return other.resolution
        elif other.resolution == TimeResolution.RAW and other.empty:
            return self.resolution
        else:
            raise ValueError("Cannot merge DateRanges with different resolutions.")

    def __add__(self, other: "DateRange") -> "DateRange":
        """
        Overload the + operator to add two DateRange objects.

        :param other: Another DateRange object to add.
        :type other: DateRange
        :return: A new DateRange object with merged ranges.
        :rtype: DateRange
        """
        return DateRange(
            ranges=self.ranges + other.ranges,
            resolution=self.__merge_resolutions(other),
        )

    def __sub__(self, other: "DateRange") -> "DateRange":
        """
        Overload the - operator to subtract ranges in other from self.

        :param other: Another DateRange object to subtract.
        :type other: DateRange
        :return: A new DateRange object with the non-overlapping ranges.
        :rtype: DateRange
        """
        if self.empty or other.empty:
            return self

        remaining_ranges = []

        for i in self.ranges:
            current_ranges = [i]  # Start with the original range

            # Subtract each overlapping range from other
            for j in other.ranges:
                new_current_ranges = []
                for current_range in current_ranges:
                    # Subtract j from current_range
                    new_current_ranges.extend(current_range - j)
                current_ranges = new_current_ranges

            # Add whatever remains after all subtractions
            remaining_ranges.extend(current_ranges)

        return DateRange(
            ranges=remaining_ranges, resolution=self.__merge_resolutions(other)
        )

    def __contains__(self, date: Union[datetime, SubDateRange, "DateRange"]) -> bool:
        """
        Check if a specific date or DateRange is contained within any of the ranges.

        :param date: A datetime object, SubDateRange, or DateRange.
        :type date: Union[datetime, SubDateRange, DateRange]
        :return: True if contained, False otherwise.
        :rtype: bool
        """
        if isinstance(date, datetime):
            return any(date in dr for dr in self.ranges)
        elif isinstance(date, SubDateRange):
            return any(date in dr for dr in self.ranges)
        elif isinstance(date, DateRange):
            _ = self.__merge_resolutions(date)
            return all(dr in self for dr in date.ranges)
        return False

    def intersection(self, other: "DateRange") -> "DateRange":
        """
        Return the intersection of two DateRange objects.

        :param other: Another DateRange object.
        :type other: DateRange
        :return: A new DateRange object representing the intersections.
        :rtype: DateRange
        """
        resolution = self.__merge_resolutions(other)
        intersections = []
        for range1 in self.ranges:
            for range2 in other.ranges:
                latest_start = (
                    max(range1.start, range2.start)
                    if range1.start and range2.start
                    else range1.start or range2.start
                )
                earliest_end = (
                    min(range1.end, range2.end)
                    if range1.end and range2.end
                    else range1.end or range2.end
                )
                if (
                    latest_start is None
                    or earliest_end is None
                    or latest_start < earliest_end
                ):
                    intersections.append(SubDateRange(latest_start, earliest_end))
        return DateRange(ranges=intersections, resolution=resolution)

    def gaps(self) -> "DateRange":
        """
        Calculate the gaps between consecutive DateRanges.

        :return: A new DateRange object representing the gaps between ranges.
        :rtype: DateRange
        """
        self.remove_overlaps()
        gaps = []
        for i in range(1, len(self.ranges)):
            prev_end = self.ranges[i - 1].end
            current_start = self.ranges[i].start
            if (
                prev_end is not None
                and current_start is not None
                and current_start > prev_end
            ):
                gaps.append(SubDateRange(prev_end, current_start))
        return DateRange(gaps, resolution=self.resolution)

    def union(self) -> "DateRange":
        """
        Return a DateRange covering the entire period, including gaps.

        :return: A new DateRange covering the full period from the earliest start to the latest end.
        :rtype: DateRange
        """
        return DateRange(
            start=self.ranges[0].start,
            end=self.ranges[-1].end,
            resolution=self.resolution,
        )

    def __radd__(self, other: Union[int, "DateRange"]) -> "DateRange":
        """
        Support the sum() function to combine multiple DateRanges.

        :param other: Another DateRange object or integer for sum initialization.
        :type other: Union[DateRange, int]
        :return: A combined DateRange object.
        :rtype: DateRange
        """
        if other == 0:
            return self
        if isinstance(other, int):
            return self
        return self + other

    def iter_ranges(
        self, freq: timedelta
    ) -> Generator[tuple[datetime, datetime], None, None]:
        """
        Iterate over the ranges of the DateRange.

        :return: A generator yielding tuples of start and end datetimes.
        :rtype: Generator[tuple[datetime, datetime], None, None]
        """
        if self.rend is None or self.lstart is None:
            raise ValueError("DateRange must have both start and end dates defined.")
        n = math.ceil((self.rend - self.lstart) / freq)
        end = self.lstart
        for i in range(1, n):
            start = end
            end = self.lstart + i * freq
            yield start, end
        yield end, self.rend


def timestep_start(step: Enum | str, t: datetime) -> datetime:
    """
    Computes the start of the current timestep.

    :param step: The time resolution step.
    :type step: Enum | str
    :param t: The datetime for which to evaluate the step start.
    :type t: datetime
    :return: The start time of the timestep.
    :rtype: datetime

    Examples:
        >>> from datetime import datetime
        >>> from preheat_open.time import timestep_start, TimeResolution
        >>> t = datetime(2023, 1, 1, 12, 34, 56)
        >>> print(timestep_start(TimeResolution.HOUR, t))
        2023-01-01 12:00:00
    """
    if isinstance(step, Enum) and isinstance(step.value, str):
        step = step.value

    if step is None or step == "raw":
        return t
    elif step in ["second", "1s"]:
        t_start = t.replace(microsecond=0)
    elif step == "15s":
        sec_start = int(t.second / 15) * 15
        t_start = t.replace(microsecond=0, second=sec_start)
    elif step == "30s":
        sec_start = int(t.second / 30) * 30
        t_start = t.replace(microsecond=0, second=sec_start)
    elif step == "1min":
        t_start = t.replace(microsecond=0, second=0)
    elif step in ["minute", "5min"]:
        min_start = int(t.minute / 5) * 5
        t_start = t.replace(microsecond=0, second=0, minute=min_start)
    elif step == "15min":
        min_start = int(t.minute / 15) * 15
        t_start = t.replace(microsecond=0, second=0, minute=min_start)
    elif step == "30min":
        min_start = int(t.minute / 30) * 30
        t_start = t.replace(microsecond=0, second=0, minute=min_start)
    elif step == "hour":
        t_start = t.replace(microsecond=0, second=0, minute=0)
    elif step == "day":
        t_start = t.replace(microsecond=0, second=0, minute=0, hour=0)
    elif step == "month":
        t_start = t.replace(microsecond=0, second=0, minute=0, hour=0, day=1)
    elif step == "year":
        t_start = t.replace(microsecond=0, second=0, minute=0, hour=0, day=1, month=1)
    else:
        raise ValueError(f"Unknown step: {step}")

    return t_start
