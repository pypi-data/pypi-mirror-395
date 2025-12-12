from typing import Any

from sqlalchemy import ColumnElement
from sqlmodel import or_, and_


class ConditionOperator:
    """A utility class to easily generate common expressions"""
    def __init__(self, *values: Any):
        self.values = values

    def get_expression(self, column: ColumnElement) -> ColumnElement:
        """Builds and returns the appropriate expression.

        :param column: The column on which to evaluate
        :return: the expression
        """
        raise NotImplementedError('Must implement `get_expression` in subclass')


class GreaterThan(ConditionOperator):
    def get_expression(self, column: ColumnElement) -> ColumnElement:
        return column > self.values[0]


class GreaterThanEqualTo(ConditionOperator):
    def get_expression(self, column: ColumnElement) -> ColumnElement:
        return column >= self.values[0]


class LessThan(ConditionOperator):
    def get_expression(self, column: ColumnElement) -> ColumnElement:
        return column < self.values[0]


class LessThanEqualTo(ConditionOperator):
    def get_expression(self, column: ColumnElement) -> ColumnElement:
        return column <= self.values[0]


class Between(ConditionOperator):
    def get_expression(self, column: ColumnElement) -> ColumnElement:
        lower_bound, upper_bound = self.values
        return and_(column >= lower_bound, column <= upper_bound)


class AnyOf(ConditionOperator):
    def get_expression(self, column: ColumnElement) -> ColumnElement:
        return or_(*[column == value for value in self.values])


class NoneOf(ConditionOperator):
    def get_expression(self, column: ColumnElement) -> ColumnElement:
        return and_(*[column != value for value in self.values])


class IsSet(ConditionOperator):
    """Expression to filter to rows that have a value set for a specific Column"""
    def get_expression(self, column: ColumnElement) -> ColumnElement:
        return or_(column == True, and_(column != None, column != False))


class NotSet(ConditionOperator):
    """Expression to filter to rows that have no value set for a specific Column"""
    def get_expression(self, column: ColumnElement) -> ColumnElement:
        return or_(column == False, column == None)


is_set = IsSet()
not_set = NotSet()
