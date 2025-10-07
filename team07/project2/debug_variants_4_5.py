#!/usr/bin/env python3

import sys
import random
import os

# Add the path to the bomberman module
sys.path.insert(0, '../../Bomberman')
from game import Game
from monsters.stupid_monster import StupidMonster
from monsters.selfpreserving_monster import SelfPreservingMonster

# Add the path to the team07 module
sys.path.insert(1, '..')
from testcharacter import TestCharacter

# Create the game
rounds = 5  # Fewer rounds for focused debugging
variant_names = ["Variant 4 (Aggressive)", "Variant 5 (Multiple Monsters)"]
success_counts = [0, 0]  # Track wins for each variant

print("=" * 60)
print("DEBUGGING VARIANTS 4 & 5 - Q-LEARNING ANALYSIS")
print("=" * 60)

for i in range(0, rounds):
    print(f"\n--- ROUND {i+1}/{rounds} ---")
    random.seed(random.randint(1, 99999))
    
    ###############################################################################
    # Variant 4 - Aggressive Monster
    print(f"\nRunning {variant_names[0]}...")
    g = Game.fromfile('map.txt')
    g.add_character(TestCharacter("me", "C", 0, 0))
    g.add_monster(SelfPreservingMonster("aggressive", "A", 7, 18, 2))  # Aggressive monster at exit
    
    print(f"Game setup: Character at (0,0), Aggressive monster at (7,18)")
    print(f"Exit at: (7,18)")
    
    g.go(50)  # More realistic number of steps for debugging
    
    # Check if character escaped (found exit) - look for CHARACTER_FOUND_EXIT event
    success = False
    for event in g.world.events:
        if hasattr(event, 'tpe') and event.tpe == 4:  # CHARACTER_FOUND_EXIT
            success = True
            break
    
    if success:
        success_counts[0] += 1
        print(f"✓ {variant_names[0]}: SUCCESS!")
    else:
        print(f"✗ {variant_names[0]}: FAILED")
        # Debug information
        print(f"  - Character position: {g.world.characters[0].x if g.world.characters else 'DEAD'}, {g.world.characters[0].y if g.world.characters else 'DEAD'}")
        print(f"  - Monster positions: {[(m.x, m.y) for m in g.world.monsters] if g.world.monsters else 'ALL DEAD'}")
        print(f"  - Events: {[event.tpe for event in g.world.events] if g.world.events else 'None'}")
    
    ###############################################################################
    # Variant 5 - Multiple Monsters
    print(f"\nRunning {variant_names[1]}...")
    g = Game.fromfile('map.txt')
    g.add_character(TestCharacter("me", "C", 0, 0))
    g.add_monster(StupidMonster("stupid", "S", 7, 18))  # Stupid monster at exit
    g.add_monster(SelfPreservingMonster("aggressive", "A", 0, 18, 2))  # Aggressive monster at bottom-left
    
    print(f"Game setup: Character at (0,0), Stupid monster at (7,18), Aggressive monster at (0,18)")
    print(f"Exit at: (7,18)")
    
    g.go(50)  # More realistic number of steps for debugging
    
    # Check if character escaped (found exit) - look for CHARACTER_FOUND_EXIT event
    success = False
    for event in g.world.events:
        if hasattr(event, 'tpe') and event.tpe == 4:  # CHARACTER_FOUND_EXIT
            success = True
            break
    
    if success:
        success_counts[1] += 1
        print(f"✓ {variant_names[1]}: SUCCESS!")
    else:
        print(f"✗ {variant_names[1]}: FAILED")
        # Debug information
        print(f"  - Character position: {g.world.characters[0].x if g.world.characters else 'DEAD'}, {g.world.characters[0].y if g.world.characters else 'DEAD'}")
        print(f"  - Monster positions: {[(m.x, m.y) for m in g.world.monsters] if g.world.monsters else 'ALL DEAD'}")
        print(f"  - Events: {[event.tpe for event in g.world.events] if g.world.events else 'None'}")

# Print final statistics
print("\n" + "=" * 60)
print("DEBUG RESULTS - VARIANTS 4 & 5")
print("=" * 60)
for i, variant_name in enumerate(variant_names):
    success_rate = (success_counts[i] / rounds) * 100
    status = "✓ PASS" if success_rate >= 50 else "✗ FAIL"
    print(f"{variant_name}: {success_counts[i]}/{rounds} ({success_rate:.1f}%) {status}")

print("\n" + "=" * 60)
print("ANALYSIS SUMMARY")
print("=" * 60)
print(f"Total Successes: {sum(success_counts)}/{rounds * 2} ({(sum(success_counts) / (rounds * 2)) * 100:.1f}%)")
print(f"Variants Above 50%: {sum(1 for count in success_counts if (count/rounds) >= 0.5)}/2")

print("\n" + "=" * 60)
print("DEBUGGING NOTES")
print("=" * 60)
print("This test runs only 1 step per game to analyze:")
print("1. Initial Q-Learning decision making")
print("2. Character vs monster positioning")
print("3. Event generation patterns")
print("4. Success/failure causes")
print("=" * 60)
