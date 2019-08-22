import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../')

def run_random_game():
    pass


def run_full_game_tree():
    pass

def get_game_description(test_game):
    f = open("tests/games/" + test_game + ".gdl")
    return f.read()