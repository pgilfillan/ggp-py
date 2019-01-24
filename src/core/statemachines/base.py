from core.state.state import State

class StateMachine:

    def __init__(self, description):
        pass

    def is_terminal(self, state):
        return False

    def get_goal_value(self, state, player):
        pass

    def get_initial_state(self):
        return State()

    def get_legal_moves(self, state, player):
        pass

    def get_legal_joint_moves(self, state):
        pass

    def get_next_state(self, state, moves):
        pass