from typing import Any

from daomodel.util import names_of


class PropertyFilter:
    """Base class for property filters with operator overloading support."""
    
    def evaluate(self, model: Any) -> set[str]:
        """Evaluates this filter against the model and returns matching property names.
        
        :param model: The model to evaluate against
        :return: A set of property names that match this filter
        """
        raise NotImplementedError('Must implement `evaluate` in subclass')
    
    def __and__(self, other):
        """Overload the & operator to create an AND filter."""
        return AndFilter(self, other)
    
    def __or__(self, other):
        """Overload the | operator to create an OR filter."""
        return OrFilter(self, other)
    
    def __invert__(self):
        """Overload the ~ operator to create a NOT filter."""
        return NotFilter(self)


class AndFilter(PropertyFilter):
    """Combines multiple filters with AND logic."""
    
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def evaluate(self, model) -> set[str]:
        """Returns properties that match ALL of the combined filters."""
        return self.left.evaluate(model).intersection(self.right.evaluate(model))
    
    def __repr__(self):
        return f'({self.left} & {self.right})'


class OrFilter(PropertyFilter):
    """Combines multiple filters with OR logic."""
    
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def evaluate(self, model) -> set[str]:
        """Returns properties that match ANY of the combined filters."""
        return self.left.evaluate(model).union(self.right.evaluate(model))
    
    def __repr__(self):
        return f'({self.left} | {self.right})'


class NotFilter(PropertyFilter):
    """Negates a filter."""
    
    def __init__(self, operand):
        self.operand = operand
    
    def evaluate(self, model) -> set[str]:
        """Returns properties that do NOT match the given filter."""
        all_props = set(names_of(model.get_properties()))
        return all_props.difference(self.operand.evaluate(model))
    
    def __repr__(self):
        return f'~{self.operand}'


class BasicPropertyFilter(PropertyFilter):
    """Filter for specific property categories."""
    
    def __init__(self, name):
        self.name = name
    
    def evaluate(self, model) -> set[str]:
        """Returns properties that match this category."""
        if self.name == 'ALL':
            return set(names_of(model.get_properties()))
        elif self.name == 'PK':
            return set(model.get_pk_names())
        elif self.name == 'FK':
            return set(names_of(model.get_fk_properties()))
        elif self.name == 'DEFAULT':
            return ALL.evaluate(model).difference(model.model_dump(exclude_defaults=True))
        elif self.name == 'NONE':
            return ALL.evaluate(model).difference(model.model_dump(exclude_none=True))
        return set()
    
    def __repr__(self):
        return f'{self.name}'


ALL = BasicPropertyFilter('ALL')
PK = BasicPropertyFilter('PK')
FK = BasicPropertyFilter('FK')
DEFAULT = BasicPropertyFilter('DEFAULT')
NONE = BasicPropertyFilter('NONE')
