# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
import random
from game import Game
from monsters.stupid_monster import StupidMonster
from monsters.selfpreserving_monster import SelfPreservingMonster

# TODO This is your code!
sys.path.insert(1, '../teamNN')
from testcharacter import TestCharacter

# Create the game
rounds = 10  # 10 rounds for better statistics
variant_names = ["Variant 1 (Solo)", "Variant 2 (Stupid Monster)", "Variant 3 (Self-Preserving)", "Variant 4 (Aggressive)", "Variant 5 (Multiple Monsters)"]
success_counts = [0, 0, 0, 0, 0]  # Track wins for each variant

print("=" * 60)
print("Q-LEARNING TRAINING WITH SUCCESS RATE TRACKING")
print("=" * 60)

for i in range(0, rounds):
    print(f"\n--- ROUND {i+1}/{rounds} ---")
    random.seed(random.randint(1, 99999))
    
    ###############################################################################
    # Variant 1
    print(f"\nRunning {variant_names[0]}...")
    g = Game.fromfile('map.txt')
    g.add_character(TestCharacter("me", # name
                                "C",  # avatar
                                0, 0  # position
    ))
    g.go(500)  # Increased to 500 steps for more time
    
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

    ###############################################################################
    # Variant 2
    print(f"\nRunning {variant_names[1]}...")
    g = Game.fromfile('map.txt')
    g.add_monster(StupidMonster("stupid", # name
                                "S",      # avatar
                                3, 9      # position
    ))
    g.add_character(TestCharacter("me", # name
                                "C",  # avatar
                                0, 0  # position
    ))
    g.go(500)  # Increased to 500 steps for more time
    
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

    ###############################################################################
    # Variant 3
    print(f"\nRunning {variant_names[2]}...")
    g = Game.fromfile('map.txt')
    g.add_monster(SelfPreservingMonster("selfpreserving", # name
                                        "S",              # avatar
                                        3, 9,             # position
                                        1                 # detection range
    ))
    g.add_character(TestCharacter("me", # name
                                "C",  # avatar
                                0, 0  # position
    ))
    g.go(500)  # Increased to 500 steps for more time
    
    # Check if character escaped (found exit) - look for CHARACTER_FOUND_EXIT event
    success = False
    for event in g.world.events:
        if hasattr(event, 'tpe') and event.tpe == 4:  # CHARACTER_FOUND_EXIT
            success = True
            break
    
    if success:
        success_counts[2] += 1
        print(f"✓ {variant_names[2]}: SUCCESS!")
    else:
        print(f"✗ {variant_names[2]}: FAILED")

    ###############################################################################
    # Variant 4
    print(f"\nRunning {variant_names[3]}...")
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
    g.go(500)  # Increased to 500 steps for more time
    
    # Check if character escaped (found exit) - look for CHARACTER_FOUND_EXIT event
    success = False
    for event in g.world.events:
        if hasattr(event, 'tpe') and event.tpe == 4:  # CHARACTER_FOUND_EXIT
            success = True
            break
    
    if success:
        success_counts[3] += 1
        print(f"✓ {variant_names[3]}: SUCCESS!")
    else:
        print(f"✗ {variant_names[3]}: FAILED")
    
    ###############################################################################
    # Variant 5
    print(f"\nRunning {variant_names[4]}...")
    g = Game.fromfile('map.txt')
    g.add_monster(StupidMonster("stupid", # name
                            "S",      # avatar
                            3, 5,     # position
    ))
    g.add_monster(SelfPreservingMonster("aggressive", # name
                                    "A",          # avatar
                                    3, 13,        # position
                                    2             # detection range
    ))
    g.add_character(TestCharacter("me", # name
                                "C",  # avatar
                                0, 0  # position
    ))
    g.go(500)  # Increased to 500 steps for more time
    
    # Check if character escaped (found exit) - look for CHARACTER_FOUND_EXIT event
    success = False
    for event in g.world.events:
        if hasattr(event, 'tpe') and event.tpe == 4:  # CHARACTER_FOUND_EXIT
            success = True
            break
    
    if success:
        success_counts[4] += 1
        print(f"✓ {variant_names[4]}: SUCCESS!")
    else:
        print(f"✗ {variant_names[4]}: FAILED")

# Print final statistics
print("\n" + "=" * 60)
print("FINAL SUCCESS RATE STATISTICS")
print("=" * 60)
for i, variant_name in enumerate(variant_names):
    success_rate = (success_counts[i] / rounds) * 100
    status = "✓ PASS" if success_rate >= 50 else "✗ FAIL"
    print(f"{variant_name}: {success_counts[i]}/{rounds} ({success_rate:.1f}%) {status}")

print("\n" + "=" * 60)
print("OVERALL PERFORMANCE")
print("=" * 60)
total_successes = sum(success_counts)
overall_rate = (total_successes / (rounds * 5)) * 100
print(f"Total Successes: {total_successes}/{rounds * 5} ({overall_rate:.1f}%)")
print(f"Variants Above 50%: {sum(1 for count in success_counts if (count/rounds) >= 0.5)}/5")

