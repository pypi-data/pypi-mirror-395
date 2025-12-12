from enum import Enum
from typing import Any, Optional, Callable, TypeVar

from daomodel import DAOModel
from daomodel.property_filter import PK


class Preference(Enum):
    """Represents the preference of values in a model comparison.

    The available options are:
    - LEFT: Indicates preference for the 'left' side value.
    - RIGHT: Indicates preference for the 'right' side value.
    - NEITHER: Indicates that neither value is preferred.
    - BOTH: Indicates that both values are equally preferable.
    - NOT_APPLICABLE: Indicates that a preference does not apply in the given context i.e. the name field of two customers.
    """
    NOT_APPLICABLE = -1
    NEITHER = 0
    LEFT = 1
    RIGHT = 2
    BOTH = 3


PreferenceRuleFunction = Callable[[list], Preference] | Callable[[Any, Any, ...], Preference]
PreferenceRule = PreferenceRuleFunction | Preference


T = TypeVar('T', bound=DAOModel)


class ModelDiff(dict[str, tuple[Any, Any]]):
    """A dictionary wrapper of differing property values between two DAOModel instances.

    While designed to compare like models, it should work between different model types. Though that is untested.

    The keys in the dictionary represent the property names, and the value for the key contains each object value.
    Properties that share the same value across the objects are excluded.

    :param left: The left model instance used for comparison
    :param right: The right model instance used for comparison
    :param include_pk: True to include primary key values in the diff (False by default)
    :param preference_rules: Dictionary of field names to rules that define value preferences (see `execute_rule`)
    """
    def __init__(self,
                 left: T,
                 right: T,
                 include_pk: Optional[bool] = False,
                 **preference_rules: PreferenceRule):
        super().__init__()
        self.left: T = left
        self.right: T = right
        self.preference_rules = preference_rules

        filter_expr = [] if include_pk else [~PK]
        left_values = left.get_property_values(*filter_expr)
        right_values = right.get_property_values(*filter_expr)

        for k, v in left_values.items():
            if right_values[k] != v:
                self[k] = (v, right_values[k])

    def has_left_value(self, field: str) -> bool:
        """Returns True if the left value for the specified field exists"""
        return self.get_right(field) is not None

    def get_left(self, field: str) -> Any:
        """Fetches the value of the left object.

        :param field: The name of the field to fetch
        :return: The left value for the specified field
        :raises KeyError: if the field is invalid or otherwise not included in this diff
        """
        if field not in self:
            raise KeyError(f'{field} not found in diff.')
        return self.get(field)[0]

    def has_right_value(self, field: str) -> bool:
        """Returns True if the right value for the specified field exists"""
        return self.get_right(field) is not None

    def get_right(self, field: str) -> Any:
        """Fetches the value of the right object.

        :param field: The name of the field to fetch
        :return: The right value for the specified field
        :raises KeyError: if the field is invalid or otherwise not included in this diff
        """
        if field not in self:
            raise KeyError(f'{field} not found in diff.')
        return self.get(field)[1]

    def all_values(self, field: str) -> list[Any]:
        """Returns a list containing the values for the specified field, ordered from left to right."""
        return [self.get_left(field), self.get_right(field)]

    def get_preferred(self, field: str) -> Preference:
        """Determines which of the differing values is preferred.

        :param field: The name of the field
        :return: The Preference between the possible values
        :raises KeyError: if the field is invalid or otherwise not included in this diff
        :raises NotImplementedError: if there is no applicable preference rule provided for the field
        """
        if field not in self:
            raise KeyError(f'{field} not found in diff.')

        rule = self._find_rule(field)
        resolution = self.execute_rule(rule, self.all_values(field))
        preference = self.map_resolution_to_preference(resolution, field)

        return preference

    def _find_rule(self, field: str) -> Callable:
        """Finds the rule for determining the preferred value for the specified field."""
        def raise_error(*_) -> Any:
            raise NotImplementedError(f'No rule is defined to determine preference for {field}')
        return self.preference_rules.get(field, self.preference_rules.get('default', raise_error))

    @staticmethod
    def execute_rule(rule: PreferenceRule, values: list) -> Preference | Optional[Any]:
        """Conducts the rule for the specified field to determine the preferred value.

        A PreferenceRule may be a function or a static Preference i.e. LEFT, RIGHT, BOTH, NEITHER, or NOT_APPLICABLE.
        In the case of a function, it must accept multiple arguments, in the format of multiple args, *args, or a list.
        The return value of the function must be a Preference, one of the field values, or None.

        For example:
            def prefer_longer_name(values: list[str]) -> str:
                return max(values, key=len)

            def prefer_true(left: bool, right: bool) -> Preference:
                if left:
                    return Preference.LEFT
                elif right:
                    return Preference.RIGHT
                else
                    return Preference.NEITHER

        :param rule: The rule to execute
        :param values: The field values to apply the rule against
        :return: The resolved Preference or value based on the rule
        """
        if callable(rule):
            try:
                return rule(*values)
            except TypeError:
                return rule(values)
        return rule

    def map_resolution_to_preference(self, resolution: Preference | Optional[Any], field: str) -> Preference:
        """Converts a given resolution to its corresponding Preference

        :param resolution: The resolved value of Preference for the field
        :param field: The name of the field the resolution applies to
        :return: The appropriate Preference for the resolution
        """
        if isinstance(resolution, Preference):
            return resolution
        elif resolution == self.get_left(field):
            return Preference.LEFT
        elif resolution == self.get_right(field):
            return Preference.RIGHT
        else:
            return Preference.NEITHER
