from dataclasses import dataclass
from enum import Enum
from functools import partial
from io import StringIO
from typing import Any, Callable, ClassVar, Generator, Optional

import pandas as pd
from requests.exceptions import HTTPError
from requests.models import Response

from preheat_open.configuration import NeogridApiConfig

from ..collection import Collection
from ..interfaces import Adapter, BuildingModel
from ..loadable_types import (
    ComfortProfiles,
    ComponentData,
    ElectricityPrices,
    LoadableData,
    SetpointSchedule,
)
from ..location import Location, LocationInformation
from ..supplypoint import AppliedPriceComponent, PriceData
from ..time import DateRange, TimeResolution, datetime, timedelta
from ..unit import Component, Device, Unit
from ..zone import Zone
from .cache import Cache, easy_cache, get_cache
from .factories import (
    AppliedPriceComponentFactory,
    ComfortProfilesFactory,
    DeviceFactory,
    ElectricityPriceItemFactory,
    LocationFactory,
    LocationInformationFactory,
    PriceDataFactory,
    ScheduleItemFactory,
)
from .session import ApiSession
from .types import (
    ComponentQuery,
    ComponentType,
    ControlSettingType,
    DeviceQuery,
    UnitQuery,
    UnitSubType,
    UnitType,
    ZoneQuery,
)


class LocationNotFoundError(Exception):
    pass


class MissingElectricityContractError(Exception):
    pass


@dataclass
class EndpointInformation:
    endpoint: Callable
    id_tag: str
    id_limit: int | None
    measurement_limit: int | None
    time_limit: dict[TimeResolution, timedelta] | timedelta | None
    out: str

    def __hash__(self) -> int:
        return hash(self.endpoint)


class MeasurementEndpointType(EndpointInformation, Enum):
    UNIT = lambda x: "units/measurements", "id", 100, 89_900, None, "csv"
    DEVICE = lambda x: "measurements", "cid", 100, 89_900, None, "csv"
    WEATHER = (
        lambda x: f"weather/{x}",
        "type_id",
        None,
        None,
        {TimeResolution.HOUR: timedelta(days=30)},
        "csv",
    )
    EARLIEST = lambda x: "units/measurements/earliest", "id", 1000, None, None, "json"
    LATEST = lambda x: "units/measurements/latest", "id", 1000, None, None, "json"
    COMFORTPROFILE = (
        lambda x: "locations/{x}/comfortprofile/setpoints",
        None,
        None,
        None,
        timedelta(days=30),
        "json",
    )


class TimestampType(Enum):
    ISO = "iso_8601"
    EPOCH = "epoch_milliseconds"


