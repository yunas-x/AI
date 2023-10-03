from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

from operator import eq

T = TypeVar('T')

@dataclass(frozen=True)
class Anything():
    def __eq__(self, other):
        return True

    def __le__(self, other):
        return True

    def __ge__(self, other):
        return True

    def __ne__(self, other):
        return True

@dataclass(frozen=True)
class FieldSelector(Generic[T]):
    name: str
    action: Callable = eq
    value: T | Anything = Anything()
  
