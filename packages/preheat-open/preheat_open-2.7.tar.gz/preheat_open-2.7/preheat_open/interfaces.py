from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import wraps
from typing import TYPE_CHECKING, Any, ClassVar, TypeVar, final

from requests.models import Response

from .loadable_types import ComfortProfiles, ElectricityPrices
from .time import DateRange

if TYPE_CHECKING:
    from .collection import Collection
    from .loadable_types import SetpointSchedule
    from .location import Location, LocationInformation
    from .supplypoint import AppliedPriceComponent, PriceData
    from .unit import Component, Device, Unit

logger = logging.getLogger(__name__)


def log_method_call(logger=logger, level="debug"):
    """
    Decorator that logs method calls with their arguments.

    This decorator automatically logs method calls on adapter classes,
    including the class name, method name, and all arguments.

    :param logger: Logger instance to use for logging
    :type logger: logging.Logger
    :param level: Log level to use (default: "debug")
    :type level: str
    :return: Decorator function
    :rtype: Callable

    Example:
        >>> import logging
        >>> test_logger = logging.getLogger("test")
        >>>
        >>> @log_method_call(logger=test_logger, level="info")
        ... def example_method(self, arg1, arg2=None):
        ...     return f"Called with {arg1}, {arg2}"
        >>>
        >>> class TestClass:
        ...     def __init__(self):
        ...         pass
        >>>
        >>> # The decorator works on methods
        >>> callable(log_method_call())
        True
    """

    def decorator(method):
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            # Format the arguments and keyword arguments
            args_str = ", ".join(repr(arg) for arg in args)
            kwargs_str = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())
            all_args_str = ", ".join(filter(None, [args_str, kwargs_str]))

            # Log the formatted message
            getattr(logger, level)(
                "%s.%s(%s)",
                self.__class__.__name__,
                method.__name__,
                all_args_str,
            )
            return method(self, *args, **kwargs)

        return wrapper

    return decorator


@dataclass
class BuildingModel:
    """
    Configuration class that defines the types used by a building management system.

    This class acts as a registry of types used for different building components,
    queries, and operations. It allows adapters to specify which concrete types
    they work with for different building elements.

    :param component_query_type: Type used for querying components
    :type component_query_type: type
    :param component_type: Type representing building components
    :type component_type: type
    :param unit_query_type: Type used for querying units
    :type unit_query_type: type
    :param unit_type: Type representing building units
    :type unit_type: type
    :param unit_subtype: Subtype of units for specialization
    :type unit_subtype: type
    :param device_query_type: Type used for querying devices
    :type device_query_type: type
    :param device_type: Type representing building devices
    :type device_type: type
    :param zone_query_type: Type used for querying zones
    :type zone_query_type: type
    :param zone_type: Type representing building zones
    :type zone_type: type
    :param control_setting_type: Type for control settings
    :type control_setting_type: type

    Example:
        >>> # Create a simple building model configuration
        >>> class SimpleComponent: pass
        >>> class SimpleQuery: pass
        >>>
        >>> model = BuildingModel(
        ...     component_query_type=SimpleQuery,
        ...     component_type=SimpleComponent,
        ...     unit_query_type=SimpleQuery,
        ...     unit_type=SimpleComponent,
        ...     unit_subtype=SimpleComponent,
        ...     device_query_type=SimpleQuery,
        ...     device_type=SimpleComponent,
        ...     zone_query_type=SimpleQuery,
        ...     zone_type=SimpleComponent,
        ...     control_setting_type=SimpleComponent
        ... )
        >>> model.component_type == SimpleComponent
        True
    """

    component_query_type: type
    component_type: type
    unit_query_type: type
    unit_type: type
    unit_subtype: type
    device_query_type: type
    device_type: type
    zone_query_type: type
    zone_type: type
    control_setting_type: type


T = TypeVar("T", bound="Adapter")


