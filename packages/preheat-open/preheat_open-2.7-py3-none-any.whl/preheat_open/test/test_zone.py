import pytest

from preheat_open.zone import VentilationInfo, Zone


@pytest.fixture
def zone():
    sub_zone1 = Zone(
        id=2,
        name="SubZone",
        type="Residential",
        external_identifier="SubZone1",
        area=50.0,
        has_external_wall=True,
        parent=None,
        sub_zones=[],
        units=[],
        adjacent_zones=[],
        comfort_profile_id=11,
        ventilation_information=VentilationInfo(
            has_ventilation_supply=True, has_ventilation_exhaust=False
        ),
    )
    sub_zone2 = Zone(
        id=3,
        name="SubZone2",
        type="Residential",
        external_identifier="SubZone2",
        area=50.0,
        has_external_wall=True,
        parent=None,
        sub_zones=[],
        units=[],
        adjacent_zones=[],
        comfort_profile_id=12,
        ventilation_information=VentilationInfo(
            has_ventilation_supply=True, has_ventilation_exhaust=False
        ),
    )
    return Zone(
        id=1,
        name="MainZone",
        type="Residential",
        external_identifier="Zone1",
        area=100.0,
        has_external_wall=True,
        parent=None,
        sub_zones=[sub_zone1, sub_zone2],
        units=[],
        adjacent_zones=[2, 3],
        comfort_profile_id=10,
        ventilation_information=VentilationInfo(
            has_ventilation_supply=True, has_ventilation_exhaust=False
        ),
    )


def test_zone_post_init(zone):
    assert len(zone.sub_zones) == 2
    assert isinstance(zone.sub_zones[0], Zone)
    assert zone.sub_zones[0].name == "SubZone"


def test_zone_to_building_model_dict(zone):
    expected_dict = {
        "id": 1,
        "name": "MainZone",
        "type": "Residential",
        "externalIdentifier": "Zone1",
        "area": 100.0,
        "hasExternalWall": True,
        "subZones": [z.to_building_model_dict() for z in zone.sub_zones],
        "adjacentZones": [2, 3],
        "comfortProfileId": 10,
        "ventilation_information": {
            "has_ventilation_supply": True,
            "has_ventilation_exhaust": False,
        },
    }
    assert zone.to_building_model_dict() == expected_dict


def test_zone_from_building_model_dict():
    data = {
        "id": 1,
        "name": "MainZone",
        "type": "Residential",
        "externalIdentifier": "Zone1",
        "area": 100.0,
        "hasExternalWall": True,
        "parent": None,
        "subZones": [],
        "units": [],
        "adjacentZones": [2, 3],
        "comfortProfileId": 10,
        "ventilation_information": {
            "has_ventilation_supply": True,
            "has_ventilation_exhaust": False,
        },
    }
    zone = Zone.from_building_model_dict(data)
    assert zone.id == 1
    assert zone.name == "MainZone"
    assert zone.type == "Residential"
    assert zone.external_identifier == "Zone1"
    assert zone.area == 100.0
    assert zone.has_external_wall is True
    assert zone.parent is None
    assert zone.adjacent_zones == [2, 3]
    assert zone.comfort_profile_id == 10
    assert zone.ventilation_information.has_ventilation_supply is True
    assert zone.ventilation_information.has_ventilation_exhaust is False


def test_zone_repr(zone):
    assert repr(zone) == "Zone(type=Residential, name=MainZone, id=1)"
