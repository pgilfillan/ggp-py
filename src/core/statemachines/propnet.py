from .base import StateMachine
from ..state.state import State
from ..propnet_arch.propnet import PropNet
from ..propnet_arch.node import PropNetNode

class PropNetStateMachine(StateMachine):

    def __init__(self, description):
        self.propnet = PropNet(description)

    def is_terminal(self, state):
        self.propnet.clear()
        self.propnet.mark_bases(state)
        return self.propnet.node_mark(self.propnet.terminal)

    def get_goal_value(self, state, player):
        self.propnet.clear()
        self.propnet.mark_bases(state)
        reward_nodes = self.propnet.rewards
        for node in reward_nodes[player]:
            if self.propnet.node_mark(node):
                return str(node.term.inner_terms[2])

        print("Error: failed to get goal value for player: " + player)

    def get_initial_state(self):
        self.propnet.reset_to_initial()
        return State(self.propnet.get_state())

    # TODO: figure out transitions for legals
    def get_legal_moves(self, state, player):
        legals = set()

        self.propnet.clear()
        self.propnet.mark_bases(state)
        legal_nodes = self.propnet.legals[player]
        for node in legal_nodes:
            if self.propnet.node_mark(node):
                legals.add(str(node.inner_terms[2]))

        return legals

    def get_legal_joint_moves(self, state):
        pass

    def get_next_state(self, state, moves):
        self.propnet.clear()
        self.propnet.mark_inputs(moves)
        self.propnet.mark_bases(state)
        next_state = set()
        for base, base_node in self.propnet.bases.items():
            if base_node.in_edge is None:
                if base_node.value:
                    next_state.add(base)
            elif self.propnet.node_mark(base_node.in_edge.sources[0]):
                    next_state.add(base)
        
        return next_state
            
    def get_roles(self):
        return self.propnet.roles