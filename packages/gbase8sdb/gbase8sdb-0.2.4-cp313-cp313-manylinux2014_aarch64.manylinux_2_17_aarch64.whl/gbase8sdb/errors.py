# coding: utf-8

import re
from . import exceptions

ERR_EXCEPTION_TYPES = {
    1: exceptions.InterfaceError,
    2: exceptions.ProgrammingError,
    3: exceptions.NotSupportedError,
    4: exceptions.DatabaseError,
    5: exceptions.InternalError,
    6: exceptions.OperationalError,
    7: exceptions.Warning,
}

# dbapi error code in InterfaceError
ERR_MISSING_ERROR = 1000
ERR_NOT_CONNECTED = 1001
ERR_NOT_A_QUERY = 1002
ERR_CURSOR_NOT_OPEN = 1003

# dbapi error code in ProgrammingError
ERR_NO_STATEMENT = 2001
ERR_NO_STATEMENT_PREPARED = 2002
ERR_WRONG_EXECUTE_PARAMETERS_TYPE = 2003
ERR_WRONG_EXECUTEMANY_PARAMETERS_TYPE = 2004
ERR_ARGS_AND_KEYWORD_ARGS = 2005
ERR_MIXED_POSITIONAL_AND_NAMED_BINDS = 2006
ERR_EXPECTING_TYPE = 2007
ERR_MIXED_ELEMENT_TYPES = 2008
ERR_WRONG_ARRAY_DEFINITION = 2009
ERR_ARGS_MUST_BE_LIST_OR_TUPLE = 2010
ERR_KEYWORD_ARGS_MUST_BE_DICT = 2011
ERR_DUPLICATED_PARAMETER = 2012
ERR_EXPECTING_VAR = 2013
ERR_INCORRECT_VAR_ARRAYSIZE = 2014
ERR_INVALID_MAKEDSN_ARG = 2015
ERR_INIT_GBASE8S_CLIENT_NOT_CALLED = 2016
ERR_INVALID_GCI_ATTR_TYPE = 2017
ERR_INVALID_CONNECT_PARAMS = 2018
ERR_EXPECTING_LIST_FOR_ARRAY_VAR = 2019
ERR_INVALID_LOB_OFFSET = 2020
ERR_INVALID_ARRAYSIZE = 2021
ERR_INVALID_LOB_AMOUNT = 2022
ERR_INVALID_ARGS = 2023

# dbapi error code in NotSupportedError
ERR_TIME_NOT_SUPPORTED = 3000
ERR_PYTHON_VALUE_NOT_SUPPORTED = 3001
ERR_PYTHON_TYPE_NOT_SUPPORTED = 3002
ERR_UNSUPPORTED_TYPE_SET = 3003
ERR_ARRAYS_OF_ARRAYS = 3004
ERR_GBASE8S_TYPE_NOT_SUPPORTED = 3005
ERR_DB_TYPE_NOT_SUPPORTED = 3006
ERR_SELF_BIND_NOT_SUPPORTED = 3007
ERR_UNSUPPORTED_PYTHON_TYPE_FOR_DB_TYPE = 3008
ERR_LOB_OF_WRONG_TYPE = 3009
ERR_GBASE8S_TYPE_NAME_NOT_SUPPORTED = 3010
ERR_NAMED_TIMEZONE_NOT_SUPPORTED = 3011
ERR_CURSOR_DIFF_CONNECTION = 3012


# dbapi error code in DatabaseError
ERR_GBASE8S_NUMBER_NO_REPR = 4000
ERR_INVALID_NUMBER = 4001
ERR_NUMBER_WITH_INVALID_EXPONENT = 4002
ERR_NUMBER_STRING_OF_ZERO_LENGTH = 4003
ERR_NUMBER_STRING_TOO_LONG = 4004
ERR_NUMBER_WITH_EMPTY_EXPONENT = 4005
ERR_CONTENT_INVALID_AFTER_NUMBER = 4006


# error code in InternalError
ERR_BUFFER_LENGTH_INSUFFICIENT = 5001
ERR_INTEGER_TOO_LARGE = 5002
ERR_UNEXPECTED_NEGATIVE_INTEGER = 5003
ERR_UNEXPECTED_END_OF_DATA = 5004


