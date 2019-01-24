from base import StateMachine
from core.state.state import State

class PropNetStateMachine(StateMachine):

    def __init__(self, description):
        self.propnet = None

    def is_terminal(self, state):
        return self.propnet.terminal.value

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