@dataclass
class MeasurementsGetter:
    api_session: ApiSession
    components: list[Component]
    date_range: DateRange
    timestamp_type: TimestampType

    def subdivide_ids(self, endpoint_type: MeasurementEndpointType, ids: list[int]):
        return [
            ids[x : x + endpoint_type.id_limit]
            for x in range(0, len(ids), endpoint_type.id_limit)
        ]

    def get_time_freq(
        self,
        endpoint_type: MeasurementEndpointType,
        ids: list[int],
        date_range: DateRange,
    ) -> timedelta:
        if endpoint_type.measurement_limit is not None:
            return (
                date_range.resolution.timedelta
                * (endpoint_type.measurement_limit - 100)
                / len(ids)
            )
        else:
            if isinstance(endpoint_type.time_limit, dict):
                return (
                    endpoint_type.time_limit[self.date_range.resolution]
                    if self.date_range.resolution in endpoint_type.time_limit
                    else timedelta(days=100_000)
                )
            else:
                return endpoint_type.time_limit

    def get_params(
        self,
        endpoint_type: MeasurementEndpointType,
        ids: list[int],
        date_range: DateRange = None,
    ) -> Generator[dict[str, Any], None, None]:
        if date_range is None:
            yield from self.get_params(
                endpoint_type=endpoint_type,
                ids=ids,
                date_range=self.date_range,
            )
        elif endpoint_type.id_limit is not None and len(ids) > endpoint_type.id_limit:
            for ids_chunk in self.subdivide_ids(endpoint_type=endpoint_type, ids=ids):
                yield from self.get_params(
                    endpoint_type=endpoint_type, ids=ids_chunk, date_range=date_range
                )
        else:
            freq = self.get_time_freq(
                endpoint_type=endpoint_type, ids=ids, date_range=date_range
            )
            for start, end in date_range.iter_ranges(freq=freq):
                yield self.format_params(
                    endpoint_type=endpoint_type,
                    start=start,
                    end=end,
                    ids=ids,
                )

    def format_params(
        self,
        endpoint_type: MeasurementEndpointType,
        ids: list[int],
        start: datetime,
        end: datetime,
    ):
        if (
            endpoint_type == MeasurementEndpointType.WEATHER
            and self.date_range.resolution > TimeResolution.HOUR
        ):
            resolution = TimeResolution.HOUR
        else:
            resolution = self.date_range.resolution
        return {
            f"{endpoint_type.id_tag}s": ids,
            "start_time": start,
            "end_time": end,
            "time_resolution": resolution,
            "timestamp_type": self.timestamp_type,
        }

    def sort_components(self) -> dict[MeasurementEndpointType, dict[int, Component]]:
        wmap, umap, dmap = {}, {}, {}
        for comp in self.components:
            if isinstance(comp.parent, Unit):
                if comp.parent.type == UnitType.WEATHER_FORECAST:
                    if comp.parent.location.id in wmap:
                        wmap[comp.parent.location.id][comp.id] = comp
                    else:
                        wmap[comp.parent.location.id] = {comp.id: comp}
                else:
                    umap[comp.id] = comp
            elif isinstance(comp.parent, Device):
                dmap[comp.cid] = comp
            else:
                raise TypeError(f"Invalid component type, '{type(comp)}'!")

        sorted_dict = {
            MeasurementEndpointType.DEVICE: dmap,
            MeasurementEndpointType.UNIT: umap,
        } | {MeasurementEndpointType.WEATHER: wm for loc_id, wm in wmap.items()}

        return {key: val for key, val in sorted_dict.items() if val}

    def make_requests(
        self,
        endpoint_type: MeasurementEndpointType,
        ids: list[int],
        location_id: int = None,
    ):
        for params in self.get_params(endpoint_type=endpoint_type, ids=ids):
            resp = self.api_session.get(
                endpoint=endpoint_type.endpoint(location_id),
                params=params,
                out=endpoint_type.out,
            ).text
            if endpoint_type.out == "csv":
                yield pd.read_csv(
                    StringIO(resp),
                    sep=";",
                    parse_dates=["time"],
                    date_format=self.api_session.datetime_format,
                ).pivot(index="time", columns=endpoint_type.id_tag, values="value")
            elif endpoint_type.out == "json":
                raise NotImplementedError()

    @staticmethod
    def get_location_id(component_map: dict[int, Component]) -> int | None:
        return (
            loc_ids[0]
            if len(
                set(
                    loc_ids := [
                        comp.parent.location.id for comp in component_map.values()
                    ]
                )
            )
            == 1
            else None
        )

    def load_measurements(self) -> None:
        for endpoint_type, component_map in self.sort_components().items():
            df = pd.concat(
                list(
                    self.make_requests(
                        endpoint_type=endpoint_type,
                        ids=list(component_map.keys()),
                        location_id=self.get_location_id(component_map),
                    )
                )
            )
            for col, component in component_map.items():
                comp_data = component.measurements[self.date_range.resolution]
                if col in df:
                    cdata = ComponentData(measurements=df[col].dropna())
                else:
                    cdata = ComponentData()
                comp_data.update(date_range=self.date_range, data=cdata)


building_model = BuildingModel(
    component_query_type=ComponentQuery,
    component_type=ComponentType,
    unit_query_type=UnitQuery,
    unit_type=UnitType,
    unit_subtype=UnitSubType,
    device_query_type=DeviceQuery,
    device_type=Device,
    zone_query_type=ZoneQuery,
    zone_type=Zone,
    control_setting_type=ControlSettingType,
)