class ErrorWrapper:
    regex_server_error = re.compile("ERROR:\s+\-(?P<code>[0-9]+):\s+.*")
    regex_gci_error = re.compile("ERROR:\[GCI\]\s+.*")

    def __init__(
        self,
        message: str = None,
        context: str = None,
        isrecoverable: bool = False,
        iswarning: bool = False,
        code: int = 0,
        offset: int = 0,
    ) -> None:      
        self.exc_type = exceptions.DatabaseError
        self.is_session_dead = False
        self.offset = offset
        self.code = code
        self.full_code = ""
        self.iswarning = iswarning
        self.isrecoverable = isrecoverable
        self.context = context
        self.message = message
        self._wrapper_error()

    def _wrapper_error(self):
        if self.message is not None:
            if not self.message.startswith("ERROR"):    # GDPI ERROR
                pos = self.message.find(":")
                if pos > 0:
                    self.full_code = self.message[:pos]
            else:
                match = self.regex_server_error.match(self.message)
                if match is not None:                  #   Gbase8s error
                    self.code = int(match.group("code"))
                    self.full_code = f"GBA-{self.code}"
                else:                                   #   GCI error
                    match = self.regex_gci_error.match(self.message)
                    if match is not None:
                        self.full_code = f"GCI-{self.code}"

        if self.full_code.startswith("DBAPI-"):
            driver_error_num = int(self.full_code[6:])
            self.exc_type = ERR_EXCEPTION_TYPES[driver_error_num // 1000]
        elif self.full_code.startswith("GCI-"): # GCI error as InterfaceError
            self.exc_type = exceptions.InterfaceError
        elif self.code != 0:
            if self.code in ERR_INTEGRITY_ERROR_CODES:
                self.exc_type = exceptions.IntegrityError
            elif self.code in ERR_PROGRAMMING_ERROR_CODES:
                self.exc_type = exceptions.ProgrammingError
            elif self.code in ERR_DATA_ERROR_CODES:
                self.exc_type = exceptions.DataError


    def __str__(self):
        return self.message


# error raise by gbase8sdb
ERROR_TYPE = "DBAPI"

def _get_whole_error(code: int, **kwargs) -> str:
    msg_map = ERROR_MSG_MAPPING.get(code, None)
    if not msg_map:
        msg_map = f"not found error code: {code}."
        kwargs = {}
        code = ERR_MISSING_ERROR
    try:
        whole_msg = msg_map.format(**kwargs)
    except KeyError:
        whole_msg = msg_map + "\nformat error with :\n" + str(kwargs)
    return f"{ERROR_TYPE}-{code:04}: {whole_msg}"


def _create_error_wrapper(code: int, context_error_message: str = None, cause: Exception = None, **args) -> ErrorWrapper:
    message = _get_whole_error(code, **args)
    if context_error_message is None and cause is not None:
        context_error_message = str(cause)
    if context_error_message is not None:
        message = f"{message}\n{context_error_message}"
    return ErrorWrapper(message)


def raise_error(error_num: int, context_error_message: str = None, cause: Exception = None, **args) -> None:
    error = _create_error_wrapper(error_num, context_error_message, cause, **args)
    raise error.exc_type(error) from cause



# GBA codes in IntegrityError
ERR_INTEGRITY_ERROR_CODES = [
    268,  # unique constraint violated
    391,  # cannot insert NULL
    530,  # check constraint violated
    691,  # referential constraint
    703,  # Primary key on table has a field with a null key value
]
# GBA codes in ProgrammingError
ERR_PROGRAMMING_ERROR_CODES = [
    206,  # table not found
    310,  # table already exists
    201,  # syntax error 
]

# GBA codes in DataError
ERR_DATA_ERROR_CODES = [
    1202,  # divide by zero.
]


# mapping error code and error message
ERROR_MSG_MAPPING = {
    ERR_KEYWORD_ARGS_MUST_BE_DICT: (
        '<keyword_parameters> must be dict'
    ),
    ERR_LOB_OF_WRONG_TYPE: (
        "LOB must be type {expected_type_name}, not type {actual_type_name}"
    ),
    ERR_MIXED_ELEMENT_TYPES: (
        "The element {element} does not match the data type of the preceding elements."
    ),
    ERR_MIXED_POSITIONAL_AND_NAMED_BINDS: (
        "Positional and named bindings are not allowed to be used together"
    ),
    ERR_NAMED_TIMEZONE_NOT_SUPPORTED: (
        "Other modes are incompatible with the use of named time zones"
    ),
    ERR_NO_STATEMENT: (
        "Neither a statement is specified nor a prior one prepared"
    ),
    ERR_NO_STATEMENT_PREPARED: (
        "statement should be prepared in advance"
    ),
    ERR_NOT_A_QUERY: (
        "No rows are returned by the executed statement"
    ),
    ERR_NOT_CONNECTED: (
        "The database connection is not established"
    ),
    ERR_NUMBER_STRING_OF_ZERO_LENGTH: "invalid number: zero length string",
    ERR_NUMBER_STRING_TOO_LONG: "invalid number: string too long",
    ERR_NUMBER_WITH_EMPTY_EXPONENT: "invalid number: empty exponent",
    ERR_NUMBER_WITH_INVALID_EXPONENT: "invalid number: invalid exponent",
    ERR_GBASE8S_NUMBER_NO_REPR: (
        "The value is incapable of being expressed as a Gbase8s number"
        ),
    ERR_GBASE8S_TYPE_NAME_NOT_SUPPORTED: 'not support Gbase8s data type name "{name}"',
    ERR_GBASE8S_TYPE_NOT_SUPPORTED: "not support Gbase8s data type {num}",
    ERR_PYTHON_TYPE_NOT_SUPPORTED: "not support Python type {typ}",
    ERR_PYTHON_VALUE_NOT_SUPPORTED: 'not support Python value of type "{type_name}"',
    ERR_SELF_BIND_NOT_SUPPORTED: "binding to self is not supported",
    ERR_TIME_NOT_SUPPORTED: (
        "Gbase8s Database does not support time only variables"
    ),
    ERR_UNEXPECTED_END_OF_DATA: (
        "unexpected end of data: want {num_bytes_wanted} bytes but "
        "only {num_bytes_available} bytes are available"
    ),
    ERR_UNEXPECTED_NEGATIVE_INTEGER: (
       "Internal error: a negative integer was read, "
       "but a positive integer was anticipated"
    ),
    ERR_UNSUPPORTED_PYTHON_TYPE_FOR_DB_TYPE: (
        "unsupported Python type {py_type_name} for database type "
        "{db_type_name}"
    ),
    ERR_UNSUPPORTED_TYPE_SET: "type {db_type_name} does not support being set",
    ERR_WRONG_ARRAY_DEFINITION: (
        "expecting a list of two elements [type, numelems]"
    ),
    ERR_WRONG_EXECUTE_PARAMETERS_TYPE: (
        "expecting a dictionary, list or tuple, or keyword args"
    ),
    ERR_WRONG_EXECUTEMANY_PARAMETERS_TYPE: (
        'For the "parameters" argument, a list of sequences '
        'or dictionaries is expected, '
        "or alternatively, an integer to denote the execution count of the statement"
    ), 
    ERR_INVALID_GCI_ATTR_TYPE: "invalid GCI attribute type {attr_type}",
    ERR_INVALID_NUMBER: "invalid number",
    ERR_INVALID_MAKEDSN_ARG: '"{name}" argument contains invalid values',
    ERR_INVALID_LOB_OFFSET: "LOB offset must be greater than zero",
    ERR_INVALID_LOB_AMOUNT: "LOB amount must be greater than zero",
    ERR_INVALID_CONNECT_PARAMS: "invalid connection params",
    ERR_INVALID_ARRAYSIZE: "arraysize must be an integer greater than zero",
    ERR_INTEGER_TOO_LARGE: (
        "internal error: read integer of length {length} when expecting "
        "integer of no more than length {max_length}"
    ),   
    ERR_INIT_GBASE8S_CLIENT_NOT_CALLED: (
        "init_gbase8s_client() must be called first"
    ),
    ERR_INCORRECT_VAR_ARRAYSIZE: (
        "variable array size of {var_arraysize} is "
        "too small (should be at least {required_arraysize})"
    ),
    ERR_EXPECTING_VAR: (
        "type handler should return None or the value returned by a call "
        "to cursor.var()"
    ),
    ERR_EXPECTING_TYPE: "expected a type",
    ERR_EXPECTING_LIST_FOR_ARRAY_VAR: (
        "expecting list when setting array variables"
    ),  
    ERR_DUPLICATED_PARAMETER: (
        '"{deprecated_name}" and "{new_name}" cannot be specified together'
    ),
    ERR_DB_TYPE_NOT_SUPPORTED: 'database type "{name}" is not supported',
    ERR_CURSOR_NOT_OPEN: "cursor is not open",
    ERR_CURSOR_DIFF_CONNECTION: (
        "It is not supported to bind a cursor from a different connection."
    ),
    ERR_CONTENT_INVALID_AFTER_NUMBER: "invalid number (content after number)",   
    ERR_BUFFER_LENGTH_INSUFFICIENT: (
        "internal error: buffer of length {actual_buffer_len} "
        "insufficient to hold {required_buffer_len} bytes"
    ),
    ERR_ARRAYS_OF_ARRAYS: "arrays of arrays are not supported",
    ERR_ARGS_AND_KEYWORD_ARGS: (
        "expecting positional arguments or keyword arguments, not both"
    ),
    ERR_ARGS_MUST_BE_LIST_OR_TUPLE: "arguments must be a list or tuple",
    ERR_INVALID_ARGS: "Invalid arguments", 
}
