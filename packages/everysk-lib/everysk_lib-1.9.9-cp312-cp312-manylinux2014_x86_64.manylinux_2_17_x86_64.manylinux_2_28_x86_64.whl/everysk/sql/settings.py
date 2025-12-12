###############################################################################
#
# (C) Copyright 2025 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################

# Activate this setting to log all SQL queries
POSTGRESQL_LOG_QUERIES: bool = False

# Connection settings
POSTGRESQL_CONNECTION_DATABASE: str = None
POSTGRESQL_CONNECTION_PASSWORD: str = None
POSTGRESQL_CONNECTION_PORT: int = 5432
POSTGRESQL_CONNECTION_HOST: str = None
POSTGRESQL_CONNECTION_USER: str = None
POSTGRESQL_POOL_MAX_SIZE: int = 10
POSTGRESQL_POOL_MIN_SIZE: int = 1

# https://www.psycopg.org/psycopg3/docs/api/pool.html
# Maximum time, in seconds, that a connection can stay unused in the pool before being closed, and the pool shrunk.
# This only happens to connections more than min_size, if max_size allowed the pool to grow.
POSTGRESQL_POOL_MAX_IDLE: int = 60 * 5  # 5 minutes

# The maximum lifetime of a connection in the pool, in seconds. Connections used for longer get closed and replaced by
# a new one. The amount is reduced by a random 10% to avoid mass eviction.
POSTGRESQL_POOL_MAX_LIFETIME: int = 60 * 30  # 30 minutes

# Maximum number of requests that can be queued to the pool, after which new requests will fail.
# Raising TooManyRequests, 0 means no queue limit.
POSTGRESQL_POOL_MAX_WAITING: int = 0

# If the connections are opened on init or later.
POSTGRESQL_POOL_OPEN: bool = True

# Maximum time, in seconds, the pool will try to create a connection. If a connection attempt fails, the pool will try
# to reconnect a few times, using an exponential backoff and some random factor to avoid mass attempts.
POSTGRESQL_POOL_RECONNECT_TIMEOUT: int = 60 * 2  # 2 minutes

# The default maximum time in seconds that a client can wait to receive a connection
# from the pool (using connection() or getconn()).
POSTGRESQL_POOL_TIMEOUT: int = 30  # 30 seconds
