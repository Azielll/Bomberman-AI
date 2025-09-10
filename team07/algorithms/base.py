class BombermanAlgorithm:
    """
    Base class for all Bomberman AI algorithms.
    """
    
    def __init__(self, name="Unknown Algorithm"):
        self.name = name
    
    def get_action(self, wrld, character):
        """
        Get the next action for the character given the world state.
        
        Args:
            wrld: SensedWorld object containing current game state
            character: CharacterEntity object representing the AI character
            
        Returns:
            tuple: (dx, dy) where:
                - dx, dy: movement direction (-1, 0, 1)
        """
        # Default: do nothing
        return (0, 0)
