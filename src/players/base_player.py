from core.statemachines.propnet import PropNetStateMachine
from core.state.state import State


class BasePlayer:
    
    def __init__(self, match):
        self.match = match
        self.state_machine = PropNetStateMachine(match.description)

    def select_move(self, state):
        pass

    def prepare(self):
        pass

    def study(self):
        pass