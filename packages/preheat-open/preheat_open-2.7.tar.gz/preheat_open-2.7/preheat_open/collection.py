import logging
from typing import Callable, Generator

import pandas as pd

from .configuration import PersonalConfig
from .interfaces import Adapter
from .location import Location, LocationInformation
from .measurements import get_measurements
from .query import Query
from .time import ZoneInfo, tzinfo
from .unit import Component, Device, Unit
from .zone import Zone

logger = logging.getLogger(__name__)


class Collection:
    """
    Represents a collection of locations for building management systems.

    A Collection manages multiple locations and provides unified access to their
    building models, measurements, and components. It supports lazy loading of
    building models and filtering capabilities.

    :param locations: Dictionary mapping LocationInformation to Location objects
    :type locations: dict[LocationInformation, Location | None] | None
    :param adapter: Data adapter for accessing external systems
    :type adapter: Adapter | None
    :param _models_loaded: Whether building models have been loaded
    :type _models_loaded: bool

    .. note::
        Building models are loaded lazily when first accessed through methods
        like :meth:`get_units`, :meth:`get_devices`, etc.

    Example:
        >>> from preheat_open.collection import Collection
        >>> from preheat_open.location import LocationInformation
        >>>
        >>> # Create empty collection
        >>> collection = Collection()
        >>> len(collection.locations)
        0

        >>> # Create collection with location information
        >>> loc_info = LocationInformation(id=1, label="Building A")
        >>> collection = Collection(locations={loc_info: None})
        >>> len(collection.locations)
        1
    """

    def __init__(
        self,
        locations: dict[LocationInformation, Location | None] | None = None,
        adapter: Adapter | None = None,
        _models_loaded: bool = False,
    ):
        """
        Initialize the Collection.

        :param locations: The locations in the collection
        :type locations: dict[LocationInformation, Location | None] | None
        :param adapter: The adapter for data access
        :type adapter: Adapter | None
        :param _models_loaded: Whether models are loaded
        :type _models_loaded: bool

        Example:
            >>> collection = Collection()
            >>> collection.locations
            {}
            >>> collection._models_loaded
            False
        """
        self.locations = locations or {}
        self.adapter = adapter
        self._models_loaded = _models_loaded

        # Post-initialization processing
        if (
            all([loc is not None for loc in self.locations.values()])
            and len(self.locations) > 0
        ):
            self._models_loaded = True

    @classmethod
    def from_location_ids(
        cls, location_ids: list[int], adapter: Adapter, **kwargs
    ) -> "Collection":
        """
        Create a collection from a list of location IDs.

        This factory method retrieves location data using the provided adapter
        and creates a Collection instance with the loaded locations.

        :param location_ids: List of location IDs to load
        :type location_ids: list[int]
        :param adapter: Data adapter for retrieving locations
        :type adapter: Adapter
        :param kwargs: Additional keyword arguments passed to constructor
        :return: New Collection instance with loaded locations
        :rtype: Collection

        :raises ValueError: If adapter cannot retrieve locations for given IDs
        """
        locations = adapter.get_locations(location_ids)
        return cls(
            locations={l.information: l for l in locations},
            adapter=adapter,
            **kwargs,
        )

    @classmethod
    def from_location_information_list(
        cls, location_information_list: list[LocationInformation], **kwargs
    ) -> "Collection":
        """
        Create a collection from a list of LocationInformation objects.

        This factory method creates a Collection with placeholder entries
        that will be loaded lazily when needed.

        :param location_information_list: List of location information objects
        :type location_information_list: list[LocationInformation]
        :param kwargs: Additional keyword arguments passed to constructor
        :return: New Collection instance with location placeholders
        :rtype: Collection

        Example:
            >>> from preheat_open.location import LocationInformation
            >>>
            >>> loc_infos = [
            ...     LocationInformation(id=1, label="Building A"),
            ...     LocationInformation(id=2, label="Building B")
            ... ]
            >>> collection = Collection.from_location_information_list(loc_infos)
            >>> len(collection.locations)
            2
            >>> all(loc is None for loc in collection.locations.values())
            True
        """
        return cls(
            locations={loc_info: None for loc_info in location_information_list},
            **kwargs,
        )

    def get_keys(self, **kwargs) -> Generator[LocationInformation, None, None]:
        """
        Retrieve LocationInformation keys filtered by attributes.

        Yields LocationInformation objects that match the specified attribute filters.
        All provided keyword arguments must match the corresponding attributes.

        :param kwargs: Attribute filters (attribute_name=value)
        :return: Generator yielding matching LocationInformation objects
        :rtype: Generator[LocationInformation, None, None]
        """
        for loc_info in self.locations.keys():
            if all(getattr(loc_info, key) == value for key, value in kwargs.items()):
                yield loc_info

    def load_building_models(self) -> None:
        """
        Load building models for locations that haven't been loaded yet.

        This method identifies locations with None values and loads their
        building models using the configured adapter. Only loads models
        for locations with valid IDs.

        :raises ValueError: If adapter is not set when loading is required

        .. note::
            This method is called automatically by other methods when
            building models are needed.
        """
        ids_to_load = [
            loc_info.id
            for loc_info, model in self.locations.items()
            if model is None and loc_info.id is not None
        ]
        if ids_to_load:
            if self.adapter is None:
                raise ValueError("Adapter is not set. Cannot load building models.")
            logger.debug("Loading building models for location IDs: %s", ids_to_load)
            models = self.adapter.get_locations(location_ids=ids_to_load)
            for model in models:
                key = next(self.get_keys(id=model.id))
                self.locations[key] = model

    def filter(self, location_info_filter: Callable) -> "Collection":
        """
        Create a filtered collection based on a filter function.

        Applies the provided filter function to LocationInformation objects
        and returns a new Collection containing only matching locations.

        :param location_info_filter: Function that takes LocationInformation and returns bool
        :type location_info_filter: Callable[[LocationInformation], bool]
        :return: New filtered Collection instance
        :rtype: Collection

        Example:
            >>> from preheat_open.location import LocationInformation
            >>>
            >>> loc1 = LocationInformation(id=1, label="Building A")
            >>> loc2 = LocationInformation(id=2, label="Building B")
            >>> collection = Collection(locations={loc1: None, loc2: None})
            >>>
            >>> # Filter by label containing "A"
            >>> filtered = collection.filter(lambda loc: "A" in loc.label)
            >>> len(filtered.locations)
            1
            >>> list(filtered.locations.keys())[0].label
            'Building A'
        """
        return Collection(
            locations={
                loc_info: loc
                for loc_info, loc in self.locations.items()
                if location_info_filter(loc_info)
            },
            adapter=self.adapter,
        )

    def get_locations(
        self,
    ) -> Generator[Location, None, None]:
        """
        Retrieve all loaded Location objects in the collection.

        Loads building models for locations that are not yet loaded.

        :return: Generator yielding loaded Location objects
        :rtype: Generator[Location, None, None]
        """
        if not self._models_loaded:
            self.load_building_models()
        for _, loc in self.locations.items():
            if loc is not None:
                yield loc

    def get_measurements(
        self,
        **kwargs,
    ) -> pd.DataFrame:
        """
        Retrieve measurements for all locations in the collection.

        Automatically loads building models if not already loaded, then
        retrieves measurements using the configured measurement system.

        :param kwargs: Additional arguments passed to measurement retrieval
        :return: DataFrame containing measurements from all locations
        :rtype: pd.DataFrame

        .. seealso::
            :func:`preheat_open.measurements.get_measurements` for available parameters
        """
        if not self._models_loaded:
            self.load_building_models()
        return get_measurements(
            obj=self,
            **kwargs,
        )

    def get_units(
        self,
        query: Query | dict | None = None,
        **kwargs,
    ) -> Generator[Unit, None, None]:
        """
        Retrieve units from all locations in the collection.

        Automatically loads building models if needed, then yields all units
        that match the optional query criteria.

        :param query: Query object to filter units
        :type query: Query | None
        :param kwargs: Additional arguments passed to location unit retrieval
        :return: Generator yielding Unit objects
        :rtype: Generator[Unit, None, None]
        """
        if not self._models_loaded:
            self.load_building_models()
        for location in self.get_locations():
            yield from location.get_units(
                query=query,
                **kwargs,
            )

    def get_devices(
        self,
        query: Query | list[Query | dict[str, str]] | None = None,
        **kwargs,
    ) -> Generator[Device, None, None]:
        """
        Retrieve devices from all locations in the collection.

        Automatically loads building models if needed, then yields all devices
        that match the optional query criteria.

        :param query: Query object(s) or dict to filter devices
        :type query: Query | list[Query | dict[str, str]] | None
        :param kwargs: Additional arguments passed to location device retrieval
        :return: Generator yielding Device objects
        :rtype: Generator[Device, None, None]
        """
        if not self._models_loaded:
            self.load_building_models()
        for location in self.get_locations():
            yield from location.get_devices(
                query=query,
                **kwargs,
            )

    def get_zones(
        self,
        query: Query | list[Query] | None = None,
        **kwargs,
    ) -> Generator[Zone, None, None]:
        """
        Retrieve zones from all locations in the collection.

        Automatically loads building models if needed, then yields all zones
        that match the optional query criteria.

        :param query: Query object(s) to filter zones
        :type query: Query | list[Query] | None
        :param kwargs: Additional arguments passed to location zone retrieval
        :return: Generator yielding Zone objects
        :rtype: Generator[Zone, None, None]
        """
        if not self._models_loaded:
            self.load_building_models()
        for location in self.get_locations():
            yield from location.get_zones(
                query=query,
                **kwargs,
            )

    def get_components(
        self,
        query: Query | list[Query | dict[str, str]] | None = None,
        **kwargs,
    ) -> Generator[Component, None, None]:
        """
        Retrieve components from all locations in the collection.

        Automatically loads building models if needed, then yields all components
        that match the optional query criteria.

        :param query: Query object(s) or dict to filter components
        :type query: Query | list[Query | dict[str, str]] | None
        :param kwargs: Additional arguments passed to location component retrieval
        :return: Generator yielding Component objects
        :rtype: Generator[Component, None, None]
        """
        if not self._models_loaded:
            self.load_building_models()
        for location in self.get_locations():
            yield from location.get_components(
                query=query,
                **kwargs,
            )

    @property
    def timezone(self) -> tzinfo:
        """
        Get the timezone for the collection.

        Returns the timezone from the personal configuration. This property
        provides a fallback timezone when individual locations don't specify one.

        :return: Timezone information object
        :rtype: tzinfo

        Example:
            >>> collection = Collection()
            >>> tz = collection.timezone
            >>> isinstance(tz, tzinfo)
            True
            >>> # Timezone comes from PersonalConfig
            >>> str(type(tz).__name__)
            'ZoneInfo'
        """
        timezone = ZoneInfo(PersonalConfig().timezone)
        logger.debug(
            "Tried using timezone on %s. Fallback to timezone from configuration: %s",
            self.__class__.__name__,
            timezone,
        )
        return timezone
