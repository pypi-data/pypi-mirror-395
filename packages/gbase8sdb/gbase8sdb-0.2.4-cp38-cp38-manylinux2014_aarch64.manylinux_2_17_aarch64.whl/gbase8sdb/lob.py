# coding: utf-8

from typing import Any, Union


from . import __name__ as MODULE_NAME
from . import errors
from .driver import DB_TYPE_BLOB
import asyncio



class LOB:
    __module__ = MODULE_NAME
    
    def __str__(self):        
        return str(self.read())

    def __del__(self):
        self._cyobj.free_lob()

    def __reduce__(self):
        value = self.read()
        return (type(value), (value,))

    
    @classmethod
    def _create_with_cyobj(cls, cyobj):
        lob = cls.__new__(cls)
        lob._cyobj = cyobj
        lob.encoding = cyobj.client_locale
        return lob

    def _check_value_to_write(self, value):
        if isinstance(value, bytes):
            if self.type is DB_TYPE_BLOB:
                return value
            else:
                return value.decode(self.encoding)
        elif isinstance(value, str):
            if self.type is DB_TYPE_BLOB:
                return value.encode(self.encoding)
            else:
                return value
        else:
            raise TypeError("expecting string or bytes")        

    def close(self):
        self._cyobj.close()

    def getchunksize(self):
        return self._cyobj.get_chunk_size()

    def isopen(self):
        return self._cyobj.get_is_open()

    def open(self):
        self._cyobj.open()

    def read(self, offset: int = 1, amount: int = None):
        if amount is None:
            amount = self._cyobj.get_max_amount()
            if amount >= offset:
                amount = amount - offset + 1
            else:
                amount = 1
        elif amount <= 0:
            errors.raise_error(errors.ERR_INVALID_LOB_AMOUNT)
        if offset <= 0:
            errors.raise_error(errors.ERR_INVALID_LOB_OFFSET)
        return self._cyobj.read(offset, amount)

    def size(self):
        return self._cyobj.get_size()

    def trim(self, new_size: int = 0, *, newSize: int = None):
        if newSize is not None:
            if new_size != 0:
                errors.raise_error(
                    errors.ERR_DUPLICATED_PARAMETER,
                    deprecated_name="newSize",
                    new_name="new_size",
                )
            new_size = newSize
        self._cyobj.trim(new_size)

    def write(self, data: Union[str, bytes], offset: int = 1):
        self._cyobj.write(self._check_value_to_write(data), offset)

    @property
    def type(self):
        return self._cyobj.dbtype

class AsyncLOB(LOB):
    __module__ = MODULE_NAME 

    @classmethod
    def _create_with_cyobj(cls, cyobj):
        lob = cls.__new__(cls)
        # lob._loop = asyncio.get_event_loop()
        # try:
        #     lob._loop = asyncio.get_running_loop()
        # except RuntimeError:
        #     return asyncio.get_event_loop_policy().get_event_loop()
        lob._cyobj = cyobj
        lob.encoding = cyobj.client_locale
        return lob


    async def close(self):
        await self._loop.run_in_executor(None, self._cyobj.close)

    async def getchunksize(self):
        return await self._loop.run_in_executor(None, self._cyobj.get_chunk_size)

    async def isopen(self):
        return await self._loop.run_in_executor(None, self._cyobj.get_is_open)

    async def open(self):
        await self._loop.run_in_executor(None, self._cyobj.open)

    async def read(self, offset: int = 1, amount: int = None):
        if amount is None:
            amount = self._cyobj.get_max_amount()
            if amount >= offset:
                amount = amount - offset + 1
            else:
                amount = 1
        elif amount <= 0:
            errors.raise_error(errors.ERR_INVALID_LOB_AMOUNT)
        if offset <= 0:
            errors.raise_error(errors.ERR_INVALID_LOB_OFFSET)
        return await self._loop.run_in_executor(None, self._cyobj.read, offset, amount)

    async def size(self):
        return await self._loop.run_in_executor(None, self._cyobj.get_size)

    async def trim(self, new_size: int = 0, *, newSize: int = None):
        if newSize is not None:
            if new_size != 0:
                errors.raise_error(
                    errors.ERR_DUPLICATED_PARAMETER,
                    deprecated_name="newSize",
                    new_name="new_size",
                )
            new_size = newSize
        await self._loop.run_in_executor(None, self._cyobj.trim, new_size)

    async def write(self, data: Union[str, bytes], offset: int = 1):
        await self._loop.run_in_executor(None, self._cyobj.write, self._check_value_to_write(data), offset)
