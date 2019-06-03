from src.core.statemachines.prolog import PrologStateMachine
import random

games = ["test"]

for game in games:
    description = "games/" + game + "/" + game + ".pl"
    sm = PrologStateMachine(description)
    curr_state = sm.get_initial_state()

    moves_played = 0
    max_moves = 10
    while moves_played < max_moves and not sm.is_terminal(curr_state):
        print("Curr state:", curr_state)
        joint_moves = sm.get_legal_joint_moves(curr_state)
        next_moves = {}
        for player in joint_moves:
            next_moves[player] = random.choice(joint_moves[player])
        print("Chosen moves:", next_moves)
        curr_state = sm.get_next_state(curr_state, next_moves)
        moves_played += 1

    if moves_played == max_moves:
        print("Game ended before terminating: max moves reached")
    else:
        print("Game ended in", moves_played, "moves")