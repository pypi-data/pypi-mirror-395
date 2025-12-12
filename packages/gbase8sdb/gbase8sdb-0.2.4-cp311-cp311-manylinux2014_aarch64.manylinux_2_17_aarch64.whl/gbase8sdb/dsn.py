# coding: utf-8
from . import errors

def makedsn(
    server_name: str,
    db_name: str,
    host: str = None,
    port: int = None,
    protocol: str = 'onsoctcp',
    db_locale: str = 'zh_CN.57372',
    client_locale: str = 'zh_CN.57372',
    sqlmode: str = 'oracle',
    delimident: int = 1,
    **params
) -> str:
    """
    Return a string for use as the dsn parameter for connect().
    """
    dsn = f"gbase8s:GBASEDBTSERVER={server_name};DATABASE={db_name};"
    if 'sqlh_file' in params and params['sqlh_file'] is not None:
        dsn += f"SQLH_FILE={params.pop('sqlh_file')};"
    elif all((host, port, protocol)):
        dsn += f"HOST={host};SERVICE={port};PROTOCOL={protocol};"
    else:
        errors.raise_error(errors.ERR_INVALID_MAKEDSN_ARG, 
                          context_error_message="The arguments for host, port, and protocol are mandatory if you do not use the argument sqlh_file.",
                          name="host|port|protocol")
    if db_locale:
        dsn += f"DB_LOCALE={db_locale};"
    if client_locale:
        dsn += f"CLIENT_LOCALE={client_locale};"
    if sqlmode:
        dsn += f"SQLMODE={sqlmode};"
    if str(delimident) in ('1', 'y', 'Y'):
        dsn += f"DELIMIDENT=1;"
    for k, v in params.items():
        k_u = k.upper()
        if k_u not in ('GBASEDBTSERVER', 'DATABASE', 'HOST', 
                    'PORT', 'PROTOCOL', 'DB_LOCALE', 'CLIENT_LOCALE', 'SQLMODE',
                    'GCI_FACTORY', 'DELIMIDENT'):
            if v is not None:
                dsn += f"{k_u}={v};"
        else:
            errors.raise_error(errors.ERR_INVALID_MAKEDSN_ARG,
                              context_error_message=f"not supported parameter {k}",
                              name="params")
    dsn += "GCI_FACTORY=4;"
    return dsn
