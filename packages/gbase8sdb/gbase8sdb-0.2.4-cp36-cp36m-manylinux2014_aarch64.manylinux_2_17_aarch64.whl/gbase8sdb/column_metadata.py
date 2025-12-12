# coding: utf-8
from typing import Union

from . import __name__ as MODULE_NAME

from .driver import (
    DbType,
    DB_TYPE_NUMBER,
    DB_TYPE_BINARY_INTEGER,
    DB_TYPE_BINARY_DOUBLE,
    DB_TYPE_BINARY_FLOAT,
    DB_TYPE_TIMESTAMP_TZ,
    DB_TYPE_TIMESTAMP_LTZ,
    DB_TYPE_TIMESTAMP,
    DB_TYPE_DATE,

)


class ColumnMetaData:

    __module__ = MODULE_NAME


    def __str__(self):
        return str(tuple(self))
    
    def __repr__(self):
        return repr(tuple(self))


    def __len__(self):
        return 7

    
    def __eq__(self, other):
        return tuple(self) == other
    
    def __getitem__(self, index):
        description = (
            self.name,
            self.type_code,
            self.display_size,
            self.internal_size,
            self.precision,
            self.scale,
            self.null_ok,
        )
        return description[index]

    @classmethod
    def _create_with_cyobj(cls, cyobj):
        info = cls.__new__(cls)
        info._type = None
        info._cyobj = cyobj
        return info
    
    @staticmethod
    def _is_date_type(dbtype):
        return dbtype in {DB_TYPE_DATE, DB_TYPE_TIMESTAMP, DB_TYPE_TIMESTAMP_LTZ, DB_TYPE_TIMESTAMP_TZ}

    @staticmethod
    def _is_numeric_type(dbtype):
        return dbtype in {DB_TYPE_BINARY_FLOAT, DB_TYPE_BINARY_DOUBLE, DB_TYPE_BINARY_INTEGER, DB_TYPE_NUMBER}

    @property
    def internal_size(self):
        if self._cyobj.size > 0:
            return self._cyobj.buffer_size

    @property
    def is_json(self):
        return self._cyobj.is_json

    @property
    def name(self) -> str:
        return self._cyobj.name



    @property
    def precision(self) -> Union[int, None]:
        if self._cyobj.precision or self._cyobj.scale:
            return self._cyobj.precision



    @property
    def type(self) -> DbType:
        if self._type is None:
            self._type = self._cyobj.dbtype
        return self._type

    @property
    def type_code(self) -> DbType:
        return self._cyobj.dbtype
    
    @property
    def display_size(self):
        if self._cyobj.size > 0:
            return self._cyobj.size
        dbtype = self._cyobj.dbtype
        if self._is_numeric_type(dbtype):
            if self._cyobj.precision:
                display_size = self._cyobj.precision + 1
                if self._cyobj.scale > 0:
                    display_size += self._cyobj.scale + 1
            else:
                display_size = 127
            return display_size
        elif self._is_date_type(dbtype):
            return 23
    
    @property
    def scale(self):
        if self._cyobj.precision or self._cyobj.scale:
            return self._cyobj.scale
    
    @property
    def null_ok(self):
        return self._cyobj.nulls_allowed
