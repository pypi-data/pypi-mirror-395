import doctest
from dataclasses import dataclass

import pytest

import preheat_open.interfaces


@dataclass
class TClass:
    attr1: int
    attr2: str = ""
    attr3: str = ""


class MockFactory(preheat_open.interfaces.Factory):
    _return_class = TClass
    _translation_dict = {
        "attr1": "Attr1",
        "attr2": "Attr2",
        "attr3": "Attr3",
    }


@pytest.fixture(scope="module")
def test_input_dict():
    return {
        "Attr1": 23,
        "Attr2": "Foo",
    }


def test_build_factory(test_input_dict):
    obj = MockFactory(test_input_dict.copy()).build()
    assert isinstance(obj, TClass)
    assert obj.attr1 == 23
    assert obj.attr2 == "Foo"
    assert obj.attr3 == ""


def test_build_factory_with_params(test_input_dict):
    obj2 = MockFactory(test_input_dict.copy()).build(Attr3="Bar")
    assert isinstance(obj2, TClass)
    assert obj2.attr1 == 23
    assert obj2.attr2 == "Foo"
    assert obj2.attr3 == "Bar"


def test_factory_translate():
    d = MockFactory.translate(TClass(23, "Foo"))
    assert d == {"Attr1": 23, "Attr2": "Foo", "Attr3": ""}


def test_doctests():
    """
    Run doctests for the interfaces module.
    These tests ensure that the Factory and BuildingModel classes work as expected.
    """
    result = doctest.testmod(preheat_open.interfaces)
    assert result.failed == 0, f"Doctests failed: {result.failed} errors found"
