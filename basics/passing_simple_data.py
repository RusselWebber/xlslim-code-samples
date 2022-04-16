from datetime import datetime
from math import pi


def echo_type(x):
    return repr(type(x))


def echo_type_int(x: int) -> str:
    return repr(type(x))


def echo_type_float(x: float) -> str:
    return repr(type(x))


def echo_type_string(x: str) -> str:
    return repr(type(x))


def echo_type_bool(x: bool) -> str:
    return repr(type(x))


def echo_type_datetime(x: datetime) -> str:
    return repr(type(x))


def return_int() -> int:
    return 1


def return_float() -> float:
    return pi


def return_string() -> str:
    return "Hello!"


def return_bool() -> bool:
    return False


def return_datetime() -> datetime:
    return datetime.now()


def return_int_no_type_hints():
    return 1


def return_float_no_type_hints():
    return pi


def return_string_no_type_hints():
    return "Hello!"


def return_bool_no_type_hints():
    return False


def return_datetime_no_type_hints():
    return datetime.now()
