"""
Expectimax algorithm for Bomberman AI
"""
from .base import BombermanAlgorithm

class ExpectimaxAlgorithm(BombermanAlgorithm):
    """
    Expectimax algorithm implementation.
    """
    
    def __init__(self, depth=3):
        super().__init__("Expectimax")
        self.depth = depth
    
    def get_action(self, wrld, character):
        """
        Get next action using expectimax algorithm.
        """
        # TODO: Implement expectimax logic
        return (0, 0)