class Adapter(ABC):
    """
    Abstract base class for building management system adapters.

    An Adapter provides a standardized interface for accessing different
    building management systems. It handles connections, data retrieval,
    and system-specific operations while presenting a unified API.

    :cvar building_model: Configuration defining the types used by this adapter
    :type building_model: BuildingModel

    .. note::
        All concrete adapters must implement the abstract methods defined here.
        The adapter automatically logs method calls for methods starting with
        "get_", "put_", or "load_".

    Example:
        >>> # Abstract class cannot be instantiated directly
        >>> try:
        ...     adapter = Adapter()
        ... except TypeError as e:
        ...     "Can't instantiate abstract class" in str(e)
        True
    """

    def __init__(self, building_model: BuildingModel) -> None:
        self.building_model: BuildingModel = building_model

    @abstractmethod
    def open(self) -> None:
        """
        Open connection to the building management system.

        This method should establish any necessary connections, authenticate,
        and prepare the adapter for data operations.

        :raises ConnectionError: If connection cannot be established
        """
        pass

    @abstractmethod
    def close(self) -> None:
        """
        Close connection to the building management system.

        This method should clean up resources, close connections, and
        perform any necessary cleanup operations.
        """
        pass

    def __enter__(self: T) -> T:
        """
        Context manager entry point.

        Automatically opens the connection when entering the context.

        :return: The adapter instance
        :rtype: Adapter
        """
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        """
        Context manager exit point.

        Automatically closes the connection when exiting the context.

        :param exc_type: Exception type if an exception occurred
        :param exc_value: Exception value if an exception occurred
        :param traceback: Traceback if an exception occurred
        :return: False to propagate exceptions
        :rtype: bool
        """
        self.close()
        return False

    @abstractmethod
    def get_features(self, location_id: int):
        """
        Retrieve available features for a specific location.

        :param location_id: ID of the location to query
        :type location_id: int
        :return: Available features for the location
        """
        pass

    @abstractmethod
    def get_all_locations_information(self) -> list[LocationInformation]:
        """
        Retrieve information about all available locations.

        :return: List of location information objects
        :rtype: list[LocationInformation]
        """
        pass

    @abstractmethod
    def get_all_locations_collection(self) -> Collection:
        """
        Retrieve a collection containing all available locations.

        :return: Collection with all locations
        :rtype: Collection
        """
        pass

    @abstractmethod
    def get_location(self, location_id: int) -> Location:
        """
        Retrieve a specific location by ID.

        :param location_id: ID of the location to retrieve
        :type location_id: int
        :return: Location object
        :rtype: Location
        :raises ValueError: If location ID is not found
        """
        pass

    @abstractmethod
    def get_locations(self, location_ids: list[int]) -> list[Location]:
        """
        Retrieve multiple locations by their IDs.

        :param location_ids: List of location IDs to retrieve
        :type location_ids: list[int]
        :return: List of location objects
        :rtype: list[Location]
        :raises ValueError: If any location ID is not found
        """
        pass

    @abstractmethod
    def get_devices(self, location_id: int) -> list[Device]:
        """
        Retrieve all devices for a specific location.

        :param location_id: ID of the location
        :type location_id: int
        :return: List of devices in the location
        :rtype: list[Device]
        """
        pass

    @abstractmethod
    def load_measurements(
        self,
        components: list[Component],
        date_range: DateRange,
    ) -> None:
        """
        Load measurement data for specified components and date range.

        This method loads measurement data into the components' internal storage,
        typically for later retrieval or analysis.

        :param components: List of components to load measurements for
        :type components: list[Component]
        :param date_range: Time range for the measurements
        :type date_range: DateRange
        :raises ValueError: If components or date range is invalid
        """
        pass

    @abstractmethod
    def get_comfort_profile_setpoints(
        self, date_range: DateRange, location: Location | int
    ) -> ComfortProfiles:
        """
        Retrieve comfort profile setpoints for a location and date range.

        :param date_range: Time range for the comfort profiles
        :type date_range: DateRange
        :param location: Location object or location ID
        :type location: Location | int
        :return: List of comfort profiles
        :rtype: list[ComfortProfile]
        """
        pass

    @abstractmethod
    def get_price_components(
        self,
        supply_point_ids: list[int],
    ) -> dict[int, list[AppliedPriceComponent]]:
        """
        Retrieve price components for specified supply points.

        :param supply_point_ids: List of supply point IDs
        :type supply_point_ids: list[int]
        :return: Dictionary mapping supply point IDs to their price components
        :rtype: dict[int, list[AppliedPriceComponent]]
        """
        pass

    @abstractmethod
    def get_price_data(
        self,
        date_range: DateRange,
        price_component_ids: list[int],
    ) -> dict[int, PriceData]:
        """
        Retrieve price data for specified components and date range.

        :param date_range: Time range for the price data
        :type date_range: DateRange
        :param price_component_ids: List of price component IDs
        :type price_component_ids: list[int]
        :return: Dictionary mapping component IDs to their price data
        :rtype: dict[int, PriceData]
        """
        pass

    @abstractmethod
    def put_setpoint_schedule(
        self, schedule: SetpointSchedule, control_unit: Unit
    ) -> Response:
        """
        Upload a setpoint schedule to a control unit.

        :param schedule: Setpoint schedule to upload
        :type schedule: SetpointSchedule
        :param control_unit: Control unit to receive the schedule
        :type control_unit: Unit
        :return: HTTP response from the upload operation
        :rtype: Response
        :raises ValueError: If schedule or control unit is invalid
        """
        pass

    @abstractmethod
    def get_setpoint_schedule(
        self,
        date_range: DateRange,
        control_unit: Unit,
    ) -> SetpointSchedule:
        """
        Retrieve setpoint schedule from a control unit.

        :param control_unit: Control unit to query
        :type control_unit: Unit
        :param date_range: Time range for the schedule
        :type date_range: DateRange
        :return: Setpoint schedule
        :rtype: SetpointSchedule
        """
        pass

    @abstractmethod
    def get_electricity_prices(
        self,
        date_range: DateRange,
        unit: Unit,
        include_vat: bool,
        include_tariff: bool,
    ) -> ElectricityPrices:
        """
        Retrieve electricity prices for a unit and date range.

        :param unit: Unit to get prices for
        :type unit: Unit
        :param date_range: Time range for the prices
        :type date_range: DateRange
        :param include_vat: Whether to include VAT in prices
        :type include_vat: bool
        :param include_tariff: Whether to include tariff in prices
        :type include_tariff: bool
        :return: Electricity price data
        :rtype: ElectricityPrices
        """
        pass

    def location_post_setup(self, location: Location) -> None:
        """
        Perform post-setup operations on a location.

        This method is called after a location has been created and allows
        the adapter to perform any additional setup or configuration.

        :param location: Location that was just created
        :type location: Location

        Example:
            >>> # Default implementation does nothing
            >>> class TestAdapter(Adapter):
            ...     def location_post_setup(self, location):
            ...         pass  # Custom setup logic would go here
            >>>
            >>> # Method exists and is callable
            >>> hasattr(Adapter, 'location_post_setup')
            True
        """
        pass

    def __init_subclass__(cls, **kwargs):
        """
        Automatically apply logging to adapter methods.

        This method is called when a subclass of Adapter is created.
        It automatically applies the log_method_call decorator to methods
        that start with "get_", "put_", or "load_".

        :param kwargs: Keyword arguments passed to the subclass
        """
        super().__init_subclass__(**kwargs)
        for method_name in dir(cls):
            if any(method_name.startswith(s) for s in ["get_", "put_", "load_"]):
                method = getattr(cls, method_name, None)
                if method and not hasattr(method, "_is_logged"):
                    # Apply decorator and mark the method as already decorated
                    logged_method = log_method_call(logger=logger)(method)
                    setattr(logged_method, "_is_logged", True)
                    setattr(cls, method_name, logged_method)


