###############################################################################
#
# (C) Copyright 2025 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################
import hashlib
from functools import partial

from psycopg.types.json import Jsonb, set_json_dumps, set_json_loads

from everysk.core.object import BaseDict
from everysk.core.serialize import dumps, loads
from everysk.sql.utils import ConditionOperator

# https://www.psycopg.org/psycopg3/docs/basic/adapt.html#json-adaptation
set_json_dumps(
    partial(
        dumps,
        add_class_path=True,
        date_format='%Y-%m-%d',
        datetime_format='%Y-%m-%dT%H:%M:%S',
        indent=None,
        separators=(',', ':'),
        use_undefined=True,
    )
)
set_json_loads(partial(loads, use_undefined=True, instantiate_object=True))


## Constants
_SQL_FIELDS = {
    'bool': 'BOOLEAN',
    'bytes': 'BYTEA',
    'date': 'DATE',
    'Date': 'DATE',
    'datetime': 'TIMESTAMPTZ',
    'DateTime': 'TIMESTAMPTZ',
    'dict': 'JSONB',
    'float': 'FLOAT',
    'int': 'INTEGER',
    'list': 'JSONB',
    'set': 'JSONB',
    'str': 'TEXT',
    'tuple': 'JSONB',
}
_SQL_ORDER_BY = {'asc': 'ASC NULLS LAST', 'desc': 'DESC NULLS LAST'}

# SQL queries constants

# Create new schema
_SQL_CREATE_SCHEMA = 'CREATE SCHEMA IF NOT EXISTS "{schema}"'

## Use {name} when you need to replace a value in the query using the format method.
## Use %(name)s when you need to replace a value in the query using the execute method.
_SQL_CREATE_TABLE = 'CREATE TABLE IF NOT EXISTS "{schema}"."{table}" ({fields})'

# https://www.postgresqltutorial.com/postgresql-delete/
_SQL_DELETE = 'DELETE FROM "{schema}"."{table}" WHERE "{primary_key}" = ANY(%(ids)s)'

# https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-upsert/
# https://stackoverflow.com/a/30917361
_SQL_INSERT_OR_UPDATE = (
    'INSERT INTO "{schema}"."{table}" ({fields}) VALUES ({values}) ON CONFLICT ({primary_key}) DO UPDATE SET {update}'
)

# create index
_SQL_INDEX = (
    'CREATE INDEX IF NOT EXISTS "index_{table_name}_{index_name}_btree" ON "{schema}"."{table_name}" '
    "USING btree ({fields} NULLS LAST) WITH (deduplicate_items='true')"
)

# https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-select/
_SQL_SELECT = 'SELECT {fields} FROM "{schema}"."{table}" {group_by} ORDER BY {order_by} {limit} {offset}'
_SQL_SELECT_WHERE = (
    'SELECT {fields} FROM "{schema}"."{table}" {conditions} {group_by} ORDER BY {order_by} {limit} {offset}'
)

# set field to not null
_SQL_SET_NOT_NULL = 'ALTER TABLE IF EXISTS "{schema}"."{table}" ALTER COLUMN "{field}" SET NOT NULL'


