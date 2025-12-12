# coding: utf-8
"""
the package of gbase8sdb __init__ module
"""

import sys
import collections

apilevel = "2.0"
paramstyle = "qmark"
threadsafety = 2

# version info
from .version import __version__
version = __version__

# import GSDK
# from . import driver, gsdk_driver
from . import driver

from .driver import (
    DB_TYPE_BINARY_DOUBLE,
    DB_TYPE_BINARY_FLOAT,
    DB_TYPE_BINARY_INTEGER,
    DB_TYPE_BLOB,
    DB_TYPE_CHAR,
    DB_TYPE_CLOB,
    DB_TYPE_CURSOR,
    DB_TYPE_DATE,   # map to TIMESTAMP
    DB_TYPE_INTERVAL_DS,
    DB_TYPE_INTERVAL_YM,
    DB_TYPE_LONG_NVARCHAR,
    DB_TYPE_NCHAR,
    DB_TYPE_NCLOB,
    DB_TYPE_NUMBER,
    DB_TYPE_NVARCHAR,
    DB_TYPE_TIMESTAMP,
    DB_TYPE_TIMESTAMP_TZ,
    DB_TYPE_VARCHAR,
    # DB API
    BINARY,
    DATETIME,
    NUMBER,
    ROWID,
    STRING,
)


from .exceptions import (
    Warning as Warning,
    Error as Error,
    DatabaseError as DatabaseError,
    DataError as DataError,
    IntegrityError as IntegrityError,
    InterfaceError as InterfaceError,
    InternalError as InternalError,
    NotSupportedError as NotSupportedError,
    OperationalError as OperationalError,
    ProgrammingError as ProgrammingError,
)

from .defaults import defaults

from .connection import (
    connect, 
    connect_async, 
    Connection, 
    AsyncConnection
)

from .cursor import  Cursor, AsyncCursor

from .lob import LOB, AsyncLOB

from .column_metadata import ColumnMetaData

from .var import Var

from .dsn import makedsn

from .driver import load_gsdk as __load_gsdk, clientversion

from .constructors import (
    Binary as Binary,
    Date as Date,
    DateFromTicks as DateFromTicks,
    Time as Time,
    TimeFromTicks as TimeFromTicks,
    Timestamp as Timestamp,
    TimestampFromTicks as TimestampFromTicks,
)


IntervalYM = collections.namedtuple("IntervalYM", ["years", "months"])


package = sys.modules[__name__]
driver.init_driver(package)


del package
del sys
del driver, connection, constructors
del cursor, dsn, exceptions, column_metadata
del lob
del var

__load_gsdk()


__all__ = [
    # defined in DB API
    "apilevel", "paramstyle", "threadsafety", 
    "BINARY", "DATETIME", "NUMBER", "ROWID", "STRING",
    "Binary", "Date", "DateFromTicks", "Time", "TimeFromTicks", "Timestamp", "TimestampFromTicks",
    "Warning", "Error", "DatabaseError", "DataError", "IntegrityError", "InterfaceError",
    "InternalError", "NotSupportedError", "OperationalError", "ProgrammingError",
    "connect", "Connection", "connect_async", "AsyncConnection", "AsyncCursor", "AsyncLOB",
    # not define in DB API
    "DB_TYPE_BINARY_DOUBLE", "DB_TYPE_BINARY_FLOAT", "DB_TYPE_BINARY_INTEGER", "DB_TYPE_BLOB",
    "DB_TYPE_CHAR", "DB_TYPE_CLOB", "DB_TYPE_CURSOR", "DB_TYPE_DATE", "DB_TYPE_INTERVAL_DS",
    "DB_TYPE_INTERVAL_YM", "DB_TYPE_LONG_NVARCHAR", "DB_TYPE_NCHAR", "DB_TYPE_NCLOB",
    "DB_TYPE_NUMBER", "DB_TYPE_NVARCHAR", "DB_TYPE_TIMESTAMP", "DB_TYPE_TIMESTAMP_TZ", "DB_TYPE_VARCHAR",
    "ColumnMetaData", "Var", "makedsn", "clientversion", "IntervalYM", 
    "defaults", "Cursor", "LOB", "version"
]
