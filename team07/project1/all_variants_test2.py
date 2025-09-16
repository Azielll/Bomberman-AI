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

# Number of games you want to test
# (Change this to change how many tests you do!)
number_of_games = 20  # Reduced for detailed analysis

# Tracks the number of wins for each variant
v1_wins = 0.0
v2_wins = 0.0
v3_wins = 0.0
v4_wins = 0.0
v5_wins = 0.0

print("Enhanced A* Algorithm - Comprehensive Testing")
print("=" * 50)
print(f"Testing {number_of_games} games per variant...")
print("=" * 50)

###################### Variant 1 ######################
print("Testing Variant 1 (Basic)...")
for i in range(0, 10):
    # create the game~
    g = Game.fromfile('map.txt')

    # add the test character~
    g.add_character(TestCharacter("me", "C", 0, 0))
    
    # run the game~
    g.go(1)

    # check the events in the finished game
    if len(g.world.events) >= 0:
        for event in g.world.events:
            if (4 == event.tpe):
                v1_wins = v1_wins + 1.0

###################### Variant 2 ######################
print("Testing Variant 2 (Aggressive Monster)...")
v2_details = []
for i in range(0, number_of_games):
    random.seed(random.randint(0,999))
    # create the game~
    g = Game.fromfile('map.txt')

    # add the monster~ 
    g.add_monster(StupidMonster("stupid", "S", 3, 9))

    # add the test character~
    g.add_character(TestCharacter("me", "C", 0, 0))
    
    # run the game~
    g.go(1)

    # check the events in the finished game
    won = False
    death_cause = "timeout"
    if len(g.world.events) >= 0:
        for event in g.world.events:
            if (4 == event.tpe):
                v2_wins = v2_wins + 1.0
                won = True
            elif (2 == event.tpe):  # Character killed
                death_cause = "killed by monster"
    
    v2_details.append(f"Game {i+1}: {'WON' if won else 'LOST'} - {death_cause}")

###################### Variant 3 ######################
print("Testing Variant 3 (Multiple Monsters)...")
for i in range(0, number_of_games):
    random.seed(random.randint(0,999))
    # create the game~
    g = Game.fromfile('map.txt')

    # add the monster~
    g.add_monster(SelfPreservingMonster("selfpreserving", "S", 3, 9, 1))

    # add the test character~
    g.add_character(TestCharacter("me", "C", 0, 0))
    
    # run the game~
    g.go(1)

    # check the events in the finished game
    if len(g.world.events) >= 0:
        for event in g.world.events:
            if (4 == event.tpe):
                v3_wins = v3_wins + 1.0

###################### Variant 4 ######################
print("Testing Variant 4 (Complex Maze)...")
v4_details = []
for i in range(0, number_of_games):
    random.seed(random.randint(0,999))
    # create the game~
    g = Game.fromfile('map.txt')

    # add the monster~
    g.add_monster(SelfPreservingMonster("aggresive", "A", 7, 13, 2))

    # add the test character~
    g.add_character(TestCharacter("me", "C", 0, 0))
    
    # run the game~
    g.go(1)

    # check the events in the finished game
    won = False
    death_cause = "timeout"
    if len(g.world.events) >= 0:
        for event in g.world.events:
            if (4 == event.tpe):
                v4_wins = v4_wins + 1.0
                won = True
            elif (2 == event.tpe):  # Character killed
                death_cause = "killed by monster"
    
    v4_details.append(f"Game {i+1}: {'WON' if won else 'LOST'} - {death_cause}")

###################### Variant 5 ######################
print("Testing Variant 5 (Multiple Aggressive)...")
v5_details = []
for i in range(0, number_of_games):
    random.seed(random.randint(0,999))
    # create the game~
    g = Game.fromfile('map.txt')

    # add the monsters~
    g.add_monster(StupidMonster("stupid", "S", 3, 9))
    g.add_monster(SelfPreservingMonster("aggresive", "A", 7, 13, 1))

    # add the test character~
    g.add_character(TestCharacter("me", "C", 0, 0))
    
    # run the game~
    g.go(1)

    # check the events in the finished game
    won = False
    death_cause = "timeout"
    if len(g.world.events) >= 0:
        for event in g.world.events:
            if (4 == event.tpe):
                v5_wins = v5_wins + 1.0
                won = True
            elif (2 == event.tpe):  # Character killed
                death_cause = "killed by monster"
    
    v5_details.append(f"Game {i+1}: {'WON' if won else 'LOST'} - {death_cause}")

# Calculate win percentages
v1_win_pa = (v1_wins / 10) * 100
v2_win_pa = (v2_wins / number_of_games) * 100
v3_win_pa = (v3_wins / number_of_games) * 100
v4_win_pa = (v4_wins / number_of_games) * 100
v5_win_pa = (v5_wins / number_of_games) * 100

print("\n" + "=" * 50)
print("ENHANCED A* ALGORITHM RESULTS")
print("=" * 50)
print(f"Variant 1  Win Rate: {v1_win_pa:.1f}%")
print(f"Variant 2  Win Rate: {v2_win_pa:.1f}%")
print(f"Variant 3  Win Rate: {v3_win_pa:.1f}%")
print(f"Variant 4  Win Rate: {v4_win_pa:.1f}%")
print(f"Variant 5  Win Rate: {v5_win_pa:.1f}%")
print("=" * 50)

# Calculate overall performance
total_games = 10 + (number_of_games * 4)
total_wins = v1_wins + v2_wins + v3_wins + v4_wins + v5_wins
overall_win_rate = (total_wins / total_games) * 100

print(f"Overall Win Rate: {overall_win_rate:.1f}%")
print(f"Total Games: {total_games}")
print(f"Total Wins: {int(total_wins)}")
print("=" * 50)

# Detailed analysis for failing variants
print("\nDETAILED ANALYSIS:")
print("=" * 50)
print("Variant 2 Details:")
for detail in v2_details:
    print(f"  {detail}")

print("\nVariant 4 Details:")
for detail in v4_details:
    print(f"  {detail}")

print("\nVariant 5 Details:")
for detail in v5_details:
    print(f"  {detail}")