# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
import random
from game import Game
from monsters.selfpreserving_monster import SelfPreservingMonster

# TODO This is your code!
sys.path.insert(1, '../teamNN')
from testcharacter import TestCharacter

# Create the game
rounds = 10  # 10 rounds for better statistics
variant_name = "Variant 4 (Aggressive)"
success_count = 0  # Track wins for this variant

print("=" * 60)
print("VARIANT 4 TESTING - AGGRESSIVE MONSTER")
print("=" * 60)

for i in range(0, rounds):
    print(f"\n--- ROUND {i+1}/{rounds} ---")
    random.seed(random.randint(1, 99999))
    
    ###############################################################################
    # Variant 4 - Aggressive Monster
    print(f"\nRunning {variant_name}...")
    g = Game.fromfile('map.txt')
    g.add_monster(SelfPreservingMonster("aggressive", # name
                                        "A",          # avatar
                                        3, 13,        # position
                                        2             # detection range
    ))
    g.add_character(TestCharacter("me", # name
                                "C",  # avatar
                                0, 0  # position
    ))
    g.go(500)  # 500 steps for full game
    
    # Check if character escaped (found exit) - look for CHARACTER_FOUND_EXIT event
    success = False
    for event in g.world.events:
        if hasattr(event, 'tpe') and event.tpe == 4:  # CHARACTER_FOUND_EXIT
            success = True
            break
    
    if success:
        success_count += 1
        print(f"✓ {variant_name}: SUCCESS!")
    else:
        print(f"✗ {variant_name}: FAILED")

# Print final statistics
print("\n" + "=" * 60)
print("VARIANT 4 FINAL RESULTS")
print("=" * 60)
success_rate = (success_count / rounds) * 100
status = "✓ PASS" if success_rate >= 50 else "✗ FAIL"
print(f"{variant_name}: {success_count}/{rounds} ({success_rate:.1f}%) {status}")

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"Total Successes: {success_count}/{rounds}")
print(f"Success Rate: {success_rate:.1f}%")
print(f"Status: {status}")
