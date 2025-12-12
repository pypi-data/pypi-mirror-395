"""
loadable_types.py

This module defines classes related to loadable data types, schedules, and comfort profiles.

Classes:
    LoadableDataType
    LoadableData
    OperationType
    ScheduleItem
    SetpointSchedule
    ComponentData
    Setpoint
    ComfortProfile
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import tzinfo
from enum import Enum
from typing import Any, Callable, Optional, TypeVar

import numpy as np
import pandas as pd

from .time import DateRange, datetime


@dataclass
class LoadableDataType(ABC):
    """
    Represents data that can be loaded for a specific date range.

    :ivar loaded_date_range: The date range for the loaded data.
    :vartype loaded_date_range: DateRange
    """

    @abstractmethod
    def get_data(self, date_range: DateRange) -> Any:
        """
        Retrieves data for the specified date range.

        :param date_range: The date range for which to retrieve data.
        :type date_range: DateRange
        :return: The data for the specified date range.
        :rtype: Any
        """

    @abstractmethod
    def add_data(self, data: Any) -> None:
        """
        Adds data to the loaded data.

        :param data: The data to add.
        :type data: Any
        """


T = TypeVar("T", bound=LoadableDataType)


@dataclass
class LoadableData:
    data: T
    date_range: DateRange = field(default_factory=DateRange)
    getter: Callable | None = None
    setter: Callable | None = None

    def get(self, date_range: DateRange) -> T:
        date_range_to_load = self.request(date_range)
        if not date_range_to_load.empty and self.getter is not None:
            loaded_data = self.getter(date_range_to_load)
            self.update(date_range=date_range_to_load, data=loaded_data)

        return self.data.get_data(date_range)

    def request(self, date_range: DateRange) -> DateRange:
        """
        Returns the date range that needs to be loaded.
        """
        return date_range - self.date_range

    def update(self, date_range: DateRange, data) -> None:
        self.data.add_data(data)
        self.date_range += date_range

    def set(self, data: LoadableDataType) -> None:
        self.data = data
        if self.setter is None:
            raise ValueError("No setter function defined")
        else:
            self.setter(data)

    def __getattr__(self, name: str) -> Any:
        """
        Retrieves an attribute from the object.

        :param name: The name of the attribute to retrieve.
        :type name: str
        :return: The value of the attribute.
        :rtype: Any
        """
        return getattr(self.data, name)


class OperationType(Enum):
    """
    Enum representing the type of operation for a schedule item.

    Attributes:
        NORMAL: Normal operation.
        CLOSED: Closed operation.
        OFF: Off operation.
    """

    NORMAL = "NORMAL"
    CLOSED = "CLOSED"
    OFF = "OFF"

    def __repr__(self):
        """
        Returns a string representation of the OperationType enum.

        :return: The name of the enum member.
        :rtype: str
        """
        return self.name


class InvalidScheduleError(Exception):
    """
    Exception raised for errors in the schedule.
    """


class ScheduleReason(Enum):
    """
    Enum representing the reasons for a schedule item.
    """

    SUMMER_MODE = "SUMMER_MODE"
    FALLBACK = "FALLBACK"
    LEARNING_MODE = "LEARNING_MODE"
    LEGIONELLA_PREVENTION = "LEGIONELLA_PREVENTION"
    MISSING_DATA = "MISSING_DATA"
    USER_OVERRIDE = "USER_OVERRIDE"
    MANUAL_CONTROL = "MANUAL_CONTROL"
    BOOST_MOD = "BOOST_MOD"
    FROST_PROTECTION = "FROST_PROTECTION"
    NIGHT_SETBACK = "NIGHT_SETBACK"
    WEATHER_COMPENSATION = "WEATHER_COMPENSATION"
    DEMAND_RESPONSE = "DEMAND_RESPONSE"
    MAINTENANCE_MODE = "MAINTENANCE_MODE"
    NORMAL_MODE = "NORMAL_MODE"

    def __repr__(self):
        """
        Returns a string representation of the ScheduleReason enum.

        :return: The name of the enum member.
        :rtype: str
        """
        return self.name


@dataclass
class ScheduleItem:
    """
    Represents an item in a schedule.

    :ivar start: The start time of the schedule item.
    :vartype start: datetime
    :ivar value: The value of the schedule item.
    :vartype value: float
    :ivar operation: The operation type of the schedule item.
    :vartype operation: OperationType
    :ivar owner_id: The ID of the owner of the schedule item.
    :vartype owner_id: int, optional
    """

    start: datetime
    value: float
    operation: OperationType = OperationType.NORMAL
    reason: ScheduleReason = ScheduleReason.NORMAL_MODE
    owner_id: int | None = None

    def __post_init__(self):
        """
        Post-initialization processing to validate the schedule item.
        """
        if self.value is None:
            raise InvalidScheduleError("Schedule values are not allowed to be None")
        if not isinstance(self.operation, OperationType):
            self.operation = OperationType(self.operation)
        if not isinstance(self.reason, (type(None), ScheduleReason)):
            self.reason = ScheduleReason(self.reason)
        if np.isinf(self.value):
            raise InvalidScheduleError("Schedule values are not allowed to be infinite")

    def __lt__(self, other):
        """
        Compares this schedule item with another for sorting.

        :param other: The other schedule item to compare with.
        :type other: ScheduleItem
        :return: True if this schedule item is less than the other, False otherwise.
        :rtype: bool
        :raises ValueError: If the other object is not a ScheduleItem.
        """
        if not isinstance(other, ScheduleItem):
            raise ValueError(f"Cannot compare ScheduleItem to {type(other)}")
        return self.start < other.start

    def __repr__(self) -> str:
        """
        Returns a string representation of the ScheduleItem object.

        :return: A string in the format "YYYY-MM-DDTHH:MM:SS value operation".
        :rtype: str
        """
        return f"{self.start.replace(microsecond=0).isoformat()} {self.value:.2f} {self.operation.__repr__()}"


@dataclass
class SetpointSchedule(LoadableDataType):
    """
    Represents a setpoint schedule containing multiple schedule items.

    :ivar parent: The parent unit of the setpoint schedule.
    :vartype parent: Unit, optional
    :ivar schedule: A list of schedule items.
    :vartype schedule: list[ScheduleItem]
    """

    schedule: list[ScheduleItem] = field(default_factory=list)

    def __repr__(self) -> str:
        """
        Returns a string representation of the SetpointSchedule object.

        :return: A string describing the setpoint schedule and its items.
        :rtype: str
        """
        lines = [f"Control schedule:"]
        if len(self.schedule) > 20:
            lines.extend([item.__repr__() for item in self.schedule[:10]])
            lines.append("...")
            lines.extend([item.__repr__() for item in self.schedule[-10:]])
        else:
            lines.extend([item.__repr__() for item in self.schedule])
        return "\n".join(lines)

    @property
    def empty(self):
        """
        Checks if the setpoint schedule is empty.

        :return: True if the schedule is empty, False otherwise.
        :rtype: bool
        """
        return len(self.schedule) == 0

    def astimezone(self, tz: tzinfo) -> SetpointSchedule:
        """
        Converts the setpoint schedule to the specified timezone.

        :param tz: The timezone to convert to.
        :type tz: tzinfo
        :return: A SetpointSchedule object with the schedule items converted to the specified timezone.
        :rtype: SetpointSchedule
        """
        return SetpointSchedule(
            schedule=[
                ScheduleItem(
                    start=item.start.astimezone(tz),
                    value=item.value,
                    operation=item.operation,
                    owner_id=item.owner_id,
                    reason=item.reason,
                )
                for item in self.schedule
            ]
        )

    def get_data(self, date_range: DateRange) -> SetpointSchedule:
        """
        Retrieves schedule items for the specified date range.

        :param date_range: The date range for which to retrieve schedule items.
        :type date_range: DateRange
        :return: A tuple containing the date range and the schedule items.
        :rtype: tuple[DateRange, list[ScheduleItem]]
        """
        schedule = [s for s in self.schedule if s.start in date_range]
        return SetpointSchedule(schedule=schedule)

    def add_data(self, data: SetpointSchedule) -> None:
        """
        Adds schedule items to the setpoint schedule.

        :param data: The schedule items to add.
        :type data: SetpointSchedule
        """
        self.schedule = [
            s for s in self.schedule if all(s.start != d.start for d in data.schedule)
        ]
        self.schedule.extend(data.schedule)

    def to_frame(self) -> pd.DataFrame:
        """
        Converts the setpoint schedule to a pandas DataFrame.

        :return: A DataFrame containing the schedule items.
        :rtype: pd.DataFrame
        """
        df = pd.DataFrame(
            [
                (
                    item.start,
                    item.value,
                    item.operation.value,
                    item.reason.value if item.reason else None,
                    item.owner_id,
                )
                for item in self.schedule
            ],
            columns=["time", "value", "operation", "reason", "owner_id"],
        )
        df.set_index("time", inplace=True)
        return df

    @classmethod
    def from_frame(cls, frame: pd.DataFrame) -> SetpointSchedule:
        """
        Creates a SetpointSchedule object from a pandas DataFrame.

        :param frame: The DataFrame containing the schedule items.
        :type frame: pd.DataFrame
        :param parent: The parent unit of the setpoint schedule.
        :type parent: Unit
        :return: A SetpointSchedule object.
        :rtype: SetpointSchedule
        """
        return cls(
            schedule=[
                ScheduleItem(
                    start=index,
                    value=row["value"],
                    operation=OperationType(row["operation"]),
                    owner_id=row["owner_id"] if "owner_id" in frame.columns else None,
                )
                for index, row in frame.iterrows()
            ],
        )

    @classmethod
    def from_series(cls, series: pd.Series) -> SetpointSchedule:
        """
        Creates a SetpointSchedule object from a pandas Series.

        :param series: The Series containing the schedule items.
        :type series: pd.Series
        :param parent: The parent unit of the setpoint schedule.
        :type parent: Unit
        :return: A SetpointSchedule object.
        :rtype: SetpointSchedule
        """
        return cls(
            schedule=[
                ScheduleItem(
                    start=index,
                    value=value,
                    operation=OperationType.NORMAL,
                )
                for index, value in series.items()
            ],
        )


@dataclass
class ComponentData(LoadableDataType):
    """
    Represents data for a component, including measurements and date range.

    :ivar date_range: The date range for the component data.
    :vartype date_range: DateRange
    :ivar measurements: The measurements for the component data.
    :vartype measurements: pd.Series
    """

    measurements: pd.Series = field(
        default_factory=lambda: pd.Series(index=pd.to_datetime([]))
    )

    def get_data(
        self,
        date_range: DateRange,
    ) -> ComponentData:
        """
        Retrieves measurements for the specified date range.

        :param date_range: The date range for which to retrieve measurements.
        :type date_range: DateRange
        :return: A tuple containing the date range and the measurements.
        :rtype: tuple[DateRange, pd.Series]
        """
        m = self.measurements
        if m.empty:
            return ComponentData(measurements=m)
        else:
            return ComponentData(
                measurements=m.loc[
                    (date_range.lstart <= m.index) & (m.index < date_range.rend)
                ]
            )

    def __repr__(self) -> str:
        """
        Returns a string representation of the ComponentData object.

        :return: A string describing the component data.
        :rtype: str
        """
        return f"{self.__class__.__name__}"

    def add_data(self, data: ComponentData | None) -> None:
        """
        Adds measurements to the component data.

        :param data: The measurements to add.
        :type data: pd.Series | None
        """
        series = data.measurements if data is not None else None
        if series is not None:
            df_col = series.dropna()
            if self.measurements.empty:
                self.measurements = df_col
            else:
                new_data = pd.concat(
                    [None if df.empty else df for df in [df_col, self.measurements]]
                )
                self.measurements = new_data[~new_data.index.duplicated(keep="first")]


@dataclass
class Setpoint:
    """
    Represents a setpoint for a specific time.

    :ivar max: The maximum value of the setpoint.
    :vartype max: Optional[float]
    :ivar min: The minimum value of the setpoint.
    :vartype min: Optional[float]
    :ivar setpoint: The setpoint value.
    :vartype setpoint: Optional[float]
    :ivar time: The time at which the setpoint is applied.
    :vartype time: Optional[datetime]
    :ivar vacation: Indicates if the setpoint is for a vacation period.
    :vartype vacation: bool
    """

    max: Optional[float] = None
    min: Optional[float] = None
    setpoint: Optional[float] = None
    time: Optional[datetime] = None
    vacation: bool = False
    override: bool = False

    def __repr__(self) -> str:
        """
        Returns a string representation of the Setpoint object.

        :return: A string in the format "YYYY-MM-DDTHH:MM:SS setpoint vacation".
        :rtype: str
        """
        time = self.time.replace(microsecond=0).isoformat() if self.time else "None"
        return f"{time} {self.setpoint:.1f} {self.vacation}"


@dataclass
class ComfortProfiles(LoadableDataType):
    """
    Represents a collection of comfort profiles.


    """

    profiles: dict[int, ComfortProfile] = field(default_factory=dict)

    def __repr__(self) -> str:
        """
        Returns a string representation of the ComfortProfiles object.

        :return: A string describing the comfort profiles.
        :rtype: str
        """
        return f"Comfort profiles: {list(self.profiles.keys())}"

    def astimezone(self, tz: tzinfo) -> ComfortProfiles:
        """
        Converts the comfort profiles to the specified timezone.

        :param tz: The timezone to convert to.
        :type tz: tzinfo
        :return: A ComfortProfiles object with the comfort profiles converted to the specified timezone.
        :rtype: ComfortProfiles
        """
        return ComfortProfiles(
            profiles={
                id: profile.astimezone(tz) for id, profile in self.profiles.items()
            }
        )

    def get_data(self, date_range: DateRange) -> ComfortProfiles:
        """
        Retrieves comfort profiles for the specified date range.

        :param date_range: The date range for which to retrieve comfort profiles.
        :type date_range: DateRange
        :return: A tuple containing the date range and the comfort profiles.
        :rtype: tuple[DateRange, ComfortProfiles]
        """
        profiles = {
            id: profile.get_data(date_range) for id, profile in self.profiles.items()
        }
        return ComfortProfiles(profiles=profiles)

    def add_data(self, data: ComfortProfiles) -> None:
        """
        Adds comfort profiles to the collection.

        :param data: The comfort profiles to add.
        :type data: ComfortProfiles
        """
        for id, profile in data.profiles.items():
            if id in self.profiles:
                self.profiles[id].add_data(profile)
            else:
                self.profiles[id] = profile

    def get_profile(self, id: int) -> ComfortProfile:
        """
        Retrieves a comfort profile by ID.

        :param id: The ID of the comfort profile to retrieve.
        :type id: int
        :return: The comfort profile with the specified ID.
        :rtype: ComfortProfile
        """
        return self.profiles.get(id)


@dataclass
class ComfortProfile(LoadableDataType):
    """
    Represents a comfort profile containing multiple setpoints.

    :ivar id: The unique identifier of the comfort profile.
    :vartype id: Optional[int]
    :ivar name: The name of the comfort profile.
    :vartype name: str
    :ivar setpoints: A list of setpoints associated with the comfort profile.
    :vartype setpoints: list[Setpoint]
    """

    id: Optional[int] = None
    name: str = ""
    setpoints: list[Setpoint] = field(default_factory=list)
    flexibility: float | None = None

    def __repr__(self) -> str:
        """
        Returns a string representation of the ComfortProfile object.

        :return: A string describing the comfort profile and its setpoints.
        :rtype: str
        """
        lines = [
            f"Comfort profile, {self.id}, {self.name}:",
            "Time, Setpoint, Vacation",
        ]
        if len(self.setpoints) > 20:
            lines.extend([item.__repr__() for item in self.setpoints[:10]])
            lines.append("...")
            lines.extend([item.__repr__() for item in self.setpoints[-10:]])
        else:
            lines.extend([item.__repr__() for item in self.setpoints])
        return "\n".join(lines)

    def astimezone(self, tz: tzinfo) -> ComfortProfile:
        """
        Converts the comfort profile to the specified timezone.

        :param tz: The timezone to convert to.
        :type tz: tzinfo
        :return: A ComfortProfile object with the setpoints converted to the specified timezone.
        :rtype: ComfortProfile
        """
        return ComfortProfile(
            id=self.id,
            name=self.name,
            setpoints=[
                Setpoint(
                    time=item.time.astimezone(tz),
                    setpoint=item.setpoint,
                    min=item.min,
                    max=item.max,
                    vacation=item.vacation,
                )
                for item in self.setpoints
            ],
        )

    def get_data(self, date_range: DateRange) -> ComfortProfile:
        """
        Retrieves setpoints for the specified date range.

        :param date_range: The date range for which to retrieve setpoints.
        :type date_range: DateRange
        :return: A tuple containing the date range and the setpoints.
        :rtype: tuple[DateRange, list[Setpoint]]
        """
        setpoints = [
            s for s in self.setpoints if date_range.lstart <= s.time < date_range.rend
        ]
        return ComfortProfile(id=self.id, name=self.name, setpoints=setpoints)

    def add_data(self, data: ComfortProfile) -> None:
        """
        Adds setpoints to the comfort profile.

        :param data: The setpoints to add.
        :type data: ComfortProfile
        """
        self.setpoints = [
            s for s in self.setpoints if all(s.time != d.time for d in data.setpoints)
        ]
        self.setpoints.extend(data.setpoints)

    def to_frame(self) -> pd.DataFrame:
        """
        Converts the comfort profile to a pandas DataFrame.

        :return: A DataFrame containing the setpoints.
        :rtype: pd.DataFrame
        """
        return pd.DataFrame(
            data=[
                [s.time, s.setpoint, s.min, s.max, s.vacation] for s in self.setpoints
            ],
            columns=["time", "setpoint", "min", "max", "vacation"],
        ).set_index("time")


@dataclass
class ElectricityPriceItem:
    """
    Represents an electricity price item.

    :ivar start: The start datetime of the electricity price item.
    :vartype start: datetime
    :ivar end: The end datetime of the electricity price item.
    :vartype end: datetime
    :ivar price: The price of the electricity price item.
    :vartype price: float
    :ivar currency: The currency of the electricity price item.
    :vartype currency: str
    """

    time: datetime
    value: float

    def __le__(self, other: "ElectricityPriceItem") -> bool:
        """
        Compares two electricity price items for less than or equal to.

        :param other: The other electricity price item.
        :type other: ElectricityPriceItem
        :return: True if less than or equal to, False otherwise.
        :rtype: bool
        """
        return self.time <= other.time

    def __lt__(self, other: "ElectricityPriceItem") -> bool:
        """
        Compares two electricity price items for less than.

        :param other: The other electricity price item.
        :type other: ElectricityPriceItem
        :return: True if less than, False otherwise.
        :rtype: bool
        """
        return self.time < other.time


@dataclass
class ElectricityPrices(LoadableDataType):
    """
    Represents electricity prices.

    :ivar data: A list of electricity price items.
    :vartype data: list[ElectricityPriceItem]
    :ivar tariff_included: Indicates if the tariff is included in the prices.
    :vartype tariff_included: bool
    :ivar vat_included: Indicates if the VAT is included in the prices.
    :vartype vat_included: bool
    :ivar unit: The unit of the electricity prices.
    :vartype unit: Unit
    """

    data: list[ElectricityPriceItem] = field(default_factory=list)
    tariff_included: bool = None
    vat_included: bool = None

    def get_data(self, date_range: DateRange) -> ElectricityPrices:
        return ElectricityPrices(
            data=[
                x for x in self.data if date_range.lstart <= x.time < date_range.rend
            ],
            tariff_included=self.tariff_included,
            vat_included=self.vat_included,
        )

    def add_data(self, data: ElectricityPrices) -> None:
        self.data = [x for x in self.data if all(x.time != d.time for d in data.data)]
        self.data = self.data + data.data
        self.data.sort()

    def to_frame(self) -> pd.DataFrame:
        """
        Converts the electricity prices to a pandas DataFrame.

        :return: A DataFrame of the electricity prices.
        :rtype: pd.DataFrame
        """
        return pd.DataFrame(
            [(x.time, x.value) for x in self.data],
            columns=["time", "value"],
        ).set_index("time")
