from __future__ import annotations

import os
from dataclasses import dataclass, field
from enum import Enum
from functools import lru_cache
from typing import ClassVar, Type

import yaml

from ..query import Query
from ..unit import Component, Device, Unit
from ..zone import Zone


class ControlSettingDataType(Enum):
    BOOL = "BOOL"
    DECIMAL = "DECIMAL"
    ENUM = "ENUM"
    INT = "INT"


class ControlSettingUiType(Enum):
    CHECKBOX = "CHECKBOX"
    NUMBER = "NUMBER"
    RANGE = "RANGE"
    SELECT = "SELECT"


class __ControlSettingTypeEnum(Enum):
    def __init__(
        self,
        id: int,
        key: str,
        default_value: int | float | bool,
        min: int | float,
        max: int | float,
        step: int | float,
        type: ControlSettingDataType,
        ui_type: ControlSettingUiType,
        unit,
        show_in_ui,
        description,
        ui_order,
        ui_advanced,
    ):
        self.key = key
        self.id = id
        self.default_value = default_value
        self.min = min
        self.max = max
        self.step = step
        self.type = (
            type
            if isinstance(type, ControlSettingDataType)
            else ControlSettingDataType(type)
        )
        self.ui_type = (
            ui_type
            if isinstance(ui_type, ControlSettingUiType)
            else ControlSettingUiType(ui_type)
        )
        self.unit = unit
        self.show_in_ui = show_in_ui
        self.description = description
        self.ui_order = ui_order
        self.ui_advanced = ui_advanced

    @classmethod
    def from_key(self, key: str) -> __ControlSettingTypeEnum:
        lookup = {setting.key: setting for setting in self.__members__.values()}
        return lookup[key] if key in lookup else None

    @classmethod
    def contains(cls, value: __ControlSettingTypeEnum) -> bool:
        try:
            cls.from_key(value)
        except:
            return False
        return True


@lru_cache(maxsize=1)
def control_setting_types() -> dict:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(
        file=dir_path + "/control_setting_type.yaml", mode="r", encoding="utf8"
    ) as file:
        return yaml.safe_load(file)


ControlSettingType = __ControlSettingTypeEnum(
    "ControlSettingType",
    {setting["key"]: tuple(setting.values()) for setting in control_setting_types()},
)


class RelatedUnitType(Enum):
    COLD_WATER = "coldWaterId"
    COOLING = "coolingId"
    COOLING_COIL = "coolingCoilIds"
    COOLING_SECONDARY = "coolingSecondaryId"
    ELECTRICITY = "electricityId"
    HEATING = "heatingId"
    HEATING_COIL = "heatingCoilIds"
    HEATING_SECONDARY = "heatingSecondaryId"
    HOT_WATER = "hotWaterId"
    MAIN = "mainId"

    @property
    def unittype(self) -> UnitType:
        lookup = {
            RelatedUnitType.COLD_WATER: UnitType.COLD_WATER,
            RelatedUnitType.COOLING: UnitType.COOLING,
            RelatedUnitType.COOLING_COIL: UnitType.COOLING_COIL,
            RelatedUnitType.COOLING_SECONDARY: UnitType.SECONDARY,
            RelatedUnitType.ELECTRICITY: UnitType.ELECTRICITY,
            RelatedUnitType.HEATING: UnitType.HEATING,
            RelatedUnitType.HEATING_COIL: UnitType.HEATING_COIL,
            RelatedUnitType.HEATING_SECONDARY: UnitType.SECONDARY,
            RelatedUnitType.HOT_WATER: UnitType.HOT_WATER,
            RelatedUnitType.MAIN: UnitType.MAIN,
        }
        return lookup[self] if self in lookup else []


class UnitDescriptorType(Enum):
    ACTIVE = "active"
    BATTERY_CAPACITY = "batteryCapacity"
    BRAND = "brand"
    BUILDINGS_COVERED = "buildingsCovered"
    COMPASS_HEADING = "compassHeading"
    CONFIGURATION = "configuration"
    HEAT_CURVE_OFFSET = "heatCurveOffset"
    HEAT_PUMP_CAPACITY = "heatpumpCapacity"
    MAX_CHARGE_POWER = "maxChargePower"
    MAX_CONVERTER_PEAK_POWER = "maxConverterPeakPower"
    MAX_DISCHARGE_POWER = "maxDischargePower"
    MAX_STATE_OF_CHARGE = "maxStateOfCharge"
    METER_TYPE = "meterType"
    MIN_STATE_OF_CHARGE = "minStateOfCharge"
    NETTO_CAPACITY = "nettoCapacity"
    PANEL_ANGLE = "panelAngle"
    PANEL_PEAK_POWER = "panelPeakPower"
    PLACED_BEFORE_HEAT_RECOVERY = "placedBeforeHeatRecovery"
    PLACEMENT = "placement"
    PLACEMENT_NUMBER = "placementNumber"
    PRODUCES = "produces"

    @property
    def expected_type(self) -> Type:
        lookup = {
            UnitDescriptorType.ACTIVE: bool,
            UnitDescriptorType.BATTERY_CAPACITY: float,
            UnitDescriptorType.BRAND: str,
            UnitDescriptorType.BUILDINGS_COVERED: int,
            UnitDescriptorType.COMPASS_HEADING: float,
            UnitDescriptorType.CONFIGURATION: dict,
            UnitDescriptorType.HEAT_CURVE_OFFSET: float,
            UnitDescriptorType.HEAT_PUMP_CAPACITY: float,
            UnitDescriptorType.MAX_CHARGE_POWER: float,
            UnitDescriptorType.MAX_CONVERTER_PEAK_POWER: float,
            UnitDescriptorType.MAX_DISCHARGE_POWER: float,
            UnitDescriptorType.MAX_STATE_OF_CHARGE: float,
            UnitDescriptorType.METER_TYPE: str,
            UnitDescriptorType.MIN_STATE_OF_CHARGE: float,
            UnitDescriptorType.NETTO_CAPACITY: float,
            UnitDescriptorType.PANEL_ANGLE: float,
            UnitDescriptorType.PANEL_PEAK_POWER: float,
            UnitDescriptorType.PLACED_BEFORE_HEAT_RECOVERY: bool,
            UnitDescriptorType.PLACEMENT: str,
            UnitDescriptorType.PLACEMENT_NUMBER: int,
            UnitDescriptorType.PRODUCES: str,
        }
        return lookup[self] if self in lookup else str


