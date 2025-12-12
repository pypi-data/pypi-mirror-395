from itertools import chain

import pandas as pd

from ..interfaces import Factory
from ..loadable_types import (
    ComfortProfile,
    ComfortProfiles,
    ElectricityPriceItem,
    OperationType,
    ScheduleItem,
    ScheduleReason,
    Setpoint,
)
from ..location import Location, LocationCharacteristics, LocationInformation
from ..supplypoint import (
    ApplicationContext,
    ApplicationType,
    AppliedPriceComponent,
    Authority,
    BillingContext,
    FixedPriceData,
    FixedPricePeriod,
    FormatType,
    PriceArea,
    PriceComponent,
    PriceComponentType,
    PriceData,
    SupplyPoint,
)
from ..time import DateRange
from ..unit import (
    Component,
    ControlSetting,
    ControlSettings,
    Device,
    Unit,
    UnitDescriptors,
)
from ..zone import VentilationInfo, Zone
from .session import api_string_to_datetime
from .types import ComponentType, ControlSettingType, UnitSubType, UnitType


class UnitComponentFactory(Factory):
    _return_class = Component
    _translation_dict = {
        "cid": "cid",
        "id": "id",
        "name": "name",
        "type": "type",
        "unit": "unit",
        "std_unit_divisor": "stdUnitDivisor",
        "std_unit": "stdUnit",
        "min": "min",
        "max": "max",
    }


class ControlSettingFactory(Factory):
    _return_class = ControlSetting
    _translation_dict = {
        "type": "type",
        "value": "value",
        "unit": "unit",
    }

    def make_sub_classes(self) -> None:
        self.input_dict["type"] = ControlSettingType.from_key(
            self.input_dict.pop("key")
        )


class ControlSettingsFactory(Factory):
    _return_class = ControlSettings
    _translation_dict = {
        "settings": "settings",
        "parent": "parent",
    }

    def make_sub_classes(self) -> None:
        parent = self.input_dict.pop("parent")
        self.input_dict = {
            "settings": {
                key: ControlSettingFactory(item | {"key": key}).build()
                for key, item in self.input_dict["settings"].items()
            }
        }
        self.input_dict["parent"] = parent


class UnitFactory(Factory):
    _return_class = Unit
    _translation_dict = {
        "type": "unit_type",
        "subtype": "type",
        "id": "id",
        "name": "name",
        "components": "components",
        "descriptors": "descriptors",
        "zones": "zoneIds",
        "shared": "shared",
        "shared_from": "sharedFrom",
        "shared_locations": "sharedLocations",
        "children": "children",
        "related_units": "related_units",
        "buildings_covered": "buildingsCovered",
        "covers_building": "coversBuilding",
        "control_settings": "control_settings",
        "electricity_prices": "electricity_prices",
        "setpoint_schedule": "setpoint_schedule",
    }

    def make_sub_classes(self) -> None:
        unit_type: UnitType = self.input_dict["unit_type"]
        if "type" in self.input_dict:
            self.input_dict["type"] = (
                UnitSubType(t) if (t := self.input_dict["type"]) else None
            )
        self.input_dict["children"] = [
            UnitFactory(input_dict=child | {"unit_type": child_type}).build()
            for child_type in unit_type.children
            if (
                children := val
                if isinstance((val := self.input_dict.pop(child_type.value, [])), list)
                else [val]
            )
            for child in children
            if child is not None
        ]
        self.input_dict["components"] = [
            UnitComponentFactory(comp | {"type": comp_type}).build()
            for comp_type in unit_type.components
            if (comp := self.input_dict.pop(comp_type.value, None)) is not None
        ]
        self.input_dict["descriptors"] = UnitDescriptors(
            **{
                d.value: self.input_dict.pop(d.value)
                for d in unit_type.descriptors
                if d.value in self.input_dict
            }
        )
        self.input_dict["related_units"] = list(
            chain(
                *[
                    record if isinstance(record, list) else [record]
                    for related_unit in unit_type.related_units
                    if (record := self.input_dict.pop(related_unit.value))
                ]
            )
        )
        if "zoneId" in self.input_dict:
            self.input_dict["zoneIds"] = [self.input_dict.pop("zoneId")]
        if "controlSettings" in self.input_dict:
            self.input_dict["control_settings"] = ControlSettingsFactory(
                {
                    "settings": self.input_dict.pop("controlSettings"),
                    "parent": self.input_dict["id"],
                }
            ).build()


class WeatherComponentFactory(Factory):
    _return_class = Component
    _translation_dict = {
        "id": "id",
        "name": "name",
        "unit": "unit",
        "type": "type",
    }


class WeatherFactory(Factory):
    _return_class = Unit
    _translation_dict = {
        "id": "gridId",
        "name": "name",
        "type": "unit_type",
        "components": "types",
    }

    def make_sub_classes(self) -> None:
        self.input_dict["types"] = [
            WeatherComponentFactory(
                comp | {"type": ComponentType(comp["name"])}
            ).build()
            for comp in self.input_dict["types"]
        ]
        self.input_dict["name"] = "Weather Forecast"


