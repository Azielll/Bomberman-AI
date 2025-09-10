# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
from algorithms.astar import AStarAlgorithm
from algorithms.minimax import MinimaxAlgorithm
from algorithms.local_search import LocalSearchAlgorithm

class TestCharacter(CharacterEntity):
    def __init__(self, name, avatar, x, y):
        super().__init__(name, avatar, x, y)
        # Choose which algorithm to use
        self.algorithm = AStarAlgorithm()  # Change this to switch algorithms
    
    def do(self, wrld):
        # Get action from algorithm
        dx, dy = self.algorithm.get_action(wrld, self)
        
        # Execute the movement
        self.move(dx, dy)