class ComponentType(Enum):
    ACTIVE_EXPORT_CONSUMPTION = "active_export_consumption"
    ACTIVE_EXPORT_COUNTER = "active_export_counter"
    AIR_TEMPERATURE_AFTER = "airTemperatureAfter"
    AIR_TEMPERATURE_BEFORE = "airTemperatureBefore"
    AMBIENT_TEMPERATURE = "ambientTemperature"
    APPARENT_ENERGY = "apparent_energy"
    APPARENT_POWER = "apparent_power"
    BACKUP_ON = "backupOn"
    BATTERY_PERCENTAGE = "batteryPercentage"
    BATTERY_VOLTAGE = "batteryVoltage"
    CHARGE_TEMPERATURE = "chargeT"
    CHARGE_PUMP = "chargePump"
    CHARGING = "charging"
    CIRCULATION_PUMP = "circulationPump"
    CIRCULATION_TEMPERATURE = "circulationT"
    CLOUDINESS_ = "Cloudiness"
    CO2 = "co2"
    CONSUMPTION = "consumption"
    CONTROL_INPUT = "controlInput"
    CONTROL_SWITCH = "controlSwitch"
    CONTROLLED_SIGNAL = "controlledSignal"
    CURRENT = "current"
    CURRENT_WINDOW_POSITION = "currentWindowPosition"
    DAMPER_POSITION = "damperPosition"
    DEACTIVATE_CHARGING = "deactivateCharging"
    DEACTIVATE_FEED_IN = "deactivateFeedIn"
    DEFROST_ON = "defrostOn"
    DEW_POINT_TEMPERATURE_ = "DewPointTemperature"
    DIFFERENTIAL_PRESSURE = "differentialPressure"
    DIFFUSE_SUN_POWER_ = "DiffuseSunPower"
    DIRECT_SUN_POWER_ = "DirectSunPower"
    DIRECT_SUN_POWER_VERTICAL_ = "DirectSunPowerVertical"
    DMI_TEMPERATURE = "dmiTemperature"
    EMITTER_TEMPERATURE = "emitterT"
    ENERGY = "energy"
    ERROR_WINDOW_POSITION = "errorWindowPosition"
    ESS_MODE = "essMode"
    EXHAUST_AIR_FLOW = "exhaustAirFlow"
    EXHAUST_AIR_PRESSURE = "exhaustAirPressure"
    EXHAUST_AIR_SPEED = "exhaustAirSpeed"
    EXHAUST_AIR_TEMPERATURE = "exhaustAirTemperature"
    EXTRACT_AIR_FLOW = "extractAirFlow"
    EXTRACT_AIR_HUMIDITY = "extractAirHumidity"
    EXTRACT_AIR_PRESSURE = "extractAirPressure"
    EXTRACT_AIR_SPEED = "extractAirSpeed"
    EXTRACT_AIR_TEMPERATURE = "extractAirTemperature"
    EXTRACT_CO2 = "extractCO2"
    EXTRACT_FILTER_DIFFERENTIAL_PRESSURE = "extractFilterDifferentialPressure"
    FLOOR_TEMPERATURE = "floorTemperature"
    FLOOR_TEMPERATURE_MAX = "floorTemperatureMax"
    FLOOR_TEMPERATURE_MIN = "floorTemperatureMin"
    FLOW = "flow"
    FLOW_ACCUMULATED_RETURN_TEMPERATURE = "flowAccumulatedReturnT"
    FLOW_ACCUMULATED_SUPPLY_TEMPERATURE = "flowAccumulatedSupplyT"
    FOG_ = "Fog"
    FREQUENCY = "frequency"
    HCA = "hca"
    HEARTBEAT = "heartbeat"
    HEAT_RECOVERY_EXCHANGER_LOADING = "heatRecoveryExchangerLoading"
    HEAT_RECOVERY_RECOVERED_TEMPERATURE = "heatRecoveryRecoveredTemperature"
    HIGH_CLOUDS_ = "HighClouds"
    HOME = "home"
    HOT_GAS = "hotGas"
    HUMIDITY = "humidity"
    HUMIDITY_ = "Humidity"
    HP_ON = "hpOn"
    INLET_DAMPER_POSITION = "inletDamperPosition"
    INLET_FAN_SPEED = "inletFanSpeed"
    INTAKE_AIR_FLOW = "intakeAirFlow"
    INTAKE_AIR_PRESSURE = "intakeAirPressure"
    INTAKE_AIR_SPEED = "intakeAirSpeed"
    INTAKE_AIR_TEMPERATURE = "intakeAirTemperature"
    INTAKE_FILTER_DIFFERENTIAL_PRESSURE = "intakeFilterDifferentialPressure"
    LOADING = "loading"
    LOW_CLOUDS_ = "LowClouds"
    MEDIUM_CLOUDS_ = "MediumClouds"
    MINIMUM_STATE_OF_CHARGE = "minimumStateOfCharge"
    MODE = "mode"
    MOTOR_POSITION = "motorPosition"
    MOTOR_RANGE = "motorRange"
    NOISE_LEVEL_AVG = "noiseLevelAvg"
    NOISE_LEVEL_PEAK = "noiseLevelPeak"
    ORIGINAL_SETPOINT = "originalSetPoint"
    OUTLET_DAMPER_POSITION = "outletDamperPosition"
    OUTLET_FAN_SPEED = "outletFanSpeed"
    OVERRIDE_MODE = "overrideMode"
    OVERRIDE_POSITION = "overridePosition"
    OVERRIDE_STATE = "overrideState"
    PERCENTAGE_CONTROLLER = "percentageController"
    PLUGGED_IN = "plugged_in"
    POSITION = "position"
    POWER = "power"
    PRECIPITATION_ = "Precipitation"
    PRESSURE = "pressure"
    PRESSURE_ = "Pressure"
    PRIMARY_FLOW = "primaryFlow"
    PRIMARY_RETURN_TEMPERATURE = "primaryReturnT"
    PRIMARY_SUPPLY_TEMPERATURE = "primarySupplyT"
    PUMP = "pump"
    PUMP_ON_OFF = "pumpOnOff"
    RADON_LONG_TERM = "radonLongTerm"
    RADON_SHORT_TERM = "radonShortTerm"
    RANGE = "range"
    RADIATOR_TEMPERATURE = "radiatorTempeture"
    RECOVERED_TEMPERATURE = "recoveredTemperature"
    REACTIVE_EXPORT = "reactive_export"
    REACTIVE_IMPORT = "reactive_import"
    REACTIVE_POWER = "reactive_power"
    RELAY_OFF = "relayOff"
    RELAY_ON = "relayOn"
    RETURN_PRESSURE = "returnPressure"
    RETURN_TEMPERATURE = "returnT"
    SECONDARY_CONTROLLED_SIGNAL = "secondaryControlledSignal"
    SENSOR_1 = "sensor1"
    SENSOR_2 = "sensor2"
    SENSOR_3 = "sensor3"
    SENSOR_4 = "sensor4"
    SENSOR_5 = "sensor5"
    SENSOR_6 = "sensor6"
    SENSOR_7 = "sensor7"
    SENSOR_8 = "sensor8"
    SENSOR_9 = "sensor9"
    SENSOR_10 = "sensor10"
    SENSOR_11 = "sensor11"
    SENSOR_12 = "sensor12"
    SENSOR_13 = "sensor13"
    SENSOR_14 = "sensor14"
    SENSOR_15 = "sensor15"
    SENSOR_16 = "sensor16"
    SENSOR_17 = "sensor17"
    SENSOR_18 = "sensor18"
    SENSOR_19 = "sensor19"
    SENSOR_20 = "sensor20"
    SETPOINT = "setPoint"
    SETPOINT_AIR_FLOW = "setPointAirFlow"
    SETPOINT_CO2 = "setPointCO2"
    SETPOINT_EXTRACT_TEMPERATURE = "setPointExtractTemperature"
    SETPOINT_HEAT_RECOVERY_SUPPLY_TEMPERATURE = "setPointHeatRecoverySupplyTemperature"
    SETPOINT_HUMIDITY = "setPointHumidity"
    SETPOINT_OFFSET = "setPointOffset"
    SETPOINT_SUPPLY_TEMPERATURE = "setPointSupplyTemperature"
    SETPOINT_TEMPERATURE = "setPointTemperature"
    SETPOINT_TEMPERATURE_MAX = "setPointTemperatureMax"
    SETPOINT_TEMPERATURE_MIN = "setPointTemperatureMin"
    SG_RELAY_1 = "sgRelay1"
    SG_RELAY_2 = "sgRelay2"
    START_COUNTER = "startCounter"
    STATE = "state"
    STATE_OF_CHARGE = "stateOfCharge"
    SUPPLY_AIR_FLOW = "supplyAirFlow"
    SUPPLY_AIR_PRESSURE = "supplyAirPressure"
    SUPPLY_AIR_SPEED = "supplyAirSpeed"
    SUPPLY_AIR_TEMPERATURE = "supplyAirTemperature"
    SUPPLY_PRESSURE = "supplyPressure"
    SUPPLY_TEMPERATURE = "supplyT"
    SUN_ALTITUDE_ = "SunAltitude"
    SUN_AZIMUTH_ = "SunAzimuth"
    TANK_BOTTOM_TEMPERATURE = "tankBottomT"
    TANK_TEMPERATURE = "tankTemperature"
    TANK_TOP_TEMPERATURE = "tankTopT"
    TEMPERATURE = "temperature"
    TEMPERATURE_ = "Temperature"
    THERMOSTAT_MOTOR_POSITION = "thermostatMotorPosition"
    THERMOSTAT_MOTOR_POSITION_PERCENT = "thermostatMotorPositionPercent"
    THERMOSTAT_MOTOR_RANGE = "thermostatMotorRange"
    VALVE_CURRENT = "valveCurrent"
    VALVE_OPENING = "valveOpening"
    VENTILATION_ON = "ventilationOn"
    VOC = "voc"
    VOLUME = "volume"
    VOLUME_CONSUMPTION = "volumeConsumption"
    WINDOW_OPENING = "windowOpening"
    WIND_DIRECTION = "windDirection"
    WIND_DIRECTION_ = "WindDirection"
    WIND_GUST_ = "WindGust"
    WIND_SPEED = "windSpeed"
    WIND_SPEED_ = "WindSpeed"
    VOLTAGE_CONTROLLER = "voltageController"

    def __repr__(self) -> str:
        return self.name


