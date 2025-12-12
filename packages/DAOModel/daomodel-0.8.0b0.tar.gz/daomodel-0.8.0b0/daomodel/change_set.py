from typing import Any, Optional

from daomodel.dao import Conflict
from daomodel.model_diff import ModelDiff, Preference, PreferenceRule, T
from daomodel.property_filter import DEFAULT


BASELINE_VALUE = Preference.LEFT
TARGET_VALUE = Preference.RIGHT


class Unresolved:
    """Represents an unresolved conflict within a ChangeSet.

    This is a simple wrapper for the target value to act as a label.
    """
    def __init__(self, target: Any):
        self.target = target

    def __eq__(self, other: Any) -> bool:
        return self.target == other.target if isinstance(other, Unresolved) else False

    def __hash__(self) -> int:
        return hash(self.target)

    def __repr__(self) -> str:
        return f'Unresolved(target={repr(self.target)})'


class Resolved:
    """Represents a resolved value for a specific conflict.

    Stores the original target as well as the resolution of a conflict in the context of a ChangeSet.
    """
    def __init__(self, target: Any, resolution: Any):
        self.target = target
        self.resolution = resolution

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Resolved):
            return self.target == other.target and self.resolution == other.resolution
        return False

    def __hash__(self) -> int:
        return hash((self.target, self.resolution))

    def __repr__(self) -> str:
        return f'Resolved(target={repr(self.target)}, resolution={repr(self.resolution)})'


class ChangeSet(ModelDiff):
    """A directional model diff with the left being the baseline and the right being the target.

    Unlike the standard ModelDiff, PK is excluded by default.

    The `conflict_resolution` argument allows users to define specific conflict resolution rules
    for handling differences between the baseline and target models. This parameter can
    accept field-specific resolution methods or a default resolution method for all fields.
    If no resolution can be determined, a `Conflict` exception is raised. Note: This resolution
    is only applicable for a Preference of `BOTH` as determined by `get_preferred()`.

    Examples:
    1. Field-Specific Resolution:
       ```
       def prefer_longer_name(values: list[str]):
           return max(values, key=len)

       ChangeSet(baseline, target, name=prefer_longer_name)
       ```

    2. Default Resolution:
       ```
       def conflict_str(values: list[Any]):
           return f'Unresolved conflict: {values}'

       ChangeSet(baseline, target, default=conflict_str)
       ```

    3. Mixed Resolution:
       ```
       ChangeSet(baseline, target, default=conflict_str, amount=sum)
       ```

    4. Using a Preference for Conflict Resolution:
       ```
       from model_diff import Preference

       ChangeSet(baseline, target, default=Preference.LEFT, status=Preference.RIGHT)
       ```

       or use the helper constants:
       ```
       from model_diff import BASELINE_VALUE, TARGET_VALUE

       ChangeSet(baseline, target, default=BASELINE_VALUE, status=TARGET_VALUE)
       ```

    5. Static Resolution:
       ```
       ChangeSet(baseline, target, name='Static Name', default='Default Value')
       ```

    View the test code for more examples.
    """
    def __init__(self,
                 baseline: T,
                 target: T,
                 include_pk: Optional[bool] = False,
                 **rules: PreferenceRule):
        self.conflict_resolution = {
            k[:-9]: rules.pop(k)
            for k in list(rules)
            if k.endswith('_conflict')
        }
        super().__init__(baseline, target, include_pk, **rules)
        self.modified_in_baseline = self.left.get_property_names(~DEFAULT)
        self.modified_in_target = self.right.get_property_names(~DEFAULT)

    def get_baseline(self, field: str) -> Any:
        """Fetches the value of the baseline model.

        :param field: The name of the field to fetch
        :return: The baseline value for the specified field
        :raises KeyError: if the field is invalid or otherwise not included in this diff
        """
        return self.get_left(field)

    def get_target(self, field: str) -> Any:
        """Fetches the value of the target model.

        :param field: The name of the field to fetch
        :return: The target value for the specified field
        :raises KeyError: if the field is invalid or otherwise not included in this diff
        """
        return self.get_right(field)

    def has_target_value(self, field: str) -> bool:
        """Returns True if the target value for the specified field exists"""
        return self.get_target(field) is not None

    def get_resolution(self, field: str) -> Any:
        """Returns the resolved value for the specified field.

        This will be the new value for the specified field if the change set were to be applied.

        :param field: The name of the field to fetch
        :return: The resolved value, which is the target value unless resolve_preferences() was called
        """
        target = self.get_target(field)
        return target.resolution if isinstance(target, Resolved) else target

    def get_preferred(self, field: str) -> Preference:
        try:
            return super().get_preferred(field)
        except NotImplementedError:
            if field in self.modified_in_baseline and field in self.modified_in_target:
                return Preference.BOTH
            elif field in self.modified_in_baseline:
                return Preference.LEFT
            else:
                return Preference.RIGHT

    def resolve_conflict(self, field: str) -> Preference | Any:
        """Defines how to handle conflicts between preferred values.

        A conflict occurs when both the baseline and target have unique meaningful values for a field.
        Conflict resolution guidelines are to be provided during construction if needed.
        Alternatively, the implementer may completely override this function in order to have full control.

        :param field: The field having a conflict
        :return: The result of the resolution which may be the baseline value, target value, or something new entirely
        :raises Conflict: if a resolution cannot be determined
        """
        def raise_conflict(*values: Any) -> Any:
            raise Conflict(msg=f'Unable to determine preferred result for {field}: {values}')

        default = self.conflict_resolution.get('default', raise_conflict)
        resolution_method = self.conflict_resolution.get(field, default)
        resolution = resolution_method(self.all_values(field)) if callable(resolution_method) else resolution_method

        preference = self.map_resolution_to_preference(resolution, field)
        if preference == Preference.NEITHER:
            preference = resolution
        return preference

    def resolve_preferences(self) -> 'ChangeSet':
        """Removes unwanted changes, preserving the meaningful values, regardless of them being from baseline or target

        :return: This ChangeSet to allow for chaining function calls
        :raises Conflict: if both baseline and target have meaningful values (unless resolve_conflict is overridden)
        """
        for field in list(self.keys()):
            preferred = self.get_preferred(field)
            if preferred == Preference.BOTH:
                preferred = self.resolve_conflict(field)
            match preferred:
                case Preference.NOT_APPLICABLE | Preference.NEITHER | Preference.BOTH:
                    self[field] = (self.get_baseline(field), Unresolved(self.get_target(field)))
                case Preference.LEFT:
                    del self[field]
                case Preference.RIGHT:
                    pass
                case _:
                    self[field] = (self.get_baseline(field), Resolved(self.get_target(field), preferred))
        return self

    def apply(self) -> T:
        """Enacts these changes upon the baseline.

        You will typically want to call resolve_preferences prior to this.
        """
        self.left.set_values(**{field: self.get_resolution(field) for field in self.keys()})
        return self.left


