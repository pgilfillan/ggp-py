import os
import sys
import random

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../')

def run_random_game(statemachine, num_retries=1):
    for retry in range(num_retries):
        print("Starting randomly played game", retry)
        curr_state = statemachine.get_initial_state()
        while not statemachine.is_terminal(curr_state):
            print("Current state:", curr_state)
            joint_moves = statemachine.get_legal_joint_moves(curr_state)
            chosen = {}
            for role in joint_moves:
                chosen[role] = random.sample(joint_moves[role], 1)[0]
            print("Chosen moves:", chosen)
            curr_state = statemachine.get_next_state(curr_state, chosen)
        print("Game ended in state", curr_state)


def run_full_game_tree(statemachine):
    pass

def get_game_description(test_game):
    f = open("tests/games/" + test_game + ".gdl")
    return f.read()