class UnitType(Enum):
    BATTERY = "batteries"
    CAR = "cars"
    CAR_CHARGER = "carChargers"
    CIRCULATION_PUMP = "circulationPump"
    COLD_WATER = "coldWater"
    CONTROL = "controls"
    COOLING = "cooling"
    COOLING_COIL = "coolingCoils"
    CUSTOM = "custom"
    ELECTRICITY = "electricity"
    FLOOR_HEATING_LOOP = "floorHeatingLoops"
    HCA = "hca"
    HEAT_EXCHANGER = "heatExchangers"
    HEAT_PUMP = "heatPumps"
    HEAT_RECOVERY = "heatRecovery"
    HEATING = "heating"
    HEATING_COIL = "heatingCoils"
    HOT_WATER = "hotWater"
    INDOOR_CLIMATE = "indoorClimate"
    LOCAL_WEATHER_STATION = "localWeatherStations"
    MAIN = "main"
    MOTORIZED_VALVE = "motorizedValve"
    PV = "pvs"
    RADIATOR = "radiators"
    SECONDARY = "secondaries"
    SECONDARY_HEAT_EXCHANGER = "secondaryHeatExchanger"
    SECONDARY_HEAT_EXCHANGER_WITH_TANK = "secondaryHeatExchangerWithTank"
    SECONDARY_TANK = "secondaryTank"
    SUB_HEATING = "subHeating"
    SUB_METER = "subMeters"
    SUB_VENTILATION = "subVentilations"
    THERMOSTAT = "thermostat"
    VENTILATION = "ventilation"
    WEATHER_FORECAST = "weatherForecast"
    WINDOW = "window"

    def __repr__(self) -> str:
        return self.name

    @property
    def components(self) -> list[ComponentType]:
        lookup = {
            UnitType.BATTERY: [
                ComponentType.STATE_OF_CHARGE,
                ComponentType.DEACTIVATE_CHARGING,
                ComponentType.DEACTIVATE_FEED_IN,
                ComponentType.ESS_MODE,
                ComponentType.MINIMUM_STATE_OF_CHARGE,
            ],
            UnitType.CAR: [
                ComponentType.CHARGING,
                ComponentType.HOME,
                ComponentType.PLUGGED_IN,
                ComponentType.RANGE,
                ComponentType.STATE_OF_CHARGE,
                ComponentType.POWER,
            ],
            UnitType.CIRCULATION_PUMP: [
                ComponentType.MODE,
                ComponentType.OVERRIDE_MODE,
                ComponentType.OVERRIDE_STATE,
                ComponentType.STATE,
            ],
            UnitType.COLD_WATER: [
                ComponentType.FLOW,
                ComponentType.SUPPLY_TEMPERATURE,
                ComponentType.VOLUME,
                ComponentType.VOLUME_CONSUMPTION,
            ],
            UnitType.CONTROL: [
                ComponentType.CONTROL_INPUT,
                ComponentType.CONTROL_SWITCH,
                ComponentType.CONTROLLED_SIGNAL,
                ComponentType.HEARTBEAT,
                ComponentType.MOTOR_POSITION,
                ComponentType.ORIGINAL_SETPOINT,
                ComponentType.PERCENTAGE_CONTROLLER,
                ComponentType.PUMP_ON_OFF,
                ComponentType.RELAY_OFF,
                ComponentType.RELAY_ON,
                ComponentType.SECONDARY_CONTROLLED_SIGNAL,
                ComponentType.SETPOINT,
                ComponentType.SETPOINT_OFFSET,
                ComponentType.VOLTAGE_CONTROLLER,
                ComponentType.SG_RELAY_1,
                ComponentType.SG_RELAY_2,
            ],
            UnitType.COOLING: [
                ComponentType.CONSUMPTION,
                ComponentType.ENERGY,
                ComponentType.FLOW_ACCUMULATED_RETURN_TEMPERATURE,
                ComponentType.FLOW_ACCUMULATED_SUPPLY_TEMPERATURE,
                ComponentType.POWER,
                ComponentType.PRIMARY_FLOW,
                ComponentType.PRIMARY_RETURN_TEMPERATURE,
                ComponentType.PRIMARY_SUPPLY_TEMPERATURE,
                ComponentType.VOLUME,
                ComponentType.VOLUME_CONSUMPTION,
            ],
            UnitType.COOLING_COIL: [
                ComponentType.AIR_TEMPERATURE_AFTER,
                ComponentType.AIR_TEMPERATURE_BEFORE,
                ComponentType.CIRCULATION_PUMP,
                ComponentType.RETURN_TEMPERATURE,
                ComponentType.SUPPLY_TEMPERATURE,
                ComponentType.VALVE_OPENING,
            ],
            UnitType.CUSTOM: [
                ComponentType.SENSOR_1,
                ComponentType.SENSOR_2,
                ComponentType.SENSOR_3,
                ComponentType.SENSOR_4,
                ComponentType.SENSOR_5,
                ComponentType.SENSOR_6,
                ComponentType.SENSOR_7,
                ComponentType.SENSOR_8,
                ComponentType.SENSOR_9,
                ComponentType.SENSOR_10,
                ComponentType.SENSOR_11,
                ComponentType.SENSOR_12,
                ComponentType.SENSOR_13,
                ComponentType.SENSOR_14,
                ComponentType.SENSOR_15,
                ComponentType.SENSOR_16,
                ComponentType.SENSOR_17,
                ComponentType.SENSOR_18,
                ComponentType.SENSOR_19,
                ComponentType.SENSOR_20,
            ],
            UnitType.ELECTRICITY: [
                ComponentType.CONSUMPTION,
                ComponentType.ENERGY,
                ComponentType.POWER,
                ComponentType.ACTIVE_EXPORT_CONSUMPTION,
                ComponentType.ACTIVE_EXPORT_COUNTER,
                ComponentType.REACTIVE_IMPORT,
                ComponentType.REACTIVE_EXPORT,
                ComponentType.APPARENT_ENERGY,
                ComponentType.APPARENT_POWER,
                ComponentType.REACTIVE_POWER,
                ComponentType.FREQUENCY,
                ComponentType.CURRENT,
            ],
            UnitType.FLOOR_HEATING_LOOP: [
                ComponentType.CIRCULATION_PUMP,
                ComponentType.RETURN_TEMPERATURE,
                ComponentType.SUPPLY_TEMPERATURE,
                ComponentType.VALVE_CURRENT,
                ComponentType.VALVE_OPENING,
            ],
            UnitType.HCA: [
                ComponentType.AMBIENT_TEMPERATURE,
                ComponentType.BATTERY_PERCENTAGE,
                ComponentType.HCA,
                ComponentType.RADIATOR_TEMPERATURE,
            ],
            UnitType.HEAT_EXCHANGER: [
                ComponentType.CONSUMPTION,
                ComponentType.ENERGY,
                ComponentType.FLOW,
                ComponentType.FLOW_ACCUMULATED_RETURN_TEMPERATURE,
                ComponentType.FLOW_ACCUMULATED_SUPPLY_TEMPERATURE,
                ComponentType.POWER,
                ComponentType.RETURN_TEMPERATURE,
                ComponentType.SUPPLY_TEMPERATURE,
                ComponentType.VOLUME,
                ComponentType.VOLUME_CONSUMPTION,
            ],
            UnitType.HEAT_PUMP: [
                ComponentType.BACKUP_ON,
                ComponentType.DEFROST_ON,
                ComponentType.HOT_GAS,
                ComponentType.HP_ON,
                ComponentType.START_COUNTER,
                ComponentType.TANK_TEMPERATURE,
            ],
            UnitType.HEAT_RECOVERY: [
                ComponentType.DAMPER_POSITION,
                ComponentType.LOADING,
                ComponentType.RECOVERED_TEMPERATURE,
            ],
            UnitType.HEATING: [
                ComponentType.CONSUMPTION,
                ComponentType.ENERGY,
                ComponentType.FLOW_ACCUMULATED_RETURN_TEMPERATURE,
                ComponentType.FLOW_ACCUMULATED_SUPPLY_TEMPERATURE,
                ComponentType.POWER,
                ComponentType.PRIMARY_FLOW,
                ComponentType.PRIMARY_RETURN_TEMPERATURE,
                ComponentType.PRIMARY_SUPPLY_TEMPERATURE,
                ComponentType.VOLUME,
                ComponentType.VOLUME_CONSUMPTION,
            ],
            UnitType.HEATING_COIL: [
                ComponentType.AIR_TEMPERATURE_AFTER,
                ComponentType.AIR_TEMPERATURE_BEFORE,
                ComponentType.CIRCULATION_PUMP,
                ComponentType.RETURN_TEMPERATURE,
                ComponentType.SUPPLY_TEMPERATURE,
                ComponentType.VALVE_OPENING,
            ],
            UnitType.HOT_WATER: [
                ComponentType.CONSUMPTION,
                ComponentType.ENERGY,
                ComponentType.FLOW_ACCUMULATED_RETURN_TEMPERATURE,
                ComponentType.FLOW_ACCUMULATED_SUPPLY_TEMPERATURE,
                ComponentType.POWER,
                ComponentType.PRIMARY_FLOW,
                ComponentType.PRIMARY_RETURN_TEMPERATURE,
                ComponentType.PRIMARY_SUPPLY_TEMPERATURE,
                ComponentType.VOLUME,
                ComponentType.VOLUME_CONSUMPTION,
            ],
            UnitType.INDOOR_CLIMATE: [
                ComponentType.BATTERY_VOLTAGE,
                ComponentType.CO2,
                ComponentType.FLOOR_TEMPERATURE,
                ComponentType.FLOOR_TEMPERATURE_MAX,
                ComponentType.FLOOR_TEMPERATURE_MIN,
                ComponentType.HUMIDITY,
                ComponentType.NOISE_LEVEL_AVG,
                ComponentType.NOISE_LEVEL_PEAK,
                ComponentType.RADON_LONG_TERM,
                ComponentType.RADON_SHORT_TERM,
                ComponentType.SETPOINT_TEMPERATURE,
                ComponentType.SETPOINT_TEMPERATURE_MAX,
                ComponentType.SETPOINT_TEMPERATURE_MIN,
                ComponentType.TEMPERATURE,
                ComponentType.THERMOSTAT_MOTOR_POSITION,
                ComponentType.THERMOSTAT_MOTOR_RANGE,
                ComponentType.VOC,
                ComponentType.WINDOW_OPENING,
            ],
            UnitType.LOCAL_WEATHER_STATION: [
                ComponentType.AMBIENT_TEMPERATURE,
                ComponentType.WIND_DIRECTION,
                ComponentType.WIND_SPEED,
            ],
            UnitType.MAIN: [
                ComponentType.CONSUMPTION,
                ComponentType.ENERGY,
                ComponentType.FLOW,
                ComponentType.FLOW_ACCUMULATED_RETURN_TEMPERATURE,
                ComponentType.FLOW_ACCUMULATED_SUPPLY_TEMPERATURE,
                ComponentType.POWER,
                ComponentType.RETURN_TEMPERATURE,
                ComponentType.SUPPLY_TEMPERATURE,
                ComponentType.VOLUME,
                ComponentType.VOLUME_CONSUMPTION,
            ],
            UnitType.MOTORIZED_VALVE: [
                ComponentType.MODE,
                ComponentType.OVERRIDE_MODE,
                ComponentType.OVERRIDE_POSITION,
                ComponentType.POSITION,
            ],
            UnitType.RADIATOR: [
                ComponentType.EMITTER_TEMPERATURE,
                ComponentType.RETURN_TEMPERATURE,
                ComponentType.SUPPLY_TEMPERATURE,
            ],
            UnitType.SECONDARY: [
                ComponentType.CONSUMPTION,
                ComponentType.DIFFERENTIAL_PRESSURE,
                ComponentType.ENERGY,
                ComponentType.FLOW,
                ComponentType.FLOW_ACCUMULATED_RETURN_TEMPERATURE,
                ComponentType.FLOW_ACCUMULATED_SUPPLY_TEMPERATURE,
                ComponentType.POWER,
                ComponentType.PRESSURE,
                ComponentType.PUMP,
                ComponentType.RETURN_PRESSURE,
                ComponentType.RETURN_TEMPERATURE,
                ComponentType.SUPPLY_PRESSURE,
                ComponentType.SUPPLY_TEMPERATURE,
                ComponentType.VOLUME,
                ComponentType.VOLUME_CONSUMPTION,
            ],
            UnitType.SECONDARY_HEAT_EXCHANGER: [
                ComponentType.RETURN_TEMPERATURE,
                ComponentType.SUPPLY_TEMPERATURE,
            ],
            UnitType.SECONDARY_HEAT_EXCHANGER_WITH_TANK: [
                ComponentType.CHARGE_TEMPERATURE,
                ComponentType.RETURN_TEMPERATURE,
                ComponentType.SUPPLY_TEMPERATURE,
                ComponentType.TANK_BOTTOM_TEMPERATURE,
                ComponentType.TANK_TOP_TEMPERATURE,
                ComponentType.CIRCULATION_PUMP,
                ComponentType.CHARGE_PUMP,
                ComponentType.CIRCULATION_TEMPERATURE,
            ],
            UnitType.SECONDARY_TANK: [
                ComponentType.CHARGE_TEMPERATURE,
                ComponentType.RETURN_TEMPERATURE,
                ComponentType.SUPPLY_TEMPERATURE,
                ComponentType.TANK_BOTTOM_TEMPERATURE,
                ComponentType.TANK_TOP_TEMPERATURE,
            ],
            UnitType.SUB_HEATING: [
                ComponentType.CONSUMPTION,
                ComponentType.ENERGY,
                ComponentType.FLOW_ACCUMULATED_RETURN_TEMPERATURE,
                ComponentType.FLOW_ACCUMULATED_SUPPLY_TEMPERATURE,
                ComponentType.POWER,
                ComponentType.PRIMARY_FLOW,
                ComponentType.PRIMARY_RETURN_TEMPERATURE,
                ComponentType.PRIMARY_SUPPLY_TEMPERATURE,
                ComponentType.VOLUME,
                ComponentType.VOLUME_CONSUMPTION,
            ],
            UnitType.SUB_METER: [
                ComponentType.CONSUMPTION,
                ComponentType.ENERGY,
                ComponentType.FLOW,
                ComponentType.FLOW_ACCUMULATED_RETURN_TEMPERATURE,
                ComponentType.FLOW_ACCUMULATED_SUPPLY_TEMPERATURE,
                ComponentType.POWER,
                ComponentType.RETURN_TEMPERATURE,
                ComponentType.SUPPLY_TEMPERATURE,
                ComponentType.VOLUME,
                ComponentType.VOLUME_CONSUMPTION,
                ComponentType.ACTIVE_EXPORT_CONSUMPTION,
                ComponentType.ACTIVE_EXPORT_COUNTER,
                ComponentType.REACTIVE_IMPORT,
                ComponentType.REACTIVE_EXPORT,
                ComponentType.APPARENT_ENERGY,
                ComponentType.APPARENT_POWER,
                ComponentType.REACTIVE_POWER,
                ComponentType.FREQUENCY,
                ComponentType.CURRENT,
            ],
            UnitType.SUB_VENTILATION: [
                ComponentType.EXHAUST_AIR_FLOW,
                ComponentType.EXHAUST_AIR_PRESSURE,
                ComponentType.EXHAUST_AIR_SPEED,
                ComponentType.EXHAUST_AIR_TEMPERATURE,
                ComponentType.EXTRACT_AIR_FLOW,
                ComponentType.EXTRACT_AIR_HUMIDITY,
                ComponentType.EXTRACT_AIR_PRESSURE,
                ComponentType.EXTRACT_AIR_SPEED,
                ComponentType.EXTRACT_AIR_TEMPERATURE,
                ComponentType.EXTRACT_CO2,
                ComponentType.EXTRACT_FILTER_DIFFERENTIAL_PRESSURE,
                ComponentType.HEAT_RECOVERY_EXCHANGER_LOADING,
                ComponentType.HEAT_RECOVERY_RECOVERED_TEMPERATURE,
                ComponentType.INLET_DAMPER_POSITION,
                ComponentType.INLET_FAN_SPEED,
                ComponentType.INTAKE_AIR_FLOW,
                ComponentType.INTAKE_AIR_PRESSURE,
                ComponentType.INTAKE_AIR_SPEED,
                ComponentType.INTAKE_AIR_TEMPERATURE,
                ComponentType.INTAKE_FILTER_DIFFERENTIAL_PRESSURE,
                ComponentType.OUTLET_DAMPER_POSITION,
                ComponentType.OUTLET_FAN_SPEED,
                ComponentType.SETPOINT_AIR_FLOW,
                ComponentType.SETPOINT_CO2,
                ComponentType.SETPOINT_EXTRACT_TEMPERATURE,
                ComponentType.SETPOINT_HEAT_RECOVERY_SUPPLY_TEMPERATURE,
                ComponentType.SETPOINT_HUMIDITY,
                ComponentType.SETPOINT_SUPPLY_TEMPERATURE,
                ComponentType.SUPPLY_AIR_FLOW,
                ComponentType.SUPPLY_AIR_PRESSURE,
                ComponentType.SUPPLY_AIR_SPEED,
                ComponentType.SUPPLY_AIR_TEMPERATURE,
                ComponentType.VENTILATION_ON,
            ],
            UnitType.THERMOSTAT: [
                ComponentType.TEMPERATURE,
                ComponentType.MOTOR_POSITION,
                ComponentType.MOTOR_RANGE,
                ComponentType.THERMOSTAT_MOTOR_POSITION_PERCENT,
                ComponentType.SETPOINT,
                ComponentType.BATTERY_VOLTAGE,
            ],
            UnitType.VENTILATION: [
                ComponentType.EXHAUST_AIR_FLOW,
                ComponentType.EXHAUST_AIR_PRESSURE,
                ComponentType.EXHAUST_AIR_SPEED,
                ComponentType.EXHAUST_AIR_TEMPERATURE,
                ComponentType.EXTRACT_AIR_FLOW,
                ComponentType.EXTRACT_AIR_HUMIDITY,
                ComponentType.EXTRACT_AIR_PRESSURE,
                ComponentType.EXTRACT_AIR_SPEED,
                ComponentType.EXTRACT_AIR_TEMPERATURE,
                ComponentType.EXTRACT_CO2,
                ComponentType.EXTRACT_FILTER_DIFFERENTIAL_PRESSURE,
                ComponentType.HEAT_RECOVERY_EXCHANGER_LOADING,
                ComponentType.HEAT_RECOVERY_RECOVERED_TEMPERATURE,
                ComponentType.INLET_DAMPER_POSITION,
                ComponentType.INLET_FAN_SPEED,
                ComponentType.INTAKE_AIR_FLOW,
                ComponentType.INTAKE_AIR_PRESSURE,
                ComponentType.INTAKE_AIR_SPEED,
                ComponentType.INTAKE_AIR_TEMPERATURE,
                ComponentType.INTAKE_FILTER_DIFFERENTIAL_PRESSURE,
                ComponentType.OUTLET_DAMPER_POSITION,
                ComponentType.OUTLET_FAN_SPEED,
                ComponentType.SETPOINT_AIR_FLOW,
                ComponentType.SETPOINT_CO2,
                ComponentType.SETPOINT_EXTRACT_TEMPERATURE,
                ComponentType.SETPOINT_HEAT_RECOVERY_SUPPLY_TEMPERATURE,
                ComponentType.SETPOINT_HUMIDITY,
                ComponentType.SETPOINT_SUPPLY_TEMPERATURE,
                ComponentType.SUPPLY_AIR_FLOW,
                ComponentType.SUPPLY_AIR_PRESSURE,
                ComponentType.SUPPLY_AIR_SPEED,
                ComponentType.SUPPLY_AIR_TEMPERATURE,
                ComponentType.VENTILATION_ON,
            ],
            UnitType.WEATHER_FORECAST: [
                ComponentType.TEMPERATURE_,
                ComponentType.HUMIDITY_,
                ComponentType.WIND_DIRECTION_,
                ComponentType.WIND_SPEED_,
                ComponentType.PRESSURE_,
                ComponentType.LOW_CLOUDS_,
                ComponentType.MEDIUM_CLOUDS_,
                ComponentType.HIGH_CLOUDS_,
                ComponentType.FOG_,
                ComponentType.WIND_GUST_,
                ComponentType.DEW_POINT_TEMPERATURE_,
                ComponentType.CLOUDINESS_,
                ComponentType.PRECIPITATION_,
                ComponentType.DIRECT_SUN_POWER_,
                ComponentType.DIFFUSE_SUN_POWER_,
                ComponentType.SUN_ALTITUDE_,
                ComponentType.SUN_AZIMUTH_,
                ComponentType.DIRECT_SUN_POWER_VERTICAL_,
            ],
            UnitType.WINDOW: [
                ComponentType.CURRENT_WINDOW_POSITION,
                ComponentType.ERROR_WINDOW_POSITION,
            ],
        }
        return lookup[self] if self in lookup else []

    @property
    def children(self) -> list[UnitType]:
        lookup = {
            UnitType.BATTERY: [UnitType.CONTROL],
            UnitType.CAR: [UnitType.CONTROL],
            UnitType.COLD_WATER: [UnitType.SUB_METER],
            UnitType.COOLING: [UnitType.COOLING_COIL, UnitType.SECONDARY],
            UnitType.COOLING_COIL: [UnitType.CONTROL],
            UnitType.CUSTOM: [UnitType.CONTROL],
            UnitType.ELECTRICITY: [UnitType.SUB_METER],
            UnitType.FLOOR_HEATING_LOOP: [UnitType.CONTROL],
            UnitType.HEAT_EXCHANGER: [UnitType.CONTROL],
            UnitType.HEAT_PUMP: [UnitType.CONTROL],
            UnitType.HEAT_RECOVERY: [UnitType.CONTROL],
            UnitType.HEATING: [
                UnitType.FLOOR_HEATING_LOOP,
                UnitType.HEATING_COIL,
                UnitType.SECONDARY,
                UnitType.SUB_HEATING,
            ],
            UnitType.HEATING_COIL: [UnitType.CONTROL],
            UnitType.HOT_WATER: [
                UnitType.SECONDARY_HEAT_EXCHANGER,
                UnitType.SECONDARY_HEAT_EXCHANGER_WITH_TANK,
                UnitType.SECONDARY_TANK,
            ],
            UnitType.LOCAL_WEATHER_STATION: [UnitType.CONTROL],
            UnitType.MAIN: [UnitType.HEAT_EXCHANGER],
            UnitType.RADIATOR: [UnitType.CONTROL, UnitType.HCA, UnitType.THERMOSTAT],
            UnitType.SECONDARY: [
                UnitType.CONTROL,
                UnitType.FLOOR_HEATING_LOOP,
                UnitType.HEATING_COIL,
                UnitType.RADIATOR,
                UnitType.SECONDARY,
                UnitType.SUB_METER,
                UnitType.COOLING_COIL,
                UnitType.MOTORIZED_VALVE,
                UnitType.CIRCULATION_PUMP,
            ],
            UnitType.SECONDARY_HEAT_EXCHANGER: [
                UnitType.CONTROL,
                UnitType.SUB_METER,
                UnitType.MOTORIZED_VALVE,
                UnitType.CIRCULATION_PUMP,
            ],
            UnitType.SECONDARY_HEAT_EXCHANGER_WITH_TANK: [
                UnitType.CONTROL,
                UnitType.SUB_METER,
            ],
            UnitType.SECONDARY_TANK: [UnitType.CONTROL, UnitType.SUB_METER],
            UnitType.SUB_HEATING: [
                UnitType.FLOOR_HEATING_LOOP,
                UnitType.SECONDARY,
                UnitType.HEATING_COIL,
                UnitType.SUB_HEATING,
            ],
            UnitType.SUB_METER: [UnitType.SUB_METER],
            UnitType.SUB_VENTILATION: [UnitType.CONTROL, UnitType.HEAT_RECOVERY],
            UnitType.THERMOSTAT: [UnitType.CONTROL],
            UnitType.VENTILATION: [
                UnitType.CONTROL,
                UnitType.HEAT_RECOVERY,
                UnitType.SUB_VENTILATION,
            ],
        }
        return lookup[self] if self in lookup else []

    @property
    def descriptors(self) -> list[UnitDescriptorType]:
        lookup = {
            UnitType.CAR: [
                UnitDescriptorType.BATTERY_CAPACITY,
            ],
            UnitType.BATTERY: [
                UnitDescriptorType.MAX_CHARGE_POWER,
                UnitDescriptorType.MAX_DISCHARGE_POWER,
                UnitDescriptorType.MIN_STATE_OF_CHARGE,
                UnitDescriptorType.MAX_STATE_OF_CHARGE,
                UnitDescriptorType.NETTO_CAPACITY,
            ],
            UnitType.COLD_WATER: [
                UnitDescriptorType.BUILDINGS_COVERED,
                UnitDescriptorType.PLACEMENT,
            ],
            UnitType.CONTROL: [UnitDescriptorType.ACTIVE],
            UnitType.COOLING: [UnitDescriptorType.BUILDINGS_COVERED],
            UnitType.COOLING_COIL: [
                UnitDescriptorType.PLACED_BEFORE_HEAT_RECOVERY,
                UnitDescriptorType.PLACEMENT_NUMBER,
            ],
            UnitType.ELECTRICITY: [
                UnitDescriptorType.BUILDINGS_COVERED,
                UnitDescriptorType.METER_TYPE,
                UnitDescriptorType.CONFIGURATION,
            ],
            UnitType.HEAT_PUMP: [
                UnitDescriptorType.BRAND,
                UnitDescriptorType.HEAT_CURVE_OFFSET,
                UnitDescriptorType.HEAT_PUMP_CAPACITY,
                UnitDescriptorType.PRODUCES,
            ],
            UnitType.HEATING: [UnitDescriptorType.BUILDINGS_COVERED],
            UnitType.HEATING_COIL: [
                UnitDescriptorType.PLACED_BEFORE_HEAT_RECOVERY,
                UnitDescriptorType.PLACEMENT_NUMBER,
            ],
            UnitType.HOT_WATER: [UnitDescriptorType.BUILDINGS_COVERED],
            UnitType.MAIN: [UnitDescriptorType.BUILDINGS_COVERED],
            UnitType.PV: [
                UnitDescriptorType.COMPASS_HEADING,
                UnitDescriptorType.MAX_CONVERTER_PEAK_POWER,
                UnitDescriptorType.PANEL_ANGLE,
                UnitDescriptorType.PANEL_PEAK_POWER,
            ],
            UnitType.SUB_HEATING: [
                UnitDescriptorType.BUILDINGS_COVERED,
            ],
            UnitType.SUB_METER: [
                UnitDescriptorType.METER_TYPE,
                UnitDescriptorType.CONFIGURATION,
                UnitDescriptorType.PLACEMENT,
            ],
        }
        return lookup[self] if self in lookup else []

    @property
    def related_units(self) -> list[RelatedUnitType]:
        lookup = {
            UnitType.BATTERY: [RelatedUnitType.ELECTRICITY],
            UnitType.CAR_CHARGER: [RelatedUnitType.ELECTRICITY],
            UnitType.HEAT_PUMP: [
                RelatedUnitType.ELECTRICITY,
                RelatedUnitType.HEATING,
                RelatedUnitType.COOLING,
                RelatedUnitType.HOT_WATER,
                RelatedUnitType.MAIN,
            ],
            UnitType.PV: [RelatedUnitType.ELECTRICITY],
            UnitType.SECONDARY_HEAT_EXCHANGER: [RelatedUnitType.COLD_WATER],
            UnitType.SECONDARY_HEAT_EXCHANGER_WITH_TANK: [RelatedUnitType.COLD_WATER],
            UnitType.SECONDARY_TANK: [RelatedUnitType.COLD_WATER],
            UnitType.SUB_VENTILATION: [
                RelatedUnitType.COOLING_COIL,
                RelatedUnitType.ELECTRICITY,
                RelatedUnitType.HEATING_COIL,
                RelatedUnitType.HEATING_SECONDARY,
                RelatedUnitType.COOLING_SECONDARY,
            ],
            UnitType.VENTILATION: [
                RelatedUnitType.COOLING_COIL,
                RelatedUnitType.ELECTRICITY,
                RelatedUnitType.HEATING_COIL,
                RelatedUnitType.HEATING_SECONDARY,
                RelatedUnitType.COOLING_SECONDARY,
            ],
        }
        return lookup[self] if self in lookup else []

    @property
    def is_top_level(self) -> bool:
        return self in [
            UnitType.CAR,
            UnitType.CAR_CHARGER,
            UnitType.COLD_WATER,
            UnitType.COOLING,
            UnitType.CUSTOM,
            UnitType.ELECTRICITY,
            UnitType.HEAT_PUMP,
            UnitType.HEATING,
            UnitType.HOT_WATER,
            UnitType.INDOOR_CLIMATE,
            UnitType.LOCAL_WEATHER_STATION,
            UnitType.MAIN,
            UnitType.PV,
            UnitType.VENTILATION,
            UnitType.WINDOW,
            UnitType.BATTERY,
        ]


