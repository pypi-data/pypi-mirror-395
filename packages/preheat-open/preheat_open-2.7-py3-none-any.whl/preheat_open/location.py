"""
location.py

This module defines classes related to setpoints and comfort profiles for managing
temperature settings and schedules.

Classes:
    Setpoint
    ComfortProfile
    LocationCharacteristics
    LocationInformation
    Location
"""

from dataclasses import dataclass
from itertools import chain
from typing import Generator, Optional

import pandas as pd

from .interfaces import Adapter
from .loadable_types import ComfortProfiles, LoadableData
from .measurements import get_measurements
from .query import Query, query_stuff, unique
from .supplypoint import SupplyPoint
from .time import DateRange, ZoneInfo, tzinfo
from .unit import Component, Device, Unit
from .zone import Zone


@dataclass
class LocationCharacteristics:
    """
    Represents the characteristics of a location.

    :ivar area: The area of the location.
    :vartype area: Optional[float]
    :ivar number_of_apartments: The number of apartments in the location.
    :vartype number_of_apartments: Optional[int]
    :ivar type: The type of the location.
    :vartype type: str
    """

    area: Optional[float] = None
    number_of_apartments: Optional[int] = None
    type: str = ""


@dataclass(frozen=True)
class LocationInformation:
    """
    Represents the information of a location.

    :ivar address: The address of the location.
    :vartype address: str
    :ivar city: The city where the location is situated.
    :vartype city: str
    :ivar country: The country where the location is situated.
    :vartype country: str
    :ivar label: A label for the location.
    :vartype label: str
    :ivar latitude: The latitude of the location.
    :vartype latitude: Optional[float]
    :ivar longitude: The longitude of the location.
    :vartype longitude: Optional[float]
    :ivar id: The unique identifier of the location.
    :vartype id: Optional[int]
    :ivar organisation_id: The ID of the organisation associated with the location.
    :vartype organisation_id: Optional[int]
    :ivar organisation_name: The name of the organisation associated with the location.
    :vartype organisation_name: str
    :ivar parent_organisation_id: The ID of the parent organisation.
    :vartype parent_organisation_id: Optional[int]
    :ivar parent_organisation_name: The name of the parent organisation.
    :vartype parent_organisation_name: str
    :ivar timezone: The timezone of the location.
    :vartype timezone: str
    :ivar zipcode: The zipcode of the location.
    :vartype zipcode: str
    :ivar setpoints: A list of setpoints associated with the location.
    :vartype setpoints: list
    """

    address: str = ""
    city: str = ""
    country: str = ""
    label: str = ""
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    id: Optional[int] = None
    organisation_id: Optional[int] = None
    organisation_name: str = ""
    parent_organisation_id: Optional[int] = None
    parent_organisation_name: str = ""
    timezone: str = ""
    zipcode: str = ""

    def __repr__(self) -> str:
        """
        Returns a string representation of the LocationInformation object.

        :return: A string describing the location information.
        :rtype: str
        """
        label = f"{self.label}, " if self.label else ""
        return (
            f"{self.__class__.__name__}({self.id}: {label}{self.address}, {self.city})"
        )

    def __hash__(self) -> int:
        """
        Returns a hash value for the LocationInformation object.

        :return: An integer hash value.
        :rtype: int
        """
        return hash(
            (
                self.address,
                self.city,
                self.country,
                self.label,
                self.latitude,
                self.longitude,
                self.id,
                self.organisation_id,
                self.organisation_name,
                self.parent_organisation_id,
                self.parent_organisation_name,
                self.timezone,
                self.zipcode,
            )
        )


