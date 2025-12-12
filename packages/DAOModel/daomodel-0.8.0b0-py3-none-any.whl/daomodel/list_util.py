from typing import TypeVar, Any, Iterable, Optional


T = TypeVar('T', bound=Any)


def ensure_iter(elements: Iterable[T] | T) -> Iterable[T] | list[T]:
    """Ensures that the provided argument is iterable.

    Single, non-Iterable items are converted to a single-item list.
    In this context, a str is not considered to be Iterable.

    :param elements: The input that may or may not be Iterable
    :return: The provided Iterable or a single item list
    """
    if not isinstance(elements, Iterable) or type(elements) is str:
        elements = [elements]
    return elements


def in_order(original: Iterable[T], order: list[T]) -> list[T]:
    """Returns provided items as an ordered list.

    Repeated items will be deduplicated.
    Items not defined within the order will be excluded.
    The order is allowed to contain extraneous items that aren't applicable to the provided items.

    :param original: The (likely unordered) collection of items
    :param order: The defined order of items
    :return: a new list of the items following the defined order
    """
    return [item for item in order if item in original]


def strip_whitespace(values: list[T]) -> list[T]:
    """Trim leading and trailing whitespace from strings in a list."""
    return [value.strip() for value in values]


def exclude_falsy(values: list[T]) -> list[T]:
    """Returns a list of only the truthy values (excluding None, '', 0, False, etc)."""
    return [v for v in values if v]


def dedupe(original: list[T], keep_last=False) -> list[T]:
    """Creates a filtered copy of a list that does not include duplicates.

    :param original: The list to filter
    :param keep_last: True to keep the last occurrence of a duplicate, otherwise the first occurrence will be kept
    :return: a new list that maintains order but is guaranteed to have no duplicates
    """
    if keep_last:
        return dedupe(original[::-1])[::-1]
    else:
        return list(dict.fromkeys(original))


def most_frequent(values: list[T]) -> T:
    """Determines the most frequently occurring value within the provided iterable.

    In the case of a tie (multiple values with the same highest frequency),
    the function returns the first value encountered with that frequency.

    :param values: A list containing values to evaluate
    :return: The most common value from the provided iterable
    """
    return max(values, key=values.count)


def longest(values: list[str]) -> Optional[str]:
    """Finds the longest string in a list of strings.

    In the case of a tie (multiple values of the same length),
    the function returns the first value encountered with that length.

    :param values: A list containing strings to check
    :return: The longest string from the provided list.
    """
    try:
        return max(values, key=len)
    except ValueError:
        return None


def first_str_with(substring: str, strings: list[str]) -> Optional[str]:
    """Returns the first str that contains the given substring.

    :param substring: The substring to search for.
    :param strings: One or more strings to check.
    :return: The first string (if any) that contains the substring.
    """
    for s in strings:
        if substring in s:
            return s
    return None


def first(values: list[T]) -> Optional[T]:
    """Returns the first truthy value.

    :param values: Values to evaluate
    :return: First truthy value found, or None if no truthy values exist
    """
    for value in values:
        if value:
            return value
    return None


def last(values: list[T]) -> Optional[T]:
    """Returns the last truthy value.

    :param values: Values to evaluate
    :return: Last truthy value found, or None if no truthy values exist
    """
    return first(values[::-1])