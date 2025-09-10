"""
Minimax algorithm for Bomberman AI
"""
from .base import BombermanAlgorithm

class MinimaxAlgorithm(BombermanAlgorithm):
    """
    Minimax algorithm implementation.
    """
    
    def __init__(self, depth=3):
        super().__init__("Minimax")
        self.depth = depth
    
    def get_action(self, wrld, character):
        """
        Get next action using minimax algorithm.
        """
        # TODO: Implement minimax logic
        return (0, 0)