class UnitSubType(Enum):
    BOTH = "BOTH"
    CONSUMPTION = "CONSUMPTION"
    CONTROL_COOLING = "CONTROL_COOLING"
    CONTROL_HEAT = "CONTROL_HEAT"
    CONTROL_HEAT_PUMP_BLOCKING = "CONTROL_HEAT_PUMP_BLOCKING"
    CONTROL_HEAT_PUMP_BLOCKING_OFFSET = "CONTROL_HEAT_PUMP_BLOCKING_OFFSET"
    CONTROL_HEAT_PUMP_BLOCKING_WITH_MAPPING = "CONTROL_HEAT_PUMP_BLOCKING_WITH_MAPPING"
    CONTROL_HEAT_PUMP_BLOCKING_WITH_SLIDER_MAPPING = (
        "CONTROL_HEAT_PUMP_BLOCKING_WITH_SLIDER_MAPPING"
    )
    CONTROL_HEAT_PUMP_HEAT_CURVE_OFFSET = "CONTROL_HEAT_PUMP_HEAT_CURVE_OFFSET"
    CONTROL_HEAT_PUMP_ON_OFF = "CONTROL_HEAT_PUMP_ON_OFF"
    CONTROL_OTHER_EXTERNAL = "CONTROL_OTHER_EXTERNAL"
    CONTROL_OUTDOOR_TEMPERATURE = "CONTROL_OUTDOOR_TEMPERATURE"
    CONTROL_RETURN_LIMITER = "CONTROL_RETURN_LIMITER"
    CONTROL_SG_READY = "CONTROL_SG_READY"
    CONTROL_TANK_TEMPERATURE_MAX = "CONTROL_TANK_TEMPERATURE_MAX"
    CONTROL_TANK_TEMPERATURE_MIN = "CONTROL_TANK_TEMPERATURE_MIN"
    CONTROL_WATER_CIRCULATION = "CONTROL_WATER_CIRCULATION"
    CONTROL_WATER_TANK = "CONTROL_WATER_TANK"
    CONTROL_ZONE = "CONTROL_ZONE"
    COUNTER_FLOW_HEAT_EXCHANGER = "COUNTER_FLOW_HEAT_EXCHANGER"
    DIRECT = "DIRECT"
    HEAT_EXCHANGER = "HEAT_EXCHANGER"
    HEAT_EXCHANGER_WITH_TANK = "HEAT_EXCHANGER_WITH_TANK"
    HOT_WATER_TANK = "HOT_WATER_TANK"
    MIXING_LOOP = "MIXING_LOOP"
    PRODUCTION = "PRODUCTION"
    ROTARY_WHEEL_HEAT_EXCHANGER = "ROTARY_WHEEL_HEAT_EXCHANGER"


