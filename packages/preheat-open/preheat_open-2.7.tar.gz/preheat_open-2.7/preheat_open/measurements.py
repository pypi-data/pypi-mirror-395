"""
measurements.py

This module defines classes and functions for handling measurements, including measurement handlers,
mappers, and utilities for retrieving and renaming measurement data.

Classes:
    MeasurementsHandler
    AmbigiuousMapError
    Mapper
    AttributeMapper
    MapApplier

Functions:
    get_measurements
"""

import logging
from abc import ABC, abstractmethod
from collections import ChainMap
from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, Any, Union

import numpy as np
import pandas as pd

from .interfaces import Adapter
from .query import Query, build_instance_from_dict
from .time import DateRange

if TYPE_CHECKING:
    from .collection import Collection
    from .location import Location
    from .unit import Component, Device
    from .zone import Zone


logger = logging.getLogger(__name__)


@dataclass
class MeasurementsRetriever:
    """
    Handles the retrieval and processing of measurements for a given date range and components.

    :ivar date_range: The date range for which to retrieve measurements.
    :vartype date_range: DateRange
    :ivar components: The list of components to retrieve measurements for.
    :vartype components: list[Component]
    :ivar adapter: The adapter used to load measurements.
    :vartype adapter: Adapter
    """

    date_range: DateRange
    components: list["Component"]
    adapter: Adapter

    def get_measurements(self) -> pd.DataFrame:
        """
        Retrieves and processes measurements for the specified components and date range.

        :return: A DataFrame containing the measurements.
        :rtype: pd.DataFrame
        """
        needs_loading = {
            component: missing_dr
            for component in self.components
            if not (missing_dr := component.check_measurement(self.date_range)).empty
        }

        if needs_loading:
            load_range = sum(needs_loading.values())
            self.adapter.load_measurements(
                date_range=load_range,
                components=list(needs_loading.keys()),
            )

        comp_data, comp_missing_data = [], []
        for component in self.components:
            data = component.get_measurement(
                date_range=self.date_range
            ).measurements.rename(
                component.id if component.id is not None else component.cid
            )
            (comp_missing_data if data.empty else comp_data).append(data)
        if comp_data:
            df = pd.concat(comp_data, axis=1).reindex(
                self.date_range.to_pandas_date_range()
            )
            if comp_missing_data:
                logger.info(
                    "No data found for components: %s",
                    [d.name for d in comp_missing_data],
                )
                df[[d.name for d in comp_missing_data]] = np.nan
        else:
            logger.info(
                "No data found for any components: %s",
                [d.name for d in comp_missing_data],
            )
            df = pd.DataFrame(
                columns=[c.name for c in comp_missing_data],
                index=self.date_range.to_pandas_date_range(),
            )

        return df


class AmbigiuousMapError(Exception):
    """
    Exception raised when a mapping is ambiguous.
    """

    pass


@dataclass
class MapItem(ABC):
    """
    Abstract base class for mappers that map components to strings.
    """

    @abstractmethod
    def map(self, component: "Component") -> str:
        """
        Maps a component to a string.

        :param component: The component to map.
        :type component: Component
        :return: The mapped string.
        :rtype: str
        """
        pass


@dataclass
class AttrMap(MapItem):
    """
    Maps a component to a string based on a specified attribute.

    :ivar attribute: The attribute to use for mapping.
    :vartype attribute: str
    """

    attribute: str

    def map(self, component: "Component") -> str:
        """
        Maps a component to a string based on the specified attribute.

        :param component: The component to map.
        :type component: Component
        :return: The mapped string.
        :rtype: str
        """
        attributes = self.attribute.split(".")
        obj = component
        for a in attributes:
            if hasattr(obj, a):
                obj = getattr(obj, a)
            else:
                raise AttributeError(f"{obj} has no attribute '{a}'. Mapping failed.")
        if isinstance(obj, Enum):
            obj = obj.value
        return str(obj)


