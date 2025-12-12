from datetime import datetime, timezone
from typing import TypeVar, Generic, Any, Optional

from sqlmodel import Field
from sqlalchemy import Column
from sqlmodel.main import FieldInfo

from daomodel.util import reference_of

T = TypeVar('T')


class Identifier(Generic[T]):
    """A type annotation for primary key fields.

    Usage:
        class MyModel(DAOModel, table=True)
            id: Identifier[str]
            ...
    """
    pass


class Unsearchable(Generic[T]):
    """A type annotation to mark a field as not searchable.

    Usage:
        class MyModel(DAOModel, table=True)
            ...
            internal_notes: Unsearchable[str]
            ...
    """
    pass


class Protected(Generic[T]):
    """A type annotation for foreign key fields with RESTRICT delete behavior.

    This prevents the referenced object from being deleted if it is still referenced.

    Usage:
        class MyModel(DAOModel, table=True)
            ...
            parent: Protected[ParentModel]
            ...
    """
    pass


class ReferenceTo(FieldInfo):
    """Shortcut for defining a foreign key field.

    This class is used by the metaclass to set up foreign key constraints.
    It stores the target information, which the metaclass can then use
    to create the appropriate foreign key constraints and configurations.

    :param target: Either a string in the format 'table.column', a Column object, or a model attribute
    :param **kwargs: Additional arguments to pass to Field

    Usage:
        class MyModel(DAOModel, table=True)
            ...
            other_id: int = ReferenceTo('other_model.id')
            # or
            other_id: int = ReferenceTo(OtherModel.id)
    """
    def __init__(self, target: Optional[str|Column|Any] = None, **kwargs: Any):
        if 'foreign_key' not in kwargs:
            kwargs['foreign_key'] = (
                target if isinstance(target, str) else
                reference_of(target) if target is not None else
                None
            )
        super().__init__(**kwargs)


class no_case_str(str):
    """Marker type for a case-insensitive string column."""
    pass


def utc_now():
    """Returns the current UTC time with timezone information."""
    return datetime.now(timezone.utc)


CurrentTimestampField = Field(default_factory=utc_now)
AutoUpdatingTimestampField = Field(default_factory=utc_now, sa_column_kwargs={'onupdate': utc_now})
