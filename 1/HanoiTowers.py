from ast import Dict
from typing import Self
from Pilar import Pilar


class HanoiTowers:
    
    def __init__(self, pillars: dict[int, Pilar]):
        """
        Args:
            pillars (Dict[int, Pilar]): integers only from 0 following to N
        """
        
        self._pillars: Dict[int, Pilar] = pillars
    
    @property
    def numtowers(self):
        return len(self._pillars)
    
    @property
    def numdisks(self) -> int:
        return sum(len(v) for v in self._pillars.values())
    
    def __len__(self) -> str:
        return len(self._pillars)
    
    def __repr__(self) -> str:
        return "\n\n".join(map(str, self._pillars.values()))
    
    def to_tabbed_str(self, num=0):
        s = ""
        for val in self._pillars.values():
            s += val.to_tabbed_str(n=num)
        return s
    
    @property
    def is_final(self) -> bool:
        return len(self._pillars.get(self.numtowers-1)) == self.numdisks 
    
    @property
    def score(self) -> int:     
        # Subtract numbers of first pillars disks and last pillars disks
        return len(self._pillars.get(0)) - len(self._pillars.get(len(self) - 1)) * 2
        #return len(self._pillars.get(0)) - len(self._pillars.get(len(self) - 1))

    def __eq__(self, __value: Self) -> bool:
        return self._pillars.values() == __value._pillars.values()

        
    def move_disk(self, _from: int, _to: int) -> bool:
        __to = self._pillars.get(_to)
        __from = self._pillars.get(_from)
        
        if not __from.can_pull():
            return False
        
        disk = __from.pull()
        
        if __to.can_push(disk):
            __to.push(disk=disk)
            return True
        else:
            __from.push(disk=disk)
            return False