class ZoneFactory(Factory):
    _return_class = Zone
    _translation_dict = {
        "id": "id",
        "name": "name",
        "external_identifier": "externalIdentifier",
        "area": "zoneArea",
        "has_external_wall": "hasExternalWall",
        "sub_zones": "subZones",
        "adjacent_zones": "adjacentZones",
        "type": "type",
        "comfort_profile_id": "comfortProfileId",
        "ventilation_information": "ventilation_information",
    }

    def make_sub_classes(self) -> None:
        self.input_dict["adjacentZones"] = [
            d["zoneId"] for d in self.input_dict["adjacentZones"]
        ]
        self.input_dict["subZones"] = [
            ZoneFactory(d) for d in self.input_dict["subZones"]
        ]
        self.input_dict["ventilation_information"] = VentilationInfo(
            has_ventilation_supply=self.input_dict.pop("ventilationSupply"),
            has_ventilation_exhaust=self.input_dict.pop("ventilationExhaust"),
        )


class LocationCharacteristicsFactory(Factory):
    _return_class = LocationCharacteristics
    _translation_dict = {
        "area": "buildingArea",
        "type": "buildingType",
        "number_of_apartments": "apartments",
    }


class LocationInformationFactory(Factory):
    _return_class = LocationInformation
    _translation_dict = {
        "address": "address",
        "city": "city",
        "country": "country",
        "label": "label",
        "latitude": "latitude",
        "longitude": "longitude",
        "id": "locationId",
        "organisation_id": "organizationId",
        "organisation_name": "organizationName",
        "parent_organisation_id": "parentOrganizationId",
        "parent_organisation_name": "parentOrganizationName",
        "timezone": "timezone",
        "zipcode": "zipcode",
    }


class SupplyPointFactory(Factory):
    _return_class = SupplyPoint
    _translation_dict = {
        "id": "id",
        "name": "name",
        "sub_type": "subType",
        "type": "type",
        "units": "unitIds",
    }


class LocationFactory(Factory):
    _return_class = Location
    _translation_dict = {
        "id": "id",
        "information": "location",
        "zones": "zones",
        "units": "units",
        "characteristics": "characteristics",
        "supply_points": "supply_points",
        "adapter": "adapter",
    }

    def make_sub_classes(self) -> None:
        self.input_dict["units"] = [
            UnitFactory(input_dict=d | {"unit_type": utype}).build()
            for utype in UnitType
            if utype.is_top_level
            for d in self.input_dict.pop(utype.value)
        ] + [
            WeatherFactory(
                input_dict=self.input_dict.pop(UnitType.WEATHER_FORECAST.value)
                | {
                    "unit_type": UnitType.WEATHER_FORECAST,
                }
            ).build()
        ]

        self.input_dict["zones"] = [
            ZoneFactory(zone).build() for zone in self.input_dict["zones"]
        ]
        self.input_dict["location"] = LocationInformationFactory(
            self.input_dict["location"]
        ).build()
        self.input_dict["id"] = self.input_dict["location"].id
        self.input_dict["characteristics"] = LocationCharacteristicsFactory(
            {
                key: self.input_dict.pop(key)
                for key in ["buildingArea", "buildingType", "apartments"]
            }
        ).build()
        self.input_dict["supply_points"] = [
            SupplyPointFactory(sp_i).build()
            for sp_i in self.input_dict.pop("supplyPoints")
        ]


class DeviceComponentFactory(Factory):
    _return_class = Component
    _translation_dict = {
        "cid": "cid",
        "id": "id",
        "max": "max",
        "min": "min",
        "name": "name",
        "type": "typeName",
        "unit": "unit",
    }


class DeviceFactory(Factory):
    _return_class = Device
    _translation_dict = {
        "name": "name",
        "id": "id",
        "type": "typeName",
        "serial": "serial",
        "components": "components",
    }

    def make_sub_classes(self) -> None:
        self.input_dict["components"] = [
            DeviceComponentFactory(r).build() for r in self.input_dict["components"]
        ]


class PriceComponentTypeFactory(Factory):
    _return_class = PriceComponentType
    _translation_dict = {
        "id": "id",
        "name": "Name",
    }


class PriceAreaFactory(Factory):
    _return_class = PriceArea
    _translation_dict = {
        "id": "id",
        "name": "name",
        "supply_type": "supplyType",
    }


class AuthorityFactory(Factory):
    _return_class = Authority
    _translation_dict = {
        "id": "id",
        "name": "name",
    }


