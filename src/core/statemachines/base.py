from ..state.state import State
from abc import ABC, abstractmethod

class StateMachine(ABC):

    def __init__(self, description):
        pass

    @abstractmethod
    def get_initial_state(self):
        return State()

    @abstractmethod
    def is_terminal(self, state):
        return False

    @abstractmethod
    def get_goal_value(self, state, player):
        pass

    @abstractmethod
    def get_legal_moves(self, state, player):
        pass

    @abstractmethod
    def get_legal_joint_moves(self, state):
        pass

    @abstractmethod
    def get_next_state(self, state, moves):
        pass

    @abstractmethod
    def get_roles(self):
        pass