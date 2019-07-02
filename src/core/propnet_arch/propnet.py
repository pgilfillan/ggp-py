from pyswip import Prolog
from ..gdl.general.definitions import Term
from ..util.prolog import load_game_description
from .node import PropNetNode, PropNetEdge

class PropNet:

    def __init__(self, description):
        self.roles = None
        self.inputs = None
        self.bases = None
        self.views = None
        self.legals = None
        self.rewards = None
        self.terminal = None

        load_game_description(description)
        self.prolog = Prolog()

        self.load_bases()
        self.load_inputs()
        self.load_views()


        print([key for key in self.inputs])
        print([key for key in self.bases])

        self.prolog.assertz("does(white,mark)")
        print(list(self.prolog.query("next(X)")))

        self.terminal = PropNetNode("terminal", False)

    def load_bases(self):
        self.bases = {}
        bases_query = list(self.prolog.query("base(X)"))
        for bases_result in bases_query:
            name = bases_result["X"]
            self.bases[name] = Term(name, len(list(self.prolog.query("init(" + name + ")"))) >= 1)

    def load_inputs(self):
        self.inputs = {}
        inputs_query = list(self.prolog.query("input(X)"))
        for input_result in inputs_query:
            name = input_result["X"]
            self.inputs[name] = Term(name, False)

    def load_views(self):
        pass


class PropNetHiddenInfo(PropNet):

    def __init__(self, description):
        super(PropNetHiddenInfo, self).__init__(description)
        self.unknowns = None