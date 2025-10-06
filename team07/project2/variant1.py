# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
from game import Game
import pygame

# TODO This is your code!
sys.path.insert(1, '../teamNN')
from testcharacter import TestCharacter

def create_game():
    """Create a game instance for training/testing."""
    # Create the game
    g = Game.fromfile('map.txt')

    # TODO Add your character
    g.add_character(TestCharacter("me", # name
                                  "C",  # avatar
                                  0, 0  # position
    ))
    return g

# Run!
if __name__ == "__main__":
    g = create_game()
    g.go(500)