class Location:
    """
    Represents a location in the PreHEAT sense.

    :ivar id: The unique identifier of the location.
    :vartype id: Optional[int]
    :ivar information: The information of the location.
    :vartype information: LocationInformation
    :ivar zones: A list of zones associated with the location.
    :vartype zones: list[Zone]
    :ivar units: A list of units associated with the location.
    :vartype units: list[Unit]
    :ivar characteristics: The characteristics of the location.
    :vartype characteristics: LocationCharacteristics
    :ivar supply_points: A list of supply points associated with the location.
    :vartype supply_points: list[SupplyPoint]
    :ivar _device_query_type: The query type for devices.
    :vartype _device_query_type: Query
    :ivar __devices: A list of devices associated with the location.
    :vartype __devices: list[Device]
    :ivar __devices_loaded: Indicates if the devices have been loaded.
    :vartype __devices_loaded: bool
    :ivar adapter: The adapter for the location.
    :vartype adapter: Adapter
    :ivar comfort_profiles: A list of comfort profiles associated with the location.
    :vartype comfort_profiles: list[ComfortProfile]
    """

    def __init__(
        self,
        id: int | None = None,
        information: LocationInformation | None = None,
        zones: list[Zone] | None = None,
        units: list[Unit] | None = None,
        characteristics: LocationCharacteristics | None = None,
        supply_points: list[SupplyPoint] | None = None,
        adapter: Adapter | None = None,
        comfort_profiles: LoadableData | None = None,
    ):
        self.id: int | None = id
        self.information: LocationInformation = (
            information if information is not None else LocationInformation()
        )
        self.zones: list[Zone] = zones if zones is not None else []
        self.units: list[Unit] = units if units is not None else []
        self.characteristics: LocationCharacteristics = (
            characteristics
            if characteristics is not None
            else LocationCharacteristics()
        )
        self.supply_points: list[SupplyPoint] = (
            supply_points if supply_points is not None else []
        )
        self.__devices: list[Device] = []
        self.__devices_loaded = False
        self.__adapter = None
        self.comfort_profiles: LoadableData | None = comfort_profiles

        if adapter is not None:
            self.adapter = adapter

        self.__post_init__()

    def __post_init__(self) -> None:
        """
        Post-initialization processing to set up units and zones.
        """

        def assign_location(item, location):
            item.location = self
            for iitem in getattr(item, "sub_units", getattr(item, "sub_zones", [])):
                assign_location(iitem, location)

        for item in chain(self.devices, self.units, self.zones):
            assign_location(item, self)
        for unit in self.get_units(shared=[]):
            unit.location = self
            for child in unit.children:
                child.parent = unit
            for component in unit.components:
                component.parent = unit
            unit.zones = [
                zone
                for zid in unit.zones
                if isinstance(zid, int) and (zone := unique(self.get_zones(id=zid)))
            ]
            for zone in unit.zones:
                zone.units.append(unit)
            unit.related_units = [
                unique(self.get_units(id=unit_id)) for unit_id in unit.related_units
            ]
            if unit.control_settings is not None:
                unit.control_settings.parent = unit
        try:
            self.adapter.location_post_setup(self)
        except AttributeError:
            pass

    @property
    def adapter(self) -> Adapter:
        """
        Returns the adapter associated with the location.

        :return: The adapter for the location.
        :rtype: Adapter
        """
        if self.__adapter is None:
            raise AttributeError(f"Adapter is not set for location {self}. ")
        return self.__adapter

    @adapter.setter
    def adapter(self, value: Adapter) -> None:
        """
        Sets the adapter for the location.

        :param value: The adapter to set.
        :type value: Adapter
        """
        if not isinstance(value, Adapter):
            raise TypeError("Adapter must be an instance of Adapter.")
        self.__adapter = value

    def to_building_model_dict(self) -> dict:
        """
        Converts the location to a building model dictionary.

        :return: A dictionary containing the location information.
        :rtype: dict
        """
        return {
            "id": self.id,
            "information": self.information.__dict__,
            "zones": [zone.to_building_model_dict() for zone in self.zones],
            "units": [unit.to_building_model_dict() for unit in self.units],
            "characteristics": self.characteristics.__dict__,
        }

    @classmethod
    def from_building_model_dict(cls, data: dict, adapter: Adapter) -> "Location":
        """
        Creates a Location object from a building model dictionary.
        """
        return cls(
            id=data["id"],
            information=LocationInformation(**data["information"]),
            zones=[Zone.from_building_model_dict(z) for z in data["zones"]],
            units=[
                Unit.from_building_model_dict(u, adapter=adapter) for u in data["units"]
            ],
            characteristics=LocationCharacteristics(**data["characteristics"]),
            adapter=adapter,
        )

    def __repr__(self) -> str:
        """
        Returns a string representation of the Location object.

        :return: A string describing the location.
        :rtype: str
        """
        return f"{self.__class__.__name__}({self.information})"

    def __hash__(self) -> int:
        """
        Returns a hash value for the Location object.

        :return: An integer hash value.
        :rtype: int
        """
        return hash(
            self.information,
        )

    def __eq__(self, other: object) -> bool:
        """
        Compares the location to another object.

        :param other: The object to compare to.
        :type other: object
        :return: True if the objects are equal, False otherwise.
        :rtype: bool
        """
        if not isinstance(other, Location):
            return False
        return self.information == other.information

    @property
    def timezone(self) -> tzinfo:
        """
        Returns the timezone of the location.

        :return: The timezone of the location.
        :rtype: tzinfo
        """
        return ZoneInfo(self.information.timezone)

    @property
    def devices(self) -> list[Device]:
        """
        Returns the list of devices associated with the location.

        :return: A list of devices.
        :rtype: list[Device]
        """
        if not self.__devices_loaded:
            if not self.id:
                raise AttributeError("Location ID is not set, cannot load devices.")
            try:
                self.__devices = self.adapter.get_devices(self.id)
            except AttributeError:
                return []
            for device in self.__devices:
                device.location = self
            self.__devices_loaded = True
        return self.__devices

    def get_measurements(
        self,
        **kwargs,
    ) -> pd.DataFrame:
        """
        Retrieves measurements for the location.

        :param components: The components to get measurements for.
        :type components: list[Component] | Query | dict
        :param date_range: The date range for the measurements.
        :type date_range: DateRange, optional
        :param mapper: The mapper to apply to the measurements.
        :type mapper: MapApplier, optional
        :param kwargs: Additional arguments.
        :return: A DataFrame containing the measurements.
        :rtype: pd.DataFrame
        """
        return get_measurements(
            obj=self,
            **kwargs,
        )

    def get_units(
        self,
        query: Query | None = None,
        **kwargs,
    ) -> Generator[Unit, None, None]:
        """
        Retrieves units associated with the location.

        :param query: The query to filter units.
        :type query: Query, optional
        :param kwargs: Additional arguments.
        :return: A generator yielding units.
        :rtype: Generator[Unit, None, None]
        """
        for unit in self.units:
            yield from unit.get_sub_units(
                query=query,
                include_self=True,
                include_related_units=False,
                **kwargs,
            )

    def get_devices(
        self,
        query: Query | list[Query | dict] | None = None,
        **kwargs,
    ) -> Generator[Device, None, None]:
        """
        Retrieves devices associated with the location.

        :param query: The query to filter devices.
        :type query: Query | list[Query | dict], optional
        :param kwargs: Additional arguments.
        :return: A generator yielding devices.
        :rtype: Generator[Device, None, None]
        """
        yield from (
            device
            for device in query_stuff(
                obj=self,
                sub_obj_attrs=["devices"],
                query=query,
                query_type=self.adapter.building_model.device_query_type,
                **kwargs,
            )
            if isinstance(device, Device)
        )

    def get_zones(
        self,
        query: Query | list[Query] | None = None,
        **kwargs,
    ) -> Generator[Zone, None, None]:
        """
        Retrieves zones associated with the location.

        :param query: The query to filter zones.
        :type query: Query, optional
        :param kwargs: Additional arguments.
        :return: A generator yielding zones.
        :rtype: Generator[Zone, None, None]
        """
        for zone in self.zones:
            yield from zone.get_sub_zones(
                query=query,
                include_self=True,
                **kwargs,
            )

    def get_components(
        self,
        query: Query | list[Query | dict] | None = None,
        **kwargs,
    ) -> Generator[Component, None, None]:
        """
        Retrieves components associated with the location.

        :param query: The query to filter components.
        :type query: Query | list[Query | dict], optional
        :param kwargs: Additional arguments.
        :return: A generator yielding components.
        :rtype: Generator[Component, None, None]
        """
        for unit in self.units:
            yield from query_stuff(
                obj=unit,
                sub_obj_attrs=["components", "children"],
                query=query,
                query_type=self.adapter.building_model.component_query_type,
                include_obj=False,
                **kwargs,
            )

    def get_comfort_profiles(self, date_range: DateRange) -> ComfortProfiles:
        """
        Retrieves comfort profiles for the location within the specified time range.

        :param date_range: The date range for the comfort profiles.
        :type date_range: DateRange
        :return: A list of comfort profiles.
        :rtype: list[ComfortProfile]
        """
        if not date_range.tz_aware:
            date_range = date_range.astimezone(self.timezone)
        if self.comfort_profiles is None:
            raise ValueError(
                f"Comfort profiles are not configured properly for location {self}."
            )
        return self.comfort_profiles.get(date_range=date_range)

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__.update(d)
