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
# (Change this to change hw many tests you do!)
number_of_games = 100

# Tracks the number of wins for each variant
v1_wins = 0.0
v2_wins = 0.0
v3_wins = 0.0
v4_wins = 0.0
v5_wins = 0.0

###################### Varaint 1 ######################
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


###################### Varaint 2 ######################
for i in range(1, number_of_games + 1):
    random.seed(i)
    # create the game~
    g = Game.fromfile('map.txt')

    # add the monster~ 
    g.add_monster(StupidMonster("stupid", "S", 3, 9))

    # add the test character~
    g.add_character(TestCharacter("me", "C", 0, 0))
    
    # run the game~
    g.go(1)

    # check the events in the finished game
    if len(g.world.events) >= 0:
        for event in g.world.events:
            if (4 == event.tpe):
                v2_wins = v2_wins + 1.0


###################### Varaint 3 ######################
for i in range(1, number_of_games + 1):
    random.seed(i)
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


###################### Varaint 4 ######################
for i in range(1, number_of_games + 1):
    random.seed(i)
    # create the game~
    g = Game.fromfile('map.txt')

    # add the monster~
    g.add_monster(SelfPreservingMonster("aggresive", "A", 7, 13, 2))

    # add the test character~
    g.add_character(TestCharacter("me", "C", 0, 0))
    
    # run the game~
    g.go(1)

    # check the events in the finished game
    if len(g.world.events) >= 0:
        for event in g.world.events:
            if (4 == event.tpe):
                v4_wins = v4_wins + 1.0


###################### Varaint 5 ######################
for i in range(1, number_of_games + 1):
    random.seed(i)
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
    if len(g.world.events) >= 0:
        for event in g.world.events:
            if (4 == event.tpe):
                v5_wins = v5_wins + 1.0


v1_win_pa = (v1_wins / 10) * 100
v2_win_pa = (v2_wins / number_of_games) * 100
v3_win_pa = (v3_wins / number_of_games) * 100
v4_win_pa = (v4_wins / number_of_games) * 100
v5_win_pa = (v5_wins / number_of_games) * 100

print("Variant 1 Win Rate: ", v1_win_pa, "%")
print("Variant 2 Win Rate: ", v2_win_pa, "%")
print("Variant 3 Win Rate: ", v3_win_pa, "%")
print("Variant 4 Win Rate: ", v4_win_pa, "%")
print("Variant 5 Win Rate: ", v5_win_pa, "%")

