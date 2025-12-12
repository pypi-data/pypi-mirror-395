# coding: utf-8

"""
Database API functions
"""
import datetime
from . import errors


def Date(year: int, month: int, day: int) -> datetime.date:
    return datetime.date(year, month, day)

def Time(hour: int, minute: int, second: int) -> None:
    errors.raise_error(errors.ERR_TIME_NOT_SUPPORTED)
    
def Timestamp(year: int, month: int, day: int, hour: int, minute: int, second: int) -> datetime.datetime:
    return datetime.datetime(year, month, day, hour, minute, second)

def DateFromTicks(ticks: float) -> datetime.date:
    return datetime.date.fromtimestamp(ticks)


def TimeFromTicks(ticks: float) -> None:
    errors.raise_error(errors.ERR_TIME_NOT_SUPPORTED)


def TimestampFromTicks(ticks: float) -> datetime.datetime:
    return datetime.datetime.fromtimestamp(ticks)


def Binary(value, encoding='utf-8') -> bytes:
    if isinstance(value, str):
        return value.encode(encoding)
    return bytes(value)
