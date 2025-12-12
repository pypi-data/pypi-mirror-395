###############################################################################
#
# (C) Copyright 2023 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################
# ruff: noqa: F401

## Remember to prefix all import with EveryskLib to avoid clash with other tests

## Cloud function Test Cases
try:
    from everysk.core.cloud_function.tests import CloudFunctionTestCase as EveryskLibCloudFunctionTestCase
except ModuleNotFoundError as error:
    # This will prevent running these tests if redis is not installed
    if not error.args[0].startswith("No module named 'redis'"):
        raise

## Compress Test Cases
from everysk.core._tests.compress import CompressGzipJsonTestCase as EveryskLibCompressGzipJsonTestCase
from everysk.core._tests.compress import CompressGzipPickleTestCase as EveryskLibCompressGzipPickleTestCase
from everysk.core._tests.compress import CompressTestCase as EveryskLibCompressTestCase
from everysk.core._tests.compress import CompressZlibJsonTestCase as EveryskLibCompressZlibJsonTestCase
from everysk.core._tests.compress import CompressZlibPickleTestCase as EveryskLibCompressZlibPickleTestCase
from everysk.core._tests.compress import FileHandlingTestCase as EveryskLibFileHandlingTestCase

## Config Test Cases
from everysk.core._tests.config import SettingsManagerTestCase as EveryskLibSettingsManagerTestCase
from everysk.core._tests.config import SettingsModulesTestCase as EveryskLibSettingsModulesTestCase
from everysk.core._tests.config import SettingsTestCase as EveryskLibSettingsTestCase

## Exceptions Test Cases
from everysk.core._tests.exceptions import BaseExceptionTestCase as EveryskLibBaseExceptionTestCase
from everysk.core._tests.exceptions import DefaultErrorTestCase as EveryskLibDefaultErrorTestCase
from everysk.core._tests.exceptions import FieldValueErrorTestCase as EveryskLibFieldValueErrorTestCase
from everysk.core._tests.exceptions import HandledExceptionTestCase as EveryskLibHandledExceptionTestCase
from everysk.core._tests.exceptions import HttpErrorTestCase as EveryskLibHttpErrorTestCase
from everysk.core._tests.exceptions import ReadonlyErrorTestCase as EveryskLibReadonlyErrorTestCase
from everysk.core._tests.exceptions import RequiredErrorTestCase as EveryskLibRequiredErrorTestCase
from everysk.core._tests.exceptions import SDKExceptionsTestCase as EveryskLibSDKExceptionsTestCase
from everysk.core._tests.exceptions import TestAPIError as EveryskLibTestAPIError

## Fields Test Cases
from everysk.core._tests.fields import BoolFieldTestCase as EveryskLibBoolFieldTestCase
from everysk.core._tests.fields import ChoiceFieldTestCase as EveryskLibChoiceFieldTestCase
from everysk.core._tests.fields import COD3770TestCase as EveryskLibCOD3770TestCase
from everysk.core._tests.fields import DateFieldTestCase as EveryskLibDateFieldTestCase
from everysk.core._tests.fields import DateTimeFieldTestCase as EveryskLibDateTimeFieldTestCase
from everysk.core._tests.fields import DictFieldTestCase as EveryskLibDictFieldTestCase
from everysk.core._tests.fields import EmailFieldTestCase as EveryskLibEmailFieldTestCase
from everysk.core._tests.fields import FieldTestCase as EveryskLibFieldTestCase
from everysk.core._tests.fields import FieldUndefinedTestCase as EveryskLibFieldUndefinedTestCase
from everysk.core._tests.fields import FloatFieldTestCase as EveryskLibFloatFieldTestCase
from everysk.core._tests.fields import IntFieldTestCase as EveryskLibIntFieldTestCase
from everysk.core._tests.fields import IteratorFieldTestCase as EveryskLibIteratorFieldTestCase
from everysk.core._tests.fields import ListFieldTestCase as EveryskLibListFieldTestCase
from everysk.core._tests.fields import ObjectInitPropertyTestCase as EveryskLibObjectInitPropertyTestCase
from everysk.core._tests.fields import SetFieldTestCase as EveryskLibSetFieldTestCase
from everysk.core._tests.fields import StrFieldTestCase as EveryskLibStrFieldTestCase
from everysk.core._tests.fields import TupleFieldTestCase as EveryskLibTupleFieldTestCase
from everysk.core._tests.fields import URLFieldTestCase as EveryskLibURLFieldTestCase

