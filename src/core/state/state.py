
class State:

    def __init__(self, contents):
        self.contents = contents

class GDLII_State(State):
    
    def __init__(self, contents, percepts):
        super(GDLII_State, self).__init__(contents)
        self.percepts = percepts