"""
Query Module for Object Filtering and Retrieval
===============================================

This module provides classes and functions for querying objects based on specified criteria.
It supports filtering objects by attributes, nested object querying, and unique element retrieval.

Classes:
    Query: Represents a query for filtering objects based on specified attributes
    NoElementError: Raised when no elements are found in a generator
    NoUniqueElementError: Raised when multiple elements are found where one is expected

Functions:
    build_instance_from_dict: Builds class instances from dictionaries
    query_stuff: Queries objects and their sub-objects recursively
    unique: Returns the unique element from a generator
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from inspect import signature
from typing import ClassVar, Generator, Iterable, Sequence, Type, TypeVar

T = TypeVar("T")
QueryT = TypeVar("QueryT", bound="Query")


def build_instance_from_dict(
    cls: Type[T], data: dict, remove_keys: bool = True
) -> tuple[T, dict]:
    """
    Build an instance of a dataclass from a dictionary.

    This function creates an instance of the specified class using values from
    the provided dictionary. It only uses keys that match the class constructor
    parameters and optionally removes used keys from the dictionary.

    :param cls: The class to build an instance of
    :type cls: Type[T]
    :param data: The dictionary containing constructor parameters
    :type data: dict
    :param remove_keys: Whether to remove used keys from the dictionary
    :type remove_keys: bool
    :return: Tuple of the created instance and remaining dictionary
    :rtype: tuple[T, dict]

    Example:
        >>> from dataclasses import dataclass
        >>>
        >>> @dataclass
        ... class Person:
        ...     name: str
        ...     age: int
        >>>
        >>> data = {"name": "Alice", "age": 30, "city": "NYC"}
        >>> person, remaining = build_instance_from_dict(Person, data.copy())
        >>> person.name
        'Alice'
        >>> person.age
        30
        >>> remaining
        {'city': 'NYC'}
    """

    cls_fields = list(signature(cls.__init__).parameters)

    obj = cls(**{k: v for k, v in data.items() if k in cls_fields})

    if remove_keys:
        for k in cls_fields:
            data.pop(k, None)

    return obj, data


@dataclass
class Query:
    """
    Represents a query for filtering objects based on specified attributes.

    A Query object defines criteria for filtering objects by their attributes.
    It supports exact matching, list-based filtering, and exclusion patterns.
    Queries can be combined and used to filter collections of objects.

    :cvar _class: The class type that the query is designed to filter
    :type _class: ClassVar
    :param exclude: A nested Query object for exclusion criteria
    :type exclude: Query, optional

    .. note::
        This is an abstract base class. Concrete query classes should inherit
        from this class and define their specific filtering attributes.
        When inheriting, ensure that the eq=False parameter is set in the dataclass decorator
        to prevent default equality checks based on object identity.

    Example:
        >>> # Create a simple query subclass for demonstration
        >>> from dataclasses import field
        >>> @dataclass(eq=False)
        ... class SimpleQuery(Query):
        ...     name: list[str] = field(default_factory=list)
        ...     _class = object  # Normally would be a specific class
        >>>
        >>> query = SimpleQuery(name="test")
        >>> query.name
        ['test']
    """

    _class: ClassVar
    exclude: Query | None = None

    def __post_init__(self):
        """
        Initialize query attributes after instance creation.

        This method converts single values to lists and applies type conversion
        to query attributes. It also handles nested exclude queries.

        Example:
            >>> from dataclasses import field
            >>> @dataclass(eq=False)
            ... class TestQuery(Query):
            ...     name: list[str] = field(default_factory=list)
            ...     _class = object
            >>>
            >>> query = TestQuery(name="single")
            >>> isinstance(query.name, list)
            True
            >>> query.name
            ['single']
        """
        for attribute, value in self.__dict__.items():
            if attribute == "exclude":
                if value is not None and isinstance(value, dict):
                    setattr(self, attribute, self.from_kwargs(**value))
            else:
                value = value if isinstance(value, list) else [value]
                setattr(
                    self, attribute, [self.convert_attr(v, attribute) for v in value]
                )

    @classmethod
    def is_type(cls, obj: object) -> bool:
        """
        Check if an object is of the type this query is designed to filter.

        This method uses a naming convention where the query class name
        ends with "Query" and the target class name is the prefix.

        :param obj: The object to check
        :type obj: object
        :return: True if the object matches the expected type
        :rtype: bool

        Example:
            >>> from dataclasses import field
            >>> @dataclass(eq=False)
            ... class PersonQuery(Query):
            ...     _class = object
            >>>
            >>> class Person:
            ...     pass
            >>>
            >>> person = Person()
            >>> PersonQuery.is_type(person)
            True
        """
        return cls.__name__[:-5] == obj.__class__.__name__

    def __eq__(self, other: object) -> bool:
        """
        Check if an object matches this query's criteria.

        This method evaluates whether the given object satisfies all the
        filtering conditions defined in this query. It also handles
        exclusion criteria if specified.

        :param other: The object to evaluate against the query
        :type other: object
        :return: True if the object matches all criteria
        :rtype: bool

        Example:
            >>> from dataclasses import dataclass, field
            >>> @dataclass
            ... class Person:
            ...     name: str
            ...     age: int
            >>>
            >>> @dataclass(eq=False)
            ... class PersonQuery(Query):
            ...     name: list[str] = field(default_factory=list)
            ...     age: list[int] = field(default_factory=list)
            ...     _class = Person
            >>>
            >>> person = Person("Alice", 30)
            >>> query = PersonQuery(name="Alice")
            >>> query == person
            True
            >>>
            >>> query2 = PersonQuery(name="Bob")
            >>> query2 == person
            False
        """

        def match(attr, query_list):
            if attr is None and not query_list:
                return True
            else:
                return attr in query_list

        if isinstance(other, self._class):
            matches = [
                match(getattr(other, attr_name), query_list)
                for attr_name, query_list in self.__dict__.items()
                if query_list and attr_name != "exclude"
            ]
            if self.exclude is not None and self.exclude == other:
                return False
            return all(matches)
        return False

    def isin(self, iterable: Iterable) -> bool:
        """
        Check if this query matches any element in an iterable.

        This method iterates through the provided iterable and returns True
        if any element matches this query's criteria.

        :param iterable: The iterable to search through
        :type iterable: Iterable
        :return: True if any element matches the query
        :rtype: bool

        Example:
            >>> from dataclasses import field
            >>> @dataclass
            ... class Person:
            ...     name: str
            >>>
            >>> @dataclass(eq=False)
            ... class PersonQuery(Query):
            ...     name: list[str] = field(default_factory=list)
            ...     _class = Person
            >>>
            >>> people = [Person("Alice"), Person("Bob"), Person("Charlie")]
            >>> query = PersonQuery(name="Bob")
            >>> query.isin(people)
            True
            >>>
            >>> query2 = PersonQuery(name="David")
            >>> query2.isin(people)
            False
        """
        return any(self == item for item in iterable)

    @classmethod
    def convert_attr(cls, value, name):
        """
        Convert an attribute value to the appropriate type.

        This method applies type conversion based on class-defined type hints
        or special type attributes. It supports both direct instantiation
        and dictionary-based construction.

        :param value: The value to convert
        :type value: Any
        :param name: The attribute name for type lookup
        :type name: str
        :return: The converted value
        :rtype: Any

        Example:
            >>> from dataclasses import field
            >>> @dataclass(eq=False)
            ... class TestQuery(Query):
            ...     _type_age = int
            ...     _class = object
            >>>
            >>> converted = TestQuery.convert_attr("25", "age")
            >>> converted
            25
            >>> isinstance(converted, int)
            True
        """
        if not isinstance(value, list):
            try:
                class_type = getattr(cls, f"_type_{name}")
                class_type = cls if class_type == "self" else class_type
                if not isinstance(value, class_type):
                    value = (
                        class_type(**value)
                        if isinstance(value, dict)
                        else class_type(value)
                    )
            except AttributeError:
                pass
        return value

    @classmethod
    def from_kwargs(
        cls: Type[QueryT],
        query: QueryT | None = None,
        **kwargs,
    ) -> QueryT:
        """
        Create a Query object from keyword arguments.

        This factory method creates a new Query instance from keyword arguments,
        with optional base query for inheritance. It validates that all provided
        keys are valid attributes for the query class.

        :param query: An existing Query object to use as a base
        :type query: Query, optional
        :param kwargs: Additional keyword arguments for query attributes
        :return: A new Query object of the same type as the class
        :rtype: QueryT
        :raises TypeError: If unknown keys are provided in kwargs

        Example:
            >>> from dataclasses import field
            >>> @dataclass(eq=False)
            ... class PersonQuery(Query):
            ...     name: list[str] = field(default_factory=list)
            ...     age: list[int] = field(default_factory=list)
            ...     _class = object
            >>>
            >>> query = PersonQuery.from_kwargs(name="Alice", age=30)
            >>> type(query).__name__
            'PersonQuery'
            >>> query.name
            ['Alice']
            >>> query.age
            [30]
        """
        if query is None:
            allowed_keys = [f.name for f in fields(cls)]
            if wrong_keys := [
                key for key, _ in kwargs.items() if key not in allowed_keys
            ]:
                raise TypeError(
                    f"Unknown keys received when instantiating {cls}. Expected keys are {allowed_keys} but received {wrong_keys}."
                )
            build_pars = {
                key: cls.convert_attr(val, key)
                for key, val in kwargs.items()
                if key in allowed_keys
            }

            return cls(**build_pars)  # type: ignore
        return query


def query_stuff(
    obj: object,
    query: Query | Sequence[Query | dict] | dict | None,
    sub_obj_attrs: list[str],
    sub_obj_attrs_for_removal: list[str] | None = None,
    query_type: type[Query] | None = None,
    include_obj: bool = False,
    **kwargs,
) -> Generator[object, None, None]:
    """
    Recursively query objects and their sub-objects based on specified criteria.

    This function performs a recursive search through an object and its nested
    attributes, yielding all objects that match the provided query criteria.
    It supports filtering by multiple queries and can traverse complex object
    hierarchies.

    :param obj: The root object to start querying from
    :type obj: object
    :param query: The query or list of queries to apply for filtering
    :type query: Query | Sequence[Query | dict] | None
    :param sub_obj_attrs: Attribute names containing sub-objects to query
    :type sub_obj_attrs: list[str]
    :param sub_obj_attrs_for_removal: Attributes to skip in nested queries
    :type sub_obj_attrs_for_removal: list[str], optional
    :param query_type: The Query class type to use for filtering
    :type query_type: type
    :param include_obj: Whether to include the root object if it matches
    :type include_obj: bool
    :param kwargs: Additional keyword arguments for query creation
    :return: Generator yielding objects that match the query
    :rtype: Generator[object, None, None]

    Example:
        >>> # Create a simple object hierarchy for demonstration
        >>> from dataclasses import field
        >>> @dataclass
        ... class Person:
        ...     name: str
        ...     children: list = None
        ...     def __post_init__(self):
        ...         self.children = self.children or []
        >>>
        >>> @dataclass(eq=False)
        ... class PersonQuery(Query):
        ...     name: list[str] = field(default_factory=list)
        ...     _class = Person
        >>>
        >>> # Create test data
        >>> child1 = Person("Alice")
        >>> child2 = Person("Bob")
        >>> parent = Person("Charlie", [child1, child2])
        >>>
        >>> # Query for specific name
        >>> results = list(query_stuff(
        ...     parent,
        ...     PersonQuery(name="Alice"),
        ...     ["children"],
        ...     query_type=PersonQuery
        ... ))
        >>> len(results)
        1
        >>> results[0].name
        'Alice'
    """
    if query_type is None:
        raise ValueError(
            "query_type must be specified. It should be a subclass of Query."
        )
    sub_obj_attrs_for_removal = (
        sub_obj_attrs_for_removal if sub_obj_attrs_for_removal is not None else []
    )

    if isinstance(query, list):
        queries = [
            q if isinstance(q, Query) else query_type.from_kwargs(**q) for q in query
        ]
    elif isinstance(query, dict):
        queries = [query_type.from_kwargs(**query)]
    else:
        queries = [
            query if isinstance(query, Query) else query_type.from_kwargs(**kwargs)
        ]
    # Yield the object if it is a match to the query
    if query_type.is_type(obj) and include_obj and obj in queries:
        yield obj
    # Iterate through the sub-objects and query them
    for sub_obj_attr in sub_obj_attrs:
        try:
            sub_objs = getattr(obj, sub_obj_attr)
        except AttributeError:
            continue
        else:
            sub_objs = sub_objs if isinstance(sub_objs, Iterable) else [sub_objs]
            sub_obj_attrs_i = [
                i for i in sub_obj_attrs if i not in sub_obj_attrs_for_removal
            ]
            if sub_obj_attr == "related_units" and "children" in sub_obj_attrs_i:
                sub_obj_attrs_i.remove("children")
            for sub_obj in sub_objs:
                yield from query_stuff(
                    obj=sub_obj,
                    sub_obj_attrs=sub_obj_attrs_i,
                    query=queries,
                    query_type=query_type,
                    include_obj=True,
                )


class NoElementError(Exception):
    """
    Exception raised when no elements are found in a generator.

    This exception is raised by the :func:`unique` function when attempting
    to retrieve a unique element from a generator that yields no elements.

    Example:
        >>> def empty_generator():
        ...     return
        ...     yield  # This line is never reached
        >>>
        >>> try:
        ...     unique(empty_generator())
        ... except NoElementError as e:
        ...     str(e)
        'Generator yields no elements'
    """


class NoUniqueElementError(Exception):
    """
    Exception raised when multiple elements are found where one is expected.

    This exception is raised by the :func:`unique` function when attempting
    to retrieve a unique element from a generator that yields multiple elements.

    Example:
        >>> def multi_generator():
        ...     yield 1
        ...     yield 2
        >>>
        >>> try:
        ...     unique(multi_generator())
        ... except NoUniqueElementError as e:
        ...     str(e)
        'Generator yields more than one unique element'
    """


def unique(generator: Generator[T, None, None]) -> T:
    """
    Return the unique element from a generator.

    This function ensures that a generator yields exactly one element.
    It raises appropriate exceptions if the generator yields zero or
    multiple elements.

    :param generator: A generator that should yield exactly one element
    :type generator: Generator[T, None, None]
    :return: The unique element from the generator
    :rtype: T
    :raises NoElementError: If the generator yields no elements
    :raises NoUniqueElementError: If the generator yields multiple elements

    Example:
        >>> def single_generator():
        ...     yield "unique_value"
        >>>
        >>> result = unique(single_generator())
        >>> result
        'unique_value'

        >>> def empty_generator():
        ...     return
        ...     yield  # Never reached
        >>>
        >>> try:
        ...     unique(empty_generator())
        ... except NoElementError:
        ...     print("No elements found")
        No elements found

        >>> def multi_generator():
        ...     yield 1
        ...     yield 2
        >>>
        >>> try:
        ...     unique(multi_generator())
        ... except NoUniqueElementError:
        ...     print("Multiple elements found")
        Multiple elements found
    """
    try:
        # Get the first element from the generator
        unique_element = next(generator)
    except StopIteration as e:
        # Raise an error if the generator yields no elements
        raise NoElementError("Generator yields no elements") from e

    try:
        # Try to get the second element from the generator
        next(generator)
        # If we get here, it means there is more than one element
        raise NoUniqueElementError("Generator yields more than one unique element")
    except StopIteration:
        # If StopIteration is raised, it means there was only one element
        pass

    return unique_element
