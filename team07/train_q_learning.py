#!/usr/bin/env python3
"""
Training script for Approximate Q-Learning Bomberman AI
Runs multiple episodes to train the agent and saves learned weights
"""

import sys
import os
sys.path.insert(0, '../../Bomberman')
sys.path.insert(1, '.')

from game import Game
from testcharacter import TestCharacter
from algorithms.q_learning import ApproximateQLearning

def train_variant(variant_file, max_episodes=1000, target_success_rate=0.5):
    """
    Train Q-Learning agent on a specific variant.
    """
    print(f"\n=== Training on {variant_file} ===")
    
    # Create Q-Learning agent
    q_agent = ApproximateQLearning()
    
    # Try to load existing weights
    weights_file = f"weights_{variant_file.replace('.py', '')}.json"
    q_agent.weights_file = weights_file
    q_agent.load_weights()
    
    # Set training mode
    q_agent.set_training_mode(True)
    
    episode_count = 0
    successful_episodes = 0
    
    while episode_count < max_episodes:
        episode_count += 1
        q_agent.total_episodes += 1
        
        print(f"\nEpisode {episode_count}/{max_episodes}")
        
        # Create game instance
        if variant_file == "variant1.py":
            from variant1 import create_game
            g = create_game()
        elif variant_file == "variant2.py":
            from variant2 import create_game
            g = create_game()
        elif variant_file == "variant3.py":
            from variant3 import create_game
            g = create_game()
        elif variant_file == "variant4.py":
            from variant4 import create_game
            g = create_game()
        elif variant_file == "variant5.py":
            from variant5 import create_game
            g = create_game()
        else:
            print(f"Unknown variant: {variant_file}")
            return
        
        # Run episode
        episode_reward = run_episode(g, q_agent)
        
        # Check if episode was successful
        if episode_reward > 0:
            successful_episodes += 1
            q_agent.successful_episodes += 1
            print(f"✓ Episode {episode_count} SUCCESS! Reward: {episode_reward}")
        else:
            print(f"✗ Episode {episode_count} FAILED. Reward: {episode_reward}")
        
        # Update learning
        q_agent.learn_from_episode([episode_reward])
        
        # Save weights every 50 episodes
        if episode_count % 50 == 0:
            q_agent.save_weights()
            success_rate = successful_episodes / episode_count
            print(f"Progress: {success_rate:.2f} success rate ({successful_episodes}/{episode_count})")
        
        # Check if we've reached target success rate
        if episode_count >= 100:  # Minimum episodes before checking
            current_success_rate = successful_episodes / episode_count
            if current_success_rate >= target_success_rate:
                print(f"\n🎉 Target success rate reached! {current_success_rate:.2f} >= {target_success_rate}")
                break
    
    # Final save
    q_agent.save_weights()
    final_success_rate = successful_episodes / episode_count
    print(f"\n=== Training Complete ===")
    print(f"Final success rate: {final_success_rate:.2f} ({successful_episodes}/{episode_count})")
    print(f"Weights saved to: {weights_file}")
    
    return final_success_rate

