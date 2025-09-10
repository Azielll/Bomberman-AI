"""
A* pathfinding algorithm for Bomberman AI
"""
from .base import BombermanAlgorithm

class AStarAlgorithm(BombermanAlgorithm):
    """
    A* pathfinding algorithm implementation.
    """
    
    def __init__(self):
        super().__init__("A* Pathfinding")
    
    def get_action(self, wrld, character):
        """
        Get next action using A* pathfinding.
        """
        # Step 3: Test heuristic function
        self.test_heuristic_function(wrld, character)
        
        # For now, just do nothing
        return (0, 0)
    
    def is_valid_position(self, wrld, x, y):
        """Check if position is valid and walkable."""
        # Check bounds
        if x < 0 or x >= wrld.width() or y < 0 or y >= wrld.height():
            return False
        
        # Check if cell is walkable (empty or exit)
        return wrld.empty_at(x, y) or wrld.exit_at(x, y)
    

    def get_neighbors(self):
        """Get all 8-directional neighbors."""
        return [(-1, -1), (-1, 0), (-1, 1),
                (0, -1),           (0, 1),
                (1, -1),  (1, 0),  (1, 1)]


    def heuristic(self, pos1, pos2):
        """Chebyshev distance heuristic (optimal for 8-directional movement)."""
        dx = abs(pos1[0] - pos2[0])
        dy = abs(pos1[1] - pos2[1])
        return max(dx, dy)
        def test_heuristic_function(self, wrld, character):
        """
        Step 3: Test heuristic function with known examples.
        """
        print("=== HEURISTIC TESTING ===")
        
        # Test 1: Current position to exit
        if wrld.exitcell:
            exit_x, exit_y = wrld.exitcell
            current_distance = self.heuristic((character.x, character.y), (exit_x, exit_y))
            print(f"Current position ({character.x}, {character.y}) to exit ({exit_x}, {exit_y}): {current_distance}")
        
        # Test 2: Known examples
        test_cases = [
            ((0, 0), (0, 0), 0),      # Same position
            ((0, 0), (1, 0), 1),      # One step right
            ((0, 0), (0, 1), 1),      # One step down
            ((0, 0), (1, 1), 1),      # One step diagonal
            ((0, 0), (3, 0), 3),      # Three steps right
            ((0, 0), (0, 3), 3),      # Three steps down
            ((0, 0), (3, 3), 3),      # Three steps diagonal
            ((0, 0), (2, 3), 3),      # Mixed: max(2,3) = 3
            ((0, 0), (5, 2), 5),      # Mixed: max(5,2) = 5
        ]
        
        print("\nTesting known examples:")
        all_correct = True
        for pos1, pos2, expected in test_cases:
            result = self.heuristic(pos1, pos2)
            correct = result == expected
            all_correct = all_correct and correct
            status = "✓" if correct else "✗"
            print(f"  {status} {pos1} to {pos2}: {result} (expected {expected})")
        
        print(f"\nAll tests {'PASSED' if all_correct else 'FAILED'}")
        
        # Test 3: Check all neighbors from current position
        if wrld.exitcell:
            exit_x, exit_y = wrld.exitcell
            print(f"\nNeighbor distances from ({character.x}, {character.y}) to exit ({exit_x}, {exit_y}):")
            for dx, dy in self.get_neighbors():
                new_x, new_y = character.x + dx, character.y + dy
                if 0 <= new_x < wrld.width() and 0 <= new_y < wrld.height():
                    distance = self.heuristic((new_x, new_y), (exit_x, exit_y))
                    print(f"  ({new_x}, {new_y}): {distance}")
        
        print("=== END HEURISTIC TESTING ===\n")

