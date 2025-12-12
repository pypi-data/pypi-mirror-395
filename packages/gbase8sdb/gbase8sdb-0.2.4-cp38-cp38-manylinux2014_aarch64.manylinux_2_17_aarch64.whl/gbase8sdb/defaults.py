# coding: utf-8

from . import driver
from . import __name__ as MODULE_NAME


class Defaults:
    __module__ = MODULE_NAME

    def __init__(self) -> None:
        self._cyobj = driver.DEFAULTS

    @property
    def arraysize(self) -> int:
        return self._cyobj.arraysize

    @arraysize.setter
    def arraysize(self, value: int):
        self._cyobj.arraysize = value

    @property
    def fetch_lobs(self) -> bool:
        return self._cyobj.fetch_lobs

    @fetch_lobs.setter
    def fetch_lobs(self, value: str):
        self._cyobj.fetch_lobs = value

    @property
    def fetch_decimals(self) -> bool:
        return self._cyobj.fetch_decimals

    @fetch_decimals.setter
    def fetch_decimals(self, value: str):
        self._cyobj.fetch_decimals = value

    @property
    def prefetchrows(self) -> int:
        return self._cyobj.prefetchrows

    @prefetchrows.setter
    def prefetchrows(self, value: int):
        self._cyobj.prefetchrows = value


defaults = Defaults()