## Date, DateTime Test Cases
from everysk.core.datetime.tests.calendar import CalendarTestCase as EveryskLibCalendarTestCase
from everysk.core.datetime.tests.date import DateTestCase as EveryskLibDateTestCase
from everysk.core.datetime.tests.date_mixin import GetHolidaysTestCase as EveryskLibDateMixinGetHolidaysTestCase
from everysk.core.datetime.tests.datetime import DateTimeTestCase as EveryskLibDateTimeTestCase

## Firestore Test Cases
try:
    from everysk.core._tests.firestore import (
        BaseDocumentCachedConfigTestCase as EveryskLibBaseDocumentCachedConfigTestCase,
    )
    from everysk.core._tests.firestore import BaseDocumentConfigTestCase as EveryskLibBaseDocumentConfigTestCase
    from everysk.core._tests.firestore import DocumentCachedTestCase as EveryskLibDocumentCachedTestCase
    from everysk.core._tests.firestore import DocumentTestCase as EveryskLibDocumentTestCase
    from everysk.core._tests.firestore import FirestoreClientTestCase as EveryskLibFirestoreClientTestCase
    from everysk.core._tests.firestore import LoadsPaginatedTestCase as EveryskLibLoadsPaginatedTestCase
except ModuleNotFoundError as error:
    # This will prevent running these tests if google-cloud-firestore is not installed
    if not error.args[0].startswith("No module named 'google"):
        raise

## Http Test Cases
try:
    from everysk.core._tests.http import HttpConnectionConfigTestCase as EveryskLibHttpConnectionConfigTestCase
    from everysk.core._tests.http import HttpConnectionTestCase as EveryskLibHttpConnectionTestCase
    from everysk.core._tests.http import HttpDELETEConnectionTestCase as EveryskLibHttpDELETEConnectioNTestCase
    from everysk.core._tests.http import HttpGETConnectionTestCase as EveryskLibHttpGETConnectionTestCase
    from everysk.core._tests.http import HttpHEADConnectionTestCase as EveryskLibHttpHEADConnectionTestCase
    from everysk.core._tests.http import HttpOPTIONSConnectionTestCase as EveryskLibHttpOPTIONSConnectionTestCase
    from everysk.core._tests.http import HttpPATCHConnectionTestCase as EveryskLibHttpPATCHConnectionTestCase
    from everysk.core._tests.http import (
        HttpPOSTCompressedConnectionTestCase as EveryskLibHttpPOSTCompressedConnectionTestCase,
    )
    from everysk.core._tests.http import HttpPOSTConnectionTestCase as EveryskLibHttpPOSTConnectionTestCase
    from everysk.core._tests.http import HttpPUTConnectionTestCase as EveryskLibHttpPUTCompressedConnectionTestCase
    from everysk.core._tests.http import HttpSDKPOSTConnectionTestCase as EveryskLibHttpSDKPOSTConnectionTestCase
except ModuleNotFoundError as error:
    # This will prevent running these tests if requests is not installed
    if not error.args[0].startswith("No module named 'requests'"):
        raise

## Lists Test Cases
from everysk.core._tests.lists import SlicesTestCase as EveryskLibSlicesTestCase
from everysk.core._tests.lists import SortListDictTestCase as EveryskLibSortListDictTestCase
from everysk.core._tests.lists import SplitInSlicesTestCase as EveryskLibSplitInSlicesTestCase