def run_episode(game, q_agent):
    """
    Run a single episode with timeout to prevent infinite oscillation.
    """
    # Store original draw method to avoid display during training
    original_draw = game.draw
    game.draw = lambda: None  # Disable display during training
    
    # Track initial position to detect oscillation
    initial_x, initial_y = None, None
    oscillation_count = 0
    max_oscillation = 200  # Give more time for bomb discovery
    
    # Run game with step-by-step monitoring
    for step in range(1000):  # Max 1000 steps per episode
        # Get character position before step
        character = None
        for k, clist in game.world.characters.items():
            for c in clist:
                if c.name == "me":
                    character = c
                    break
        
        if character:
            if initial_x is None:
                initial_x, initial_y = character.x, character.y
                print(f"DEBUG: Agent starts at ({initial_x}, {initial_y})")
            
            # Check for oscillation (returning to initial position)
            if character.x == initial_x and character.y == initial_y:
                oscillation_count += 1
                if oscillation_count > max_oscillation:
                    print(f"DEBUG: Episode stopped due to oscillation at step {step}")
                    break
            else:
                oscillation_count = 0  # Reset if moved away
            
            # Check if character reached exit
            if game.world.exitcell and character.x == game.world.exitcell[0] and character.y == game.world.exitcell[1]:
                print(f"DEBUG: Episode SUCCESS at step {step}")
                break
            
            # Check if character died (more robust check)
            character_still_exists = False
            for k, clist in game.world.characters.items():
                for c in clist:
                    if c.name == "me":
                        character_still_exists = True
                        break
                if character_still_exists:
                    break
            
            if not character_still_exists:
                print(f"DEBUG: Episode FAILED (died) at step {step}")
                break
        else:
            print(f"DEBUG: No character found at step {step}")
            break
        
        # Execute one step
        game.world.next()
    
    # Restore original draw method
    game.draw = original_draw
    
    # Calculate final reward based on game outcome
    episode_reward = 0
    
    if character:
        # Check if character reached exit or died
        if game.world.exitcell and character.x == game.world.exitcell[0] and character.y == game.world.exitcell[1]:
            episode_reward = 1000  # Success
        else:
            episode_reward = -1000  # Failed
    
    return episode_reward

def test_trained_agent(variant_file, num_tests=10):
    """
    Test the trained agent to see if it achieves 5/10 success rate.
    """
    print(f"\n=== Testing trained agent on {variant_file} ===")
    
    # Create Q-Learning agent
    q_agent = ApproximateQLearning()
    
    # Load trained weights
    weights_file = f"weights_{variant_file.replace('.py', '')}.json"
    q_agent.weights_file = weights_file
    
    if not q_agent.load_weights():
        print("No trained weights found! Please train first.")
        return 0.0
    
    # Set test mode (reduced exploration)
    q_agent.set_training_mode(False)
    
    successful_tests = 0
    
    for test_num in range(1, num_tests + 1):
        print(f"\nTest {test_num}/{num_tests}")
        
        # Create game instance
        if variant_file == "variant1.py":
            from variant1 import create_game
            g = create_game()
        elif variant_file == "variant2.py":
            from variant2 import create_game
            g = create_game()
        elif variant_file == "variant3.py":
            from variant3 import create_game
            g = create_game()
        elif variant_file == "variant4.py":
            from variant4 import create_game
            g = create_game()
        elif variant_file == "variant5.py":
            from variant5 import create_game
            g = create_game()
        else:
            print(f"Unknown variant: {variant_file}")
            return 0.0
        
        # Run test episode
        episode_reward = run_episode(g, q_agent)
        
        if episode_reward > 0:
            successful_tests += 1
            print(f"✓ Test {test_num} SUCCESS! Reward: {episode_reward}")
        else:
            print(f"✗ Test {test_num} FAILED. Reward: {episode_reward}")
    
    success_rate = successful_tests / num_tests
    print(f"\n=== Test Results ===")
    print(f"Success rate: {success_rate:.2f} ({successful_tests}/{num_tests})")
    
    if success_rate >= 0.5:
        print("🎉 PASSED! Agent achieves 50%+ success rate")
    else:
        print("❌ FAILED! Agent needs more training")
    
    return success_rate

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Train and test Q-Learning Bomberman AI")
    parser.add_argument("variant", help="Variant file to train/test (e.g., variant1.py)")
    parser.add_argument("--train", action="store_true", help="Train the agent")
    parser.add_argument("--test", action="store_true", help="Test the trained agent")
    parser.add_argument("--episodes", type=int, default=1000, help="Max training episodes")
    parser.add_argument("--tests", type=int, default=10, help="Number of test runs")
    
    args = parser.parse_args()
    
    if args.train:
        train_variant(args.variant, args.episodes)
    
    if args.test:
        test_trained_agent(args.variant, args.tests)
    
    if not args.train and not args.test:
        print("Please specify --train and/or --test")
