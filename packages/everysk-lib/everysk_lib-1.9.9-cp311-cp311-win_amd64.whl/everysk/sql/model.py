###############################################################################
#
# (C) Copyright 2025 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################
import inspect
from copy import deepcopy
from types import GenericAlias, UnionType
from typing import Any, Generic, Literal, Self, TypeVar, Union, get_args, get_origin

from everysk.core.datetime import Date, DateTime
from everysk.sql.connection import execute
from everysk.sql.query import Query

FT = TypeVar('FT')
MT = TypeVar('MT', bound='BaseModel')


class BaseModelMetaClass(type):
    # Method called when a class is created in the Python runtime
    def __new__(cls, name: str, bases: tuple[type, ...], attrs: dict[str, Any]) -> MT:
        # Attributes that are inside annotations -> var: str or var: str = 'value'
        # Attributes that are not inside annotations -> var = 'value'
        # We need to get both
        for key in attrs['__annotations__'].keys() | attrs.keys():
            # Discard internal attributes
            if not key.startswith('__'):
                default_value = attrs.get(key)
                if not inspect.isroutine(default_value) and not isinstance(default_value, (property, BaseModelField)):
                    # If the attribute is not inside annotations (var = 'value'), we add it
                    if key not in attrs['__annotations__']:
                        attrs['__annotations__'][key] = type(default_value)

                    # Get the type from the annotations
                    field_type = attrs['__annotations__'].get(key)
                    # Change the attribute to a BaseModelField descriptor
                    attrs[key] = BaseModelField(default=default_value, field_type=field_type)

        obj: BaseModel = super().__new__(cls, name, bases, attrs)
        obj._generate_attributes()  # noqa: SLF001
        obj._generate_fields()  # noqa: SLF001
        obj._generate_query()  # noqa: SLF001
        return obj

    def __setattr__(cls: 'BaseModel', name: str, value: Any) -> None:
        # Internal attributes are set normally
        # They are __attributes__, __fields__, __query__
        if name.startswith('__'):
            return super().__setattr__(name, value)

        if name in cls.__attributes__:
            # Get the type that was already defined to validate the value
            field_type = cls.__attributes__[name].field_type
        else:
            # If the attribute is not defined, we add it
            field_type = type(value)
            cls.__annotations__[name] = field_type
            cls.__attributes__[name] = field_type
            if not name.startswith('_'):
                cls.__fields__[name] = field_type

        # Change the attribute to a BaseModelField descriptor
        value = BaseModelField(default=value, field_type=field_type, field_name=name)
        return super().__setattr__(name, value)

    def __delattr__(cls: 'BaseModel', name: str) -> None:
        if name in cls.__attributes__:
            del cls.__attributes__[name]

        if name in cls.__fields__:
            del cls.__fields__[name]

        if name in cls.__annotations__:
            del cls.__annotations__[name]

        return super().__delattr__(name)


