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
from algorithms.q_learning import ApproximateQLearning

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
                        print("Detected Variant 1 - Using Approximate Q-Learning Algorithm")
                        q_agent = ApproximateQLearning()
                        
                        # Check if we're in training mode by looking at the call stack
                        training_mode = False
                        frame = caller_frame
                        while frame:
                            if 'train_q_learning' in frame.f_code.co_filename:
                                training_mode = True
                                break
                            frame = frame.f_back
                        
                        q_agent.set_training_mode(training_mode)
                        q_agent.weights_file = "weights_variant1.json"
                        q_agent.load_weights()
                        return q_agent
                    elif 'variant2' in filename.lower():
                        print("Detected Variant 2 - Using Approximate Q-Learning Algorithm")
                        q_agent = ApproximateQLearning()
                        q_agent.set_training_mode(False)  # Test mode FIRST
                        q_agent.weights_file = "weights_variant2.json"
                        q_agent.load_weights()
                        return q_agent
                    elif 'variant3' in filename.lower():
                        print("Detected Variant 3 - Using Approximate Q-Learning Algorithm")
                        q_agent = ApproximateQLearning()
                        q_agent.set_training_mode(False)  # Test mode FIRST
                        q_agent.weights_file = "weights_variant3.json"
                        q_agent.load_weights()
                        return q_agent
                    elif 'variant4' in filename.lower():
                        print("Detected Variant 4 - Using Approximate Q-Learning Algorithm")
                        q_agent = ApproximateQLearning()
                        q_agent.set_training_mode(False)  # Test mode FIRST
                        q_agent.weights_file = "weights_variant4.json"
                        q_agent.load_weights()
                        return q_agent
                    elif 'variant5' in filename.lower():
                        print("Detected Variant 5 - Using Approximate Q-Learning Algorithm")
                        q_agent = ApproximateQLearning()
                        q_agent.set_training_mode(False)  # Test mode FIRST
                        q_agent.weights_file = "weights_variant5.json"
                        q_agent.load_weights()
                        return q_agent
                caller_frame = caller_frame.f_back
        finally:
            del frame
        
        # Fallback: check command line arguments
        for arg in sys.argv:
            if 'variant' in arg.lower():
                print("Detected variant context - Using Approximate Q-Learning Algorithm")
                q_agent = ApproximateQLearning()
                q_agent.set_training_mode(False)  # Test mode
                return q_agent
        
        # Default to Q-Learning for all variants
        print("Default: Using Approximate Q-Learning Algorithm")
        q_agent = ApproximateQLearning()
        q_agent.set_training_mode(False)  # Test mode
        return q_agent
    
    def do(self, wrld):
        # Get action from algorithm
        action = self.algorithm.get_action(wrld, self)
        
        # Execute the action
        if action == "BOMB":
            # Place bomb
            self.place_bomb()
        else:
            # Movement action
            dx, dy = action
            self.move(dx, dy)
