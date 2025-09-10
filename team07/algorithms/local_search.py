from .base import BombermanAlgorithm

class LocalSearchAlgorithm(BombermanAlgorithm):
    """
    Local search algorithm implementation.
    """
    
    def __init__(self, search_type="hill_climbing"):
        super().__init__("Local Search")
        self.search_type = search_type
    
    def get_action(self, wrld, character):
        """
        Get next action using local search.
        """
        # TODO: Implement local search logic
        return (0, 0)