class BaseModelField(Generic[FT]):
    # https://docs.python.org/3.12/howto/descriptor.html
    default: FT | None
    field_name: str
    field_type: FT

    def __init__(self, default: FT | None = None, *, field_type: FT, field_name: str | None = None) -> None:
        if isinstance(field_type, GenericAlias):
            # We need to get the origin of the generic type
            field_type = get_origin(field_type)
        # TypeError: typing.Union cannot be used with isinstance()
        # The correct class of Unions is types.UnionType
        elif isinstance(field_type, UnionType):
            # We need to find if there are GenericAlias inside the Union
            types = []
            for _type in get_args(field_type):
                if isinstance(_type, GenericAlias):
                    _type = get_origin(_type)
                # We discard NoneType from the Union because it's normally used as optional
                # This check is here because None is always the last type in the Union
                if _type is type(None):
                    continue
                types.append(_type)

            # If there is only one type, we use it directly
            if len(types) == 1:
                field_type = types[0]
            else:
                field_type = Union[tuple(types)]  # noqa: UP007

        self.field_type = field_type
        self.field_name = field_name
        # We always validate the default value
        if default is not None:
            self.validate(default)

        self.default = default

    def __delete__(self, obj: 'BaseModel') -> None:
        if self.field_name in obj:
            del obj[self.field_name]

    def __get__(self, obj: 'BaseModel', cls: type) -> FT:
        # First we get the value from the dict, if not present we get the value from the default
        if obj is None:
            return self.default

        return obj.get(self.field_name, self.default)

    def __set__(self, obj: 'BaseModel', value: FT) -> None:
        value = self.clean_value(value)

        if obj._validate_fields:  # noqa: SLF001
            self.validate(value)

        obj[self.field_name] = value

    def __set_name__(self, cls: type, name: str) -> None:
        self.field_name = name

    ## Validation methods
    def clean_value(self, value: object) -> object:
        # The database value is datetime or date, we need to convert it to DateTime or Date
        # Or we could store it as ISO format string and convert it back
        if value:
            # The result from the database could be a string, datetime or date
            # We need to convert it to DateTime or Date
            if self.field_type in (DateTime, Date):
                if isinstance(value, str):
                    return self.field_type.fromisoformat(value)

                return self.field_type.ensure(value)

            # For sets and tuples, we save them as JSONB in the database that is a list
            # when we get it back, we need to convert it to set or tuple
            if self.field_type in (set, tuple):
                return self.field_type(value)

        return value

    def _validate_instance(self, value: object) -> None:
        if value and not isinstance(value, self.field_type):
            name = self.field_name
            type_name = self.field_type.__qualname__
            received_name = type(value).__qualname__
            msg = f'Field {name} must be of type {type_name}, got {received_name}.'
            raise TypeError(msg)

    def validate(self, value: object) -> None:
        validate_func = getattr(self, f'_validate_{self.field_name}', self._validate_instance)
        validate_func(value=value)


