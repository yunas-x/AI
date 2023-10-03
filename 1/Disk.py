from dataclasses import dataclass
from typing import Self

@dataclass(frozen=True)
class Disk:
    size: int
    
    def __str__(self):
        return "=" * self.size
    
    def __repr__(self):
        return str(self)
    
    def __eq__(self, __value: Self) -> bool:
        return self.size == __value.size