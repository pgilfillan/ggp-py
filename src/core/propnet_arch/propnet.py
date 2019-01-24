
class PropNet:

    #Needs roles, inputs, bases, views, legals, rewards, terminal
    def __init__(self, description):
        self.roles = None
        self.inputs = None
        self.bases = None
        self.views = None
        self.legals = None
        self.rewards = None
        self.terminal = None

class PropNetHiddenInfo:

    def __init__(self, description):
        super(PropNetHiddenInfo, self).__init__(description)
        self.unknowns = None