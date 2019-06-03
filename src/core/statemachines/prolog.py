from .base import StateMachine
from ..state.state import State
from pyswip import Prolog
from ..gdl.general.definitions import Term

class PrologStateMachine(StateMachine):

    def __init__(self, description):
        self.prolog = Prolog()
        self.prolog.consult(description)

    def get_initial_state(self):
        bases = []
        bases_query = list(self.prolog.query("base(X)"))
        for bases_result in bases_query:
            name = str(bases_result["X"])
            if len(list(self.prolog.query("init(" + name + ")"))) == 1:
                bases.append(Term(name))
        return State(bases)

    def is_terminal(self, state):
        self.set_base_truths(state)
        return len(list(self.prolog.query("terminal"))) == 1

    def get_goal_value(self, state, player):
        self.set_base_truths(state)
        return list(self.prolog.query("goal(" + player + ", N)"))[0]['N']

    def get_legal_moves(self, state, player):
        self.set_base_truths(state)
        return [str(result['A']) for result in list(self.prolog.query("legal(" + player + ", A)"))]

    def get_legal_joint_moves(self, state):
        self.set_base_truths(state)
        legals_query = list(self.prolog.query("legal(R, A)"))
        joint_legals = {}
        for result in legals_query:
            role = str(result['R'])
            action = str(result['A'])
            if role in joint_legals:
                joint_legals[role].append(action)
            else:
                joint_legals[role] = [action]
        return joint_legals

    def get_next_state(self, state, moves):
        self.set_base_truths(state)
        self.prolog.retractall("does(R,A)")
        for role in moves:
            self.prolog.assertz("does(" + role + ", " + moves[role] + ")")
        return State([Term(str(res['P'])) for res in list(self.prolog.query("next(P)"))])

    def get_next_states(self, state, moves=None):
        if moves == None:
            pass
        else:
            pass

    def set_base_truths(self, state):
        self.prolog.retractall("true(X)")
        for term in state.true_terms:
            if term.value:
                self.prolog.assertz("true(" + term.name + ")")