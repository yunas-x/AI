from collections import deque
from typing import Callable, List, Self
from copy import deepcopy

from HanoiTowers import HanoiTowers
from Metadata import Metadata

class HanoiTowersTree:

    def __init__(self,  item: HanoiTowers, metadata: Metadata = Metadata(), parent: Self=None, children: List[Self]=None):
        self.children: List[HanoiTowersTree] = children
        self.item: HanoiTowers = item
        self.metadata: Metadata = metadata
        self.parent: HanoiTowersTree = parent
    
    def children_create(self) -> List[Self]:
        children: List[HanoiTowersTree] = list()
        for i in range(self.item.numtowers):
            for j in range(i+1, self.item.numtowers):
                new_children = self.__get_children_on_move(i, j)
                children.extend(new_children)
        
        return children
    
    def __get_children_on_move(self, _from: int, _to: int) -> List[Self]:
        
        children: List[HanoiTowersTree] = list()
        parents = self.parents
        
        new_state, is_moved = self.__make_move(_from, _to)
        is_parent = new_state.is_in(parents)
            
        if is_moved and not is_parent:
            children.append(new_state)
        
        new_state, is_moved = self.__make_move(_to, _from)
        is_parent = new_state.is_in(parents)
        
        if is_moved and not is_parent:
            children.append(new_state)
            
        return children

    def is_in(self, __in: list[Self]):
        if not __in:
            return False
        return any(self.item == tree.item for tree in __in)

    @property
    def parents(self) -> List[Self]:
        temp = self
        parents: List[HanoiTowersTree] = list()
        while temp.parent:
            parents.append(temp.parent)
            temp = temp.parent

        return parents
    
    @property
    def metrics(self) -> int:
        return self.item.score + self.metadata.step

    def __make_move(self, _from: int, _to: int):
        new_item = deepcopy(self.item)
        new_meta = Metadata(False, self.metadata.step+1)
        child = HanoiTowersTree(item=new_item, metadata=new_meta, parent=self)
        is_moved = child.item.move_disk(_from, _to)
        return child, is_moved
    
    def __repr__(self) -> str:
        __repr = ""
        to_visit: deque[HanoiTowersTree] = deque()
        to_visit.append(self)
        
        while to_visit:
            this = to_visit.popleft()
            __repr += this.item.to_tabbed_str(num=this.metadata.step)
            __repr += "\n\n"
            if this.children:
                to_visit.extendleft(this.children)

        return __repr
    
    @property
    def str_view(self) -> str:
        return self.item

    @property
    def leaves(self) -> list[Self]:
        to_visit: deque[HanoiTowersTree] = deque()
        to_visit.append(self)
        leaves: List[HanoiTowersTree] = list()
        
        while to_visit:
            this = to_visit.popleft()
            if this.children:
                to_visit.extendleft(this.children)
            else:
                leaves.append(this)

        return leaves
    
    @property
    def best_leaf(self) -> Self:
        leaves = self.leaves
        
        key: Callable[[HanoiTowersTree], HanoiTowersTree] = lambda leaf: leaf.metrics
            
        best_leaf: HanoiTowersTree = min(leaves, key=key)
        best_leaf.metadata.is_best = True
        return best_leaf  