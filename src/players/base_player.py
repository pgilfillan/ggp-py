from ..core.statemachines.propnet import PropNetStateMachine
from ..core.state.state import State
from abc import ABC, abstractmethod

class BasePlayer(ABC):
    
    def __init__(self, match):
        self.match = match

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