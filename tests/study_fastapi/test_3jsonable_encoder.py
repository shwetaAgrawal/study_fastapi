"""Testing FastAPI json encoding behaviour for compound objects."""

import datetime
from enum import Enum
from typing import Any, NamedTuple

import pytest
from attr import dataclass

from study_fastapi.a3_jsonable_encoder import (
    get_fastapi_encoded_string,
    get_fastapi_jsonencoded,
    get_json_dumps,
)


def get_date():
    """Exploring with builtin compund obj which have __str__ and __repr__ methods."""
    return datetime.datetime(2024, 1, 1, 12, 0, 0)


class SampleClass1:
    """Exploring with custom class without any __str__ and __repr__ implementations."""

    int_val: int
    str_val: str
    bool_val: bool

    def __init__(self, int_val: int = 0, str_val: str = "", bool_val: bool = False) -> None:
        self.int_val = int_val
        self.str_val = str_val
        self.bool_val = bool_val

    def get_vals(self):
        """Get all the values.

        Adding method to class to check json conversion for objects with methods.
        """
        return (self.int_val, self.str_val, self.bool_val)


class SampleClass2:
    """Exploring compound objects."""

    obj1: SampleClass1
    date_obj: datetime.datetime

    def __init__(self) -> None:
        self.obj1 = SampleClass1()
        self.date_obj = get_date()

    def get_vals(self):
        """Get the values. Added to test json encoding for object with methods."""
        return (self.obj1.get_vals(), self.date_obj)


@dataclass
class SampleDataClass1:
    """Exploring data class for json encoding."""

    int_val: int = 0
    str_val: str = ""
    bool_val: bool = False


@dataclass
class SampleDataClass2:
    """Exploring data class with compound object."""

    obj1: SampleClass1 = SampleClass1()
    date_obj: datetime.datetime = get_date()


class TestCaseSet(Enum):
    ALL = "all"
    SIMPLE = "simple"
    COMPLEX = "complex"


class TestCase(NamedTuple):
    test_obj: Any
    expected_type: type
    expected_str: str
    test_id: str


def get_test_objects(which: TestCaseSet = TestCaseSet.ALL):
    """Method to get objects for running tests"""
    sample_class1_obj_str = '{"int_val": 0, "str_val": "", "bool_val": false}'
    sample_class2_obj_str = '{{"obj1": {}, "date_obj": "{}"}}'.format(
        sample_class1_obj_str, SampleClass2().date_obj.isoformat()
    )
    sample_data_class2_obj_str = '{{"obj1": {}, "date_obj": "{}"}}'.format(
        sample_class1_obj_str, SampleClass2().date_obj.isoformat()
    )
    simple_list = [
        TestCase(5, int, "5", "int"),
        TestCase(True, bool, "true", "bool"),
        TestCase("hi", str, '"hi"', "str"),
        TestCase(2.3, float, "2.3", "float"),
        TestCase([1, 2, 3], list, "[1, 2, 3]", "list"),
        TestCase(
            {"key": "value", "key2": "value2"}, dict, '{"key": "value", "key2": "value2"}', "dict"
        ),
    ]
    complex_list = [
        TestCase(get_date(), str, '"{}"'.format(get_date().isoformat()), "date"),
        TestCase(SampleClass1(), dict, sample_class1_obj_str, "SampleClass1"),
        TestCase(SampleClass2(), dict, sample_class2_obj_str, "SampleClass2"),
        TestCase(SampleDataClass1(), dict, sample_class1_obj_str, "SampleDataClass1"),
        TestCase(SampleDataClass2(), dict, sample_data_class2_obj_str, "SampleDataClass2"),
    ]
    match which:
        case TestCaseSet.SIMPLE:
            return simple_list
        case TestCaseSet.COMPLEX:
            return complex_list
        case TestCaseSet.ALL:
            return simple_list + complex_list


@pytest.fixture(params=get_test_objects(TestCaseSet.ALL), ids=lambda case: case.test_id)
def case(request) -> TestCase:
    return request.param


@pytest.fixture(params=get_test_objects(TestCaseSet.SIMPLE), ids=lambda case: case.test_id)
def simple_case(request) -> TestCase:
    return request.param


@pytest.fixture(params=get_test_objects(TestCaseSet.COMPLEX), ids=lambda case: case.test_id)
def complex_case(request) -> TestCase:
    return request.param


def test_fastapi_jsonable_encoder(case: TestCase):
    """Test fastapi json encoding behavior for these objects"""
    obj = get_fastapi_jsonencoded(case.test_obj)
    assert obj
    assert type(obj) is case.expected_type


def test_fastapi_encoded_string(case: TestCase):
    """Test fastapi json encoding behavior for these objects"""
    json_str_fastapi = get_fastapi_encoded_string(case.test_obj)
    assert json_str_fastapi
    assert isinstance(json_str_fastapi, str)
    assert json_str_fastapi == case.expected_str


def test_json_dumps_success(simple_case: TestCase):
    """Test fastapi json encoding behavior for these objects"""
    json_str = get_json_dumps(simple_case.test_obj)
    assert json_str
    assert isinstance(json_str, str)
    assert json_str == simple_case.expected_str


def test_json_dumps_failure(complex_case: TestCase):
    """Test fastapi json encoding behavior for the complex objects"""
    with pytest.raises(TypeError):
        _ = get_json_dumps(complex_case.test_obj)
