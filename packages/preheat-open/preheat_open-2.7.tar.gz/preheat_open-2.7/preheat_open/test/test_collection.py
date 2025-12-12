import doctest
from datetime import datetime

import pandas as pd
import pytest

import preheat_open as po
import preheat_open.collection
from preheat_open.interfaces import Adapter


@pytest.fixture(scope="module")
def test_collection(mock_adapter: Adapter):
    loc_info = mock_adapter.get_all_locations_information()
    return po.Collection.from_location_information_list(
        location_information_list=loc_info, adapter=mock_adapter
    )


def test_collection_locations(test_collection: po.Collection):
    test_collection.load_building_models()
    assert isinstance(test_collection.locations, dict)
    assert len(test_collection.locations) > 0
    for info, loc in test_collection.locations.items():
        assert isinstance(info, po.LocationInformation)
        assert isinstance(loc, po.Location)


def test_collection_get_measurements(test_collection: po.Collection):
    df = test_collection.get_measurements(
        date_range=po.DateRange(
            start=datetime(2024, 6, 1),
            end=datetime(2024, 6, 2),
            resolution=po.TimeResolution.HOUR,
        )
    )
    assert isinstance(df, pd.DataFrame)


def test_collection_get_units(test_collection: po.Collection):
    units = list(test_collection.get_units())
    assert all(isinstance(unit, po.Unit) for unit in units)


def test_collection_get_devices(test_collection: po.Collection):
    devices = list(test_collection.get_devices())
    assert all(isinstance(device, po.Device) for device in devices)


def test_collection_get_zones(test_collection: po.Collection):
    zones = list(test_collection.get_zones())
    assert all(isinstance(zone, po.Zone) for zone in zones)


def test_collection_get_components(test_collection: po.Collection):
    components = list(test_collection.get_components())
    assert all(isinstance(component, po.Component) for component in components)


def test_collection_timezone(test_collection: po.Collection):
    timezone = test_collection.timezone
    assert timezone.key == "Europe/Copenhagen"  # Assuming default timezone


def test_doctests():
    """
    Run doctests for the collection module.
    """
    results = doctest.testmod(preheat_open.collection)
    assert (
        results.failed == 0
    ), f"Doctests failed: {results.failed} failed out of {results.attempted}"
