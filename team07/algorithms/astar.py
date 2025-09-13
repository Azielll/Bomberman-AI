"""
A* pathfinding algorithm for Bomberman AI
"""
from .base import BombermanAlgorithm
import heapq

class Node:
    """Node for A* pathfinding"""
    def __init__(self, x, y, g_cost, h_cost, parent=None):
        self.x = x
        self.y = y
        self.g_cost = g_cost
        self.h_cost = h_cost
        self.f_cost = g_cost + h_cost
        self.parent = parent
    
    def __lt__(self, other):
        return self.f_cost < other.f_cost
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.x, self.y))

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
        # If no exit, do nothing
        if not wrld.exitcell:
            return (0, 0)
        
        # Find path to exit
        path = self.find_path(wrld, character)
        
        # If path found, return first move
        if path and len(path) > 1:
            next_pos = path[1]  # First step in path
            dx = next_pos[0] - character.x
            dy = next_pos[1] - character.y
            return (dx, dy)
        
        # No path found or already at goal
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
    
    def add_to_open_set(self, open_set, node):
        """Add a node to the open set (priority queue)."""
        heapq.heappush(open_set, node)
    
    def get_best_node(self, open_set):
        """Get the node with lowest f_cost from open set."""
        if not open_set:
            return None
        return heapq.heappop(open_set)
    
    def reconstruct_path(self, goal_node):
        """Reconstruct path from goal node back to start using parent pointers."""
        path = []
        current = goal_node
        
        # Trace back from goal to start
        while current is not None:
            path.append((current.x, current.y))
            current = current.parent
        
        # Reverse to get path from start to goal
        path.reverse()
        return path
    
    def find_path(self, wrld, character):
        """
        Find path from character position to exit using A*.
        Returns list of (x, y) coordinates representing the path.
        """
        # Basic setup
        start = (character.x, character.y)
        goal = wrld.exitcell
        
        # If already at goal, return just the start position
        if start == goal:
            return [start]
        
        # Initialize open and closed sets
        open_set = []           # Priority queue of nodes to explore
        closed_set = set()      # Set of positions we've already explored
        
        # Create start node and add to open set
        start_g_cost = 0  # Cost from start to start is 0
        start_h_cost = self.heuristic(start, goal)  # Heuristic cost to goal
        start_node = Node(start[0], start[1], start_g_cost, start_h_cost)
        
        # Add start node to open set
        self.add_to_open_set(open_set, start_node)
        
        # Main A* search loop
        while open_set:
            # Get the best node (lowest f_cost)
            current_node = self.get_best_node(open_set)
            if not current_node:
                break
                
            # Check if we reached the goal
            if (current_node.x, current_node.y) == goal:
                # Reconstruct path from goal to start
                path = self.reconstruct_path(current_node)
                return path
            
            # Add current position to closed set
            closed_set.add((current_node.x, current_node.y))
            
            # Explore neighbors
            for dx, dy in self.get_neighbors():
                neighbor_x = current_node.x + dx
                neighbor_y = current_node.y + dy
                neighbor_pos = (neighbor_x, neighbor_y)
                
                # Skip if not valid position
                if not self.is_valid_position(wrld, neighbor_x, neighbor_y):
                    continue
                
                # Skip if already explored
                if neighbor_pos in closed_set:
                    continue
                
                # Calculate costs for this neighbor
                neighbor_g_cost = current_node.g_cost + 1  # Each move costs 1
                neighbor_h_cost = self.heuristic(neighbor_pos, goal)
                neighbor_node = Node(neighbor_x, neighbor_y, neighbor_g_cost, neighbor_h_cost, current_node)
                
                # Add to open set
                self.add_to_open_set(open_set, neighbor_node)
            
        # No path found
        return None
    
    
    