@dataclass
class StrMap(MapItem):
    """
    Maps a component to a string based on a specified string.

    :ivar string: The string to use for mapping.
    :vartype string: str
    """

    string: str

    def map(self, component: "Component") -> str:
        """
        Maps a component to a string based on the specified string.

        :param component: The component to map.
        :type component: Component
        :return: The mapped string.
        :rtype: str
        """
        return self.string


@dataclass
class Mapper:
    """
    Applies a mapping to components and renames DataFrame columns accordingly.

    :ivar map: The mapping of components to strings.
    :vartype map: dict[Component, str]
    :ivar convention: The list of mappers to use for generating the map.
    :vartype convention: list[Mapper]
    :ivar components: The list of components to map.
    :vartype components: list[Component]
    """

    map: dict["Component", str] = field(default_factory=dict, repr=False)
    convention: list[MapItem] = field(default_factory=list)
    _components: list["Component"] = field(default_factory=list, repr=False)
    prefix: str = ""
    suffix: str = ""
    separator: str = "_"

    def __post_init__(self):
        """
        Post-initialization processing to generate or check the map.
        """
        if self.map:
            self.check_ambigiousness()

    def check(self):
        if self.map:
            self.check_ambigiousness()
        elif self.convention:
            self.create_map()
            self.check_ambigiousness()
        else:
            self.generate_convention()

    @property
    def components(self) -> list["Component"]:
        return self._components

    @components.setter
    def components(self, value: list["Component"]):
        self._components = value
        self.check()

    def check_ambigiousness(self):
        """
        Checks if the map is ambiguous and raises an error if it is.
        """
        output_names = list(self.map.values())
        if list(dict.fromkeys(output_names)) != output_names:
            raise AmbigiuousMapError("Input map is ambigius")

    def generate_convention(self):
        """
        Generates a convention for mapping components.
        """
        convention_try = []
        for m in [
            AttrMap("type"),
            AttrMap("parent.type"),
            AttrMap("parent.id"),
        ]:
            convention_try.append(m)
            self.convention = convention_try
            self.create_map()
            try:
                self.check_ambigiousness()
            except AmbigiuousMapError:
                pass
            else:
                break

    def create_map(self):
        """
        Creates a map of components to strings based on the convention.
        """
        self.map = {comp: self.get_name(comp) for comp in self.components}

    def default_column_name(self, component: "Component") -> int:
        """
        Returns the default column name for a component.

        :param component: The component to get the default column name for.
        :type component: Component
        :return: The default column name.
        :rtype: int
        """
        column_name = (
            component.id if isinstance(component.type, Enum) else component.cid
        )
        if column_name is None:
            raise ValueError(
                f"Component {component} has no id or cid. Cannot determine default column name."
            )
        return column_name

    def rename_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Renames the columns of a DataFrame based on the map.

        :param df: The DataFrame to rename.
        :type df: pd.DataFrame
        :return: The renamed DataFrame.
        :rtype: pd.DataFrame
        """
        if not self.map:
            self.__post_init__()
        map = {self.default_column_name(comp): name for comp, name in self.map.items()}
        return df.rename(columns=map)

    def get_name(self, component: "Component") -> str:
        """
        Gets the name for a component based on the convention.

        :param component: The component to get the name for.
        :type component: Component
        :return: The name of the component.
        :rtype: str
        """
        name = self.separator.join(
            mapitem.map(component) for mapitem in self.convention
        )
        namelist = [part for part in [self.prefix, name, self.suffix] if part]
        name = self.separator.join(namelist)
        return name


@dataclass
class PostProcess:
    """
    Post-processes a DataFrame after mapping.

    :ivar func: The function to apply to the DataFrame.
    :vartype func: Callable
    """

    method: str
    params: dict = field(default_factory=dict)

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Applies the post-processing function to a DataFrame.

        :param df: The DataFrame to apply the function to.
        :type df: pd.DataFrame
        :return: The processed DataFrame.
        :rtype: pd.DataFrame
        """
        if hasattr(df, self.method):
            return getattr(df, self.method)(**self.params)
        else:
            raise AttributeError(f"'DataFrame' object has no attribute '{self.method}'")


