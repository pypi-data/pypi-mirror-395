from __future__ import annotations

import copy
import glob
import pathlib
import random
import string
from abc import ABC, abstractmethod
from functools import partial

import numpy as np
import pandas as pd
import yaml
from requests.models import Response

# Avoid importing the top-level package here to prevent circular/partial init issues.
from ..collection import Collection
from ..interfaces import Adapter
from ..loadable_types import (
    ComfortProfile,
    ComfortProfiles,
    ComponentData,
    ElectricityPriceItem,
    ElectricityPrices,
    LoadableData,
    OperationType,
    ScheduleItem,
    Setpoint,
    SetpointSchedule,
)
from ..location import Location, LocationInformation
from ..supplypoint import AppliedPriceComponent, PriceData
from ..time import DateRange, TimeResolution
from ..unit import Component, Device, Unit
from .adapter import TimestampType, building_model
from .types import ComponentType, UnitQuery, UnitType


class MockApiAdapter(Adapter):
    """
    Mock adapter implementation for testing and development purposes.

    This adapter provides simulated data and responses for testing
    without requiring a real backend system.
    """

    def __init__(self, mocks_path: str | None = None):
        """
        Initialize the MockApiAdapter.

        :param mocks_path: Path to the directory containing mock data files
        :type mocks_path: str
        """
        self.mocks_path = mocks_path or str(pathlib.Path(__file__).parent.resolve())
        super().__init__(building_model=building_model)

    def open(self):
        pass

    def close(self):
        pass

    def get_location(self, location_id: int) -> Location:
        path = f"{self.mocks_path}/locations/{location_id}.yaml"
        with open(path, "r") as file:
            building_model_dict = yaml.safe_load(file)
        return Location.from_building_model_dict(data=building_model_dict, adapter=self)

    def get_locations(self, location_ids: list[int]) -> list[Location]:
        return [self.get_location(location_id) for location_id in location_ids]

    def get_all_locations_information(self) -> list[LocationInformation]:
        directory_path = (
            pathlib.Path(__file__).parent.resolve() / "test/mocks/locations"
        )
        yaml_files = glob.glob(str(directory_path / "*.yaml"))
        loc_info = []
        for file in yaml_files:
            with open(file, "r") as f:
                building_model_dict = yaml.safe_load(f)
            loc = Location.from_building_model_dict(
                data=building_model_dict, adapter=self
            )
            loc_info.append(loc.information)
        return loc_info

    def get_all_locations_collection(self) -> Collection:
        return Collection.from_location_information_list(
            location_information_list=self.get_all_locations_information(),
            adapter=self,
        )

    def get_devices(self, location_id: int) -> list[Device]:
        return []

    def load_measurements(
        self,
        components: list[Component],
        date_range: DateRange,
        timestamp_type: TimestampType = TimestampType.ISO,
    ) -> None:
        for component in components:
            loadabletype = component.measurements[date_range.resolution]
            mocked_data = mock_component_data(
                date_range=date_range, component_type=component.type  # type: ignore[arg-type]
            )
            mocked_data.measurements.rename(
                component.id if isinstance(component.parent, Unit) else component.cid,
                inplace=True,
            )
            loadabletype.update(date_range=date_range, data=mocked_data)

    def get_price_components(
        self,
        supply_point_ids: list[int],
    ) -> dict[int, list[AppliedPriceComponent]]:
        pass

    def get_price_data(
        self,
        date_range: DateRange,
        price_component_ids: list[int],
        timestamp_type: TimestampType = TimestampType.ISO,
    ) -> dict[int, PriceData]:
        pass

    def get_setpoint_schedule(
        self,
        date_range: DateRange,
        control_unit: Unit,
    ) -> SetpointSchedule:
        date_range = copy.deepcopy(date_range)
        date_range.resolution = TimeResolution.HOUR
        dr = date_range.to_pandas_date_range()
        values = np.random.uniform(10, 50, len(dr))
        return SetpointSchedule(
            schedule=[
                ScheduleItem(start=t, value=v, operation=OperationType.NORMAL)
                for t, v in zip(dr, values)
            ]
        )

    def put_setpoint_schedule(
        self,
        schedule: SetpointSchedule,
        control_unit: Unit,
    ) -> Response:
        pass

    def get_comfort_profile_setpoints(self, date_range, location) -> ComfortProfiles:
        date_range = copy.deepcopy(date_range)
        comfort_profile_ids = (
            cp
            if (cp := [zone.comfort_profile_id for zone in location.get_zones()])
            else [1]
        )
        date_range.resolution = TimeResolution.HOUR
        dr = date_range.to_pandas_date_range()
        return ComfortProfiles(
            profiles={
                _id: ComfortProfile(
                    id=_id, setpoints=[Setpoint(time=t, setpoint=21) for t in dr]
                )
                for _id in comfort_profile_ids
            }
        )

    def get_electricity_prices(
        self,
        date_range: DateRange,
        unit: Unit,
        include_vat: bool,
        include_tariff: bool,
    ) -> ElectricityPrices:
        date_range = copy.deepcopy(date_range)
        date_range.resolution = TimeResolution.HOUR
        dr = date_range.to_pandas_date_range()
        return ElectricityPrices(
            data=[
                ElectricityPriceItem(time=t, value=np.random.uniform(0, 4)) for t in dr
            ],
            tariff_included=include_tariff,
            vat_included=include_vat,
        )

    def get_features(self, location_id):
        pass

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


