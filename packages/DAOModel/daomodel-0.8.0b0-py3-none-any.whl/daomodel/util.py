from typing import Iterable, Any

from sqlalchemy import Column


class MissingInput(Exception):
    """Indicates that required information was not provided."""
    def __init__(self, detail: str):
        self.detail = detail


class InvalidArgumentCount(Exception):
    """Indicates that an incorrect number of arguments was provided."""
    def __init__(self, expected: int, got: int, context: str = None):
        self.detail = f'Expected {expected} values, got {got}'
        if context:
            self.detail += f' for {context}'


class UnsupportedFeatureError(Exception):
    """Indicates that a feature is not yet supported.

    If you think the feature should be implemented, please open an issue on GitHub.
    """
    def __init__(self, detail: str):
        self.detail = detail + (' Note: This functionality is not yet supported. '
                                'Please submit a request through GitHub if you would like it implemented.')


def reference_of(column: Column) -> str:
    """
    Prepares a str reference of a column.

    :param column: The column to convert
    :return: The 'table.column' notation of the Column
    """
    return f'{column.table.name}.{column.name}'


def names_of(properties: Iterable[Column]) -> list[str]:
    """
    Reduces Columns to just their names.

    :param properties: A group of Columns
    :return: A list of names matching the order of the Columns provided
    """
    return [p.name for p in properties]


def values_from_dict(*keys: Any, **values: Any) -> tuple:
    """Pulls specific values from a dictionary.

    :param keys: The keys to read from the dict
    :param values: The dictionary containing the values
    :return: A tuple of values read from the dict, in the same order as keys
    """
    result = []
    for key in keys:
        if key in values:
            result.append(values[key])
        else:
            raise MissingInput(f'Requested key {key} not found in dictionary')
    return tuple(result)


def retain_in_dict(d: dict[Any, Any], *keys: Any) -> dict[Any, Any]:
    """Filters a dictionary to specified keys.

    The source dict remains unmodified.

    :param d: The dictionary to filter down
    :param keys: The target keys for the new dict
    :return: The reduced values as a new dict
    """
    return {key: d[key] for key in keys if key in d}


def remove_from_dict(d: dict[Any, Any], *keys: Any) -> dict[Any, Any]:
    """Removes specified key/value pairs from a dictionary.

    The source dict remains unmodified.

    :param d: The dictionary to adjust
    :param keys: The keys to remove from the dict
    :return: The modified values as a new dict
    """
    return {k: v for k, v in d.items() if k not in keys}


def next_id() -> None:
    """Indicates to the model that an id should be auto-incremented"""
    return None
