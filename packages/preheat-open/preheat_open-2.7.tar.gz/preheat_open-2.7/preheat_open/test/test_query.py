from __future__ import annotations

import doctest
from dataclasses import dataclass, field
from datetime import datetime
from typing import ClassVar, Generator

import pytest

import preheat_open.query


@dataclass
class TClass:
    id: int
    attr1: str = ""
    attr2: str = ""
    attr3: list[TClass] = field(default_factory=list)
    attr4: TClass = None


@dataclass(eq=False)
class TClassQuery(preheat_open.query.Query):
    id: list[int] = field(default_factory=list)
    attr1: list[str] = field(default_factory=list)
    attr2: list[str] = field(default_factory=list)
    attr4: list[TClass] = field(default_factory=list)
    _type_attr4: ClassVar[type] = TClass
    _class: ClassVar[type] = TClass


@pytest.fixture(scope="module")
def test_object0():
    return TClass(id=1, attr1="value1", attr2="value2", attr3=[])


@pytest.fixture(scope="module")
def test_object1():
    return TClass(
        id=2,
        attr1="value1",
        attr2="value3",
        attr3=[
            TClass(id=5, attr1="value1", attr2="value2", attr3=[]),
            TClass(id=4, attr1="value2", attr2="value3", attr3=[]),
        ],
    )


@pytest.fixture(scope="module")
def test_object2():
    return TClass(id=3, attr1="value3", attr2="value2", attr3=[])


@pytest.fixture(scope="module")
def test_query0():
    return TClassQuery(attr1=["value1"])


@pytest.fixture(scope="module")
def test_query1():
    return TClassQuery(id=[2], attr1=["value1"], attr2=["value3"])


@pytest.fixture(scope="module")
def test_query2():
    return TClassQuery(id=[3], attr1=["value3"], attr2=["value2"])


@pytest.mark.parametrize(
    "query, expected",
    [
        (TClassQuery(attr1="value1"), (["value1"], [])),
        (TClassQuery(attr2="value2"), ([], ["value2"])),
    ],
)
def test_query_post_init(query, expected):
    attr1, attr2 = expected
    assert query.attr1 == attr1
    assert query.attr2 == attr2


@pytest.mark.parametrize(
    "obj, query, expected",
    [
        ("test_object0", "test_query0", True),
        ("test_object1", "test_query1", True),
        ("test_object2", "test_query2", True),
        ("test_object0", "test_query1", False),
        ("test_object1", "test_query0", True),
        ("test_object0", "test_query2", False),
        ("test_object2", "test_query0", False),
        ("test_object1", "test_query2", False),
        ("test_object2", "test_query1", False),
    ],
)
def test_query_equal(obj, query, expected, request):
    fobj = request.getfixturevalue(obj)
    fquery = request.getfixturevalue(query)
    assert (fobj == fquery) == expected


def test_query_convert_attr():
    converted = TClassQuery.convert_attr({"id": 0, "attr1": "test"}, "attr4")
    assert isinstance(converted, TClass)
    assert converted.attr1 == "test"


def test_query_from_kwargs():
    kwargs = dict(attr1="value1", attr2="value2")
    query: TClassQuery = TClassQuery.from_kwargs(**kwargs)
    assert query.attr1 == ["value1"]
    assert query.attr2 == ["value2"]


@pytest.mark.parametrize(
    "query, obj, expected",
    [
        ("test_query0", "test_object0", 1),
        ("test_query1", "test_object1", 1),
        ("test_query2", "test_object2", 1),
        ("test_query1", "test_object0", 0),
        ("test_query0", "test_object1", 2),
        ("test_query2", "test_object0", 0),
        ("test_query0", "test_object2", 0),
        ("test_query1", "test_object2", 0),
        ("test_query2", "test_object1", 0),
    ],
)
def test_query_stuff(query, obj, expected, request):
    fquery = request.getfixturevalue(query)
    fobj = request.getfixturevalue(obj)
    results = list(
        preheat_open.query.query_stuff(
            obj=fobj,
            query=fquery,
            query_type=TClassQuery,
            sub_obj_attrs=["attr3"],
            include_obj=True,
        )
    )
    assert len(results) == expected


def test_unique():
    def generator() -> Generator[int, None, None]:
        yield 1

    assert preheat_open.query.unique(generator()) == 1

    def generator_multiple() -> Generator[int, None, None]:
        yield 1
        yield 2

    with pytest.raises(preheat_open.query.NoUniqueElementError):
        preheat_open.query.unique(generator_multiple())

    def generator_none() -> Generator[int, None, None]:
        if False:
            yield

    with pytest.raises(preheat_open.query.NoElementError):
        preheat_open.query.unique(generator_none())


def test_doctests():
    """
    Run doctests for the interfaces module.
    """
    result = doctest.testmod(preheat_open.query)
    assert result.failed == 0, f"Doctests failed: {result.failed} errors"
