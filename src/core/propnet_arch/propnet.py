from pyswip import Prolog
from ..gdl.general.definitions import Term

class PropNet:

    def __init__(self, description):
        self.roles = None
        self.inputs = None
        self.bases = None
        self.views = None
        self.legals = None
        self.rewards = None
        self.terminal = None

        prolog = Prolog()
        prolog.consult(description)

        self.bases = {}
        bases_query = list(prolog.query("base(X)"))

        for bases_result in bases_query:
            name = bases_result["X"]
            self.bases[name] = Term(name, len(list(prolog.query("init(" + name + ")"))) == 1)



class PropNetHiddenInfo(PropNet):

    def __init__(self, description):
        super(PropNetHiddenInfo, self).__init__(description)
        self.unknowns = None