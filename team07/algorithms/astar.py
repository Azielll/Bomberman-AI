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
        Get next action using A* pathfinding with escape route priority.
        """
        # If no exit, do nothing
        if not wrld.exitcell:
            return (0, 0)
        
        # Check monster detection
        monsters = self.get_all_monsters(wrld)
        print(f"Character at ({character.x}, {character.y})")
        print(f"Found {len(monsters)} monsters")
        for i, (mx, my, dr) in enumerate(monsters):
            distance = max(abs(character.x - mx), abs(character.y - my))
            print(f"Monster {i} at ({mx}, {my}), detection_range={dr}, distance={distance}")
        
        # Check if monster is close (within detection range)
        if self.is_monster_close(wrld, character):
            print("ESCAPE MODE ACTIVATED!")
            # Priority: Escape from monster
            return self.find_escape_route(wrld, character)
        else:
            print("Using normal A* pathfinding")
        
        # Normal A* pathfinding to exit
        path = self.find_path(wrld, character)
        
        # If path found, return first move
        if path and len(path) > 1:
            next_pos = path[1]  # First step in path
            dx = next_pos[0] - character.x
            dy = next_pos[1] - character.y
            return (dx, dy)
        
        # No path found or already at goal
        return (0, 0)
    
    def is_valid_position(self, wrld, x, y, monsters=None):
        """Check if position is valid and walkable."""
        # Check bounds
        if x < 0 or x >= wrld.width() or y < 0 or y >= wrld.height():
            return False
        
        # Check if cell is walkable (empty or exit)
        if not (wrld.empty_at(x, y) or wrld.exit_at(x, y)):
            return False
        
        # Check if position is too close to any monster
        if self.is_too_close_to_monster(wrld, x, y, monsters):
            return False
        
        return True
    
    def get_all_monsters(self, wrld):
        """Get all monster positions in the world."""
        monsters = []
        for x in range(wrld.width()):
            for y in range(wrld.height()):
                monster_list = wrld.monsters_at(x, y)
                if monster_list:
                    for monster in monster_list:
                        # Get detection range, default to 2 if not available
                        detection_range = getattr(monster, 'rnge', 2)
                        monsters.append((x, y, detection_range))
        return monsters
    
    def is_too_close_to_monster(self, wrld, x, y, monsters=None):
        """Check if position is too close to any monster."""
        if monsters is None:
            monsters = self.get_all_monsters(wrld)
        for monster_x, monster_y, detection_range in monsters:
            # Calculate distance to monster
            distance = max(abs(x - monster_x), abs(y - monster_y))
            # Only avoid if very close (within 1 cell of detection range)
            # This allows getting closer but not too close
            if distance <= 1:
                return True
        return False
    
    def is_monster_close(self, wrld, character):
        """Check if any monster is close to character (within detection range)."""
        monsters = self.get_all_monsters(wrld)
        for monster_x, monster_y, detection_range in monsters:
            # Calculate distance to monster
            distance = max(abs(character.x - monster_x), abs(character.y - monster_y))
            # If within detection range, monster is close
            if distance <= detection_range:
                return True
        return False
    
    def find_escape_route(self, wrld, character):
        """Find the best escape route when monster is close."""
        monsters = self.get_all_monsters(wrld)
        if not monsters:
            return (0, 0)
        
        # Find the closest monster
        closest_monster = None
        closest_distance = float('inf')
        for monster_x, monster_y, detection_range in monsters:
            distance = max(abs(character.x - monster_x), abs(character.y - monster_y))
            if distance < closest_distance:
                closest_distance = distance
                closest_monster = (monster_x, monster_y)
        
        if not closest_monster:
            return (0, 0)
        
        monster_x, monster_y = closest_monster
        
        # Try all 8 directions and find the one that maximizes distance
        best_direction = (0, 0)
        best_distance = 0
        
        for dx, dy in self.get_neighbors():
            new_x = character.x + dx
            new_y = character.y + dy
            
            # Check if this direction is valid
            if self.is_valid_position(wrld, new_x, new_y, monsters):
                # Calculate distance to monster from new position
                new_distance = max(abs(new_x - monster_x), abs(new_y - monster_y))
                
                # If this direction gives more distance, it's better
                if new_distance > best_distance:
                    best_distance = new_distance
                    best_direction = (dx, dy)
        
        # If we found a good direction, use it
        if best_direction != (0, 0):
            return best_direction
        
        # Fallback: try any valid direction
        for dx, dy in self.get_neighbors():
            new_x = character.x + dx
            new_y = character.y + dy
            if self.is_valid_position(wrld, new_x, new_y, monsters):
                return (dx, dy)
        
        # If no escape route found, don't move
        return (0, 0)
    

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
        # Get monsters once to avoid repeated scanning
        monsters = self.get_all_monsters(wrld)
        
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
                if not self.is_valid_position(wrld, neighbor_x, neighbor_y, monsters):
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
    
    
    