## Log Test Cases
from everysk.core._tests.log import LoggerExtraDataTestCase as EveryskLibLoggerExtraDataTestCase
from everysk.core._tests.log import LoggerFormatterTestCase as EveryskLibLoggerFormatterTestCase
from everysk.core._tests.log import LoggerJsonTestCase as EveryskLibLoggerJsonTestCase
from everysk.core._tests.log import LoggerManagerTestCase as EveryskLibLoggerManagerTestCase
from everysk.core._tests.log import LoggerMethodsTestCase as EveryskLibLoggerMethodsTestCase
from everysk.core._tests.log import LoggerStackLevelTestCase as EveryskLibLoggerStackLevelTestCase
from everysk.core._tests.log import LoggerStdoutTestCase as EveryskLibLoggerStdoutTestCase
from everysk.core._tests.log import LoggerTestCase as EveryskLibLoggerTestCase
from everysk.core._tests.log import LoggerTraceTestCase as EveryskLibLogTraceTestCase

try:
    # We need requests to run this test
    from everysk.core._tests.log import LoggerSlackTestCase as EveryskLibLoggerSlackTestCase
except ModuleNotFoundError as error:
    # This will prevent running these tests if requests is not installed
    if not error.args[0].startswith("No module named 'requests'"):
        raise

## Number Test Cases
from everysk.core._tests.number import NumberTestCase as EveryskLibNumberTestCase

## Object Test Cases
from everysk.core._tests.object import AfterInitTestCase as EveryskLibAfterInitTestCase
from everysk.core._tests.object import BaseDictPropertyTestCase as EveryskLibBaseDictPropertyTestCase
from everysk.core._tests.object import BaseDictSuperTestCase as EveryskLibBaseDictSuperTestCase
from everysk.core._tests.object import BaseDictTestCase as EveryskLibBaseDictTestCase
from everysk.core._tests.object import BaseFieldTestCase as EveryskLibBaseFieldTestCase
from everysk.core._tests.object import BaseObjectTestCase as EveryskLibBaseObjectTestCase
from everysk.core._tests.object import BeforeInitTestCase as EveryskLibBeforeInitTestCase
from everysk.core._tests.object import ConfigHashTestCase as EveryskLibConfigHashTestCase
from everysk.core._tests.object import FrozenDictTestCase as EveryskLibFrozenDictTestCase
from everysk.core._tests.object import FrozenObjectTestCase as EveryskLibFrozenObjectTestCase
from everysk.core._tests.object import MetaClassAttributesTestCase as EveryskLibMetaClassAttributesTestCase
from everysk.core._tests.object import MetaClassConfigTestCase as EveryskLibMetaClassConfigTestCase
from everysk.core._tests.object import NpArrayTestCase as EveryskLibNpArrayTestCase
from everysk.core._tests.object import RequiredTestCase as EveryskLibRequiredTestCase
from everysk.core._tests.object import SilentTestCase as EveryskLibSilentTestCase
from everysk.core._tests.object import TypingCheckingTestCase as EveryskLibTypingCheckingTestCase
from everysk.core._tests.object import ValidateTestCase as EveryskLibValidateTestCase

## Redis Test Cases
try:
    from everysk.core._tests.redis import CacheDecoratorTestCase as EveryskLibCacheDecoratorTestCase
    from everysk.core._tests.redis import RedisCacheCompressedTestCase as EveryskLibRedisCacheCompressedTestCase
    from everysk.core._tests.redis import RedisCacheGetSetTestCase as EveryskLibRedisCacheGetSetTestCase
    from everysk.core._tests.redis import RedisCacheTestCase as EveryskLibRedisCacheTestCase
    from everysk.core._tests.redis import RedisChannelTestCase as EveryskLibRedisChannelTestCase
    from everysk.core._tests.redis import RedisClientTestCase as EveryskLibRedisClientTestCase
    from everysk.core._tests.redis import RedisListTestCase as EveryskLibRedisListTestCase
    from everysk.core._tests.redis import RedisLockTestCase as EveryskLibRedisLockTestCase