class ComponentCharacteristic(ABC):
    """
    Abstract base class for component characteristics in mock data generation.
    """

    @abstractmethod
    def mock(self, data: pd.Series) -> pd.Series:
        pass


class CCNoisy(ComponentCharacteristic):
    """
    Component characteristic that adds noise to data.
    """

    def __init__(self, mean: float = 0.0, std: float = 1.0):
        """
        Initialize CCNoisy.

        :param mean: Mean of the noise distribution
        :type mean: float
        :param std: Standard deviation of the noise distribution
        :type std: float
        """
        self.mean = mean
        self.std = std

    def mock(self, data: pd.Series) -> pd.Series:
        return pd.Series(
            np.random.normal(self.mean, self.std, len(data)), index=data.index
        )


class CCMonotonicAscending(ComponentCharacteristic):
    """
    Component characteristic that creates monotonically ascending data.
    """

    def mock(self, data: pd.Series) -> pd.Series:
        return data.abs().cumsum()


class CCRangeConstricted(ComponentCharacteristic):
    """
    Component characteristic that constrains data to a specific range.
    """

    def __init__(self, min: float = 0.0, max: float = 100.0):
        """
        Initialize CCRangeConstricted.

        :param min: Minimum value of the range
        :type min: float
        :param max: Maximum value of the range
        :type max: float
        """
        self.min = min
        self.max = max

    def mock(self, data: pd.Series) -> pd.Series:
        imin = data.min()
        imax = data.max()
        if imin == imax:
            data = pd.Series(
                np.full(len(data), self.max / 2 - self.min / 2), index=data.index
            )
        else:
            data = self.min + (self.max - self.min) * (data - imin) / (imax - imin)
        return data


class CCYearlyPeriodic(ComponentCharacteristic):
    """
    Component characteristic that adds yearly periodic variation.
    """

    def __init__(self, amplitude: float = 1.0, day_of_year_top: float = 365 / 2):
        """
        Initialize CCYearlyPeriodic.

        :param amplitude: Amplitude of the periodic variation
        :type amplitude: float
        :param day_of_year_top: Day of year when the sine wave peaks
        :type day_of_year_top: float
        """
        self.amplitude = amplitude
        self.day_of_year_top = day_of_year_top

    def mock(self, data: pd.Series) -> pd.Series:
        return data + pd.Series(
            self.amplitude
            * np.sin(2 * np.pi * (data.index.dayofyear - self.day_of_year_top) / 365),
            index=data.index,
        )


class CCDailyPeriodic(ComponentCharacteristic):
    """
    Component characteristic that adds daily periodic variation.
    """

    def __init__(self, amplitude: float = 1.0, hour_of_day_top: float = 12):
        """
        Initialize CCDailyPeriodic.

        :param amplitude: Amplitude of the periodic variation
        :type amplitude: float
        :param hour_of_day_top: Hour of day when the sine wave peaks
        :type hour_of_day_top: float
        """
        self.amplitude = amplitude
        self.hour_of_day_top = hour_of_day_top

    def mock(self, data: pd.Series) -> pd.Series:
        return data + pd.Series(
            self.amplitude
            * np.sin(2 * np.pi * (data.index.hour - self.hour_of_day_top) / 24),
            index=data.index,
        )


