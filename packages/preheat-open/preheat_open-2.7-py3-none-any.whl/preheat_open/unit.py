"""
unit.py

This module defines units and their auxiliary functions, including components, devices, and control settings.

Classes:
    UnitDescriptors
    NotFoundError
    ControlSetting
    ControlSettings
    ComponentData
    Component
    Device
    Unit

Functions:
    _standard_measurement_dict
"""

from __future__ import annotations

import logging
from enum import Enum
from typing import TYPE_CHECKING, Any, Generator

import pandas as pd
from requests.models import Response

from preheat_open.loadable_types import ComponentData

from .interfaces import Adapter, Factory
from .loadable_types import ElectricityPrices, LoadableData, SetpointSchedule
from .measurements import get_measurements
from .query import Query, query_stuff
from .time import DateRange, TimeResolution, tzinfo

if TYPE_CHECKING:
    from .location import Location
    from .zone import Zone

logger = logging.getLogger(__name__)


class UnitDescriptors:
    """
    Represents descriptors for a unit.

    :param parameter_dict: A dictionary of parameters to initialize the descriptors.
    :type parameter_dict: dict
    """

    def __init__(self, **parameter_dict):
        self.__dict__.update(parameter_dict)

    def to_dict(self) -> dict:
        """
        Converts the UnitDescriptors object to a dictionary.

        :return: A dictionary representation of the unit descriptors.
        :rtype: dict
        """
        return self.__dict__


class NotFoundError(Exception):
    """
    Exception raised when a requested item is not found.
    """

    pass


def _standard_measurement_dict() -> dict[TimeResolution, LoadableData]:
    """
    Creates a standard measurement dictionary with default component data for each time resolution.

    :return: A dictionary mapping time resolutions to component data.
    :rtype: dict[TimeResolution, ComponentData]
    """
    return {res: LoadableData(data=ComponentData()) for res in TimeResolution}


class Component:
    """
    Defines a component in the PreHEAT sense.

    :ivar cid: The component ID.
    :vartype cid: int
    :ivar id: The ID of the component.
    :vartype id: int
    :ivar name: The name of the component.
    :vartype name: str
    :ivar type: The type of the component.
    :vartype type: Enum
    :ivar min: The minimum value of the component.
    :vartype min: float
    :ivar max: The maximum value of the component.
    :vartype max: float
    :ivar unit: The unit of the component.
    :vartype unit: str
    :ivar measurements: The measurements of the component.
    :vartype measurements: dict[TimeResolution, ComponentData]
    :ivar std_unit: The standard unit of the component.
    :vartype std_unit: str
    :ivar std_unit_divisor: The standard unit divisor of the component.
    :vartype std_unit_divisor: float
    :ivar parent: The parent unit or device of the component.
    :vartype parent: Unit | Device
    """

    def __init__(
        self,
        cid: int | None = None,
        id: int | None = None,
        name: str = "",
        type: Enum | None = None,
        min: float | None = None,
        max: float | None = None,
        unit: str = "",
        measurements: dict[TimeResolution, LoadableData] | None = None,
        std_unit: str = "",
        std_unit_divisor: float = 1.0,
        parent: Unit | Device | None = None,
    ):
        self.cid = cid
        self.id = id
        self.name = name
        self.type = type
        self.min = min
        self.max = max
        self.unit = unit
        self.measurements = (
            measurements if measurements is not None else _standard_measurement_dict()
        )
        self.std_unit = std_unit
        self.std_unit_divisor = std_unit_divisor
        self.parent = parent

    def to_building_model_dict(self) -> dict:
        """
        Converts the Component object to a dictionary.

        :return: A dictionary representation of the component.
        :rtype: dict
        """
        return {
            "cid": self.cid,
            "id": self.id,
            "name": self.name,
            "type": self.type.value if self.type else None,
        }

    @classmethod
    def from_building_model_dict(cls, data: dict, adapter: Adapter) -> "Component":
        """
        Creates a Component object from a building model dictionary.
        """
        return cls(
            cid=data["cid"],
            id=data["id"],
            name=data["name"],
            type=adapter.building_model.component_type(data["type"]),
        )

    def check_measurement(self, date_range: DateRange) -> DateRange:
        """
        Checks if measurements are available for the specified date range.

        :param date_range: The date range to check.
        :type date_range: DateRange
        :return: The missing date range.
        :rtype: DateRange
        """
        return self.measurements[date_range.resolution].request(date_range)

    def get_measurement(
        self,
        date_range: DateRange,
    ) -> ComponentData:
        """
        Retrieves measurements for the specified date range.

        :param date_range: The date range for which to retrieve measurements.
        :type date_range: DateRange
        :return: The component data for the specified date range.
        :rtype: ComponentData
        """
        missing_dr = self.check_measurement(date_range)
        if not missing_dr.empty:
            logger.warning(
                "Missing data for %s, date_range=%s, missing_date_range=%r",
                self,
                date_range,
                missing_dr,
            )
        cdata: ComponentData = self.measurements[date_range.resolution].get(
            date_range=date_range
        )
        cdata.measurements.rename(
            self.id if isinstance(self.parent, Unit) else self.cid, inplace=True
        )
        return cdata

    def __repr__(self) -> str:
        """
        Returns a string representation of the Component object.

        :return: A string describing the component.
        :rtype: str
        """
        id_str = f"id={self.id}" if isinstance(self.parent, Unit) else f"cid={self.cid}"
        return f"{self.__class__.__name__}({id_str}, type={self.type.__repr__()}, name={self.name})"

    def __hash__(self):
        """
        Returns a hash value for the Component object.

        :return: The hash value.
        :rtype: int
        """
        parent_type = type(self.parent)
        return hash(
            (
                parent_type,
                self.id if isinstance(parent_type, Unit) else self.cid,
                self.type,
            )
        )

    def __eq__(self, other: object) -> bool:
        """
        Compares the Component object with another object for equality.

        :param other: The object to compare.
        :type other: Any
        :return: True if the objects are equal, False otherwise.
        :rtype: bool
        """
        return (
            isinstance(other, Component)
            and self.id == other.id
            and self.cid == other.cid
            and self.type == other.type
            and self.name == other.name
            and self.parent == other.parent
        )