@dataclass(eq=False)
class UnitQuery(Query):
    id: list[int] = field(default_factory=list)
    name: list[str] = field(default_factory=list)
    shared: list[bool] = field(default_factory=lambda: [False, None])
    type: list[UnitType] = field(default_factory=list)
    _type_type: ClassVar[type] = UnitType
    subtype: list[UnitSubType] = field(default_factory=list)
    _subtype_type: ClassVar[type] = UnitSubType
    parent: list[UnitQuery] = field(default_factory=list)
    _type_parent: ClassVar[type] = "self"
    exclude: list[UnitQuery] = field(default_factory=list)
    _type_exclude: ClassVar[type] = "self"
    _class: ClassVar[type] = Unit


@dataclass(eq=False)
class ComponentQuery(Query):
    cid: list[int] = field(default_factory=list)
    id: list[int] = field(default_factory=list)
    name: list[str] = field(default_factory=list)
    unit: list[str] = field(default_factory=list)
    type: list[ComponentType] = field(default_factory=list)
    _type_type: ClassVar[type] = ComponentType
    parent: list[UnitQuery] = field(default_factory=list)
    _type_parent: ClassVar[type] = UnitQuery
    exclude: list[ComponentQuery] = field(default_factory=list)
    _type_exclude: ClassVar[type] = "self"
    _class: ClassVar[type] = Component


@dataclass(eq=False)
class DeviceQuery(Query):
    id: list[int] = field(default_factory=list)
    name: list[str] = field(default_factory=list)
    type: list[str] = field(default_factory=list)
    _class: ClassVar[type] = Device


@dataclass(eq=False)
class ZoneQuery(Query):
    id: list[int] = field(default_factory=list)
    name: list[str] = field(default_factory=list)
    type: list[str] = field(default_factory=list)
    external_identifier: list[str] = field(default_factory=list)
    _class: ClassVar[type] = Zone


class BuildingType(Enum):
    """
    Enum class for building types, effectively decoupling from database values
    """

    # For each of these elements, the value must be one of the ones found by querying:
    #       SELECT DISTINCT(building_type) FROM building_characteristics
    APARTMENT_BUILDING = "APARTMENT_BUILDING"
    MULTI_FAMILY_HOUSE = "TERRACED_HOUSE"
    OFFICE_BUILDING = "OFFICE_BUILDING"
    OTHER = "OTHER"
    SCHOOL = "SCHOOL"
    SHOPPING_CENTER = "SHOPPING_CENTER"
    SINGLE_FAMILY_HOUSE = "SINGLE_FAMILY_HOME"
    TEST = "TEST"