def get_component_type_mocks(
    component_type: ComponentType,
) -> list[ComponentCharacteristic]:
    lookup = {
        ComponentType.FLOW: [CCNoisy(), CCRangeConstricted(min=0.0, max=500.0)],
        ComponentType.SUPPLY_TEMPERATURE: [
            CCNoisy(),
            CCDailyPeriodic(hour_of_day_top=19),
            CCRangeConstricted(min=10, max=100),
        ],
        ComponentType.RETURN_TEMPERATURE: [
            CCNoisy(),
            CCDailyPeriodic(hour_of_day_top=19),
            CCRangeConstricted(min=10, max=100),
        ],
        ComponentType.PRIMARY_SUPPLY_TEMPERATURE: [
            CCNoisy(),
            CCDailyPeriodic(hour_of_day_top=19),
            CCRangeConstricted(min=10, max=100),
        ],
        ComponentType.PRIMARY_RETURN_TEMPERATURE: [
            CCNoisy(),
            CCDailyPeriodic(hour_of_day_top=19),
            CCRangeConstricted(min=10, max=100),
        ],
        ComponentType.VOLUME: [
            CCNoisy(),
            CCYearlyPeriodic(day_of_year_top=30),
            CCRangeConstricted(min=0, max=20),
            CCMonotonicAscending(),
        ],
        ComponentType.ENERGY: [
            CCNoisy(),
            CCYearlyPeriodic(day_of_year_top=30),
            CCRangeConstricted(min=0, max=20),
            CCMonotonicAscending(),
        ],
        ComponentType.POWER: [
            CCNoisy(),
            CCYearlyPeriodic(day_of_year_top=30),
            CCRangeConstricted(min=0, max=20),
        ],
        ComponentType.HP_ON: [CCNoisy(), CCRangeConstricted(min=0.0, max=1.0)],
        ComponentType.MOTOR_POSITION: [
            CCNoisy(),
            CCRangeConstricted(min=0.0, max=100.0),
        ],
        ComponentType.AMBIENT_TEMPERATURE: [
            CCNoisy(),
            CCDailyPeriodic(),
            CCYearlyPeriodic(day_of_year_top=200),
            CCRangeConstricted(min=-10.0, max=40.0),
        ],
        ComponentType.TEMPERATURE: [
            CCNoisy(),
            CCDailyPeriodic(),
            CCYearlyPeriodic(day_of_year_top=200),
            CCRangeConstricted(min=10, max=40),
        ],
        ComponentType.SETPOINT: [
            CCNoisy(),
            CCDailyPeriodic(),
            CCYearlyPeriodic(day_of_year_top=200),
            CCRangeConstricted(min=10, max=40),
        ],
        ComponentType.HUMIDITY: [CCNoisy(), CCRangeConstricted(min=50, max=80)],
        ComponentType.CONTROL_INPUT: [
            CCNoisy(),
            CCRangeConstricted(min=50, max=60),
        ],
        ComponentType.CONTROLLED_SIGNAL: [
            CCNoisy(),
            CCRangeConstricted(min=45, max=65),
        ],
    }
    return lookup[component_type] if component_type in lookup else [CCNoisy()]


def mock_component_data(
    date_range: DateRange, component_type: ComponentType
) -> ComponentData:
    index = date_range.to_pandas_date_range()
    series = pd.Series(np.zeros(shape=len(index)), index=index)
    for chts in get_component_type_mocks(component_type):
        series = chts.mock(series)
    return ComponentData(measurements=series)


def generate_random_string(length=8):
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


# Helper function to generate unique random integers
def generate_unique_random_ints(count, start=1000, end=9999):
    return random.sample(range(start, end + 1), count)


# Main function to edit the dictionary
def anonymize_building_model_dict(
    building_model_dict: dict, mock_id: int, unit_ids_to_mock: list[int]
) -> tuple[dict, dict[int, int]]:
    random.seed(mock_id)
    mock_unit_mapping = {}
    keys_to_replace = {
        "name": generate_random_string,
        "description": generate_random_string,
        "address": generate_random_string,
        "city": generate_random_string,
        "country": generate_random_string,
        "label": generate_random_string,
        "postcode": generate_random_string,
        "organisation_name": generate_random_string,
        "parent_organisation_name": generate_random_string,
        "latitude": lambda: random.uniform(0, 90),
        "longitude": lambda: random.uniform(0, 180),
        "area": lambda: random.uniform(0, 1000),
        "zipcode": lambda: str(random.randint(1000, 9999)),
    }
    dictionary = {}

    def anonymize(key, d, ids, pkey="information"):
        if isinstance(d, dict):
            return {k: anonymize(k, v, ids, key) for k, v in d.items()}
        elif isinstance(d, list):
            return [anonymize(key, v, ids, pkey) for v in d]
        elif key in keys_to_replace:
            return keys_to_replace[key]()
        elif d is None:
            return None
        elif key.endswith("id") or key.endswith("Id"):
            if key == "unit_id":
                key = "id"
                pkey = "children"
            dkey = f"{pkey}_{key}_{d}"
            if dkey in dictionary:
                return dictionary[dkey]
            dictionary[dkey] = ids.pop()
            if d in unit_ids_to_mock:
                mock_unit_mapping[d] = dictionary[dkey]
            return dictionary[dkey]
        else:
            return d

    # Generate unique random integers for keys ending in "id"
    unique_ints = generate_unique_random_ints(10000, end=99999)

    anon = anonymize("information", building_model_dict, unique_ints)

    def add_consistency(key, d):
        if isinstance(d, dict):
            return {k: add_consistency(k, v) for k, v in d.items()}
        elif isinstance(d, list):
            return [add_consistency(key, v) for v in d]
        elif key == "related_units":
            for key_try in [f"children_id_{d}", f"units_id_{d}"]:
                if key_try in dictionary:
                    return dictionary[key_try]
        elif key in ("zones", "adjacentZones"):
            for key_try in [f"zones_id_{d}", f"subZones_id_{d}"]:
                if key_try in dictionary:
                    return dictionary[key_try]
        else:
            return d

    anon = add_consistency(None, anon)

    anon["id"] = mock_id
    anon["information"]["id"] = mock_id

    return anon, mock_unit_mapping
