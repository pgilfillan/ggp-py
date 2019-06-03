from ..gdl.general.definitions import Term

class State:

    def __init__(self, true_terms):
        self.true_terms = true_terms

    def __str__(self):
        return '[' + ', '.join([term.name for term in self.true_terms]) + ']'
