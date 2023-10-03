from typing import Dict

from Disk import Disk
from HanoiTowers import HanoiTowers
from HanoiTowersTree import HanoiTowersTree
from Pilar import Pilar


class HanoiTowersGameBuilder:
    
    def create_new_game_tree(self, size: int=3, npilars: int=3) -> HanoiTowersTree:
        assert(size >= 1)
        assert(npilars >= 2)
        
        pillars: Dict[int, Pilar] = {i: Pilar(size=size) for i in range(npilars)}
        
        for i in range(size, 0, -1):
            pillars.get(0).push(disk=Disk(i))
        
        return HanoiTowersTree(item=HanoiTowers(pillars=pillars))