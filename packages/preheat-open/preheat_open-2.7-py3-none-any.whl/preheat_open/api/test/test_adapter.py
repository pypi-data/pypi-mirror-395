from datetime import datetime

import pytest

import preheat_open as po
import preheat_open.api as papi
from preheat_open.api.adapter import LocationNotFoundError
from preheat_open.loadable_types import (
    ComfortProfile,
    ComfortProfiles,
    ElectricityPrices,
)

TEST_LOCATION_ID = 2756


@pytest.fixture
def date_range():
    return po.DateRange(
        start=datetime(2024, 1, 1),
        end=datetime(2024, 1, 15),
        resolution=po.TimeResolution.HOUR,
    )


@pytest.fixture
def real_location(api_adapter):
    return api_adapter.get_location(location_id=TEST_LOCATION_ID)


@pytest.fixture
def real_unit(real_location):
    return real_location.units[0]


def test_get_features(api_adapter, real_location):
    features = api_adapter.get_features(location_id=real_location.id)
    assert isinstance(features, list)


def test_get_all_locations_information(api_adapter):
    locations_info = api_adapter.get_all_locations_information()
    assert isinstance(locations_info, list)
    assert all(isinstance(info, po.LocationInformation) for info in locations_info)


def test_get_all_locations_collection(api_adapter):
    collection = api_adapter.get_all_locations_collection()
    assert isinstance(collection, po.Collection)


def test_get_location(real_location):
    assert isinstance(real_location, po.Location)


def test_get_location_not_found(api_adapter):
    with pytest.raises(LocationNotFoundError):
        api_adapter.get_location(location_id=999)


def test_get_locations(api_adapter):
    locations = api_adapter.get_locations(location_ids=[TEST_LOCATION_ID])
    assert isinstance(locations, list)
    assert all(isinstance(loc, po.Location) for loc in locations)


def test_get_devices(api_adapter):
    devices = api_adapter.get_devices(location_id=TEST_LOCATION_ID)
    assert isinstance(devices, list)
    assert all(isinstance(device, po.Device) for device in devices)


def test_load_measurements(api_adapter, date_range):
    components = [
        po.Component(
            id=1,
            parent=po.Unit(
                id=1,
                type=papi.UnitType.WEATHER_FORECAST,
                location=po.Location(id=TEST_LOCATION_ID),
            ),
        )
    ]
    api_adapter.load_measurements(components=components, date_range=date_range)
    assert components[0].measurements[date_range.resolution] is not None


def test_get_price_components(api_adapter, real_location):
    test_supply_point = real_location.supply_points[0]
    price_components = api_adapter.get_price_components(
        supply_point_ids=[test_supply_point.id]
    )
    assert isinstance(price_components, dict)
    assert all(isinstance(key, int) for key in price_components.keys())
    assert all(isinstance(value, list) for value in price_components.values())
    assert all(
        isinstance(item, po.AppliedPriceComponent)
        for sublist in price_components.values()
        for item in sublist
    )


def test_get_price_data(api_adapter, date_range):
    price_data = api_adapter.get_price_data(
        date_range=date_range, price_component_ids=[1]
    )
    assert isinstance(price_data, dict)
    assert all(isinstance(key, int) for key in price_data.keys())
    assert all(isinstance(value, po.PriceData) for value in price_data.values())


def test_get_setpoint_schedule(api_adapter, real_location, date_range):
    control_unit = list(real_location.get_units(type="controls"))[0]
    setpoint_schedule = api_adapter.get_setpoint_schedule(
        control_unit=control_unit, date_range=date_range
    )
    assert isinstance(setpoint_schedule, po.SetpointSchedule)


def test_get_comfort_profile_setpoints(api_adapter, date_range, real_location):
    comfort_profiles = api_adapter.get_comfort_profile_setpoints(
        date_range=date_range, location=real_location
    )
    assert isinstance(comfort_profiles, ComfortProfiles)
    assert all(
        isinstance(profile, ComfortProfile)
        for id, profile in comfort_profiles.profiles.items()
    )


def test_get_electricity_prices(api_adapter, date_range, real_location):
    electricity_unit = list(real_location.get_units(type="electricity"))[0]
    electricity_prices = api_adapter.get_electricity_prices(
        unit=electricity_unit, date_range=date_range
    )
    assert isinstance(electricity_prices, ElectricityPrices)
