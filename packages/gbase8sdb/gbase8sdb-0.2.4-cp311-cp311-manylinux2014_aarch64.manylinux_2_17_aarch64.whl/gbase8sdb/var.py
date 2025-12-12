# coding: utf-8

from typing import Any, Callable
from .driver import DbType


class Var:
    def __repr__(self):
        value = self._cyobj.get_all_values()
        if not self._cyobj.is_array and len(value) == 1:
            value = value[0]
        typ = self._type
        return f"<gbase8sdb.Var of type {typ.name} with value {repr(value)}>"

    @classmethod
    def _create_with_cyobj(cls, impl, typ=None):
        var = cls.__new__(cls)
        var._cyobj = impl
        if typ is not None:
            var._type = typ
        else:
            var._type = impl.dbtype
        return var

    @property
    def actual_elements(self) -> int:
        if self._cyobj.is_array:
            return self._cyobj.num_elements_in_array
        return self._cyobj.num_elements

    @property
    def actualElements(self) -> int:
        return self.actual_elements

    @property
    def buffer_size(self) -> int:
        return self._cyobj.buffer_size

    @property
    def bufferSize(self) -> int:
        return self.buffer_size

    @property
    def convert_nulls(self) -> bool:
        return self._cyobj.convert_nulls

    def getvalue(self, pos: int = 0) -> Any:
        return self._cyobj.get_value(pos)

    @property
    def inconverter(self) -> Callable:
        return self._cyobj.inconverter

    @property
    def num_elements(self) -> int:
        return self._cyobj.num_elements

    @property
    def numElements(self) -> int:
        return self.num_elements

    @property
    def outconverter(self) -> Callable:
        return self._cyobj.outconverter

    def setvalue(self, pos: int, value: Any) -> None:
        self._cyobj.set_value(pos, value)

    @property
    def size(self) -> int:
        return self._cyobj.size

    @property
    def type(self) -> DbType:
        return self._type

    @property
    def values(self) -> list:
        return self._cyobj.get_all_values()
