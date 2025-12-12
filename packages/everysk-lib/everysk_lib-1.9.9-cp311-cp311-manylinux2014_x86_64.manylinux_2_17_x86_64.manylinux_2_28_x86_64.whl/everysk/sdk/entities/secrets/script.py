###############################################################################
#
# (C) Copyright 2025 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################
import base64
from collections.abc import Callable
from inspect import isclass
from typing import Any

import six

from everysk.config import settings
from everysk.core.exceptions import FieldValueError, WorkerError
from everysk.core.object import BaseDict
from everysk.core.string import import_from_string
from everysk.sdk.base import BaseSDK
from everysk.sdk.entities import File
from everysk.sdk.entities.base import QueryMetaClass

###############################################################################
#  Class Implementation
###############################################################################


class SecretsScript(BaseDict, BaseSDK):
    _klass: Callable = None

    def __init__(self, _klass: Callable) -> None:
        super().__init__(_klass=None)

        if _klass is not None and not isclass(_klass):
            try:
                _klass = import_from_string(settings.EVERYSK_SDK_ENTITIES_MODULES_PATH[_klass])
            except KeyError:
                raise FieldValueError(
                    f"The _klass value '{_klass}' must be a class or a string with the class name."
                ) from KeyError

        self._klass = _klass

    def _process__klass(self, value: Any) -> Any:
        """
        This method is used to process the '_klass' attribute.
        """
        return value.__name__

    def _from_base_64(self, file_data: str) -> str:
        """
        Decodes the base 64 string data to normal sting.

        Args:
            file_data (str or bytes): The input data to be decoded. This can be a string or bytes.

        Returns:
            str: The decoded version of the input data as a string.
        """
        return six.ensure_str(base64.b64decode(six.ensure_str(file_data)))

    def _get_secrets_from_file(self, query: str | BaseDict | list[str], variant: str, workspace: str) -> str:
        secrets_file = File.script.fetch(query, variant, workspace)

        if not secrets_file:
            return None

        return self._from_base_64(secrets_file.data)

    def normalize(self, value: str | BaseDict | list[str], variant: str, workspace: str = None) -> str:
        normalized_value: str = None

        if variant == 'selectSecrets':
            from everysk.sdk.entities import Secrets

            normalized_value = Secrets.value_from_path(value)

        elif variant in {'metaString', 'password'}:
            normalized_value = value

        elif variant in {'selectFile', 'tagLatest', 'linkLatest'}:
            normalized_value = self._get_secrets_from_file(value, variant, workspace)

        elif variant == 'previousWorkers':
            if isinstance(value, str) and not File.validate_id(value):
                normalized_value = value

            else:
                normalized_value = self._get_secrets_from_file(value, variant, workspace)

        else:
            raise WorkerError(f'Unsupported secrets variant `{variant}`')

        return normalized_value


class SecretsScriptMetaClass(QueryMetaClass):
    """
    Metaclass for the Script class that allows for the script attribute to be accessed
    directly from the entity class.

    Example:
        To access the script attribute from the entity class:
        >>> MyClass.script
        Script()

    Notes:
        This metaclass overrides the __getatrribute__ method to enable direct access
    """

    def __getattribute__(cls, __name: str) -> Any:
        """
        Get the script attribute from the entity class.
        """
        if __name == 'script':
            return SecretsScript(cls)
        return super().__getattribute__(__name)