class Device:
    """
    A device is a grouping of signals originating from a single physical data source (device),
    which is not linked to the building model.

    :ivar type: The type of the device.
    :vartype type: str
    :ivar id: The ID of the device.
    :vartype id: int | None
    :ivar name: The name of the device.
    :vartype name: str
    :ivar components: A list of components associated with the device.
    :vartype components: list[Component]
    :ivar adapter: The adapter for the device.
    :vartype adapter: Adapter
    :ivar location: The location of the device.
    :vartype location: Location
    :ivar _component_query_type: The query type for components.
    :vartype _component_query_type: type
    """

    def __init__(
        self,
        type: str = "",
        id: int | None = None,
        serial: str = "",
        name: str = "",
        components: list[Component] | None = None,
        location: Location | None = None,
    ):
        self.type: str = type
        self.id: int | None = id
        self.serial: str = serial
        self.name: str = name
        self.components: list[Component] = components if components is not None else []
        self.location: Location | None = location

        # Post-initialization
        for comp in self.components:
            comp.parent = self

    def __repr__(self) -> str:
        """
        Returns a string representation of the Device object.

        :return: A string describing the device.
        :rtype: str
        """
        return f"{self.__class__.__name__}(type={self.type.__repr__()}, name={self.name}, id={self.id})"

    @property
    def timezone(self) -> tzinfo:
        """
        Returns the timezone of the device.

        :return: The timezone of the device.
        :rtype: tzinfo
        """
        if self.location is None:
            raise ValueError(
                "Cannot infer timezone from Location since Device has no location set."
            )
        return self.location.timezone

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
        query: Query | list[Query | dict[str, Any]] | None = None,
        include_self: bool = False,
        **kwargs,
    ) -> Generator[Any, None, None]:
        """
        Retrieves components associated with the device based on the specified query.

        :param query: The query or list of queries to filter components.
        :type query: Query | list[Query | dict] | None
        :param include_self: Whether to include the device itself in the results if it matches the query.
        :type include_self: bool
        :param kwargs: Additional keyword arguments for the query.
        :return: A generator yielding components that match the query.
        :rtype: Generator[Component, None, None]
        """
        yield from query_stuff(
            obj=self,
            sub_obj_attrs=["components", "children", "related_units"],
            sub_obj_attrs_for_removal=["related_units"],
            query=query,
            query_type=self.location.adapter.building_model.component_query_type,
            include_obj=include_self,
            **kwargs,
        )


