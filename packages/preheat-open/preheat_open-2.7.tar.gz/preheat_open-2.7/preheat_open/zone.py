"""
zone.py

This module defines classes related to building zones, including ventilation information and zone management.

Classes:
    VentilationInfo
    Zone
"""

from __future__ import annotations

from datetime import tzinfo
from typing import TYPE_CHECKING, Any, Generator, Sequence

import pandas as pd

from .interfaces import Factory
from .loadable_types import ComfortProfile
from .measurements import get_measurements
from .query import Query, query_stuff
from .time import DateRange
from .unit import Unit

if TYPE_CHECKING:
    from .location import Location


class VentilationInfo:
    """
    Represents ventilation information for a zone.

    :ivar has_ventilation_supply: Indicates if the zone has ventilation supply.
    :vartype has_ventilation_supply: bool
    :ivar has_ventilation_exhaust: Indicates if the zone has ventilation exhaust.
    :vartype has_ventilation_exhaust: bool
    """

    def __init__(
        self,
        has_ventilation_supply: bool | None = None,
        has_ventilation_exhaust: bool | None = None,
    ):
        """
        Initialize VentilationInfo.

        :param has_ventilation_supply: Indicates if the zone has ventilation supply
        :type has_ventilation_supply: bool
        :param has_ventilation_exhaust: Indicates if the zone has ventilation exhaust
        :type has_ventilation_exhaust: bool
        """
        self.has_ventilation_supply: bool | None = has_ventilation_supply
        self.has_ventilation_exhaust: bool | None = has_ventilation_exhaust

    def __repr__(self) -> str:
        """
        Returns a string representation of the VentilationInfo object.

        :return: A string in the format "VentilationInfo(Supply: {has_ventilation_supply}, Exhaust: {has_ventilation_exhaust})".
        :rtype: str
        """
        return f"VentilationInfo(Supply: {self.has_ventilation_supply}, Exhaust: {self.has_ventilation_exhaust})"


