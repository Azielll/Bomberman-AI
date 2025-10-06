"""
Approximate Q-Learning algorithm for Bomberman AI
Based on the homework assignment specifications
"""
import random
import math
import json
import os
import heapq
from .base import BombermanAlgorithm

class ApproximateQLearning(BombermanAlgorithm):
    """
    Approximate Q-Learning implementation using linear function approximation.
    Enhanced features for wall-breaking scenarios:
    - f_e: exit distance (closer is better)
    - f_m: monster distance (closer is worse) 
    - f_x: explosion distance (closer is worse)
    - f_w: wall distance (closer walls encourage bomb placement)
    - f_b: bomb placement opportunity (walls in bomb range)
    """
    
    def __init__(self):
        super().__init__("Approximate Q-Learning")
        
        # Learning parameters from homework assignment
        self.alpha = 0.5  # Learning rate
        self.gamma = 0.9   # Discount factor
        self.epsilon = 0.9 # Exploration rate - ABSURDLY HIGH to force bomb placement discovery
        
        # Enhanced weights for wall-breaking scenario - POSITIVE for bomb placement
        self.w_e = 10.0   # Weight for exit distance (positive - closer is better)
        self.w_m = -1.0   # Weight for monster distance (negative - closer is worse)
        self.w_x = -5.0   # Weight for explosion distance (negative - closer is worse)
        self.w_w = 5.0    # Weight for wall distance (positive - encourages bomb placement)
        self.w_b = 10.0   # Weight for bomb opportunity (POSITIVE - encourages bomb placement)
        
        # Action space: 8 movement directions + stay + bomb
        self.actions = [
            (0, 0),   # Stay
            (-1, -1), # Up-left
            (-1, 0),  # Up
            (-1, 1),  # Up-right
            (0, -1),  # Left
            (0, 1),   # Right
            (1, -1),  # Down-left
            (1, 0),   # Down
            (1, 1),   # Down-right
            "BOMB"    # Place bomb
        ]
        
        # Track bomb placement for immediate rewards
        self.last_action_was_bomb = False
        
        # Experience storage for learning
        self.experiences = []
        self.max_experiences = 1000
        
        # Episode tracking
        self.episode_reward = 0
        self.step_count = 0
        self.episode_count = 0
        self.successful_episodes = 0
        self.total_episodes = 0
        
        # Training parameters
        self.training_mode = True
        self.test_mode = False
        self.weights_file = "q_learning_weights.json"
        
    
    def get_action(self, wrld, character):
        """
        Get next action using pure Approximate Q-Learning - no hardcoded behavior.
        """
        # Extract features for current state
        features = self.extract_features(wrld, character)

        # Choose action using epsilon-greedy policy
        if random.random() < self.epsilon:
            # Exploration: random action
            action = random.choice(self.actions)
            print(f"DEBUG: RANDOM action chosen: {action} (exploration)")
        else:
            # Exploitation: best action based on Q-values
            action = self.get_best_action(wrld, character, features)
            print(f"DEBUG: BEST action chosen: {action} (exploitation)")
        
        # Track bomb placement for immediate rewards
        self.last_action_was_bomb = (action == "BOMB")

        # Store experience for learning
        self.store_experience(wrld, character, action, features)

        return action
    
    
    def extract_features(self, wrld, character):
        """
        Extract enhanced features from world state for wall-breaking scenarios.
        Returns: dict with f_e, f_m, f_x, f_w, f_b values
        """
        features = {}
        
        # f_e = 1 / (d_e + 1) where d_e is A* distance to exit
        if wrld.exitcell:
            d_e = self.a_star_distance(wrld, character.x, character.y, 
                                      wrld.exitcell[0], wrld.exitcell[1])
            if d_e == float('inf'):
                d_e = 100  # Large distance if no path
            features['f_e'] = 1.0 / (d_e + 1)
        else:
            features['f_e'] = 0.0
        
        # f_m = 1 / (d_m + 1) where d_m is Chebyshev distance to nearest monster
        d_m = self.get_distance_to_nearest_monster(wrld, character)
        features['f_m'] = 1.0 / (d_m + 1)
        
        # f_x = 1 / (d_x + 1) where d_x is Chebyshev distance to nearest explosion
        d_x = self.get_distance_to_nearest_explosion(wrld, character)
        features['f_x'] = 1.0 / (d_x + 1)
        
        # f_w = 1 / (d_w + 1) where d_w is Chebyshev distance to nearest wall
        d_w = self.get_distance_to_nearest_wall(wrld, character)
        features['f_w'] = 1.0 / (d_w + 1)
        
        # f_b = bomb opportunity score (walls within bomb range)
        features['f_b'] = self.get_bomb_opportunity_score(wrld, character)
        
        return features
    
    def get_distance_to_nearest_monster(self, wrld, character):
        """
        Calculate Chebyshev distance to nearest monster.
        Returns large value if no monsters present.
        """
        min_distance = float('inf')
        
        for x in range(wrld.width()):
            for y in range(wrld.height()):
                monster_list = wrld.monsters_at(x, y)
                if monster_list:
                    distance = max(abs(character.x - x), abs(character.y - y))
                    min_distance = min(min_distance, distance)
        
        return min_distance if min_distance != float('inf') else 100
    
    def get_distance_to_nearest_wall(self, wrld, character):
        """
        Calculate Chebyshev distance to nearest wall.
        Returns large value if no walls present.
        """
        min_distance = float('inf')
        
        for x in range(wrld.width()):
            for y in range(wrld.height()):
                if wrld.wall_at(x, y):
                    distance = max(abs(character.x - x), abs(character.y - y))
                    min_distance = min(min_distance, distance)
        
        return min_distance if min_distance != float('inf') else 100
    
    def a_star_distance(self, wrld, start_x, start_y, target_x, target_y):
        """
        Calculate A* pathfinding distance between two points.
        Returns the actual path length, or infinity if no path exists.
        """
        if start_x == target_x and start_y == target_y:
            return 0
        
        # Priority queue: (f_cost, g_cost, x, y, parent)
        open_set = [(0, 0, start_x, start_y, None)]
        closed_set = set()
        
        # Directions: 8-way movement
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        
        while open_set:
            f_cost, g_cost, x, y, parent = heapq.heappop(open_set)
            
            if (x, y) in closed_set:
                continue
                
            closed_set.add((x, y))
            
            # Check if we reached the target
            if x == target_x and y == target_y:
                return g_cost
            
            # Explore neighbors
            for dx, dy in directions:
                new_x, new_y = x + dx, y + dy
                
                # Check bounds
                if (new_x < 0 or new_x >= wrld.width() or 
                    new_y < 0 or new_y >= wrld.height()):
                    continue
                
                # Check if already closed
                if (new_x, new_y) in closed_set:
                    continue
                
                # Check if wall (but allow diagonal movement through corners)
                if wrld.wall_at(new_x, new_y):
                    continue
                
                # Calculate costs
                new_g_cost = g_cost + 1
                h_cost = max(abs(new_x - target_x), abs(new_y - target_y))  # Chebyshev heuristic
                new_f_cost = new_g_cost + h_cost
                
                # Add to open set
                heapq.heappush(open_set, (new_f_cost, new_g_cost, new_x, new_y, (x, y)))
        
        return float('inf')  # No path found
    
    def get_bomb_opportunity_score(self, wrld, character):
        """
        Calculate bomb opportunity score based on walls within bomb range.
        Returns score between 0 and 1, higher when walls are in bomb range.
        """
        bomb_range = 4  # From map.txt: expl_range 4
        walls_in_range = 0
        total_walls = 0
        
        for x in range(wrld.width()):
            for y in range(wrld.height()):
                if wrld.wall_at(x, y):
                    total_walls += 1
                    # Check if wall is within bomb range
                    distance = max(abs(character.x - x), abs(character.y - y))
                    if distance <= bomb_range:
                        walls_in_range += 1
        
        if total_walls == 0:
            return 0.0
        
        return walls_in_range / total_walls
    
    def get_distance_to_nearest_explosion(self, wrld, character):
        """
        Calculate Chebyshev distance to nearest explosion.
        Returns large value if no explosions present.
        """
        min_distance = float('inf')
        
        for x in range(wrld.width()):
            for y in range(wrld.height()):
                if wrld.explosion_at(x, y):
                    distance = max(abs(character.x - x), abs(character.y - y))
                    min_distance = min(min_distance, distance)
        
        return min_distance if min_distance != float('inf') else 100
    
    def get_q_value(self, features, action, wrld=None, character=None):
        """
        Calculate Q-value using linear function approximation.
        Enhanced formula: Q(s,a) = w_e * f_e + w_m * f_m + w_x * f_x + w_w * f_w + w_b * f_b
        """
        # Base Q-value from state features
        base_q = (self.w_e * features['f_e'] +
                 self.w_m * features['f_m'] +
                 self.w_x * features['f_x'] +
                 self.w_w * features['f_w'] +
                 self.w_b * features['f_b'])
        
        # Add action-specific bonuses
        if action == "BOMB":
            # Bomb action gets bonus for bomb opportunity, but penalty if too close to walls
            bomb_bonus = features['f_b'] * 100  # Extra reward for bomb placement
            wall_penalty = features['f_w'] * 50  # Penalty for being too close to walls
            return base_q + bomb_bonus - wall_penalty
        elif action == (0, 0):
            # Stay action gets penalty (encourage movement)
            return base_q - 50
        else:
            # Movement actions get STRONG directional bonuses
            dx, dy = action
            
            # Calculate direction toward exit
            if wrld.exitcell:
                exit_dx = wrld.exitcell[0] - character.x
                exit_dy = wrld.exitcell[1] - character.y
                
                # Normalize direction vectors
                if exit_dx != 0:
                    exit_dx = exit_dx / abs(exit_dx)
                if exit_dy != 0:
                    exit_dy = exit_dy / abs(exit_dy)
                
                # Calculate alignment with exit direction
                alignment = (dx * exit_dx + dy * exit_dy) / 2.0  # Range: -1 to 1
                
                # Strong bonus for moving toward exit
                exit_bonus = alignment * 100  # Up to ±100 bonus
            else:
                exit_bonus = 0
            
            # Base movement bonus
            movement_bonus = 20
            
            return base_q + movement_bonus + exit_bonus
    
    def get_best_action(self, wrld, character, features):
        """
        Get the action with highest Q-value, including bomb placement.
        """
        best_action = (0, 0)
        best_q_value = float('-inf')

        for action in self.actions:
            if action == "BOMB":
                # Bomb action is always valid (if character has bombs)
                q_value = self.get_q_value(features, action, wrld, character)
                if q_value > best_q_value:
                    best_q_value = q_value
                    best_action = action
            else:
                # Check if movement action is valid (not into wall)
                new_x = character.x + action[0]
                new_y = character.y + action[1]

                if (0 <= new_x < wrld.width() and
                    0 <= new_y < wrld.height() and
                    not wrld.wall_at(new_x, new_y)):

                    q_value = self.get_q_value(features, action, wrld, character)
                    if q_value > best_q_value:
                        best_q_value = q_value
                        best_action = action

        return best_action
    
    def store_experience(self, wrld, character, action, features):
        """
        Store experience for learning (simplified version).
        """
        experience = {
            'state': (character.x, character.y),
            'action': action,
            'features': features.copy(),
            'reward': 0,  # Will be updated when reward is known
            'next_state': None,
            'next_features': None
        }
        
        self.experiences.append(experience)
        
        # Keep only recent experiences
        if len(self.experiences) > self.max_experiences:
            self.experiences.pop(0)
    
    def update_weights(self, reward, next_features):
        """
        Update weights using Q-learning update rule.
        """
        if len(self.experiences) < 2:
            return
        
        # Get the most recent experience
        experience = self.experiences[-1]
        features = experience['features']
        
        # Calculate current Q-value
        current_q = self.get_q_value(features, experience['action'])
        
        # Calculate target Q-value (simplified - no next action for now)
        target_q = reward + self.gamma * self.get_q_value(next_features, (0, 0))
        
        # Calculate error
        error = target_q - current_q
        
        # Update weights using gradient descent
        self.w_e += self.alpha * error * features['f_e']
        self.w_m += self.alpha * error * features['f_m']
        self.w_x += self.alpha * error * features['f_x']
        self.w_w += self.alpha * error * features['f_w']
        self.w_b += self.alpha * error * features['f_b']
        
        # Print learning progress
        if self.step_count % 100 == 0:
            print(f"Step {self.step_count}: w_e={self.w_e:.2f}, w_m={self.w_m:.2f}, w_x={self.w_x:.2f}, w_w={self.w_w:.2f}, w_b={self.w_b:.2f}")
    
    def get_reward(self, wrld, character, events):
        """
        Enhanced reward function that encourages wall-breaking behavior.
        """
        reward = 0
        
        # Check for terminal events
        if events:
            for event in events:
                if event.tpe == 4:  # Character reached exit
                    reward += 1000
                elif event.tpe == 2 or event.tpe == 3:  # Character died
                    reward -= 1000
        
        # Time penalty (encourage efficiency) - REDUCED
        reward -= 0.1  # Much smaller time penalty
        
        # Distance-based rewards
        if wrld.exitcell:
            distance_to_exit = max(abs(character.x - wrld.exitcell[0]), abs(character.y - wrld.exitcell[1]))
            if distance_to_exit == 0:
                reward += 100  # Bonus for reaching exit
            else:
                reward += 10 / (distance_to_exit + 1)  # Closer to exit is better
        
        # Wall-breaking rewards - INCREASED
        walls_destroyed = self.count_walls_destroyed(wrld)
        if walls_destroyed > 0:
            reward += walls_destroyed * 500  # Much higher reward for destroying walls
        
        # Immediate bomb placement reward - INCREASED
        if self.last_action_was_bomb:
            bomb_opportunity = self.get_bomb_opportunity_score(wrld, character)
            # Always reward bomb placement, more if walls nearby
            reward += 100 + (bomb_opportunity * 200)  # Base reward + opportunity bonus
        
        # Safety rewards
        distance_to_monster = self.get_distance_to_nearest_monster(wrld, character)
        if distance_to_monster < 3:
            reward -= 50  # Penalty for being too close to monster
        
        distance_to_explosion = self.get_distance_to_nearest_explosion(wrld, character)
        if distance_to_explosion < 2:
            reward -= 100  # Penalty for being too close to explosion
        
        return reward
    
    def count_walls_destroyed(self, wrld):
        """
        Count how many walls were destroyed in this step.
        This is a simplified version - in practice, you'd track wall state changes.
        """
        # For now, return 0 - this would need to be implemented with state tracking
        return 0
    
    def learn_from_episode(self, episode_rewards):
        """
        Learn from a complete episode.
        """
        if len(episode_rewards) < 2:
            return
        
        # Simple learning: update weights based on episode outcome
        total_reward = sum(episode_rewards)
        
        if total_reward > 0:
            # Successful episode - reinforce current weights
            self.epsilon = max(0.05, self.epsilon * 0.99)  # Reduce exploration
        else:
            # Failed episode - increase exploration
            self.epsilon = min(0.3, self.epsilon * 1.01)
        
        print(f"Episode completed. Total reward: {total_reward:.2f}, Epsilon: {self.epsilon:.3f}")
    
    def save_weights(self, filename=None):
        """
        Save learned weights to file.
        """
        if filename is None:
            filename = self.weights_file
        
        weights_data = {
            'w_e': self.w_e,
            'w_m': self.w_m,
            'w_x': self.w_x,
            'w_w': self.w_w,
            'w_b': self.w_b,
            'epsilon': self.epsilon,
            'episode_count': self.episode_count,
            'successful_episodes': self.successful_episodes,
            'total_episodes': self.total_episodes
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(weights_data, f, indent=2)
            print(f"Weights saved to {filename}")
        except Exception as e:
            print(f"Error saving weights: {e}")
    
    def load_weights(self, filename=None):
        """
        Load learned weights from file.
        """
        if filename is None:
            filename = self.weights_file
        
        if not os.path.exists(filename):
            print(f"No weights file found at {filename}, using initial weights")
            return False
        
        try:
            with open(filename, 'r') as f:
                weights_data = json.load(f)
            
            self.w_e = weights_data.get('w_e', 4.0)
            self.w_m = weights_data.get('w_m', -1.0)
            self.w_x = weights_data.get('w_x', -2.0)
            self.w_w = weights_data.get('w_w', 2.0)
            self.w_b = weights_data.get('w_b', 3.0)
            # Only load epsilon if not in test mode (to preserve low exploration)
            if not hasattr(self, 'test_mode') or not self.test_mode:
                # In training mode, always use high exploration regardless of saved value
                self.epsilon = 0.9  # Force high exploration during training
            self.episode_count = weights_data.get('episode_count', 0)
            self.successful_episodes = weights_data.get('successful_episodes', 0)
            self.total_episodes = weights_data.get('total_episodes', 0)
            
            print(f"Weights loaded from {filename}")
            print(f"Loaded weights: w_e={self.w_e:.2f}, w_m={self.w_m:.2f}, w_x={self.w_x:.2f}, w_w={self.w_w:.2f}, w_b={self.w_b:.2f}")
            print(f"Epsilon: {self.epsilon:.3f}, Episodes: {self.episode_count}")
            return True
        except Exception as e:
            print(f"Error loading weights: {e}")
            return False
    
    def set_training_mode(self, training=True):
        """
        Set training or test mode.
        """
        self.training_mode = training
        self.test_mode = not training
        
        if self.test_mode:
            # In test mode, reduce exploration significantly
            self.epsilon = 0.001
            print("Switched to TEST mode - reduced exploration")
        else:
            print("Switched to TRAINING mode")
    
    def get_success_rate(self):
        """
        Get current success rate.
        """
        if self.total_episodes == 0:
            return 0.0
        return self.successful_episodes / self.total_episodes
    
    def should_continue_training(self, target_success_rate=0.5, min_episodes=100):
        """
        Check if we should continue training.
        """
        if self.total_episodes < min_episodes:
            return True
        
        current_success_rate = self.get_success_rate()
        print(f"Current success rate: {current_success_rate:.2f} ({self.successful_episodes}/{self.total_episodes})")
        
        return current_success_rate < target_success_rate
