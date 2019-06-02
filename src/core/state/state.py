from ..gdl.general.definitions import Term

class State:

    def __init__(self, base_terms):
        self.base_terms = base_terms

    def __str__(self):
        ret = "{ "
        at_first = True
        for term in self.base_terms:
            if at_first:
                ret += term.name + ": " + str(term.value)
                at_first = False
            else:
                ret += ", " + term.name + ": " + str(term.value)
        ret += " }"
        return ret