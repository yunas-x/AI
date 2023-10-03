from HanoiTowersGameBuilder import HanoiTowersGameBuilder
from HanoiTowersTree import HanoiTowersTree

import seaborn as sns

class HanoiTowersGame:
    
    @property
    def is_over(self) -> bool:
        return any(leaf.item.is_final for leaf in self.__tree.leaves)
    
    def __init__(self, size: int=3, npilars: int=3) -> None:
        self.__tree: HanoiTowersTree = HanoiTowersGameBuilder().create_new_game_tree(size=size, npilars=npilars)
        
    def solve(self) -> int:
        nbest = 0
        nleaves = 1
        while not self.is_over:
            nleaves += self.__move()
            nbest += 1
        return nbest / nleaves
        
    def __repr__(self) -> str:
        return repr(self.__tree)    
    
    def __move(self) -> int:
        best_leaf = self.__tree.best_leaf
        print(self.__tree.best_leaf.metrics)
        children = best_leaf.children_create()
        best_leaf.children = children
        return len(children)
           
        
if __name__ == "__main__":
    game = HanoiTowersGame(size=3)
    metrics = game.solve()
    print(game)
    print(metrics)
    print(game.is_over)
    #sns.lineplot(x=game.history.keys(), y=game.history.values())
        
    
    
