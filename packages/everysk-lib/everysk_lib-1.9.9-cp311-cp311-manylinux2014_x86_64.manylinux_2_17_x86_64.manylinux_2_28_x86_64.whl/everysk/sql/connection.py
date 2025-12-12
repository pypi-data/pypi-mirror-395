###############################################################################
#
# (C) Copyright 2025 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################
from collections.abc import Callable
from contextvars import ContextVar, Token
from os import getpid
from types import TracebackType
from typing import Literal

from psycopg import Connection, OperationalError
from psycopg_pool import ConnectionPool as _ConnectionPool

from everysk.config import settings
from everysk.core.log import Logger
from everysk.core.retry import retry
from everysk.sql.row_factory import cls_row, dict_row

_CONNECTIONS: dict[str, 'ConnectionPool'] = {}
log = Logger('everysk-lib-sql-query')


def _log(message: str, extra: dict | None = None) -> None:
    if settings.POSTGRESQL_LOG_QUERIES:
        log.debug(message, extra=extra)


class ConnectionPool(_ConnectionPool):
    def __del__(self) -> None:
        # To close the connections when the pool is deleted
        # https://everysk.atlassian.net/browse/COD-8885
        try:
            return super().__del__()
        except RuntimeError:
            # The connection is already closed or discarded because we cannot join the current thread
            # RuntimeError: cannot join current thread
            pass

        return None


class Transaction:
    ## Private attributes
    _connection: Connection
    _pool: ConnectionPool
    _token: Token

    ## Public attributes
    connection: ContextVar[Connection] = ContextVar('postgresql-psqlpy-transaction', default=None)

    def __init__(self, dsn: str | None = None) -> None:
        self._pool: ConnectionPool = get_pool(dsn=dsn)

    def __enter__(self) -> None:
        self._connection = self._pool.getconn()
        self._token = self.connection.set(self._connection)

        return self

    def __exit__(
        self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: TracebackType | None
    ) -> None:
        if exc_type is None:
            self._connection.commit()
        else:
            self._connection.rollback()

        self.connection.reset(self._token)
        # Return the connection to the pool
        self._pool.putconn(self._connection)

        return False


def make_connection_dsn(
    host: str | None = None,
    port: int | None = None,
    user: str | None = None,
    password: str | None = None,
    database: str | None = None,
) -> str:
    """
    Create a PostgreSQL connection DSN from settings.
    Supports both TCP and Unix socket connections.
    If parameters are provided, they override the settings.
    """
    options: dict[str, str | int] = {
        'host': host or settings.POSTGRESQL_CONNECTION_HOST,
        'port': port or settings.POSTGRESQL_CONNECTION_PORT,
        'user': user or settings.POSTGRESQL_CONNECTION_USER,
        'password': password or settings.POSTGRESQL_CONNECTION_PASSWORD,
        'database': database or settings.POSTGRESQL_CONNECTION_DATABASE,
    }
    # Handle Unix socket connections
    if options['host'].startswith('/'):
        return 'postgresql:///{database}?host={host}&user={user}&password={password}'.format(**options)

    # Standard TCP connection
    return 'postgresql://{user}:{password}@{host}:{port}/{database}'.format(**options)


def get_pool(dsn: str | None = None, **kwargs) -> ConnectionPool:
    """
    Retrieve a database connection pool for the given DSN.

    If no DSN is provided, a default DSN is generated. The connection pool is cached
    based on the process ID and DSN hash to ensure reuse within the same process.
    If a pool for the given key does not exist, a new one is created with the specified
    maximum size and SSL mode.

    Importantly, this is necessary because connections cannot be shared between processes.

    Args:
        dsn (str | None): The Data Source Name for the database connection. If None, a default DSN is used.
        **kwargs: Additional keyword arguments to configure the connection pool.

    Returns:
        ConnectionPool: The connection pool associated with the given DSN.
    """
    dsn = dsn or make_connection_dsn()
    # https://www.psycopg.org/psycopg3/docs/api/pool.html
    kwargs['check'] = ConnectionPool.check_connection
    kwargs['min_size'] = kwargs.get('min_size', settings.POSTGRESQL_POOL_MIN_SIZE)
    kwargs['max_size'] = kwargs.get('max_size', settings.POSTGRESQL_POOL_MAX_SIZE)
    kwargs['max_idle'] = kwargs.get('max_idle', settings.POSTGRESQL_POOL_MAX_IDLE)
    kwargs['max_lifetime'] = kwargs.get('max_lifetime', settings.POSTGRESQL_POOL_MAX_LIFETIME)
    kwargs['max_waiting'] = kwargs.get('max_waiting', settings.POSTGRESQL_POOL_MAX_WAITING)
    kwargs['reconnect_timeout'] = kwargs.get('reconnect_timeout', settings.POSTGRESQL_POOL_RECONNECT_TIMEOUT)
    kwargs['timeout'] = kwargs.get('timeout', settings.POSTGRESQL_POOL_TIMEOUT)
    kwargs['open'] = kwargs.get('open', settings.POSTGRESQL_POOL_OPEN)

    key = f'{getpid()}:{hash(dsn)}'
    if key not in _CONNECTIONS:
        _CONNECTIONS[key] = ConnectionPool(conninfo=dsn, **kwargs)

    return _CONNECTIONS[key]


def execute(
    query: str,
    params: dict | None = None,
    return_type: Literal['dict', 'list'] = 'list',
    dsn: str | None = None,
    cls: type | None = None,
    loads: Callable | None = None,
) -> list[dict] | list[object] | dict | None:
    """
    Execute a query and return the results.
    If return_type is a class, return a list of instances of that class.
    If return_type is a string, return a dictionary keyed by that string.
    Otherwise, return a list of dictionaries.

    Args:
        query (str): The SQL query to execute.
        params (dict | None, optional): The parameters to include in the query. Defaults to None.
        return_type (Literal['dict', 'list'], optional): The type of return value. Defaults to 'list'.
        dsn (str | None, optional): The DSN to use for the connection. Defaults to None.
        cls (type | None, optional): The class to map the results to. Defaults to None.
        loads (Callable | None, optional): Optional function to process each value. Defaults to None.
        retry (int, optional): The current retry count. Defaults to 0.
    """
    conn: Connection = Transaction.connection.get()
    if not conn:
        pool: ConnectionPool = get_pool(dsn=dsn)
        conn: Connection = pool.getconn()
        is_transactional = False
        log_message = 'PostgreSQL query executed.'
    else:
        is_transactional = True
        log_message = 'PostgreSQL query executed within transaction.'

    _log(log_message, extra={'labels': {'query': query, 'params': params}})

    row_factory = cls_row(cls, loads) if cls else dict_row(loads)
    # For transactions we let it be controlled externally by the context manager
    try:
        with conn.cursor(row_factory=row_factory) as cur:
            result = retry(cur.execute, {'query': query, 'params': params}, retries=3, exceptions=OperationalError)

            if result.description:
                result = cur.fetchall()
            else:
                result = None
    except Exception:
        # On error we need to rollback
        if not is_transactional:
            conn.rollback()
        raise

    else:
        # Block that only executes if no exception was raised in the try block
        if not is_transactional:
            conn.commit()

    finally:
        # We only return the connection to the pool if we are not in a transaction
        if not is_transactional:
            pool.putconn(conn)

    if result and cls and return_type == 'dict':
        return {row[cls._primary_key]: row for row in result}

    return result
