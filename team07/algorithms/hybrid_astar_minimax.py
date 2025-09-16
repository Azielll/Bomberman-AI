"""
Hybrid A* + Minimax algorithm for Bomberman AI
Combines A* pathfinding with Minimax for adversarial scenarios
"""
import heapq
import math
import random

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

class HybridAStarMinimax:
    """
    Hybrid A* + Minimax algorithm implementation.
    Uses A* for general pathfinding and Minimax for multi-monster scenarios.
    """
    
    def __init__(self):
        pass
    
    def get_action(self, wrld, character):
        """
        Get next action using hybrid A* + Minimax approach.
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
        
        # Strategy selection based on monster situation
        if self.are_multiple_monsters_close(wrld, character):
            print("MULTIPLE MONSTERS CLOSE - Using Minimax strategy")
            return self.minimax_escape_route(wrld, character)
        elif self.is_monster_close(wrld, character):
            print("SINGLE MONSTER CLOSE - Using multi-step escape")
            return self.find_escape_route(wrld, character)
        else:
            print("NO MONSTERS CLOSE - Using A* pathfinding")
        
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
    
    def are_multiple_monsters_close(self, wrld, character):
        """Check if multiple monsters are within detection range."""
        monsters = self.get_all_monsters(wrld)
        close_monsters = 0
        
        for monster_x, monster_y, detection_range in monsters:
            distance = max(abs(character.x - monster_x), abs(character.y - monster_y))
            if distance <= detection_range:
                close_monsters += 1
        
        return close_monsters >= 2
    
    def find_escape_route(self, wrld, character):
        """Find the best escape route when monster is close using multi-step planning."""
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
        
        # Multi-step escape planning: evaluate each direction by looking 2-3 steps ahead
        best_direction = (0, 0)
        best_score = -1
        
        for dx, dy in self.get_neighbors():
            new_x = character.x + dx
            new_y = character.y + dy
            
            # For escape mode, use a more permissive validity check
            if self.is_escape_valid_position(wrld, new_x, new_y, monsters, monster_x, monster_y):
                # Evaluate this direction by looking ahead 2-3 steps
                score = self.evaluate_escape_direction(wrld, new_x, new_y, monster_x, monster_y, monsters, steps=3)
                
                if score > best_score:
                    best_score = score
                    best_direction = (dx, dy)
        
        # If we found a good direction, use it
        if best_direction != (0, 0):
            return best_direction
        
        # Fallback: try any valid direction with permissive check
        for dx, dy in self.get_neighbors():
            new_x = character.x + dx
            new_y = character.y + dy
            if self.is_escape_valid_position(wrld, new_x, new_y, monsters, monster_x, monster_y):
                return (dx, dy)
        
        # If no escape route found, don't move
        return (0, 0)
    
    def is_escape_valid_position(self, wrld, x, y, monsters, monster_x, monster_y):
        """More permissive validity check for escape mode."""
        # Check boundaries
        if x < 0 or x >= wrld.width() or y < 0 or y >= wrld.height():
            return False
        
        # Check if position is walkable (not a wall)
        if not (wrld.empty_at(x, y) or wrld.exit_at(x, y)):
            return False
        
        # For escape mode, allow positions that are adjacent to monsters if they're moving away
        distance_to_monster = max(abs(x - monster_x), abs(y - monster_y))
        if distance_to_monster <= 1:
            # Only allow if we're moving away from the monster
            # This is a simplified check - in practice, we want to allow movement that increases distance
            return True  # Allow adjacent positions in escape mode
        
        # For other positions, use normal monster avoidance
        return not self.is_too_close_to_monster(wrld, x, y, monsters)
    
    def evaluate_escape_direction(self, wrld, start_x, start_y, monster_x, monster_y, monsters, steps=3):
        """Evaluate an escape direction by looking multiple steps ahead."""
        score = 0
        current_x, current_y = start_x, start_y
        
        for step in range(steps):
            # Calculate distance to monster from current position
            distance_to_monster = max(abs(current_x - monster_x), abs(current_y - monster_y))
            
            # Base score: distance from monster (higher is better)
            score += distance_to_monster * (steps - step)  # Weight earlier steps more
            
            # Check if this position is valid
            if not self.is_valid_position(wrld, current_x, current_y, monsters):
                # Penalty for invalid positions
                score -= 10 * (steps - step)
                break
            
            # Check if we're getting closer to the exit
            distance_to_exit = max(abs(current_x - wrld.exitcell[0]), abs(current_y - wrld.exitcell[1]))
            if step > 0:  # Only check progress after first step
                score += 2  # Small bonus for making progress toward exit
            
            # Predict where monster will move next (simplified: assume it moves toward character)
            if step < steps - 1:  # Don't predict on last step
                predicted_monster_x = monster_x + (1 if current_x > monster_x else -1 if current_x < monster_x else 0)
                predicted_monster_y = monster_y + (1 if current_y > monster_y else -1 if current_y < monster_y else 0)
                
                # Update monster position for next iteration
                monster_x, monster_y = predicted_monster_x, predicted_monster_y
                
                # Find next best move from current position
                best_next_move = self.find_best_next_escape_move(wrld, current_x, current_y, monster_x, monster_y, monsters)
                if best_next_move:
                    current_x += best_next_move[0]
                    current_y += best_next_move[1]
                else:
                    # No valid next move - this direction leads to a dead end
                    score -= 20
                    break
        
        return score
    
    def find_best_next_escape_move(self, wrld, x, y, monster_x, monster_y, monsters):
        """Find the best next move from a given position during escape planning."""
        best_direction = None
        best_distance = -1
        
        for dx, dy in self.get_neighbors():
            new_x = x + dx
            new_y = y + dy
            
            if self.is_valid_position(wrld, new_x, new_y, monsters):
                distance = max(abs(new_x - monster_x), abs(new_y - monster_y))
                if distance > best_distance:
                    best_distance = distance
                    best_direction = (dx, dy)
        
        return best_direction
    
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
        
        print(f"A* Pathfinding: Start={start}, Goal={goal}")
        
        # If already at goal, return just the start position
        if start == goal:
            print("Already at goal!")
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
                print("A* Pathfinding: Path found!")
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
        print("A* Pathfinding: No path found!")
        return None

    # Minimax related functions
    def minimax_escape_route(self, wrld, character, depth=3):
        """Use minimax to find best escape route considering monster responses."""
        monsters = self.get_all_monsters(wrld)
        best_move = None
        best_score = float('-inf')
        
        for dx, dy in self.get_neighbors():
            new_x = character.x + dx
            new_y = character.y + dy
            
            if self.is_valid_position(wrld, new_x, new_y, monsters):
                new_pos = (new_x, new_y)
                monster_positions = [(mx, my) for mx, my, _ in monsters]
                
                score = self.minimax(wrld, new_pos, monster_positions, depth, False)
                
                if score > best_score:
                    best_score = score
                    best_move = (dx, dy)
        
        return best_move or (0, 0)
    
    def minimax(self, wrld, character_pos, monster_positions, depth, is_maximizing):
        """Minimax algorithm for adversarial decision making."""
        if depth == 0:
            return self.evaluate_position(wrld, character_pos, monster_positions)
        
        if is_maximizing:
            # Character's turn - maximize score
            max_score = float('-inf')
            
            for dx, dy in self.get_neighbors():
                new_x = character_pos[0] + dx
                new_y = character_pos[1] + dy
                
                if self.is_valid_position(wrld, new_x, new_y, []):
                    new_pos = (new_x, new_y)
                    score = self.minimax(wrld, new_pos, monster_positions, depth - 1, False)
                    max_score = max(max_score, score)
            
            return max_score
        else:
            # Monsters' turn - minimize score
            min_score = float('inf')
            
            # Simulate monster movements
            for i, (monster_x, monster_y) in enumerate(monster_positions):
                # Predict monster movement toward character
                predicted_monster_pos = self.predict_monster_movement(monster_x, monster_y, character_pos)
                
                # Update monster positions
                new_monster_positions = monster_positions.copy()
                new_monster_positions[i] = predicted_monster_pos
                
                score = self.minimax(wrld, character_pos, new_monster_positions, depth - 1, True)
                min_score = min(min_score, score)
            
            return min_score
    
    def predict_monster_movement(self, monster_x, monster_y, target_pos):
        """Predict where a monster will move next."""
        target_x, target_y = target_pos
        
        # Calculate direction toward target
        dx = 0
        dy = 0
        
        if monster_x < target_x:
            dx = 1
        elif monster_x > target_x:
            dx = -1
            
        if monster_y < target_y:
            dy = 1
        elif monster_y > target_y:
            dy = -1
        
        return (monster_x + dx, monster_y + dy)
    
    def evaluate_position(self, wrld, character_pos, monster_positions):
        """Evaluate a position for the minimax algorithm."""
        char_x, char_y = character_pos
        
        # Distance to exit (higher is better)
        exit_distance = max(abs(char_x - wrld.exitcell[0]), abs(char_y - wrld.exitcell[1]))
        
        # Distance to closest monster (higher is better)
        min_monster_distance = float('inf')
        for monster_x, monster_y in monster_positions:
            distance = max(abs(char_x - monster_x), abs(char_y - monster_y))
            min_monster_distance = min(min_monster_distance, distance)
        
        # Safety score (avoid being cornered)
        safety_score = self.calculate_safety_score(wrld, character_pos, monster_positions)
        
        # Weighted evaluation
        score = exit_distance * 0.3 + min_monster_distance * 0.5 + safety_score * 0.2
        
        return score
    
    def calculate_safety_score(self, wrld, character_pos, monster_positions):
        """Calculate how safe a position is from being cornered."""
        char_x, char_y = character_pos
        safety_score = 0
        
        # Check available escape routes
        escape_routes = 0
        for dx, dy in self.get_neighbors():
            new_x = char_x + dx
            new_y = char_y + dy
            
            if self.is_valid_position(wrld, new_x, new_y, []):
                # Check if this direction leads away from monsters
                distance_improvement = 0
                for monster_x, monster_y in monster_positions:
                    current_distance = max(abs(char_x - monster_x), abs(char_y - monster_y))
                    new_distance = max(abs(new_x - monster_x), abs(new_y - monster_y))
                    distance_improvement += new_distance - current_distance
                
                if distance_improvement > 0:
                    escape_routes += 1
        
        safety_score = escape_routes * 10  # Bonus for having escape routes
        
        return safety_score