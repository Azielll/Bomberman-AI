#!/usr/bin/env python3

import sys
import random
import os

# Add the path to the bomberman module
sys.path.insert(0, '../../Bomberman')
from game import Game
from monsters.selfpreserving_monster import SelfPreservingMonster

# Add the path to the team07 module
sys.path.insert(1, '..')
from testcharacter import TestCharacter

print("=" * 80)
print("VARIANT 4 DIAGNOSIS - AGGRESSIVE MONSTER ANALYSIS")
print("=" * 80)

# Run multiple detailed analyses
for test_num in range(1, 4):
    print(f"\n{'='*20} TEST {test_num} {'='*20}")
    
    # Set random seed for reproducibility
    random.seed(42 + test_num)
    
    # Create Variant 4 game
    g = Game.fromfile('map.txt')
    g.add_monster(SelfPreservingMonster("aggressive", "A", 3, 13, 2))  # Detection range 2
    g.add_character(TestCharacter("me", "C", 0, 0))
    
    print(f"Initial Setup:")
    print(f"  - Character at: (0, 0)")
    print(f"  - Aggressive monster at: (3, 13) with detection range 2")
    print(f"  - Exit at: (7, 18)")
    
    step_count = 0
    max_steps = 100  # Limit for detailed analysis
    
    while step_count < max_steps and not g.done():
        step_count += 1
        
        # Get current positions
        if g.world.characters:
            char = list(g.world.characters.values())[0][0]  # First character from first cell
            char_pos = (char.x, char.y)
        else:
            char_pos = "DEAD"
            
        if g.world.monsters:
            monster = list(g.world.monsters.values())[0][0]  # First monster from first cell
            monster_pos = (monster.x, monster.y)
        else:
            monster_pos = "DEAD"
        
        # Calculate distance between character and monster
        if char_pos != "DEAD" and monster_pos != "DEAD":
            distance = ((char_pos[0] - monster_pos[0])**2 + (char_pos[1] - monster_pos[1])**2)**0.5
        else:
            distance = "N/A"
        
        # Check if character is in monster's detection range
        in_detection_range = distance != "N/A" and distance <= 2
        
        print(f"\nStep {step_count}:")
        print(f"  Character: {char_pos}")
        print(f"  Monster: {monster_pos}")
        print(f"  Distance: {distance:.2f}" if distance != "N/A" else f"  Distance: {distance}")
        print(f"  In detection range: {in_detection_range}")
        
        # Check for events
        if g.world.events:
            for event in g.world.events:
                if hasattr(event, 'tpe'):
                    if event.tpe == 3:  # CHARACTER_KILLED_BY_MONSTER
                        print(f"  🚨 CHARACTER KILLED BY MONSTER!")
                        break
                    elif event.tpe == 4:  # CHARACTER_FOUND_EXIT
                        print(f"  🎉 CHARACTER FOUND EXIT!")
                        break
        
        # Run one step
        (g.world, g.events) = g.world.next()
        
        # Check if game ended
        if not g.world.characters:
            print(f"\n❌ GAME ENDED: Character died at step {step_count}")
            break
        elif g.world.exitcell and not g.world.characters:
            print(f"\n✅ GAME ENDED: Character escaped at step {step_count}")
            break
    
    if step_count >= max_steps:
        print(f"\n⏰ ANALYSIS STOPPED: Reached {max_steps} steps")
    
    print(f"\nFinal State:")
    print(f"  Steps taken: {step_count}")
    print(f"  Character alive: {len(g.world.characters) > 0}")
    print(f"  Monster alive: {len(g.world.monsters) > 0}")
    
    # Check final events
    if g.world.events:
        for event in g.world.events:
            if hasattr(event, 'tpe'):
                if event.tpe == 3:
                    print(f"  Result: Character was killed by monster")
                elif event.tpe == 4:
                    print(f"  Result: Character found exit")

print("\n" + "=" * 80)
print("DIAGNOSIS COMPLETE")
print("=" * 80)
