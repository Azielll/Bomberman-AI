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
sys.path.insert(1, '../team07')
from testcharacter import TestCharacter

print("Testing Hybrid A* + Minimax on Variant 5 (10 times)")
print("=" * 60)

# Test 10 different seeds
seeds_to_test = [123, 456, 789, 999, 111, 222, 333, 444, 555, 666]
wins = 0
losses = 0

for i, seed in enumerate(seeds_to_test, 1):
    print(f"\nTest {i}/10 with seed {seed}:")
    print("-" * 30)
    
    random.seed(seed)
    g = Game.fromfile('map.txt')
    
    # Add monsters to match Variant 5 setup
    g.add_monster(StupidMonster("stupid", "S", 3, 5))
    g.add_monster(SelfPreservingMonster("aggressive", "A", 7, 13, 1))
    
    g.add_character(TestCharacter("me", "C", 0, 0))
    
    # Run for 300 turns (same as original variant5.py)
    g.go(300)
    
    # Check result
    won = False
    for event in g.world.events:
        if (4 == event.tpe):  # Event type 4 = found exit
            won = True
            break
    
    if won:
        print(f"✅ WON with seed {seed}")
        wins += 1
    else:
        print(f"❌ LOST with seed {seed}")
        losses += 1

print("\n" + "=" * 60)
print("FINAL RESULTS:")
print(f"Wins: {wins}/10")
print(f"Losses: {losses}/10")
print(f"Win Rate: {wins/10*100:.1f}%")

if wins >= 6:  # More than 50% (6+ wins out of 10)
    print("🎉 SUCCESS: Achieved more than 50% win rate!")
else:
    print("❌ FAILED: Did not achieve more than 50% win rate")