class MergeSet(ChangeSet):
    """Used for managing and resolving differences between a baseline and multiple target models.

    This class extends functionality of `ChangeSet` to handle scenarios where
    multiple target models are compared against a baseline. It initializes with
    a baseline model and one or more target models, identifying differences and
    allowing for conflict resolution between them. The class provides utilities
    to access and resolve values for specific fields across the baseline and
    targets.

    For more details regarding initialization, see ChangeSet.
    """
    def __init__(self, baseline: T, *targets: T, **rules: PreferenceRule):
        super().__init__(baseline, targets[0], **rules)
        self.right = targets
        for model in targets:
            self.modified_in_target += model.get_property_names(~DEFAULT)

        for model in targets:
            for k, v in ModelDiff(baseline, model).items():
                self[k] = (v[0], [None] * len(targets))

        for index, model in enumerate(targets):
            for k, v in self.items():
                v[1][index] = model.get_value_of(k)

    def has_target_value(self, field: str) -> bool:
        """Returns whether the target contains any non-None values."""
        return any(target is not None for target in self.get_target(field))

    def all_values(self, field: str) -> list[Any]:
        """Returns a list containing the baseline value followed by all target values for the specified field."""
        return [self.get_baseline(field)] + self.get_target(field)

    def resolve_conflict(self, field: str) -> tuple[Preference.RIGHT, int] | Any:
        resolution = super().resolve_conflict(field)
        if resolution is Preference.NEITHER:
            resolution = None

        target_values = self.get_target(field)
        if resolution in target_values:
            if len(target_values) == 1:
                return Preference.RIGHT
            else:
                return Preference.RIGHT, target_values.index(resolution)
        elif resolution is None:
            return Preference.NEITHER
        else:
            return resolution