class PriceComponentFactory(Factory):
    _return_class = PriceComponent
    _translation_dict = {
        "id": "id",
        "name": "name",
        "description": "description",
        "created": "created",
        "type": "type",
        "unit": "unit",
        "format_type": "formatType",
        "application_type": "applicationType",
        "unit_component_type": "unitComponentType",
        "timezone": "timezone",
        "price_area": "priceArea",
        "authority": "authority",
    }

    def make_sub_classes(self) -> None:
        self.input_dict["type"] = PriceComponentTypeFactory(
            self.input_dict["type"]
        ).build()
        self.input_dict["formatType"] = FormatType(self.input_dict["formatType"])
        self.input_dict["applicationType"] = ApplicationType(
            self.input_dict["applicationType"]
        )
        self.input_dict["priceArea"] = PriceAreaFactory(
            self.input_dict["priceArea"]
        ).build()
        self.input_dict["authority"] = AuthorityFactory(
            self.input_dict["authority"]
        ).build()
        self.input_dict["created"] = api_string_to_datetime(self.input_dict["created"])


class AppliedPriceComponentFactory(Factory):
    _return_class = AppliedPriceComponent
    _translation_dict = {
        "id": "id",
        "supplypoint_id": "supplyPointId",
        "price_component": "priceComponent",
        "contract_id": "contractId",
        "created": "created",
        "valid_range": "valid_range",
        "billing_context": "billingContext",
        "application_context": "applicationContext",
    }

    def make_sub_classes(self) -> None:
        self.input_dict["valid_range"] = DateRange(
            start=api_string_to_datetime(val)
            if (val := self.input_dict.pop("validFrom"))
            else None,
            end=api_string_to_datetime(val)
            if (val := self.input_dict.pop("validTo"))
            else None,
        )
        self.input_dict["priceComponent"] = PriceComponentFactory(
            self.input_dict["priceComponent"]
        ).build()
        self.input_dict["billingContext"] = BillingContext(
            self.input_dict["billingContext"]
        )
        self.input_dict["applicationContext"] = ApplicationContext(
            self.input_dict["applicationContext"]
        )


class FixedPriceDataFactory(Factory):
    _return_class = FixedPriceData
    _translation_dict = {
        "position": "position",
        "price": "price",
    }


class FixedPricePeriodFactory(Factory):
    _return_class = FixedPricePeriod
    _translation_dict = {
        "data": "data",
        "date_range": "dateRange",
        "resolution": "resolution",
    }

    def make_sub_classes(self) -> None:
        self.input_dict["data"] = [
            FixedPriceDataFactory(elem).build() for elem in self.input_dict["data"]
        ]
        self.input_dict["dateRange"] = DateRange(
            start=api_string_to_datetime(val)
            if (val := self.input_dict.pop("validFrom"))
            else None,
            end=api_string_to_datetime(val)
            if (val := self.input_dict.pop("validTo"))
            else None,
        )


class PriceDataFactory(Factory):
    _return_class = PriceData
    _translation_dict = {
        "fixed_price_data": "fixedPriceData",
        "time_series_data": "timeSeriesData",
    }

    def make_sub_classes(self) -> None:
        fpd = (
            []
            if self.input_dict["fixedPriceData"] is None
            else self.input_dict["fixedPriceData"]
        )
        self.input_dict["fixedPriceData"] = [
            FixedPricePeriodFactory(elem).build() for elem in fpd
        ]
        self.input_dict["timeSeriesData"] = (
            pd.Series(data) if (data := self.input_dict["timeSeriesData"]) else None
        )


class ScheduleItemFactory(Factory):
    _return_class = ScheduleItem
    _translation_dict = {
        "start": "startTime",
        "value": "value",
        "owner_id": "ownerId",
        "operation": "operation",
        "reason": "reason",
    }

    def make_sub_classes(self) -> None:
        self.input_dict["startTime"] = api_string_to_datetime(
            self.input_dict["startTime"]
        )
        self.input_dict["operation"] = OperationType(self.input_dict["operation"])
        self.input_dict["reason"] = ScheduleReason(self.input_dict.pop("controlReason"))


class SetpointFactory(Factory):
    _return_class = Setpoint
    _translation_dict = {
        "time": "time",
        "setpoint": "setpoint",
        "vacation": "vacation",
        "min": "min",
        "max": "max",
        "override": "override",
    }

    def make_sub_classes(self) -> None:
        self.input_dict["time"] = api_string_to_datetime(self.input_dict["time"])


class ComfortProfileFactory(Factory):
    _return_class = ComfortProfile
    _translation_dict = {
        "id": "id",
        "name": "name",
        "setpoints": "setpoints",
        "flexibility": "flexibility",
    }

    def make_sub_classes(self) -> None:
        self.input_dict["setpoints"] = [
            SetpointFactory(elem).build() for elem in self.input_dict["setpoints"]
        ]


class ComfortProfilesFactory(Factory):
    _return_class = ComfortProfiles
    _translation_dict = {
        "profiles": "comfortProfiles",
    }

    def make_sub_classes(self) -> None:
        self.input_dict["comfortProfiles"] = {
            elem["id"]: ComfortProfileFactory(elem).build()
            for elem in self.input_dict["comfortProfiles"]
        }


class ElectricityPriceItemFactory(Factory):
    _return_class = ElectricityPriceItem
    _translation_dict = {
        "time": "time",
        "value": "value",
    }

    def make_sub_classes(self) -> None:
        self.input_dict["time"] = api_string_to_datetime(self.input_dict["time"])