class BaseModel(dict, metaclass=BaseModelMetaClass):
    # https://docs.python.org/3/reference/datamodel.html#slots
    # These are class attributes that are not in the __dict__
    __slots__ = ('__attributes__', '__dict__', '__fields__', '__query__')

    ## Private attributes
    _dsn: str = None
    _primary_key: str = None
    _schema: str = None
    _table_name: str = None
    _validate_fields: bool = True

    ## Public attributes
    # All public attributes are table fields and keys of the dict
    created_on: DateTime = None
    updated_on: DateTime = None

    ## Internal methods
    def __init__(self, *, validate_fields: bool | None = None, **kwargs) -> None:
        # If validate_fields is None, we use the class attribute
        if validate_fields is not None:
            self._validate_fields = validate_fields

        if self._validate_fields:
            for key, value in kwargs.items():
                self._validate(key, value)

        # Set created_on if not provided
        if 'created_on' not in kwargs:
            kwargs['created_on'] = DateTime.now()

        # We need to set all fields to None to complete the dict keys
        fields = self._get_field_values(init_values=kwargs)
        super().__init__(**fields)

    def __repr__(self) -> str:
        return self.__str__()

    def __setitem__(self, key: str, value: Any) -> None:
        if self._validate_fields:
            self._validate(key, value)

        return super().__setitem__(key, value)

    def __str__(self) -> str:
        # Use the class name and primary key for string representation
        class_name = type(self).__name__
        if self._primary_key is not None:
            pk = getattr(self, self._primary_key, None)
            if pk is not None:
                return f'{class_name}({self._primary_key}={pk})'

        return f'{class_name}()'

    ## Private methods
    def _get_field_values(self, *, init_values: dict[str, Any] | None = None) -> dict[str, Any]:
        if init_values is None:
            init_values = {}

        # Get only fields that are not already in init_values
        cls = type(self)
        fields = cls._get_fields() - init_values.keys()
        for field in fields:
            value = getattr(self, field, None)
            init_values[field] = value

        return init_values

    def _validate(self, key: str, value: Any) -> None:
        if key in self._get_attributes():
            field = self._get_attributes()[key]
            value = field.clean_value(value)
            field.validate(value)
        else:
            msg = f'Field {key} is not defined in {type(self).__name__}.'
            raise KeyError(msg)

    ## Class methods
    @classmethod
    def _execute(
        cls,
        query: str,
        params: dict | None = None,
        return_type: Literal['dict', 'list'] = 'list',
        klass: type | None = None,
    ) -> Any:
        kwargs = {'query': query, 'params': params, 'return_type': return_type, 'dsn': cls._dsn, 'cls': klass}
        return execute(**kwargs)

    @classmethod
    def _generate_attributes(cls) -> None:
        cls.__attributes__ = {}
        # We need to get all attributes from the class and its bases
        # We stop at BaseModel (inclusive)
        for base in cls.mro()[:-2]:
            # Annotations are all attributes that are defined in the class
            # In the __dict__ is the correct Field descriptor for each attribute
            if base.__attributes__:
                cls.__attributes__.update(base.__attributes__)
                # If the base has the attributes, we don't need to get the others
                break
            # If we don't have the attributes in the base, we make then
            keys = base.__annotations__.keys()
            cls.__attributes__.update({key: base.__dict__[key] for key in keys})

    @classmethod
    def _generate_fields(cls) -> None:
        # Fields are all attributes except those starting with _
        cls.__fields__ = {
            key: field.field_type for key, field in cls._get_attributes().items() if not key.startswith('_')
        }

    @classmethod
    def _generate_query(cls) -> None:
        cls.__query__ = Query(table_name=cls._table_name, primary_key=cls._primary_key, schema=cls._schema)

    @classmethod
    def _get_attributes(cls) -> dict[str, BaseModelField]:
        if cls.__attributes__ is None:
            cls._generate_attributes()

        return cls.__attributes__

    @classmethod
    def _get_fields(cls) -> dict[str, type]:
        if cls.__fields__ is None:
            cls._generate_fields()

        return cls.__fields__

    @classmethod
    def _get_query(cls) -> Query:
        if cls.__query__ is None:
            cls._generate_query()

        return cls.__query__

    @classmethod
    def create_table(cls) -> None:
        # First we create the table if it doesn't exist
        sql = cls._get_query().parse_create_table(fields=cls._get_fields())
        cls._execute(query=sql)
        # Then we create the index on the primary key if it doesn't exist
        sql = cls._get_query().parse_index(fields=cls._primary_key)
        cls._execute(query=sql)

    @classmethod
    def loads(
        cls,
        fields: list | None = None,
        order_by: str | None = None,
        limit: int | None = None,
        return_type: Literal['dict', 'list'] = 'list',
        **conditions: dict,
    ) -> list[Self] | dict[str, Self]:
        if fields is None:
            fields = set(cls._get_fields().keys())
        sql, params = cls._get_query().parse_select(
            fields=fields, order_by=order_by, limit=limit, conditions=conditions
        )
        return cls._execute(query=sql, params=params, return_type=return_type, klass=cls)

    ## Instance methods
    def delete(self) -> None:
        cls = type(self)
        sql = cls._get_query().parse_delete()
        cls._execute(query=sql, params={'ids': [getattr(self, self._primary_key)]})

    def load(self) -> Self:
        cls = type(self)
        conditions = {f'{self._primary_key}__eq': getattr(self, self._primary_key)}
        sql, params = cls._get_query().parse_select(fields=cls._get_fields(), limit=1, conditions=conditions)
        results = cls._execute(query=sql, params=params)

        if not results:
            msg = f'{cls.__name__} with {self._primary_key}={getattr(self, self._primary_key)} not found.'
            raise ValueError(msg)

        self.update(results[0])
        return self

    def save(self) -> Self:
        self.updated_on = DateTime.now()
        cls = type(self)
        sql = cls._get_query().parse_insert_or_update(fields=cls._get_fields())
        # We need to change some values so they can be used as params
        # To avoid modifying the current instance, we create a copy of it
        # The deepcopy creates a new instance of the same class so we need to change it
        # to dict avoiding validation and other checks
        params = dict(deepcopy(self))
        params = cls._get_query().parse_insert_or_update_params(params=params)
        cls._execute(query=sql, params=params)
        return self

    def update(self, *args, **kwargs) -> None:
        dct = dict(*args, **kwargs)
        if self._validate_fields:
            for key, value in dct.items():
                self._validate(key, value)

        super().update(dct)
