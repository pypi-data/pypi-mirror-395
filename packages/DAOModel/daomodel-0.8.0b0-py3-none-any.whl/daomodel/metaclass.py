from typing import Dict, Any, Tuple, Type, get_origin, get_args, Union, Optional, List, ForwardRef
import inspect
import uuid
from sqlmodel.main import SQLModelMetaclass, Field, FieldInfo, RelationshipInfo, Relationship
from sqlalchemy import ForeignKey, JSON, String

from daomodel.util import reference_of, UnsupportedFeatureError
from daomodel.fields import no_case_str, Identifier, Unsearchable, Protected, ReferenceTo


class Annotation:
    """A utility class to help manage a type-annotated field."""
    def __init__(self, field_name: str, field_type: type[Any]):
        self.name = field_name

        self.modifiers = set()
        for modifier in [Unsearchable, Identifier, Protected]:
            if get_origin(field_type) is modifier:
                self.modifiers.add(modifier)
                field_type = get_args(field_type)[0]
        if get_origin(field_type) is Union:
            args = get_args(field_type)
            if len(args) == 2 and args[1] is type(None):
                self.modifiers.add(Optional)
                field_type = args[0]

        self.type = field_type
        self.args = {}

    def is_private(self) -> bool:
        """Check whether the annotation is for a private field."""
        return self.name.startswith('_')

    def has_modifier(self, modifier: Any) -> bool:
        """Check whether the annotation has a specified modifier.

        :param modifier: The modifier to check for, valid modifiers are Unsearchable, Identifier, Protected, Optional
        :return: True if the annotation has the modifier
        """
        return modifier in self.modifiers

    def is_relationship(self) -> bool:
        """Check whether the annotation is a defined relationship to another model"""
        origin = get_origin(self.type)
        if origin not in (list, List):
            return False
        args = get_args(self.type)
        return args and len(args) == 1 and (isinstance(args[0], (str, ForwardRef)) or inspect.isclass(args[0]))

    def is_dao_model(self) -> bool:
        """Check whether the annotation is a DAOModel."""
        return inspect.isclass(self.type) and 'DAOModel' in (base.__name__ for base in inspect.getmro(self.type))

    def __getitem__(self, key: str) -> Any:
        return self.args.get(key)

    def __setitem__(self, key: str, value: Any) -> None:
        self.args[key] = value


class ClassDictHelper:
    """A utility class to help manage class dictionary and annotations in metaclasses."""
    def __init__(self, class_dict: dict[str, Any]):
        self.class_dict = class_dict

    @property
    def annotations(self) -> dict[str, Any]:
        return self.class_dict.get('__annotations__', {})

    def set_annotation(self, field: Annotation) -> None:
        """Set an annotation for a field, automatically handling optional types if nullable is True."""
        self.annotations[field.name] = Union[field.type, None] if field['nullable'] else field.type

    @property
    def fields(self) -> list[Annotation]:
        fields = [Annotation(field_name, field_type) for field_name, field_type in self.annotations.items()]
        return [field for field in fields if not field.is_private() and not self.is_relationship(field)]

    def is_relationship(self, field: Annotation) -> bool:
        return field in self and isinstance(self[field], RelationshipInfo)

    def is_reference(self, field: Annotation) -> bool:
        return field in self and isinstance(self[field], ReferenceTo)

    def add_unsearchable(self, field: Annotation) -> None:
        """Mark a field as unsearchable within in the class dictionary."""
        self.class_dict.setdefault('_unsearchable', set()).add(field.name)

    def __getitem__(self, field: Annotation) -> Any:
        return self.class_dict.get(field.name)

    def __setitem__(self, field: Annotation, value: Any) -> None:
        self.class_dict[field.name] = value

    def __contains__(self, field: Annotation) -> bool:
        return field.name in self.class_dict


class DAOModelMetaclass(SQLModelMetaclass):
    """A metaclass for DAOModel that adds support for modifiers and special typing within annotations."""
    def __new__(
            cls,
            name: str,
            bases: Tuple[Type[Any], ...],
            class_dict: Dict[str, Any],
            **kwargs: Any,
    ) -> Any:
        model = ClassDictHelper(class_dict)

        for field in model.fields:
            if field.is_relationship():
                model[field] = Relationship()
                continue
            cls._process_field_modifiers(field, model)
            cls._process_field_type(field, model)
            model.set_annotation(field)
            cls._process_existing_field(field, model)

        return super().__new__(cls, name, bases, class_dict, **kwargs)

    @classmethod
    def _process_field_modifiers(cls, field: Annotation, model: ClassDictHelper) -> None:
        """Process field modifiers like Unsearchable, Identifier, and Optional."""
        if field.has_modifier(Unsearchable):
            model.add_unsearchable(field)
        if field.has_modifier(Identifier):
            field['primary_key'] = True
        field['nullable'] = field.has_modifier(Optional)

    @classmethod
    def _process_field_type(cls, field: Annotation, model: ClassDictHelper) -> None:
        """Process field type-specific settings."""
        if field.type is uuid.UUID:
            field['default_factory'] = uuid.uuid4
        elif field.type is dict:
            field['sa_type'] = JSON
        elif field.type is no_case_str:
            field.type = str
            field['sa_type'] = String(collation='NOCASE')
        elif model.is_reference(field) or field.is_dao_model():
            cls._process_reference_field(field, model)

    @classmethod
    def _process_reference_field(cls, field: Annotation, model: ClassDictHelper) -> None:
        """Process fields that reference other models, AKA foreign key fields."""
        if field.is_dao_model():
            cls._process_dao_model_reference(field)
        else:
            field['foreign_key'] = getattr(model[field], 'foreign_key')

        field['ondelete'] = cls._determine_ondelete_behavior(field, model)

        field['sa_column_args'] = [
            ForeignKey(
                field['foreign_key'],
                onupdate='CASCADE',
                ondelete=field['ondelete']
            )
        ]

    @classmethod
    def _process_dao_model_reference(cls, field: Annotation) -> None:
        """Process a field that directly references a DAOModel."""
        first_pk = next(iter(field.type.get_pk()))
        if len(field.type.get_pk()) != 1:
            raise UnsupportedFeatureError(
                f'Cannot auto map to composite key of {field.type.__name__}. Use '
                f'Reference(str) instead. i.e. field: int = Reference("{first_pk}")'
            )
        field.type = field.type.__annotations__[first_pk.name]
        field['foreign_key'] = reference_of(first_pk)

    @classmethod
    def _determine_ondelete_behavior(cls, field: Annotation, model: ClassDictHelper) -> str:
        """Determine the appropriate ondelete behavior for a foreign key."""
        existing_value = model[field] if field in model else None
        explicitly_set_value = getattr(existing_value, 'ondelete', None)

        return (
            explicitly_set_value if type(explicitly_set_value) is str else
            'RESTRICT' if field.has_modifier(Protected) else
            'SET NULL' if field['nullable'] else
            'CASCADE'
        )

    @classmethod
    def _process_existing_field(cls, field: Annotation, model: ClassDictHelper) -> None:
        """Process existing field values in the class dictionary."""
        if field in model:
            existing_field = model[field]
            if isinstance(existing_field, FieldInfo):
                for key, value in field.args.items():
                    setattr(existing_field, key, value)
                return
            else:
                field['default'] = existing_field
        model[field] = Field(**field.args)