class ControlSetting:
    """
    Represents a control setting for a unit.

    :ivar type: The type of the control setting.
    :vartype type: Enum
    :ivar value: The value of the control setting.
    :vartype value: Any
    :ivar unit: The unit of the control setting.
    :vartype unit: str
    """

    def __init__(self, type: Enum | None = None, value: Any = None, unit: str = ""):
        self.type = type
        self.value = value
        self.unit = unit

    def to_building_model_dict(self) -> dict:
        """
        Converts the ControlSetting object to a dictionary.

        :return: A dictionary representation of the control setting.
        :rtype: dict
        """
        return {
            "type": self.type.key,
            "value": self.value,
            "unit": self.unit,
        }

    def __repr__(self) -> str:
        """
        Returns a string representation of the ControlSetting object.

        :return: A string in the format "type=value".
        :rtype: str
        """
        return f"{self.__class__.__name__}({self.type.name if self.type else None}:{self.value})"


class ControlSettings:
    """
    Represents a collection of control settings.

    :ivar settings: A dictionary of control settings.
    :vartype settings: dict[str, ControlSetting]
    :ivar parent: The parent unit.
    :vartype parent: Unit
    """

    def __init__(self, settings: dict[str, ControlSetting], parent: "Unit" = None):
        self.settings = settings
        self.parent = parent

    def to_building_model_dict(self) -> dict:
        """
        Converts the ControlSettings object to a dictionary.

        :return: A dictionary representation of the control settings.
        :rtype: dict
        """
        return {
            "settings": [
                setting.to_building_model_dict() for setting in self.settings.values()
            ],
        }

    @classmethod
    def from_building_model_dict(
        cls, data: dict, adapter: "Adapter"
    ) -> "ControlSettings":
        """
        Creates a ControlSettings object from a building model dictionary.
        """
        for s in data["settings"]:
            s["type"] = (
                adapter.building_model.control_setting_type(s["type"])
                if s["type"]
                in adapter.building_model.control_setting_type._value2member_map_
                else s["type"]
            )
        return cls(
            settings={
                s["type"].value
                if isinstance(s["type"], Enum)
                else s["type"]: ControlSetting(**s)
                for s in data["settings"]
            },
        )

    def __repr__(self) -> str:
        """
        Returns a string representation of the ControlSettings object.

        :return: A string describing the control settings.
        :rtype: str
        """
        return f"{self.__class__.__name__}({', '.join([setting.__repr__() for setting in self.settings.values()])})"

    def get(self, itype: Enum | str, default: Any = None) -> ControlSetting:
        """
        Gets a control setting by type.
        """
        try:
            return self[itype]
        except KeyError:
            return default

    def __getitem__(self, itype: str) -> ControlSetting:
        """
        Gets a control setting by type.
        """
        if itype not in self.settings:
            raise KeyError(f"Control setting of key {itype} not found.")
        return self.settings[itype].value

    def __setitem__(self, itype: str, value: Any) -> None:
        """
        Sets a control setting by type.
        """
        if itype in self.settings:
            self.settings[itype].value = value
        else:
            self.settings[itype] = ControlSetting(
                type=self.parent.location.adapter.building_model.control_setting_type.from_key(
                    itype
                ),
                value=value,
            )

    def __delitem__(self, itype: str) -> None:
        """
        Deletes a control setting by type.
        """
        if itype in self.settings:
            del self.settings[itype]

    def __contains__(self, itype: str) -> bool:
        """
        Checks if a control setting exists by type.
        """
        return itype in self.settings