class Zone:
    """
    Defines a building zone in the PreHEAT sense.

    :ivar id: The unique identifier of the zone.
    :vartype id: int | None
    :ivar name: The name of the zone.
    :vartype name: str
    :ivar type: The type of the zone.
    :vartype type: str
    :ivar external_identifier: The external identifier of the zone.
    :vartype external_identifier: str
    :ivar area: The area of the zone.
    :vartype area: float
    :ivar has_external_wall: Indicates if the zone has an external wall.
    :vartype has_external_wall: bool
    :ivar parent: The parent zone.
    :vartype parent: Zone
    :ivar sub_zones: A list of sub-zones or factories to create sub-zones.
    :vartype sub_zones: list[Zone | Factory]
    :ivar units: A list of units associated with the zone.
    :vartype units: list[Unit]
    :ivar adjacent_zones: A list of IDs of adjacent zones.
    :vartype adjacent_zones: list[int]
    :ivar comfort_profile_id: The ID of the comfort profile associated with the zone.
    :vartype comfort_profile_id: int | None
    :ivar ventilation_information: The ventilation information of the zone.
    :vartype ventilation_information: VentilationInfo
    :ivar _zone_query_type: The query type for zones.
    :vartype _zone_query_type: type
    """

    def __init__(
        self,
        id: int | None = None,
        name: str = "",
        type: str = "",
        external_identifier: str = "",
        area: float | None = None,
        has_external_wall: bool | None = None,
        parent: Zone | None = None,
        sub_zones: list[Zone | Factory] | None = None,
        units: list[Unit] | None = None,
        adjacent_zones: list[int] | None = None,
        comfort_profile_id: int | None = None,
        ventilation_information: VentilationInfo | None = None,
        location: Location | None = None,
    ):
        """
        Initialize Zone.

        :param id: The unique identifier of the zone
        :type id: int | None
        :param name: The name of the zone
        :type name: str
        :param type: The type of the zone
        :type type: str
        :param external_identifier: The external identifier of the zone
        :type external_identifier: str
        :param area: The area of the zone
        :type area: float
        :param has_external_wall: Indicates if the zone has an external wall
        :type has_external_wall: bool
        :param parent: The parent zone
        :type parent: Zone
        :param sub_zones: A list of sub-zones or factories to create sub-zones
        :type sub_zones: list[Zone | Factory]
        :param units: A list of units associated with the zone
        :type units: list[Unit]
        :param adjacent_zones: A list of IDs of adjacent zones
        :type adjacent_zones: list[int]
        :param comfort_profile_id: The ID of the comfort profile associated with the zone
        :type comfort_profile_id: int | None
        :param ventilation_information: The ventilation information of the zone
        :type ventilation_information: VentilationInfo
        :param location: The location containing this zone
        :type location: Location
        """
        self.id: int | None = id
        self.name: str = name
        self.type: str = type
        self.external_identifier: str = external_identifier
        self.area: float | None = area
        self.has_external_wall: bool | None = has_external_wall
        self.parent: Zone | None = parent
        self.sub_zones: list[Zone] = (
            [f.build() if isinstance(f, Factory) else f for f in sub_zones]
            if sub_zones is not None
            else []
        )
        self.units: list[Unit] = units or []
        self.adjacent_zones: list[int] = adjacent_zones or []
        self.comfort_profile_id: int | None = comfort_profile_id
        self.ventilation_information: VentilationInfo | None = (
            ventilation_information or VentilationInfo()
        )
        self.location: Location | None = location

        for sub_zone in self.sub_zones:
            sub_zone.parent = self

    def to_building_model_dict(self) -> dict:
        """
        Converts the Zone object to a dictionary for the building model.

        :return: A dictionary representation of the Zone object.
        :rtype: dict
        """
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "externalIdentifier": self.external_identifier,
            "area": self.area,
            "hasExternalWall": self.has_external_wall,
            "subZones": [z.to_building_model_dict() for z in self.sub_zones],
            "adjacentZones": self.adjacent_zones,
            "comfortProfileId": self.comfort_profile_id,
            "ventilation_information": self.ventilation_information.__dict__,
        }

    @classmethod
    def from_building_model_dict(cls, data: dict) -> Zone:
        """
        Creates a Zone object from a building model dictionary.

        :param data: The building model dictionary.
        :type data: dict
        :return: A Zone object created from the building model dictionary.
        :rtype: Zone
        """
        return cls(
            id=data["id"],
            name=data["name"],
            type=data["type"],
            external_identifier=data["externalIdentifier"],
            area=data["area"],
            sub_zones=[Zone.from_building_model_dict(d) for d in data["subZones"]],
            has_external_wall=data["hasExternalWall"],
            adjacent_zones=data["adjacentZones"],
            comfort_profile_id=data["comfortProfileId"],
            ventilation_information=VentilationInfo(**data["ventilation_information"]),
        )

    @property
    def timezone(self) -> tzinfo:
        """
        Returns the timezone of the zone.

        :return: The timezone of the zone.
        :rtype: tzinfo
        """
        return self.location.timezone

    def __repr__(self) -> str:
        """
        Returns a string representation of the Zone object.

        :return: A string in the format "Zone(type={type}, name={name}, id={id})".
        :rtype: str
        """
        return f"{self.__class__.__name__}(type={self.type}, name={self.name}, id={self.id})"

    def get_sub_zones(
        self,
        query: Query | Sequence[Query] | None = None,
        include_self: bool = False,
        **kwargs,
    ) -> Generator[Any, None, None]:
        """
        Retrieves sub-zones associated with the zone based on the specified query.

        :param query: The query or list of queries to filter sub-zones.
        :type query: Query | Sequence[Query] | None
        :param include_self: Whether to include the zone itself in the results if it matches the query.
        :type include_self: bool
        :param kwargs: Additional keyword arguments for the query.
        :return: A generator yielding sub-zones that match the query.
        :rtype: Generator[Zone, None, None]
        """
        if self.location is None:
            raise ValueError("Zone must have a location to get sub-zones")
        if self.location.adapter is None:
            raise ValueError(
                "Location must have an adapter to get sub-zones from zones"
            )
        yield from query_stuff(
            obj=self,
            sub_obj_attrs=["sub_zones"],
            query=query,
            query_type=self.location.adapter.building_model.zone_query_type,
            include_obj=include_self,
            **kwargs,
        )

    def get_parents(
        self,
        query: Query | list[Query | dict[str, Any]] | None = None,
        include_self: bool = False,
        **kwargs,
    ) -> Generator[Any, None, None]:
        """
        Retrieves parent zones associated with the zone based on the specified query.

        :param query: The query or list of queries to filter parent zones.
        :type query: Query | Sequence[Query] | None
        :param include_self: Whether to include the zone itself in the results if it matches the query.
        :type include_self: bool
        :param kwargs: Additional keyword arguments for the query.
        :return: A generator yielding parent zones that match the query.
        :rtype: Generator[Zone, None, None]
        """
        if self.location is None:
            raise ValueError("Zone must have a location to get parent zones")

        yield from query_stuff(
            obj=self,
            sub_obj_attrs=["parent"],
            query=query,
            query_type=self.location.adapter.building_model.zone_query_type,
            include_obj=include_self,
            **kwargs,
        )

    def get_units(
        self,
        query: Query | Sequence[Query] | None = None,
        **kwargs,
    ) -> Generator[Any, None, None]:
        """
        Retrieves sub-units associated with the unit based on the specified query.

        :param query: The query or list of queries to filter sub-units.
        :type query: Query | Sequence[Query] | None
        :param include_self: Whether to include the unit itself in the results if it matches the query.
        :type include_self: bool
        :param kwargs: Additional keyword arguments for the query.
        :return: A generator yielding sub-units that match the query.
        :rtype: Generator[Unit, None, None]
        """
        if self.location is None:
            raise ValueError("Zone must have a location to get units")
        if self.location.adapter is None:
            raise ValueError("Location must have an adapter to get units from zones")
        yield from query_stuff(
            obj=self,
            sub_obj_attrs=["units", "children", "related_units"],
            sub_obj_attrs_for_removal=["related_units"],
            query=query,
            query_type=self.location.adapter.building_model.unit_query_type,
            include_obj=False,
            **kwargs,
        )

    def get_measurements(
        self,
        **kwargs,
    ) -> pd.DataFrame:
        """
        Retrieves measurements for the device.

        :param start: The start datetime for the measurements.
        :type start: datetime
        :param end: The end datetime for the measurements.
        :type end: datetime
        :param components: The components to get measurements for.
        :type components: list[Component] | Query | dict
        :param resolution: The time resolution for the measurements.
        :type resolution: TimeResolution
        :param mapper: The mapper to apply to the measurements.
        :type mapper: MapApplier
        :return: A DataFrame containing the measurements.
        :rtype: pd.DataFrame
        """

        return get_measurements(
            obj=self,
            **kwargs,
        )

    def get_components(
        self,
        query: Query | Sequence[Query] | None = None,
        **kwargs,
    ) -> Generator[Any, None, None]:
        """
        Retrieves components associated with the device based on the specified query.

        :param query: The query or list of queries to filter components.
        :type query: Query | Sequence[Query] | None
        :param include_self: Whether to include the device itself in the results if it matches the query.
        :type include_self: bool
        :param kwargs: Additional keyword arguments for the query.
        :return: A generator yielding components that match the query.
        :rtype: Generator[Component, None, None]
        """
        if self.location is None:
            raise ValueError("Zone must have a location to get components")
        yield from query_stuff(
            obj=self,
            sub_obj_attrs=[
                "components",
                "children",
                "related_units",
                "units",
                "sub_zones",
            ],
            sub_obj_attrs_for_removal=["related_units"],
            query=query,
            query_type=self.location.adapter.building_model.component_query_type,
            include_obj=False,
            **kwargs,
        )

    def get_comfort_profile(self, date_range: DateRange) -> ComfortProfile:
        """
        Retrieves the comfort profile for the zone within the specified time range.

        :param start: The start of the time range.
        :type start: datetime
        :param end: The end of the time range.
        :type end: datetime
        :return: The comfort profile for the zone within the specified time range.
        :rtype: ComfortProfile
        """
        if self.comfort_profile_id is None:
            raise ValueError("No comfort profile ID for zone")
        if self.location is None:
            raise ValueError("Zone must have a location to get comfort profiles")
        return self.location.get_comfort_profiles(date_range=date_range).get_profile(
            self.comfort_profile_id
        )
