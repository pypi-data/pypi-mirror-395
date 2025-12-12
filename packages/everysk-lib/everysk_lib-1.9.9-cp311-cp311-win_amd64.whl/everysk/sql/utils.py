###############################################################################
#
# (C) Copyright 2025 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################
from typing import Any

_SQL_OPERATORS = {
    'endswith': 'LIKE',
    'eq': '=',
    'gt': '>',
    'gte': '>=',
    'ilike': 'ILIKE',
    'in': 'IN',
    'inside': '?',
    'insidebinary': '?|',
    'isnotnull': 'IS NOT NULL',
    'isnull': 'IS NULL',
    'like': 'LIKE',
    'lt': '<',
    'lte': '<=',
    'ne': '!=',
    'nin': 'NOT IN',
    'startswith': 'LIKE',
}


class ConditionOperator:
    ## Public attributes
    field_operator: str = None
    field: str = None
    operator: str = None
    sql_operator: str = None
    value: Any = None

    ## Internal methods
    def __init__(self, *, field_operator: str, value: Any) -> None:
        self.field_operator = field_operator
        self.value = value

        if '__' in self.field_operator:
            self.field, self.operator = field_operator.split('__', 1)
        else:
            self.field, self.operator = field_operator, 'eq'

        # To adjust when used field__isnull = False
        if self.operator == 'isnull' and not value:
            self.operator = 'isnotnull'

        try:
            self.sql_operator = _SQL_OPERATORS[self.operator]
        except KeyError as error:
            msg = f'Invalid field({self.field}) operator: {self.operator}.'
            raise ValueError(msg) from error

    ## Operators methods
    def _operator_default(self) -> tuple[str, Any]:
        """Default operator method "field" <operator> %(field)s."""
        operation = f'{self.sql_operator} %({self.field_operator})s'
        sql = f'"{self.field}" {operation}'
        return sql, self.value

    def _operator_endswith(self) -> tuple[str, str]:
        """Operator method for endswith: "field" LIKE %value."""
        sql, value = self._operator_default()
        return sql, f'%{value}'

    def _operator_in(self) -> tuple[str, list]:
        """Operator method for in: "field" = ANY(%(field__in)s)."""
        # https://www.psycopg.org/psycopg3/docs/basic/from_pg2.html#you-cannot-use-in-s-with-a-tuple
        operation = f'ANY(%({self.field_operator})s)'
        sql = f'"{self.field}" = {operation}'
        if isinstance(self.value, str):
            return sql, self.value.split(',')

        return sql, self.value

    def _operator_isnotnull(self) -> tuple[str, None]:
        """Operator method for isnotnull: "field" IS NOT NULL."""
        sql = f'"{self.field}" IS NOT NULL'
        return sql, None

    def _operator_isnull(self) -> tuple[str, None]:
        """Operator method for isnull: "field" IS NULL."""
        sql = f'"{self.field}" IS NULL'
        return sql, None

    def _operator_like(self) -> tuple[str, str]:
        """Operator method for like: "field" LIKE %value%."""
        sql, value = self._operator_default()
        return sql, f'%{value}%'

    def _operator_ilike(self) -> tuple[str, str]:
        """Operator method for ilike: "field" ILIKE %value%."""
        return self._operator_like()

    def _operator_nin(self) -> tuple[str, list]:
        """Operator method for nin: "field" != ALL(%(field__nin)s)."""
        operation = f'ALL(%({self.field_operator})s)'
        sql = f'"{self.field}" != {operation}'
        if isinstance(self.value, str):
            return sql, self.value.split(',')

        return sql, self.value

    def _operator_startswith(self) -> tuple[str, str]:
        """Operator method for startswith: "field" LIKE value%."""
        sql, value = self._operator_default()
        return sql, f'{value}%'

    ## Public methods
    def get_sql(self) -> tuple[str, Any]:
        """
        Get the SQL representation of the field and operator.

        Example:
            field__operator = 'age__gt'
            value = 30
            returns: ('"age" > %(age__gt)s', 30)
        """
        method_name = f'_operator_{self.operator}'
        if hasattr(self, method_name):
            return getattr(self, method_name)()

        return self._operator_default()