class Factory(ABC):
    """
    Abstract factory class for creating objects from dictionaries.

    The Factory pattern provides a way to create objects from configuration
    dictionaries, with automatic translation of keys and validation of
    unused parameters.

    :param input_dict: Dictionary containing configuration data
    :type input_dict: dict[str, Any]
    :ivar _return_class: Class to instantiate
    :type _return_class: type
    :ivar _translation_dict: Mapping of attribute names to dictionary keys
    :type _translation_dict: dict[str, str]

    Example:
        >>> # Create a simple factory example
        >>> class SimpleFactory(Factory):
        ...     def __init__(self, input_dict=None):
        ...         super().__init__(input_dict or {})
        ...         self._return_class = dict
        ...         self._translation_dict = {"key": "value"}
        >>>
        >>> factory = SimpleFactory({"value": "test"})
        >>> isinstance(factory.input_dict, dict)
        True
    """

    _return_class: type
    _translation_dict: dict[str, str]

    def __init__(self, input_dict: dict[str, Any] = {}) -> None:
        """
        Initialize the factory with input configuration.

        :param input_dict: Dictionary containing configuration data
        :type input_dict: dict[str, Any]

        Example:
            >>> factory = Factory.__new__(Factory)
            >>> factory.__init__({"test": "value"})
            >>> factory.input_dict
            {'test': 'value'}
        """
        self.input_dict = input_dict

    def make_sub_classes(self) -> None:
        """
        Create any necessary sub-objects before building the main object.

        This method is called before building the main object and allows
        the factory to create any dependent objects or modify the input
        dictionary as needed.

        .. note::
            Override this method in subclasses to implement custom
            sub-object creation logic.
        """
        pass

    @final
    def build(self, **kwargs) -> Any:
        """
        Build the target object from the configuration dictionary.

        This method processes the input dictionary, creates any necessary
        sub-objects, and instantiates the target class with the translated
        parameters.

        :param kwargs: Additional keyword arguments to merge with input_dict
        :return: Instance of the target class
        :rtype: Any
        :raises TypeError: If translation fails

        Example:
            >>> class TestClass:
            ...     def __init__(self, name):
            ...         self.name = name
            >>>
            >>> class TestFactory(Factory):
            ...     def __init__(self, input_dict=None):
            ...         super().__init__(input_dict or {})
            ...         self._return_class = TestClass
            ...         self._translation_dict = {"name": "test_name"}
            >>>
            >>> factory = TestFactory({"test_name": "example"})
            >>> obj = factory.build()
            >>> obj.name
            'example'
        """
        self.input_dict.update(kwargs)
        self.make_sub_classes()
        obj = self._return_class(
            **{
                key: self.input_dict.pop(val)
                for key, val in self._translation_dict.items()
                if val in self.input_dict
            }
        )
        for key, val in self.input_dict.items():
            logger.warning(
                "Unused key-value pair in %s: (%s: %s) Context: %s",
                self.__class__,
                key,
                val,
                obj,
            )
        return obj

    @classmethod
    def translate(self, obj) -> Any:
        """
        Translate an object back to its dictionary representation.

        This class method reverses the build process, converting an object
        back to the dictionary format expected by the factory.

        :param obj: Object to translate
        :return: Dictionary representation of the object
        :rtype: Any
        :raises TypeError: If object is not of the expected type

        Example:
            >>> class TestClass:
            ...     def __init__(self, name):
            ...         self.name = name
            >>>
            >>> class TestFactory(Factory):
            ...     _return_class = TestClass
            ...     _translation_dict = {"name": "test_name"}
            >>>
            >>> obj = TestClass("example")
            >>> result = TestFactory.translate(obj)
            >>> result
            {'test_name': 'example'}
        """
        if isinstance(obj, self._return_class):
            return {
                val: getattr(obj, key) for key, val in self._translation_dict.items()
            }
        else:
            raise TypeError(
                f"Wrong object type to translate, received {type(obj)} but expected {self._return_class}."
            )
