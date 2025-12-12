from typing import Any, Iterable, Optional

from pydantic_core import PydanticUndefined
from sqlmodel import SQLModel
from sqlalchemy import Column, Engine, MetaData, Connection, ForeignKey
from str_case_util import Case
from sqlalchemy.ext.declarative import declared_attr

from daomodel.list_util import in_order
from daomodel.metaclass import DAOModelMetaclass
from daomodel.util import reference_of, names_of, retain_in_dict, remove_from_dict
from daomodel.property_filter import PropertyFilter, ALL


ColumnBreadcrumbs = tuple[type['DAOModel'], ..., Column]


class DAOModel(SQLModel, metaclass=DAOModelMetaclass):
    """An SQLModel specifically designed to support a DAO."""

    @declared_attr
    def __tablename__(self) -> str:
        return self.normalized_name()

    @classmethod
    def has_column(cls, column: Column) -> bool:
        """Returns True if the specified Column belongs to this DAOModel."""
        return column.table.name == cls.__tablename__

    @classmethod
    def normalized_name(cls) -> str:
        """A normalized version of this Model name.

        :return: The model name in snake_case form
        """
        return Case.SNAKE_CASE.format(cls.__name__)

    @classmethod
    def doc_name(cls) -> str:
        """A reader-friendly version of this Model name to be used within documentation.

        :return: The model name in Title Case
        """
        return Case.TITLE_CASE.format(cls.__name__)

    @classmethod
    def get_pk(cls) -> Iterable[Column]:
        """Returns the Columns that comprise the Primary Key for this Model.

        :return: A list of primary key columns
        """
        return cls.__table__.primary_key

    @classmethod
    def get_pk_names(cls) -> list[str]:
        """Returns the names of Columns that comprise the Primary Key for this Model.

        :return: A list (of str) of the primary key
        """
        return names_of(cls.get_pk())

    def get_pk_values(self) -> tuple:
        """Returns the values that comprise the Primary Key for this instance of the Model.

        :return: A tuple of primary key values
        """
        return tuple(getattr(self, key) for key in names_of(self.get_pk()))

    def get_pk_dict(self) -> dict[str, Any]:
        """Returns the Primary Key values for this instance of the Model.

        :return: A dict of primary key names/values
        """
        return self.model_dump(include=set(self.get_pk_names()))

    @classmethod
    def get_fks(cls) -> set[Column]:
        """Returns the Columns of other tables that are represented by Foreign Keys for this Model.

        A returned Column could be within this Model in the case of a cyclic relationship.

        :return: An unordered set of columns
        """
        return {fk.column for fk in cls.__table__.foreign_keys}

    @classmethod
    def get_fk_properties(cls) -> set[Column]:
        """Returns the Columns of this Model that represent Foreign Keys.

        :return: An unordered set of foreign key columns
        """
        return {fk.parent for fk in cls.__table__.foreign_keys}

    @classmethod
    def get_references_of(cls, model: type['DAOModel']) -> set[ForeignKey]:
        """Returns the Columns of this Model that represent Foreign Keys of the specified Model.

        :return: An unordered set of foreign key columns
        """
        return {fk for fk in cls.__table__.foreign_keys if model.has_column(fk.column)}

    @classmethod
    def get_properties(cls) -> Iterable[Column]:
        """Returns all the Columns for this Model.

        Column order will match order they are defined in code.
        Inherited properties will be listed first.

        :return: A list of columns
        """
        return cls.__table__.c

    def get_property_names(self, *filters: PropertyFilter) -> list[str]:
        """Returns the names of the specified properties for this record.

        Requested property categories may be refined through filters:

        - `ALL`: All properties
        - `PK`: Primary Key properties
        - `FK`: Foreign Key properties
        - `DEFAULT`: Properties that are equivalent to their default value
        - `NONE`: Properties that do not have a value

        ```python
        # Get all properties (default if no filter specified)
        model.get_property_names()

        # Get all primary key properties
        model.get_property_names(PK)
        ```

        Each filter can be negated by prepending `~` to indicate _NOT_:
        ```python
        # Get all non-null properties
        model.get_property_names(~NONE)

        # Get all properties that are not relationships
        model.get_property_names(~FK)
        ```

        Operators allow for combining filters into expressions:

        - `&` (AND): Properties must match both filters
        - `|` (OR): Properties must match at least one filter
        - `~` (NOT): Properties must NOT match the filter

        ```python
        # Get missing relationships
        model.get_property_names(FK & NONE)

        # Get properties that are a primary or foreign key
        model.get_property_names(PK | FK)

        # Get properties that are their default value or null
        model.get_property_names(DEFAULT | NONE)

        # Get properties that are either not null or are primary key relationships
        model.get_property_names(~NONE | PK & FK)
        ```

        Multiple filter arguments (seperated by commas) are combined with AND:
        ```python
        # Get primary keys that aren't foreign keys
        model.get_property_names(PK, ~FK)  # equivalent to: PK & ~FK

        # Make sure they are also not null
        model.get_property_names(PK, ~FK, ~NONE)  # equivalent to: PK & ~FK & ~NONE
        ```

        Combine several filters to form complex expressions:
        ```python
        # Get properties that are either primary keys that aren't foreign keys or are non-null default values
        model.get_property_names(PK & ~FK | DEFAULT & ~NONE)
        ```

        The filters within an expression are resolved in a specific order:

        1. `~` (NOT): Properties must NOT match the filter
        2. `&` (AND): Properties must match both filters
        3. `|` (OR): Properties must match at least one filter

        Therefore, the following expressions are all equivalent:
        ```python
        model.get_property_names(~NONE | PK & ~FK)
        model.get_property_names(PK & ~FK | ~NONE)
        model.get_property_names(~FK & PK | ~NONE)
        ```

        To change the order of evaluation, use parentheses:
        ```python
        # properties that are either not null or are primary keys but not foreign keys
        model.get_property_names(~FK & PK | ~NONE)

        # properties that are either not null or are not both primary and foreign keys
        model.get_property_names(~(FK & PK) | ~NONE)

        # properties that are not foreign keys and properties that are either primary keys or are non-null
        model.get_property_names(~FK & (PK | ~NONE))
        ```

        :param filters: Property filter expressions using PK, FK, DEFAULT, NONE. Multiple filters are combined with AND.
        :return: A list of property names in the order they are defined within the code
        """
        match len(filters):
            case 0:
                prop_filter = ALL
            case 1:
                prop_filter = filters[0]
            case _:
                prop_filter = filters[0]
                for next_filter in filters[1:]:
                    prop_filter &= next_filter

        result = prop_filter.evaluate(self)
        return in_order(result, names_of(self.get_properties()))

    def get_property_values(self, *filters: PropertyFilter) -> dict[str, Any]:
        """Reads values of the specified properties for this record.

        :param filters: Property filter expressions (see `get_property_names`)
        :return: A dict of property names and their values
        """
        return self.get_values_of(self.get_property_names(*filters))

    @classmethod
    def get_default(cls, column: Column|str):
        """Returns the default value for a given column

        :param column: The Column, or column name
        :return: The default value for the column
        :raises ValueError: if the column has no default value set
        """
        if not isinstance(column, str):
            column = column.name
        field = cls.model_fields.get(column)
        default = field.get_default()
        if default == PydanticUndefined:
            raise ValueError(f'No default is set for {field}.')
        return default

    def get_value_of(self, column: Column|str) -> Any:
        """Shortcut function to return the value for the specified Column.

        :param column: The Column, or column name, to read
        :raises `AttributeError`: if the column is not found.
        """
        if not isinstance(column, str):
            column = column.name
        return getattr(self, column)

    def get_values_of(self, columns: Iterable[Column|str]) -> dict[str, Any]:
        """Reads the values of multiple columns.

        :param columns: The Columns, or their names, to read
        :return: A dict of the column names and their values
        """
        return {column: self.get_value_of(column) for column in columns}

    @classmethod
    def get_searchable_properties(cls) -> Iterable[Column | ColumnBreadcrumbs]:
        """Returns all the Columns for this Model that may be searched using the DAO find function.

        All properties are searchable unless marked with the Unsearchable type annotation.

        To mark a property as unsearchable:
        ```python
        class MyModel(DAOModel, table=True):
            id: Identifier[int]  # Searchable by default
            name: str  # Searchable by default
            internal_notes: Unsearchable[str]  # Not searchable
        ```

        Properties of related models are only searchable if defined within your model's Meta class.
        Please readthedocs for more information.

        :return: A list of searchable columns
        """
        unsearchable = getattr(getattr(cls, '_unsearchable', None), 'default', set())
        searchable = [column for column in cls.get_properties() if column.name not in unsearchable]
        searchable.extend(getattr(getattr(cls, 'Meta', None), 'searchable_relations', set()))
        return searchable

    @classmethod
    def find_searchable_column(cls, prop: str|Column, foreign_tables: list[type['DAOModel']]) -> Column:
        """Returns the specified searchable Column.

        :param prop: str type reference of the Column or the Column itself
        :param foreign_tables: A list of foreign tables to be populated with tables of properties deemed to be foreign
        :return: The searchable Column
        :raises Unsearchable: if the property is not Searchable for this class
        """
        if type(prop) is not str:
            prop = reference_of(prop)
        for column in cls.get_searchable_properties():
            tables = []
            if type(column) is tuple:
                tables = column[:-1]
                column = column[-1]
            if reference_of(column) in [prop, f'{cls.normalized_name()}.{prop}']:
                foreign_tables.extend([t.__table__ for t in tables])
                if column.table is not cls.__table__:
                    foreign_tables.append(column.table)
                return column
        raise UnsearchableError(prop, cls)

    @classmethod
    def pk_values_to_dict(cls, *pk_values: Any) -> dict[str, Any]:
        """Converts the primary key values to a dictionary.

        :param pk_values: The primary key values, in order
        :return: A new dict containing the primary key values
        """
        return dict(zip(cls.get_pk_names(), *pk_values))

    def copy_model(self, source: 'DAOModel', *fields: str) -> None:
        """Copies values from another instance of this Model.

        Unless the fields are specified, all but PK are copied.

        :param source: The model instance from which to copy values
        :param fields: The names of fields to copy
        """
        if fields:
            values = source.model_dump(include=set(fields))
        else:
            values = source.model_dump(exclude=set(source.get_pk_names()))
        self.set_values(**values)

    def set_values(self, ignore_pk: Optional[bool] = False, **values: Any) -> None:
        """Copies property values to this model instance.

        By default, Primary Key values are set if present within the values.

        :param ignore_pk: True if you also wish to not set Primary Key values
        :param values: The dict including values to set
        """
        values = retain_in_dict(values, *names_of(self.get_properties()))
        if ignore_pk:
            values = remove_from_dict(values, *self.get_pk_names())
        for k, v in values.items():
            setattr(self, k, v)

    def __eq__(self, other: 'DAOModel') -> bool:
        """Instances are determined to be equal based on only their primary key."""
        return self.get_pk_values() == other.get_pk_values() if type(self) == type(other) else False

    def __hash__(self) -> int:
        return hash(self.get_pk_values())

    def __str__(self) -> str:
        """
        str representation of this is a str of the primary key.
        A single-column PK results in a simple str value of said column i.e. '1234'
        A multi-column PK results in a str of tuple of PK values i.e. ('Cod', '123 Lake Way')
        """
        pk_values = self.get_pk_values()
        if len(pk_values) == 1:
            pk_values = pk_values[0]
        return str(pk_values)


class UnsearchableError(Exception):
    """Indicates that the Search Query is not allowed for the specified field."""
    def __init__(self, prop: str, model: type(DAOModel)):
        self.detail = f'Cannot search for {prop} of {model.doc_name()}'


def all_models(bind: [Engine|Connection]) -> set[type[DAOModel]]:
    """Discovers all DAOModel types that have been created for the database.

    :param bind: The Engine or Connection for the DB
    :return: A set of applicable DAOModels
    """
    def daomodel_subclasses(cls: type[DAOModel]) -> set[type[DAOModel]]:
        """Returns all defined DAOModels"""
        subclasses = set(cls.__subclasses__())
        for subclass in subclasses.copy():
            subclasses.update(daomodel_subclasses(subclass))
        return subclasses

    metadata = MetaData()
    metadata.reflect(bind=bind)
    db_tables = metadata.tables.keys()
    return {model for model in daomodel_subclasses(DAOModel) if model.__tablename__ in db_tables}
