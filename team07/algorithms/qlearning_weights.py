
"""
Global Q-learning weights manager for Bomberman AI
"""
import json
import os

class QLearningWeights:
    """Singleton class to manage Q-learning weights globally"""
    _instance = None
    WEIGHTS_FILE = "team07_qlearning_weights.json"
    
    def __new__(cls):
        # Singleton pattern - only one instance exists
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        # Only initialize once
        if not self._initialized:
            self.games_played = 0
            self.weights = self.load_weights()
            self.alpha = 0.1      # Learning rate
            self.gamma = 0.9      # Discount factor
            self._initialized = True
            print(f"QLearningWeights initialized: {self.weights}")
    
    def load_weights(self):
        """Load weights from JSON file"""
        if os.path.exists(self.WEIGHTS_FILE):
            try:
                with open(self.WEIGHTS_FILE, 'r') as f:
                    data = json.load(f)
                    self.games_played = data.get('games_played', 0)
                    print(f"Loaded weights from file: {data['weights']}")
                    print(f"Games played so far: {self.games_played}")
                    return data['weights']
            except Exception as e:
                print(f"Error loading weights: {e}")
        
        # Default weights [monster_weight, exit_weight, bomb_weight]
        print("Using default weights: [0.0, 0.0, 0.0]")
        return [0.0, 0.0, 0.0]
    
    def save_weights(self):
        """Save weights to JSON file"""
        data = {
            'weights': self.weights,
            'games_played': self.games_played,
            'alpha': self.alpha,
            'gamma': self.gamma,
            'last_updated': str(__import__('datetime').datetime.now())
        }
        try:
            with open(self.WEIGHTS_FILE, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"Weights saved to {self.WEIGHTS_FILE}: {self.weights}")
        except Exception as e:
            print(f"Error saving weights: {e}")
    
    def get_features(self, distances):
        """Convert distances to features: [monster_dist, exit_dist, bomb_dist] -> features"""
        features = []
        for d in distances:
            if d == float('inf'):
                features.append(1.0)
            else:
                features.append(1.0 / (1.0 + d))  # Higher value for closer distance
        return features
    
    def calculate_q_value(self, distances):
        """Calculate Q-value: Q = w1*f1 + w2*f2 + w3*f3"""
        features = self.get_features(distances)
        q_value = sum(w * f for w, f in zip(self.weights, features)) + distances[1]
        return q_value
    
    def update_weights(self, last_distances, reward, current_distances):
        """Update weights using Q-learning"""
        if last_distances is None:
            return
        
        # Calculate Q-values
        current_q = self.calculate_q_value(last_distances)
        next_q = self.calculate_q_value(current_distances)
        
        # TD error: reward + gamma * next_q - current_q
        td_error = reward + self.gamma * next_q - current_q
        
        # Update each weight: w = w + alpha * td_error * feature
        features = self.get_features(last_distances)
        for i in range(len(self.weights)):
            self.weights[i] += self.alpha * td_error * features[i]
        
        print(f"Q-update: reward={reward}, td_error={td_error:.3f}")
        print(f"New weights: {[f'{w:.3f}' for w in self.weights]}")