@dataclass
class MeasurementRequest:
    query: Query | dict | None = None
    components: list["Component"] = field(default_factory=list)
    mapper: Mapper | None = None
    post_process: PostProcess | None = None
    expected_returns: int | None = None
    fallback: "MeasurementRequest | None" = None
    _fallback_activated: bool = False

    def __post_init__(self):
        if not all(comp.__class__.__name__ == "Component" for comp in self.components):
            raise ValueError("All components must be of type 'Component'")

    def __getattribute__(self, name: str) -> Any:
        if super().__getattribute__("_fallback_activated"):
            fallback = super().__getattribute__("fallback")
            return getattr(fallback, name)
        return super().__getattribute__(name)

    def load(self, obj: Union["Device", "Location", "Collection"]):
        if not self.components:
            self.components = list(obj.get_components(self.query))
            if len(self.components) == 0 and self.fallback is not None:
                self._fallback_activated = True
                self.load(obj)
            elif (
                self.expected_returns is not None
                and len(self.components) != self.expected_returns
            ):
                raise ValueError(
                    f"Expected {self.expected_returns} components, got {len(self.components)}"
                )

        self.mapper = self.mapper or Mapper()
        self.mapper.components = self.components

    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.post_process is not None:
            df = self.post_process.apply(df)
        return df


@dataclass
class MeasurementRequestHandler:
    obj: Union["Device", "Location", "Collection", "Zone"]
    requests: list[MeasurementRequest]
    date_range: DateRange
    frame: pd.DataFrame | None = None
    _mapper: Mapper | None = field(default=None, init=False)

    def __post_init__(self):
        for request in self.requests:
            request.load(self.obj)

    def get_components(self) -> list["Component"]:
        components = {comp for request in self.requests for comp in request.components}
        if not components:
            logger.warning("No components found for requests %s", self.requests)
        return list(components)

    def get_measurements(self) -> pd.DataFrame:
        components = self.get_components()
        if not components:
            return pd.DataFrame()
        retriever = MeasurementsRetriever(
            date_range=self.date_range,
            components=components,
            adapter=self.obj.adapter
            if hasattr(self.obj, "adapter")
            else self.obj.location.adapter,
        )
        self.frame = retriever.get_measurements()
        self.frame = self.mapper.rename_dataframe(self.frame)
        self.post_process()
        self.frame.index = pd.to_datetime(self.frame.index)

        return self.frame

    def post_process(self):
        for request in self.requests:
            cols = list(request.mapper.map.values())
            self.frame[cols] = request.process(self.frame[cols])

    @property
    def mapper(self):
        if self._mapper is None:
            self._mapper = Mapper(
                map=dict(ChainMap(*[request.mapper.map for request in self.requests])),
            )
        return self._mapper


def get_measurements(
    obj: Union["Device", "Location", "Collection", "Zone"],
    requests: list[MeasurementRequest] | MeasurementRequest | None = None,
    date_range: DateRange | None = None,
    **kwargs,
) -> pd.DataFrame:
    """
    Retrieves measurements for the specified object and components.

    :param obj: The object to retrieve measurements for.
    :type obj: Union[Device, Location]
    :param components: The components to retrieve measurements for.
    :type components: list[Component] | Query | dict
    :param date_range: The date range for the measurements.
    :type date_range: DateRange, optional
    :param mapper: The mapper to use for renaming DataFrame columns.
    :type mapper: MapApplier, optional
    :param kwargs: Additional keyword arguments.
    :return: A DataFrame containing the measurements.
    :rtype: pd.DataFrame
    """
    if date_range is None:
        date_range, kwargs = build_instance_from_dict(DateRange, kwargs)
    date_range.astimezone(obj.timezone)

    if requests is None:
        requests = []
    if isinstance(requests, MeasurementRequest):
        requests = [requests]
    if kwargs:
        req, kwargs = build_instance_from_dict(MeasurementRequest, kwargs)
        requests.append(req)
    if not requests:
        requests.append(MeasurementRequest())

    if kwargs:
        raise TypeError(f"Unknown keys received: {list(kwargs)}")

    handler = MeasurementRequestHandler(
        requests=requests,
        obj=obj,
        date_range=date_range,
    )
    return handler.get_measurements()
