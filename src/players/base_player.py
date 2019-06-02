from core.statemachines.propnet import PropNetStateMachine
from core.state.state import State
from abc import ABC

class BasePlayer(ABC):
    
    def __init__(self, match):
        self.match = match
        self.state_machine = PropNetStateMachine(match.description)

    @abstractmethod
    def info(self):
        pass

    @abstractmethod
    def select_move(self, select_time, state, moves):
        pass

    def study(self, study_time):
        pass

    def prepare(self, prepare_time):
        pass