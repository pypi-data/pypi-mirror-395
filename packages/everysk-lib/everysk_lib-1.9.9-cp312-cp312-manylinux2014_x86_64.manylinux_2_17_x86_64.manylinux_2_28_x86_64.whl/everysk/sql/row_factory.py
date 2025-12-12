###############################################################################
#
# (C) Copyright 2025 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################
from collections.abc import Callable, Iterable
from typing import Any

from psycopg import Cursor
from psycopg.rows import _get_names, no_result


def cls_row(cls: type, loads: Callable | None = None) -> Callable:
    """
    Function to convert a row from a cursor to an instance of the specified class.

    Args:
        cls (type): The class to instantiate for each row.
        loads (callable | None, optional): Optional function to process each value. Defaults to None.
    """

    def inner(cursor: Cursor) -> Callable:
        names = _get_names(cursor)
        if names is None:
            return no_result

        def cls_row_(values: Iterable) -> Any:
            if loads is None:
                return cls(**dict(zip(names, values, strict=True)))

            return cls(**dict(zip(names, map(loads, values), strict=True)))

        return cls_row_

    return inner


def dict_row(loads: Callable | None = None) -> Callable:
    """
    Function to convert a row from a cursor to a dictionary.

    Args:
        loads (Callable | None): Optional function to process each value. Defaults to None.
    """

    def inner(cursor: Cursor) -> Callable:
        names = _get_names(cursor)
        if names is None:
            return no_result

        def dict_row_(values: Iterable) -> dict[str, Any]:
            if loads is None:
                return dict(zip(names, values, strict=True))

            return dict(zip(names, map(loads, values), strict=True))

        return dict_row_

    return inner
