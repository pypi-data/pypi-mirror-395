###############################################################################
#
# (C) Copyright 2023 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################
# ruff: noqa: F403
try:
    # everysk/api/__init__.py imports requests
    from everysk.api.tests import *
except ModuleNotFoundError as error:
    # This will prevent running these tests if requests is not installed
    if not error.args[0].startswith("No module named 'requests'"):
        raise

from everysk.core.tests import *
from everysk.sdk.tests import *
from everysk.server.tests import *
from everysk.sql.tests import *
