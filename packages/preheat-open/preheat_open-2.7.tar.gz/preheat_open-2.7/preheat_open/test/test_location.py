from datetime import datetime

import pandas as pd

import preheat_open as po


def test_location_get_units(location):
    units = list(location.get_units())
    assert all(isinstance(unit, po.Unit) for unit in units)


def test_location_get_devices(location):
    devices = list(location.get_devices())
    assert all(isinstance(device, po.Device) for device in devices)


def test_location_get_zones(location):
    zones = list(location.get_zones())
    assert all(isinstance(zone, po.Zone) for zone in zones)


def test_location_get_components(location):
    components = list(location.get_components())
    assert all(isinstance(component, po.Component) for component in components)


def test_location_get_measurements(location):
    df = location.get_measurements(
        start=datetime(2024, 6, 1),
        end=datetime(2024, 6, 2),
        resolution=po.TimeResolution.HOUR,
    )
    assert isinstance(df, pd.DataFrame)
