# -*- coding: utf_8 -*-
###############################################################################
#
# (C) Copyright 2023 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################
from typing import Any

from everysk.config import settings
from everysk.core.exceptions import FieldValueError
from everysk.core.fields import DictField, ListField, StrField
from everysk.core.object import BaseDict
from everysk.sdk.entities.base import BaseEntity
from everysk.sdk.entities.fields import EntityDescriptionField, EntityNameField
from everysk.sdk.entities.secrets.script import SecretsScript, SecretsScriptMetaClass


###############################################################################
#   Secrets Class Implementation
###############################################################################
class Secrets(BaseEntity, metaclass=SecretsScriptMetaClass):
    script: SecretsScript = None
    _orderable_attributes = ListField(default=['created_on', 'updated_on', 'name'], readonly=True)

    id = StrField(regex=settings.SECRETS_ID_REGEX, required_lazy=True, empty_is_none=True)

    name = EntityNameField()
    description = EntityDescriptionField()
    data = DictField(required_lazy=True, empty_is_none=True)

    def to_dict(self, add_class_path: bool = False, recursion: bool = False) -> dict:
        """
        Convert the entity to a dictionary.

        Args:
            add_class_path (bool): If True, include the class path in the dictionary. Defaults to False.
            recursion (bool): If True, recursively convert nested entities to dictionaries. Defaults to False.

        Returns:
            dict: The entity as a dictionary.
        """
        dct = super().to_dict(add_class_path, recursion)

        if add_class_path is False and self.data and isinstance(self.data, BaseDict):
            dct['data'] = self.data.to_dict()

        return dct

    @staticmethod
    def get_id_prefix() -> str:
        """Get the ID prefix for the Secrets entity."""
        return settings.SECRETS_ID_PREFIX

    def _validate_data(self) -> None:
        """Validates the data field."""
        if not self.data:
            raise FieldValueError('data is required')

        if not isinstance(self.data, dict):
            raise FieldValueError('data must be a dictionary of version to Secret')

    def validate(self) -> bool:
        """
        Validate the entity properties.

        Raises:
            FieldValueError: If the entity properties are invalid.
            RequiredFieldError: If a required field is missing.

        Returns:
            bool: True if the entity properties are valid, False otherwise.

        Example usage:
            >>> entity = Secrets()
            >>> entity.validate()
            Traceback (most recent call last):
                ...
            everysk.sdk.exceptions.RequiredFieldError: The field 'name' is required.
        """
        super().validate()
        self._validate_data()
        return True

    @classmethod
    def _split_path(cls, path: str) -> tuple[str, list[str]]:
        """
        Split a path into id and keys.

        Args:
            path (str): The path to split.

        Returns:
            tuple[str, list[str]]: The id and keys.

        Raises:
            ValueError: If the path is invalid.
        """
        if not path or not isinstance(path, str) or '.' not in path:
            raise ValueError('Invalid path format. Expected format: "<secret_id>.<key1>.<key2>..."')

        values: list[str] = path.split('.')
        id, keys = values[0], values[1:]

        if cls.validate_id(id) is False:
            raise ValueError(f'Invalid id format: {id}')

        return id, keys

    @classmethod
    def value_from_path(cls, path: str) -> Any:
        """
        Retrieve a value from a given path.

        Args:
            path (str): The path to retrieve the value from.

        Returns:
            Any | None: The value retrieved from the path or None if the path is empty.
        """
        if not path:
            return None

        _, _ = cls._split_path(path)
        return cls.get_response(params={'path': path})