class Query:
    ## Public attributes
    primary_key: str = None
    schema: str = None
    table_name: str = None

    def __init__(self, table_name: str, primary_key: str, schema: str | None = None) -> None:
        # Default schema is public
        if not schema:
            schema = 'public'

        self.primary_key = primary_key
        self.schema = schema
        self.table_name = table_name

    ## Private methods
    def _sql_conditions(self, conditions: dict) -> tuple[str | None, dict]:
        """
        Generate the SQL conditions and parameters from the given conditions.
        Conditions are provided as a dictionary where the key is the field operator
        and the value is the value to compare against. Ex: {'age__gt': 30, 'name__eq': 'John'}

        Args:
            conditions (dict): A dictionary of field operators and their values.
        """
        result = []
        params = {}
        for field_operator, value in conditions.items():
            sql, param = ConditionOperator(field_operator=field_operator, value=value).get_sql()
            result.append(sql)
            if param is not None:
                params[field_operator] = param

        if result:
            sql = 'WHERE {conditions}'.format(conditions=' AND '.join(result))
        else:
            sql = None

        return sql, params

    def _sql_group_by(self, group_by: list[str] | None) -> str:
        """
        Constructs a SQL GROUP BY clause from the provided fields.

        Args:
            group_by (set | list[str] | None): A set or list of field names to group by, or None.

        Returns:
            str: A SQL GROUP BY clause string if fields are provided, otherwise an empty string.
        """
        if not group_by:
            return ''

        return 'GROUP BY {}'.format(', '.join(f'"{field}"' for field in group_by))

    def _sql_order_by(self, order_by: str | list[str]) -> str:
        """
        Generate the SQL order by clause from the given order by string.
        The order by string can be in the format 'field__operator' where operator
        can be 'asc' or 'desc'. If no operator is provided, 'asc' is used by default.

        Args:
            order_by (str): The order by string.

        Raises:
            ValueError: If the order by operator is invalid.
        """
        if not order_by:
            order_by = [f'{self.primary_key}__asc']

        if isinstance(order_by, str):
            order_by = [order.strip() for order in order_by.split(',')]

        result = []
        for order in order_by:
            if '__' in order:
                field, operator = order.split('__')

            else:
                field, operator = order, 'asc'

            try:
                operator = _SQL_ORDER_BY[operator]
            except KeyError as error:
                msg = f'Invalid order_by operator: {operator}.'
                raise ValueError(msg) from error
            result.append(f'"{field}" {operator}')

        return ', '.join(result)

    def _sql_limit(self, limit: int | str | None) -> str | None:
        """
        Generate the SQL limit clause from the given limit value.
        If limit is '*', no limit is applied. If limit is None or invalid, a default
        limit of 10 is applied.

        Args:
            limit (int | str): The limit value.

        Raises:
            TypeError: If the limit is not an integer or "*".
        """
        if limit == '*':
            return ''

        if limit is None:
            limit = 10

        if not isinstance(limit, int):
            msg = 'Limit must be an integer or "*".'
            raise TypeError(msg)

        if limit <= 0:
            limit = 10

        return f'LIMIT {limit}'

    def _sql_offset(self, offset: int | str | None) -> str:
        """
        Generates an SQL OFFSET clause using the provided offset value.

        Args:
            offset (int | str | None): The offset value to be used in the SQL query. Must be convertible to an integer.

        Returns:
            str: A string representing the SQL OFFSET clause.

        Raises:
            TypeError: If the offset is not an integer or cannot be converted to an integer.
        """
        if offset is None:
            return ''

        try:
            offset = int(offset)
        except (ValueError, TypeError) as error:
            msg = 'Offset must be an integer or a string representing it.'
            raise TypeError(msg) from error

        if offset < 0:
            msg = 'Offset must not be negative.'
            raise TypeError(msg)

        if offset == 0:
            return ''

        return f'OFFSET {offset}'

    ## Public methods
    def parse_create_schema(self) -> str:
        """
        Generates a SQL statement to create a schema using the current schema name.

        Returns:
            str: A formatted SQL string for creating the schema.
        """
        return _SQL_CREATE_SCHEMA.format(schema=self.schema)

    def parse_create_table(self, fields: dict[str, type]) -> str:
        """
        Generate the SQL create table query from the given fields.
        The fields are provided as a dictionary where the key is the field name
        and the value is the field type.

        Args:
            fields (dict[str, type]): A dictionary of field names and their types.
        """
        sql_fields = []
        for field, attr_type in fields.items():
            name = getattr(attr_type, '__name__', getattr(attr_type.__class__, '__name__', str(attr_type))).lower()
            sql_type = _SQL_FIELDS.get(name, 'TEXT')
            if field == self.primary_key:
                # Primary key should be unique and not null
                sql_type = f'{sql_type} PRIMARY KEY NOT NULL'

            sql_fields.append(f'"{field}" {sql_type}')

        fields = ', '.join(sql_fields)
        return _SQL_CREATE_TABLE.format(schema=self.schema, table=self.table_name, fields=fields)

    def parse_delete(self) -> str:
        """
        Generate the SQL delete query.
        Deletes rows based on the primary key.
        """
        return _SQL_DELETE.format(schema=self.schema, table=self.table_name, primary_key=self.primary_key)

    def parse_set_not_null(self, field: str) -> str:
        """
        Generates an SQL statement to set the specified field as NOT NULL.

        Args:
            field (str): The name of the field to modify.

        Returns:
            str: The formatted SQL statement to set the field as NOT NULL.
        """
        return _SQL_SET_NOT_NULL.format(schema=self.schema, table=self.table_name, field=field)

    def parse_index(self, fields: str, index_name: str | None = None) -> str:
        """
        Generates an SQL index creation statement for the specified fields and index name.

        Args:
            fields (str): A comma-separated string of field names to include in the index.
            index_name (str | None, optional): The name of the index. If None, a deterministic index name
                is generated based on the sorted field names.

        Returns:
            str: The formatted SQL statement for creating the index.
        """
        table_index_name: str = index_name

        if table_index_name is None:
            # Generate a eight-character deterministic index name based on the sorted field names
            fields_names: list = [x.strip().split(' ')[0].strip().lower() for x in fields.split(',')]
            fields_names.sort()
            table_index_name = hashlib.sha256('__'.join(fields_names).encode()).hexdigest()[:8]

        return _SQL_INDEX.format(
            schema=self.schema, table_name=self.table_name, fields=fields.strip(), index_name=table_index_name
        )

    def parse_insert_or_update(self, fields: set | list) -> str:
        """
        Generate the SQL insert or update query from the given fields.

        Args:
            fields (set | list): A set or list of field names to include in the query.
        """
        # Create the values string
        # We do not use " here because we are using the values as placeholders
        values = ', '.join(f'%({field})s' for field in fields)

        # Create the SQL query
        update = ', '.join(f'"{field}" = EXCLUDED."{field}"' for field in fields)
        fields = ', '.join([f'"{field}"' for field in fields])

        return _SQL_INSERT_OR_UPDATE.format(
            schema=self.schema,
            fields=fields,
            table=self.table_name,
            values=values,
            primary_key=self.primary_key,
            update=update,
        )

    def parse_insert_or_update_params(self, params: dict) -> dict:
        """
        Prepare the parameters for the insert or update query.
        This method ensures that lists, sets, and tuples are converted to JSONB
        and strings are converted to TEXT for proper handling by PostgreSQL.

        Args:
            params (dict): A dictionary of parameters to prepare.
        """
        # https://www.psycopg.org/psycopg3/docs/basic/adapt.html#json-adaptation
        for key, value in params.items():
            if isinstance(value, (set, tuple)):
                params[key] = Jsonb(list(value))
            elif isinstance(value, (dict, list)):
                params[key] = Jsonb(value)
            elif isinstance(value, BaseDict):
                params[key] = Jsonb(value.to_dict())

        return params

    def parse_select(
        self,
        fields: set | list,
        limit: int | str | None = None,
        offset: int | str | None = None,
        conditions: dict | None = None,
        group_by: list | None = None,
        order_by: str | list | None = None,
    ) -> tuple[str, dict]:
        """
        Constructs a SQL SELECT query string with optional WHERE, GROUP BY, ORDER BY, LIMIT, and OFFSET clauses.

        Args:
            fields (set | list): The fields/columns to select in the query.
            limit (int | str | None, optional): The maximum number of rows to return.
            offset (int | str | None, optional): The number of rows to skip before starting to return rows.
            conditions (dict | None, optional): Conditions for the WHERE clause.
            group_by (list | None, optional): Fields to group the results by.
            order_by (str | list | None, optional): Fields to order the results by.

        Returns:
            tuple[str, dict]: A tuple containing the SQL query string and a dictionary of parameters for the query.
        """
        params = {
            'schema': self.schema,
            # TODO: treat specials like sum, count, avg, round, etc.
            'fields': ', '.join([f'"{field}"' for field in fields]),
            'table': self.table_name,
            'limit': self._sql_limit(limit),
            'offset': self._sql_offset(offset),
            'group_by': self._sql_group_by(group_by),
            'order_by': self._sql_order_by(order_by),
        }

        sql_params = {}
        if conditions:
            where, sql_params = self._sql_conditions(conditions)
            params['conditions'] = where
            return ' '.join(_SQL_SELECT_WHERE.format(**params).split()), sql_params

        return ' '.join(_SQL_SELECT.format(**params).split()), sql_params
