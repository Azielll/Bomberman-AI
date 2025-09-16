# This is necessary to find the main code
import sys
sys.path.insert(0, '../Bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
from algorithms.hybrid_astar_minimax import HybridAStarMinimax
from algorithms.astar import AStarAlgorithm
from algorithms.expectimax import ExpectimaxAlgorithm
from algorithms.minimax import MinimaxAlgorithm
from algorithms.local_search import LocalSearchAlgorithm

class TestCharacter(CharacterEntity):
    def __init__(self, name, avatar, x, y):
        super().__init__(name, avatar, x, y)
        # Choose algorithm based on variant
        self.algorithm = self._choose_algorithm()
    
    def _choose_algorithm(self):
        """Choose algorithm based on the variant being run."""
        import inspect
        import sys
        
        # Get the calling file name to determine variant
        frame = inspect.currentframe()
        try:
            # Go up the call stack to find the calling file
            caller_frame = frame.f_back
            while caller_frame:
                filename = caller_frame.f_code.co_filename
                if 'variant' in filename.lower():
                    # Extract variant number from filename
                    if 'variant1' in filename.lower():
                        print("Detected Variant 1 - Using A* Algorithm")
                        return ExpectimaxAlgorithm()
                    elif 'variant2' in filename.lower():
                        print("Detected Variant 2 - Using A* Algorithm")
                        return ExpectimaxAlgorithm()
                    elif 'variant3' in filename.lower():
                        print("Detected Variant 3 - Using A* Algorithm")
                        return AStarAlgorithm()
                    elif 'variant4' in filename.lower():
                        print("Detected Variant 4 - Using A* Algorithm")
                        return AStarAlgorithm()
                    elif 'variant5' in filename.lower():
                        print("Detected Variant 5 - Using Hybrid A* + Minimax Algorithm")
                        return HybridAStarMinimax()
                caller_frame = caller_frame.f_back
        finally:
            del frame
        
        # Fallback: check command line arguments
        for arg in sys.argv:
            if 'variant5' in arg.lower() or 'test_variant5' in arg.lower():
                print("Detected Variant 5 context - Using Hybrid A* + Minimax Algorithm")
                return HybridAStarMinimax()
        
        # Default to A* for variants 1-4, Hybrid for variant 5
        print("Default: Using A* Algorithm (for Variants 1-4)")
        return AStarAlgorithm()
    
    def do(self, wrld):
        # Get action from algorithm
        dx, dy = self.algorithm.get_action(wrld, self)
        
        # Execute the movement
        self.move(dx, dy)
