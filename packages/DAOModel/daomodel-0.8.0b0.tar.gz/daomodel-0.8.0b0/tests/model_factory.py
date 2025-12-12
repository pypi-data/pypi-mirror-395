from typing import Any
import uuid

from daomodel import DAOModel
from daomodel.fields import Identifier


def create_test_model(field_type: Any = None, field_name: str = 'value', base_model: type = None, inherited: bool = False) -> type[DAOModel]:
    """Dynamically creates a model with the specified field type.

    :param field_type: The type annotation for the field, or exclude to only have an id field
    :param field_name: The name of the field (default: 'value')
    :param base_model: Optional base model to inherit from
    :param inherited: True if the type field should belong to a parent model that is extended by the returned model
    :return: A dynamically created DAOModel class
    """
    annotations = {'id': Identifier[int]}
    if field_type is not None:
        annotations[field_name] = field_type

    model = type(
        f'DynamicModel{uuid.uuid4().hex[:8].capitalize()}',
        (base_model or DAOModel,),
        {
            '__annotations__': annotations,
            '__module__': 'tests.field_tests.model_factory'
        },
        table=not inherited
    )
    if inherited:
        model = create_test_model(str, field_name='child_field', base_model=model)

    return model
