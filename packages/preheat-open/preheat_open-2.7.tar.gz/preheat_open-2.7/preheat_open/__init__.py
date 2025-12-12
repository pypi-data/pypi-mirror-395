"""
The preheat_open package provides methods to load building data from `Neogrids <https://www.neogrid.dk/>`_ platform
"""

# Imports for backwards compatibility of dependent code

import os
import re
import sys

from . import _version
from .collection import Collection
from .interfaces import Adapter, BuildingModel
from .loadable_types import (
    ComfortProfile,
    ComfortProfiles,
    ElectricityPriceItem,
    ElectricityPrices,
    LoadableData,
    OperationType,
    ScheduleItem,
    Setpoint,
    SetpointSchedule,
)
from .location import Location, LocationCharacteristics, LocationInformation
from .measurements import AttrMap, Mapper, MeasurementRequest, PostProcess, StrMap
from .query import unique
from .supplypoint import AppliedPriceComponent, PriceData, SupplyPoint
from .time import DateRange, TimeResolution
from .unit import Component, Device, Unit, UnitDescriptors
from .zone import Zone

__version__ = _version.get_versions()["version"]