class Unit(Device):
    """
    Defines a unit in the PreHEAT sense.

    :ivar type: The type of the unit.
    :vartype type: Enum | None
    :ivar subtype: The subtype of the unit.
    :vartype subtype: Enum | None
    :ivar descriptors: The descriptors of the unit.
    :vartype descriptors: UnitDescriptors
    :ivar zones: A list of zones associated with the unit.
    :vartype zones: list[Zone]
    :ivar shared: Indicates if the unit is shared.
    :vartype shared: bool
    :ivar shared_from: The ID of the unit from which this unit is shared.
    :vartype shared_from: int | None
    :ivar shared_locations: A list of IDs of locations where the unit is shared.
    :vartype shared_locations: list[int]
    :ivar parent: The parent unit.
    :vartype parent: Unit | None
    :ivar children: A list of child units.
    :vartype children: list[Unit]
    :ivar related_units: A list of related units.
    :vartype related_units: list[Unit]
    :ivar covers_building: Indicates if the unit covers a building.
    :vartype covers_building: bool
    :ivar buildings_covered: The number of buildings covered by the unit.
    :vartype buildings_covered: int
    :ivar control_settings: The control settings of the unit.
    :vartype control_settings: ControlSettings | None
    """

    def __init__(
        self,
        type: Enum | None = None,
        subtype: Enum | None = None,
        descriptors: UnitDescriptors | None = None,
        zones: list[Zone] | None = None,
        shared: bool = False,
        shared_from: int | None = None,
        shared_locations: list[int] | None = None,
        parent: Unit | None = None,
        children: list[Unit] | None = None,
        related_units: list[Unit] | None = None,
        covers_building: bool | None = None,
        buildings_covered: int | None = None,
        control_settings: ControlSettings | None = None,
        setpoint_schedule: LoadableData | None = None,
        electricity_prices: dict[str, dict[str, LoadableData]] | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.type: Enum | None = type
        self.subtype: Enum | None = subtype
        self.descriptors: UnitDescriptors | None = descriptors or UnitDescriptors()
        self.zones: list[Zone] = zones or []
        self.shared: bool | None = shared
        self.shared_from: int | None = shared_from
        self.shared_locations: list[int] | None = shared_locations or []
        self.parent: Unit | None = parent
        self.children: list[Unit] = children or []
        self.related_units: list[Unit] = related_units or []
        self.covers_building: bool | None = covers_building
        self.buildings_covered: int | None = buildings_covered
        self.control_settings: ControlSettings | None = control_settings
        self.setpoint_schedule: LoadableData | None = setpoint_schedule
        self.electricity_prices: dict[
            str, dict[str, LoadableData]
        ] | None = electricity_prices

        # Post-initialization
        self.children = [
            f.build() if isinstance(f, Factory) else f for f in self.children
        ]

    def to_building_model_dict(self) -> dict:
        """
        Converts the Unit object to a dictionary.

        :return: A dictionary representation of the unit.
        :rtype: dict
        """
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type.value if self.type else None,
            "subtype": None if self.subtype is None else self.subtype.value,
            "descriptors": self.descriptors.__dict__,
            "zones": [z.id for z in self.zones],
            "children": [c.to_building_model_dict() for c in self.children],
            "components": [c.to_building_model_dict() for c in self.components],
            "control_settings": None
            if self.control_settings is None
            else self.control_settings.to_building_model_dict(),
            "covers_building": self.covers_building,
            "buildings_covered": self.buildings_covered,
            "related_units": [ru.id for ru in self.related_units],
        }

    @classmethod
    def from_building_model_dict(cls, data: dict, adapter: Adapter) -> Unit:
        """
        Creates a Unit object from a building model dictionary.
        """
        return cls(
            id=data["id"],
            name=data["name"],
            type=adapter.building_model.unit_type(data["type"]),
            subtype=adapter.building_model.unit_subtype(st)
            if (st := data["subtype"]) is not None
            else None,
            descriptors=UnitDescriptors(**data["descriptors"]),
            zones=data["zones"],
            children=[
                Unit.from_building_model_dict(data=c, adapter=adapter)
                for c in data["children"]
            ],
            components=[
                Component.from_building_model_dict(data=c, adapter=adapter)
                for c in data["components"]
            ],
            control_settings=None
            if data["control_settings"] is None
            else ControlSettings.from_building_model_dict(
                data=data["control_settings"], adapter=adapter
            ),
            covers_building=data["covers_building"],
            buildings_covered=data["buildings_covered"],
            related_units=data["related_units"],
        )

    def __repr__(self) -> str:
        """
        Returns a string representation of the Unit object.

        :return: A string describing the unit.
        :rtype: str
        """
        return f"{self.__class__.__name__}(type={self.type.__repr__()}, name={self.name}, id={self.id})"

    def get_parents(
        self,
        query: Query | list[Query | dict[str, Any]] | None = None,
        include_self: bool = False,
        **kwargs,
    ) -> Generator[Any, None, None]:
        """
        Retrieves parent units associated with the unit based on the specified query.

        :param query: The query or list of queries to filter parent units.
        :type query: Query | list[Query | dict] | None
        :param include_self: Whether to include the unit itself in the results if it matches the query.
        :type include_self: bool
        :param kwargs: Additional keyword arguments for the query.
        :return: A generator yielding parent units that match the query.
        :rtype: Generator[Unit, None, None]
        """
        if self.location is None:
            raise ValueError("Cannot get parents since Unit has no location set.")

        yield from query_stuff(
            obj=self,
            sub_obj_attrs=["parent"],
            query=query,
            query_type=self.location.adapter.building_model.unit_query_type,
            include_obj=include_self,
            **kwargs,
        )

    def get_sub_units(
        self,
        query: Query | list[Query | dict[str, Any]] | None = None,
        include_self: bool = False,
        include_related_units: bool = True,
        **kwargs,
    ) -> Generator[Any, None, None]:
        """
        Retrieves sub-units associated with the unit based on the specified query.

        :param query: The query or list of queries to filter sub-units.
        :type query: Query | list[Query | dict] | None
        :param include_self: Whether to include the unit itself in the results if it matches the query.
        :type include_self: bool
        :param kwargs: Additional keyword arguments for the query.
        :return: A generator yielding sub-units that match the query.
        :rtype: Generator[Unit, None, None]
        """
        if self.location is None:
            raise ValueError("Cannot get sub-units since Unit has no location set.")

        yield from query_stuff(
            obj=self,
            sub_obj_attrs=["children", "related_units"]
            if include_related_units
            else ["children"],
            sub_obj_attrs_for_removal=["related_units"],
            query=query,
            query_type=self.location.adapter.building_model.unit_query_type,
            include_obj=include_self,
            **kwargs,
        )

    def get_zones(
        self,
        query: Query | list[Query | dict[str, Any]] | None = None,
        **kwargs,
    ) -> Generator[Any, None, None]:
        """
        Retrieves zones associated with the unit based on the specified query.

        :param query: The query or list of queries to filter zones.
        :type query: Query | list[Query | dict] | None
        :param kwargs: Additional keyword arguments for the query.
        :return: A generator yielding zones that match the query.
        :rtype: Generator[Zone, None, None]
        """
        yield from query_stuff(
            obj=self,
            sub_obj_attrs=["zones", "sub_zones"],
            query=query,
            query_type=self.location.adapter.building_model.zone_query_type,
            **kwargs,
        )

    def request_schedule(self, schedule: SetpointSchedule) -> Response:
        """
        Sends a scheduling request to the API.

        :param schedule: The schedule to execute.
        :type schedule: SetpointSchedule
        :return: The response for the scheduling request.
        :rtype: requests.Response
        """
        if self.location is None:
            raise ValueError("Unit is not properly configured. Location is missing.")
        elif self.location.adapter is None:
            raise ValueError("Location is not properly configured. Adapter is missing.")
        return self.location.adapter.put_setpoint_schedule(
            schedule=schedule, control_unit=self
        )

    def get_schedule(
        self,
        date_range: DateRange,
    ) -> SetpointSchedule:
        """
        Loads the past schedule for the unit and a given period.

        :param date_range: The date range for the schedule.
        :type date_range: DateRange
        :return: The setpoint schedule for the specified date range.
        :rtype: SetpointSchedule
        """
        if self.setpoint_schedule is None:
            raise NotFoundError("Setpoint schedule not supported for this unit.")
        return self.setpoint_schedule.get(date_range)

    def get_electricity_price(
        self,
        date_range: DateRange,
        include_tariff: bool = True,
        include_vat: bool = True,
    ) -> ElectricityPrices:
        """
        Retrieves electricity prices for the unit.

        :param date_range: The date range for the electricity prices.
        :type date_range: DateRange
        :return: A DataFrame containing the electricity prices.
        :rtype: pd.DataFrame
        """
        if self.electricity_prices is None:
            raise NotFoundError("Electricity prices not supported for this unit.")
        tariff = "tariff_included" if include_tariff else "tariff_excluded"
        vat = "vat_included" if include_vat else "vat_excluded"
        return self.electricity_prices[tariff][vat].get(date_range)
