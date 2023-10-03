from collections import deque
from typing import Self
from Disk import Disk


class Pilar:
    
    def __init__(self, size: int):
        assert(size >= 1)
        self._disks: deque[Disk] = deque(maxlen=size)
        
    def push(self, disk: Disk):
        if not self._disks:
            self._disks.append(disk)
        elif self._disks[-1].size > disk.size:
            self._disks.append(disk)
        else:
            raise ValueError()
            
    def pull(self) -> Disk:
        if not self._disks:
            raise ValueError()
        else:
            return self._disks.pop()
        
    def can_pull(self) -> bool:
        return len(self._disks) > 0
    
    def can_push(self, disk: Disk) -> bool:
        return len(self._disks) == 0 or self._disks[-1].size > disk.size
        
    def __len__(self):
        return len(self._disks)
    
    def __repr__(self):
        disks = "\n".join(map(str, reversed(self._disks)))
        return f"Pilar size={len(self)}\n{disks}"
    
    def __eq__(self, __value: Self) -> bool:
        return self._disks == __value._disks

    def to_tabbed_str(self, n=0):
        t = "\n" + "\t" * n
        s = ""
        for val in reversed(self._disks):
            s += t + str(val)
        return f"{t}Pilar size={len(self)}\n{s}"