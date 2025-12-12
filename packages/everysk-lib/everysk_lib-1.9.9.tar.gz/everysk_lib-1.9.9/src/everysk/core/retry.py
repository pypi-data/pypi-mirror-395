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

from everysk.config import settings
from everysk.core.log import Logger

log = Logger('everysk-lib-core-retry')


def retry(
    func: callable, params: dict, retry_count: int = 0, retries: int = 5, exceptions: tuple | Exception = Exception
) -> Any:
    """
    Retries a function call a number of times if it raises an exception.

    Args:
        func (callable): The function to be called.
        params (dict): The parameters to be passed to the function.
        retry_count (int, optional): The current retry count. Defaults to 0.
        retries (int, optional): The maximum number of retries. Defaults to 5.
        exceptions (tuple | Exception, optional): The exceptions to catch. Defaults to Exception.

    Raises:
        Exception: If the maximum number of retries is reached.
    """
    try:
        return func(**params)
    except exceptions:
        if retry_count < retries:
            if settings.RETRY_SHOW_LOGS:
                msg = f'Retry {retry_count + 1} of {retries} for function {func.__name__} due to exception.'
                log.warning(
                    msg,
                    extra={
                        'function': func.__name__,
                        'params': params,
                        'retry_count': retry_count + 1,
                        'max_retries': retries,
                    },
                )
            return retry(func, params, retry_count + 1, retries, exceptions)

        raise
