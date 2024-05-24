from datetime import datetime
from typing import Optional, List
from math import pi

def echo_type(a, b=None):
    return repr(type(b))

def echo_type_int(a: int, b: int = 1) -> str:
    return repr(type(b))

def echo_type_int_none(a: int, b: int = None) -> str:
    return repr(type(b))

def echo_type_optional_int(a: int, b: Optional[int] = 1) -> str:
    return repr(type(b))

def echo_type_optional_int_none(a: int, b: Optional[int] = None) -> str:
    return repr(type(b))

def echo_type_float(a: float, b: float = pi) -> str:
    return repr(type(b))

def echo_type_float_none(a: float, b: float = None) -> str:
    return repr(type(b))


def echo_type_optional_float(a: float, b: Optional[float] = pi) -> str:
    return repr(type(b))

def echo_type_optional_float_none(a: float, b: Optional[float] = None) -> str:
    return repr(type(b))

def echo_type_str(a: str, b: str = "test") -> str:
    return repr(type(b))

def echo_type_str_none(a: str, b: str = None) -> str:
    return repr(type(b))


def echo_type_optional_str(a: str, b: Optional[str] = "test") -> str:
    return repr(type(b))


def echo_type_optional_str_none(a: str, b: Optional[str] = None) -> str:
    return repr(type(b))

def echo_type_bool(a: bool, b: bool = False) -> str:
    return repr(type(b))

def echo_type_bool_none(a: bool, b: bool = None) -> str:
    return repr(type(b))


def echo_type_optional_bool(a: bool, b: Optional[bool] = False) -> str:
    return repr(type(b))

def echo_type_optional_bool_none(a: bool, b: Optional[bool] = None) -> str:
    return repr(type(b))


def echo_type_datetime(a: datetime, b: datetime = datetime.now()) -> str:
    return repr(type(b))

def echo_type_datetime_none(a: datetime, b: datetime = None) -> str:
    return repr(type(b))


def echo_type_optional_datetime(a: datetime, b: Optional[datetime] = datetime.now()) -> str:
    return repr(type(b))

def echo_type_optional_datetime_none(a: datetime, b: Optional[datetime] = None) -> str:
    return repr(type(b))

def echo_type_int_list(a: int, b: List[int] = [1]) -> str:
    return repr(type(b))

def echo_type_int_list_none(a: int, b: List[int] = None) -> str:
    return repr(type(b))

def echo_type_optional_int_list(a: int, b: Optional[List[int]] = [1]) -> str:
    return repr(type(b))

def echo_type_optional_int_list_none(a: int, b: Optional[List[int]] = None) -> str:
    return repr(type(b))

def echo_type_float_list(a: float, b: List[float] = [pi]) -> str:
    return repr(type(b))

def echo_type_float_list_none(a: float, b: List[float] = None) -> str:
    return repr(type(b))


def echo_type_optional_float_list(a: float, b: Optional[List[float]] = [pi]) -> str:
    return repr(type(b))

def echo_type_optional_float_list_none(a: float, b: Optional[List[float]] = None) -> str:
    return repr(type(b))

def echo_type_str_list(a: str, b: List[str] = ["test"]) -> str:
    return repr(type(b))

def echo_type_str_list_none(a: str, b: List[str] = None) -> str:
    return repr(type(b))


def echo_type_optional_str_list(a: str, b: Optional[List[str]] = ["test"]) -> str:
    return repr(type(b))


def echo_type_optional_str_list_none(a: str, b: Optional[List[str]] = None) -> str:
    return repr(type(b))

def echo_type_bool_list(a: bool, b: List[bool] = [False]) -> str:
    return repr(type(b))

def echo_type_bool_list_none(a: bool, b: List[bool] = None) -> str:
    return repr(type(b))


def echo_type_optional_bool_list(a: bool, b: Optional[List[bool]] = [False]) -> str:
    return repr(type(b))

def echo_type_optional_bool_list_none(a: bool, b: Optional[List[bool]] = None) -> str:
    return repr(type(b))


def echo_type_datetime_list(a: datetime, b: List[datetime] = [datetime.now()]) -> str:
    return repr(type(b))

def echo_type_datetime_list_none(a: datetime, b: List[datetime] = None) -> str:
    return repr(type(b))


def echo_type_optional_datetime_list(a: datetime, b: Optional[List[datetime]] = [datetime.now()]) -> str:
    return repr(type(b))

def echo_type_optional_datetime_list_none(a: datetime, b: Optional[List[datetime]] = None) -> str:
    return repr(type(b))