@dataclass
class ApiAdapter(Adapter):
    config: Optional[NeogridApiConfig] = None
    _api_session: Optional[ApiSession] = None
    _cache: Optional[Cache] = None
    building_model: ClassVar[BuildingModel] = building_model

    def __post_init__(self):
        self.config = NeogridApiConfig() if self.config is None else self.config

    def open(self):
        if self._api_session is None:
            self._api_session = ApiSession(
                config=self.config,
            )
        if self._cache is None:
            self._cache = get_cache()

    def close(self):
        self._api_session.close()

    @easy_cache()
    def get_features(self, location_id: int):
        resp = self._api_session.get(endpoint=f"features/{location_id}").json()
        return resp

    def location_key(self, location_id: int) -> str:
        return f"{self.__class__.__name__}_get_location_{location_id}"

    def update_location_cache(self, location: Location):
        if self._cache is not None:
            self._cache.set(self.location_key(location.id), location)

    @easy_cache()
    def get_all_locations_information(self) -> list[LocationInformation]:
        resp = self._api_session.get(endpoint="locations").json()
        if "locations" in resp:
            return [LocationInformationFactory(r).build() for r in resp["locations"]]
        else:
            raise Exception("No locations found. Check API_KEY validity.")

    def get_all_locations_collection(self) -> Collection:
        return Collection.from_location_information_list(
            location_information_list=self.get_all_locations_information(),
            adapter=self,
        )

    def get_location(self, location_id: int) -> Location:
        key = self.location_key(location_id)
        if self._cache is not None:
            location = self._cache.get(key)
            if location is not None:
                location.adapter = self
                return location

        location_not_found = False
        try:
            resp = self._api_session.get(endpoint=f"locations/{location_id}").json()
        except HTTPError as e:
            if e.response.status_code == 403:
                location_not_found = True
            else:
                raise e

        if location_not_found or "building" not in resp:
            raise LocationNotFoundError(
                f"Location not found for location_id={location_id}. Please check the location_id and that you have the proper permissions to this location."
            )

        location = LocationFactory(resp["building"] | {"adapter": self}).build()
        self.update_location_cache(location)
        return location

    def get_locations(self, location_ids: list[int]) -> list[Location]:
        cached_locations = (
            []
            if self._cache is None
            else [
                loc
                for lid in location_ids
                if (loc := self._cache.get(self.location_key(lid))) is not None
            ]
        )

        api_location_ids = [
            lid
            for lid in location_ids
            if lid not in [loc.id for loc in cached_locations]
        ]
        api_locations = []
        if api_location_ids:
            resp = self._api_session.get(
                endpoint=f"buildings", params={"id": api_location_ids}
            ).json()
            api_locations = [
                LocationFactory(r["building"] | {"adapter": self}).build()
                for _, r in resp.items()
            ]
            for loc in api_locations:
                self.update_location_cache(loc)

        return cached_locations + api_locations

    def get_devices(self, location_id: int) -> list[Device]:
        resp = self._api_session.get(endpoint=f"locations/{location_id}/devices").json()
        if "devices" in resp:
            return [DeviceFactory(r).build() for r in resp["devices"]]
        else:
            raise Exception("No devices found. Check API_KEY validity.")

    def load_measurements(
        self,
        components: list[Component],
        date_range: DateRange,
        timestamp_type: TimestampType = TimestampType.ISO,
    ) -> None:
        getter = MeasurementsGetter(
            api_session=self._api_session,
            components=components,
            date_range=date_range,
            timestamp_type=timestamp_type,
        )
        getter.load_measurements()
        locations = {comp.parent.location for comp in components}
        for loc in locations:
            self.update_location_cache(loc)

    def get_price_components(
        self,
        supply_point_ids: list[int],
    ) -> dict[int, list[AppliedPriceComponent]]:
        params = {"ids": supply_point_ids}
        resp = self._api_session.get(
            "supplypoints/pricecomponents", params=params
        ).json()
        return {
            int(key): [AppliedPriceComponentFactory(elem).build() for elem in val]
            for key, val in resp.items()
        }

    def get_price_data(
        self,
        date_range: DateRange,
        price_component_ids: list[int],
        timestamp_type: TimestampType = TimestampType.ISO,
    ) -> dict[int, PriceData]:
        params = {
            "start_time": date_range.lstart,
            "end_time": date_range.rend,
            "ids": price_component_ids,
            "timestamp_type": timestamp_type,
        }
        resp = self._api_session.get("pricecomponents/prices", params=params).json()
        return {int(key): PriceDataFactory(val).build() for key, val in resp.items()}

    def get_setpoint_schedule(
        self,
        date_range: DateRange,
        control_unit: Unit | int,
    ) -> SetpointSchedule:
        if isinstance(control_unit, Unit):
            if control_unit.type != UnitType.CONTROL:
                raise ValueError(
                    f"Unit type '{control_unit.type}' is not a control unit. Please provide a control unit."
                )
            control_unit_id = control_unit.id
        else:
            control_unit_id = control_unit
        params = {"start_time": date_range.lstart, "end_time": date_range.rend}
        resp = self._api_session.get(
            endpoint=f"controlunit/{control_unit_id}/setpoint", params=params
        ).json()
        return SetpointSchedule(
            schedule=[ScheduleItemFactory(r).build() for r in resp]
        ).astimezone(tz=control_unit.timezone)

    def put_setpoint_schedule(
        self,
        schedule: SetpointSchedule,
        control_unit: Unit | int,
    ) -> Response:
        if isinstance(control_unit, Unit):
            if control_unit.type != UnitType.CONTROL:
                raise ValueError(
                    f"Unit type '{control_unit.type}' is not a control unit. Please provide a control unit."
                )
            control_unit_id = control_unit.id
        else:
            control_unit_id = control_unit
        payload = {
            "schedule": [
                {
                    "startTime": item.start,
                    "value": item.value,
                    "operation": item.operation,
                }
                for item in schedule.schedule
            ]
        }
        return self._api_session.put(
            endpoint=f"controlunit/{control_unit_id}/setpoint",
            json_body=payload,
        )

    def get_comfort_profile_setpoints(
        self, date_range: DateRange, location: Location | int
    ) -> ComfortProfiles:
        location_id = location.id if isinstance(location, Location) else location
        params = {"start_time": date_range.lstart, "end_time": date_range.rend}
        resp = self._api_session.get(
            endpoint=f"locations/{location_id}/comfortprofile/setpoints", params=params
        ).json()
        return ComfortProfilesFactory(resp).build().astimezone(tz=location.timezone)

    def get_electricity_prices(
        self,
        date_range: DateRange,
        unit: Unit,
        include_vat: bool = True,
        include_tariff: bool = True,
        timestamp_type: TimestampType = TimestampType.ISO,
    ) -> list[ElectricityPrices]:
        if unit.type not in (UnitType.ELECTRICITY, UnitType.SUB_METER):
            raise ValueError(
                f"Unit '{unit}' are not electricity unit. Please provide electricity units or submeters."
            )
        params = {
            "ids": [unit.id],
            "start_time": date_range.lstart,
            "end_time": date_range.rend,
            "timestamp_type": timestamp_type,
            "include_tariff": include_tariff,
            "include_vat": include_vat,
        }
        resp = self._api_session.get(
            endpoint=f"units/electricity/price", params=params
        ).json()

        prices = resp.get(str(unit.id), [])

        return ElectricityPrices(
            data=[ElectricityPriceItemFactory(item).build() for item in prices],
            tariff_included=include_tariff,
            vat_included=include_vat,
        )

    def location_post_setup(self, location: Location):
        location.comfort_profiles = (
            LoadableData(
                data=ComfortProfiles(),
                getter=partial(
                    self.get_comfort_profile_setpoints,
                    location=location,
                ),
            )
            if location.comfort_profiles is None
            else location.comfort_profiles
        )
        for u in location.get_units(UnitQuery(type=UnitType.CONTROL)):
            u.setpoint_schedule = (
                LoadableData(
                    data=SetpointSchedule(),
                    getter=partial(
                        self.get_setpoint_schedule,
                        control_unit=u,
                    ),
                    setter=partial(
                        self.put_setpoint_schedule,
                        control_unit=u,
                    ),
                )
                if u.setpoint_schedule is None
                else u.setpoint_schedule
            )
        for u in location.get_units(
            UnitQuery(type=[UnitType.ELECTRICITY, UnitType.SUB_METER])
        ):
            if u.type == UnitType.SUB_METER and u.parent.type != UnitType.ELECTRICITY:
                continue
            elif u.electricity_prices is None:
                u.electricity_prices = {
                    "tariff_included"
                    if t
                    else "tariff_excluded": {
                        "vat_included"
                        if v
                        else "vat_excluded": LoadableData(
                            data=ElectricityPrices(),
                            getter=partial(
                                self.get_electricity_prices,
                                unit=u,
                                include_vat=v,
                                include_tariff=t,
                            ),
                        )
                        for v in [True, False]
                    }
                    for t in [True, False]
                }
