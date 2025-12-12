# coding: utf-8

from typing import Any, Union, Callable

from . import __name__ as MODULE_NAME
from . import errors
from .column_metadata import ColumnMetaData
from .var import Var
from .driver import DbType
from asyncio import get_event_loop



class Cursor:
    __module__ = MODULE_NAME
    _cyobj = None

    def __init__(
        self,
        connection,
    ) -> None:
        self.connection = connection
        self._cyobj = connection._cyobj.create_cursor_impl(False)
        
    def __del__(self):
        if self._cyobj is not None:
            self._cyobj.close(in_del=True)

    def __enter__(self):
        self._verify_open()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self._verify_open()
        self._cyobj.close(in_del=True)
        self._cyobj = None

    def __repr__(self):
        cls_name = f"{self.__class__.__module__}.{self.__class__.__qualname__}"
        return f"<{cls_name} on {self.connection!r}>"

    def __iter__(self):
        return self

    def __next__(self):
        self._verify_fetch()
        row = self._cyobj.fetch_next_row(self)
        if row is not None:
            return row
        raise StopIteration

    def _get_gci_attr(self, attr_num: int, attr_type: int) -> Any:
        self._verify_open()
        return self._cyobj._get_gci_attr(attr_num, attr_type)

    def _set_gci_attr(self, attr_num: int, attr_type: int, value: Any) -> None:
        self._verify_open()
        self._cyobj._set_gci_attr(attr_num, attr_type, value)
        
        
    @staticmethod
    def _check_proc_args(parameters: Union[list, tuple], keyword_parameters: dict):
        if parameters is not None and not isinstance(parameters, (list, tuple)):
            errors.raise_error(errors.ERR_ARGS_MUST_BE_LIST_OR_TUPLE)
        if keyword_parameters is not None and not isinstance(
            keyword_parameters, dict
        ):
            errors.raise_error(errors.ERR_KEYWORD_ARGS_MUST_BE_DICT)

    def _call(
        self,
        name: str,
        parameters: Union[list, tuple],
        keyword_parameters: dict,
        return_value: Any = None,
    ) -> None:
        self._check_proc_args(parameters, keyword_parameters)
        self._verify_open()
        statement, bind_values = self._call_get_execute_args(
            name, parameters, keyword_parameters, return_value
        )
        return self.execute(statement, bind_values)

    def _call_get_execute_args(
        self,
        name: str,
        parameters: Union[list, tuple],
        keyword_parameters: dict,
        return_value: str = None,
    ) -> None:
        bind_names = []
        bind_values = []
        statement_parts = ["begin "]
        if return_value is not None:
            statement_parts.append(":retval := ")
            bind_values.append(return_value)
        statement_parts.append(name + "(")
        if parameters:
            bind_values.extend(parameters)
            bind_names = [":%d" % (i + 1) for i in range(len(parameters))]
        if keyword_parameters:
            for arg_name, arg_value in keyword_parameters.items():
                bind_values.append(arg_value)
                bind_names.append(f"{arg_name} => :{len(bind_names) + 1}")
        statement_parts.append(",".join(bind_names))
        statement_parts.append("); end;")
        statement = "".join(statement_parts)
        return (statement, bind_values)    
    
    def _prepare(
        self, statement: str, tag: str = None, cache_statement: bool = True
    ) -> None:
        self._cyobj.prepare(statement, tag, cache_statement)

    def _prepare_for_execute(
        self, statement, parameters, keyword_parameters=None
    ):
        self._verify_open()
        self._cyobj._prepare_for_execute(
            self, statement, parameters, keyword_parameters
        )

    def _verify_fetch(self) -> None:
        self._verify_open()
        if not self._cyobj.is_query(self):
            errors.raise_error(errors.ERR_NOT_A_QUERY)

    def _verify_open(self) -> None:
        if self._cyobj is None:
            errors.raise_error(errors.ERR_CURSOR_NOT_OPEN)
        self.connection._verify_connected()
    

    def callproc(
        self,
        name: str,
        parameters: Union[list, tuple] = None,
        keyword_parameters: dict = None,
        *,
        keywordParameters: dict = None,
    ) -> list:
        if keywordParameters is not None:
            if keyword_parameters is not None:
                errors.raise_error(
                    errors.ERR_DUPLICATED_PARAMETER,
                    deprecated_name="keywordParameters",
                    new_name="keyword_parameters",
                )
            keyword_parameters = keywordParameters
        self._call(name, parameters, keyword_parameters)
        if parameters is None:
            return []
        return [
            v.get_value(0) for v in self._cyobj.bind_vars[: len(parameters)]
        ]

    def execute(
        self,
        statement: Union[str, None],
        parameters: Union[list, tuple, dict] = None,
        **keyword_parameters: Any,
    ) -> Any:
        self._prepare_for_execute(statement, parameters, keyword_parameters)
        impl = self._cyobj
        impl.execute(self)
        if impl.fetch_vars is not None:
            return self

    def executemany(
        self,
        statement: Union[str, None],
        parameters: Union[list, int],
        batcherrors: bool = False,
        arraydmlrowcounts: bool = False,
    ) -> None:
        self._verify_open()
        num_execs = self._cyobj._prepare_for_executemany(
            self, statement, parameters
        )
        self._cyobj.executemany(
            self, num_execs, bool(batcherrors), bool(arraydmlrowcounts)
        )

    def fetchall(self) -> list:
        self._verify_fetch()
        result = []
        fetch_next_row = self._cyobj.fetch_next_row
        while True:
            row = fetch_next_row(self)
            if row is None:
                break
            result.append(row)
        return result

    def fetchmany(self, size: int = None, numRows: int = None) -> list:
        self._verify_fetch()
        if size is None:
            if numRows is not None:
                size = numRows
            else:
                size = self._cyobj.arraysize
        elif numRows is not None:
            errors.raise_error(
                errors.ERR_DUPLICATED_PARAMETER,
                deprecated_name="numRows",
                new_name="size",
            )
        result = []
        fetch_next_row = self._cyobj.fetch_next_row
        while len(result) < size:
            row = fetch_next_row(self)
            if row is None:
                break
            result.append(row)
        return result

    def fetchone(self) -> Any:
        self._verify_fetch()
        return self._cyobj.fetch_next_row(self)

    def parse(self, statement: str) -> None:
        self._verify_open()
        self._prepare(statement)
        self._cyobj.parse(self)

    def bindnames(self) -> list:
        self._verify_open()
        if self._cyobj.statement is None:
            errors.raise_error(errors.ERR_NO_STATEMENT_PREPARED)
        return self._cyobj.get_bind_names()

    def close(self) -> None:
        self._verify_open()
        self._cyobj.close()
        self._cyobj = None

    def setinputsizes(self, *args: Any, **kwargs: Any) -> Union[list, dict]:
        if args and kwargs:
            errors.raise_error(errors.ERR_ARGS_AND_KEYWORD_ARGS)
        elif args or kwargs:
            self._verify_open()
            return self._cyobj.setinputsizes(self.connection, args, kwargs)
        return []

    def setoutputsize(self, size: int, column: int = 0) -> None:
        pass

    def prepare(
        self, statement: str, tag: str = None, cache_statement: bool = True
    ) -> None:
        self._verify_open()
        self._prepare(statement, tag, cache_statement)

    def var(
        self,
        typ: Union[DbType, type],
        size: int = 0,
        arraysize: int = 1,
        inconverter: Callable = None,
        outconverter: Callable = None,
        encoding_errors: str = None,
        bypass_decode: bool = False,
        convert_nulls: bool = False,
        *,
        encodingErrors: str = None,
    ) -> "Var":
        self._verify_open()
        if encodingErrors is not None:
            if encoding_errors is not None:
                errors.raise_error(
                    errors.ERR_DUPLICATED_PARAMETER,
                    deprecated_name="encodingErrors",
                    new_name="encoding_errors",
                )
            encoding_errors = encodingErrors
        return self._cyobj.create_var(
            self.connection,
            typ,
            size,
            arraysize,
            inconverter,
            outconverter,
            encoding_errors,
            bypass_decode,
            convert_nulls=convert_nulls,
        )

    def arrayvar(
        self,
        typ: Union[DbType, type],
        value: Union[list, int],
        size: int = 0,
    ) -> Var:
        self._verify_open()
        if isinstance(value, list):
            num_elements = len(value)
        elif isinstance(value, int):
            num_elements = value
        else:
            raise TypeError("expecting integer or list of values")
        var = self._cyobj.create_var(
            self.connection,
            typ,
            size=size,
            num_elements=num_elements,
            is_array=True,
        )
        if isinstance(value, list):
            var.setvalue(0, value)
        return var

    @property
    def arraysize(self) -> int:
        self._verify_open()
        return self._cyobj.arraysize

    @arraysize.setter
    def arraysize(self, value: int) -> None:
        self._verify_open()
        if not isinstance(value, int) or value <= 0:
            errors.raise_error(errors.ERR_INVALID_ARRAYSIZE)
        self._cyobj.arraysize = value

    @property
    def bindvars(self) -> list:
        self._verify_open()
        return self._cyobj.get_bind_vars()

    @property
    def description(self) -> tuple:
        self._verify_open()
        if self._cyobj.is_query(self):
            return [
                ColumnMetaData._create_with_cyobj(i) for i in self._cyobj.column_metadata_impls
            ]

    @property
    def fetchvars(self) -> list:
        self._verify_open()
        return self._cyobj.get_fetch_vars()

    @property
    def inputtypehandler(self) -> Callable:
        self._verify_open()
        return self._cyobj.inputtypehandler

    @inputtypehandler.setter
    def inputtypehandler(self, value: Callable) -> None:
        self._verify_open()
        self._cyobj.inputtypehandler = value

    @property
    def lastrowid(self) -> str:
        self._verify_open()
        lastrowid = self._cyobj.get_lastrowid()
        return int(lastrowid) if lastrowid else None

    @property
    def outputtypehandler(self) -> Callable:
        self._verify_open()
        return self._cyobj.outputtypehandler

    @outputtypehandler.setter
    def outputtypehandler(self, value: Callable) -> None:
        self._verify_open()
        self._cyobj.outputtypehandler = value

    @property
    def prefetchrows(self) -> int:
        self._verify_open()
        return self._cyobj.prefetchrows

    @prefetchrows.setter
    def prefetchrows(self, value: int) -> None:
        self._verify_open()
        self._cyobj.prefetchrows = value


    @property
    def rowcount(self) -> int:
        if self._cyobj is not None and self.connection._cyobj is not None:
            return self._cyobj.rowcount
        return -1

    @property
    def rowfactory(self) -> Callable:
        self._verify_open()
        return self._cyobj.rowfactory

    @rowfactory.setter
    def rowfactory(self, value: Callable) -> None:
        self._verify_open()
        self._cyobj.rowfactory = value

    @property
    def scrollable(self) -> bool:
        self._verify_open()
        return False
    
    @property
    def statement(self) -> Union[str, None]:
        if self._cyobj is not None:
            return self._cyobj.statement

    @property
    def warning(self) -> Union[errors.ErrorWrapper, None]:
        self._verify_open()
        return self._cyobj.warning


