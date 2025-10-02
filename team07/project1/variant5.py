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
random.seed(123) # TODO Change this if you want different random choices
g = Game.fromfile('map.txt')
g.add_monster(StupidMonster("stupid", # name
                            "S",      # avatar
                            3, 5,     # position
))
g.add_monster(SelfPreservingMonster("aggressive", # name
                                    "A",          # avatar
                                    7, 13,        # position
                                    1             # detection range
))

# TODO Add your character
g.add_character(TestCharacter("me", # name
                              "C",  # avatar
                              0, 0  # position
))
# In variant5.py, after creating the game but before running:
print(f"Game object: {g}")
print(f"Has ai_characters attribute: {hasattr(g, 'ai_characters')}")
if hasattr(g, 'ai_characters'):
    print(f"AI characters list: {g.ai_characters}")

# Also check which game.py is being used:
import game
print(f"Game module path: {game.__file__}")
# Run!
g.go(1)  
