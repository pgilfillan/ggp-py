from src.core.statemachines.prolog import PrologStateMachine

sm = PrologStateMachine("games/test/test.pl")
init_state = sm.get_initial_state()
print("Initial state:", init_state)
moves = sm.get_legal_moves(init_state, "player1")
print("Legal moves for player1:", moves)
joint_moves = sm.get_legal_joint_moves(init_state)
print("Legal joint moves:", joint_moves)
print("Is terminal:", sm.is_terminal(init_state))
print("Goal value:", sm.get_goal_value(init_state, "player1"))