class AsyncCursor(Cursor):
    __module__ = MODULE_NAME

    def __init__(self, connection) -> None:
        super().__init__(connection)
        if getattr(connection, "_loop", None):
            self._loop = connection._loop
        else:
            self._loop = get_event_loop()

    async def __aenter__(self):
        self._verify_open()
        return self

    async def __aexit__(self, *exc_info):
        self._verify_open()
        await self._loop.run_in_executor(None, self._cyobj.close, True)
        self._cyobj = None

    def __aiter__(self):
        return self

    async def __anext__(self):
        self._verify_fetch()
        row = await self._loop.run_in_executor(None, self._cyobj.fetch_next_row, self)
        if row is not None:
            return row
        raise StopAsyncIteration
        
    async def _call(
        self,
        name: str,
        parameters: Union[list, tuple],
        keyword_parameters: dict,
        return_value: Any = None,
    ) -> None:
        self._check_proc_args(parameters, keyword_parameters)
        self._verify_open()
        statement, bind_values = self._call_get_execute_args(
            name, parameters, keyword_parameters, return_value
        )
        return await self.execute(statement, bind_values)  
    
    async def _prepare_for_execute(
        self, statement, parameters, keyword_parameters=None
    ):
        self._verify_open()
        await self._loop.run_in_executor(None,  self._cyobj._prepare_for_execute,
            self, statement, parameters, keyword_parameters
        )
    
    async def callproc(
        self,
        name: str,
        parameters: Union[list, tuple] = None,
        keyword_parameters: dict = None,
        *,
        keywordParameters: dict = None,
    ) -> list:
        if keywordParameters is not None:
            if keyword_parameters is not None:
                errors.raise_error(
                    errors.ERR_DUPLICATED_PARAMETER,
                    deprecated_name="keywordParameters",
                    new_name="keyword_parameters",
                )
            keyword_parameters = keywordParameters
        await self._call(name, parameters, keyword_parameters)
        if parameters is None:
            return []
        return [
            v.get_value(0) for v in self._cyobj.bind_vars[: len(parameters)]
        ]

    async def execute(
        self,
        statement: Union[str, None],
        parameters: Union[list, tuple, dict] = None,
        **keyword_parameters: Any,
    ) -> Any:
        await self._prepare_for_execute(statement, parameters, keyword_parameters)
        impl = self._cyobj
        await self._loop.run_in_executor(None, impl.execute, self)
        if impl.fetch_vars is not None:
            return self

    async def executemany(
        self,
        statement: Union[str, None],
        parameters: Union[list, int],
        batcherrors: bool = False,
        arraydmlrowcounts: bool = False,
    ) -> None:
        self._verify_open()
        num_execs = await self._loop.run_in_executor(None, self._cyobj._prepare_for_executemany,
            self, statement, parameters
        )
        await self._loop.run_in_executor(None, self._cyobj.executemany, self, num_execs, bool(batcherrors), bool(arraydmlrowcounts))

    async def fetchall(self) -> list:
        self._verify_fetch()
        result = []
        fetch_next_row = self._cyobj.fetch_next_row
        while True:
            row = await self._loop.run_in_executor(None, fetch_next_row, self)
            if row is None:
                break
            result.append(row)
        return result

    async def fetchmany(self, size: int = None, numRows: int = None) -> list:
        self._verify_fetch()
        if size is None:
            if numRows is not None:
                size = numRows
            else:
                size = self._cyobj.arraysize
        elif numRows is not None:
            errors.raise_error(
                errors.ERR_DUPLICATED_PARAMETER,
                deprecated_name="numRows",
                new_name="size",
            )
        result = []
        fetch_next_row = self._cyobj.fetch_next_row
        while len(result) < size:
            row = await self._loop.run_in_executor(None, fetch_next_row, self)
            if row is None:
                break
            result.append(row)
        return result

    async def fetchone(self) -> Any:
        self._verify_fetch()
        row = await self._loop.run_in_executor(None, self._cyobj.fetch_next_row, self)
        return row

    async def parse(self, statement: str) -> None:
        self._verify_open()
        self._prepare(statement)
        await self._loop.run_in_executor(None, self._cyobj.parse, self)
