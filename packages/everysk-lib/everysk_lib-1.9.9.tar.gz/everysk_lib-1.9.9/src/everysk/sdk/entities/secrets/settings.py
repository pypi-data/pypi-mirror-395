###############################################################################
#
# (C) Copyright 2023 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################
from everysk.core.fields import IntField, RegexField, StrField

###############################################################################
#   Settings Implementation
###############################################################################
SECRETS_ID_PREFIX = StrField(default='scrt_', readonly=True)
SECRETS_ID_REGEX = RegexField(default=r'^scrt_[a-zA-Z0-9]{25}', readonly=True)
SECRETS_ID_MAX_LENGTH = IntField(default=30, readonly=True)  # len(SECRETS_ID_PREFIX) + ENTITY_ID_LENGTH
