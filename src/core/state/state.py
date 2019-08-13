from ..gdl.general.definitions import Term

class State:

    def __init__(self, true_terms):
        self.true_terms = true_terms

    def __str__(self):
        return '{' + ', '.join([term.__str__() for term in self.true_terms]) + '}'

    def __iter__(self):
        return self.true_terms.__iter__()

    def __next__(self):
        return self.true_terms.__next__()