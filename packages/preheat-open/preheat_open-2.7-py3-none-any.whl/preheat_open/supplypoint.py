"""
supplypoint.py

This module defines classes and enums related to supply points, price components, and their associated data.

Classes:
    Authority
    PriceArea
    PriceComponentType
    PriceComponent
    FixedPriceData
    FixedPricePeriod
    PriceData
    AppliedPriceComponent
    SupplyPoint

Enums:
    ApplicationContext
    ApplicationType
    BillingContext
    FormatType
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING

import pandas as pd

from .time import DateRange, datetime, tzinfo

if TYPE_CHECKING:
    from .location import Location
    from .unit import Unit


class ApplicationContext(Enum):
    """
    Enum representing the context in which an application is used.

    Attributes:
        BILLING: Billing context.
        APPLICATION: Environmental impact context.
        OTHER: Other context.
    """

    BILLING = "BILLING"
    APPLICATION = "ENVIRONMENTAL_IMPACT"
    OTHER = "OTHER"

    def __repr__(self) -> str:
        """
        Returns a string representation of the ApplicationContext enum.

        :return: The name of the enum member.
        :rtype: str
        """
        return self.name


class ApplicationType(Enum):
    """
    Enum representing the type of application.

    Attributes:
        PRICE_PER_UNIT: Price per unit application type.
        FLAT_FEE: Flat fee application type.
    """

    PRICE_PER_UNIT = "PRICE_PER_UNIT"
    FLAT_FEE = "FLAT_FEE"

    def __repr__(self) -> str:
        """
        Returns a string representation of the ApplicationType enum.

        :return: The name of the enum member.
        :rtype: str
        """
        return self.name


class BillingContext(Enum):
    """
    Enum representing the billing context.

    Attributes:
        NONE: No billing context.
        ADD_TO_BILL: Add to bill context.
        SUBTRACT_FROM_BILL: Subtract from bill context.
    """

    NONE = "NONE"
    ADD_TO_BILL = "ADD_TO_BILL"
    SUBTRACT_FROM_BILL = "SUBTRACT_FROM_BILL"

    def __repr__(self) -> str:
        """
        Returns a string representation of the BillingContext enum.

        :return: The name of the enum member.
        :rtype: str
        """
        return self.name


class FormatType(Enum):
    """
    Enum representing the format type of a price component.

    Attributes:
        FIXED_PRICE: Fixed price format type.
        TIMESERIES: Timeseries format type.
    """

    FIXED_PRICE = "FIXED_PRICE"
    TIMESERIES = "TIMESERIES"

    def __repr__(self) -> str:
        """
        Returns a string representation of the FormatType enum.

        :return: The name of the enum member.
        :rtype: str
        """
        return self.name


@dataclass
class Authority:
    """
    Represents an authority entity.

    :ivar id: The unique identifier of the authority.
    :vartype id: int
    :ivar name: The name of the authority.
    :vartype name: str
    """

    id: int = None
    name: str = ""


@dataclass
class PriceArea:
    """
    Represents a price area.

    :ivar id: The unique identifier of the price area.
    :vartype id: int
    :ivar name: The name of the price area.
    :vartype name: str
    :ivar supply_type: The type of supply in the price area.
    :vartype supply_type: str
    """

    id: int = None
    name: str = ""
    supply_type: str = ""


@dataclass
class PriceComponentType:
    """
    Represents a type of price component.

    :ivar id: The unique identifier of the price component type.
    :vartype id: int
    :ivar name: The name of the price component type.
    :vartype name: str
    """

    id: int = None
    name: str = ""


@dataclass
class PriceComponent:
    """
    Represents a price component.

    :ivar id: The unique identifier of the price component.
    :vartype id: int
    :ivar name: The name of the price component.
    :vartype name: str
    :ivar description: The description of the price component.
    :vartype description: str
    :ivar created: The creation datetime of the price component.
    :vartype created: datetime
    :ivar type: The type of the price component.
    :vartype type: PriceComponentType
    :ivar unit: The unit of the price component.
    :vartype unit: str
    :ivar format_type: The format type of the price component.
    :vartype format_type: FormatType
    :ivar application_type: The application type of the price component.
    :vartype application_type: ApplicationType
    :ivar unit_component_type: The unit component type of the price component.
    :vartype unit_component_type: Enum
    :ivar timezone: The timezone of the price component.
    :vartype timezone: tzinfo
    :ivar price_area: The price area of the price component.
    :vartype price_area: PriceArea
    :ivar authority: The authority of the price component.
    :vartype authority: Authority
    """

    id: int = None
    name: str = ""
    description: str = ""
    created: datetime = None
    type: PriceComponentType = None
    unit: str = ""
    format_type: FormatType = None
    application_type: ApplicationType = None
    unit_component_type: Enum = None
    timezone: tzinfo = None
    price_area: PriceArea = None
    authority: Authority = None


@dataclass
class FixedPriceData:
    """
    Represents fixed price data.

    :ivar position: The position of the fixed price data.
    :vartype position: int
    :ivar price: The price value.
    :vartype price: float
    """

    position: int = None
    price: float = None


@dataclass
class FixedPricePeriod:
    """
    Represents a period of fixed price data.

    :ivar data: A list of fixed price data.
    :vartype data: list[FixedPriceData]
    :ivar date_range: The date range of the fixed price period.
    :vartype date_range: DateRange
    :ivar resolution: The resolution of the fixed price period.
    :vartype resolution: str
    """

    data: list[FixedPriceData] = field(default_factory=list)
    date_range: DateRange = field(default_factory=DateRange)
    resolution: str = ""


@dataclass
class PriceData:
    """
    Represents price data, including fixed price data and time series data.

    :ivar fixed_price_data: A list of fixed price periods.
    :vartype fixed_price_data: list[FixedPricePeriod]
    :ivar time_series_data: The time series data.
    :vartype time_series_data: pd.Series
    """

    fixed_price_data: list[FixedPricePeriod] = field(default_factory=list)
    time_series_data: pd.Series = None


@dataclass
class AppliedPriceComponent:
    """
    Represents an applied price component.

    :ivar id: The unique identifier of the applied price component.
    :vartype id: int
    :ivar supplypoint_id: The ID of the associated supply point.
    :vartype supplypoint_id: int
    :ivar price_component: The price component.
    :vartype price_component: PriceComponent
    :ivar contract_id: The ID of the associated contract.
    :vartype contract_id: int
    :ivar created: The creation datetime of the applied price component.
    :vartype created: datetime
    :ivar valid_range: The valid date range of the applied price component.
    :vartype valid_range: DateRange
    :ivar billing_context: The billing context.
    :vartype billing_context: str
    :ivar application_context: The application context.
    :vartype application_context: str
    :ivar price_data: The price data.
    :vartype price_data: PriceData
    """

    id: int = None
    supplypoint_id: int = None
    price_component: PriceComponent = field(default_factory=PriceComponent)
    contract_id: int = None
    created: datetime = None
    valid_range: DateRange = field(default_factory=DateRange)
    billing_context: str = ""
    application_context: str = ""
    price_data: PriceData = None


@dataclass
class SupplyPoint:
    """
    Represents a supply point.

    :ivar id: The unique identifier of the supply point.
    :vartype id: int
    :ivar name: The name of the supply point.
    :vartype name: str
    :ivar sub_type: The subtype of the supply point.
    :vartype sub_type: str
    :ivar type: The type of the supply point.
    :vartype type: str
    :ivar units: A list of units associated with the supply point.
    :vartype units: list[Unit]
    :ivar adapter: The adapter for the supply point.
    :vartype adapter: Adapter
    :ivar __price_components: A list of applied price components.
    :vartype __price_components: list[AppliedPriceComponent]
    :ivar __price_components_loaded: Indicates if the price components have been loaded.
    :vartype __price_components_loaded: bool
    """

    id: int = None
    name: str = ""
    sub_type: str = ""
    type: str = ""
    units: list["Unit"] = field(default_factory=list)
    __price_components: list[AppliedPriceComponent] = field(
        default_factory=list, init=False, repr=False
    )
    __price_components_loaded: bool = field(default=False, init=False, repr=False)
    location: "Location" = None

    @property
    def price_components(self):
        """
        Returns the list of applied price components associated with the supply point.

        :return: A list of applied price components.
        :rtype: list[AppliedPriceComponent]
        """
        if not self.__price_components_loaded:
            self.__price_components = self.location.adapter.get_price_components(
                self.id
            )[self.id]
            self.__price_components_loaded = True
        return self.__price_components