except ModuleNotFoundError as error:
    # This will prevent running these tests if redis is not installed
    if not error.args[0].startswith("No module named 'redis'"):
        raise

## Retry Test Cases
from everysk.core._tests.retry import RetryTestCase as EveryskLibRetryTestCase

## Serialize Test Cases
from everysk.core._tests.serialize.test_json import SerializeJsonDumpsTestCase as EveryskLibSerializeJsonDumpsTestCase
from everysk.core._tests.serialize.test_json import SerializeJsonLoadsTestCase as EveryskLibSerializeJsonLoadsTestCase
from everysk.core._tests.serialize.test_pickle import (
    SerializePickleDumpsTestCase as EveryskLibSerializePickleDumpsTestCase,
)
from everysk.core._tests.serialize.test_pickle import (
    SerializePickleLoadsTestCase as EveryskLibSerializePickleLoadsTestCase,
)

try:
    from everysk.core._tests.serialize.test_orjson import (
        SerializeOrjsonDumpsTestCase as EveryskLibSerializeOrjsonDumpsTestCase,
    )
    from everysk.core._tests.serialize.test_orjson import (
        SerializeOrjsonLoadsTestCase as EveryskLibSerializeOrjsonLoadsTestCase,
    )
except ModuleNotFoundError as error:
    # This will prevent running these tests if orjson is not installed
    if not error.args[0].startswith("No module named 'orjson'"):
        raise

## SFTP Test Cases
try:
    from everysk.core._tests.sftp import KnownHostsTestCase as EveryskLibKnownHostsTestCase
    from everysk.core._tests.sftp import SFTPTestCase as EveryskLibSFTPTestCase
except ModuleNotFoundError as error:
    # This will prevent running these tests if Paramiko is not installed
    if not error.args[0].startswith("No module named 'paramiko'"):
        raise

## Signing Test Cases
from everysk.core._tests.signing import SignTestCase as EveryskLibSignTestCase
from everysk.core._tests.signing import UnsignTestCase as EveryskLibUnsignTestCase

## String Test Cases
from everysk.core._tests.string import StringTestCase as EveryskLibStringTestCase

## Slack Test Cases
try:
    from everysk.core._tests.slack import SlackTestCase as EveryskLibSlackTestCase
except ModuleNotFoundError as error:
    # This will prevent running these tests if requests is not installed
    if not error.args[0].startswith("No module named 'requests'"):
        raise


## Thread Test Cases
from everysk.core._tests.threads import ThreadPoolTestCase as EveryskLibThreadPoolTestCase
from everysk.core._tests.threads import ThreadTestCase as EveryskLibThreadTestCase

## Undefined Test Cases
from everysk.core._tests.undefined import UndefinedTestCase as EveryskLibUndefinedTestCase

## Unittest Test Cases
from everysk.core._tests.unittests import SDKUnittestTestCase as EveryskLibSDKUnittestTestCase

## Utils Test Cases
from everysk.core._tests.utils import BoolConverterTestCase as EveryskLibBoolConverterTestCase
from everysk.core._tests.utils import SearchKeyTestCase as EveryskLibSearchKeyTestCase

## Workers Test Cases
try:
    from everysk.core._tests.workers import BaseGoogleTestCase as EveryskLibBaseGoogleTestCase
    from everysk.core._tests.workers import TaskGoogleTestCase as EveryskLibTaskGoogleTestCase
    from everysk.core._tests.workers import WorkerGoogleTestCase as EveryskLibWorkerGoogleTestCase
except ModuleNotFoundError as error:
    # This will prevent running these tests if google-cloud-tasks is not installed
    if not error.args[0].startswith("No module named 'google"):
        raise
