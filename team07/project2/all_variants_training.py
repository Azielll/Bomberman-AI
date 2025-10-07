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
rounds = 10

for i in range(0, rounds):

    random.seed(random.randint(1, 99999))
###############################################################################
    # Variant 1
    g = Game.fromfile('map.txt')
    g.add_character(TestCharacter("me", # name
                                "C",  # avatar
                                0, 0  # position
    ))
    g.go(50)

###############################################################################
    # Variant 2
    g = Game.fromfile('map.txt')
    g.add_monster(StupidMonster("stupid", # name
                                "S",      # avatar
                                3, 9      # position
    ))
    g.add_character(TestCharacter("me", # name
                                "C",  # avatar
                                0, 0  # position
    ))
    g.go(50)

###############################################################################
    # Variant 3
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
    g.go(50)

###############################################################################
    # Variant 4
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
    g.go(50)
    
###############################################################################
    # Variant 5
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
    g.go(50)

